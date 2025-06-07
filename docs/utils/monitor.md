流程: node_exporter(收集数据) -> Prometheus(保存数据) -> Grafana(展示数据)

## 📌 exporter

node_exporter，用于收集服务器性能指标，默认端口9100。

mysql_exporter，用于收集连接数、慢查询、数据库表锁等，默认端口9104。

常用的exporter下载:  
https://www.cnblogs.com/momoyan/p/11520755.html

## 📌 Prometheus

开源的监控报警系统与时序系统，默认端口9090。

对时间精度要求高，若服务器时间与现实时间不同步，可能导致无法收集准确数据。

```shell
date  # 查当前时间
sudo ntpdate ntp.aliyun.com  # 校准ntp服务时间

# 若依然显示N/A，则执行以下命令清缓存
cd /usr/local/prometheus/
rm -rf data/
mkdir data
```

### 🚁 启动Prometheus

1. cd /usr/local/prometheus
2. vim prometheus.yml，配置文件中设置需要`exporter`对应的ip地址
3. ./prometheus --config.file=prometheus.yml
4. 进入prometheus的web页面，查看监控目标  
   http://192.168.80.170:9090/targets

=== "prometheus.yml"

    ```yaml
    - job_name: 'prometheus'
        static_configs:
          - targets: [ 'localhost:9090' ]  # 端口号9090
    
    - job_name: 'agent'
        static_configs:
          - targets: [ '192.168.80.170:9100','192.168.80.168:9100' ]  # node_exporter监控多服务器
    
    - job_name: 'mysql'
        static_configs:
          - targets: [ '192.168.80.170:9104','192.168.80.168:9104' ]  # mysql_exporter监控多服务器
    ```

## 📌 Grafana

开源、可视化的监控工具，用于展示收集到的数据，默认端口3000。

访问grafana服务:  
http://192.168.80.170:3000/

默认账号密码: admin/admin

1.配置数据源

Configuration -> Add data source -> url填Prometheus所在的服务器（如`http://192.168.80.170:9090`）

2.导入模版

若显示N/A，则需要进行校准时间。

3.显示时间选择: 近30分钟，刷新频率： 5秒/次。

!!! note "补充"

    修改服务器配置重启时，Grafana展示可能会有延迟。

### 🚁 监控服务器

#### 🔧 系统平均负载

系统平均负载: CPU在一段时间内的使用量

一般来说，系统平均负载超过`CPU核数`数倍时，视为异常。

### 🚁 监控mysql

常关注的指标:

Current QPS-每秒处理查询数

Connections-连接数

Slow Queries-慢查询数，设置慢查询阈值如1秒

Table Locks-表级锁，控制并发访问的机制，防止同时对一个表进行读写。

#### 🔧 Table Locks

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

      