## 📌 构建MySQL镜像

### 🚁 准备工作

=== "Dockerfile"

    ```
    FROM mysql
    ENV MYSQL_ROOT_PASSWORD=123456
    ENV LANG=C.UTF-8
    COPY my.cnf /etc/mysql/my.cnf
    COPY init.sql /docker-entrypoint-initdb.d/
    
    # 持久化数据卷
    VOLUME /var/lib/mysql
    ```

=== "init.sql"

    ```sql
    CREATE DATABASE mydb;
    USE mydb;
    
    CREATE TABLE users (
      id INT(11) NOT NULL AUTO_INCREMENT,
      name VARCHAR(50) NOT NULL,
      email VARCHAR(50) NOT NULL,
      PRIMARY KEY (id)
    );
    INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');
    INSERT INTO users (name, email) VALUES ('Jane Doe', 'jane@example.com');
    ```

=== "my.cnf"

    ```
    [mysqld]
    character-set-server=utf8mb4
    collation-server=utf8mb4_unicode_ci
    max_connections=100    
    ```

### 🚁 构建镜像

准备好以上文件后，在Windows PowerShell中执行build指令，构建MySQL镜像。

```shell
docker build -t my-mysql .

# -f：指定Dockerfile文件路径
```

> 202406：拉取镜像失败，许多国内镜像源也已失效。有效的镜像源可参考：https://www.cnblogs.com/ikuai/p/18233775

### 🚁 运行容器并检查状态

首次运行容器会进行初始化，记得关注日志。

```shell
docker run -d -p 53306:3306 --name my-mysql -v ${pwd}:/var/lib/mysql my-mysql

# -d：守护态运行容器，实现容器的持久化运行，即使终端关闭或主机重启，容器仍然会自动启动并继续提供服务。
# -v：直接输入windows的路径会报错，${pwd}代表当前目录（要求空目录），即把当前目录挂载到容器的`/var/lib/mysql`目录；或者使用数据卷容器进行挂载。
```

### 🚁 其他指令补充

| 命令                                         | 说明                 |
|:-------------------------------------------|:-------------------|
| `docker ps`                                | 查看容器运行状态，找到对应的容器ID |
| `docker exec -it {container_id} sh`        | 进入容器               |
| `docker start {container_id}`              | 启动容器               |
| `docker stop {container_id}`               | 停用容器               |
| `docker restart {container_id}`            | 重启容器               |
| `docker logs -f --tail=200 {container_id}` | 日志尾部200行并持续刷新      |
| `docker create --name {自定名称} {image_name}` | 创建数据卷容器            |

### 🚁 连接数据库

mysql -p mydb  
当容器正常运行，在容器内输入命令连数据库

## 📌 导出镜像

```shell
# 导出镜像为 tar 文件
docker save -o my-mysql.tar my-mysql

# 在其他机器上导入镜像
docker load -i my-mysql.tar

# 运行新镜像
docker run -d --name {自定名称} -p 3306:3306 my-mysql
```

## 📌 推送镜像

先建好阿里云容器镜像服务-个人实例，并配置命名空间。

```shell
# 登录阿里云容器镜像仓库
docker login -u {username} -p {password} registry.cn-hangzhou.aliyuncs.com

# 标记镜像
docker tag my-mysql registry.cn-hangzhou.aliyuncs.com/{namespace}/my-mysql

# 推送镜像
docker push registry.cn-hangzhou.aliyuncs.com/{namespace}/my-mysql
```

---

[参考的这一篇博客](https://blog.csdn.net/Liu__sir__/article/details/130643737)