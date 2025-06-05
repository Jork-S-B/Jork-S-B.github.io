## 📌 bin目录

=== "catalina.sh"

```shell
# 设置堆内存，不超过机器的70%
# HeapDumpPath: 堆存储文件，溢出的日志记录路径
JAVA_OPTS="-Xms512m -Xmx1024m -XX:PermSize=128m -XX:MaxPermSize=256m -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/tomcat/dump.hprof"
```

!!! note "补充"

    内存泄漏: 程序设计时的失误，代码运行完成后未能正确回收/释放资源。结果导致程序性能下降，最终可能引发系统崩溃。
    
    内存溢出: 内存泄漏会引发内存溢出，程序试图分配超过实际可用的内存大小。
    
    通过长时间压测，可以发现内存泄漏问题，报错OutOfMemory 或 OOM

