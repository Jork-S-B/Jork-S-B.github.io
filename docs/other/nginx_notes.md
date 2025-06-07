* 高性能、开源的Web服务器，可用作反向代理、负载均衡器和HTTP缓存。
* 支持多种协议，包括HTTP、HTTPS、SMTP、POP3和IMAP等，并且可以通过模块化的结构来扩展其功能。
* 优点：占用资源少、稳定性高、并发能力强等。
* 用途，广泛应用于互联网领域。特别是高并发、大流量的网站和应用程序。

## 📌 Nginx常用指令

|       指令        | 说明              |
|:---------------:|:----------------|
|   start nginx   | 启动服务            |
| nginx -s reopen | 重启服务            |
| **nginx -s reload** | 重新加载配置，改配置时记得重载 |
|  nginx -s stop  | 强制停止服务          |
|  nginx -s quit  | 处理完所有请求后退出服务    |
|    nginx -V     | 打印版本信息          |

### 🚁 正向代理

客户端通过代理服务器proxy访问，而不是直接访问目标服务器。

### 🚁 反向代理

服务端不直接响应，通过代理服务器proxy转发；可以选择负载均衡策略，减小服务器压力。

## 📌 部署html网页

设置配置文件，启动服务，修改前记得备份。

=== "nginx.conf"

    ```
    # 以上的内容省略 
    # 负载均衡，分发节点的ip
    upstream dsshop{
        # ip_hash;  # 优先转发权重高的服务器
        # weight权重，权重越高，被分发的概率越大，需要承担的压力就越大
        server {host}:{端口号} weight=1;    
        server {host2}:{端口号} weight=1;    
        # server {host3}:{端口号} backup;    
    }
    
    # 虚拟主机配置
    server {
        listen       {自定端口号};
        server_name  {本机ip/域名};

        location / {
            root   {静态网页路径};
            index  index.html;

            ＃ 仅允许指定ip访问
            allow {某个ip地址};
            deny all;

            proxy_set_header Host $host;
        }
        
        # 让host处理只动态资源，如html
        location /web/ {
            proxy_pass http://host:port;
        }
        
        # 让host2处理只静态资源
        location /images/ {
            proxy_pass http://host2:port;
        }
        
        error_page 500 502 503 504 /50x.html;
        location = /50x.html. {
            root html;
        }
    }
    ```

## 📌 一些网络知识

* 动态ip与静态ip: 局域网内的ip一般使用DHCP方式，每次登录到网络会随机分配ip。若经常变动，不方便访问。
* 虚拟机的网络模式:   
NAT模式: 虚拟机只能通过主机访问。  
桥接模式: 获取局域网里的真实ip，使局域网机器都可访问虚拟机。  
* 网关: 类似路由器，连接多个局域网。
* DNS: 域名解析为对应ip地址。

!!! note "如何设置静态ip"

    1. 查网关
    2. 查DNS: 8.8.8.8
    3. 修改配置文件: /etc/sysconfig/network-scripts/ifcfg-ens33
    4. 重启网络服务: systemctl restart network

---
