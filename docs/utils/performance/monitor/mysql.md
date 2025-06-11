## 📌 指标分析

Current QPS-每秒处理查询数

Connections-连接数

### 🚁 Slow Queries

慢查询数，设置慢查询阈值如1秒。

#### 🔧 设置慢查询

=== "/etc/my.cnf"

改配置文件后重启服务: `systemctl restart mysqld`

```shell
log_output=table  # 将慢查询日志保存到表中
slow_query_log=1  # 开启慢查询
long_query_time=1  # 慢查询超时时间为1秒
max_connections=512  # 最大连接数
```

### 🚁 Table Locks

表级锁，控制并发访问的机制，防止同时对一个表进行读写。

包含以下指标: 

* Table_locks_immediate  
表示一个线程请求表锁时，立即获得锁的次数。即：无需等待，直接加锁成功。

* Table_locks_waited  
表示一个线程请求表锁时，需要等待其他线程释放锁的次数。即：发生锁竞争，出现阻塞。

理想状态下，Table_locks_immediate 应远大于 Table_locks_waited。

若后者持续增长，说明存在较多锁竞争，可能影响并发性能。

!!! note "优化建议"

    * 优先使用`InnoDB`存储引擎: 支持行级锁，大幅减少锁冲突。
    * 优化慢查询、添加合适索引。
    * 尽量避免长事务，及时提交事务以释放锁资源。
    * 设置报警规则，当`Table_locks_waited`突增时及时通知。

### 🚁 相关变量

```sql
# 查看数据库中与慢查询相关的变量
show variables like '%slow_query%';

# 查询数据库中的最大连接数
show variables like '%max_connections%';

# 长查询的执行时间阈值，超过该时间的查询被记录为慢查询
show variables like '%long_query%';
```

