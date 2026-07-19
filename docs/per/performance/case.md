# 营销活动压测面试案例 —— 移动云盘会员日活动

## 一、案例背景

某运营商开展“全网移动云盘会员日”营销活动，活动规则如下：

- **活动时间**：2025-07-15 至 2027-07-15（长期活动）
- **核心玩法**：会员日开启当天，用户可通过完成**拉新、拉活、AI工具试用**等任务获取抽奖次数或积分，用于抽奖或兑换奖品
- **约束条件**：奖品设有**库存限制**
- **数据统计周期**：当天

### 活动核心数据及术语说明

> **术语说明**：

**PV（Page View，页面浏览量）** 指活动页面被打开/刷新的总次数（用户每刷新一次即累计一次），反映页面被请求的总量；

**UV（Unique Visitor，独立访客）** 指访问页面的去重设备/用户数（同一用户多次访问仅计一次），用于衡量真实的用户覆盖规模。两者结合可计算人均浏览深度（PV/UV）及分析活动吸引力。

| 指标 | 数值 |
|------|------|
| PV | 1,315,078 |
| UV | 626,039 |
| 登陆用户数 | 469,431 |
| 登录转换率 | 74.98% |
| 中奖数 | 154,130 |
| 中奖率 | 32.83% |
| 中奖用户数 | 115,953 |
| 领奖数 | 78,024 |
| 领奖率 | 50.62% |

### 关键特征

- 任务**仅在每月会员日开启当天可做**
- 任务包括：拉新/拉活/指定活动停留浏览几秒/AI工具（如文生图）试用，跳转到对应活动h5，满足条件后获得抽奖次数。
  - **AI 工具试用流程**：用户跳转到 AI 服务 H5 页面 → 完成试用 → AI 服务通过http回调通知活动系统 → 活动系统轮询检查任务状态 → 发放抽奖次数（非同步调用,不会成为性能瓶颈）
- 流量时间分布高度偏斜（开启瞬间突增）
- 核心写接口集中在活动开启首日

## 二、技术风险分析

基于活动特性，识别以下六大风险：

| 序号 | 风险点 | 风险描述 | 严重等级 |
|:---|:---|:---|:---|
| 1 | **库存超卖/负数** | 使用"查库存→扣减"非原子操作，或缓存与DB不一致，导致奖品超发 | ⭐⭐⭐⭐⭐ |
| 2 | **重复领取/幂等性** | 网络超时导致用户重试，后端未做幂等校验，同一任务多次发放积分/奖品 | ⭐⭐⭐⭐ |
| 3 | **外部依赖故障** | 外部依赖响应超时（>3s），占满Tomcat线程池，导致级联故障 | ⭐⭐⭐⭐ |
| 4 | **缓存击穿/雪崩** | 热点奖品Key在Redis中失效，大量请求直接打到数据库 | ⭐⭐⭐ |
| 5 | **数据库行锁竞争** | 更新用户积分时无索引或锁等待超时，高并发下死锁率上升 | ⭐⭐⭐ |
| 6 | **日志/监控被冲垮** | 500 TPS下每个请求打印大量日志，撑爆磁盘IO和ES索引队列 | ⭐⭐ |

## 三、压测关键指标获取与计算

数据来源以APM（SkyWalking）埋点日志为主

#### 1. 数据来源及业务配比计算

遵循 **"历史基线 + 业务预期 + 漏斗转化"** 三层校准。

**数据来源权重建议**：

| 数据源 | 权重 | 理由 |
|:---|:---|:---|
| **APM 埋点日志** | 50-60% | 最精准，含实时调用量、RT、错误率 |
| **数据侧预测增长** | 20-30% | 业务侧对营销力度、用户增长有预判 |
| **漏斗转化衰减** | 10-20% | 修正压测脚本，确保符合业务逻辑 |

**团队协作职责边界**：

| 职责项 | 主要负责方 | 测试人员需掌握/行动 |
| :--- | :--- | :--- |
| SkyWalking 探针部署 | **开发/运维** | 提醒运维压测期间临时关闭或过滤探针，避免污染线上监控 |
| SkyWalking 数据提取 | **测试人员（自行动手）** | 登录 Dashboard 按接口维度导出调用量 CSV |
| 业务转化率（中奖率等） | **数据侧（BI/DBA）** | 主动提出统计口径（如按小时粒度），拿到数据后校准压测脚本 |
| Nginx 原始日志捞取 | **运维/基础架构组** | 掌握 Shell（awk/grep）自行分析，不依赖运维代劳 |

#### 2. 高峰期QPS、TPS、并发数计算

#### SkyWalking 提供的数据指标

| 原生指标 | 含义 | 获取路径 |
|:---|:---|:---|
| **CPM** | Calls Per Minute（每分钟调用数） | Dashboard → Service/Endpoint → CPM 折线图 |
| **响应时间** | P50/P75/P90/P95/P99 RT | Dashboard → Response Time 折线图 |
| **错误率** | Error Rate % | Dashboard → Error 折线图 |
| **SLA** | 成功率 % | Dashboard → SLA 折线图 |

#### 数据提取步骤

**步骤一：定位高峰时段**
```
1. Dashboard → Service Dashboard
2. 时间选活动当天全天
3. CPM 折线图峰值 → 鼠标悬停看具体时间（如 10:05）
```

**步骤二：放大高峰时段获取接口级数据**
```
1. 时间范围改为高峰时段（如 10:00-10:15）
2. Service → Endpoint List
3. 点击 Export → CSV（含各接口 CPM、P99 RT）
```

#### QPS/TPS/并发数计算

| 指标 | 计算公式 | 说明 |
|:---|:---|:---|
| **QPS** | CPM ÷ 60 | 读接口（GET）每秒查询数 |
| **TPS** | CPM ÷ 60 | 写接口（POST/PUT/DELETE）每秒事务数 |
| **并发数** | QPS × 平均响应时间（秒） | Little 定律：并发 = QPS × RT |

**计算示例（高峰时段 10:00-10:10）**：

| 接口 | CPM | P99 RT | QPS/TPS | 并发数 |
|:---|:---|:---|:---|:---|
| GET /api/user/info | 18,000 | 150ms | 300 QPS | 300×0.15 = 45 |
| POST /api/lottery/draw | 6,000 | 300ms | 100 TPS | 100×0.3 = 30 |
| POST /api/task/submit | 30,000 | 200ms | 500 TPS | 500×0.2 = 100 |
| **合计** | - | - | **900** | **175** |

#### 注意事项

- CPM 粒度为 1 分钟，高峰时段建议取多个点求平均
- 区分读写：GET → QPS，POST/PUT/DELETE → TPS
- 并发计算用平均值更准确，压测目标设定用 P99
- 如需按业务关键字筛选（如"会员日"），需提前埋 `ActiveSpan.tag("activity", "会员日")`

最终得出压测目标：
- 目标TPS：700-1000
- 实际达标TPS：850

## 四、JMeter 压测方案设计

### 4.1 策略总览

采用 **"梯度增压 + 混合场景"** 策略，模拟真实用户路径：登录 → 做任务 → 抽奖。

### 4.2 关键元件清单

#### （1）线程组（Thread Group）

| 元件 | 类型 | 用途 |
|:---|:---|:---|
| 梯度压测线程组 | `Concurrency Thread Group` 或 `Ultimate Thread Group` | 阶梯爬坡：100 → 300 → 500 → 700 → 1000 TPS，每阶段持续 5 分钟，逐步寻找系统拐点 |
| 预热线程组 | `setUp Thread Group` | 提前缓存登录态，预热系统 |

#### （2）配置元件（Config Elements）

| 元件 | 用途 |
|:---|:---|
| `CSV Data Set Config` | 准备50万测试用户数据（手机号+用户ID），模拟真实UV |
| `HTTP Cookie Manager` | 自动管理Session/Cookie，模拟浏览器会话保持 |
| `HTTP Request Defaults` | 统一设置域名、连接超时（3s）、响应超时（5s） |

#### （3）逻辑控制器（Logic Controllers）

| 元件 | 用途 |
|:---|:---|
| `Throughput Controller` | 控制流量配比：任务提交60% / 抽奖30% / 登录10%（依据：任务为核心业务且中奖率32.83%需衰减） |
| `If Controller` | 根据CSV中的 `task_type` 动态路由到"拉新""拉活"或"AI试用"采样器 |

#### （4）采样器与处理器（Samplers & Processors）

| 元件 | 用途 |
|:---|:---|
| `HTTP Request` | 分别配置登录、任务提交、抽奖三个接口 |
| `JSR223 PreProcessor`（关键） | 生成幂等Token（UUID+时间戳+UserID的MD5），放入Header `Idempotent-Key`，模拟防重提交 |
| `JSON Extractor`（后置） | 从登录响应提取 `accessToken`/`sessionId`，传递给后续请求 |
| `BeanShell PostProcessor` | 增强断言：解析返回JSON，若 `code=-1` 标记为业务失败；若库存字段<0则强制断言失败（检测超卖） |

#### （5）定时器（Timers）

| 元件 | 用途 |
|:---|:---|
| `Uniform Random Timer` | 请求间添加 100~300ms 随机思考时间，仿真真实用户操作间隙 |

#### （6）断言（Assertions）

| 元件 | 用途 |
|:---|:---|
| `Response Assertion` | 校验响应是否包含 `"success":true` |
| `Duration Assertion` | 核心接口RT ≤ 500ms，登录RT ≤ 1s，超过则标记失败 |

#### （7）监听器（Listeners）

| 元件 | 用途 |
|:---|:---|
| `Backend Listener` | 配置 InfluxDB + Grafana，实时监控TPS、RT百分位（P99）、错误率 |
| `Aggregate Report` / `Summary Report` | 保存 `.jtl` 结果文件，用于后期分析 |
| `Active Threads Over Time` | 直观查看并发线程与实际TPS的匹配关系 |

### 4.3 JMeter 测试计划树形结构

```
Test Plan（会员日活动压测）
│
├── setUp Thread Group（预热线程组）
│   ├── CSV Data Set Config（预热用户数据）
│   ├── HTTP Request（登录预热）
│   │   ├── JSON Extractor（提取 token）
│   │   └── Response Assertion（校验登录成功）
│   └── Uniform Random Timer（100-200ms）
│
├── Concurrency Thread Group（梯度压测线程组）
│   │
│   ├── 【配置元件】
│   │   ├── CSV Data Set Config
│   │   │   └── 文件：users.csv（50万测试用户）
│   │   ├── HTTP Cookie Manager（自动管理 Session）
│   │   └── HTTP Request Defaults
│   │       ├── 服务器：activity.xxx.com
│   │       ├── 连接超时：3000ms
│   │       └── 响应超时：5000ms
│   │
│   ├── 【登录场景】（10%流量）
│   │   ├── Throughput Controller（Percent Executions: 10%）
│   │   ├── HTTP Request（POST /api/login）
│   │   │   ├── JSR223 PreProcessor（生成幂等 Token）
│   │   │   ├── JSON Extractor（提取 accessToken）
│   │   │   ├── BeanShell PostProcessor（校验 code=0）
│   │   │   └── Duration Assertion（RT ≤ 1s）
│   │   └── Uniform Random Timer（200-500ms）
│   │
│   ├── 【做任务场景】（60%流量）
│   │   ├── Throughput Controller（Percent Executions: 60%）
│   │   │
│   │   ├── If Controller（${task_type} == "拉新"）
│   │   │   └── HTTP Request（POST /api/task/invite）
│   │   │       ├── JSR223 PreProcessor（生成 taskId）
│   │   │       ├── Response Assertion（校验 success=true）
│   │   │       └── Duration Assertion（RT ≤ 500ms）
│   │   │
│   │   ├── If Controller（${task_type} == "拉活"）
│   │   │   └── HTTP Request（POST /api/task/active）
│   │   │       ├── JSR223 PreProcessor（生成 taskId）
│   │   │       ├── Response Assertion（校验 success=true）
│   │   │       └── Duration Assertion（RT ≤ 500ms）
│   │   │
│   │   ├── If Controller（${task_type} == "AI试用"）
│   │   │   └── HTTP Request（POST /api/task/ai-trial）
│   │   │       ├── JSR223 PreProcessor（生成 taskId）
│   │   │       ├── Response Assertion（校验 success=true）
│   │   │       └── Duration Assertion（RT ≤ 500ms）
│   │   │
│   │   └── Uniform Random Timer（100-300ms）
│   │
│   ├── 【抽奖场景】（30%流量）
│   │   ├── Throughput Controller（Percent Executions: 30%）
│   │   ├── HTTP Request（POST /api/lottery/draw）
│   │   │   ├── JSR223 PreProcessor（生成幂等 Token）
│   │   │   ├── JSON Extractor（提取 prizeId）
│   │   │   ├── BeanShell PostProcessor（检测库存是否为负数）
│   │   │   ├── Response Assertion（校验 success=true）
│   │   │   └── Duration Assertion（RT ≤ 500ms）
│   │   └── Uniform Random Timer（150-350ms）
│   │
│   └── 【监听器】
│       ├── Backend Listener（InfluxDB + Grafana）
│       │   ├── influxdbUrl: http://influxdb:8086
│       │   ├── application: member_day_activity
│       │   └── measurement: jmeter_results
│       ├── Aggregate Report（保存 jtl 文件）
│       └── Active Threads Over Time（实时监控并发）
│
└── tearDown Thread Group（清理线程组）
    └── Debug Sampler（输出测试结果摘要）
```

**关键节点说明**：

| 节点层级 | 作用 | 备注 |
|:---|:---|:---|
| **Test Plan** | 测试计划根节点 | 定义全局配置（用户变量、类路径） |
| **Thread Group** | 并发控制核心 | 梯度增压：100→300→500→700→1000 TPS |
| **Throughput Controller** | 流量分配 | 按业务配比控制场景权重 |
| **If Controller** | 动态路由 | 根据参数路由到不同任务类型 |
| **PreProcessor** | 前置处理 | 生成幂等 Token、签名等 |
| **PostProcessor** | 后置处理 | 提取变量、增强断言 |
| **Assertion** | 结果校验 | 响应码、响应时间、业务逻辑 |

**压测执行流程**：

```
1. setUp Thread Group 预热（100 线程）
   └─→ 登录系统，缓存热点数据

2. Concurrency Thread Group 梯度加压
   ├─→ 阶段一：100 线程，持续 5 分钟
   ├─→ 阶段二：300 线程，持续 5 分钟
   ├─→ 阶段三：500 线程，持续 5 分钟
   ├─→ 阶段四：700 线程，持续 5 分钟
   └─→ 阶段五：1000 线程，持续 10 分钟

3. Backend Listener 实时监控
   └─→ InfluxDB 收集指标 → Grafana 展示曲线

4. tearDown Thread Group 清理
   └─→ 输出测试摘要，生成报告
```

### 4.4 针对特定风险的压测执行方案

| 风险点 | JMeter 针对性策略 |
|:---|:---|
| **超卖（库存扣减）** | 使用 `Synchronizing Timer`，设定50线程同时释放（瞬间集合点），模拟50人同时抢最后一个库存，观察是否返回负数 |
| **AI接口超时阻塞** | HTTP Request单独设置连接超时1s/响应超时2s，配合 `Constant Throughput Timer` 在错误率>5%时强制降级 |
| **缓存穿透/DB压力** | 固定热点奖品ID，清除Redis缓存后并发压测，观察DB的QPS和连接数飙升情况 |
| **日志风暴** | 压测期间禁用 `View Results Tree`，仅依赖 `Simple Data Writer` 落盘，避免压测机自身成为瓶颈 |

### 4.5 补充方案：基于 Locust 的全链路压测

> **为什么需要 Locust？** JMeter 适合标准化压测，但对于**复杂业务逻辑**（如动态签名、加密参数、多步骤依赖），Python 编写更灵活。

#### 4.5.1 Locust vs JMeter 对比

| 维度 | JMeter | Locust |
|:---|:---|:---|
| **编写语言** | Java/Groovy（GUI 配置为主） | Python（代码为主，更灵活） |
| **脚本维护** | XML 配置，可读性差 | Python 代码，易维护、易版本控制 |
| **复杂逻辑** | BeanShell/Groovy 脚本，调试困难 | 原生 Python，支持断点、IDE 调试 |
| **分布式压测** | Master-Slave 模式（需配置） | Master-Worker 模式（一条命令启动） |
| **资源消耗** | 每个 VU 约 1MB 堆内存 | 每个 VU 约 几十 KB（轻量级协程） |
| **实时监控** | 需配置 Backend Listener | 自带 Web UI，实时展示曲线 |
| **扩展性** | 插件机制，Java 生态 | Python 生态，集成第三方库容易 |
| **适用场景** | 标准化压测、团队协作、合规审计 | 复杂业务逻辑、快速迭代、技术团队 |

**Locust 核心优势**：
- **轻量级**：基于协程（gevent），单机可支持数万并发
- **灵活**：Python 代码编写，支持复杂业务逻辑（如加密、签名）
- **易扩展**：可直接调用第三方库（如 requests、PyCryptodome）
- **实时监控**：Web UI 实时展示 TPS、RT、错误率曲线

#### 4.5.2 Locust 压测脚本示例

**场景**：会员日活动全链路压测（登录 → 做任务 → 抽奖）

```python
# locustfile.py
from locust import HttpUser, task, between, events
import json
import hashlib
import time
from random import randint, choice

class MemberDayUser(HttpUser):
    """
    会员日活动用户行为模拟
    业务流程：登录 → 做任务 → 抽奖 → 查领奖记录
    """
    wait_time = between(1, 3)  # 请求间等待 1-3 秒

    def on_start(self):
        """初始化：模拟登录获取 token"""
        self.phone = f"13800{randint(100000, 999999)}"
        self.user_id = None
        self.access_token = None
        self.prize_ids = []

        # 登录接口
        self.login()

    def login(self):
        """登录接口"""
        payload = {
            "phone": self.phone,
            "deviceId": f"device_{randint(1000, 9999)}"
        }

        with self.client.post("/api/login", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0:
                    self.access_token = data["data"]["accessToken"]
                    self.user_id = data["data"]["userId"]
                    response.success()
                else:
                    response.failure(f"登录失败: {data.get('msg')}")
            else:
                response.failure(f"HTTP {response.status_code}")

    def generate_idempotent_token(self):
        """生成幂等 Token（MD5）"""
        timestamp = int(time.time() * 1000)
        raw = f"{self.user_id}_{timestamp}_{randint(1000, 9999)}"
        return hashlib.md5(raw.encode()).hexdigest()

    @task(10)
    def do_task_invite(self):
        """任务1：拉新（权重10）"""
        if not self.access_token:
            return

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Idempotent-Key": self.generate_idempotent_token()
        }

        payload = {
            "taskId": f"task_{randint(10000, 99999)}",
            "taskType": "invite",
            "inviteCode": f"CODE{randint(1000, 9999)}"
        }

        with self.client.post("/api/task/submit", json=payload, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    response.success()
                else:
                    response.failure(f"任务提交失败: {data.get('msg')}")
            else:
                response.failure(f"HTTP {response.status_code}")

    @task(6)
    def do_task_ai_trial(self):
        """任务2：AI 工具试用（权重6）"""
        if not self.access_token:
            return

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Idempotent-Key": self.generate_idempotent_token()
        }

        payload = {
            "taskId": f"task_{randint(10000, 99999)}",
            "taskType": "ai_trial",
            "aiTool": choice(["text2img", "img2img", "ocr"])
        }

        with self.client.post("/api/task/submit", json=payload, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    response.success()
                else:
                    response.failure(f"AI 试用失败: {data.get('msg')}")
            else:
                response.failure(f"HTTP {response.status_code}")

    @task(3)
    def lottery_draw(self):
        """抽奖（权重3）"""
        if not self.access_token:
            return

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Idempotent-Key": self.generate_idempotent_token()
        }

        payload = {
            "lotteryId": f"lottery_{randint(10000, 99999)}",
            "activityId": "member_day_2025"
        }

        with self.client.post("/api/lottery/draw", json=payload, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    prize_id = data["data"].get("prizeId")
                    if prize_id:
                        self.prize_ids.append(prize_id)
                    response.success()
                else:
                    response.failure(f"抽奖失败: {data.get('msg')}")
            else:
                response.failure(f"HTTP {response.status_code}")

    @task(2)
    def get_lottery_history(self):
        """查领奖记录（权重2）"""
        if not self.access_token or not self.prize_ids:
            return

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        with self.client.get("/api/lottery/history", headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    response.success()
                else:
                    response.failure(f"查询失败: {data.get('msg')}")
            else:
                response.failure(f"HTTP {response.status_code}")

# 自定义事件监听：实时统计业务指标
@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """每个请求完成后触发"""
    if exception:
        print(f"请求失败: {name}, 错误: {exception}")
    else:
        # 可扩展：将数据推送到 InfluxDB
        pass
```

**关键设计说明**：

1. **任务权重**：`@task(10)` 表示拉新任务权重为 10，抽奖权重为 3，流量配比约为 10:3
2. **幂等 Token**：每个写接口都生成唯一的幂等 Token，防止重复提交
3. **动态令牌管理**：登录后自动提取 `accessToken`，后续请求自动携带
4. **业务逻辑验证**：`catch_response=True` 允许自定义成功/失败判断逻辑
5. **链式依赖**：抽奖成功后记录 `prizeId`，用于后续"查领奖记录"场景

#### 4.5.3 分布式压测与监控

**启动 Master 节点**：
```bash
# 启动 Web UI（默认 http://localhost:8089）
locust -f locustfile.py --master

# 指定并发数和增长率（命令行模式）
locust -f locustfile.py --master -u 1000 -r 100 -t 30m
# -u: 总用户数 1000
# -r: 每秒启动用户数 100
# -t: 持续时间 30 分钟
```

**启动 Worker 节点**（多台压测机）：
```bash
# Worker 1
locust -f locustfile.py --worker --master-host=192.168.1.100

# Worker 2
locust -f locustfile.py --worker --master-host=192.168.1.100

# Worker 3
locust -f locustfile.py --worker --master-host=192.168.1.100
```

**实时监控（Web UI）**：
- **Total RPS**：总请求数/秒
- **Total Failures/s**：失败请求数/秒
- **Response Time (ms)**：平均响应时间
- **Active Users**：当前活跃用户数

**导出报告**：
```bash
# 导出 CSV 格式结果
locust -f locustfile.py --headless -u 1000 -r 100 -t 30m --csv=member_day_test

# 生成文件：
# - member_day_test_stats.csv（统计结果）
# - member_day_test_stats_history.csv（历史数据）
# - member_day_test_failures.csv（失败记录）
```

#### 4.5.4 Locust 高级特性

**1. 自定义负载形状（阶梯加压）**：
```python
from locust import LoadTestShape

class StagesLoadShape(LoadTestShape):
    """阶梯加压：100 → 300 → 500 → 700 → 1000 TPS"""
    # Web UI 无duration参数
    stages = [
        {"duration": 300, "users": 100, "spawn_rate": 10},   # 5 分钟，100 用户
        {"duration": 600, "users": 300, "spawn_rate": 20},   # 10 分钟，300 用户
        {"duration": 900, "users": 500, "spawn_rate": 30},   # 15 分钟，500 用户
        {"duration": 1200, "users": 700, "spawn_rate": 40},  # 20 分钟，700 用户
        {"duration": 1800, "users": 1000, "spawn_rate": 50}, # 30 分钟，1000 用户
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return (stage["users"], stage["spawn_rate"])

        return None  # 结束压测

# 使用自定义负载形状
locust -f locustfile.py --headless --class-shape=StagesLoadShape
```

**2. 集成 InfluxDB + Grafana 实时监控**：
```python
from locust import events
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB 配置
client = InfluxDBClient(url="http://localhost:8086", token="my-token")
write_api = client.write_api(write_options=SYNCHRONOUS)

@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """每个请求推送到 InfluxDB"""
    point = Point("locust_requests") \
        .tag("request_type", request_type) \
        .tag("name", name) \
        .field("response_time", response_time) \
        .field("response_length", response_length) \
        .field("success", 1 if not exception else 0)

    write_api.write(bucket="locust", record=point)
```

**3. 复杂业务逻辑（加密参数）**：
```python
from Crypto.Cipher import AES
import base64

class EncryptedUser(HttpUser):
    """需要加密参数的接口"""

    def encrypt_params(self, data):
        """AES 加密"""
        key = b"16bytesecretkey!!"
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted = cipher.encrypt(data.encode().ljust(32))
        return base64.b64encode(encrypted).decode()

    @task
    def encrypted_request(self):
        """加密请求"""
        raw_data = json.dumps({"userId": self.user_id, "timestamp": time.time()})
        encrypted_data = self.encrypt_params(raw_data)

        self.client.post("/api/encrypted", json={"data": encrypted_data})
```

#### 4.5.5 面试对比：JMeter vs Locust

**面试官可能追问**："你为什么选择 Locust 而不是 JMeter？两者的优劣是什么？"

**回答策略**：

> "我们项目中同时使用了 JMeter 和 Locust，各有优势：
>
> **JMeter 适合标准化压测**：
> - 团队协作友好：GUI 配置，非技术人员也能操作
> - 合规审计：JMX 文件可直接作为测试用例存档
> - 生态成熟：大量插件、文档、培训资料
>
> **Locust 适合复杂业务逻辑**：
> - **加密参数**：本次压测的登录接口需要 AES 加密，Locust 直接调用 PyCryptodome 库，JMeter 需要写 BeanShell 脚本，调试困难
> - **动态签名**：每个请求需要根据时间戳和用户 ID 生成签名，Python 代码一目了然
> - **链式依赖**：抽奖成功后才能查领奖记录，Locust 的 `on_start` 和任务权重机制天然支持
> - **轻量级**：单机支持数万并发，JMeter 单机安全上限约 1500-2000 线程
>
> **我的建议**：
> - 如果是**标准化接口压测**（如 REST API、数据库、MQ），优先 JMeter
> - 如果是**复杂业务逻辑压测**（如加密、签名、多步骤依赖），优先 Locust
> - 如果是**全链路压测**（包括前端、网关、后端），可以组合使用：JMeter 压测标准接口，Locust 压测复杂逻辑"

**加分项**：

> "我在项目中还遇到了一个 JMeter 难以解决的问题：**动态令牌管理**。每次请求需要从上一个接口的响应中提取变量，JMeter 的 JSON Extractor 虽然能实现，但配置复杂且难以调试。而 Locust 直接用 Python 代码解析 JSON，一行代码就能搞定：
>
> ```python
> data = response.json()
> self.access_token = data["data"]["accessToken"]
> ```
>
> 这让我深刻体会到：**工具选择没有绝对优劣，关键是根据场景选择最合适的工具**。"


## 五、面试追问高频题与深度答疑

### Q1：压测链路业务配比，当只有elk+nginx时，如何获取？

> **面试官考察点**：在没有 APM 的情况下，是否具备从基础日志中提取压测数据的能力。

**（一）Nginx 日志提取接口 PV 分布**

当没有 APM 时，Nginx access.log 是最基础的数据来源。

**基础命令**：
```bash
cat access.log | awk '{print $7}' | sort | uniq -c | sort -rn | head -20
```

**生产级优化**（面试加分点）：
```bash
# 1. 过滤静态资源，只看业务接口
cat access.log | grep -v -E '\.(css|js|png|jpg|gif|ico)$' \
  | awk '{print $7}' | sort | uniq -c | sort -rn | head -20

# 2. 按高峰时段切片（如活动开启后10分钟）
grep "15/Jul/2025:10:0[0-9]" access.log \
  | awk '{print $7}' | sort | uniq -c | sort -rn | head -20

# 3. 统计各接口 QPS（按分钟粒度）
grep "15/Jul/2025:10:0[0-9]" access.log \
  | awk '{print $4, $7}' | awk -F: '{print $2":"$3}' \
  | uniq -c | awk '{print $1/60, $2}'  # 每分钟调用量 ÷ 60 = QPS
```

**推荐工具**：
- **GoAccess**：实时分析 Nginx 日志，生成 HTML 报告，直接看接口 PV 排名
- **ELK/Kibana**：将 Nginx 日志导入 ES，用 Kibana Visualize 做接口调用量折线图

**（二）ELK 提取业务转化率**

ELK 存储的是应用日志（如业务日志、错误日志），可用于提取转化率。

**典型查询（Kibana Discover）**：
```
# 查询中奖日志
message: "lottery_success" AND activity: "会员日"

# 统计中奖次数
activity: "会员日" AND message: "lottery_success" | count()

# 计算中奖率
中奖次数 / 抽奖请求次数（需两条查询合并）
```

**注意**：ELK 查业务转化率的前提是**应用日志中有业务埋点**（如中奖、领奖的日志输出）。如果没有业务埋点，则需从业务数据库/数据仓库获取。

**（三）业务配比计算流程（ELK + Nginx 组合）**

```
1. Nginx 日志 → 各接口 PV 比例（如登录 10%、任务提交 60%、抽奖 30%）
2. ELK 日志 → 业务转化率（如中奖率 32.83%、领奖率 50.62%）
3. 业务数据库 → 用户漏斗数据（如登录转化率、任务完成率）
4. 三者结合 → 校准压测脚本的业务配比
```

**（四）局限性对比**

| 数据源 | 优势 | 局限 |
|:---|:---|:---|
| **Nginx 日志** | 有 PV/QPS，无需额外部署 | 无响应时间、无业务转化率 |
| **ELK 日志** | 可查业务埋点、错误堆栈 | 需应用埋点，无调用链路 |
| **APM** | 有调用链路、RT、错误率 | 需部署探针，有学习成本 |

**面试金句**：
> "当只有 Nginx + ELK 时，我会先用 Shell 命令或 GoAccess 从 Nginx 日志提取接口 PV 分布，再用 ELK 查业务埋点日志获取转化率。虽然没有 APM 的链路追踪，但组合使用仍能得到合理的压测配比。如果条件允许，我会建议团队引入 SkyWalking 等轻量级 APM。"

---

通过nginx日志统计接口访问量

```shell
cat access.log | awk '{print $7}' | sort | uniq -c | sort -rn | head -20
# 命令含义：awk '{print $7}' 提取URI路径 → sort排序 → uniq -c统计次数 → sort -rn降序 → head -20取Top20。
```

“Nginx日志法仅适用于宏观PV总量和接口热点排序，但无法支撑压测配比决策，因为：

1.无法关联用户行为漏斗（不知道这15万次抽奖是由多少‘登录用户’发起的，也无法知道‘任务完成数’）。

2.无法剔除静态资源/爬虫/健康检查（K8s的/actuator/health探针会污染统计）。

3.实时性差（离线分析，无法动态调整压测模型）。”


### Q2：如何评估并发用户数？压测机台数怎么算？（QPS=1万，RT=500ms）

> **面试官考察点**：是否掌握 **Little定律** 和施压机性能瓶颈。

**第一步：计算总并发线程数（VU）**

- **Little定律**：并发用户数 = QPS × 平均响应时间（秒）
- 代入：10,000 QPS × 0.5s = **5,000 并发线程（VU）**

**第二步：计算所需压测机台数**

**单台施压机上限认知**：

- JMeter每个线程（VU）默认占用约 **1MB 堆内存**
- 8C16G施压机，分配 `-Xmx12G`，理论上限 12,000 线程
- **生产经验值**：单台安全并发控制在 **1,500 ~ 2,000 VU**（超过则GC频繁，数据失真）

**计算公式**：

- 所需台数 = 5,000 ÷ 1,500 ≈ **3.3 台**
- **最终建议**：准备 **4台施压机**（3主力 + 1冗余），确保施压机带宽 > 被压机带宽

### Q3：压测时 TPS 上不去但 CPU/内存不高的排查方向？Arthas 何时上场？

> **面试官考察点**：区分"业务处理慢"与"网络/中间件/OS限制"的能力，以及是否会使用高级动态诊断工具。

**核心结论**：TPS上不去但CPU/内存空闲 → **瓶颈不在应用计算或堆内存，而是卡在"IO等待"或"外部协调"**。

**（一）基础排查方向（按优先级）**：

| 优先级 | 排查方向 | 具体方法 |
|:---|:---|:---|
| 1 | **数据库/Redis连接池** | 查看 `DataSource` 活跃连接数是否等于 `maximumPoolSize`，大量线程在等待连接 |
| 2 | **下游依赖超时（AI/第三方）** | 检查调用第三方接口的响应超时配置，线程堆栈是否有大量 `SocketTimeout` |
| 3 | **网卡带宽打满** | 用 `iftop`/`nload` 查看网卡流量是否达到内网限速（如1Gbps） |
| 4 | **OS内核限制** | 检查 `net.ipv4.ip_local_port_range`（默认3万）是否耗尽，`TIME_WAIT` 堆积 |
| 5 | **分布式锁竞争** | 抽奖扣库存用 `Redisson` 或 `select...for update`，大量线程在自旋等待锁释放 |
| 6 | **GC停顿** | 查看GC日志，检查是否频繁发生STW（虽然CPU不高，G1的Concurrent Mark阶段偶发） |

**（二）高级武器——Arthas（在线动态诊断，无需重启）**

当 `jstack` 只能看到线程状态但无法定位深层原因时，**Arthas 是冲击高分的关键**。以下是3个杀手级场景：

| 场景 | Arthas 命令 | 实战效果 |
| :--- | :--- | :--- |
| **定位外部接口超时根因** | `trace com.xxx.TaskService submitTask` | 动态打印方法内**每一步**的精确耗时。若发现 900ms 耗费在 `HttpClient.execute()`，而业务代码仅用 1ms → **秒级定位网络IO超时**。 |
| **线上临时开启 DEBUG 日志** | `logger --name ROOT --level debug` | 怀疑分布式锁 `tryLock` 在空转，但线上 INFO 级别看不到。实时改为 DEBUG 观察等待时间，验证完再改回，**免重启**。 |
| **反编译验证线上代码版本** | `jad --source-only com.xxx.StockService` | 怀疑部署包不是最新代码。直接反编译 JVM 内存中的字节码，若发现确实缺少判空逻辑 → **实锤截图，终结扯皮**。 |

**面试金句**：
> “当 `top -H` 和 `jstack` 看不出明显锁等待时，我会果断上 **Arthas 的 `watch` 命令**，监控扣库存方法的入参和返回值，观察 `remainingStock` 是否在临界值异常归零。Arthas 让我能在不停服的情况下完成‘手术刀式’的精准诊断。”

### Q4:压测有没有遇到什么瓶颈,做了什么优化?

> **面试官考察点**:是否具备真实的压测实战经验,以及从发现问题到解决问题的完整闭环能力。

**核心结论**:压测过程中确实遇到了多个瓶颈,主要集中在**数据库连接池耗尽、缓存穿透导致DB压力、分布式锁竞争加剧**三个方面。

#### (一)瓶颈一:数据库连接池耗尽

**问题现象**:
- 压测到500 TPS时,错误率突然飙升至15%
- 应用日志大量报错:`HikariPool-1 - Connection is not available, request timed out after 30000ms`
- 通过 `jstack` 发现大量线程处于 `WAITING` 状态,堆栈显示在 `HikariPool.getConnection`

**根因分析**:
- HikariCP默认配置 `maximumPoolSize=10`,远低于实际需求
- 每个抽奖请求涉及多表操作(用户积分扣减、库存扣减、中奖记录写入),平均耗时200ms
- 500 TPS下,理论连接需求 = 500 × 0.2 = 100个连接

**优化方案**:
```yaml
# HikariCP 配置调整
spring:
  datasource:
    hikari:
      maximum-pool-size: 100        # 从10调整为100
      minimum-idle: 20              # 最小空闲连接数
      connection-timeout: 10000     # 连接超时从30s改为10s
      idle-timeout: 600000          # 空闲连接超时10分钟
      max-lifetime: 1800000         # 连接最大存活30分钟
```

**优化效果**:
- 错误率从15%降至0.02%
- 连接池利用率从95%降至60%
- 支持TPS从500提升到850

---

#### (二)瓶颈二:热点奖品缓存穿透导致DB压力激增

**问题现象**:
- 压测300 TPS持续10分钟后,数据库CPU飙升至85%
- DB连接数从50增至200,慢查询日志出现大量 `SELECT * FROM prize_stock WHERE prize_id = 100`
- Redis命中率从95%降至60%

**根因分析**:
- 热点奖品ID(如iPhone、现金红包)被大量并发请求
- Redis中的库存Key设置TTL=10分钟,压测期间频繁过期导致缓存穿透
- 缓存失效瞬间,大量请求直接查询数据库,形成"缓存雪崩"

**优化方案**:

**方案一:热点Key永不过期 + 异步刷新**
```java
// 伪代码:热点奖品库存Key永不过期
public void initHotPrizeCache() {
    String key = "prize_stock:" + hotPrizeId;
    redisTemplate.opsForValue().set(key, stock, Duration.ofDays(30)); // 设置长TTL

    // 启动后台线程定时刷新库存
    scheduledExecutor.scheduleAtFixedRate(() -> {
        Integer dbStock = stockDao.selectById(hotPrizeId);
        redisTemplate.opsForValue().set(key, dbStock);
    }, 0, 5, TimeUnit.MINUTES); // 每5分钟从DB同步
}
```

**方案二:使用Redis分布式锁防止缓存击穿**
```java
// 双重检查锁 + 缓存重建
public Integer getPrizeStock(Long prizeId) {
    String key = "prize_stock:" + prizeId;
    Integer stock = (Integer) redisTemplate.opsForValue().get(key);

    if (stock == null) {
        // 加分布式锁防止多个线程同时重建缓存
        String lockKey = "lock:prize_stock:" + prizeId;
        RLock lock = redissonClient.getLock(lockKey);
        try {
            if (lock.tryLock(5, 10, TimeUnit.SECONDS)) {
                // 再次检查缓存(双重检查)
                stock = (Integer) redisTemplate.opsForValue().get(key);
                if (stock == null) {
                    stock = stockDao.selectById(prizeId);
                    redisTemplate.opsForValue().set(key, stock, Duration.ofMinutes(10));
                }
            }
        } finally {
            lock.unlock();
        }
    }
    return stock;
}
```

**优化效果**:
- Redis命中率从60%回升至95%
- DB CPU从85%降至35%
- DB连接数稳定在80左右

---

#### (三)瓶颈三:分布式锁竞争导致响应时间抖动

**问题现象**:
- 压测600 TPS时,P99 RT合格(480ms),但P999 RT飙升至3.5秒
- Grafana监控显示抽奖接口RT出现明显毛刺
- 日志中出现 `Redisson tryLock timeout` 警告

**根因分析**:
- 抽奖扣库存使用 `Redisson.tryLock()`,高并发下大量线程在自旋等待锁释放
- 锁持有时间过长(平均150ms),导致锁等待队列堆积
- Redis单节点锁在600 TPS下成为瓶颈

**优化方案**:

**方案一:锁粒度优化——从全局锁改为分段锁**
```java
// 原方案:全局锁(所有奖品共用)
String lockKey = "lock:lottery_draw";

// 优化方案:分段锁(按奖品ID分锁)
String lockKey = "lock:lottery_draw:" + prizeId;

// 进一步优化:按奖品ID + 用户ID分锁(防止同一用户重复中奖)
String lockKey = "lock:lottery_draw:" + prizeId + ":" + userId;
```

**方案二:锁持有时间压缩——原子操作替代锁**
```java
// 原方案:先查库存,再加锁扣减
Integer stock = getStock(prizeId);
if (stock > 0) {
    lock.lock();
    try {
        stockDao.decrementStock(prizeId);
    } finally {
        lock.unlock();
    }
}

// 优化方案:Redis Lua脚本原子扣减(无需分布式锁)
String script = "local stock = redis.call('GET', KEYS[1]) " +
                "if tonumber(stock) > 0 then " +
                "    redis.call('DECR', KEYS[1]) " +
                "    return 1 " +
                "else return 0 end";
Long result = redisTemplate.execute(new DefaultRedisScript<>(script, Long.class),
                                    Arrays.asList("prize_stock:" + prizeId));
if (result == 1) {
    // 扣减成功,异步写入DB
    asyncStockDao.decrementStock(prizeId);
}
```

**方案三:引入队列削峰**
```java
// 高并发场景:抽奖请求先入队,异步处理
@RestController
public class LotteryController {
    @Autowired
    private RabbitMQProducer producer;

    @PostMapping("/lottery/draw")
    public Result draw(@RequestBody LotteryRequest req) {
        // 快速入队响应
        producer.send("lottery_queue", req);
        return Result.success("抽奖请求已提交,请稍后查看结果");
    }
}

// 后台消费者批量处理
@Consumer(queueName = "lottery_queue")
public void consume(List<LotteryRequest> requests) {
    // 批量扣减库存,减少锁竞争
    stockDao.batchDecrementStock(extractPrizeIds(requests));
}
```

**优化效果**:
- P999 RT从3.5秒降至600ms
- 锁等待超时错误从20%降至0
- 支持TPS从600提升到850

---

#### (四)瓶颈四:活动奖品配置大 Key 导致抽奖接口响应慢

**问题现象**:
- 压测"抽奖"环节时,接口 P95 RT 从 200ms 升至 1.2s
- Redis 内存占用持续上涨,突破 80%
- 通过 `redis-cli --bigkeys` 发现 Key `activity:prizes:2025` 大小约 1.5MB
- 用 `redis-cli --stat` 观察到,每次抽奖查询该 Key 时,内网带宽出现 120Mbps 流量尖峰

**根因分析**:
- **业务场景**:活动有多个奖品(iPhone、现金红包、会员权益、积分等),每个奖品包含:
  - 基础信息:名称、图片URL、描述、价值
  - 库存信息:总库存、剩余库存、已发放数量
  - 限制规则:每人限领次数、用户等级限制、地域限制
  - 展示配置:排序权重、标签、活动时间
- **错误设计**:开发将所有奖品的完整配置存成单个 String Key:
  ```
  Key: activity:prizes:2025
  Value: {
    "prizes": [
      {"id":1,"name":"iPhone","img":"http://...","stock":100,"rules":{...}},
      {"id":2,"name":"现金红包","img":"http://...","stock":5000,"rules":{...}},
      ... // 共 20+ 个奖品,总计 1.5MB
    ]
  }
  ```
- **性能瓶颈**:
  - 每次抽奖都查询 1.5MB 配置数据(实际只需读取库存字段)
  - 单次 GET 操作耗时 150ms+(Redis 序列化 + 网络传输)
  - 高并发下占用大量带宽和 CPU,导致 Redis 响应变慢
  - 影响其他依赖 Redis 的接口(如用户信息查询)

**排查手段**:
```bash
# 1. 使用 bigkeys 扫描大 Key
redis-cli --bigkeys -i 0.1

# 2. 实时监控网络流量(观察到流量尖峰)
redis-cli --stat

# 3. 查看大 Key 具体内容
redis-cli --raw GET "activity:prizes:2025" | wc -c  # 查看字节数
```

**优化方案**:

**方案一:数据结构重构——按奖品拆分 Key**
```java
// 原方案:所有奖品配置存成单个 String(错误)
String key = "activity:prizes:2025";
String allPrizesJson = redisTemplate.opsForValue().get(key); // 1.5MB

// 优化方案:每个奖品独立 Key
String key = "activity:prize:" + prizeId;
Prize prize = (Prize) redisTemplate.opsForValue().get(key); // <10KB

// 初始化时批量写入
public void initPrizeCache() {
    for (Prize prize : prizeList) {
        String key = "activity:prize:" + prize.getId();
        redisTemplate.opsForValue().set(key, prize, 7, TimeUnit.DAYS);
    }
}
```

**方案二:库存与配置分离——核心数据独立缓存**
```java
// 将高频访问的库存数据独立存储
// Key 1: 库存信息(高频读写)
String stockKey = "activity:prize:stock:" + prizeId;
redisTemplate.opsForValue().set(stockKey, stock, 7, TimeUnit.DAYS);

// Key 2: 配置信息(低频只读)
String configKey = "activity:prize:config:" + prizeId;
redisTemplate.opsForValue().set(configKey, config, 7, TimeUnit.DAYS);

// 抽奖时只查询库存(几 KB)
Integer stock = (Integer) redisTemplate.opsForValue().get(stockKey);
```

**方案三:本地缓存热点奖品配置**
```java
// 使用 Caffeine 缓存热点奖品配置(如 iPhone、现金红包)
private Cache<Long, Prize> prizeCache = Caffeine.newBuilder()
    .maximumSize(20) // 缓存热点奖品
    .expireAfterWrite(10, TimeUnit.MINUTES)
    .build();

public Prize getPrize(Long prizeId) {
    // 先查本地缓存
    Prize prize = prizeCache.getIfPresent(prizeId);
    if (prize != null) {
        return prize;
    }

    // 本地未命中,查 Redis
    String key = "activity:prize:" + prizeId;
    prize = (Prize) redisTemplate.opsForValue().get(key);
    if (prize != null) {
        prizeCache.put(prizeId, prize);
    }
    return prize;
}
```

**方案四:Redis Hash 结构——按字段拆分(适合部分更新场景)**
```java
// 使用 Hash 结构存储奖品信息,按字段拆分
String key = "activity:prize:" + prizeId;
redisTemplate.opsForHash().put(key, "name", "iPhone");
redisTemplate.opsForHash().put(key, "stock", "100");
redisTemplate.opsForHash().put(key, "config", configJson);

// 只获取库存字段(HGET 传输量极小)
Integer stock = (Integer) redisTemplate.opsForHash().get(key, "stock");
```

**优化效果**:
- Redis 内存占用从 80% 降至稳定水位 45%
- "抽奖"接口 P95 RT 从 1.2s 降至 180ms
- 单次查询 Redis 数据量从 1.5MB 降至 <10KB
- Redis 缓存命中率保持 95% 以上

**面试对比分析：大 Key 问题 vs 缓存击穿**

> **面试官可能追问**："你刚才说大 Key 导致性能问题，那和缓存击穿有什么区别？在实际项目中如何区分？"

| 维度 | 大 Key 问题 | 缓存击穿（缓存未命中） |
|:---|:---|:---|
| **问题本质** | Redis Key 存在，但 Value 过大（1MB+） | Redis Key 不存在或失效，大量请求穿透到 DB |
| **典型场景** | 将多个实体的完整信息存成单个 Key（如所有奖品配置） | 键名拼接错误、缓存过期、缓存被意外删除 |
| **问题表现** | Redis 响应变慢、内存占用高、网络带宽打满 | 数据库 QPS 飙升、连接池耗尽、慢查询增多 |
| **排查手段** | `redis-cli --bigkeys` 扫描大 Key<br>`redis-cli --stat` 观察网络流量尖峰 | 检查应用日志是否有缓存未命中日志<br>对比 Redis Key 和业务代码中的键名拼接逻辑 |
| **根因定位** | 业务代码设计问题（将多个实体存成单个 Key） | 键名拼接逻辑错误（如奖品编码写错） |
| **优化方案** | 数据结构重构（String 改 Hash/拆分 Key）<br>本地缓存热点数据 | 修复键名拼接逻辑<br>增加缓存预热<br>增加分布式锁防止并发重建 |

**实际案例对比**：

**案例一：大 Key 问题（本次压测）**
```bash
# 问题：所有奖品配置存成单个 Key，大小 1.5MB
Key: activity:prizes:2025
Value: {"prizes":[{...},{...}]} // 1.5MB

# 排查：通过 bigkeys 发现
$ redis-cli --bigkeys
[found] "activity:prizes:2025" with 1572864 bytes

# 优化：按奖品拆分 Key
Key: activity:prize:1
Value: {"name":"iPhone","stock":100} // <10KB
```

**案例二：缓存击穿（历史项目）**
```bash
# 问题：奖品编码拼接错误，导致缓存 Key 不存在
业务代码：String key = "activity:prize:" + prizeCode; // prizeCode="iPhone15"
实际缓存：activity:prize:iPhone-15-pro-max  // 缓存中是"iPhone-15-pro-max"

# 排查：对比 Redis Key 和业务代码
$ redis-cli KEYS "activity:prize:*"
1) "activity:prize:iPhone-15-pro-max"
2) "activity:prize:现金红包"

# 应用日志显示：
[WARN] Cache miss for key: activity:prize:iPhone15

# 优化：修复键名拼接逻辑
String key = "activity:prize:" + prizeCode.replace("-", ""); // 去掉横杠
```

**面试金句**：
> "大 Key 和缓存击穿虽然都会导致性能问题，但根因和排查思路完全不同。大 Key 是'有缓存但太大'，缓存击穿是'没有缓存或缓存失效'。我在项目中先用 `redis-cli --bigkeys` 和 `--stat` 排除大 Key 问题，再检查应用日志和 Redis Key 列表定位缓存击穿。这两个问题都需要在代码 Review 阶段预防，而不是等压测才发现。"

---

#### (五)瓶颈五:同步调用积分系统导致任务提交和抽奖接口超时

**问题现象**:
- 压测"做任务"环节时,任务提交接口 P999 RT 飙升至 2-4 秒
- 压测"抽奖"环节时,抽奖接口 P999 RT 飙升至 3-5 秒
- 压测到 400 TPS 时,Tomcat 线程池出现大量 BLOCKED 状态线程
- 应用日志报错: `java.net.SocketTimeoutException: Read timed out`
- 通过 Arthas 的 `trace` 命令发现,积分系统调用耗时 500ms-2s

**根因分析**:
- **业务场景**:
  - **做任务**:用户完成任务后,需同步调用积分系统增加积分或发放抽奖次数
  - **抽奖**:用户抽奖时,需同步调用积分系统扣减积分(如消耗积分抽奖)
- **同步阻塞**:业务逻辑要求必须拿到积分系统响应才能继续,无法跳过
- **性能瓶颈**:
  - 积分系统是外部微服务,响应时间不可控(平均 500ms,高峰期可达 2s)
  - 同步调用导致 Tomcat 线程长时间阻塞,并发能力受限
  - 当积分系统故障或响应慢时,会拖垮整个活动系统
  - 积分系统自身也可能因为活动高峰流量而压力过大

**Arthas 排查过程**:
```bash
# 追踪任务提交接口的耗时分布
trace com.xxx.activity.service.TaskService submitTask '#cost > 100' -n 5

# 追踪抽奖接口的耗时分布
trace com.xxx.activity.service.LotteryService drawLottery '#cost > 100' -n 5

# 追踪积分系统调用链路
trace com.xxx.point.service.PointService addPoint '#cost > 100' -n 5
trace com.xxx.point.service.PointService deductPoint '#cost > 100' -n 5
```

**优化方案**:

**方案一:引入超时控制与熔断降级(Sentinel,适合弱依赖场景)**
```java
// 使用 Sentinel 进行熔断降级
@SentinelResource(
    value = "addPoint",
    fallback = "addPointFallback"
)
public PointResult addPoint(String userId, Integer points, String taskId) {
    // 设置超时时间为 500ms
    return pointServiceClient.addPoint(userId, points, taskId, 500, TimeUnit.MILLISECONDS);
}

// 熔断后降级逻辑:异步补偿
public PointResult addPointFallback(String userId, Integer points, String taskId) {
    // 记录到补偿表,定时任务重试
    compensateDao.insert(new CompensateTask(userId, points, taskId, "ADD_POINT"));

    // 返回成功(先快速响应,后台补偿)
    return PointResult.success("积分将在 5 分钟内到账");
}

// Sentinel 熔断规则
DegradeRule rule = new DegradeRule("addPoint")
    .setGrade(CircuitBreakerStrategy.SLOW_REQUEST_RATIO.getType())
    .setSlowRatioThreshold(0.5)  // 慢调用比例 > 50%
    .setStatIntervalMs(10000)
    .setSlowRequestDuration(500)  // 慢调用阈值 500ms
    .setTimeWindow(10);           // 熔断时长 10 秒
```

**方案二:消息队列异步解耦(RabbitMQ,推荐)**
```java
// 做任务:快速入队
@PostMapping("/task/complete")
public Result completeTask(@RequestBody TaskRequest req) {
    String taskId = UUID.randomUUID().toString();
    req.setTaskId(taskId);

    // 快速入队(耗时 <10ms)
    rabbitTemplate.convertAndSend("task_exchange", "task.complete", req);

    return Result.success("任务完成,积分将在 5 分钟内到账");
}

// 抽奖:快速入队
@PostMapping("/lottery/draw")
public Result drawLottery(@RequestBody LotteryRequest req) {
    String lotteryId = UUID.randomUUID().toString();
    req.setLotteryId(lotteryId);

    // 快速入队(耗时 <10ms)
    rabbitTemplate.convertAndSend("lottery_exchange", "lottery.draw", req);

    return Result.success("抽奖请求已提交,请稍后查看结果");
}

// 消费者:异步调用积分系统
@RabbitListener(queues = "task_complete_queue")
public void consumeTaskComplete(TaskRequest req) {
    String userId = req.getUserId();
    Integer points = req.getPoints();
    String taskId = req.getTaskId();

    try {
        // 调用积分系统(可设置更长超时,不阻塞主流程)
        PointResult result = pointServiceClient.addPoint(userId, points, taskId);

        if (result.isSuccess()) {
            // 发放抽奖次数
            lotteryService.addLotteryChance(userId, taskId);
            log.info("积分发放成功: userId={}, points={}", userId, points);
        } else {
            log.warn("积分发放失败: userId={}, reason={}", userId, result.getMsg());
        }
    } catch (Exception e) {
        log.error("积分系统异常: userId={}", userId, e);
        // 发送到死信队列,人工介入或重试
        rabbitTemplate.convertAndSend("task_dlx_exchange", "task.failed", req);
    }
}
```

**方案三:本地积分预扣 + 异步同步(适合强依赖场景)**
```java
// 抽奖时:本地预扣积分,异步同步到积分系统
@Transactional
public LotteryResult drawLottery(String userId, Long prizeId) {
    // 1. 本地预扣积分(快速)
    UserPoint userPoint = userPointDao.selectByUserId(userId);
    if (userPoint.getPoints() < 10) {
        throw new BusinessException("积分不足");
    }
    userPoint.setPoints(userPoint.getPoints() - 10);
    userPointDao.updateById(userPoint);

    // 2. 执行抽奖逻辑
    Prize prize = lotteryEngine.draw(prizeId);

    // 3. 异步同步到积分系统
    CompletableFuture.runAsync(() -> {
        pointServiceClient.deductPoint(userId, 10, "抽奖消费");
    }, asyncExecutor);

    return LotteryResult.success(prize);
}
```

**方案四:积分系统接口优化(服务端优化)**
```java
// 积分系统侧:批量接口提升吞吐量
@PostMapping("/point/batchAdd")
public BatchResult batchAddPoint(@RequestBody List<PointRequest> requests) {
    // 批量插入数据库,减少 IO 次数
    List<PointRecord> records = requests.stream()
        .map(req -> new PointRecord(req.getUserId(), req.getPoints(), req.getTaskId()))
        .collect(Collectors.toList());
    pointRecordDao.batchInsert(records);

    // 批量更新用户积分(使用 CASE WHEN 批量更新)
    userPointDao.batchAddPoints(records);

    return BatchResult.success(requests.size());
}

// 活动侧:定时批量调用积分系统
@Scheduled(fixedRate = 5000) // 每 5 秒批量同步一次
public void batchSyncPoints() {
    // 从本地缓冲区取出待同步的积分变更
    List<PointRequest> pendingPoints = pointBuffer.drain(100);

    if (!pendingPoints.isEmpty()) {
        // 批量调用积分系统
        pointServiceClient.batchAddPoint(pendingPoints);
    }
}
```

**优化效果**:
- "任务提交"接口 P99 RT 从 2s 降至 150ms
- "抽奖"接口 P99 RT 从 3s 降至 180ms
- 积分系统故障时自动降级,不影响用户操作
- 系统并发能力提升约 50%(从 400 TPS 提升至 850 TPS)
- 实现了业务解耦,积分系统可独立扩容

**补充:如何保证最终一致性?**
```java
// 消费者端增加幂等性校验
@RabbitListener(queues = "task_complete_queue")
public void consumeTaskComplete(TaskRequest req) {
    String taskId = req.getTaskId();

    // 幂等性校验:检查是否已处理过该任务
    String lockKey = "task:lock:" + taskId;
    boolean locked = redisTemplate.opsForValue().setIfAbsent(lockKey, "1", 5, TimeUnit.MINUTES);
    if (!locked) {
        log.warn("任务已处理,跳过: taskId={}", taskId);
        return;
    }

    // 执行业务逻辑...
}

// 增加补偿机制:定时任务扫描未完成任务
@Scheduled(fixedRate = 300000) // 每 5 分钟执行一次
public void checkUnfinishedTasks() {
    List<Task> unfinishedTasks = taskDao.selectUnfinishedTasks();
    for (Task task : unfinishedTasks) {
        // 重新发送到队列
        rabbitTemplate.convertAndSend("task_exchange", "task.complete", task);
    }
}

// 积分系统侧:增加分布式锁防止重复扣减
public PointResult addPoint(String userId, Integer points, String taskId) {
    String lockKey = "point:lock:" + taskId;
    RLock lock = redissonClient.getLock(lockKey);

    try {
        if (lock.tryLock(5, 10, TimeUnit.SECONDS)) {
            // 再次检查是否已处理(双重检查)
            PointRecord record = pointRecordDao.selectByTaskId(taskId);
            if (record != null) {
                return PointResult.success("已处理");
            }

            // 执行积分增加逻辑
            userPointDao.addPoint(userId, points);
            pointRecordDao.insert(new PointRecord(userId, points, taskId));

            return PointResult.success();
        }
    } finally {
        lock.unlock();
    }
    return PointResult.fail("获取锁失败");
}
```

---

#### (六)其他优化措施

| 优化项 | 具体措施 | 效果 |
|:---|:---|:---|
| **日志优化** | 生产环境禁用DEBUG日志,INFO日志改为异步写入(Logback AsyncAppender) | 磁盘IO从80%降至30% |
| **索引优化** | 为 `user_points.user_id` 和 `prize_stock.prize_id` 添加唯一索引 | 查询RT从200ms降至50ms |
| **批量处理** | 中奖记录从单条插入改为批量插入(每100条一批) | DB写入TPS从200提升到800 |
| **预热策略** | 压测前预热热点奖品缓存和用户积分缓存 | 冷启动RT从2秒降至500ms |

---

**面试金句**:
> "压测最大的价值不是得出一个数字,而是发现瓶颈并验证优化效果。我们这次压测从500 TPS提升到850 TPS,过程中解决了数据库连接池耗尽、热点奖品缓存穿透、分布式锁竞争、活动奖品配置大 Key、同步调用积分系统超时五个关键瓶颈,每个瓶颈的优化都是基于真实数据分析和根因定位,而不是盲目调参。"


## 六、压测通过标准建议

| 维度 | 标准 |
|:---|:---|
| 核心接口 RT(P99) | ≤ 500ms |
| 登录接口 RT(P99) | ≤ 1s |
| 错误率 | ≤ 0.1%(不含业务预期的"库存不足") |
| 系统资源水位 | CPU ≤ 70%,内存 ≤ 80% |
| 压测时长 | 峰值水位持续 **30分钟** 无劣化趋势 |
| 超卖检测 | 库存字段 ≥ 0,无负数记录 |


> **面试官终极追问提示**:"如果压测时发现 P99 响应时间合格,但 P999 飞得很高,你如何排查?"——此时可回答:**检查GC日志中的Full GC频率、查看是否有跨机房调用、检查是否有热点Key的驱逐重加载逻辑。**