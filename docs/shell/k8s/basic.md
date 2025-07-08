# K8S-Kubernetes

## 📌 云原生

云原生是指一种构建和运行应用程序的方法论，它充分利用了云计算模型的优势，包括但不限于：

* 容器化：使用容器（如Docker）来打包应用及其依赖项，使得应用可以在任何地方运行。
* 微服务架构：将大型应用程序分解为小型、独立的服务，这些服务可以独立部署、扩展和维护。
* DevOps文化：强调开发和运维团队之间的紧密协作，以实现快速迭代和持续交付。
* 持续集成/持续部署(CI/CD)：自动化测试和部署流程，确保代码更改可以快速可靠地发布。
* 弹性伸缩：根据需求自动调整资源，确保应用始终具有足够的性能和可用性。

## 📌 云计算服务

* Iaas（基础设施即服务）：云计算服务模型中最基础的一层，它提供了计算、存储、网络等基础设施资源作为服务。适合需要高度定制化环境的企业，或者非HTTP业务（如游戏客户端、数据分析）。

* PaaS（平台即服务）：一种云计算服务模型，它为开发者提供了一套完整的开发和部署环境，包括操作系统、数据库服务器、Web服务器和其他中间件，以及中件层服务如MySQL、Apache等。客户控制上层的应用程序部署与应用托管的环境。--面向程序员

* SaaS（软件即服务）：一种通过互联网提供软件应用的服务模型，服务商提供基于软件的解决方案，满足客户最终需求；案例如OA、Office 365、iCloud等应用，客户无需考虑专业技术知识。--面向产品经理甚至是用户

## 📌 虚拟机/Docker/K8S

* 虚拟机：对宿主机操作系统的调用不可避免地需要经过拦截和处理，存在性能消耗，尤其对计算资源、网络和磁盘IO损耗非常大。

* Docker：创建容器进程时，指定该进程所需启用的一组Namespace参数，后续容器运行时仅限定在命名空间指定的资源、文件、配置等。因此容器可以说是一种特殊的进程，避免了虚拟化的性能损耗。“敏捷”和“高性能”是容器相较于虚拟机最大的优势，但也有不足之处，最主要的是隔离不彻底。

* Kubernetes：可移植可拓展的开源平台，用于管理容器化的工作负载和服务。本质是应用服务和服务器的中间层，通过暴露一系列api能力，简化服务的部署流程，促进声明式配置和自动化，使容器化应用简单高效。

## 📌 概念

* Pod-舱，k8s的最小调度单元，至少包含一个容器；可看作是一组紧密关联的***容器***集合，共享同一个***网络命名空间***和***存储卷***。

* Node-工作节点，执行由Kubernetes API Server分配的任务（通过kubelet接收），比如运行一个或多个Pod。

可以是裸机服务器、虚拟机、容器等，负责实际运行各个应用服务，并共享节点的内存和cpu等计算资源。

* Control Plane-控制平面(master)，k8s的核心组件，负责xian管理集群，包括Pod、Service、Deployment等。通过调用k8s提供的api接口，即可操作服务资源，资源分配由scheduler调度器完成。

控制平面和节点的组合称为Cluster-集群，集群相互独立，为了将集群内部的服务暴露给外部用户使用，所以还需要`ingress`控制器。

* Namespace-命名空间，提供逻辑隔离，将集群资源划分为多个虚拟分组（如开发环境、测试环境）。

* Deployment-部署，管理`Pod`的生命周期（创建、更新、扩缩容），确保指定数量的`Pod`副本运行。必须部署在某个`Namespace`下。

* Service-服务，为`Pod`提供稳定的网络访问端点（IP/DNS），实现负载均衡。通过标签选择器绑定`Deployment`管理的`Pod`。

`Deployment`创建的`Pod`由`Service`暴露给外部或其他服务。

!!! note "kind"

    * Deployment: 扩缩容、滚动更新、回滚代码等
    * Service: 定义pod访问方式，实现负载均衡
    * DaemonSet: 每个工作节点都自动部署，适用于`exporter`
    * ReplicationController: 维护指定数量的pod，适用于`mysql`
    * StatefulSet: 有状态的副本集，有序创建、有序删除。适用于`nacos`

!!! note "补充"

    根据`Kubernetes`的默认配置，`NodePort`类型的服务对外暴露的端口范围是30000-32767。

### 🚁 调用服务

外部请求先到达K8S集群的ingress控制器，然后请求会被转发到K8S某个node的kube proxy，再找到对应的pod，然后将请求转发给对应的服务；处理结果原路返回。

## 📌 Kubernetes的主要特性

* 自动恢复：自动重启失败容器、替换异常节点。
* 弹性伸缩：根据负载自动扩缩容。
* 服务发现与负载均衡：自动分配`IP`和`DNS`名称。
* 滚动更新与回滚：支持逐步更新和版本回退。

## 📌 kubectl-一些K8S命令

### 🚁 部署服务

```shell
kubectl create -f xxx.yaml  # 部署服务
kubectl apply -f xxx.yaml  # 部署或更新服务，即滚动更新
kubectl delete -f xxx.yaml  # 删除服务
```

### 🚁 使节点进入维护状态

??? abstract "点击查看"

    kubetcl cordon {node}

### 🚁 查看命名空间

??? abstract "点击查看"

    kubetcl get namespace

### 🚁 查看当前命名空间下的pod

??? abstract "点击查看"

    kubectl -n {namespace} get pods -o wide

### 🚁 查看pod信息(挂载目录、CPU和内存限制等)、重启原因等

??? abstract "点击查看"

    kubectl -n {namespace} describe pod {podId}

### 🚁 查看pod的deployment信息

??? abstract "点击查看"

    kubectl -n {namespace} get deployments.apps -o yaml

### 🚁 进入容器

??? abstract "点击查看"

    kubectl -n {namespace} exec -it {podId} sh

    kubectl -n {namespace} exec -it {podId} -- bash  # 俩横杠后接的实际是指令

### 🚁 查看容器控制台日志

??? abstract "点击查看"

    kubectl -n {namespace} logs -f --tail=200 {podId}

### 🚁 删除/重启pod

??? abstract "点击查看"

    重启pod  
    kubectl -n {namespace} delete pods {podId1} {podId2}

    创建新容器，待正常运行后再退出原容器  
    kubectl -n {namespace} rollout restart deployment {app}
    
    重新部署pod  
    kubectl -n {namespace} get pod {podname} -o yaml | kubectl replace --force -f -

### 🚁 调整pod副本数/扩容

??? abstract "点击查看"

    kubectl -n {namespace} scale deployment {podId} --replicas=2

### 🚁 把容器内的文件cp到本地

??? abstract "点击查看"

    kubectl cp {namespace}/{podId}:/tmp ./tmp

### 🚁 查看Pod的资源使用情况

??? abstract "点击查看"

    kubectl -n {namespace} top pod {podname}

    进入容器后执行top，查看的是pod内部的cpu、内存使用情况，相比更详细，能看到进程级别的使用量。

=== "k8s_getCpu.sh"

    ```shell
    # $()和 ` `  # 在bash shell中，$() 与` ` (反引号) 都是用来做命令替换用
    
    # 打印pod的cpu占用率、内存使用率，$2/20"%"，即CPU使用量除以上限值2000，再乘100拼接百分比符号
    # kubectl top pod -n {namespace} | grep -E '{service1}|{service2}' | awk '{print $1,$2,$2/20"%" , $3,$3/25"%"}'
    
    # 单行循环打印pod的cpu使用量，for语句后加分号而非冒号
    # for app in ${kubectl get deployments.apps -n {namespace}| grep -E '{service1}|{service2}' | awk '{print $1}'); do echo ${app}; kubectl -n {namespace} describle deployments.apps ${app}| grep -B 1 "cpu:"; echo "------------------------------------"; done
    
    n=1
    while(($n<1000))  # []/[[]] (())都是做判断，但后者可以直接使用大于小于而无需转义（还有数学运算）
    do
        TIME=`date+%Y%m%d%H%M%S`  # 时间戳
        echo "$TIME";
        n=$((n+1));
        kubectl top pod -n {namespace} | grep -E '{service1}|{service2}|CPU' | awk '{if(NR>1){printf "%-50s %-8s %-8s\n", $1, $2/20"%", $3/25"%"} else{printf "%-50s %-8s %-8s\n", $1, $2, $3}}'
        sleep 90;  # K8S不能实时获取到容器CPU使用量，大约1分钟更新一次
    done
    ```

参考资料：

1. [shell中的if语句](https://blog.csdn.net/wxx_0124/article/details/95305625)
2. [shell中$[] $(())，[ ] (( )) [[ ]]作用与区别](https://zhuanlan.zhihu.com/p/82112596)

---