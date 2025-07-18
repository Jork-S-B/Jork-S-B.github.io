## 1.服务器配置

* 设置服务器为固定/静态ip
* 设置主机名（/etc/hostname）为master、node节点
* 设置解析hosts值
* 关闭防火墙: `systemctl disable firewalld`
* 关闭swap空间: `swapoff -a && sed -i '/swap/ s$^\(.*\)$#\1$g' /etc/fstab`
* 关闭selinux: `setenforce 0 && sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config`
* 修改docker配置: `/etc/docker/daemon.json`
* 配置k8s的镜像加速: `/etc/yum.repos.d/kubernetes.repo`
* 安装k8s组件: `yum install kubelet-1.22.2 kubeadm-1.22.2 kubectl-1.22.2 -y`
* 设置kubelet开机启动: `systemctl enable kubelet && systemctl start kubelet`
* 修改网络配置
* Centos7安装NFS，服务器间共享数据: `yum install nfs-common nfs-utils -y`
* 安装Docker

=== "设置静态ip"

    ```shell
    vi /etc/sysconfig/network-scripts/ifcfg-ens33
    # i-insert模式
    BOOTPROTO="static"
    ONBOOT="yes"
    IPADDR="192.168.1.100"
    NETMASK="255.255.255.0"
    GATEWAY="192.168.1.1"
    DNS1="192.168.1.1"
    # :wq-保存并退出
    systemctl restart network
    ```

=== "设置解析hosts值"

    ```shell
    vi /etc/hosts
    # i-insert模式
    192.168.1.100 master
    192.168.1.101 node1
    192.168.1.102 node2
    # :wq-保存并退出
    ```

=== "修改docker配置"

    ```json
    {
      "registry-mirrors": [
        "https://v2c6fjn8.mirror.aliyuncs.com"
      ],
      // 避免docker与k8s的文件驱动不一致
      "exec-opts": [
        "native.cgroupdriver=systemd"
      ],
      // 日志文件格式
      "log-driver": "json-file",
      "log-opts": {
        "max-size": "100m"
      },
      // 存储驱动程序
      "storage-driver": "overlay2"
    }
    ```

=== "配置k8s的镜像加速"

    ```text
    [kubernetes]
    name=Kubernetes
    baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
    enabled=1
    gpgcheck=1
    exclude=kube*
    repo_gpgcheck=0
    gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
    ```

=== "修改网络配置"

    ```shell
    vi /etc/sysctl.d/k8s.conf
    # i-insert模式
    net.bridge.bridge-nf-call-ip6tables = 1
    net.bridge.bridge-nf-call-iptables = 1
    net.ipv4.ip_forward = 1
    vm.swappiness = 0
    # :wq-保存并退出
    # 使配置生效
    sysctl -p /etc/sysctl.d/k8s.conf
    sysctl --system
    # 重启kubelet服务
    systemctl restart kubelet
    ```

## 2.主节点部署

### 2.1.生成初始化文件: `kubeadm-config.yaml`，并修改

=== "生成初始化文件"

    ```shell
    mkdir -p /root/whm
    cd /root/whm
    kubeadm config print init-defaults > kubeadm-config.yaml
    ```

=== "kubeadm-config.yaml"

    ```yaml
    localAPIEndpoint:
      advertisedAddress: 192.168.1.100  # master节点的ip地址
      bindPort: 6443
    # 中间省略一些配置不用改
    imageRepository: registry.aliyuncs.com/google_containers
    ```

### 2.2.拉取镜像

```shell
kubeadm config images list --config kubeadm-config.yaml
kubeadm config images pull --config kubeadm-config.yaml
```

### 2.3.初始化主节点（CPU核心数量需大于1）

kubeadm init --config=kubeadm-config.yaml

=== "根据打印信息运行命令"

    ```shell
    # 建目录，配置环境
    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config
    
    # 工作节点加入集群
    kubeadm join 192.168.1.100:6443 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:xxx
    ```

此时`kubectl get node`只有主节点，状态为`NotReady`

### 2.4.配置网络状态

`kubernetes`⽀持多种类型⽹络插件，要求网络⽀持CNI（Container Network Interface）插件即可。

常⻅的有`calico`、`flannel`、`canal`、`weave`等。

安装calico: `kubectl apply -f calico.yaml`

查看节点进度: `kubectl get node -A`

## 3.工作节点部署

工作节点加入集群，从`2.3.初始化主节点`打印信息加入集群，或重新生成Token或证书密码。

```shell
# 在master节点执行
# 查看token
kubeadm token list

# 查看sha256密码
openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'

# 查看节点状态
kubectl get node
```

## 4.部署微服务
