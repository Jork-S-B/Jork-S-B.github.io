## 📌 JVM

JDK-开发工具包 > JRE-运行环境/运行时类库 > JVM-Java虚拟机

Java的跨平台特性得以实现靠的是JVM，相当于Java在每个平台都放了一个虚拟机，而Java程序则运行在虚拟机中。

### 🚁 生命周期: 

1.JVM实例起点: 任何一个拥有`public static void main(String[] args)`方法的类，都可以作为JVM的起点。

2.JVM实例运行: 内部有两种线程: 守护线程和非守护线程，前者通常由JVM自己使用，后者通常包括main()。

3.JVM实例结束: 当程序中所有非守护线程都结束时。

## 📌 GC

GC线程也是守护线程的一种，用于回收不再使用的对象，并释放占用的内存空间。

### 🚁 年轻代

Eden Space + Survivor 0 + Survivor 1

存放新创建对象的内存区域，采用复制算法进行垃圾回收，回收频率高，且回收过程通常较快。

### 🚁 老年代

Old Gen

存放长时间存活对象的内存区域，可能是经过多次垃圾回收仍然存活的，或者是一直存在于程序运行期间的。

老年代的垃圾回收相对低频，采用更复杂的算法进行垃圾回收，回收时间较长，且在新生代垃圾回收完成后进行，以减少对应用程序的影响。

### 🚁 元空间

Perm Gen

存储类的元数据（类的结构、方法、字段等信息），由Java虚拟机自动管理元空间的内存。

### 🚁 需要关注的指标

**GC频次**: collections / GC Time = 每几秒进行1次GC

GC频次的大小，需要根据业务体量、数据级、服务器资源等来进行综合评估。

频繁回收会导致应用程序表现不佳，可能内存不够导致，或代码中可能存在内存空间释放不合理的地方。

## 📌 VisualVM

JDK1.8及以前版本，bin目录自带VisualVM，否则需要自行安装。

下载地址: http://visualvm.github.io/download.html

=== "visualvm/etc/visualvm.conf"

    ```txt
    visualvm_jdkhome='jdk路径'
    ```

### 🚁 JMX监控线程死锁

`JMX`，Java平台提供的一个管理和监控Java应用程序的标准。不支持查看GC，但是可以对堆内存、cpu、类、线程的监控。

1.[catalina-jmx-remote.jar](JVM/Fcatalina-jmx-remote.jar)，Apache Tomcat服务器中用于支持远程JMX访问的扩展包。

将该jar包放到`tomcat/lib`目录里即可。

2.配置JMX后重启tomcat。

=== "catalina.sh"

    ```shell
    # 位于tomcat的bin目录: cd /usr/local/tomcat/bin
    -Djava.rmi.server.hostname=ip  # 指定用于JMX连接的服务器
    -Dcom.sun.management.jmxremote.port=10001
    -Dcom.sun.management.jmxremote.ssl=false  # 不启用JMX SSL安全连接
    -Dcom.sun.management.jmxremote.authenticate=false  # 不进行用户验证
    ```

3.`VisualVM`添加并输入远程主机名，并在远程机上添加JMX连接。

若连接失败，可以关掉防火墙，或将端口添加至白名单。

```shell
systemctl stop firewalld
firewall-cmd --list-ports  # 列出开放端口
firewall-cmd --add-port=10001/tcp --permanent  # 白名单永久添加10001端口
```

### 🚁 jstatd监控GC

`jstatd`，独立的远程监控工具，用于监控和收集Java应用程序的运行时统计信息。

1.`VisualVM`安装插件: [Visual GC](JVM/Fcom-sun-tools-visualvm-modules-visualgc.nbm)，下载后进行离线安装。

2.[java.policy](JVM/java.policy)，放到`jdk/jre/lib/security`，用于配置访问权限。

3.启动`jstatd`服务，端口为1003。

```shell
./jstatd -J-Djava.security.policy=jstatd.all.policy -p 10003
```

4.`VisualVM`在远程机上添加jstatd连接。