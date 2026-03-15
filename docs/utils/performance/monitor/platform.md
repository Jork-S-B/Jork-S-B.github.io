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
          - targets: [ '192.168.80.170:9100','192.168.80.168:9100' ]  # node_exporter监控多服务器或多个工作节点
    
    - job_name: 'mysql'
        static_configs:
          - targets: [ '192.168.80.170:9104','192.168.80.168:9104' ]  # mysql_exporter监控多服务器或多个工作节点
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

    [Grafana模版下载](https://grafana.com/grafana/dashboards/)

## 📌 Docker搭建监控平台

CAdvisor，用于分析运行中容器的资源占用和性能指标，负责收集、聚合、处理和输出运行中容器的信息。

=== "配置文件prometheus.yml"

      ```yaml
      global:
        scrape_interval: 60s
        evaluation_interval: 60s
      scrape_configs:
        - job_name: prometheus
          static_configs:
            - targets: [ '172.17.0.1:9090' ]
              labels:
                instance: prometheus
        - job_name: linux
          static_configs:
            - targets: [ '172.17.0.1:9100' ]
        - job_name: mysql
          static_configs:
            - targets: [ '172.17.0.1:9104' ]
        - job_name: 'cadvisor'
          static_configs:
            - targets: [ '172.17.0.1:8081' ]
      ```

=== "docker run"
      
      ```shell
      # 创建并启动node-exporter容器
      docker run -id --name node-exporter -p 9100:9100 \
         -v "/proc:/host/proc:ro" \
         -v "/sys:/host/sys:ro" \
         -v "/:/rootfs:ro" \
         registry.cn-hangzhou.aliyuncs.com/{namespace}/node-exporter
         
      # 创建并启动mysqld-exporter容器
      # 172.17.0.1，docker宿主机与容器的默认网桥
      docker run -id --name mysql-exporter --privileged=true -p 9104:9104 \
         -e DATA_SOURCE_NAME="root:whm@(172.17.0.1:3306)/" \
         registry.cn-hangzhou.aliyuncs.com/{namespace}/mysqld-exporter
         
      # 创建并启动prometheus容器
      docker run -id --name prometheus -p 9090:9090 \
         -v ./prometheus.yml:/etc/prometheus/prometheus.yml \
         -v /etc/localtime:/etc/localtime:ro \
         registry.cn-hangzhou.aliyuncs.com/{namespace}/prometheus
         
      # 创建并启动grafana容器
      docker run -id --name=grafana -p 3000:3000 \
         -v /opt/grafana/data:/var/lib/grafana \
         -v /etc/localtime:/etc/localtime:ro \
         registry.cn-hangzhou.aliyuncs.com/{namespace}/grafana
      
      # 创建并启动CAdvisor容器
      # 如果使用Docker Desktop + WSL2，/var/lib/docker可能为空导致无数据
      docker run -id \
         --volume=/:/rootfs:ro \
         --volume=/var/run:/var/run:ro \
         --volume=/sys:/sys:ro \
         --volume=/var/lib/docker/:/var/lib/docker:ro \
         --volume=/dev/disk/:/dev/disk:ro \
         --publish=8081:8080 \
         --detach=true \
         --name=cadvisor \
         registry.cn-hangzhou.aliyuncs.com/{namespace}/cadvisor
      ```

=== "docker-compose-monitor.yaml"
      
      ```yaml
      version: '3.3'
      
      services:
        node-exporter:
          image: registry.cn-hangzhou.aliyuncs.com/{namespace}/node-exporter
          container_name: node-exporter
          ports:
            - "9100:9100"
          volumes:
            - "/proc:/host/proc:ro"
            - "/sys:/host/sys:ro"
            - "/:/rootfs:ro"
          restart: always
      
        mysql-exporter:
          image: registry.cn-hangzhou.aliyuncs.com/{namespace}/mysqld-exporter
          container_name: mysql-exporter
          privileged: true
          ports:
            - "9104:9104"
          environment:
            DATA_SOURCE_NAME: "root:sq@(172.17.0.1:3306)/"
          restart: always
      
        prometheus:
          image: registry.cn-hangzhou.aliyuncs.com/{namespace}/prometheus
          container_name: prometheus
          ports:
            - "9090:9090"
          volumes:
            - "./prometheus.yml:/etc/prometheus/prometheus.yml"
            - "/etc/localtime:/etc/localtime:ro"
          restart: always
      
        grafana:
          image: registry.cn-hangzhou.aliyuncs.com/{namespace}/grafana
          container_name: grafana
          ports:
            - "3000:3000"
          volumes:
            - "/opt/grafana/data:/var/lib/grafana"
            - "/etc/localtime:/etc/localtime:ro"
          restart: always
      
        cadvisor:
          image: registry.cn-hangzhou.aliyuncs.com/{namespace}/cadvisor
          container_name: cadvisor
          ports:
            - "8081:8080"
          volumes:
            - "/:/rootfs:ro"
            - "/var/run:/var/run:ro"
            - "/sys:/sys:ro"
            - "/var/lib/docker/:/var/lib/docker:ro"
            - "/dev/disk/:/dev/disk:ro"
          restart: always
      
      ```

## 📌 指标分析

[监控服务器](./server.md)

[监控Mysql](./mysql.md)

---