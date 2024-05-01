# 性能测试

* 性能测试，评估系统整体性能的测试，主要指标有响应时间、吞吐量、资源利用率等。
* 压力测试，在强负载（大数据量、大量并发用户等）下的测试。
* 负载测试，在一定负载情况下的系统性能测试（不关注稳定性，也就是说不关注长时间运行，只是得到不同负载下相关性能指标即可）。

---

## 📌 JMeter的使用

1. 用户定义的变量，内容包括线程数8、ramp_up_time启动所有线程所需时间、循环次数、持续时间300s、启动延迟时间。
2. 登录请求线程组，搭配正则表达式提取器、BeanShell PostProcessor将token设置为全局变量。
3. Http请求默认值，包括协议、ip、端口、编码。
4. Http信息头管理器，包括报文类型、token等信息。
5. 被测请求线程组，包括事务控制器、csv数据文件（参数化）、请求、提取器、响应断言、断言结果、汇总报告。
6. 总体的结果树、报告、事务响应时间图
7. 生成html报告，平均响应时间200ms-1200ms

参考资料：[JMeter压力测试完整流程](https://blog.csdn.net/m0_47747596/article/details/131658904)

### 🚁 后置处理器

* 边界提取器，输入左边界/右边界，提取边界里的数据。
* 其他的还有json提取器、正则提取器、xpath提取器等。

### 🚁 并发

同步定时器，等待线程数到预设数量后触发事务，达到集合点的作用。

参考资料：[JMeter并发设置](https://zhuanlan.zhihu.com/p/594119162?utm_id=0)

### 🚁 断言

* 响应断言，可以配置匹配响应文本、请求头、响应头等，或者设置包括、相等等规则
* 数据包字节大小断言
* 持续时间断言，判断是否在指定时间内返回响应结果
* beanshell断言

## 📌 需要关注的指标

吞吐量、响应时间和用户数量：刚开始吞吐量随着用户数量的增加逐渐变大，当达到一定程度时，逐渐平缓直到变成一条平线；而响应时间随着用户数量的增长逐渐变大。

!!! note "补充"
    
    吞吐量-Throughput，指单位时间内系统能够完成的工作量。
    TPS-Transactions Per Second，指系统每秒钟能够处理的事务和交易的数量。

### 🚁 20240501

#### 负载测试

1. shell脚本写死循环让CPU使用率（nmon C监控）跑到80%以上。
2. 调用关键业务的接口持续5分钟，线程数8。
3. 要求平均响应时间在2s内。

#### 压力测试

关注的指标：并发数、响应时间、TPS-每秒处理事务数。

🎬 场景：并发数太高，吞吐量小，影响得到的响应时间准确性。

需要从小并发往上递增加压，TPS随之往上增长；当TPS不涨时，此时的并发数就是最佳并发数。

---

而当在最佳并发数下出现响应时间过长的情况时：

🤔 分析原因：

* 网络延迟：检查网络状况，确保网络带宽和稳定性满足测试需求。（局域网一般影响不大）

* 服务器性能：检查服务器CPU、内存等资源使用情况，判断是否由于资源不足导致性能下降。

* 接口设计：检查接口是否涉及复杂计算或大量数据处理，这些操作可能导致响应时间延长。

* 代码优化：分析代码实现，看是否存在可以优化的地方，如减少数据库查询次数、使用缓存等。

🔎 处理方法：

* 优化网络：如果网络延迟是主要原因，可以尝试升级网络设备、优化网络配置或选择更稳定的网络环境进行测试。

* 升级服务器：如果服务器性能不足，可以考虑升级服务器硬件或增加服务器数量来提高处理能力。

* 优化接口设计：对于涉及复杂计算或大量数据处理的接口，可以尝试优化算法、减少数据处理量或采用异步处理方式来提高响应速度。

* 优化代码：对代码进行性能分析，找出性能瓶颈并进行优化。可以考虑使用更高效的算法、减少数据库查询次数、使用缓存等技术来提高响应速度。

* 引入缓存机制：对于经常访问的数据或计算结果，可以将其缓存在内存或缓存数据库中，以减少对数据库的访问次数，提高响应速度。

* 使用分布式缓存：将经常访问的数据缓存到内存中，以减少数据库的访问次数，提高接口的响应速度。


---