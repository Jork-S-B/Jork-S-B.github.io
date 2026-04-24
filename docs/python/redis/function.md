## 常用方法详解

### String（字符串）- 最基本类型

| 方法                         | 说明         | 示例                              |
|----------------------------|------------|---------------------------------|
| `SET key value`            | 设置键值对      | `r.set('name', 'Alice')`        |
| `GET key`                  | 获取值        | `r.get('name')` → `'Alice'`     |
| `MSET key1 val1 key2 val2` | 批量设置       | `r.mset({'a': 1, 'b': 2})`      |
| `MGET key1 key2`           | 批量获取       | `r.mget(['a', 'b'])` → `[1, 2]` |
| `INCR key`                 | 值加 1（原子操作） | `r.incr('counter')`             |
| `DECR key`                 | 值减 1       | `r.decr('counter')`             |
| `INCRBY key amount`        | 增加指定值      | `r.incrby('score', 10)`         |
| `EXPIRE key seconds`       | 设置过期时间     | `r.expire('token', 3600)`       |
| `TTL key`                  | 查看剩余过期时间   | `r.ttl('token')`                |

### Hash（哈希）- 适合存储对象

| 方法                         | 说明       | 示例                                               |
|----------------------------|----------|--------------------------------------------------|
| `HSET key field value`     | 设置字段值    | `r.hset('user:1', 'name', 'Bob')`                |
| `HGET key field`           | 获取字段值    | `r.hget('user:1', 'name')`                       |
| `HMSET key dict`           | 批量设置字段   | `r.hmset('user:1', {'name': 'Bob', 'age': 25})`  |
| `HGETALL key`              | 获取所有字段   | `r.hgetall('user:1')` → `{b'name': b'Bob', ...}` |
| `HDEL key field`           | 删除字段     | `r.hdel('user:1', 'age')`                        |
| `HEXISTS key field`        | 判断字段是否存在 | `r.hexists('user:1', 'name')` → `True`           |
| `HINCRBY key field amount` | 字段值增加    | `r.hincrby('user:1', 'score', 5)`                |

### List（列表）- 有序可重复

| 方法                     | 说明       | 示例                          |
|------------------------|----------|-----------------------------|
| `LPUSH key value`      | 从左侧插入    | `r.lpush('tasks', 'task1')` |
| `RPUSH key value`      | 从右侧插入    | `r.rpush('tasks', 'task2')` |
| `LPOP key`             | 从左侧弹出    | `r.lpop('tasks')`           |
| `RPOP key`             | 从右侧弹出    | `r.rpop('tasks')`           |
| `LRANGE key start end` | 获取范围元素   | `r.lrange('tasks', 0, -1)`  |
| `LLEN key`             | 列表长度     | `r.llen('tasks')`           |
| `LINDEX key index`     | 获取指定索引元素 | `r.lindex('tasks', 0)`      |

### Set（集合）- 无序不重复

| 方法                      | 说明       | 示例                                                |
|-------------------------|----------|---------------------------------------------------|
| `SADD key member`       | 添加成员     | `r.sadd('processed_ids', 'msg123')`               |
| `SISMEMBER key member`  | 检查成员是否存在 | `r.sismember('processed_ids', 'msg123')` → `True` |
| `SCARD key`             | 集合大小     | `r.scard('processed_ids')` → `42`                 |
| `SMEMBERS key`          | 获取所有成员   | `r.smembers('processed_ids')`                     |
| `SREM key member`       | 删除成员     | `r.srem('processed_ids', 'msg123')`               |
| `SINTER key1 key2`      | 交集       | `r.sinter('set1', 'set2')`                        |
| `SUNION key1 key2`      | 并集       | `r.sunion('set1', 'set2')`                        |
| `SDIFF key1 key2`       | 差集       | `r.sdiff('set1', 'set2')`                         |
| `SRANDMEMBER key count` | 随机获取成员   | `r.srandmember('set1', 3)`                        |

### Sorted Set（有序集合）- 带分数的集合

| 方法                          | 说明       | 示例                                           |
|-----------------------------|----------|----------------------------------------------|
| `ZADD key score member`     | 添加成员及分数  | `r.zadd('leaderboard', {'Alice': 100})`      |
| `ZRANGE key start end`      | 按分数升序获取  | `r.zrange('leaderboard', 0, -1)`             |
| `ZREVRANGE key start end`   | 按分数降序获取  | `r.zrevrange('leaderboard', 0, 9)`           |
| `ZRANK key member`          | 获取排名（升序） | `r.zrank('leaderboard', 'Alice')`            |
| `ZSCORE key member`         | 获取分数     | `r.zscore('leaderboard', 'Alice')` → `100.0` |
| `ZCARD key`                 | 集合大小     | `r.zcard('leaderboard')`                     |
| `ZINCRBY key amount member` | 增加分数     | `r.zincrby('leaderboard', 10, 'Alice')`      |

### 通用操作

| 方法                  | 说明      | 示例                          |
|---------------------|---------|-----------------------------|
| `EXISTS key`        | 键是否存在   | `r.exists('name')` → `True` |
| `DEL key`           | 删除键     | `r.delete('name')`          |
| `KEYS pattern`      | 匹配键名    | `r.keys('user:*')`          |
| `TYPE key`          | 获取键类型   | `r.type('mykey')` → `'set'` |
| `RENAME key newkey` | 重命名     | `r.rename('old', 'new')`    |
| `RANDOMKEY`         | 随机返回一个键 | `r.randomkey()`             |

### 事务与管道

| 方法           | 说明         | 示例                                               |
|--------------|------------|--------------------------------------------------|
| `PIPELINE()` | 创建管道（批量执行） | `pipe = r.pipeline()`                            |
| `MULTI/EXEC` | 事务         | `pipe.multi().set('a', 1).set('b', 2).execute()` |
| `WATCH key`  | 乐观锁        | `r.watch('counter')`                             |
