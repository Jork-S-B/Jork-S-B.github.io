.env，环境变量，一般不想写死在代码里，又不想提交至git。

## 📌 文件要求

* 文件名：`.env`，通常位于根目录。
* 数据结构：键值对，如`APP_ENV=development`。键名必须全大写，键值字符串无需双引号，除非需要保留空格或特殊符号。
* 通过逗号分隔多个值。
* 键值不支持json等复杂的结构，也不支持python语法。

## 📌 调用

```python
# pip install python-dotenv

import os
from dotenv import load_dotenv

load_dotenv()  # 从根目录读取.env
print(os.getenv('APP_ENV'))

```

## 📌 添加至.gitignore

```.gitignore
# 忽略.env文件
.env

# 忽略.env开头的文件
.env.*

```