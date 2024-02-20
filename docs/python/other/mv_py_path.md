# Python路径迁移

在windows系统安装python3.11时，默认安装在`C:\Users\用户名\AppData\Local\Programs\Python\Python311\`。

如果需要将python3.11迁移到其他盘符，如D盘，则需要如下步骤：

1. 将python3.11路径移动到D盘，并修改环境变量PATH。

2. 此时pip -V 不可用，但卸载后重装即可。
```
python -m pip uninstall -y pip
# 通过以下链接安全下载get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```
[参考链接](https://blog.csdn.net/qq_41929184/article/details/104825688)

3. 迁移前已安装的库，也需要重新安装一遍。
```
pip freeze > requirements.txt  # 导出已安装的库
pip uninstall -y -r requirements.txt
pip install -r requirements.txt
```

---
最后更新: 2024/01/01 16:34
