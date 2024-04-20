## 常用方法

|       方法       | 说明                    |
|:--------------:|:----------------------|
| `json.dump()`  | JSON格式的字典序列化至指定json文件 |
| `json.load()`  | 指定JSON文件反序列化为字典       |
| `json.dumps()` | 字典转符合JSON标准的字符串       |
| `json.loads()` | 符合JSON标准的字符串转字典       |

JSON标准：包含键值对、数组等，并且所有的字符串必须用***双引号***包围

`json.dumps(dict1)`跟`str(dict1)`打印效果类似，但后者转换的字符串中是以单引号包围。

`json.loads(str1)`跟`eval(str1)`打印效果类似，但后者不安全不高效（该方法会执行字符串中有效的代码或表达式）。

```python
import json

dict1 = {'no': '1', 'regex_str': '物品\t单价\t数量'}
filename = 'output.json'

with open(filename, 'w') as f:
    # ensure_ascii=False，保留非ASCII字符如汉字
    # indent=2，格式化，指定每级缩进的空格数为2
    json.dump(dict1, f, ensure_ascii=False, indent=2)  # dict1写入到output.json

with open(filename, 'r') as f:
    f_dict = json.load(f)  # 从output.json读取内容转为字典
    print(f_dict)  # 输出{'no': '1', 'regex_str': '物品\t单价\t数量'}

s = json.dumps(f_dict, ensure_ascii=False)  # f_dict转字符串
print(s)  # 输出{"no": "1", "regex_str": "物品\t单价\t数量"}

d = json.loads(s)  # str转dict
print(d)  # 输出{'no': '1', 'regex_str': '物品\t单价\t数量'}

print(d.get('regex_str'))  # 直接print()会自动转义，输出：物品    单价  数量
print(repr(d.get('regex_str')))  # repr()会保留转义或者特殊字符，输出：'物品\t单价\t数量'
print(eval(repr(d.get('regex_str'))))  # eval()执行转义，输出：物品    单价  数量

```

!!! note "补充"
    
    * `eval()`可用于执行字符串中的有效代码或表达式，但处理不受信任输入的情况应避免使用。
    * 与之相比，`ast.literal_eval()`只能处理基本数据类型的字面量，因此无法执行任何潜在有害的操作。当输入包含非预期的数据，抛ValueError异常。

    
    ```python
    import ast
    s = "[1, 2, {'key': 'value'}, 'hello']"
    
    # 使用 literal_eval 解析字符串
    data = ast.literal_eval(s)

    print(data)  # 输出：[1, 2, {'key': 'value'}, 'hello']
    ```
---