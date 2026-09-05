## 一、核心业务流量模型（权重配比）

基于埋点数据（PV/UV/中奖/领奖率），最终确定的接口权重与预期 QPS 分配如下：

| 接口类型 | 权重占比 | 目标 QPS | 依赖/关联说明 |
| :--- | :--- | :--- | :--- |
| **浏览（首页/列表）** | 500 (50%) | 12,500 | 纯读，无依赖 |
| **活动说明** | 150 (15%) | 3,750 | 纯读，无依赖 |
| **任务详情** | 150 (15%) | 3,750 | 弱依赖（产生 `task_id` 缓存，但不强制跳转） |
| **任务跳转（开始任务）** | 100 (10%) | 2,500 | 依赖 `task_id`（优先取缓存，无则随机池兜底） |
| **登录** | 50 (5%) | 1,250 | 独立接口，负责刷新 Token |
| **抽奖** | 43 (4.3%) | 1,075 | 无依赖（产出 `prize_id`，但按 50.62% 概率入队） |
| **领奖** | 7 (0.7%) | 175 | **弱关联**（消费队列中的 `user_id + prize_id`；队列空则查奖品列表） |

---

## 二、核心技术架构与设计决策

| 架构决策点 | 最终落地方案 | 解决的核心痛点 |
| :--- | :--- | :--- |
| **压测引擎** | Locust + FastHttpUser（K8s 分布式） | 高并发协程模型，资源占用低 |
| **流量调度** | 顶层使用 **`@task` 加权随机**（拒绝全量 SequentialTaskSet） | 保证 50% 浏览 vs 0.7% 领奖的悬殊比例不失真 |
| **抽奖→领奖关联** | **会话级有界队列**（`self.pending_prizes`，Max=5） + 50.62% 衰减因子 | 解耦权重，同时精准模拟“中奖后一半人放弃”的真实数据 |
| **队列并发安全** | **实例私有队列 + 单协程串行执行**，无锁设计 | 无需引入线程锁/Redis分布式锁，零并发冲突，性能最优 |
| **鉴权与容灾** | CSV 账号池硬隔离分片 + **401 自动重试机制**（`_auth_request` 封装） | 解决分布式下账号互踢风暴；模拟 Token 过期自动续期 |
| **分布式账号隔离** | K8s Downward API 注入 `POD_NAME`，按序号对 CSV **逻辑分片（Sharding）** | 17 个 Worker 各用各的账号段，绝对互斥 |
| **代码与数据打包** | **Dockerfile 内置 CSV**（`COPY` 进 `/app`），不可变镜像交付 | 规避 ConfigMap 1MiB 大小限制，无需依赖外部存储卷 |
| **可观测性** | **被测服务**挂载 SkyWalking Agent；**Locust 仅传递 `sw8` Header** | 客户端不发压污染，链路追踪清晰 |

---

## 三、队列并发安全深度论证（重要补充）

### 1. 为什么绝对不存在并发冲突？

| 维度 | 分析 | 结论 |
| :--- | :--- | :--- |
| **单 VU 内部执行模型** | Locust 中每个虚拟用户（VU）是一个独立的 **Greenlet（协程）**。同一个 VU 内的 `do_draw`（抽奖）和 `do_claim`（领奖）**严格串行执行**，中间隔着 `wait_time`（思考时间）。 | 同一时刻只有一个操作在修改 `self.pending_prizes`。 |
| **队列作用域** | `self.pending_prizes` 是 **实例属性**，绑定在单个 VU 对象上。VU-A 的队列和 VU-B 的队列**内存地址完全隔离**。 | 不存在多 VU 竞争同一把锁的场景。 |
| **跨 Worker 隔离** | K8s 中 17 个 Worker 是独立进程，内存空间互不共享。Worker-1 里的 VU 完全看不到 Worker-2 里的队列。 | 分布式架构天然物理隔离。 |

### 2. 唯一的“伪并发”场景与防呆设计

**场景**：一个用户连续抽中 6 次奖，但一次都没领，队列会怎样？

- **无保护**：队列无限膨胀 → 单 VU 内存泄漏 → Worker OOM。
- **我们的方案**：设定 `MAX_PENDING = 5`，当队列已满时，**丢弃最旧的奖品**（`pop(0)`），保证内存恒定。

> **关键实现细节**：`append` 和 `pop(0)` 在同一个函数（`do_draw`）的同一个协程中**顺序执行**，不涉及任何跨线程/跨协程切换，因此 100% 线程安全，无需 `threading.Lock`。

---

## 四、代码仓库目录与镜像打包设计

### 1. 项目目录结构（推荐）

```
locust-loadtest/
├── Dockerfile                     # 镜像构建文件
├── requirements.txt               # Python 依赖（如有额外需要）
├── locustfile.py                  # 主压测脚本
├── accounts.csv                   # 账号池（≥ 57,600 行）
├── README.md                      # 使用说明（可选）
└── .dockerignore                  # 忽略无用文件（如 .git, __pycache__）
```

### 2. Dockerfile（关键）

```dockerfile
FROM locustio/locust:2.24.1

# 设置工作目录
WORKDIR /app

# 复制依赖文件（利用 Docker 缓存层）
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 复制压测脚本和账号数据（核心）
COPY locustfile.py .
COPY accounts.csv .

# 验证文件已复制（可选，构建时查看日志）
RUN ls -la /app/

# 默认启动命令（由 K8s 覆盖，此处仅为留空）
CMD ["locust", "--version"]
```

### 3. .dockerignore（优化构建速度）

```
__pycache__
*.pyc
.git
.gitignore
README.md
*.log
```

---

## 五、Locust 关键代码实现（完整核心片段）

### 1. AccountPool 分片加载（CSV 与代码同级）

```python
import os
import csv
import queue
import random
from locust import FastHttpUser, task, between, LoadTestShape

class AccountPool:
    """按 K8s Pod 序号分片加载 CSV，实现硬隔离"""
    def __init__(self):
        # 1. 获取 Pod 序号（如 locust-worker-5 -> 5）
        pod_name = os.getenv("POD_NAME", "locust-worker-0")
        try:
            self.worker_id = int(pod_name.split("-")[-1])
        except ValueError:
            self.worker_id = 0
        
        self.total_workers = int(os.getenv("TOTAL_WORKERS", 17))
        
        # 2. 读取与脚本同目录的 CSV（利用 __file__ 定位）
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_dir, "accounts.csv")
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)  # 列名：username, password
            all_accounts = list(reader)
        
        # 3. 分片切割（均分）
        total = len(all_accounts)
        chunk_size = total // self.total_workers
        start = self.worker_id * chunk_size
        end = start + chunk_size if self.worker_id < self.total_workers - 1 else total
        
        self.my_accounts = all_accounts[start:end]
        random.shuffle(self.my_accounts)  # 打乱，避免同时压测前缀连续账号
        
        # 4. 放入线程安全队列（跨 VU 取账号互斥）
        self.pool = queue.Queue()
        for acc in self.my_accounts:
            self.pool.put(acc)
        
        print(f"Worker-{self.worker_id} 分得账号数: {len(self.my_accounts)}")
    
    def get_account(self):
        """阻塞获取一个账号，直至有可用"""
        return self.pool.get()

# 全局初始化（在所有 VU 启动前执行一次）
account_pool = AccountPool()
```

### 2. 主用户类（含 401 自动重试 + 有界队列）

```python
class AppUser(FastHttpUser):
    wait_time = between(0.5, 1.5)

    def on_start(self):
        """每个 VU 启动时，从分片池中领取专属账号"""
        self.account = account_pool.get_account()
        self.username = self.account["username"]
        self.password = self.account["password"]
        self.token = None
        self.user_id = None
        self.cached_task_id = None
        self.pending_prizes = []  # 有界队列，Max=5
        
        # 首次登录（必须成功，否则该 VU 报废）
        self._do_login()

    def _do_login(self):
        """执行真实登录，更新 token 和 user_id"""
        payload = {"username": self.username, "password": self.password}
        resp = self.client.post("/api/login", json=payload)
        if resp.status_code == 200:
            data = resp.json()
            self.token = data.get("token")
            self.user_id = data.get("user_id", self.username)
            return True
        else:
            raise Exception(f"用户 {self.username} 登录失败，状态码: {resp.status_code}")

    def _auth_request(self, method, url, **kwargs):
        """
        核心封装：自动携带 Token，若返回 401 则刷新 Token 并重试一次
        """
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        if self.token:
            kwargs["headers"]["Authorization"] = f"Bearer {self.token}"
        
        resp = self.client.request(method, url, **kwargs)
        
        # 鉴权失败，尝试重新登录并重试
        if resp.status_code == 401:
            if self._do_login():
                kwargs["headers"]["Authorization"] = f"Bearer {self.token}"
                resp = self.client.request(method, url, **kwargs)
            else:
                resp.failure(f"重新登录失败，用户 {self.username}")
        
        return resp

    # ========== 业务接口（按权重分配） ==========
    @task(500)
    def browse(self):
        resp = self._auth_request("GET", "/api/activity/list")
        if resp.status_code != 200:
            resp.failure(f"浏览失败: {resp.status_code}")

    @task(150)
    def view_rules(self):
        # 类似实现...
        pass

    @task(150)
    def view_task_detail(self):
        task_id = random.choice([1001, 1002, 1003])
        resp = self._auth_request("GET", f"/api/task/detail?task_id={task_id}")
        if resp.status_code == 200:
            self.cached_task_id = task_id  # 缓存，供后续跳转

    @task(100)
    def start_task(self):
        task_id = self.cached_task_id or random.choice([1001, 1002, 1003])
        resp = self._auth_request("POST", "/api/task/start", json={"task_id": task_id})

    @task(50)
    def do_login(self):
        """主动刷新 Token（模拟用户重新登录）"""
        self._do_login()

    # ========== 抽奖 + 有界队列（核心） ==========
    MAX_PENDING = 5  # 队列容量保护

    @task(43)
    def do_draw(self):
        resp = self._auth_request("POST", "/api/draw")
        if resp.status_code != 200:
            resp.failure(f"抽奖失败: {resp.status_code}")
            return
        
        data = resp.json()
        if data.get("data", {}).get("win") is True:
            prize_id = data["data"].get("prize_id")
            if prize_id and random.random() < 0.5062:  # 50.62% 领奖率
                # 队列容量保护（丢弃最旧奖品，防止内存泄漏）
                if len(self.pending_prizes) >= self.MAX_PENDING:
                    self.pending_prizes.pop(0)  # 丢弃最旧的
                self.pending_prizes.append({
                    "user_id": self.user_id,
                    "prize_id": prize_id
                })

    @task(7)
    def do_claim(self):
        if self.pending_prizes:
            item = self.pending_prizes.pop()  # LIFO，模拟最近中奖先领
            resp = self._auth_request("POST", "/api/claim", json={
                "prize_id": item["prize_id"],
                "user_id": item["user_id"]
            })
            if resp.status_code != 200:
                resp.failure(f"领奖失败: {resp.status_code}")
        else:
            # 队列为空，查看我的奖品（维持发压连贯性）
            self._auth_request("GET", "/api/prize/my-list")
```

### 3. 阶梯升压控制（LoadTestShape）

```python
class StepsLoadTest(LoadTestShape):
    stages = [
        {"duration": 120, "users": 12000, "spawn_rate": 50},   # 25%
        {"duration": 120, "users": 24000, "spawn_rate": 50},   # 50%
        {"duration": 180, "users": 36000, "spawn_rate": 50},   # 75%
        {"duration": 300, "users": 48000, "spawn_rate": 50},   # 100% 目标
        {"duration": 120, "users": 57600, "spawn_rate": 50},   # 120% 破极
    ]
    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return (stage["users"], stage["spawn_rate"])
        return None
```

---

## 六、K8s 分布式部署与分片配置

### 1. Worker Deployment（含环境变量注入）

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: locust-worker
spec:
  replicas: 17
  selector:
    matchLabels:
      app: locust-worker
  template:
    metadata:
      labels:
        app: locust-worker
    spec:
      containers:
      - name: worker
        image: your-registry/locust-loadtest:latest   # 镜像内含 CSV
        args: ["--worker", "--master-host=locust-master"]
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: TOTAL_WORKERS
          value: "17"          # 必须与 replicas 保持一致
        - name: LOCUST_HOST   # 可选，被测服务地址
          value: "https://your-target-domain.com"
        resources:
          requests:
            cpu: "2"
            memory: "4Gi"
          limits:
            cpu: "4"
            memory: "6Gi"
        # 调大文件句柄限制（关键）
        securityContext:
          sysctls:
          - name: net.core.somaxconn
            value: "65535"
          - name: net.ipv4.tcp_max_syn_backlog
            value: "65535"
```

### 2. Master Service & Deployment（简要）

```yaml
apiVersion: v1
kind: Service
metadata:
  name: locust-master
spec:
  clusterIP: None
  ports:
  - name: comm
    port: 5557
  - name: comm2
    port: 5558
  - name: web-ui
    port: 8089
  selector:
    app: locust-master
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: locust-master
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: master
        image: your-registry/locust-loadtest:latest
        args: ["--master", "--headless", "--web-port=8089", "--expect-workers=17"]
        ports:
        - containerPort: 8089
        resources:
          requests:
            cpu: "500m"
            memory: "1Gi"
```

---

## 七、资源规划与阶梯升压策略

| 阶段 | 时长 | 总 VU（用户数） | 目标总 QPS | 校验目的 |
| :--- | :--- | :--- | :--- | :--- |
| Stage 1 | 2 min | 12,000 | ~6,250 (25%) | 验证连通性与缓存 |
| Stage 2 | 2 min | 24,000 | ~12,500 (50%) | 观察中间件水位 |
| Stage 3 | 3 min | 36,000 | ~18,750 (75%) | 逼近临界点 |
| Stage 4 | 5 min | **48,000** | **~25,000 (100%)** | **目标容量持续验证** |
| Stage 5 | 2 min | 57,600 | ~30,000 (120%) | 寻找系统天花板 |

---

## 八、监控与成功标准（Checklist）

| 层级 | 工具 | 重点关注指标 | 通过阈值 |
| :--- | :--- | :--- | :--- |
| 压测客户端 | Locust Web UI / CSV | 总 QPS 是否达到 25k；错误率 | 错误率 < 1% |
| 压测机（Worker） | Grafana + Prometheus | CPU ≥ 85% 预警；内存无持续增长（队列防溢出） | CPU < 90%，内存 < 5Gi |
| 被测服务 | SkyWalking（服务端 Agent） | 抽奖/领奖 P95 RT；数据库连接池活跃数 | P95 < 200ms（读）/ < 500ms（写） |
| 业务逻辑 | 数据库/日志 | 中奖入队数 ≈ 领奖请求数 × 2（因 50% 转化率） | 无奖品丢失或重复领取 |

---

## 九、执行前最终检查清单

- [ ] `accounts.csv` 账号数量 ≥ **57,600** 行（`wc -l accounts.csv` 确认）。
- [ ] `TOTAL_WORKERS` 环境变量值与 Deployment `replicas` 一致（均为 17）。
- [ ] Docker 镜像已构建并推送到仓库（`docker build -t your-registry/locust-loadtest:latest .`）。
- [ ] 被测服务已挂载 SkyWalking Agent，且压测接口已预热（如奖品池预先填充）。
- [ ] K8s 集群节点 `ulimit -n` 已调大，或 Pod 中已配置 `securityContext.sysctls`。
- [ ] Master 启动参数包含 `--expect-workers=17`，确保 Worker 全部连入后才开始发压。
