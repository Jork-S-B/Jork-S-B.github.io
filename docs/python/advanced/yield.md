处理大数据（比如读百万行日志）时，如何节省内存？

通过传统方式，一次性读到内存，可能直接OOM

```python
# 错误示范：一次性加载所有行到列表
with open('huge.log', 'r') as f:
    lines = f.readlines()  # 如果文件有1GB，内存就炸了
    for line in lines:
        process(line)
```

## 惰性求值

生成器通过惰性求值(lazy evaluation): 每次只产生一个值，不保留历史。用 yield 实现的函数返回一个迭代器，每次 next() 时才执行到下一个 yield。

生成器几乎不占内存，适合处理无限流或超大文件。

```python
def read_large_log(file_path):
    """生成器：每次 yield 一行，内存只存当前行"""
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:          # 文件对象本身也是生成器，逐行读取
            yield line.strip()  # 返回一行，然后暂停，等待下次调用

# 使用生成器处理百万行日志
for log_line in read_large_log('huge.log'):
    if 'ERROR' in log_line:
        print(log_line)  # 每次只处理一行，内存占用极小
```

适用场景

- 读取百万行接口日志
- 分页拉取API数据
- 解析大XML/JSON
- 造大量测试数据

```python
def data_generator(): 
  while True: 
    yield create_row()
```