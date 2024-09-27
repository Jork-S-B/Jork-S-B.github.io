=== "dockerfile"
    
    ```
    # 使用 Rocky Linux 9.3 作为基础镜像
    FROM rockylinux:9.3
    
    # 维护者信息
    LABEL maintainer="whm@example.com"
    
    ENV LANG=zh_CN.GB2312
    ENV NLS_LANG="AMERICAN_AMERICA.ZHS16GBK"
    
    # 更新包索引并安装 vim
    RUN dnf update -y && \
        dnf install -y vim
    
    # 安装 OpenSSH 服务器
    RUN dnf install -y openssh-server
    
    # 设置 SSH 服务开机启动
    RUN systemctl enable sshd
    
    # 生成 SSH 主机密钥
    RUN mkdir -p /etc/ssh && \
        ssh-keygen -A
        
    # 清理缓存以减小镜像大小
    RUN dnf clean all
    
    # 修改root密码
    RUN echo "root:root" | chpasswd
    
    # 创建新用户
    RUN useradd -m -s /bin/bash whm
    
    # 设置新用户密码
    RUN echo "whm:whm" | chpasswd
    
    # 将用户添加到 wheel 组
    RUN usermod -aG wheel whm
    
    # 允许 wheel 组用户使用 sudo
    RUN echo "%wheel ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/wheel
    
    # 设置容器启动后的默认命令
    # CMD ["/bin/bash"]
    # 多个CMD命令只执行最后一个
    # 启动 SSH 服务
    CMD ["/usr/sbin/sshd", "-D"]	
    ```
    
=== "运行"

    ```shell
    docker build -t my-rockylinux .
    
    # docker run --rm  # 在容器停止后自动删除容器
    # -it：使容器以交互模式运行，并分配一个伪tty终端，允许在容器内部进行操作
    docker run -it -p 5022:22 --name rockylinux.9.3 my-rockylinux
    ```

=== "检查与调试"

    ```shell
    ssh whm@localhost -p 5022

    # 查看系统版本信息
    cat /etc/system-release
    # 或者更详细的系统信息
    cat /etc/os-release
    ```

20240910存在的问题：容器起来后，发现系统版本为`Rocky Linux release 9.4 (Blue Onyx)`，高了一个小版本。