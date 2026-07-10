---
tags: [全链路压测]
---

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

### 4.3 针对特定风险的压测执行方案

| 风险点 | JMeter 针对性策略 |
|:---|:---|
| **超卖（库存扣减）** | 使用 `Synchronizing Timer`，设定50线程同时释放（瞬间集合点），模拟50人同时抢最后一个库存，观察是否返回负数 |
| **AI接口超时阻塞** | HTTP Request单独设置连接超时1s/响应超时2s，配合 `Constant Throughput Timer` 在错误率>5%时强制降级 |
| **缓存穿透/DB压力** | 固定热点奖品ID，清除Redis缓存后并发压测，观察DB的QPS和连接数飙升情况 |
| **日志风暴** | 压测期间禁用 `View Results Tree`，仅依赖 `Simple Data Writer` 落盘，避免压测机自身成为瓶颈 |


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

#### (四)其他优化措施

| 优化项 | 具体措施 | 效果 |
|:---|:---|:---|
| **日志优化** | 生产环境禁用DEBUG日志,INFO日志改为异步写入(Logback AsyncAppender) | 磁盘IO从80%降至30% |
| **索引优化** | 为 `user_points.user_id` 和 `prize_stock.prize_id` 添加唯一索引 | 查询RT从200ms降至50ms |
| **批量处理** | 中奖记录从单条插入改为批量插入(每100条一批) | DB写入TPS从200提升到800 |
| **预热策略** | 压测前预热热点奖品缓存和用户积分缓存 | 冷启动RT从2秒降至500ms |

---

**面试金句**:
> "压测最大的价值不是得出一个数字,而是发现瓶颈并验证优化效果。我们这次压测从500 TPS提升到850 TPS,过程中解决了数据库连接池耗尽、缓存穿透、分布式锁竞争三个关键瓶颈,每个瓶颈的优化都是基于真实数据分析和根因定位,而不是盲目调参。"


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