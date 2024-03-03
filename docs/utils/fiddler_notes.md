# Fiddler笔记

### 🚁 断点调试

Fiddler可以在请求发送至服务端前打断点，或者在服务端发响应结果时打断点(请求前，响应后)。

通过请求断点，在`Inspectors`选项卡可修改cookie、修改session、修改报文内容等。

https请求抓包，需要在`Tools`->`Options...`->`HTTPS`选项卡，勾选`Capture HTTPS CONNENCTS`等选项，并安装证书。

![img.png](image/https.png)

### 🚁 请求转发

在`AutoResponder`选项卡，增加转发规则，设置匹配请求的方式及转发的内容。

![img.png](image/AutoResponder.png)

匹配请求的方式：

*  `EXACT`-精确匹配，如`EXACT:http://ip:port/xxx`

*  `regex`-以正则表达式匹配，如`regex:http://[^:]*:\d{4}/(.*)`

转发的内容可设置为其他http请求、url或者本地文件等。

!!!note "补充"

	若需设置延迅时间，右键点击规则-＞`Set Latency`设置时间（单位为毫秒），并勾选`enable latency`。

### 🚁 构造请求

针对一些长流程进行接口测试时，可通过`Composer`，构造请求报文进行调试，待调通后再进行集成测试，提高效率。

通过此方式也可构造SQL注入、XSS注入payload，检查程序能否妥善处理。

1. 从捕获的请求列表，拖拽待测请求至右侧`Composer`选项卡，便可写入报文。
2. 修改请求报文，单击`Execute`按钮即可发送请求。

![img.png](image/Composer.png)

### 🚁 请求代理

1.`Tools`->`Options...`->`Connections`选项卡，设置端口号，勾选`Allow remote computers to connect`选项。

2.设置代理认证：

3.手机连接同网段的WiFi后，设置代理，把机器IP及端口填入对应项。若设置了代理认证则还需填写用户名、密码。

### 🚁 模拟弱网



参考资料：[Fiddler详解](https://www.cnblogs.com/cty136/p/11479142.html)

---
