专门为微服务、云原生和基于容器的架构设计的分布式系统性能监控工具，具备链路追踪、监控/统计程序运行时的指标（包括网关、操作系统等）。

Topology-拓扑图，显示服务调用关系。

## 📌 oap

`skywalking-oap-server`，对外暴露11800、12800端口，分别用于接收数据、webui交互的端口。

## 📌 oap-ui

默认8080端口，可视化skywalking采集的数据。

## 📌 agent

基于java探针技术完成数据上报，无需修改源代码。

官网下载解压后，`config/agent.config`需要修改: 

```text
collector.backend_service=${SW_AGENT_COLLECTOR_BACKEND_SERVICE:{部署oap容器的ip}:11800}
```

### 🚁 启动

jvm参数中加入agent相关的内容，包括:

```text
-javaagent:/path/skywalking-agent.jar -Dskywalking.agent.service_name={对应服务名} -Dskywalking.logging.file_name={对应服务名}_error.log
```

---