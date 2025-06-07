## 📌 目录

日志: /usr/local/tomcat7-8083/logs/catalina.out

数据库配置: /usr/local/web/WebRoot/WEB-INF/classes/jdbc.properties

=== "catalina.sh"

```shell
# 位于tomcat的bin目录: cd /usr/local/tomcat7-8083/bin
# 设置堆内存，最大值不超过机器的70%
# HeapDumpPath: 堆存储文件，溢出的日志记录路径
JAVA_OPTS="-Xms512m -Xmx1024m -XX:PermSize=128m -XX:MaxPermSize=256m -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/tomcat/dump.hprof"

```

=== "server.xml"

```xml
<!-- 位于tomcat的conf目录: cd /usr/local/tomcat7-8083/conf -->
<!-- 端口配置 -->
<Connector executor="tomcatThreadPool" port="8083"
           protocol="org.apache.coyote.http11.Http11NioProtocol"
           connectionTimeout="20000" URIEncoding="UTF-8"
           redirectPort="8443"/>

<!-- 线程池配置，默认为200，超过maxThreads就会等待，最好不超过1000 -->
<Executor name="tomcatThreadPool" namePrefix="catalina-exec-"
          maxThreads="600" minSpareThreads="4"/>

```


!!! note "补充"

    内存泄漏: 程序设计时的失误，代码运行完成后未能正确回收/释放资源。结果导致程序性能下降，最终可能引发系统崩溃。
    
    内存溢出: 内存泄漏会引发内存溢出，程序试图分配超过实际可用的内存大小。
    
    通过长时间压测，可以发现内存泄漏问题，报错OutOfMemory 或 OOM

