# 

### 🚁 pytest + jaydebeapi

pytest运行，用例调用jaydebeapi库时，日志出现`Windows fatal exception`等一大串报错。

虽然不影响运行，但影响看日志体验。

[具体原因分析](https://www.cnblogs.com/melonHJY/p/14500744.html)

解决方法：在`pytest.ini`中配置`addopts = -p no:faulthandler`。

---
最后更新: 2024/02/07 22:30