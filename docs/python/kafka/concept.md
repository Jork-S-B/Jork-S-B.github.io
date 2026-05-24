## Broker

- 消息队列集群中的一个服务节点，负责接收生产者发送的消息、写入磁盘(持久化)、管理消息分区、以及响应消费者的拉取请求。
- 在 Kafka 中，一个 Broker 就是一个 Kafka 服务进程(一台机器或一个容器)。多个 Broker 组成集群。
- 相当于物流分拨中心

### Q：如果只有一个 Broker，挂了怎么办？

A：导致消息丢失或不可用。所以生产环境至少 3 个 Broker，并配置 replication-factor=3，保证即使一个 Broker 宕机，其他 Broker 上的副本仍可提供服务。

### Q：Broker 和 Topic、Partition 的关系？

A：每个 Partition 只能存在于一个 Broker 上(但可以有多个副本分布在不同 Broker)。多个 Partition 分布在多个 Broker 上，实现并行读写。


## Offset

偏移量：消息在分区内的唯一序号，从0递增，用于标识消息在分区中的位置。

验证堆积：

```shell
# 查看old-topic的offset
docker exec kafka kafka-run-class kafka.tools.GetOffsetShell --bootstrap-server localhost:9092 --topic old-topic --time -1
```

- -time -1 表示获取最新(latest)的 offset，即该分区当前下一条待写入消息的 offset 值(也是分区中消息的总条数)。
- -time -2 表示获取最早 offset(分区第一条消息)
- -time 0 或其他时间戳 表示获取小于等于该时间戳的最大 offset

### 幂等

收到消息 → Redis SISMEMBER 查询 → 存在则丢弃，不存在则处理 → 处理后写入Redis

幂等检查预设的异常场景：

- Kafka 消费者重启，未提交 offset
- 网络抖动导致消费成功但提交 offset 失败
- 手动重放 Topic 中的消息	
