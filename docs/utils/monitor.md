流程: node_exporter(收集数据) -> prometheus(保存数据) -> grafana(展示数据)



## 📌 监控运行结果

### 🚁 Grafana: 可视化的图形展示平台，提供了较多模板，自动收集服务器资源。

1.安装: `sudo yum install -y https://dl.grafana.com/oss/release/grafana-10.0.3-1.x86_64.rpm`

2.启动服务: `systemctl start grafana-server`  
关闭防火墙: `systemctl stop firewalld.service`

3.访问: ip:{默认端口3000}  
默认用户名密码: admin/admin

### 🚁 Influxdb: 时序数据库

1.安装: `sudo yum install -y`，具体路径待补充

2.后台运行服务: `influxd &`

3.进入数据库: `influx`  

```sql
CREATE DATABASE jmeter;
show databases;
use jmeter;
show measurements;  # 类似show tables
```

### 🚁 使用后端监听器将执行数据写入Influxdb