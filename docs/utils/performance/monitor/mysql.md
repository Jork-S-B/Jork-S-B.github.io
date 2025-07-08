## 📌 指标分析

Current QPS-每秒处理查询数

Connections-连接数

### 🚁 Slow Queries

Y轴是慢查询数量，需要设置慢查询阈值（如1秒），默认10秒。

#### 🔧 设置慢查询

改配置文件后重启服务: `systemctl restart mysqld`

=== "/etc/my.cnf"

    ```shell
    log_output = table  # 将慢查询日志保存到表中
    slow_query_log = 1  # 开启慢查询
    long_query_time = 1  # 慢查询超时时间为1秒
    max_connections = 512  # 最大连接数，要求适中
    ```

临时修改环境变量，则在mysql里执行: `set global max_connections=1000;`

#### 🔧 慢查询SQL分析

1.找到慢查询SQL原语句

```SQL
SELECT START_TIME, USER_HOST, QUERY_TIME, LOCK_TIME, DB, SQL_TEXT
FROM MYSQL.SLOW_LOG
ORDER BY START_TIME DESC LIMIT 10;
```

2.EXPLAIN SQL，或者navicat查看执行计划，查询结果如下：

| id | select_type | table  | type | possible_keys | key  | key_len | ref  | rows  | Extra       |
|----|-------------|--------|------|---------------|------|---------|------|-------|-------------|
| 1  | SIMPLE      | orders | ALL  | NULL          | NULL | NULL    | NULL | 10000 | Using where |

关键字段说明：

- type = ALL 表示进行全表扫描。
- rows = 10000 表示扫描大约10000行数据。
- Extra = Using where 表示使用WHERE过滤数据。
- possible_keys = NULL 表示没有合适的索引可用。

!!! note "type值优先级"

    CONST > EQ_REF > REF > RANGE > INDEX > ALL

    | type类型  | 说明                                            |
    |----------|-----------------------------------------------|
    | `const`  | 主键或唯一索引查找，速度最快                                |
    | `eq_ref` | 多表连接时使用主键/唯一索引                                |
    | `ref`    | 普通索引查找，效率较高                                   |
    | `range`  | 范围查询，如`WHERE id BETWEEN 1 AND 10`，需**注意**合理使用 |
    | `index`  | 全索引扫描，即遍历整个索引，**仍需优化**                        |
    | `ALL`    | 全表扫描，**应添加索引优化**                              |

3.得出结论：未使用索引进行全表查询，导致性能下降。

4.如何优化：

- 添加索引
- 避免SELECT *
- 拆分复杂查询
- 定期执行`ANALYZE TABLE`，更新统计信息帮助优化器选择更优执行计划
- 持续监控并优化慢SQL

5.优化后回测，再次查看执行计划。

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

!!! note "死锁"

    日志报错出现死锁时，让ai给SQL查出现死锁的表，并在压测时执行sql。

    或者在mysql配置文件中启用死锁日志记录: innodb_print_all_deadlocks = ON

### 🚁 相关变量

```sql
# 查看数据库中与慢查询相关的变量
show variables like '%slow_query%';

# 查询数据库中的最大连接数
show variables like '%max_connections%';

# 查询数据库中的连接数历史峰值
show variables like '%max_used_connections%';

# 长查询的执行时间阈值，超过该时间的查询被记录为慢查询
show variables like '%long_query%';
```
