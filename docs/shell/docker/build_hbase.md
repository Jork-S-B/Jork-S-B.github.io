拉取镜像

```
docker pull harisekhon/hbase:2.1
```

运行镜像

```
docker run -d -h docker-hbase \
        -p 2181:2181 \
        -p 8080:8080 \
        -p 8085:8085 \
        -p 9090:9090 \
        -p 9000:9000 \
        -p 9095:9095 \
        -p 16000:16000 \
        -p 16010:16010 \
        -p 16201:16201 \
        -p 16301:16301 \
        -p 16020:16020\
        --name hbase \
        harisekhon/hbase
```

> 端口说明：  
> 2181: ZooKeeper 端口，用于协调分布式应用程序的服务发现和配置同步。  
> 8080: HBase 的 Web UI 端口，可以通过浏览器访问，提供集群状态和一些管理功能。  
> 8085: HBase 的 Master Web UI 端口，提供关于 HBase 主节点的信息。  
> 9090: HBase 的主要 API 端口，用于 HBase 的客户端与服务器之间的通信。  
> 9095: HBase 的主要 RPC（远程过程调用）引擎端口。  
> 16000: HBase 的主区域服务器（RegionServer）端口。  
> 16010: HBase 的主区域服务器 Web UI 端口，提供有关特定 RegionServer 的信息。  
> 16201: HBase 的备用区域服务器（RegionServer）端口。  
> 16301: HBase 的备用区域服务器 Web UI 端口，提供有关备用 RegionServer 的信息。  
> 16030: HBase 的主控制台端口，提供有关 HBase 主控制台的信息。  
> 16020: HBase 的主区域服务器信息端口。

访问HBase WebUI

http://127.0.0.1:16010/master-status

```shell
# 访问HBase Shell
docker exec -it container_id bash

# 进入容器后输入
hbase shell
```

## 📌 hbase基础

非关系型（nosql）数据库

1.表名-Table Name

2.行键-RowKey

* hbase表每行数据的唯一标识符，类似关系型数据库中的主键。
* hbase按行键字典序排序存储，查询时只能基于`RowKey`或范围进行高效查询，对性能和查询效率至关重要。
* 在插入数据时动态添加，无需提前定义。

3.列族-ColumnFamily

* hbase表的物理存储单元，定义在建表时，不能随意更改。
* 一个表可以有多个列族，每个列族下可以有多个列-Qualifier。

```shell
# 建表，表名users，列族info、address
create 'users', 'info', 'address'
```

4.列/列限定符-Qualifier

* 列是列族下的具体字段，也称为列限定符（Column Qualifier）。
* 在插入数据时动态添加，无需提前定义。
* 列和列族一起构成完整的列名，即`列族:列名`。

5.时间戳-Timestamp

* hbase默认每个单元格保存多个时间戳，不指定则使用当前时间。
* 查询时可以指定获取特定版本的数据。

6.单元格-Cell

* 单元格是数据存储的最小单元，由行键、列族、列限定符和时间戳确定。
* 每个单元格存储一个值。

### 🚁 增删改查

```shell
# 插入/更新数据，行键user123，列族info、address
put 'users', 'user123', 'info:name', 'Alice'
put 'users', 'user123', 'address:city', 'Beijing'

# 查看所有表
list
# 查看表结构（列族、列限定符、时间戳等）
describe 'users'
# 扫描指定表，并指定扫描范围
scan 'users', {STARTROW => 'user100', STOPROW => 'user150'}
# 查询数据，查询指定RowKey的数据
get 'users', 'user123'

# 删除数据，删除指定行键、列族、列限定符的数据
delete 'users', 'user123', 'info:name'
# 删除整行
delete 'users', 'user123'
```

### 🚁 查询效率优化方式

* 设计良好RowKey，如固定长度填充、时间戳倒序（避免热点）、哈希前缀（均匀分布）等
* 使用Scan时限制范围
* 列族不宜过多，读取效率更高
* 创建表时指定分区
* 使用Elasticsearch等构建二级索引提升查询效率

### 🚁 适用场景

* 大数据量、高并发写入
* 高频写入、低频查询
* 需要灵活的表结构定义（Schema），列式存储，支持动态字段

---

参考资料：[HBase实践 | 使用 Docker 快速上手 HBase](https://cloud.tencent.com/developer/article/1632053)

