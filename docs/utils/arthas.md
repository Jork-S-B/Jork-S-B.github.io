Java 应用诊断利器，一款线上监控诊断产品，能在不修改应用源代码的情况下，对业务问题进行诊断。

## 📌 常用命令

### 🚁 jad-反编译

`jad 类的完整路径`，进行反编译，检查类的源代码是否正确。

### 🚁 thread-线程信息

* `thread -b`  # 查死锁
* `thread -3`  # 查CPU占用前3的线程
* `thread 23`  # thread 线程id，打印对应的堆栈，以找到实际代码

### 🚁 trace-监控方法耗时

`trace 类名 方法名`

举例: `trace --skipJDKMethod false cn.demo.advfilter.handler.JudgeLabelsHandler doJudge '#cost > 200' -n 5`

参数说明:

* --skipJDKMethod false，不跳过jdk函数，默认会跳过
* '#cost > 200'，耗时大于200ms的函数
* -n 5，指定捕捉结果的次数

!!! note "补充"

    表达式主要由ognl表达式组成，可以通过在idea装相应插件生成，包括trace、watch、tt等命令。

### 🚁 watch-实时监测方法

实时监测方法入参、返回值、是否抛异常，相当于在生产环境调试方法。

### 🚁 tt-tannel time

`tt -t 类名 方法名 -n 5`，看一段时间内，方法调用情况。

`tt -p -i 索引`，重放指定请求。

### 🚁 dashboard-仪表盘

看线程cpu使用率、机器内存变化、GC频率。

=== "GC部分"

    ```shell
    GC:
    [PS Scavenge]  # Young GC
     count: 5  # count值快速上升可能是频繁GC
     time: 120ms  # 累计耗时
    [PS MarkSweep]  # Full GC
     count: 1
     time: 80ms
    ```

判断GC是否频繁

| 类型       | 判断标准              | 优化建议             |
|:---------|:------------------|:-----------------|
| Young GC | count快速增长，每秒>1次   | 增加 -Xmn，优化对象分配逻辑 |
| Full GC  | 	count快速增长，每分钟>1次 | 增加 -Xmx，排查内存泄漏   |
| 单次GC耗时长  | time较大，单次>100ms）  | 调整GC回收器          |

### 🚁 jvm-查看jvm信息

---

参考资料：

1.[Arthas使用手册](https://arthas.aliyun.com/doc/quick-start.html)

2.[trace命令查看方法性能开销耗时、追踪方法调用路径](https://blog.csdn.net/qq_37279783/article/details/128277011)

3.[trace 参数](https://www.cnblogs.com/expiator/p/17470441.html)

4.[使用Arthas工具分析CPU飙高](https://zhuanlan.zhihu.com/p/498399364)

5.[Arthas&GC日志&GCeasy详解](https://blog.csdn.net/qq_43135259/article/details/138507367)