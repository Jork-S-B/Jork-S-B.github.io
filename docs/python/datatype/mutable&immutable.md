可变类型主要包括：列表、字典、集合

不可变类型主要包括：整数、字符串、浮点数、元组

## 📌 方法参数默认值为可变类型

方法参数默认值为可变类型时，若函数调用未传值，则调用函数时操作的实际是同个对象。

应当使用None作为默认值，并在程序中重新初始化。

```python
def func(arg_a, list_arg=None):
    list_arg = list_arg or []
    list_arg.append(arg_a)
    print(list_arg)
```

## 📌 不定数量的方法传参

* `*args`将传参打包为元组tuple，`**kwargs`将传参打包为字典dict。
* `*args`和`**kwargs`是约定俗成的命名方式，实际上可以是任何名称。
* `*args`和`**kwargs`参数通常被放置在参数列表的最后，避免编译器无法正确解析预期的固定参数。

```python
def my_function(required_arg, *args, **kwargs):
    print("固定参数:", required_arg)
    print("args:", args)
    print("kwargs:", kwargs)


my_function(1, 2, 3, key1="value1", key2="value2")

# 输出：
# 固定参数: 1
# args: (2, 3)
# kwargs: {'key1': 'value1', 'key2': 'value2'}
```

## 📌 浅拷贝与深拷贝

针对可变类型的元素

- 浅拷贝仅复制其引用，当对象存在嵌套层次时，其内部元素的引用也会被复制，修改影响原对象。适合复制不可变对象或顶层结构。

- 深拷贝会递归地复制对象及其所有嵌套层次的内容，并创建完整副本，而不是引用。

```python
a = [1, 2, [3, 4]]
b = a.copy()  # 浅拷贝
b[2][0] = 5
b[1] = 1
print(a)  # 输出[1, 2, [5, 4]]
print(b)  # 输出[1, 1, [5, 4]]

import copy

a = [1, 2, [3, 4]]
b = copy.deepcopy(a)  # 深拷贝
b[2][0] = 5
b[1] = 1
print(a)  # 输出[1, 2, [3, 4]]
print(b)  # 输出[1, 1, [5, 4]]

```

## 📌 推导式

用于从序列或其他可迭代对象创建新的列表、集合或字典。

* 列表推导式格式如：`[表达式 for 变量 in 列表 if 条件]`
* 字典推导式格式如：`{表达式1:表达式2 for 变量 in 列表 if 条件}`
* 集合推导式格式如：`{表达式 for 变量 in 列表 if 条件}`

=== "示例"

    ```python
    ml = [x for x in range(10) if x % 2 == 0]
    print(ml)  # 输出[0, 2, 4, 6, 8]
    
    md = {x: x ** 2 for x in range(10) if x % 2 == 0}
    print(md)  # 输出{0: 0, 2: 4, 4: 16, 6: 36, 8: 64}
    
    ms = {x for x in range(10) if x % 2 == 0}
    print(ms)  # 输出{0, 2, 4, 6, 8}
    
    ```

=== "推导式获取两个字典中差异的键值对"

    ```python
    def compare_dict(expected: dict, actual: dict) -> list:
        """
        推导式获取两个字典中差异的键值对
        :param expected: 预期结果
        :param actual: 实际结果
        :return: list
        """
        diff = ['{key}该键值不一致：预期为{v1}，实际为{v2}'.format(key=key, v1=expected[key], v2=actual.get(key))
                for key in expected if str(expected[key]) != str(actual.get(key))]
    
        if diff:
            print("有如下字段值不一致：")
            print('\n'.join(diff))
        else:
            print('字段值一致')
        return diff
    
    
    # 对比两个字典，并打印有差异的键值对
    dict1 = {'name': '张三', 'age': '18', 'sex': '男'}
    dict5 = {'name': '王五', 'age': 18}
    compare_dict(dict1, dict5)
    
    # 输出：
    # 有如下字段值不一致：
    # name该键值不一致：预期为张三，实际为王五
    # sex该键值不一致：预期为男，实际为None

    ```

---