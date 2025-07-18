k8s提供多种机制确保应用的可靠性和可用性。探针是其中之一。

探针类型: 

* 存活探针(liveness probe): 判断容器是否可用，否则自动删除pod,并启动重启策略。
* 就绪探针(readiness probe): 判断容器是否可以处理请求，如果没有就绪的话，就不会安排请求给他，不会删除pod。
* 启动探针(startup probe): 判断容器是否启动成功，特别适合启动时间很长的应用。

探针实现方式: 

* http协议: 前端项目nginx
* socket协议: mysql
* exec: 容器内执行命令

探针配置: 

* initialDelaySeconds: 50  # 初始延迟50秒
* periodSeconds: 10  # 探测周期，每隔10秒探测一次
* failureThreshold: 10  # 失败次数，连续10次失败才判定不存活（就绪、启动）
* successThreshold: 10  # 成功次数，连续10次成功才判定存活（就绪、启动）