* 高性能、开源的Web服务器，也可以用作反向代理服务器、负载均衡器和HTTP缓存。
* 支持多种协议，包括HTTP、HTTPS、SMTP、POP3和IMAP等，并且可以通过模块化的结构来扩展其功能。
* 优点：占用资源少、稳定性高、并发能力强等。
* 用途，广泛应用于互联网领域。特别是高并发、大流量的网站和应用程序。

## Nginx常用指令

|       指令        | 说明           |
|:---------------:|:-------------|
|   start nginx   | 启动服务         |
| nginx -s reopen | 重启服务         |
| nginx -s reload | 重新加载配置并重启服务  |
|  nginx -s stop  | 强制停止服务       |
|  nginx -s quit  | 处理完所有请求后退出服务 |
|    nginx -V     | 打印版本信息       |

## 部署html网页

设置配置文件，启动服务，修改前记得备份。

=== "nginx.conf"

    ```
    # 以上的内容省略 
    # 虚拟主机配置
    server {
        listen       {自定端口号};
        server_name  {本机ip};

        location / {
            root   {静态网页路径};
            index  index.html;

            ＃ 仅允许指定ip访问
            allow {某个ip地址};
            deny all;
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html. {
            root html;
        }
        # todo,location、upstream（负载均衡）
    }
    ```
---
