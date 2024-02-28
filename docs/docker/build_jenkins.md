docker pull jenkins/jenkins


# 创建挂载目录并授权
# mkdir -p /var/jenkins_node

# chmod 777 /var/jenkins_node

cd 'F:\Program Files\Docker\share\my-jenkins'

# 启动容器，映射主机端口及挂载目录
docker run -d --name my-jenkins -p 8088:8080 -p 50000:50000 -v ${pwd}:/var/jenkins_home jenkins/jenkins

# 看初始化密码
docker logs -f --tail=200 my-jenkins

0fde53a200744d17880f3fba15b3e2a5

This may also be found at: /var/jenkins_home/secrets/initialAdminPassword

访问localhost:8088/，然后输入上面这串密码，进入jenkins向导，安装插件

进入容器，根据指引生成ssh公钥