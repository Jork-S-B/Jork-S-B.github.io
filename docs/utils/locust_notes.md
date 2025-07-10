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