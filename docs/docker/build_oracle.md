#  

### 🚁 构建19C镜像

[参考的这一篇博客](https://blog.csdn.net/arcsin_/article/details/123707618)

准备好Dockerfile，构建镜像并运行容器。19C镜像需要2G以上磁盘空间，pull和首次运行都需要一段时间。

=== "Dockerfile_Oracle"

    ```
    FROM registry.cn-hangzhou.aliyuncs.com/zhuyijun/oracle:19c
    # 数据库实例
    ENV ORACLE_SID=ORCLCDB
    # 多租户架构下的一个容器数据库
    ENV ORACLE_PDB=ORCLPDB1
    ENV ORACLE_PWD=123456
    ENV ORACLE_EDITION=standard
    ENV ORACLE_CHARACTERSET=AL32UTF8
    
    # 持久化数据卷
    VOLUME /opt/oracle/oradata
    ```

=== "执行命令"
    
    ```sh
    docker build -f Dockerfile_Oracle -t my-oracle .
    # 注意当前路径
    docker run -d -p 49524:1521 -p 55502:5500 --name my-19c -v ${pwd}:/opt/oracle/oradata my-oracle
    ```

=== "terminal"
    
    ```sh
    --部署完成后用sqlplus检查服务是否正常运行
    --最高权限的 SYS 用户登录
    sqlplus / as sysdba
    ```

### 🚁 在指定pdb中创建用户

=== "terminal"
    
    ```sh
    --最高权限的 SYS 用户登录
    sqlplus / as sysdba
    ```

=== "sqlplus"
    
    ```sql
    --确保已连接到ORCLPDB1（Dockerfile配置的ORACLE_PDB）
    ALTER SESSION SET CONTAINER = ORCLPDB1;
    
    --在ORCLPDB1中创建用户WHM
    CREATE USER WHM IDENTIFIED BY WHM;
    
    --为用户分配默认表空间和临时表空间（假设users是默认表空间，temp是临时表空间）
    ALTER USER WHM DEFAULT TABLESPACE users QUOTA UNLIMITED ON users CONTAINER = CURRENT;
    ALTER USER WHM TEMPORARY TABLESPACE temp CONTAINER = CURRENT;
    
    --授权，授予用户在当前PDB中的权限
    GRANT create user, drop user, alter user TO WHM CONTAINER = CURRENT;
    GRANT create any view, connect, resource, dba TO WHM CONTAINER = CURRENT;
    GRANT create session, create any sequence TO WHM CONTAINER = CURRENT;
    
    COMMIT;
    
    --撤销授权则是
    --REVOKE SELECT, UPDATE, INSERT, DELETE ON TABLE_NAME FROM WHM;
    ```

!!! note "补充"
    
    12c及更高版本，若要建公共用户，则用户名需要以C##开头+username命名。

### 🚁 在宿主机使用oracledb连接
    
=== "dbutil.py"

    ```python
    import oracledb
    
    
    class DBUtil:
        def __init__(self):
            self.conn = oracledb.connect(r'WHM/WHM@127.0.0.1:49524/ORCLPDB1')
            self.cursor = self.conn.cursor()
    
        def select_data(self, sql: str) -> list:
            # SQL语句去掉分号，否则报错ORA-00911
            if sql.strip().endswith(';'):
                sql = sql.strip()[:-1]
            rows = self.cursor.execute(sql).fetchall()
            return rows
    
        def db_close(self):
            self.cursor.close()
            self.conn.close()
    
    
    if __name__ == '__main__':
        mydb = DBUtil()
        sql = 'select sysdate from dual'
        print(mydb.select_data(sql))
        mydb.db_close()

    ```

控制台打印：[(datetime.datetime(2024, 1, 15, 14, 7, 23),)]，没得问题。

---
