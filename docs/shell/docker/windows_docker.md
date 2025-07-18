## 📌 Docker Desktop

已知Docker依赖于linux内核环境，但总有大冤种（也就是我😓）想在Windows 10操作系统中部署。

参考资料：[Window Docker安装教程](https://www.runoob.com/docker/windows-docker-install.html)

安装教程第一步是安装并开启Hyper-V，但我并未执行这一步（根据提供的步骤查看也未启用Hyper-V），而是直接在官网下载了安装包，但安装时提示系统版本太低。

更新完操作系统后便安装成功，未发现Hyper-V或WSL 2等导致错误，docker指令在PowerShell中执行也正常，只能不排除潜在其他的问题。

>  2024/5/12: 电脑上还同时使用安卓模拟器时，请不要使用Hyper-V！否则会出现冲突，docker起不来。  
>  2024/8/17: 新设备首次使用尽量下载最新版：实测Windows 11安装`docker desktop 4.1.1.0`，容器初始化报错，换成4.3.2.0（20240817当前最新版）正常运行。  

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

参考资料：[错误原因分析](https://cloud.tencent.com/developer/article/2168217)

## 📌 WSL2 + Docker Desktop

1. 安装docker desktop
2. wsl2安装ubuntu内核并启用，参考资料: https://www.jianshu.com/p/f6ad57a9f16d
3. 完成后即可通过子系统ubuntu执行docker命令（docker desktop需要保持运行）

补充: 迁移wsl2 ubuntu，参考资料: https://www.sysgeek.cn/move-wsl-distros-windows/

实测可用，但wsl2中无`docker0`默认网桥（172.17.0.1），网络隔离更强，需要使用`host.docker.internal`访问宿主机服务。

!!! note "cmd-wsl命令"

    wsl -l -v  # 查看所有wsl2系统版本及运行状态
    
    wsl --shutdown {system_name}  # 关闭wsl对应服务

    wsl -d {system_name}  # 启动

## 📌 WSL2安装原生Docker

如`CAdvisor`这种服务需要监控容器状态，上述方式部署时`/var/lib/docker`可能为空导致无数据，使用该方式贴近linux系统部署docker，规避掉非必要的疑难杂症。

假设已经安装ubuntu内核并启用，按以下命令执行安装Docker。

```shell
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装依赖
sudo apt install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common

# 下载并添加 Docker 官方 GPG 密钥（使用阿里云镜像）
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 添加 Docker APT 源（阿里云镜像）
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装 Docker 引擎
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# 验证安装
sudo docker run hello-world

# 顺便安装docker-compose
sudo apt install -y docker-compose-plugin

# 验证docker-compose版本
docker compose version

# 加入开机自启
sudo systemctl enable docker
```

## 📌 Docker镜像源

/etc/docker/daemon.json，创建文件并添加内容。

完成后重启docker服务，sudo systemctl restart docker

=== "2025/06/23"

    ```json
    {
      "registry-mirrors": [
        "https://docker.m.daocloud.io",
        "https://dockerproxy.com",
        "https://docker.mirrors.ustc.edu.cn",
        "https://docker.nju.edu.cn"
      ]
    }
    ```

=== "2024/10/21"

    ```json
    {
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
