通过mitmproxy库能实现类似Fiddler抓包工具的功能，也适用于APP，但处理HTTPS请求前需要安装及配置证书。

参考资料：[mitmproxy的使用以及遇到的问题](https://blog.csdn.net/feiyu68/article/details/119665869)

代码示例可参考：[使用mitmproxy+jinja2，捕获请求并生成对应的接口测试用例](https://gitee.com/Jork-S-B/basic-auto-test/blob/master/Commons/my_proxy/api_proxy.py)