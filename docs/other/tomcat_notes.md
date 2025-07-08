## 📌 目录

日志: /usr/local/tomcat/logs/catalina.out

数据库配置: /usr/local/web/WebRoot/WEB-INF/classes/jdbc.properties

`catalina.sh`完整配置: [catalina.sh](../catalina.sh)

Tomcat的启停脚本:

* tomcat/bin/startup.sh

* tomcat/bin/shutdown.sh

=== "catalina.sh"

    ```shell
    # 位于tomcat的bin目录: cd /usr/local/tomcat/bin
    # -Xms512m -Xmx1024m: 设置堆内存，最大值不超过机器内存的70%
    # -XX:PermSize=128m -XX:MaxPermSize=256m: Java 8及以后版本中该参数无效。
    # HeapDumpPath: 堆存储文件，溢出的日志记录路径
    # -XX:NewRatio=1: 设置年轻代/老年代的比例，默认为1
    export JRE_HOME=/usr/local/jdk
    JAVA_OPTS='-Xms512m -Xmx1024m -XX:PermSize=128m -XX:MaxPermSize=256m -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/tomcat/dump.hprof -XX:NewRatio=1
        -Djava.rmi.server.hostname=ip
        -Dcom.sun.management.jmxremote.port=10001
        -Dcom.sun.management.jmxremote.ssl=false
        -Dcom.sun.management.jmxremote.authenticate=false'
    ```

=== "server.xml"

    ```xml
    <!-- 位于tomcat的conf目录: cd /usr/local/tomcat/conf -->
    <!-- 端口配置 -->
    <Connector executor="tomcatThreadPool" port="8083"
               protocol="org.apache.coyote.http11.Http11NioProtocol"
               connectionTimeout="20000" URIEncoding="UTF-8"
               redirectPort="8443"/>
    
    <!-- 线程池配置，默认为200，超过maxThreads就会等待，最好不超过1000 -->
    <Executor name="tomcatThreadPool" namePrefix="catalina-exec-"
              maxThreads="600" minSpareThreads="4"/>
    
    ```

## 📌 内存溢出分析

1.将`dump.hprof`下载导入到`Eslipse Memory Analyzer`。 

2.主要看Overview -> Reports -> Leak Suspects -> details的堆栈信息

参考资料: [内存泄露该怎么办-堆内存文件hprof分析](https://www.bilibili.com/video/BV11142167vj/?spm_id_from=333.337.search-card.all.click&vd_source=3609d4adbadc244cd438bd16fa816a8e)

todo，据说idea的功能Profiler，也能分析hprof文件。

[使用idea自带的内存泄漏分析工具](https://blog.csdn.net/weixin_43982359/article/details/132316552)