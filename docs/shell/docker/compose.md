## 📌 准备工作

### 🚁 查端口是否被占用

=== "windows"

    ```commandline
    netstat -an | findstr /i ":22"
    ```

=== "linux"

    ```shell
    # -n是禁止域名转换，即不进行DNS解析
    lsof -n
    # 或者
    # 查看系统中所有处于监听状态的TCP端口，较新的linux中逐渐被lsof取代
    netstat -tpln
    ```

### 🚁 准备镜像

=== "dockerfile"

    ```dockerfile
    FROM java:8
    WORKDIR "/usr/local/myapp"
    ADD myapp.jar .
    EXPOSE 7080
    CMD  java - jar  myapp.jar
    ```

=== "打包并推到仓库"

    ```shell
    docker build -f dockerfile -t whmmyapp .
    
    docker login -u {username} -p {password} registry.cn-hangzhou.aliyuncs.com
    
    docker push registry.cn-hangzhou.aliyuncs.com/{namespace}/whmmyapp
    ```

### 🚁 容器管理

使用portainer，可视化管理容器。

当然，docker desktop自带该功能。

```shell
docker run -id -p 9000:9000 \
--restart=always \
-v /var/run/docker.sock:/var/run/docker.sock \
--name prtainer \
registry.cn-hangzhou.aliyuncs.com/{namespace}/portainer:v1
```

## 📌 docker-compose

仅使用docker命令拉取镜像，运行容器。

```shell
# 创建并运行mysql容器
docker run -id --name mysql -p 3306:3306 \
   -v /opt/mysql/data:/var/lib/mysql \
   -e MYSQL_ROOT_PASSWORD=whm \
   registry.cn-hangzhou.aliyuncs.com/{namespace}/db:v6 
   
# 创建并运行rabbitmq容器
docker run -id --name rabbitmq  \
   -p 5672:5672  \
   -p 15672:15672 \
   -p 15692:15692 \
   -v /opt/rabbitmq/data:/var/lib/rabbitmq  \
   -e RABBITMQ_DEFAULT_USER=guest -e RABBITMQ_DEFAULT_PASS=guest \
   registry.cn-hangzhou.aliyuncs.com/{namespace}/rabbitmq
   
# 创建并运行redis容器
docker run -id --name redis \
   -p 6379:6379 \
   -v /opt/redis/data:/data  \
   -v /etc/localtime:/etc/localtime:ro \
   registry.cn-hangzhou.aliyuncs.com/{namespace}/redis
   
# 创建并运行myapp的容器
docker run -id --name myapp \
   -p 7080:7080  \
   --link mysql \
   --link rabbitmq \
   --link redis:myRedis \
   -v /etc/localtime:/etc/localtime:ro \
   registry.cn-hangzhou.aliyuncs.com/{namespace}/myapp:3.0
```

当镜像间有依赖关系时（--link），则需要手动按顺序拉起容器，或者直接使用docker-compose

=== "docker-compose-myapp.yaml"
    
    ```yaml
    version: '3.3'  
    services:
       mysql:
         image: registry.cn-hangzhou.aliyuncs.com/{namespace}/db:v6
         container_name: mysql
         volumes:
           - /opt/mysql/data:/var/lib/mysql
         restart: always
         ports:
           - "3306:3306"
         environment:
           MYSQL_ROOT_PASSWORD: whm
           
       rabbitmq:
         image: registry.cn-hangzhou.aliyuncs.com/{namespace}/rabbitmq
         container_name: rabbitmq
         volumes:
           - /opt/rabbitmq/data:/var/lib/rabbitmq
         restart: always
         ports:
           - "5672:5672"
           - "15672:15672"
           - "15692:15692"
         environment:
           RABBITMQ_DEFAULT_USER: guest
           RABBITMQ_DEFAULT_PASS: guest
           
       redis:
         image: registry.cn-hangzhou.aliyuncs.com/{namespace}/redis
         container_name: redis
         volumes:
           - /opt/redis/data:/data
         restart: always
         ports:
           - "6379:6379"
           
       myapp:
         depends_on:
           - mysql
           - rabbitmq
           - redis
         image: registry.cn-hangzhou.aliyuncs.com/{namespace}/myapp
         container_name: myapp
         links:
           - mysql:mysql
           - rabbitmq:rabbitmq
           - redis:myRedis
         ports:
           - "7080:7080"
         environment:
           - JAVA_OPTS=-Xmx450m -Xms450m -Xss256k
         restart: always
    ```

=== "创建并启动"

    ```shell
    # 首次运行
    docker-compose -f docker-compose-myapp.yaml up -d

    # 仅启动
    docker-compose -f docker-compose-myapp.yaml start
    ```