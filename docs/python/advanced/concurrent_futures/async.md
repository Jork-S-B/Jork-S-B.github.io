| 代码 | 概念 |
|---|---|
| `async def gen_cases` | 定义协程函数 |
| `gen_cases(r)` 不加 await 时 | 只是协程对象，不执行 |
| `await client...create` | 在结果返回前挂起，交还控制权给事件循环(EventLoop) |
| `asyncio.gather(*[...])` | 协程任务采集后一起交给事件循环 |
| `asyncio.run(main())` | 事件循环入口 |
| `async with sem` | Semaphore限流，控制并发数 |

事件循环与OS的交互: 当 Socket 就绪或 I/O 完成时，OS 唤醒正在等待的事件循环；事件循环执行 I/O 回调、完成 Future，再调度 Task 恢复协程。

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

## 🚁 uvloop

asyncio事件循环的替代方案，基于uvloop的asyncio的速度几乎接近了Go程序(前提是单核+IO密集型任务)的速度。

基于C语言的底层库: `libuv`（跨平台统一 epoll/kqueue/IOCP），只需替换事件循环，`解决异步IO的效率`。

??? question "为什么 C 库比 Python 快"

    1. 解释 vs 编译

        Python 代码要先编译成字节码，再由解释器逐条读、逐条执行。每执行一条字节码，都有一次“分发开销”（判断这是哪条指令、然后跳到对应处理）。

        C 代码编译成机器码，CPU 直接执行指令，没有“逐条读”这一层。

    2. 动态类型检查

        Python 里 total += i，解释器每一轮都要先查 total 是什么类型、i 是什么类型，才能决定怎么加。

        C 里 int total，类型编译期就定死，直接整数加法，不查。

    3. 对象模型开销

        Python 的 int 是对象（PyObject），有引用计数、有结构体头。每次运算都要创建新对象、改引用计数、释放旧对象。

        C 的 int 就是内存里 4/8 个字节，算完就完事。

```python
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# 编写异步代码，与之前步骤一致

asyncio.run()
```

## 🚁 异步编程中遇到CPU密集任务

思路: 把CPU密集/同步阻塞任务，放到事件循环外，避免阻塞主线程。

cpu_bound() 保持普通同步函数，用 loop.run_in_executor(process_pool, cpu_bound, text)，再 await 它

```python
import asyncio
import os
import time
from concurrent.futures import ProcessPoolExecutor


def cpu_bound(n: int) -> int:
    """模拟 CPU 密集任务：纯 Python 计算，适合放进程池。"""
    total = 0
    for i in range(n):
        total += i * i
    return total


async def heartbeat(stop: asyncio.Event) -> None:
    """心跳协程：如果事件循环没被阻塞，它会持续打印。"""
    i = 0
    while not stop.is_set():
        print(f"[heartbeat {i}] {time.strftime('%X')}")
        i += 1
        await asyncio.sleep(0.3)


async def main() -> None:
    loop = asyncio.get_running_loop()

    stop = asyncio.Event()
    hb_task = asyncio.create_task(heartbeat(stop))

    # 关键：CPU 密集用 ProcessPoolExecutor，而不是默认 ThreadPoolExecutor
    max_workers = os.cpu_count() or 4

    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        nums = [8_000_000, 9_000_000, 10_000_000, 11_000_000]

        futures = [
            loop.run_in_executor(pool, cpu_bound, n)
            for n in nums
        ]

        results = await asyncio.gather(*futures)
        print("results:", results)

    stop.set()
    await hb_task


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    print(f"elapsed: {time.perf_counter() - start:.2f}s")

```

## old

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

