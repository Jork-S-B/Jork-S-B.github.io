| 代码 | 概念 |
|---|---|
| `async def gen_cases` | 协程函数 |
| `gen_cases(r)` 不加 await | 只是协程对象，不执行 |
| `await client...create` | 在结果返回前挂起，交还控制权给事件循环(EventLoop) |
| `asyncio.gather(*[...])` | 协程任务采集后一起交给事件循环 |
| `asyncio.run(main())` | 事件循环入口 |
| `async with sem` | Semaphore限流，控制并发数 |

```python
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()

# 全局一份信号量：最多 10 个请求同时在飞
sem = asyncio.Semaphore(10)

async def gen_cases(requirement):
    # 进门前先领令牌，领不到就挂起排队（交还事件循环）
    async with sem:
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"为这个需求生成测试用例：{requirement}"}],
        )
        return resp.choices[0].message.content

async def main():
    reqs = ["登录功能", "支付功能", "注册功能", ...]  # 假设 1000 个

    # 1. 列表推导：把每个 req 变成协程（此时都还没跑）
    # 2. *：拆开成一个个协程
    # 3. gather：一起交给事件循环
    # 4. await：main 在此等全部跑完
    results = await asyncio.gather(*[gen_cases(r) for r in reqs])

    for r in results:
        print(r)

# 整个异步程序的入口：建事件循环 → 跑 main → 关闭
asyncio.run(main())
```

---

## 🚁 uvloop

asyncio事件循环的替代方案，基于uvloop的asyncio的速度几乎接近了Go程序的速度。

```python
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# 编写异步代码，与之前步骤一致

asyncio.run()
```

---

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

## 🚁 await

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

## 🚁 Task对象

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

## 🚁 asyncio.Future对象

等待异步结果，Task的基类，更底层，一般不会直接用。

## 🚁 concurrent.futures.Future对象

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

