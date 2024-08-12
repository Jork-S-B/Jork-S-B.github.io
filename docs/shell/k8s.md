# K8S-Kubernetes

## 📌 查看命名空间
kubetcl get namespace

## 📌 查看当前命名空间下的pod节点
kubectl -n {namespace} get pods -o wide

## 📌 查看节点信息(挂载目录、CPU和内存限制等)、重启原因等
kubectl -n {namespace} describe pods {podId}

## 📌 查看pod的deployment信息
kubectl -n {namespace} get deployments.apps -o yaml

## 📌 进入容器
kubectl -n {namespace} exec -it {podId} sh
kubectl -n {namespace} exec -it {podId} -- bash  # 俩横杠后接的实际是指令

## 📌 查看容器控制台日志
kubectl -n {namespace} logs -f --tail=200 {podId}

## 📌 删除/重启pod

重启pod  
kubectl -n {namespace} delete pods {podId1} {podId2}

创建新容器，待正常运行后再退出原容器  
kubectl -n {namespace} rollout restart deployment {app}

重新部署pod  
kubectl -n {namespace} get pod {podname}  -o yaml | kubectl replace --force -f -

## 📌 调整pod副本数/扩容
kubectl -n {namespace} scale deployment {podId} --replicas=2

## 📌 把容器内的文件cp到本地
kubectl cp {namespace}/{podId}:/tmp ./tmp

