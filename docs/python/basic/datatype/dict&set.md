## 📌 字典dict

* 键值对格式，如`dict1 = {'account':'7299'}`，与cookies数据格式类似。
* 无序，一个key只能对应一个value。
* 键必须为非空的、不可变对象；如`frozenset[1,2,3]`

### 🚁 字典常用方法

|                  方法                  | 说明                                             |
|:------------------------------------:|:-----------------------------------------------|
|  `dict1.get('account','Not exist')`  | 获取键'account'的值；不存在键时则返回'Not exist'避免抛异常        |
| `dict1.setdefault('account','none')` | 与get()类似，但不存在键时会设置默认值'none'                    |
|  `dict1.pop('account','Not exist')`  | 删除单个键值对，返回键'account'的值；不存在键时返回'Not exist'避免抛异常 |
|          `dict1.popitem()`           | 删除最后一个键值对，返回该键值对元组                             |
|           `dict1.clear()`            | 删除所有键值对                                        |
|     `dict1.update({'pw':'008'})`     | 更新字典，若键相同，则更新值，若键不存在，则添加键值对                    |
|           `dict1.items()`            | 返回字典中所有键值对的元组的列表，即键值对的列表                       |
|            `dict1.keys()`            | 返回字典中所有键的列表                                    |
|           `dict1.values()`           | 返回字典中所有值的列表                                    |

```python
# 仅修改键不修改值
dict1 = {'括号（）': '7299'}
dict1['无括号'] = dict1.pop('括号（）')

dict1.update({'account': '7299'})
k_list = list(dict1.keys())  # ['无括号', 'account']
v_list = list(dict1.values())  # ['7299', '7299']

k_list.append('key3')
# 列表转字典
dict2 = dict(zip(k_list, v_list))  # zip()取最少个数作为长度

list3 = ['key1']
dict3 = zip(k_list, v_list, list3)
print(list(dict3))  # 输出[('无括号', '7299', 'key1')]

```

### 🚁 字典遍历

```python
dict1 = {'account': '7299'}

for key, value in dict1.items():
    print(key, ":", value)

```

## 📌 集合set

* 与字典类似，但没有值，相当于字典的键集合。
* 创建空集合只能使用`s = set()`，因为`s={}`创建的是空字典
* 无序唯一，适用于重复内容去重
* 交集&、并集|、差集-、补集^；补集：返回两个集合的非共同元素。

## 📌 match-case

Python 3.10引入的新特性，类似switch-case

```python
def process_data(data):
    match data:
        case 0:
            return "Zero"
        case x if x > 0:
            return f"Positive number: {x}"
        case x if x < 0:
            return f"Negative number: {x}"
        case str() if len(data) > 5:
            return f"Long string: {data}"
        case str():
            return f"Short string: {data}"
        case [x, y]:
            return f"Two-element list: {x}, {y}"
        case _:
            return "Unknown data format"

# 使用示例
print(process_data(0))           # 输出: Zero
print(process_data(10))          # 输出: Positive number: 10
print(process_data(-5))          # 输出: Negative number: -5
print(process_data("hello"))     # 输出: Short string: hello
print(process_data("hello world"))  # 输出: Long string: hello world
print(process_data([1, 2]))      # 输出: Two-element list: 1, 2

```

---

