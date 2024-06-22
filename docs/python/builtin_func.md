## 📌 转换和筛选

map(func, iter)  
对可迭代对象中的每个元素应用一个指定的函数，返回一个迭代器，这个过程通常被称为映射或转换

filter(func, iter)  
对可迭代对象中的每个元素进行过滤，只保留那返回值为True的元素，返回一个迭代器

```python
tmp_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
map_list = map(lambda x: x * 2, tmp_list)
filter_list = filter(lambda x: x % 2 == 0, tmp_list)
print(list(map_list))  # [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
print(list(filter_list))  # [2, 4, 6, 8, 10]

```

## 📌 排序

sorted(iter, key=None, reverse=False)  
对可迭代对象进行排序，并返回排序后的列表，原列表不会被修改；key可传方法名

```python
tmp_list = ['Alias', 'xx', 'David', '1']
a = tmp_list.sort()
print(a)  # None,list.sort()直接在原列表排序，返回None
b = sorted(tmp_list, key=len, reverse=True)
print(b)  # ['Alias', 'David', 'xx', '1']

```

## 📌 求和求积

sum(iter, start=0)
可迭代对象中元素总和

functools.reduce(func, iter, initial=None)  
可迭代对象进行分解计算

```python
numbers = [1, 2, 3]
total = sum(numbers, start=10)
print(total)  # 输出: 16

from functools import reduce

numbers = [1, 2, 3, 4]
product = reduce(lambda x, y: x * y, numbers, 2)  # 初始值为2
print(product)  # 输出: 48

```

## 📌 all

all()  
判断可迭代对象中所有元素是否都为真；如果可迭代对象为空，也会返回True。

```python
list1 = [0, 1, 2, 3, 4, 5]
print(all(i > 0 for i in list1))  # False

```

## 📌 执行字符串表达式

eval()  
可用于执行字符串中的有效代码或表达式，但处理不受信任输入的情况应避免使用。

ast.literal_eval()  
只能处理基本数据类型的字面量，因此无法执行任何潜在有害的操作。当输入包含非预期的数据，抛ValueError异常。

总结：如果只是想安全地解析字符串形式的数据结构，应该使用`ast.literal_eval`；如果需要执行更复杂的Python代码，则应谨慎使用`eval`，并确保输入是可信的，以避免安全风险。

```python
import ast

s = "[1, 2, {'key': 'value'}, 'hello']"

data = ast.literal_eval(s)
print(data)  # 输出：[1, 2, {'key': 'value'}, 'hello']

str1 = "pow(data[1], 3)"
print(eval(str1))  # 输出：8

try:
    print(ast.literal_eval(str1))
except ValueError as e:
    print(e)  # 非字面量表达式时抛异常

```

## 📌 getattr

getattr(obj, func, defult=None)
从对象或实例中动态获取一个属性或者方法

```python
class Person:
    pass


class PersonSubclass(Person):
    
    def introduce2(self):
        print("test")


def re_func(funcname, obj=Person()):
    r = getattr(obj, funcname)()
    return r


person_subclass = PersonSubclass()
print(re_func("introduce2", person_subclass))  # 输出：test\nNone

```