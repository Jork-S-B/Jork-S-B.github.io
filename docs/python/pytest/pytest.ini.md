### 🚁 pytest + jaydebeapi

pytest运行，用例调用jaydebeapi库时，日志出现`Windows fatal exception`等一大串报错。

虽然不影响运行，但影响看日志体验。

[具体原因分析](https://www.cnblogs.com/melonHJY/p/14500744.html)

解决方法：在`pytest.ini`中配置`addopts = -p no:faulthandler`。

### 🚁 设置告警过滤

```ini
[pytest]
filterwarnings =
    error
    ignore:UserWarning  # 除UserWarning，其他的告警升级为error
```

### 🚁 指定日志格式

```ini
[pytest]
# 指定日志格式为：日期 日志级别 日志内容
# -8s代表长度为8个字符，不足时以空格补全 
log_format = %(asctime)s %(levelname)-8s %(message)s
log_date_format = %Y-%m-%d %H:%M:%S
```

---
