* 非关系型数据库，作为关系型数据库的补充，使用键值对存储数据。
* 降低磁盘IO，内存存储。
* 广泛用于缓存、消息队列、排行榜等场景。

## Redis常用指令

连接到远程Redis服务器：`./redis-cli -h ip -p port -a password`

|        指令         | 说明                 |
|:-----------------:|:-------------------|
|      keys *       | 查看所有的键             |
|      dbsize       | 键总数                |
|    exists key     | 检查键是否存在。存在：1，不存在：0 |
|      del key      | 删除键。删除成功：1，删除失败：0  |
|     type key      | 键的数据结构类型           |
| rename key newkey | 重命名键               |
|   set key value   | 设置值                |
|      get key      | 丨获取对应键的值           |
|      flushdb      | 清除当前数据库            |
|     flushall      | 清除所有数据库            |
|    info memory    | 查询内存使用情况           |

清除指定redis：`for i in $(seq 1001 1003)： do echo "flushab" | ./redis-cli -h ip -a password -p $i; done`

## Redis集群方案

* 哨兵模式，基于主从，哨兵-集群监控、消息通知、故障转移、配置中心，不保证数据零丟失，只能保证高可用。
* Redis Cluster，数据分片存储在多个互为主从的多节点上，数据写入主节点，再同步到从节点，不保证强一致性。
* Redis Sharding

---
