协程函数，使用`asynic`定义的函数：`asynic def func`，在python3.5引入。
    
协程对象，执行协程函数()时仅得到协程对象，内部代码不会执行。

```python
import asyncio

async def func():
    print('hello world')

# 运行异步函数体的内容，需要将协程对象交给事件循环进行处理。
# loop = asyncio.get_event_loop()
# loop.run_until_complete(func())
asyncio.run(func())  # 与以上两行等价，但asyncio.run在python3.7以上才可用

```

### 🚁 await

await + 可等待的对象（包括协程对象、asyncio.Future对象、Task对象）

挂起当前协程（任务），等待IO操作完成之后再继续执行。

```python
import asyncio

async def others():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return "返回值"

async def func():
    print("first")
    res1 = await others()
    print("IO请求结束，结果res1为：", res1)

    res2 = await others()
    print("IO请求结束，结果res2为：", res2)
    
asyncio.run(func())

```

### 🚁 Task对象

在事件循环中，将协程对象封装为Task对象，交给事件循环进行处理。

```python
import asyncio

async def func():
    print(1)
    await asyncio.sleep(2)
    print(2)
    return "返回值"

async def main():
    print("main开始")
    task_list = [
        asyncio.create_task(func(), name='n1'),
        asyncio.create_task(func(), name='n2')  # python3.7引入
    ]
    print("main结束")
    done, pending = await asyncio.wait(task_list, timeout=None)
    print(done)  # Set
    for task in done:
        print(task.result())

asyncio.run(main())

```

### 🚁 asyncio.Future对象

等待异步结果，Task的基类，更底层，一般不会直接用。

### 🚁 concurrent.futures.Future对象

使用线程池、进程池实现异步操作时用到的对象，主要在异步与同步间转换时使用，如异步编程时，遇到不支持异步的第三方组件。

```python
import time
import asyncio
import concurrent.futures

def func1():
    # 某个耗时操作
    time.sleep(2)
    return "test"

async def main():
    loop = asyncio.get_running_loop()
    # 内部先调用ThreadPoolExecutor的submit方法去线程池（默认是线程池）中申请一个线程去执行func1函数，返回concurrent.futures.Future对象
    # 再调用asyncio.wrap.future，将其包装为asyncio.Future对象
    fut = loop.run_in_executor(None, func1)  # 其他参数可传入func1的传参
    result = await fut
    print('default thread pool', result)

    # 在线程池中使用
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, func1)
        print('custom thread pool', result)

    # 在进程池中使用
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, func1)
        print('custom process pool', result)

asyncio.run(main())

```

### 🚁 uvloop

asyncio事件循环的替代方案，基于uvloop的asyncio的速度几乎接近了Go程序的速度。

```python
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# 编写异步代码，与之前步骤一致

asyncio.run()
```

### 🚁 通过信号量(semaphore)控制并发数量

```python
import asyncio
import aiohttp
from typing import List

# 限制最大并发数为3
semaphore = asyncio.Semaphore(3)

async def fetch_data(url: str):
    print(f"Fetching {url}")
    async with semaphore:
        # 模拟网络请求或其他耗时操作
        await asyncio.sleep(1)
        print(f"Fetched {url}")

async def main(urls: List[str]):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(url) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    urls = [
        "http://example.com/1",
        "http://example.com/2",
        "http://example.com/3",
        "http://example.com/4",
        "http://example.com/5",
        "http://example.com/6"
    ]
    asyncio.run(main(urls))

```