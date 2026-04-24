## 核心方法详解

### 1. Producer.produce() - 发送消息

produce() 是异步的，消息先入缓冲区后由后台发送。

为了保证不丢失，程序退出前必须调用 flush()；如果需要实时处理每条结果的回调，需要定期调用 poll()。

```python
producer.produce(
    topic, 
    value=json.dumps(msg).encode("utf-8"), 
    callback=delivery_report
)
```

**完整参数：**
```python
producer.produce(
    topic='my-topic',           # 主题名（必需）
    value=b'message data',      # 消息值（字节）
    key=b'message-key',         # 消息键（可选，用于分区）
    partition=-1,               # 指定分区（-1=自动）
    timestamp=None,             # 时间戳（None=当前时间）
    headers=[('key', b'value')], # 消息头（可选）
    callback=delivery_report    # 发送回调
)
```

### 2. Producer.poll() - 生产者轮询，获取回调

**作用：**
- 处理已发送消息的确认和回调
- 触发 delivery_report 回调函数
- 清理内部状态

**参数说明：**
```python
producer.poll(timeout)
# timeout: 等待时间（秒）
# 0 = 非阻塞，立即返回
# 1.0 = 阻塞最多1秒
```

**为什么需要 poll？**
```python
# 错误示例 - 没有poll，回调永远不会执行
producer.produce(topic, value=msg, callback=delivery_report)
# delivery_report 永远不会被调用！

# 正确示例 - 定期poll触发回调
producer.produce(topic, value=msg, callback=delivery_report)
producer.poll(0)  # 触发回调
```

**最佳实践：**
```python
# 高频场景 - 每N条poll一次
for i in range(total):
    producer.produce(topic, value=msg, callback=delivery_report)
    if i % 100 == 0:
        producer.poll(0)  # 非阻塞触发回调

# 低频场景 - 每次发送后poll
producer.produce(topic, value=msg, callback=delivery_report)
producer.poll(1.0)  # 阻塞等待确认
```

### 3. Producer.flush() - 清空缓冲区，阻塞直至消息发送完成

**作用：**
- 阻塞直到所有缓冲消息发送完成
- 确保程序退出前消息全部发送
- 常用于优雅关闭

```python
# 优雅关闭
try:
    for msg in messages:
        producer.produce(topic, value=msg)
finally:
    producer.flush()  # 确保所有消息发送完成
    producer.close()  # 关闭连接
```

### 4. Consumer.commit(msg) - 消费者提交偏移量

**作用：**
- 提交已处理消息的偏移量
- 确保消费者重启后从正确位置继续
- 实现精确一次处理语义

**提交方式对比：**

```python
# 方式1: 自动提交（enable.auto.commit=True）
# Kafka自动定期提交，可能丢失消息或重复处理

# 方式2: 手动提交当前消息
consumer.commit(msg)  # 提交特定消息的offset

# 方式3: 手动提交当前分区位置
consumer.commit()  # 提交最后消费的offset

# 方式4: 异步提交
consumer.commit(asynchronous=True)  # 不等待提交完成
```

**最佳实践：**
```python
# 精确一次处理 - 每处理一条提交一次
for msg in consumer:
    value = process_message(msg)
    consumer.commit(msg)  # 处理成功后立即提交

# 批量处理 - 每N条提交一次（性能更好）
count = 0
for msg in consumer:
    value = process_message(msg)
    count += 1
    if count % 100 == 0:
        consumer.commit()  # 批量提交
```

### 5. Consumer.poll() - 消费消息

```python
# 消费者核心方法
msg = consumer.poll(timeout=1.0)
```

**返回值：**
```python
msg = consumer.poll(timeout=1.0)

if msg is None:
    # 超时，没有新消息
    continue
if msg.error():
    # 发生错误
    print(f"Error: {msg.error()}")
else:
    # 正常消息
    print(f"Received: {msg.value()}")
```

### 6. 其他常用方法

#### Producer
```python
# 获取生产者配置信息
print(producer.list_topics())

# 关闭生产者
producer.close()

# 获取内部队列长度
print(len(producer))  # 缓冲消息数
```

#### Consumer
```python
# 订阅主题
consumer.subscribe(['topic1', 'topic2'])

# 取消订阅
consumer.unsubscribe()

# 获取当前分配分区
partitions = consumer.assignment()

# 手动分配分区
from confluent_kafka import TopicPartition
consumer.assign([TopicPartition('topic', 0)])

# 获取主题元数据
metadata = consumer.list_topics()

# 关闭消费者
consumer.close()
```

### 7. 完整示例对比

#### 生产者最佳实践
```python
from confluent_kafka import Producer

def delivery_report(err, msg):
    if err:
        print(f"发送失败: {err}")
    else:
        print(f"发送成功: {msg.topic()} [{msg.partition()}] offset={msg.offset()}")

conf = {
    'bootstrap.servers': 'localhost:9092',
    'acks': 'all',
    'retries': 3,
    'batch.size': 16384,
    'linger.ms': 10,
    'compression.type': 'lz4'
}

producer = Producer(conf)

try:
    for i in range(10000):
        producer.produce(
            'my-topic',
            value=f'message-{i}'.encode(),
            key=f'key-{i}'.encode(),
            callback=delivery_report
        )
        
        # 定期poll触发回调
        if i % 100 == 0:
            producer.poll(0)
            
finally:
    # 确保所有消息发送完成
    producer.flush()
    producer.close()
```

#### 消费者最佳实践
```python
from confluent_kafka import Consumer, KafkaException

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False  # 手动提交
}

consumer = Consumer(conf)
consumer.subscribe(['my-topic'])

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                continue
            else:
                print(f"Consumer error: {msg.error()}")
                break
        
        # 处理消息
        try:
            value = msg.value().decode('utf-8')
            print(f"Received: {value}")
            
            # 处理成功后提交
            consumer.commit(msg)
            
        except Exception as e:
            print(f"Process error: {e}")
            # 处理失败，不提交offset，消息会重新消费
            
finally:
    consumer.close()
```

### 8. 性能调优建议

```python
# 高吞吐生产者配置
high_throughput_conf = {
    'batch.size': 65536,        # 64KB
    'linger.ms': 20,            # 20ms
    'compression.type': 'lz4',  # 快速压缩
    'max.in.flight.requests.per.connection': 5,
    'queue.buffering.max.messages': 1000000
}

# 低延迟生产者配置
low_latency_conf = {
    'batch.size': 16384,        # 16KB
    'linger.ms': 0,             # 立即发送
    'compression.type': 'none', # 不压缩
    'acks': 1                   # 只等leader确认
}
```

