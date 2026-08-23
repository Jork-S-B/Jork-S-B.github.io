可变类型主要包括：列表、字典、集合

不可变类型主要包括：整数、字符串、浮点数、元组

## 📌 字符串的拼接方式

字符串不可变，每次拼接都是创建新对象并复制数据，这是性能开销的根源。

| 拼接方式 | 代码示例 | 时间复杂度 | 内存开销 | 适用场景（推荐指数） |
| :--- | :--- | :--- | :--- | :--- |
| 字面量隐式拼接 | `s = "Hello " "World"` | O(n) （编译时完成，运行时零开销） | 极低（常量池优化） | 静态长字符串换行。代码中直接写死的多行文本（如SQL、正则）。 |
| `+` 运算符 | `s = "A" + str(num) + "B"` | O(n) （CPython会做常量折叠优化） | 单次分配 | 少量确定变量的简单组合，绝对禁止在循环中使用。 |
| `f-string` | `s = f"User {name} age {age}"` | O(n) （底层调用 `PyUnicode_Append`） | 单次分配 | 运行时表达式嵌入，可读性强。 |
| `str.join()`（列表） | `s = "".join(list_of_parts)` | O(n) （预计算总长，一次性分配内存） | 极低（仅一份最终结果+列表引用） | 动态循环拼接时首选，或已知所有片段能存入列表的场景。 |
| `io.StringIO` | `buf.write("A"); buf.write("B")` | O(n) （分段缓冲，动态扩容） | 中等（维护缓冲区，类似动态数组） | 流式分段写入，适合写入逻辑复杂（含条件判断、嵌套函数）、或需要模拟文件的操作。 |

- 追求性能且数量已知，用`list + join()`
- 追求逻辑复杂、书写优雅且可接受最终占用内存，用`StringIO`
- 追求极致内存效率且可流式处理，用[`yield`](./yield/#_1)

## 📌 tuple list dict 适用场景

* 元组：适用于字段固定、只需遍历、关注数据完整性的场景；不可变使其可哈希，可作为字典的键`{(x1,x2,x3): value}`，相比列表更省内存，防误改。
* 列表：内部方法有`append()`、`insert()`、`pop()`等，适用于需要频繁修改的（有序）场景。
* 字典：键值对，适用于通过唯一键快速取值的映射关系；计数或者计算词频也使用，但`Counter`更优雅。

## 📌 == 和 is

- `==`: 对比变量值
- `is`: 对比内存地址

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

- 深拷贝 copy.deepcopy() ，递归地创建新对象，完全独立。

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

=== "推导式面试题"

    ```python
    # 面试题1：一行代码筛选出：字符串列表中，以下划线开头的字符串
    tmp = [i for i in str_list if i.startswith("_")]
    print(tmp)  # 输出['_abc', '_def']
       
    # 面试题2：对一个列表，第一步去重，第二步用推导式求出能被 5 整除的新列表，怎么写？
    lst = [10, 15, 20, 15, 10, 7, 25, 0, -5]
    unique_lst = list(set(lst))  # 简单去重，顺序可能变
    # 或保持顺序：unique_lst = list(dict.fromkeys(lst))

    # 第二步：推导式筛选能被5整除的数
    result = [x for x in unique_lst if x % 5 == 0]
    print(result)  # 输出: [10, 20, 15, 25, 0, -5]
    
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