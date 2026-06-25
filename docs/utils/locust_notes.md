基于事件和异步操作，使用协程的方式模拟用户请求。

当一个协程执行完成后会主动让出，让另一个协程开始执行，而线程切换是受系统控制，所以协程切换的代价远比线程切换的代价小的多。

因此Locust可以达到更高数量级的并发。

单台4核8G的服务器，Locust虚拟用户数可达到25000，是JMeter的5倍。

## 📌 使用Locust压测

=== "demo.py"

    ```python
    import os
    from locust import HttpUser, task
    
    class VUser(HttpUser):
        host = 'http://127.0.0.1:8080'
        
        @task
        def index(self):
            # name相同时，结果树图表会合并显示为一条
            self.client.get('/login', name='login')
            self.client.get('/favicon.ico', name='index')
            
    if __name__ == '__main__':
        # 运行后根据打印的url，设置用户数、每秒启动的用户数（Spawn rate）并执行。
        os.system('locust -f demo.py --web-host "127.0.0.1"')
    ```

=== "simulation.py"
    
    ```python
    import os
    from locust import HttpUser, task, between, constant_throughput
    
    class VUser(HttpUser):
        host = 'http://127.0.0.1:8080'
        # 每个用户请求之间等待0.5秒到10秒
        wait_time = between(0.5, 10)
        # 每个用户每10秒执行一次任务（0.1次/秒），以测试系统在稳定流量下的表现，避免瞬间高并发冲击服务
        wait_time = constant_throughput(0.1)
        
        # @task(3)表示该任务的执行权重，以模拟用户行为的优先级和分布比例
        @task(3)
        def task1(self):
            self.client.get('/favicon.ico', name='index')
            
        @task
        def task2(self):
            pass
        
        # 虚拟用户启动前会调用该方法
        def on_start(self):
            self.client.post('/loginReq', data={"username": "admin", "password": "admin"})
            # 将token存到变量
            pass
    
    @events.test_start.add_listener
    def on_test_start(environment, **kwargs):
        print(f"开始压测，当前时间为: {time.strftime('%H:%M:%S')}")

    @events.test_stop.add_listener
    def on_test_stop(environment, **kwargs):
        print(f"压测结束，当前时间为: {time.strftime('%H:%M:%S')}")

    @events.init.add_listener
    def on_locust_init(environment, **kwargs):
        print(f"当前环境为: {environment.environment_type}")
        
    if __name__ == '__main__':
        os.system('locust -f simulation.py -u 200 -r 20 -t 3m --web-host "127.0.0.1"')
    ```
    
=== "weight.py"
    
    ```python
    import os
    from locust import HttpUser, task
    
    class VUser1(HttpUser):
        weight = 3  # 多个用例设置权重
        fixed_count = 1  # 固定用户数
    
        @task
        def task(self):
            pass
    
     class VUser2(HttpUser):
        weight = 1
    
        @task
        def task(self):
            pass
    
    if __name__ == '__main__':
        os.system('locust -f weight.py -u 200 -r 20 -t 3m --web-host "127.0.0.1"')
    ```

=== "assert_res.py"

    ```python
    import os
    from locust import HttpUser, task
    
    
    class VUser(HttpUser):
        host = 'http://127.0.0.1:8080'
    
        def task(self):
            with self.client.post('/login', data={"username": "admin", "password": "admin"},
                                  catch_response=True) as response:
                try:
                    if response.json()['code'] != 0:
                        response.failure('登录失败')
                except JSONDecodeError:
                    response.failure('返回数据格式错误')
                except KeyError:
                    response.failure('返回数据缺少字段')
            self.client.get('/favicon.ico', name='index')
    
    
    if __name__ == '__main__':
        os.system('locust -f assert_res.py -u 200 -r 20 -t 3m --web-host "127.0.0.1"')
    ```

=== "tag.py"

    ```python
    import os
    from locust import HttpUser, task, tags
    
    # 与继承HttpUser相比，API相同但执行效率更高
    class VUser(FastHttpUser):
        host = 'http://127.0.0.1:8080'
        
        @tags('tag1', 'tag2')
        @task
        def task1(self):
            self.client.get('/favicon.ico', name='index')
            
    if __name__ == '__main__':
        # 筛选tag1、tag2，排除tag3的任务后执行
        os.system('locust -f tag.py -u 200 -r 20 -t 3m --tags tag1 tag2 --exclude tag3 --web-host "127.0.0.1"')
    ```

---

## 一、Locust的权重机制

### 1.1 权重定义方式

Locust通过`@task(weight)`装饰器来模拟真实用户的操作频率：

```python
@task(10)  # 权重10 - 最常见操作
def query_user_info(self):
    ...

@task(8)   # 权重8 - 常见操作
def query_product_info(self):
    ...

@task(5)   # 权重5 - 中等频率
def query_order_list(self):
    ...

@task(3)   # 权重3 - 较低频率
def create_order(self):
    ...

@task(1)   # 权重1 - 低频率
def query_inventory(self):
    ...
```

### 1.2 实际执行比例计算

权重总和：10 + 8 + 5 + 3 + 1 = 27

各任务执行比例：
- `query_user_info`：10/27 = 37.0%
- `query_product_info`：8/27 = 29.6%
- `query_order_list`：5/27 = 18.5%
- `create_order`：3/27 = 11.1%
- `query_inventory`：1/27 = 3.7%

### 1.3 权重机制的本质

**Locust的权重机制本质上是概率分布**：
- 每个虚拟用户在每次迭代时，根据权重随机选择下一个要执行的任务
- 权重越高，被选中的概率越大
- 长期运行后，各任务的执行次数比例趋近于权重比例

---

## 二、JMeter如何实现权重场景？

JMeter有**多种方式**实现类似的权重控制：

### 方式1：Throughput Controller（推荐）

#### 2.1.1 配置结构

```
Test Plan
├── Thread Group (100 users)
    ├── Throughput Controller (37.0%) - 查询用户信息
    │   └── HTTP Request: /user/users/${user_id}
    ├── Throughput Controller (29.6%) - 查询商品信息
    │   └── HTTP Request: /product/products/${product_id}
    ├── Throughput Controller (18.5%) - 查询订单列表
    │   └── HTTP Request: /order/orders/user/${user_id}
    ├── Throughput Controller (11.1%) - 创建订单
    │   └── HTTP Request: POST /order/orders
    └── Throughput Controller (3.7%) - 查询库存
        └── HTTP Request: /inventory/inventory/${product_id}
```

#### 2.1.2 配置步骤

1. **添加Thread Group**
   - 右键 Test Plan → Add → Threads (Users) → Thread Group
   - 设置 Number of Threads (users): 100
   - 设置 Ramp-Up Period: 10

2. **添加Throughput Controller**
   - 右键 Thread Group → Add → Logic Controller → Throughput Controller
   - 配置参数：
     - Name: "查询用户信息"
     - Throughput: 37.0
     - Units: "percent executions"

3. **添加HTTP Request**
   - 右键 Throughput Controller → Add → Sampler → HTTP Request
   - 配置请求参数

#### 2.1.3 Throughput Controller参数说明

| 参数 | 说明 |
|------|------|
| **Name** | 控制器名称 |
| **Throughput** | 执行百分比或执行次数 |
| **Units** | - "percent executions"：按百分比执行<br>- "executions"：按固定次数执行 |
| **Per User** | 是否每个用户独立计算 |

---

### 方式2：Weighted Switch Controller（需插件）

#### 2.2.1 安装JMeter Plugins

1. 下载 JMeter Plugins：https://jmeter-plugins.org/
2. 将 `JMeterPlugins-Standard.jar` 放入 `lib/ext` 目录
3. 重启JMeter

#### 2.2.2 配置示例

```xml
<com.blazemeter.jmeter.controller.WeightedSwitchController guiclass="com.blazemeter.jmeter.controller.WeightedSwitchControllerGui">
  <collectionProp name="WeightedSwitchController.weights">
    <stringProp>10</stringProp>  <!-- 查询用户信息 -->
    <stringProp>8</stringProp>   <!-- 查询商品信息 -->
    <stringProp>5</stringProp>   <!-- 查询订单列表 -->
    <stringProp>3</stringProp>   <!-- 创建订单 -->
    <stringProp>1</stringProp>   <!-- 查询库存 -->
  </collectionProp>
  
  <elementProp name="查询用户信息" elementType="HTTP Request">
    <stringProp name="HTTPSampler.domain">localhost</stringProp>
    <stringProp name="HTTPSampler.port">8000</stringProp>
    <stringProp name="HTTPSampler.path">/user/users/${user_id}</stringProp>
  </elementProp>
  
  <elementProp name="查询商品信息" elementType="HTTP Request">
    <stringProp name="HTTPSampler.domain">localhost</stringProp>
    <stringProp name="HTTPSampler.port">8000</stringProp>
    <stringProp name="HTTPSampler.path">/product/products/${product_id}</stringProp>
  </elementProp>
  
  <!-- 其他请求配置... -->
</com.blazemeter.jmeter.controller.WeightedSwitchController>
```

#### 2.2.3 优点

- 权重配置直观，与Locust类似
- 自动计算执行比例
- 支持动态调整权重

---

### 方式3：If Controller + 计数器（不推荐）

#### 2.3.1 配置结构

```
Thread Group
├── Counter (1 to 100, 循环)
├── If Controller (${counter} <= 37) → 查询用户信息
├── If Controller (${counter} > 37 && ${counter} <= 66) → 查询商品信息
├── If Controller (${counter} > 66 && ${counter} <= 85) → 查询订单列表
├── If Controller (${counter} > 85 && ${counter} <= 96) → 创建订单
└── If Controller (${counter} > 96) → 查询库存
```

#### 2.3.2 缺点

- 配置复杂，维护困难
- 不够灵活，调整权重需要重新计算
- 性能开销较大（每次都要判断条件）

---

## 三、Locust vs JMeter对比

| 特性 | Locust | JMeter |
|------|--------|--------|
| **权重控制** | `@task(weight)` 装饰器，简单直观 | Throughput Controller或插件 |
| **脚本编写** | Python代码，灵活易维护 | XML配置或GUI操作，学习曲线陡 |
| **分布式压测** | Master-Worker架构，原生支持 | 需要配置远程服务器 |
| **监控可视化** | Web UI实时监控 | 需要Backend Listener + Grafana |
| **资源消耗** | 轻量级，单机支持更多并发 | 较重量级，GUI模式消耗大 |
| **调试能力** | Python调试工具，方便 | 需要使用Debug Sampler |
| **扩展性** | 编写Python插件，灵活 | 需要编写Java插件 |
| **适用场景** | 开发友好，适合持续集成 | 企业级压测，GUI操作友好 |

---

## 四、实战建议

### 4.1 选择Locust的场景

- ✅ 开发团队熟悉Python
- ✅ 需要快速编写和维护测试脚本
- ✅ 需要集成到CI/CD流程
- ✅ 需要灵活的分布式压测
- ✅ 需要自定义复杂的测试逻辑

### 4.2 选择JMeter的场景

- ✅ 团队已有JMeter使用经验
- ✅ 需要GUI界面操作
- ✅ 需要丰富的测试报告
- ✅ 需要测试非HTTP协议（JDBC、JMS等）
- ✅ 企业级压测项目，有成熟的JMeter基础设施

---

## 五、完整示例

### 5.1 Locust完整示例

```python
from locust import HttpUser, task, between
import random

class FullChainUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        self.user_id = random.randint(1, 100000)
        self.token = f"mock-token-{self.user_id}"
    
    @task(10)
    def query_user_info(self):
        user_id = random.randint(1, 100000)
        self.client.get(
            f"/user/users/{user_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/user/users/[id]"
        )
    
    @task(8)
    def query_product_info(self):
        product_id = random.randint(1, 10000)
        self.client.get(
            f"/product/products/{product_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/product/products/[id]"
        )
    
    @task(5)
    def query_order_list(self):
        self.client.get(
            f"/order/orders/user/{self.user_id}?limit=20",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/order/orders/user/[id]"
        )
    
    @task(3)
    def create_order(self):
        order_data = {
            "user_id": self.user_id,
            "product_id": random.randint(1, 10000),
            "quantity": random.randint(1, 5)
        }
        self.client.post(
            "/order/orders",
            json=order_data,
            headers={"Authorization": f"Bearer {self.token}"},
            name="/order/orders [POST]"
        )
    
    @task(1)
    def query_inventory(self):
        product_id = random.randint(1, 10000)
        self.client.get(
            f"/inventory/inventory/{product_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/inventory/inventory/[id]"
        )
```

### 5.2 JMeter完整示例（.jmx片段）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="全链路压测">
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments">
        <collectionProp name="Arguments.arguments"/>
      </elementProp>
    </TestPlan>
    <hashTree>
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="用户组">
        <stringProp name="ThreadGroup.num_threads">100</stringProp>
        <stringProp name="ThreadGroup.ramp_time">10</stringProp>
        <boolProp name="ThreadGroup.scheduler">false</boolProp>
      </ThreadGroup>
      <hashTree>
        <!-- 查询用户信息 - 37% -->
        <ThroughputController guiclass="ThroughputControllerGui" testclass="ThroughputController" testname="查询用户信息">
          <intProp name="ThroughputController.style">1</intProp>
          <stringProp name="ThroughputController.throughput">37.0</stringProp>
        </ThroughputController>
        <hashTree>
          <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="查询用户信息">
            <stringProp name="HTTPSampler.domain">localhost</stringProp>
            <stringProp name="HTTPSampler.port">8000</stringProp>
            <stringProp name="HTTPSampler.path">/user/users/${user_id}</stringProp>
            <stringProp name="HTTPSampler.method">GET</stringProp>
          </HTTPSamplerProxy>
        </hashTree>
        
        <!-- 其他请求配置... -->
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
```

---

## 六、总结

1. **Locust的权重机制**：通过`@task(weight)`装饰器实现，简单直观，适合开发团队
2. **JMeter实现权重**：推荐使用Throughput Controller，按百分比控制执行频率
3. **工具选择**：根据团队技术栈、项目需求、维护成本综合考虑
4. **最佳实践**：先使用Locust快速验证，再根据需要迁移到JMeter进行企业级压测

---

**创建时间**：2026-06-21  
**文档版本**：v1.0  
**适用场景**：全链路压测、性能测试、接口测试