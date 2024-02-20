自定义标签`@pytest.mark.slow`，用于标记运行时间较长的测试用例。

运行测试时，除非明确指定，否则默认跳过这些慢速用例。

=== "conftest.py"

    ```python
    def pytest_collection_modifyitems(items):
        config = items[0].session.config  # 获取pytest配置对象
    
        if not config.getoption("--runslow"):  # 检查命令行选项中是否包含了 --runslow
            skip_slow = pytest.mark.skip(reason="need --runslow option to run")
            for item in items:
                if "slow" in item.keywords:
                    item.add_marker(skip_slow)  # 添加 skip 标签以跳过该测试用例

    import pytest
    
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

若要运行这些慢速用例，则通过参数`--runslow`来指定：

`pytest --runslow`

---
最后更新: 2024/02/07 21:56