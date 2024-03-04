### 🚁 一些符号及示例

|  符号   | 说明           |
|:-----:|:-------------|
|  `*`  | 匹配前面的模式零次或多次 |
|  `+`  | 匹配前面的模式一次或多次 |
|  `?`  | 匹配前面的模式零次或一次 |
| `.*?` | 最小匹配         |
| `.*`  | 贪婪匹配         |
| `[]`  | 匹配中括号内的字符    |
| `[^]` | 表示非中括号内的字符   |

=== "re去掉html标签"

    ```python
    html = '<p>Hello, <em>world!</em></p>'
    
    # [^>]-表示非>的字符
    regex = re.compile(r'<[^>]+>', re.S)  # re.S表示多行模式
    desc = regex.sub('', html)  # re.sub()根据regex匹配，将匹配的值替换为''
    print(desc)  # 输出Hello, world!
    
    # 或者直接re.sub()，匹配后替换
    desc = re.sub('<[^<]+?>', '', html)
    print(desc)  # 输出Hello, world!

    ```

=== "re.findall()"
    
    ```python
    text = '【xx1】【xx2】【xx3】'
    regex = re.compile(r'【(.*?)】')
    # re.findall()根据regex匹配，将匹配的值存储为列表
    data = re.findall(regex, text)
    print(data)  # 输出['xx1', 'xx2', 'xx3']

    ```

=== "非捕获分组"

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
        # (?:...) 非捕获分组，非捕获分组，表达式匹配到的内容不再进行捕获
        # <[^>]+> 匹配html标签
        # \{.*?\} 匹配{xxx}格式的参数
        # [^<>{}:]+ 无花括号、尖角符号、冒号的字符串
        zh_res = re.findall(r'(?:<[^>]+>|\{.*?\}|[^<>{}:]+|:)', cn)
        en_res = re.findall(r'(?:<[^>]+>|\{.*?\}|[^<>{}:]+|:)', en)
        for i in range(len(zh_res)):
            if zh_res[i].strip() != en_res[i].strip():
                zh_res[i] += f'({en_res[i].strip()})'
    
        marge_str = ''.join(zh_res)
        return marge_str
    
    
    if __name__ == '__main__':
        print(repr(zh_en_merge('<b>{description}</b>\n日期:{1}\n时间:{2}', '<b>{description}</b>\nDate:{1}\nTime:{2}')))

    ```

=== "re.spilt()"
    
    ```python
    test_str = 'sheep dog pig \n bird \t cock'
    # \s+ 匹配一个或多个空白字符（包括空格、换行符、制表符等）
    split_result = re.split(r'\s+', test_str)
    print(split_result)  # ['sheep', 'dog', 'pig', 'bird', 'cock']

    ```

=== "匹配年月"

    ```python
    ^([1-9]\d{3})(([0]{0,1}[1-9])|([1][0-2]))$
    # ^-代表开头  $-代表结束
    # [1-9] 表示一个'1至9'以内的数字
    # \d 表示[0-9]  \d{3} 表示三个[0-9]数字
    # [0]{0,1} 零出现0或1次
    ```

!!! note "补充"

    ```
    re.match(str,str2)匹配以str开头的字符串，失败返回none，成功返回match对象，需搭配group使用
    re.search()在整个字符串匹配，失败返回none，成功返回match对象，需搭配group使用
    matchObj.group(n)返回第n个匹配的子串,n从1开始计数。
    如果没有分组，则matchObj.group()/matchObj.group(0)返回整个匹配的子串。
    ```

