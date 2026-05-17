## 📌 pytest + jaydebeapi

pytest运行，用例调用jaydebeapi库时，日志出现`Windows fatal exception`等一大串报错。

虽然不影响运行，但影响看日志体验。

[具体原因分析](https://www.cnblogs.com/melonHJY/p/14500744.html)

解决方法：在`pytest.ini`中配置`addopts = -p no:faulthandler`，`addopts`也可配置其他默认运行参数。

## 📌 设置告警过滤

```ini
[pytest]
filterwarnings =
    error
    ignore::UserWarning  # 除UserWarning，其他的告警升级为error
```

## 📌 指定日志格式

```ini
[pytest]
; 指定日志格式为：日期 日志级别 日志内容
; -8s代表长度为8个字符，不足时以空格补全 
log_format = %(asctime)s %(levelname)-8s %(message)s
log_date_format = %Y-%m-%d %H:%M:%S
```

## 📌 自定义标签

定义标签`@pytest.mark.slow`，用于标记运行时间较长的测试用例。

搭配`python -m not slow`使用，只需在pytest.ini注册标签即可。

若要使其在运行测试用例时，除非明确指定，否则默认跳过这些慢速用例，则还需使用钩子方法。

=== "conftest.py"

    ```python
    def pytest_collection_modifyitems(items):
        config = items[0].session.config  # 获取pytest配置对象
    
        if not config.getoption("--runslow"):  # 检查命令行选项中是否包含了 --runslow
            skip_slow = pytest.mark.skip(reason="need --runslow option to run")
            for item in items:
                if "slow" in item.keywords:
                    item.add_marker(skip_slow)  # 添加 skip 标签以跳过该测试用例
    
    ```
=== "testcase.py"

    ```python
    @pytest.mark.slow
    def test_long_running():
        pass

    ```

=== "pytest.ini"

    ```ini
    [pytest]
    markers =
        slow: 运行时间较长的测试用例
    ```

现在运行pytest时，默认情况下所有带有`@pytest.mark.slow`标签的用例都会被跳过。

若要运行这些慢速用例，则通过参数`--runslow`来指定，即`pytest --runslow`。

### 🚁 注册自定义标记

pytest 建议在配置文件（pytest.ini、pyproject.toml 或 tox.ini）中注册自定义标记，否则会触发 PytestUnknownMarkWarning。

#### 在 pyproject.toml 中注册

```toml
[tool.pytest.ini_options]
markers = [
    "p0: 最高优先级测试(冒烟)",
    "p1: 高优先级测试(核心功能)",
    "p2: 中优先级测试(次要功能)",
]
```

#### 运行筛选命令

```bash
# 只运行 p1 标记的测试
pytest -m p1

# 运行 p0 或 p1
pytest -m "p0 or p1"

# 运行除了 p2 以外的所有测试
pytest -m "not p2"
```

---
