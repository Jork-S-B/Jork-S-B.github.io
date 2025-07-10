## 📌 容器方式部署jenkins

```shell
docker pull jenkins/jenkins

# 创建挂载目录并授权
mkdir -p /var/jenkins_node
chmod 777 /var/jenkins_node
# 修改目录的所有者，以便于Jenkins容器能够操作该目录
chown -R 1000:1000 /var/jenkins_node

# 启动容器，映射主机端口及挂载目录
docker run -d --name my-jenkins -p 8088:8080 -p 50000:50000 -v /var/jenkins_node:/var/jenkins_home jenkins/jenkins
```

## 📌 初始化

1.初始化密码

docker logs -f --tail=200 my-jenkins

如：0fde53a200744d17880f3fba15b3e2a5

This may also be found at: /var/jenkins_home/secrets/initialAdminPassword

2.安装插件

访问localhost:8088/，然后输入上面这串密码，进入jenkins向导，安装推荐插件

大部分核心插件安装成功后重启容器。

* 发送邮件通知，安装插件：[email-ext.hpi](email-ext.hpi)，需要先卸载jenkins自带的邮件插件
* 展示性能测试报告（html），安装插件：`HTML Publisher`

jenkins里默认不展示css样式，需要在`系统管理->Script Console`运行命令:  
System.setProperty("hudson.model.DirectoryBrowserSupport.CSP", "")

3.在设置中修改时区为: `Asia/Shanghai`

## 📌 节点模式

创建节点，以远程执行机器上的脚本。

节点创建后，根据提示命令下载并启动`agent.jar`。

启动成功后，创建任务：指定节点、构建操作（需要执行的脚本）、构建后操作、定时/手动执行。