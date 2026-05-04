## 📌 核心特性

### 1. 数据结构丰富

- **String**：字符串、计数器、分布式锁
- **Hash**：对象存储、购物车
- **List**：消息队列、时间线
- **Set**：去重、共同好友
- **Sorted Set**：排行榜、延迟队列
- **Bitmap**：用户签到、状态标记
- **HyperLogLog**：UV 统计
- **Geo**：地理位置计算
- **Stream**：消息队列（Kafka 轻量替代）

### 2. 高性能

- 纯内存操作，读写速度 **10万+ QPS**
- 单线程模型（Redis 6 前），避免上下文切换
- IO 多路复用（epoll）

### 3. 持久化机制

| 方式        | 原理      | 优点      | 缺点         |
|-----------|---------|---------|------------|
| **RDB**   | 定时快照    | 恢复快、文件小 | 可能丢失数据     |
| **AOF**   | 记录写命令   | 数据更安全   | 文件大、恢复慢    |
| **混合持久化** | RDB+AOF | 兼顾两者    | Redis 4.0+ |

### 4. 高可用架构

- **主从复制**：读写分离
- **Sentinel（哨兵）**：基于主从，哨兵-集群监控、消息通知、故障转移、配置中心，不保证数据零丟失，只能保证高可用。
- **Cluster（集群）**：数据分片、水平扩展；数据分片存储在多个互为主从的多节点上，数据写入主节点，再同步到从节点，不保证强一致性。

### 5. 其他特性

- **事务**：`MULTI/EXEC`（不支持回滚）
- **发布订阅**：`PUB/SUB`
- **Lua 脚本**：原子操作
- **过期策略**：惰性删除 + 定期删除
- **内存淘汰策略**：LRU/LFU/TTL 等

## 📌 测试关注点

### 1. 功能测试

#### 1.1 数据结构测试

验证各数据结构的增删改查、边界值（空集合、超大元素）  

例如：Set 的 `sadd` 重复添加是否幂等、`scard` 计数是否正确

```python
# Set 去重测试
def test_set_deduplication():
    r.sadd("users", "user1", "user2", "user1")  # 检查重复添加幂等
    assert r.scard("users") == 2  # 应该去重，检查计数正确


# List 边界测试
def test_list_boundaries():
    r.lpush("queue", "item1")
    r.lpop("queue")
    assert r.llen("queue") == 0  # 空列表
    assert r.lpop("queue") is None  # 空列表弹出
```

#### 1.2 过期时间测试

```python
def test_key_expiration():
    r.setex("temp_key", 2, "value")  # 2秒过期
    assert r.get("temp_key") == b"value"
    time.sleep(3)
    assert r.get("temp_key") is None  # 已过期
```

---

### 2. 性能测试 ⭐ 重点

#### 2.1 测试指标

| 指标       | 说明         | 参考值       |
|----------|------------|-----------|
| **QPS**  | 每秒查询数      | 10万+      |
| **TPS**  | 每秒事务数      | 5万+       |
| **响应时间** | P99 < 10ms | P99 < 5ms |
| **吞吐量**  | 网络带宽       | 100MB/s+  |
| **内存使用** | 内存增长率      | 稳定        |

#### 2.2 压测工具

```bash
# redis-benchmark（官方工具）
redis-benchmark -h 127.0.0.1 -p 6379 -c 100 -n 100000 -q

# 参数说明：
# -c 100：100个并发连接
# -n 100000：每个命令执行10万次
# -q：安静模式
# -t：指定命令类型
redis-benchmark -t set,get -n 100000 -q
```

#### 2.3 Python 压测示例

```python
import redis
import time
from concurrent.futures import ThreadPoolExecutor


def benchmark_redis():
    r = redis.Redis(host='localhost', port=6379)

    # 测试 SET 性能
    start = time.time()
    for i in range(100000):
        r.set(f"key:{i}", f"value:{i}")
    duration = time.time() - start

    print(f"SET QPS: {100000 / duration:.2f}")

    # 测试并发性能
    def worker(i):
        r = redis.Redis()
        r.set(f"concurrent:{i}", i)

    start = time.time()
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(worker, range(10000))
    print(f"并发 QPS: {10000 / (time.time() - start):.2f}")
```

#### 2.4 性能测试场景/典型场景

- 大Key
- 热Key
- Pipeline批量操作
- 慢查询监控

```python
# 1. 大 Key 测试（>10KB）
def test_big_key_performance():
    big_value = "x" * 1024 * 1024  # 1MB
    r.set("big_key", big_value)
    # 观察响应时间是否显著增加


# 2. 热 Key 测试
def test_hot_key():
    r.set("hot_key", "value")
    # 1000并发同时读取同一个key
    # 观察是否成为瓶颈


# 3. Pipeline 批量操作
def test_pipeline():
    pipe = r.pipeline()
    for i in range(10000):
        pipe.set(f"batch:{i}", i)
    pipe.execute()  # 一次性发送
```

---

### 3. 异常测试

#### 3.1 内存溢出

验证各内存淘汰策略是否符合预期

- `noeviction`：不淘汰，返回错误
- `allkeys-lru`：淘汰最少使用（推荐）
- `volatile-lru`：只淘汰设了过期时间的
- `allkeys-lfu`：淘汰最不频繁使用
- `volatile-ttl`：淘汰即将过期的
- `random`：随机淘汰

```python
def test_memory_limit():
    # 配置 maxmemory 100MB
    # 测试内存淘汰策略
    r.config_set("maxmemory", "100mb")
    r.config_set("maxmemory-policy", "allkeys-lru")

    # 持续写入直到触发淘汰
    for i in range(1000000):
        r.set(f"mem_test:{i}", "x" * 1024)

    # 验证旧数据是否被淘汰
    assert r.exists("mem_test:0") == False  # 可能被淘汰
```

#### 3.2 网络异常

模拟网络异常，测试重连机制

```python
def test_network_failure():
    r = redis.Redis(socket_timeout=2, socket_connect_timeout=2)

    # 模拟网络断开
    try:
        r.set("key", "value")
    except redis.ConnectionError:
        print("连接失败，测试重连机制")

    # 测试断线重连
    r = redis.Redis(retry_on_timeout=True)
```

#### 3.3 持久化失败

模拟宕机（kill -9）、重启 Redis，比对恢复前后数据

```python
def test_persistence_failure():
    # 禁用 AOF
    r.config_set("appendonly", "no")

    # 写入数据后重启
    r.set("important", "data")
    # 手动 kill Redis 进程 （kill -9）
    # 重启后验证数据是否丢失
```

---

### 4. 安全测试

#### 4.1 认证测试

```python
def test_authentication():
    # 未认证访问
    r = redis.Redis()
    try:
        r.get("key")  # 应该失败
    except redis.ResponseError:
        pass

    # 正确认证
    r = redis.Redis(password="your_password")
    r.get("key")  # 成功
```

#### 4.2 命令注入

```python
def test_command_injection():
    # 测试特殊字符注入
    malicious_key = "key; FLUSHALL"
    r.set(malicious_key, "value")  # 应该当作普通key

    # 测试 Lua 脚本注入
    malicious_script = "'; os.execute('rm -rf /')"
    try:
        r.eval(malicious_script, 0)
    except redis.ResponseError:
        pass  # 应该被拦截
```

#### 4.3 危险命令

```python
def test_dangerous_commands():
    # 测试 FLUSHALL/FLUSHDB
    # 企业应禁用这些命令
    r.config_set("rename-command", "FLUSHALL", "")

    # 测试 KEYS *（阻塞单线程）
    # 应使用 SCAN 替代
    for key in r.scan_iter("pattern:*"):
        pass
```

---

### 5. 高可用测试

#### 5.1 主从切换

```python
def test_master_slave_failover():
    # 1. 写入主节点
    master.set("failover_test", "value")

    # 2. 停止主节点
    stop_redis(master_port)

    # 3. 等待哨兵选举新主
    time.sleep(10)

    # 4. 从新主节点读取
    new_master = get_new_master()
    assert new_master.get("failover_test") == b"value"
```

#### 5.2 集群测试

```python
def test_cluster_operations():
    from rediscluster import RedisCluster

    rc = RedisCluster(host='localhost', port=7000)

    # 测试跨节点操作
    rc.set("key1", "value1")  # 可能在节点1
    rc.set("key2", "value2")  # 可能在节点2

    # 测试多 Key 操作（必须在同一 slot）
    rc.mset({"{user}:name": "Alice", "{user}:age": 25})  # hash tag
```

---

### 6. 事务测试

#### 6.1 基本事务

```python
def test_transaction():
    pipe = r.pipeline()
    pipe.multi()
    pipe.set("a", 1)
    pipe.set("b", 2)
    results = pipe.execute()

    assert results == [True, True]
```

#### 6.2 乐观锁（WATCH）

```python
def test_watch_transaction():
    r.set("counter", 0)

    # 线程1
    pipe = r.pipeline()
    pipe.watch("counter")
    current = int(r.get("counter"))
    pipe.multi()
    pipe.set("counter", current + 1)

    # 模拟并发修改
    r.set("counter", 999)

    try:
        pipe.execute()  # 应该失败（WatchError）
    except redis.WatchError:
        print("事务回滚，数据被其他客户端修改")
```

---

### 7. 数据一致性

- 缓存与数据库双写：测试先更新 DB 后删缓存 vs 先删缓存后更新 DB 的差异  
- 主从延迟导致读取旧数据：结合业务场景判断是否可接受  
- 幂等与去重：用 Redis Set 做幂等，测试重复消息是否被正确过滤，Set 的 `sadd` 原子性保证

---

### 测试检查清单

```
✅ 功能测试
  ├─ 五种数据结构命令覆盖
  ├─ 边界值（空值、超长、特殊字符）
  ├─ 过期时间准确性
  └─ 事务原子性

✅ 性能测试
  ├─ QPS/TPS 达标
  ├─ P99 响应时间 < 10ms
  ├─ 大 Key 性能影响
  ├─ 热 Key 并发测试
  └─ Pipeline 批量操作

✅ 异常测试
  ├─ 内存溢出处理
  ├─ 网络断线重连
  ├─ 持久化失败恢复
  └─ 主从切换数据一致性

✅ 安全测试
  ├─ 认证授权
  ├─ 命令注入防护
  ├─ 危险命令禁用
  └─ 数据加密传输

✅ 高可用测试
  ├─ 哨兵自动故障转移
  ├─ 集群节点扩缩容
  ├─ 数据分片均衡性
  └─ 跨机房延迟
```

---

## 📌 Q&A

### Q: Redis 为什么快？

A：

1. 纯内存操作
2. 单线程避免上下文切换和竞争条件
3. IO 多路复用（epoll）
4. 高效的数据结构（SDS、跳表、压缩列表）

### Q: Redis 是单线程，为什么还能高并发？

A：

- IO 多路复用同时监听多个 socket
- 非阻塞 IO 操作
- 内存操作极快（纳秒级）
- Redis 6 引入多线程处理网络 IO

### Q: 缓存穿透/击穿/雪崩怎么解决？

| 问题     | 原因          | 解决方案       |
|--------|-------------|------------|
| **穿透** | 查询不存在的数据    | 布隆过滤器、缓存空值 |
| **击穿** | 热点 Key 过期   | 互斥锁、逻辑过期   |
| **雪崩** | 大量 Key 同时过期 | 随机过期时间、集群  |

#### 布隆过滤器
    
RedisBloom，一种空间效率极高的概率型数据结构，用于判断一个元素是否在一个集合中。

- 快速判断：可以告诉你一个元素"一定不存在"或"可能存在"
- 空间高效：相比哈希表、树等传统数据结构，占用空间极小
- 有误判率：可能将不存在的元素误判为存在（假阳性），但不会将存在的元素误判为不存在（无假阴性）

应用场景

- 缓存穿透防护：在数据库前加布隆过滤器，避免查询不存在的数据
- 网页爬虫去重：判断 URL 是否已爬取
- 垃圾邮件过滤：快速判断邮件地址是否在黑名单中
- 分布式系统：减少网络请求，如 HBase、Cassandra 等使用它来减少磁盘 IO

```shell
# 添加元素
BF.ADD myfilter item1

# 检查元素是否存在
BF.EXISTS myfilter item1  # 返回 1(可能存在) 或 0(一定不存在)

# 批量操作
BF.MADD myfilter item1 item2 item3
BF.MEXISTS myfilter item1 item2

```

### Q: 如何保证缓存和数据库一致性？

A：

1. **先更新数据库，再删除缓存**（推荐）
2. 延迟双删
3. 订阅 binlog 异步更新（Canal）
4. 设置合理的过期时间

---

## 📌 实战建议

### 企业测试工具推荐

1. **redis-benchmark**：官方压测工具
2. **memtier_benchmark**：更强大的压测（支持混合读写）
3. **RedisInsight**：官方可视化工具
4. **RedisShake**：数据迁移和同步测试

### 常用命令

连接到远程Redis服务器：`./redis-cli -h ip -p port -a password`

|          指令           | 说明                 |
|:---------------------:|:-------------------|
|        keys *         | 查看所有的键             |
|        dbsize         | 键总数                |
|      exists key       | 检查键是否存在。存在：1，不存在：0 |
|        del key        | 删除键。删除成功：1，删除失败：0  |
|       type key        | 键的数据结构类型           |
|   rename key newkey   | 重命名键               |
|     set key value     | 设置值                |
|        get key        | 获取对应键的值            |
|        flushdb        | 清除当前数据库            |
|       flushall        | 清除所有数据库            |
|      info memory      | 查询内存使用情况           |
| CONFIG get maxclients | 查最大连接数             |

清除指定redis：`for i in $(seq 1001 1003)： do echo "flushab" | ./redis-cli -h ip -a password -p $i; done`

#### 监控指标

```bash
# 关键监控命令
redis-cli INFO stats        # 统计信息
redis-cli INFO memory       # 内存使用
redis-cli INFO clients      # 客户端连接
redis-cli INFO replication  # 主从状态

# 设置慢查询阈值为 100ms
redis-cli config set slowlog-log-slower-than 100000
# 获取最近 10 条慢查询
redis-cli slowlog get 10
```

## 📌 性能指标

* Latency - redis响应一个请求的时间
* instantaneous_ops_pers_sec - 每秒处理请求数
* hi rate(calculated) - 缓存命中率

### 🚁 缓存击穿

指**某个**热点数据在缓存中过期的瞬间，大量并发请求直接穿透到数据库，可能导致数据库压力骤增甚至崩溃。

常见原因:

1. 业务代码或数据有问题。
2. 恶意攻击、爬虫等造成大量空命中。

解决方案:

1. 永不过期策略
2. 错峰过期
3. 逻辑过期时间：当数据过期时，异步更新数据而不阻塞请求。
4. 使用布隆过滤器快速判断数据是否存在，避免无效请求穿透到数据库。
5. 加互斥锁：当缓存失效时，只允许一个线程去加载数据，其他线程等待。
6. 缓存预热：在系统启动或低峰期预先加载热点数据到缓存。

### 🚁 缓存雪崩

指在某个时间段内，**大量**的缓存同时失效或者Redis服务宕机后恢复，导致所有请求都直接访问数据库，从而引发数据库连接或性能瓶颈，甚至宕机。

常见原因:

1. 集中过期：设置了相同的过期时间，导致大量缓存同时失效。
2. Redis宕机：Redis服务异常或网络中断，导致所有缓存不可用。
3. 缓存层故障转移失败：如集群部署时节点宕机未及时恢复。

解决方案:

1. 上述缓存击穿的解决方案
2. 熔断限流（服务降级），在访问数据库前加入熔断机制，当请求超过阈值时直接返回错误或默认值，防止数据库被压垮。
3. 缓存高可用架构（主从、集群）
4. 多级缓存架构（本地缓存+redis缓存）

---

