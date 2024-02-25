pytest参数化的方式：

* 使用测试夹具函数，`return request.param`返回参数化的数据。
* 使用`pytest.mark.parametrize`装饰器。

=== "测试用例"

    ```python
    import os
    import pytest
    
    from learn.ZhEnMerge import zh_en_merge
    from utils.SomeConstant import TESTDATA_PATH
    from utils.YamlUtil import YamlUtil
    
    testdata = YamlUtil(os.path.join(TESTDATA_PATH, 'ZhEnMergeTestData.yaml')).get_yaml_data().get('zh_en_merge_testdata')
    
    
    @pytest.fixture(params=testdata)
    def param_testdata(request):
        return request.param
    
    
    class TestZhEnMerge:
    
        def test_zh_en_merge(self, param_testdata):
            input_zh = param_testdata.get('input_zh')
            input_en = param_testdata.get('input_en')
            expected = param_testdata.get('expected')
            assert zh_en_merge(input_zh, input_en) == expected
    
        # pytest参数化装饰器的传参格式为("参数1, 参数2", 列表数据如[(input1, expected1), (input2, expected2)]])
        # 转换为合适的传参格式
        testdata_for_parametrize = [(t.get('input_zh'), t.get('input_en'), t.get('expected')) for t in testdata]
    
        @pytest.mark.parametrize('input_zh, input_en, expected', testdata_for_parametrize)
        def test_zh_en_merge_with_parametrize(self, input_zh, input_en, expected):
            assert zh_en_merge(input_zh, input_en) == expected
    
    ```

=== "被测方法"

    ```python
    import re
    
    
    def zh_en_merge(cn: str, en: str) -> str:
        """
        把传入的字符串排除html字符、{}字符等，并以“中文(英文)”的格式进行拼接
        但由于语言语法问题导致结果不理想
        :param cn: 中文字符串
        :param en: 英文字符串
        :return: 合并后的字符串
        """
        # (?:...) 非捕获分组，保留匹配的内容不再匹配
        # <[^>]+> 匹配html标签
        # \{.*?\} 匹配{xxx}格式的参数
        # [^<>{}:]++ 无花括号、尖角符号、冒号的字符串
        zh_res = re.findall(r'(?:<[^>]+>|\{.*?\}|[^<>{}:]+|:)', cn)
        en_res = re.findall(r'(?:<[^>]+>|\{.*?\}|[^<>{}:]+|:)', en)
        for i in range(len(zh_res)):
            if zh_res[i].strip() != en_res[i].strip():
                zh_res[i] += f'({en_res[i].strip()})'
    
        marge_str = ''.join(zh_res)
        return marge_str
    
    ```

=== "YamlUtil.py"

    ```python
    import os
    import yaml
    
    
    # Yaml文件读取的工具类
    class YamlUtil:
        def __init__(self, file_dir):
            self.file_dir = str(file_dir)
    
        def get_yaml_data(self) -> dict:
            if os.path.exists(self.file_dir):
                data = open(self.file_dir, 'r', encoding='utf-8')
                res = yaml.load(data, Loader=yaml.FullLoader)
            else:
                raise FileNotFoundError("文件路径不存在，请检查")
            return res
    ```

=== "测试数据"

    ```yaml
    zh_en_merge_testdata:
      - input_zh: '<b>{description}</b>\n日期:{1}\n时间:{2}'
        input_en: '<b>{description}</b>\nDate:{1}\nTime:{2}'
        expected: '<b>{description}</b>\n日期(\nDate):{1}\n时间(\nTime):{2}'
      - input_zh: '支付<b>{0}</b>(<b>{1}</b> 来自国库)获取此资源。'
        input_en: 'Pay <b>{0}</b> (<b>{1}</b> in treasury) to claim this resource.'
        expected: '支付(Pay)<b>{0}</b>(<b>{1}</b> 来自国库)获取此资源。(in treasury) to claim this resource.)'
    ```

运行结果：

```text
TestZhEnMerge.py::TestZhEnMerge::test_zh_en_merge[param_testdata0] PASSED [ 25%]
TestZhEnMerge.py::TestZhEnMerge::test_zh_en_merge[param_testdata1] PASSED [ 50%]
TestZhEnMerge.py::TestZhEnMerge::test_zh_en_merge_with_parametrize[<b>{description}<\b>\n\u65e5\u671f:{1}\n\u65f6\u95f4:{2}-<b>{description}<\b>\nDate:{1}\nTime:{2}-<b>{description}<\b>\n\u65e5\u671f(\nDate):{1}\n\u65f6\u95f4(\nTime):{2}] PASSED [ 75%]
TestZhEnMerge.py::TestZhEnMerge::test_zh_en_merge_with_parametrize[\u652f\u4ed8<b>{0}<\b>(<b>{1}<\b> \u6765\u81ea\u56fd\u5e93)\u83b7\u53d6\u6b64\u8d44\u6e90\u3002-Pay <b>{0}<\b> (<b>{1}<\b> in treasury) to claim this resource.-\u652f\u4ed8(Pay)<b>{0}<\b>(<b>{1}<\b> \u6765\u81ea\u56fd\u5e93)\u83b7\u53d6\u6b64\u8d44\u6e90\u3002(in treasury) to claim this resource.)] PASSED [100%]
```

### 🚁 关于控制台打印将汉字转为ASCII码

从上述运行结果可以看出，使用`pytest.mark.parametrize`装饰器时，控制台打印将汉字转为了ASCII码。

实际上各文件编码都是utf-8，且调试时也能正常解析汉字，不影响运行结果。

![parametrize_debug](./img/Snipaste_2024-02-25_13-08-27.jpg)

[解决方案](https://dandelioncloud.cn/article/details/1596087866059079681)可参考这一篇

---