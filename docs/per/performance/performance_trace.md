# 性能拐点排查实战指南

## 一、整体排查思路

```
┌─────────────────────────────────────────────────────────────────┐
│                    性能拐点排查链路                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   性能拐点出现                                                   │
│        │                                                        │
│        ▼                                                        │
│   ┌─────────────────────────────────────────────┐               │
│   │  Step 1: 可视化监控 → 定位异常环节           │               │
│   │  (Grafana / SkyWalking / Arthas)            │               │
│   └─────────────────────────────────────────────┘               │
│        │                                                        │
│        ▼                                                        │
│   ┌─────────────────────────────────────────────┐               │
│   │  Step 2: 异常环节内部日志检查                │               │
│   │  (应用日志 / 中间件日志 / 系统日志)          │               │
│   └─────────────────────────────────────────────┘               │
│        │                                                        │
│        ▼                                                        │
│   ┌─────────────────────────────────────────────┐               │
│   │  Step 3: 深度工具定位                        │               │
│   │  (trace / dump / profile)                   │               │
│   └─────────────────────────────────────────────┘               │
│        │                                                        │
│        ▼                                                        │
│   定因 → 优化 → 验证                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

***

## 二、Step 1: 可视化监控定位异常环节

### 2.1 分层监控体系

```
┌────────────────────────────────────────────────────────────────┐
│                      监控分层架构                               │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Layer 4: 业务层                                               │
│  ├── 接口成功率、业务错误码分布                                 │
│  └── 来源: 业务埋点、日志聚合                                   │
│                                                                │
│  Layer 3: 应用层                                               │
│  ├── JVM (GC频率、堆内存、线程数)                              │
│  ├── 线程池 (活跃线程、队列长度)                                │
│  └── 来源: Prometheus + Micrometer / SkyWalking               │
│                                                                │
│  Layer 2: 中间件层                                             │
│  ├── MySQL (连接数、慢查询、锁等待)                            │
│  ├── Redis (内存、命中率、慢命令)                              │
│  └── 来源: Exporter (mysql_exporter, redis_exporter)          │
│                                                                │
│  Layer 1: 基础设施层                                           │
│  ├── CPU、内存、磁盘I/O、网络带宽                              │
│  └── 来源: Node Exporter + cAdvisor                           │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 2.2 Grafana Dashboard 关键指标

**应用层面板**：

```
┌─────────────────────────────────────────────────────────────┐
│                    应用层监控面板                            │
├──────────────────┬──────────────────┬───────────────────────┤
│  JVM堆内存使用率  │  GC频率          │  线程状态分布         │
│  当前: 78%       │  Young: 12次/分  │  RUNNABLE: 85        │
│  ⚠️ 接近警戒线   │  Full: 0次/分    │  BLOCKED: 12 ⚠️      │
│                  │                  │  WAITING: 45         │
├──────────────────┴──────────────────┴───────────────────────┤
│                                                             │
│  线程池监控                                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Tomcat线程池                                         │   │
│  │ ├─ active: 180 / maxThreads: 200                    │   │
│  │ ├─ queueSize: 45 ⚠️ 队列堆积                        │   │
│  │ └─ rejected: 12                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Redis 监控面板**：

```
┌─────────────────────────────────────────────────────────────┐
│                    Redis 监控面板                           │
├──────────────────┬──────────────────┬───────────────────────┤
│  内存使用率      │  缓存命中率      │  慢命令数             │
│  当前: 92% ⚠️    │  当前: 60% ⚠️    │  最近5分钟: 156       │
│  持续上涨不回落  │  从95%跌落       │  GET耗时200ms+        │
├──────────────────┴──────────────────┴───────────────────────┤
│                                                             │
│  Key 统计                                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ├─ 总Key数: 1,250,000                               │   │
│  │ ├─ 过期Key: 0 ⚠️ 无TTL设置                          │   │
│  │ ├─ evicted_keys: 45,230 ⚠️ 频繁逐出                 │   │
│  │ └─ 大Key: user:tag:xxx (2MB) ⚠️                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**数据库层面板**：

```
┌─────────────────────────────────────────────────────────────┐
│                    MySQL 监控面板                           │
├──────────────────┬──────────────────┬───────────────────────┤
│  连接数          │  慢查询数        │  锁等待               │
│  当前: 145/150   │  最近5分钟: 23   │  等待事务: 12         │
│  ⚠️ 接近上限     │  ⚠️ 异常增多     │  ⚠️ 行锁竞争          │
├──────────────────┴──────────────────┴───────────────────────┤
│                                                             │
│  连接池监控 (HikariCP)                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ├─ active: 18 / maximum: 20                         │   │
│  │ ├─ idle: 2                                          │   │
│  │ ├─ pending: 45 ⚠️ 大量等待获取连接                  │   │
│  │ └─ usage: 90%                                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 快速定位异常环节的判断逻辑

```python
def locate_bottleneck(metrics):
    """
    根据监控指标快速定位瓶颈环节
    """
    
    # 1. Redis层判断
    if metrics.redis_memory_usage > 0.9:
        return "Redis内存接近爆满，可能触发逐出策略"
    
    if metrics.redis_evicted_keys > threshold:
        return "Redis频繁逐出Key，缓存命中率下降"
    
    if metrics.redis_slowlog_count > 0:
        return "存在Redis慢命令"
    
    # 2. 数据库层判断
    if metrics.db_connection_usage > 0.9:
        return "数据库连接池不足"
    
    if metrics.slow_query_count > threshold:
        return "存在慢查询"
    
    if metrics.lock_wait_count > 0:
        return "数据库锁竞争"
    
    # 3. 应用层判断
    if metrics.thread_pool_queue_size > 0:
        return "线程池队列堆积"
    
    if metrics.blocked_thread_count > 10:
        return "线程阻塞（可能存在锁竞争）"
    
    if metrics.gc_pause_time > 100:
        return "GC停顿过长"
    
    # 4. 外部依赖判断
    if metrics.external_api_rt > 500:
        return "外部API响应慢，阻塞主流程"
    
    # 5. 基础设施层判断
    if metrics.cpu_usage > 0.85:
        return "CPU资源瓶颈"
    
    if metrics.memory_usage > 0.9:
        return "内存资源瓶颈"
    
    if metrics.network_io_wait > threshold:
        return "网络I/O瓶颈"
    
    return "需要进一步分析"
```

***

## 三、Step 2: 异常环节内部日志检查

### 3.1 Redis 层日志检查

**Redis 慢查询日志**：

```bash
# 查看 Redis 慢查询
redis-cli SLOWLOG GET 20

# 输出示例
1) 1) (integer) 1
   2) (integer) 1726123456
   3) (integer) 234567    # 执行时间(微秒) = 234ms
   4) 1) "GET"
      2) "user:tag:12345"
   5) "192.168.1.100:54321"
   6) "ad-platform"
```

**大 Key 定位**：

```bash
# 扫描大 Key
redis-cli --bigkeys

# 输出示例
-------- summary -------
Biggest string found 'user:tag:ad_space_001' has 2097152 bytes  # 2MB大Key

# 实时监控网络流量
redis-cli --stat
# 观察到每秒有几次极高的入流量尖峰（如200Mbps）
```

**内存与逐出分析**：

```bash
# 查看内存详情
redis-cli INFO memory

# 关键指标
used_memory:8589934592        # 已使用内存
maxmemory:9663676416          # 最大内存限制
mem_fragmentation_ratio:1.02  # 内存碎片率
evicted_keys:45230            # 已逐出的Key数量 ⚠️

# 查看Key数量变化
redis-cli INFO keyspace
db0:keys=1250000,expires=0,avg_ttl=0  # expires=0 表示无过期时间 ⚠️
```

### 3.2 数据库层日志检查

**MySQL 慢查询日志**：

```sql
-- 开启慢查询日志
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;

-- 查看慢查询
SELECT * FROM mysql.slow_log 
WHERE start_time > DATE_SUB(NOW(), INTERVAL 1 HOUR)
ORDER BY query_time DESC 
LIMIT 10;

-- 分析执行计划
EXPLAIN SELECT * FROM ad_rules WHERE ad_space_id = 123;
```

**执行计划关键字段解读**：

```text
+----+-------------+----------+------------+------+---------------+---------------+---------+-------+------+----------+-------+
| id | select_type | table    | partitions | type | possible_keys | key           | key_len | ref   | rows | filtered | Extra |
+----+-------------+----------+------------+------+---------------+---------------+---------+-------+------+----------+-------+
|  1 | SIMPLE      | ad_rules | NULL       | ref  | idx_space     | idx_space     | 4       | const |  156 |    100.0 | NULL  |
+----+-------------+----------+------------+------+---------------+---------------+---------+-------+------+----------+-------+

关键字段说明：
- type: 访问类型，从优到差：system > const > eq_ref > ref > range > index > ALL
  ⚠️ ALL 表示全表扫描，需要优化
- key: 实际使用的索引，NULL 表示未使用索引
- rows: 预估扫描行数，值越大效率越低
- Extra: 额外信息
  - Using index: 覆盖索引，性能好
  - Using filesort: 文件排序，需要优化
  - Using temporary: 使用临时表，需要优化
```

??? tip "回表"

    背景：InnoDB 使用 B+ 树索引：

    - 聚簇索引（一般是主键索引）的叶子节点上直接存储了完整的一行数据。

    - 二级索引（普通索引、唯一索引等）的叶子节点上只存储了索引列的值 + 主键的值。

    所谓回表，就是当我们通过二级索引查找数据时，如果要查询的字段不在该二级索引的叶子节点中，那么数据库会先通过二级索引找到对应的主键值，再拿着主键值回到聚簇索引中，把整行数据读出来。这个“回到聚簇索引再查一次”的动作，就叫回表。

    举例：

    表 user，主键是 id，有一个普通索引 idx_name 在 name 列上。

    执行 SELECT id, name, age FROM user WHERE name = '张三'。

    因为 idx_name 只存了 name 和 id，不包含 age，所以 InnoDB 会先从 idx_name 找到匹配的 id，再根据 id 去主键索引里查出 age。这就是一次回表。

**锁等待分析**：

```sql
-- 查看当前锁等待
SELECT 
    r.trx_id waiting_trx_id,
    r.trx_mysql_thread_id waiting_thread,
    r.trx_query waiting_query,
    b.trx_id blocking_trx_id,
    b.trx_mysql_thread_id blocking_thread,
    b.trx_query blocking_query
FROM information_schema.innodb_lock_waits w
INNER JOIN information_schema.innodb_trx b ON b.trx_id = w.blocking_trx_id
INNER JOIN information_schema.innodb_trx r ON r.trx_id = w.requesting_trx_id;

-- 查看InnoDB状态
SHOW ENGINE INNODB STATUS\G
```

**锁等待分析要点**：

```text
INNODB STATUS 输出关键部分：
=====================================
TRANSACTIONS
=====================================
Trx id counter 1234567
Purge done for trx's n:o < 1234560
History list length 1024
---TRANSACTION 1234566, ACTIVE 45 sec starting index read
mysql tables in use 1, locked 1
LOCK WAIT 2 lock struct(s), heap size 1136, 1 row lock(s)
MySQL thread id 100, OS thread handle 12345, query id 67890 localhost root updating
UPDATE ad_rules SET status = 1 WHERE id = 100
------- TRX HAS BEEN WAITING 45 SEC FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 58 page no 4 n bits 72 index PRIMARY of table `ad_db`.`ad_rules`
---WAITING FOR LOCK: RECORD LOCKS space id 58 page no 4 n bits 72 index PRIMARY
Record lock, heap no 2 PHYSICAL RECORD: n_fields 5; compact format; info bits 0

分析步骤：
1. 找到 LOCK WAIT 标记，确认存在锁等待
2. 查看 WAITING FOR LOCK 部分，确认等待的锁类型和位置
3. 通过 thread id 定位阻塞事务：SELECT * FROM information_schema.innodb_trx WHERE trx_mysql_thread_id = <thread_id>;
4. 分析阻塞事务的 SQL 语句，决定是否 KILL 或优化
```

### 3.3 应用层日志检查

**JVM 日志分析**：

```bash
# 查看 GC 日志
jstat -gcutil <pid> 1000 10

# 输出示例
#  S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT    GCT   
#  0.00  45.21  78.34  67.89  95.12  89.23    156    2.345     2    0.456   2.801

# 线程栈分析
jstack <pid> > thread_dump.txt
```

**应用异常日志**：

```bash
# 搜索关键异常
grep -E "Exception|Error|Timeout|Rejected" /var/log/app/app.log | tail -100

# 搜索慢请求
grep "cost=" /var/log/app/app.log | awk -F'cost=' '{print $2}' | sort -n | tail -20
```

***

## 四、Step 3: 深度工具定位

### 4.1 Arthas 调用链追踪

**追踪方法耗时**：

```bash
# 追踪风控API调用
trace com.xxx.advfilter.handler.ListJudgeShuffleHandler doJudge '#cost > 100' -n 5

# 输出示例
`---[856.45ms] com.xxx.service.AdService:match()
    +---[12.15ms] com.xxx.dao.UserDao:getTags()
    +---[45.23ms] com.xxx.dao.AdDao:getRules()
    +---[23.32ms] com.xxx.service.AdService:filterAds()
    `---[756.12ms] com.xxx.external.RiskControlApi:check()  ← 瓶颈！
```

**监控 Redis 调用**：

```bash
# 追踪 Redis 操作
trace redis.clients.jedis.Jedis get '#cost > 50' -n 5

# 输出示例
`---[234.56ms] redis.clients.jedis.Jedis:get()
    `---[230.12ms] redis.clients.jedis.Connection:sendCommand()  ← 网络传输耗时
```

### 4.2 SkyWalking 调用链分析

```
┌─────────────────────────────────────────────────────────────┐
│                    SkyWalking Trace 详情                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  /api/v1/ad/match  [总耗时: 856ms]                          │
│  │                                                          │
│  ├─ Redis GET user:tag:123        [234ms] ⚠️ 大Key读取      │
│  │                                                          │
│  ├─ MySQL SELECT ad_rules          [45ms]                    │
│  │                                                          │
│  ├─ 业务逻辑匹配                    [23ms]                   │
│  │                                                          │
│  └─ HTTP 风控API调用               [756ms] ⚠️ 外部依赖慢     │
│     └─ http://risk-control/check                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

***

## 五、实战案例

### 案例 1: Redis 大 Key 导致内存暴涨与接口变慢

#### 现象

| 指标            | 数值           | 状态      |
| ------------- | ------------ | ------- |
| Redis 内存使用率   | 92% → 持续上涨   | ⚠️ 接近爆满 |
| 缓存命中率         | 95% → 60%    | ⚠️ 大幅下降 |
| 核心 API P95 RT | 150ms → 1.8s | ⚠️ 抖动剧烈 |
| evicted\_keys | 每秒数千次        | ⚠️ 频繁逐出 |

#### Step 1: 可视化监控定位

```
┌─────────────────────────────────────────────────────────────┐
│  Grafana 监控发现                                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Redis 内存趋势图                                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │     ▲                                               │   │
│  │    ╱                                                │   │
│  │   ╱  持续上涨，不回落                               │   │
│  │  ╱                                                  │   │
│  │ ╱                                                   │   │
│  │─────────────────────────────────────────────────    │   │
│  │  90%警戒线                                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  缓存命中率趋势                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ────────┐                                           │   │
│  │         ╲                                           │   │
│  │          ╲ 从95%跌至60%                             │   │
│  │           ─────────────────────────────────────     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Step 2: 日志与工具检查

```bash
# 1. 大 Key 扫描
redis-cli --bigkeys

# 输出
-------- summary -------
Biggest string found 'user:tag:ad_space_001' has 2097152 bytes  # 2MB

# 2. 检查该 Key 的 TTL
redis-cli TTL user:tag:ad_space_001
(integer) -1  # -1 表示永不过期 ⚠️

# 3. 检查逐出情况
redis-cli INFO stats | grep evicted
evicted_keys:45230  # 大量逐出

# 4. 网络流量监控
redis-cli --stat
# 观察到每秒有几次 200Mbps 的入流量尖峰

# 5. Arthas 追踪调用栈
trace com.xxx.service.AdService getTags '#cost > 100' -n 5

# 输出
`---[234.56ms] com.xxx.service.AdService:getTags()
    `---[230.12ms] redis.clients.jedis.Jedis:get()
        └─ Key: user:tag:ad_space_001  # 确认是这个大Key
```

#### 根因分析

```
┌─────────────────────────────────────────────────────────────┐
│                    根因链路                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 业务代码使用 String 存储用户标签                         │
│     └─ 单个 Key 存储广告位所有用户标签，Value 达到 2MB       │
│                                                             │
│  2. 未设置 TTL 过期时间                                      │
│     └─ Key 永不过期，持续累积                                │
│                                                             │
│  3. 内存触达 maxmemory (90%+)                                │
│     └─ 触发 allkeys-lru 逐出策略                            │
│                                                             │
│  4. 热数据被错误逐出                                         │
│     └─ 当日活跃用户的标签被踢出                              │
│                                                             │
│  5. 缓存命中率从 95% 跌至 60%                                │
│     └─ 大量请求穿透到 MySQL                                  │
│                                                             │
│  6. 接口 RT 抖动、TPS 下降                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 解决方案

| 优化项   | 优化前          | 优化后            |
| ----- | ------------ | -------------- |
| 数据结构  | String (2MB) | Hash (按用户ID分片) |
| TTL   | 无过期          | 24小时滑动过期       |
| 单次传输量 | 2MB          | < 20KB         |
| 内存占用  | 92%          | 55%            |
| 缓存命中率 | 60%          | 95%            |

**代码改造示例**：

```java
// 优化前：String 存储所有用户标签
redisTemplate.opsForValue().set("user:tag:ad_space_001", allUserTags);

// 优化后：Hash 分片存储
String shardKey = "user:tag:" + (userId % 100);
redisTemplate.opsForHash().put(shardKey, String.valueOf(userId), userTags);
redisTemplate.expire(shardKey, 24, TimeUnit.HOURS);

// 读取时只获取单个用户
String tags = (String) redisTemplate.opsForHash().get(shardKey, String.valueOf(userId));
```

***

### 案例 2: 同步调用外部风控 API 导致响应慢

#### 现象

| 指标           | 数值            | 状态      |
| ------------ | ------------- | ------- |
| 核心 API 平均 RT | 60ms → 450ms  | ⚠️ 大幅上升 |
| P99 RT       | 150ms → 800ms | ⚠️ 不可接受 |
| TPS          | 5200 → 3800   | ⚠️ 下降明显 |
| CPU 使用率      | 45%           | 正常      |
| 错误率          | 0%            | 正常      |

#### Step 1: 可视化监控定位

```
┌─────────────────────────────────────────────────────────────┐
│  SkyWalking 调用链分析                                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  /api/v1/ad/match  [总耗时: 856ms]                          │
│  │                                                          │
│  ├─ Redis GET user:tag:123        [12ms]   ✓ 正常           │
│  │                                                          │
│  ├─ MySQL SELECT ad_rules          [45ms]  ✓ 正常           │
│  │                                                          │
│  ├─ 业务逻辑匹配                    [23ms]  ✓ 正常           │
│  │                                                          │
│  └─ HTTP 风控API调用               [756ms] ⚠️ 瓶颈          │
│     └─ http://risk-control/check                            │
│         └─ 占总耗时 88%                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Step 2: Arthas 追踪定位

```bash
# 追踪核心方法耗时
trace com.xxx.advfilter.handler.ListJudgeShuffleHandler doJudge '#cost > 100' -n 5

# 输出
`---[856.23ms] cn.xxx.advfilter.handler.ListJudgeShuffleHandler:doJudge()
    +---[12.15ms] cn.xxx.service.UserTagService:getTags()
    +---[45.32ms] cn.xxx.service.AdRuleService:getRules()
    +---[23.45ms] cn.xxx.service.AdMatchService:doMatch()
    `---[756.31ms] cn.xxx.external.RiskControlClient:check()  ← 瓶颈！

# 进一步追踪风控调用
trace cn.xxx.external.RiskControlClient check '#cost > 200' -n 5

# 输出
`---[756.12ms] cn.xxx.external.RiskControlClient:check()
    `---[755.89ms] org.apache.http.impl.client.CloseableHttpClient:execute()
        └─ 同步阻塞等待外部响应
```

#### 根因分析

```
┌─────────────────────────────────────────────────────────────┐
│                    根因链路                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 业务逻辑强依赖风控 API 结果                              │
│     └─ 必须拿到结果才能决定是否展示广告                      │
│                                                             │
│  2. 风控 API 响应慢 (300ms - 1s)                             │
│     └─ 外部系统性能问题，不可控                              │
│                                                             │
│  3. 同步调用阻塞线程                                         │
│     └─ 每个请求都要等待风控返回                              │
│                                                             │
│  4. 线程池被占满                                             │
│     └─ 大量线程处于 WAITING 状态                             │
│                                                             │
│  5. 新请求排队等待                                           │
│     └─ RT 飙升，TPS 下降                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 解决方案

**方案一：异步化改造**

```java
// 优化前：同步调用
public AdResult match(String userId, String adSpaceId) {
    List<Ad> candidates = getCandidates(userId, adSpaceId);
    RiskResult riskResult = riskControlClient.check(userId, candidates);  // 阻塞756ms
    return filterByRisk(candidates, riskResult);
}

// 优化后：异步调用 + CompletableFuture
public CompletableFuture<AdResult> matchAsync(String userId, String adSpaceId) {
    List<Ad> candidates = getCandidates(userId, adSpaceId);
    
    return CompletableFuture.supplyAsync(() -> 
        riskControlClient.check(userId, candidates), 
        riskExecutorService  // 专用线程池
    ).thenApply(riskResult -> 
        filterByRisk(candidates, riskResult)
    ).orTimeout(500, TimeUnit.MILLISECONDS)  // 超时控制
     .exceptionally(ex -> getDefaultAd());    // 降级处理
}
```

**方案二：熔断降级**

```java
// 使用 Sentinel 熔断
@SentinelResource(
    value = "riskControl",
    fallback = "getDefaultAd",
    blockHandler = "handleBlock"
)
public RiskResult check(String userId, List<Ad> candidates) {
    return riskControlClient.check(userId, candidates);
}

// 熔断降级方法
public AdResult handleBlock(String userId, String adSpaceId, BlockException ex) {
    log.warn("风控API熔断，返回兜底广告");
    return getDefaultAd();  // 返回通用兜底广告
}
```

**Sentinel 配置**：

```java
// 熔断规则：响应时间超过500ms触发熔断
DegradeRule rule = new DegradeRule("riskControl")
    .setGrade(CircuitBreakerStrategy.SLOW_REQUEST_RATIO.getType())
    .setCount(500)           // 慢调用阈值500ms
    .setSlowRatioThreshold(0.5)  // 慢调用比例50%
    .setMinRequestAmount(10)     // 最小请求数
    .setStatIntervalMs(10000)    // 统计时长10s
    .setTimeWindow(10);          // 熔断时长10s
```

#### 优化效果

| 指标        | 优化前   | 优化后   |
| --------- | ----- | ----- |
| 核心 API RT | 450ms | 60ms  |
| P99 RT    | 800ms | 150ms |
| TPS       | 3800  | 5200  |
| 风控超时影响    | 阻塞主流程 | 熔断降级  |

***

## 六、排查优先级矩阵

| 现象          | 优先排查           | 工具                             | 典型原因              |
| ----------- | -------------- | ------------------------------ | ----------------- |
| TPS低 + CPU低 | 数据库锁/连接池/外部依赖  | SHOW PROCESSLIST, Arthas trace | 行锁竞争、连接池满、外部API慢  |
| TPS低 + CPU高 | 业务逻辑/GC        | 火焰图, jstat                     | 死循环、频繁GC          |
| RT抖动 + 内存涨  | Redis大Key/内存泄漏 | --bigkeys, jmap                | 大Key、无TTL、内存泄漏    |
| 错误率上升       | 线程池/超时配置       | 应用日志, SkyWalking               | 线程池满、超时配置不当       |
| 连接超时        | 端口耗尽/带宽        | netstat, iftop                 | TIME\_WAIT过多、带宽打满 |
| 缓存命中率下降     | Redis逐出/TTL    | INFO stats, --bigkeys          | 内存满触发逐出、Key过期策略   |

***

## 七、完整排查流程示例

```
┌─────────────────────────────────────────────────────────────────┐
│              性能拐点排查实战流程                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  【现象】5000并发时，TPS 从 5200 降至 3800，RT 从 60ms 升至 450ms │
│                                                                 │
│  Step 1: 看 Grafana 监控面板                                    │
│  ├─ 应用层: CPU 45%, 堆内存 60%, GC正常                        │
│  ├─ 线程池: active=180/200, queue=50 ⚠️                        │
│  ├─ Redis: 内存 92% ⚠️, 命中率 60% ⚠️                          │
│  └─ MySQL: 连接数 45/150, 慢查询 0                              │
│                                                                 │
│  Step 2: 定位到 Redis 内存接近爆满                              │
│  ├─ redis-cli --bigkeys 发现 2MB 大Key                         │
│  ├─ INFO stats 显示 evicted_keys 大量逐出                      │
│  └─ 分析: 大Key + 无TTL → 内存满 → 逐出热数据 → 命中率下降     │
│                                                                 │
│  Step 3: Arthas 追踪确认                                        │
│  ├─ trace 发现 GET user:tag:xxx 耗时 234ms                     │
│  └─ 确认是用户标签存储问题                                      │
│                                                                 │
│  Step 4: 优化                                                   │
│  ├─ String 改 Hash，按用户ID分片                                │
│  ├─ 设置 24小时 TTL                                             │
│  └─ 单次传输从 2MB 降到 <20KB                                   │
│                                                                 │
│  Step 5: 验证                                                   │
│  └─ 再次压测，TPS 稳定在 5200，RT 60ms，内存 55%                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

***

## 八、工具速查表

| 排查方向           | 工具         | 命令/用法                           |
| -------------- | ---------- | ------------------------------- |
| **Redis 大Key** | redis-cli  | `redis-cli --bigkeys`           |
| **Redis 慢查询**  | redis-cli  | `redis-cli SLOWLOG GET 20`      |
| **Redis 内存**   | redis-cli  | `redis-cli INFO memory`         |
| **MySQL 慢查询**  | MySQL      | `SELECT * FROM mysql.slow_log`  |
| **MySQL 锁等待**  | MySQL      | `SHOW ENGINE INNODB STATUS`     |
| **JVM GC**     | jstat      | `jstat -gcutil <pid> 1000`      |
| **线程栈**        | jstack     | `jstack <pid> > dump.txt`       |
| **方法耗时**       | Arthas     | `trace 类名 方法名 '#cost > 100'`    |
| **调用链**        | SkyWalking | 查看 Trace 详情                     |
| **网络流量**       | iftop      | `iftop -i eth0`                 |
| **端口状态**       | netstat    | `netstat -an \| grep TIME_WAIT` |
