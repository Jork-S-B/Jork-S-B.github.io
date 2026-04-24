## Broker

- 消息队列集群中的一个服务节点，负责接收生产者发送的消息、写入磁盘（持久化）、管理消息分区、以及响应消费者的拉取请求。
- 在 Kafka 中，一个 Broker 就是一个 Kafka 服务进程（一台机器或一个容器）。多个 Broker 组成集群。
- 相当于物流分拨中心

### Q：如果只有一个 Broker，挂了怎么办？

A：导致消息丢失或不可用。所以生产环境至少 3 个 Broker，并配置 replication-factor=3，保证即使一个 Broker 宕机，其他 Broker 上的副本仍可提供服务。

### Q：Broker 和 Topic、Partition 的关系？

A：每个 Partition 只能存在于一个 Broker 上（但可以有多个副本分布在不同 Broker）。多个 Partition 分布在多个 Broker 上，实现并行读写。


