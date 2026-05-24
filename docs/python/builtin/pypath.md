```python
import glob
import os

basic = os.path.abspath(__file__)  # 当前文件的绝对路径
parent = os.path.dirname(basic)  # 当前文件的目录
parent = os.path.dirname(__file__)  # 获取当前文件所在目录
# target = os.getcwd()  # 获取工作目录，结果会随着调用位置而改变
target = os.path.join(parent, "strategy")

if not os.path.exists(target):
    os.mkdir(parent)

target = os.path.join(target, "*strategy*.py")  # 路径拼接
t_dir = glob.glob(target)  # 模糊匹配当前目录下所有"*strategy*.py"文件，返回类型为list
for i in t_dir:
    print(os.path.dirname(i))  # 打印文件路径
    print(os.path.basename(i))  # 打印文件名
    print(os.path.split(i))  # 分隔路径和文件名，返回类型为tuple

# 参考资料：https://www.runoob.com/python/python-os-path.html

# python3.4加入的标准库
from pathlib import Path

# 创建一个指向当前目录的Path对象，即pwd
path = Path(".")

# 创建一个指向绝对路径的Path对象
absolute_path = Path(basic)

# 使用Path对象的方法进行操作
print(path.resolve())  # 打印绝对路径
print(path.resolve().as_posix()) # 转为字符串，适用于跨平台路径
print(path.resolve().parent)  # 打印父级路径
print(path.exists())  # 检查路径是否存在
print(list(path.glob('*.py')))  # 模糊查询当前目录所有.py文件

dirs = path.resolve().parent.rglob("*strategy*.py")  # find ./ -name "*strategy*.py"，当前目录及其所有子目录中递归地搜索
for i in dirs:
    print(i)

# Path的路径拼接方式
# 使用 / 连接路径
tmp1 = path.resolve().parent / "dp_browser"
# 使用 joinpath 方法连接路径
tmp2 = tmp1.joinpath("strategy", "strategy.py")
# 改变文件名
tmp3 = tmp2.with_name("strategy.txt")
# 改变文件后缀
tmp4 = tmp3.with_suffix(".py")
print(tmp4)

```

## 📌 遍历目录及子目录

os.walk(file_path)