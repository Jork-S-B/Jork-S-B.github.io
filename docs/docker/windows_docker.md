# 

## 📌 Docker for Windows

已知Docker依赖于linux内核环境，但总有大冤种（也就是我😓）想在Windows 10操作系统中部署。

参考资料：[Window Docker安装教程](https://www.runoob.com/docker/windows-docker-install.html)

安装教程第一步是安装并开启Hyper-V，但我并未执行这一步（根据提供的步骤查看也未启用Hyper-V），而是直接在官网下载了安装包，但安装时提示系统版本太低。

更新完操作系统后便安装成功，未发现Hyper-V或WSL 2等导致错误，docker指令在PowerShell中执行也正常，只能不排除潜在其他的问题。

>  2024/5/12: 电脑上还同时使用安卓模拟器时，请不要使用Hyper-V！否则会出现冲突，docker起不来。  
>  2024/8/17: 新设备首次使用尽量下载最新版：实测Windows 11安装docker 4.1.1.0，容器初始化报错，换成4.3.2.0（20240817当前最新版）正常运行。

## 📌 启用Hyper-V后运行容器提示端口不可用

为了避免一些不必要的错误，后来还是启用了Hyper-V，此时再Docker run container时报错。
>  Error: (HTTP code 500) server error - Ports are not available: listen tcp 0.0.0.0:xxxx: bind: An attempt was made to access a socket in a way forbidden by access permissions.

解决方案：

设置“TCP 动态端口范围”，以便 Hyper-V 只保留我们设置的范围内的端口。

以管理员权限运行以下命令，将“TCP 动态端口范围”重置为 49152–65535，Docker便可使用该范围内的端口。

```commandline
netsh int ipv4 set dynamic tcp start=49152 num=16384
netsh int ipv6 set dynamic tcp start=49152 num=16384
```

参考资料：[错误原因分析](https://cloud.tencent.com/developer/article/2168217)

## 📌 镜像源

2024/10/21 - 镜像源配置

```
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "registry-mirrors": [
    "https://docker.registry.cyou",
    "https://docker-cf.registry.cyou",
    "https://dockercf.jsdelivr.fyi",
    "https://docker.jsdelivr.fyi",
    "https://dockertest.jsdelivr.fyi",
    "https://mirror.aliyuncs.com",
    "https://dockerproxy.com",
    "https://mirror.baidubce.com",
    "https://docker.m.daocloud.io",
    "https://docker.nju.edu.cn",
    "https://docker.mirrors.sjtug.sjtu.edu.cn",
    "https://docker.mirrors.ustc.edu.cn",
    "https://mirror.iscas.ac.cn",
    "https://docker.rainbond.cc"
  ]
}
```

## 📌 Windows系统启用OpenSSH

由于Window Docker启的容器无法被其他机器直接远程连接，故需启用OpenSSH。

1.安装OpenSSH服务器：系统 > 可选功能 > 添加可选功能 > 搜索“OpenSSH服务器”

2.配置与启动

管理员身份运行PowerShell，执行命令：

SSH服务自动启动

```commandline
Set-Service -Name sshd -StartupType 'Automatic'
```

启动服务

```commandline
Start-Service sshd
```

检查SSH服务器是否侦听22端口

```commandline
netstat -an | findstr /i ":22"
```

确保Windows Defender防火墙允许 TCP 22 端口的入站连接

```commandline
Get-NetFirewallRule -Name *OpenSSH-Server* | select Name, DisplayName, Description, Enabled
```

参考资料：[Windows 上的 OpenSSH：安装、配置和使用指南](https://www.sysgeek.cn/openssh-windows/)

---
