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

访问HBase Shell

```
docker exec -it container_id bash
```

进入容器后输入

```
hbase shell
```

---

参考资料：[HBase实践 | 使用 Docker 快速上手 HBase](https://cloud.tencent.com/developer/article/1632053)

