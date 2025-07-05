# WSL + kind搭建集群

## 📌 1.安装相关应用

安装`docker`、`kubernetes`、`kind`

docker安装参考: [WSL2安装原生Docker](../../docker/windows_docker/#wsl2docker) 

=== "安装kubernetes"

    ```shell
    curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
    chmod +x ./kubectl
    sudo mv ./kubectl /usr/local/bin/kubectl
    
    kubectl version --client
    ```

=== "安装kind"

    ```shell
    curl -Lo ./kind https://github.com/kubernetes-sigs/kind/releases/download/v0.8.1/kind-$(uname)-amd64
    chmod +x ./kind
    sudo mv ./kind /usr/local/bin/kind
    ```

---

参考资料：

1. [WSL2 Ubuntu+K8s+Docker开发环境部署](https://juejin.cn/post/7073035395868393485)
2. [在 Windows 下使用 WSL2 搭建 Kubernetes 集群](https://cloud.tencent.com/developer/article/1645054)


