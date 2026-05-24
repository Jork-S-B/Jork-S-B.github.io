序列：具备先后顺序，可以包含重复元素，通过序号访问。

## 📌 列表list

可变序列，创建后可修改内部元素。在内存管理上，“修改”操作直接作用于原有的内存空间，无需分配新的内存。

### 🚁 列表扩充方式

|          方式           | 补充说明       |
|:---------------------:|:-----------|
| `list1.append('999')` | 尾部追加       |
|         +或者+=         | 类似extend   |
|   `insert(0,'666')`   | 在索引位置插入列表项 |

### 🚁 列表常用方法

|          方法           | 补充说明                                     |
|:---------------------:|:-----------------------------------------|
|      `list1[-1]`      | 返回列表的最后一个元素                              |
|    `list1.sort()`     | 无返回值，直接在列表进行冒泡排序                         |
|  `list1.remove('5')`  | 删除列表中***第一个***'5'，无返回值；找不到该值时报ValueError |
|    `list1.pop(0)`     | 根据索引删除列表项，但要注意会改变后续项的索引                  |
| `list1.count("val1")` | 计数，计算"val1"在列表中的数量                       |                               
| `list1.index("val1")` | 找到"val1"在列表中的索引位置                        |                               
|    `list1.clear()`    | 清空列表                                     |                               
|    `list1.copy()`     | 浅拷贝                                      |                               
|   `list1.reverse()`   | 原地反转列表，无返回值                              |                               

```python
from typing import List


class Solution:

    @staticmethod
    # 删除nums无序列表中所有的val值
    def removeElement(nums: List[int], val: int) -> int:
        # 27. 移除元素，返回移除后数组的新长度
        while val in nums:
            nums.remove(val)
        length = len(nums)
        print('{len}, nums={nums}'.format(len=length, nums=nums))
        return length

    @staticmethod
    # 删除nums非严格递增列表中重复的元素
    def removeDuplicates(nums: List[int]) -> int:
        # 26. 删除有序数组中的重复项
        # nums = list(set(nums))  # 通过转为集合去重，但leetcode用不了该方法
        for i in range(len(nums) - 1, 0, -1):  # 遍历pop()需要倒序进行，正序pop()会改变原索引
            if nums[i] == nums[i - 1]:
                nums.pop(i)
        length = len(nums)
        print('{len}, nums={nums}'.format(len=length, nums=nums))
        return length

```

### 🚁 列表遍历方式

=== "直接遍历"

    ```python
    # 直接遍历，实际时按`索引 + 1`遍历
    list1 = [1, 24, 34]
    for item in list1:
        print(item)
    ```

=== "按索引遍历"

    ```python
    list1 = [1, 24, 34]
    for i in enumerate(list1):
        print(i)  # 输出：(0, 1)，即(索引，值)
    # 或者
    for i, x in enumerate(list1):
        print(i, x)  # 输出：0 1
    ```

=== "按下标遍历"

    ```python
    # 按下标遍历，不规范不推荐
    list1 = [1, 24, 34]
    for i in range(len(list1)):
        print(list1[i])
    ```

## 📌 元组tuple

不可变序列，创建后不能修改内部元素。在内存管理上，“修改”实际上是创建了一个新的对象，并将引用指向新对象，而原对象保持不变。

* 需要删除元素时，可利用切片的方式拆分，用连接操作符+指向新元祖。
* 只有1个元素时需要逗号如`('xx',)`

```python
tup = (1, 2, 3, 4)
# 使用切片和连接操作符来创建一个新的元组
new_tup = tup[:1] + tup[2:]
print(new_tup)  # 输出：(1, 3, 4)

```

## 📌 字符串str

特殊的序列，不可变。

### 🚁 字符串拼接的方式

大量字符串合并，且性能敏感时：

- 追求时间，优先选择list.append + str.join(Iterable)的方式

- 追求内存使用少，优先考虑+,+=

少量字符串合并或性能不敏感的场景以可读性优先。

|                  方式                   | 补充说明                               |
|:-------------------------------------:|:-----------------------------------|
| `'Hello {text}'.format(text='World')` | 当有'不受信任的外部数据'传入时禁用                 |
|          `f'Hello {局部变量名}'`           | 与format类似，可读性较高                    |
|                 +或者+=                 | 通过加号拼接，追求内存使用少时优先考虑                |
|            `'&'.join(str)`            | 在str各字符间插入'&'符号，也是将列表转为字符串的方式之一    |
|         `print('%10s' % str)`         | 类似C语言的%方式，%10s格式化左对齐，10个字符，不足时空格补全 |
|     `from string import Template`     | 面向对象的模板拼接                          |
|              `ord("A")`               | 返回字母A的Unicode编码值65                 |

```python
# ','.join()的传参非str类型时抛TypeError
try:
    list2 = [1, 2, 3]
    str2 = ','.join(list2)
except TypeError as e:
    print(e)  # 输出：sequence item 0: expected str instance, int found
    str2 = ','.join(map(str, list2))  # 先将list2的每个元素应用str()函数
else:
    print('pass')
finally:
    print(str2)  # 输出：1,2,3

```

### 🚁 字符串比较

Python字符串比较大小的原则是从左到右依次比较字符串中字符的Unicode值，如果遇到相同字符，继续比较下一个字符。

所以直接比较可能出现"3.11.0" < "3.6.0"的情况，如下示例：

```python
version = '3.8.0'
print(version < "3.6.0")  # 输出：False
version = '3.11.0'
print(version < "3.6.0")  # 输出：True

from packaging import version  # 使用第三方库比较版本号

ver = '3.11.0'
print(version.parse(ver) < version.parse("3.6.0"))

```

### 🚁 字符串常用方法

|           方法            | 说明                        |
|:-----------------------:|:--------------------------|
|     `str1.strip()`      | 去除首尾空格                    |
|     `str1.split()`      | 输入内容作为分隔符，返回列表；默认分隔符为空格   |
| `str1.replace('（','(')` | 字符串替换，此处是中文括号替换成英文符号      |
|     `str1.upper()`      | 返回大写字符串，转小写的是str1.lower() |
|   `str1.find("xxx")`    | 找到"xxx"在字符串中的索引位置         |

## 📌 切片

完整的切片表达式为`[start:end:step]`，其中`start`和`end`都是可选的，默认值为`0`和`len(obj)`，`step`默认值为`1`。

|     表达式      | 说明                                         |
|:------------:|:-------------------------------------------|
| `str[i: j]`  | 返回字符串str第i到j个元素的子序列（不包含第j个元素），当切片超过长度时结果为空 |
|  `str[:-1]`  | 返回索引0至索引-1，相当于去掉最后一位                       |
| `str[::-1] ` | 返回倒序的str                                   |

---
