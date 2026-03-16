## 📌 笔试题

### 🚁 1.统计文件词频

Please use your most familiar program language or pseudo code to finish the following examination

There is a text file with 2000 lines. There is only one word in each line.
Please output the word which appears most frequently in the first 1000 lines and also calculate how many times it appears in the file.

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
        counter = collections.Counter(words_first_1000)
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
    most_common = counter.most_common(3)
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
