基于JAVA语言，可跨平台使用。

### 🚁 断点调试

1. 在捕获的请求列表中找到待测请求，右键选择`Breakpoint`，然后可在`Proxy`->`Breakpoints`中设置断点的类型，默认包括`Request`、`Response`。
2. 待测请求右键选择`Repeat`重放请求，即可进入到断点位置。

!!! note "补充"

    https请求抓包：
    
    &nbsp;&nbsp;1.安装证书：`Help`->`SSL Proxying`->`Install Charles Root Certificate`。

    &nbsp;&nbsp;2.开启SSL代理：`Proxy`->`SSL proxying Settings`，在`Include`中添加需要代理的域名及端口。

    手机抓包/非本地浏览器:

    &nbsp;&nbsp;3.设备连接同区域网的WiFi，配置代理，ip及端口可以通过以下选项查看：

    &nbsp;&nbsp;`Help`->`SSL Proxying`->`Install Charles Root Certificate on a Mobile Device or Remote Browser`

### 🚁 请求转发

* 在请求列表中找到待测请求，右键选择`Map Remote`或者`Map Local`，可将请求转发至远程服务器或本地。
* 也可在`Tools`选项卡->`Map Remote`或者`Map Local`中，设置转发的请求及响应。

!!!note "补充"

	全局转发：`Tools`->`Rewrite`中设置转发的域名规则。

### 🚁 构造请求

* 在请求列表中找到待测请求，右键选择`Compose`，即可克隆该请求。
* 也可在`Tools`选项卡->`Compose`或者`Compose New`中，克隆或者新建请求。

### 🚁 请求代理

1. `Proxy`->`Proxy Settings`->`Proxies`，设置端口号并勾选`Enable transparent HTTP proxying`。
2. 手机连接同区域网的WiFi后，手动配置代理，把机器IP及端口填入对应项即可。

### 🚁 模拟弱网

1. `Proxy`->`Thorttle Settings`中设置规则，工具提供了3G、4G等网络的预设。
2. 设置完成后，单击工具类的小乌龟图标，即可快捷开关模拟弱网功能。

---