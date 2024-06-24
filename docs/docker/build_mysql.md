
### 🚁 构建MySQL镜像

[参考的这一篇博客](https://blog.csdn.net/Liu__sir__/article/details/130643737)

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

准备好以上文件后，在Windows PowerShell中执行build指令，构建MySQL镜像。

`docker build -t my-mysql .`

!!! note "补充"
    
    -f：可以指定Dockerfile文件路径

>  202406：拉取镜像失败，许多国内镜像源也已失效。有效的镜像源可参考：https://www.cnblogs.com/ikuai/p/18233775

### 🚁 运行容器并检查状态

\# 运行容器，并指定端口、数据目录挂载等；首次执行需要初始化，记得关注日志。

`docker run -d -p 53306:3306 --name my-mysql -v ${pwd}:/var/lib/mysql my-mysql`

!!! note "补充"

    -d：守护态运行容器，实现容器的持久化运行，即使终端关闭或主机重启，容器仍然会自动启动并继续提供服务。

    -v：${pwd}代表当前目录（要求空目录），即把当前目录挂载到容器的`/var/lib/mysql`目录。

    -v直接输入windows的路径会报错，如：

    * F:\Program Files\Docker\share\my-mysql  # 报错: invalid reference format.
    * F//Program Files/Docker/share/my-mysql  # 报错: invalid reference format: repository name must be lowercase.

\# 查看容器运行状态，找到对应的容器ID

`docker ps -a`

\# 进入容器

`docker exec -it [container_id] sh`

\# 此时若容器正常运行，输入指令`mysql -p mydb`及密码即可连上数据库。

### 🚁 其他指令补充

| 命令                                        | 说明            |
|:------------------------------------------|:--------------|
| `docker start [container_id]`             | 启动容器          |
| `docker stop [container_id]`              | 停用容器          |
| `docker restart [container_id]`           | 重启容器          |
| `docker logs -f --tail=200 [container_id]` | 日志尾部200行并持续刷新 |

# todo，增量镜像

---
