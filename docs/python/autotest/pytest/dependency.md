`pytest-dependency`: 用于声明测试用例之间的依赖关系，当某个依赖的测试失败时，依赖它的测试会被自动跳过，避免不必要的错误报告。

## 使用示例

=== "test_demo.py"

    ```python
    import pytest

    @pytest.mark.dependency()  # 被依赖的测试，可省略 name（默认函数名）
    def test_connect():
        assert True

    @pytest.mark.dependency(depends=["test_connect"])
    def test_insert():
        assert True

    @pytest.mark.dependency(depends=["test_connect", "test_insert"])
    def test_query():
        assert False  # 故意失败，会导致依赖它的测试被跳过

    @pytest.mark.dependency(depends=["test_query"], reason="test_query failed")
    def test_delete():
        assert True  # 前置用例断言失败，本测试会被跳过
    ```

作用域默认为`session`，也可指定为: scope=="module" 或 "class"

或者在全局配置`pytest.ini`或`pyproject.toml`中设置默认作用域: `dependency-scope=module`