## 📌 collections.Counter

Python标准库中的高效计数器，属于字典的子类，用于统计对象出现的次数。

### 🚁 创建方式

=== "从列表创建"

    ```python
    words = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple'] 
    counter = Counter(words) 
    print(counter) # Counter({'apple': 3, 'banana': 2, 'orange': 1})
    ```

=== "从字符串创建"

    ```python
    char_counter = Counter('hello world') 
    print(char_counter) # Counter({'l': 3, 'o': 2, 'h': 1, 'e': 1, ' ': 1, 'w': 1, 'r': 1, 'd': 1})
    ```

=== "从关键字参数创建"

    ```python
    counter_kwargs = Counter(a=3, b=2, c=1) 
    print(counter_kwargs) # Counter({'a': 3, 'b': 2, 'c': 1})
    ```

=== "空Counter"

    ```python
    counter_empty = Counter() 
    counter_empty.update(['apple', 'banana', 'apple']) 
    print(counter_empty) # Counter({'apple': 2, 'banana': 1})
    print(list(counter_empty.elements()))  # ['apple', 'apple', 'banana']
    ```

### 🚁 常用方法

| 方法                           | 说明                | 返回值类型         |
|------------------------------|-------------------|---------------|
| `Counter.most_common(n)`     | 返回出现次数最多的n个元素及其计数 | `list[tuple]` |
| `Counter.elements()`         | 展开所有元素            | `iterator`    |
| `Counter.update(iterable)`   | 更新计数器，增加计数        | `None`        |
| `Counter.subtract(iterable)` | 更新计数器，减少计数        | `None`        |
| `del counter[key]`           | 删除某个元素的计数         | -             |

### 🚁 集合用法

```python 
from collections import Counter
c1 = Counter(a=3, b=1, c=2) 
c2 = Counter(a=1, b=2, c=3)

# 加法：对应元素计数相加
print(c1 + c2) # Counter({'c': 5, 'a': 4, 'b': 3}) 

# 减法：对应元素计数相减（结果不能为负）
print(c1 - c2) # Counter({'a': 2})

# 交集：取每个元素的最小计数
print(c1 & c2) # Counter({'c': 2, 'b': 1, 'a': 1})

# 并集：取每个元素的最大计数
print(c1 | c2) # Counter({'c': 3, 'a': 3, 'b': 2})

```

## 📌 collections.deque

双端队列，线程安全的列表，支持在两端高效地添加和删除元素。

```python
from collections import deque
# 创建 deque
dq = deque([1, 2, 3])

# 右侧添加
dq.append(4) 
print(dq) # deque([1, 2, 3, 4])
# 左侧添加
dq.appendleft(0) 
print(dq) # deque([0, 1, 2, 3, 4])

# 右侧弹出
print(dq.pop()) # 4 
print(dq) # deque([0, 1, 2, 3])
# 左侧弹出
print(dq.popleft()) # 0 
print(dq) # deque([1, 2, 3])

# 限制最大长度
dq_limited = deque(maxlen=3) 
for i in range(5): 
    dq_limited.append(i) 
print(dq_limited) # deque([2, 3, 4], maxlen=3)，队列-先进先出

```

## 📌 collections.defaultdict

默认字典，当访问不存在的键时，自动提供默认值。

```python
from collections import defaultdict

# 创建默认值为 int(0) 的字典
dd = defaultdict(int) 
dd['apple'] += 1 
print(dd['apple']) # 1 
print(dd['banana']) # 0，自动创建并返回默认值

# 创建默认值为 list 的字典
dd_list = defaultdict(list) 
dd_list['fruits'].append('apple') 
print(dd_list) # defaultdict(<class 'list'>, {'fruits': ['apple']})

# 自定义默认值工厂
def default_value(): 
    return 'unknown'
dd_custom = defaultdict(default_value) 
print(dd_custom['missing']) # unknown

```

## 📌 collections.namedtuple

命名元组/具名元组类，创建带有字段名的元组子类。

实际应用场景：函数参数数量较多（一般指多于5个），且参数间有一定相关性时，[具名函数](../oop/#_8) 

```python
from collections import namedtuple

# 创建命名元组类
Point = namedtuple('Point', ['x', 'y']) 
p = Point(x=1, y=2)
print(p.x) # 1
print(p.y) # 2
print(p[0]) # 1，也可以用索引访问

# 转换为字典
print(p._asdict()) # OrderedDict([('x', 1), ('y', 2)])

# 替换字段
p_new = p._replace(x=10) 
print(p_new) # Point(x=10, y=2)

# 实际应用场景
Person = namedtuple('Person', ['name', 'age', 'city']) 
people = [ Person('Alice', 25, 'Beijing'), Person('Bob', 30, 'Shanghai') ] 
for person in people: 
    print(f"{person.name} is {person.age} years old")

```

## 📌 collections.OrderedDict

有序字典，保持插入顺序的字典（Python 3.7+：普通dict已默认有序）。

```python
from collections import OrderedDict
od = OrderedDict() 
od['first'] = 1 
od['second'] = 2 
od['third'] = 3
print(list(od.keys())) # ['first', 'second', 'third']

# 移动到末尾
od.move_to_end('first') 
print(list(od.keys())) # ['second', 'third', 'first']

# 移动到开头
od.move_to_end('first', last=False) 
print(list(od.keys())) # ['first', 'second', 'third']

```

## 📌 collections.ChainMap

链式映射,将多个字典组合成一个视图。

```python
from collections import ChainMap
dict1 = {'a': 1, 'b': 2} 
dict2 = {'b': 3, 'c': 4}
cm = ChainMap(dict1, dict2) 
print(cm['a']) # 1 
print(cm['b']) # 2，优先使用第一个字典的值 
print(cm['c']) # 4

# 添加新字典
cm_new = cm.new_child({'d': 5}) 
print(cm_new['d']) # 5

# 实际应用：合并配置
defaults = {'color': 'red', 'size': 'M'} 
user_prefs = {'size': 'L'} 
env_vars = {'color': 'blue'}
config = ChainMap(env_vars, user_prefs, defaults) 
print(config['color']) # blue，优先级：env_vars > user_prefs > defaults 
print(config['size']) # L

```

---

## 📌 笔试题

### 🚁 1.统计文件词频

Please use your most familiar program language or pseudo code to finish the following examination

There is a text file with 2000 lines. There is only one word in each line.

Please output the word which appears most frequently in the first 1000 lines and also calculate how many times it
appears in the file.

```python

import collections
import random


def find_frequent_word(filename) -> tuple:
    """
    读取文件（2000行，每行一个单词），找出前1000行中出现频率最高的单词，
    并计算该单词在整个文件中出现的总次数。
    :param filename: 文件路径
    :return: tuple
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
        lines = [line.strip() for line in all_lines]

        # 1.找出前1000行中出现频率最高的单词，及出现的次数
        words_first_1000 = lines[:1000]
        counter = collections.Counter(words_first_1000)  # 返回Counter对象，它是dict的子类
        if not counter:
            raise ValueError("前1000行中无有效的单词")
        most_common_word = max(counter, key=counter.get)
        count_in_first_1000 = counter[most_common_word]

        # 2.统计整个文件中的出现次数
        total_count = lines.count(most_common_word)

        return most_common_word, count_in_first_1000, total_count

    except FileNotFoundError:
        print("文件不存在")
    except Exception as e:
        raise Exception(f"处理文件时发生错误：{str(e)}")


def generate_test_data(filename: str, line_count: int = 2000):
    """
    生成测试数据文件，每行一个单词
    :param filename: 输出文件名
    :param line_count: 总行数，默认 2000
    """
    # 准备一些常用英语单词
    words_pool = [
        'apple', 'banana', 'orange', 'grape', 'pear',
        'cat', 'dog', 'bird', 'fish', 'rabbit',
        'red', 'blue', 'green', 'yellow', 'black',
        'one', 'two', 'three', 'four', 'five',
        'day', 'week', 'month', 'year', 'time'
    ]

    # 生成随机数据
    lines = []
    for _ in range(line_count):
        word = random.choice(words_pool)
        lines.append(word)

    # 写入文件
    with open(filename, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

    print(f"已生成测试数据到文件：{filename}")

    # 统计，作为预期结果
    first_1000 = lines[:1000]
    counter = collections.Counter(first_1000)
    most_common = counter.most_common(3)  # 返回列表，列表中每个元素为：元组 (元素值，计数)
    print(f"前1000行中出现频率最高的3个单词:")
    for word, count in most_common:
        print(f"{word}:{count}次")

    # 统计整个文件中该单词的总数
    total_count = lines.count(most_common[0][0])
    print(f"'{most_common[0][0]}'在整个文件中出现了{total_count}次")


if __name__ == "__main__":
    # 生成测试数据
    generate_test_data("input.txt", 2000)

    print("\n开始执行统计")
    word, count_first_1000, total_count = find_frequent_word(r"input.txt")

    print(f"前1000行中出现最频繁的单词是：{word}")
    print(f"该单词在前1000行中出现了{count_first_1000}次")
    print(f"该单词在整个文件(2000行)中出现了{total_count}次")

```
