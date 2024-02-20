# 

### 🚁 Docker for Windows

已知Docker依赖于linux内核环境，但总有大冤种（也就是我😓）想在Windows 10操作系统中部署。

[Window Docker安装教程](https://www.runoob.com/docker/windows-docker-install.html)

安装教程第一步是安装并开启Hyper-V，但我并未执行这一步（根据提供的步骤查看也未启用Hyper-V），而是直接在官网下载了安装包，但安装时提示系统版本太低。

更新完操作系统后便安装成功，未发现Hyper-V或WSL 2等导致错误，docker指令在PowerShell中执行也正常，只能不排除潜在其他的问题。


### 🚁 启用Hyper-V后运行容器提示端口不可用

为了避免一些不必要的错误，后来还是启用了Hyper-V，此时再Docker run container时报错。
>  Error: (HTTP code 500) server error - Ports are not available: listen tcp 0.0.0.0:xxxx: bind: An attempt was made to access a socket in a way forbidden by access permissions.

解决方案：

设置“TCP 动态端口范围”，以便 Hyper-V 只保留我们设置的范围内的端口。

以管理员权限运行以下命令，将“TCP 动态端口范围”重置为 49152–65535，Docker便可使用该范围内的端口。

```commandline
netsh int ipv4 set dynamic tcp start=49152 num=16384
netsh int ipv6 set dynamic tcp start=49152 num=16384
```

[参考来源及错误原因分析请看这篇博客](https://cloud.tencent.com/developer/article/2168217)

---
