## 📌 进程&线程&协程

程序运行时，系统会为每个进程分配不同的内存空间；而对线程而言，除了CPU，系统不会为线程分配内存，线程之间只能共享资源。

* 线程：CPU执行的最小单元，多线程无需申请资源，子线程和父线程共享资源，通信快于进程通信。

* 进程：操作系统执行的基本单元，由系统分配资源和调度。

* 协程：微线程，只有一个线程执行，当子程序内部阻塞或者I/O等待时，在多个方法间切换执行。相比多线程，省去线程切换的开销，共享资源不需加锁，执行效率更高。

## 📌 Python多线程

不能并行，但能并发。

* 并行-parallel：同一时刻，有多条指令在多个处理器上同时执行。
* 并发-concurrency：同一时刻只能有一条指令执行，但多个进程指令被快速的轮换执行，使得在宏观上具有多个进程同时执行的效果。


### 🚁 全局解释器锁GIL

Python的多线程，由于全局解释器锁GIL的存在，实际上同一时刻只有一个线程在进行，并非真正的并行，但它仍可以提高程序效率。

在多线程程序中，当一个线程阻塞时，其他线程可继续执行，以提高程序的并发性和响应性。

!!! note "总结"

    * 对于I/O密集型任务（如网络请求、文件读写、数据库查询等）和高并发场景，建议使用协程-asyncio。
    * 对于CPU密集型任务（如加解密、图形渲染、大量计算、循环等），建议使用进程。通过进程绕开GIL，实现并行。
    * 对于需要共享数据和简单的并行处理场景，可以使用线程，但需要注意Python的GIL对性能的影响。

### 🚁 线程间通信

Python中多线程通信最常用的是使用`threading`模块中的`Queue`类。  
Queue是一个线程安全的队列，可以用于线程间的数据传递和通信，避免了直接共享内存可能引发的竞态条件。

|   Queue方法   | 说明        |
|:-----------:|:----------|
|    put()    | 向队列添加元素   |
|    get()    | 从队列获取元素   |
| task_done() | 通知队列任务已完成 |

```python
import threading
from queue import Queue


# 生产者线程
def producer(q):
    for i in range(5):
        q.put(i)
        print(f"Produced: {i}")
    q.put("生产者线程结束")


# 消费者线程
def consumer(q):
    while True:
        item = q.get()
        if item == "生产者线程结束":
            q.task_done()
            break
        print(f"Consumed: {item}")
        q.task_done()


# 创建队列
queue = Queue()

# 创建生产者和消费者线程
producer_thread = threading.Thread(target=producer, args=(queue,))
consumer_thread = threading.Thread(target=consumer, args=(queue,))

# 启动线程
producer_thread.start()
consumer_thread.start()

# 等待生产者线程结束
producer_thread.join()

# 等待消费者线程处理完所有任务
queue.join()
consumer_thread.join()

print("All threads finished.")
```

### 🚁 锁

悲观锁认为在任务时候都可能存在并发冲突，因此在访问共享资源时，会将其锁定，直至完成操作后才释放锁。  
实现方式如数据库的行级锁和JAVA的synchronized关键字，先取锁再访问。  
优点是可以保证数据的一致性，但在高并发时频繁加锁和释放锁，会导致性能下降。

乐观锁认为并发冲突的概率较小，因此在访问共享资源时不会立即加锁，先进行操作，然后在更新时检查资源是否被修改；若更新失败则重试。  
实现方式如版本号机制、数据库中的CAS(Compare And Swap)操作和JAVA的Atomic类，先访问再取锁。  
优点是可以提升高并发性能，但在并发冲突较多时需要多次重试，可能导致性能下降。

=== "Python锁示例"

    ```python
    import threading
    
    """
    Lock: 互斥锁，可以由任意线程解锁，不能重复上锁；重复上锁可能会导致死锁
    RLock: 重入锁，只能由锁定线程解锁，可以重复上锁，但也要重复解锁；适合递归调用的场景
    其他的还有Condition-条件锁，Event-事件锁，Semaphore-信号量锁等
    """
    # 创建一个锁对象
    lock = threading.RLock()
    
    # 全局变量
    counter = 0
    
    # def increment_counter():
    #     global counter
    #     # 获取锁
    #     lock.acquire()
    #     try:
    #         counter += 1
    #         print(f"Incremented counter to {counter}")
    #     finally:
    #         # 释放锁
    #         lock.release()
    
    # 使用with语句自动获取和释放锁，更加安全，也更易于阅读和维护
    def increment_counter():
        global counter
        with lock:  # 缺少锁会遇到竞态条件，导致最终计算结果不正确
            counter += 1
            print(f"Incremented counter to {counter}")
    
    # 创建线程列表
    threads = []
    
    # 创建并启动10个线程
    for _ in range(10):
        thread = threading.Thread(target=increment_counter)
        threads.append(thread)
        thread.start()
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()  # 阻塞主进程，直到线程结束
    
    # 输出最终的计数器值
    print(f"Final counter value: {counter}")
    
    ```

#### 🔧 死锁

造成死锁的原因：系统资源不足、进程推进顺序不当、资源分配不当。形成条件有：

* 互斥，一个资源每次只能被一个进程使用
* 请求和保持：一个进程因请求资源而阻塞时，对已有资源保持不放
* 不可剥夺：进程已获得的资源，使用完前不能强行剥夺
* 循环等待：若干进程形成头尾相连的循环等待资源

避免死锁：银行家算法，通过统计各进程对资源的最大需求，满足时进行分发（破坏条件-循环等待）。

造成死锁时会导致资源被锁定、系统性能下降、进程停止运行等情况。

### 🚁 线程池

Python中的线程池通常使用`concurrent.futures`模块中的`ThreadPoolExecutor`类来实现。  
线程池可以有效地管理一定数量的线程，避免频繁创建和销毁线程的开销，同时限制并发线程的数量，防止资源耗尽。

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# 目标函数
def worker(x):
    time.sleep(0.1)
    return x * x

# 创建一个线程池，指定最大线程数量
with ThreadPoolExecutor(max_workers=5) as executor:
    # 使用map方法提交任务
    results = executor.map(worker, [1, 2, 3, 4, 5])
    for result in results:
        print(result)

# 或者使用submit方法提交任务，并获取Future对象
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(worker, x) for x in [1, 2, 3, 4, 5]]
    # 使用as_completed遍历已完成的Future对象并获取结果，类似于Thread.join()
    for future in as_completed(futures):
        print(future.result())

print("Done!")

```

---

## 📌 Python多进程

```python
"""
subprocess: 调用外部函数的多进程
multiprocessing: 启动内部函数的多进程
"""
import subprocess

p = subprocess.Popen("Python -V", stdout=subprocess.PIPE)
print(p.stdout.readlines())
```

### 🚁 进程间通信

当多个进程同时调用共享资源如全局变量时，各进程会先进行一次深拷贝再执行操作，进程间不会互相影响。但进程间相互隔离，无法直接访问。

实现进程间通信的方式：管道、共享存储器系统、消息传递系统、信号量（共享内存、信号、队列）

* multiprocessing.Pipe(): 管道，初始化时传参`duplex=False`，创建单向管道，默认为双向管道
* multiprocessing.Queue(): 队列，双向通信
* multiprocessing.Manager(): 数据共享，但不加锁时进程不安全；使用必须搭配join方法进行阻塞
* multiprocessing.Value(): 定义一个多进程间可共享的变量，进程安全
* multiprocessing.Array(): 定义一个多进程间可共享的数组，进程安全

=== "管道"

    ```python
    import multiprocessing
    import time
    
    
    def send(pipe):
        str = "hello"
        for i in range(5):
            print("sender:", str)
            pipe.send(str)  # 不支持发送类的实例
            time.sleep(0.1)
    
    
    def receive(pipe):
        for i in range(5):
            print("receiver:", pipe.recv())
            time.sleep(0.1)
    
    
    if __name__ == '__main__':  # 多进程必须要在main方法执行，作为模块内一部分去执行则报错
        sender, receiver = multiprocessing.Pipe()
        
        multiprocessing.Process(target=send, args=(sender,)).start()
        multiprocessing.Process(target=receive, args=(receiver,)).start()
    
    ```

=== "队列"
    
    ```python
    import multiprocessing
    import time
    
    
    def send(queue):
        str = "hello"
        for i in range(5):
            print("sender:", str)
            queue.put(str)
            time.sleep(0.1)
    
    
    def receive(queue):
        for i in range(5):
            print("receiver:", queue.get(True, 0.1))  # 阻塞最多0.1等待队列，无内容则抛queue.Empty异常
            time.sleep(0.1)
    
    
    if __name__ == '__main__':  # 多进程必须要在main方法执行，作为模块内一部分去执行则报错
        q = multiprocessing.Queue()
    
        multiprocessing.Process(target=send, args=(q,)).start()
        multiprocessing.Process(target=receive, args=(q,)).start()
    
    ```

=== "数据共享"

    ```python
    import multiprocessing
    import time
    
    
    def process_1(shared_var: list, lock):
        for i in range(5):
            with lock:
                shared_var.pop()
                print("process_1:", shared_var)
                time.sleep(0.1)
    
    
    def process_2(shared_var: list, lock):
        for i in range(5):
            with lock:
                shared_var.pop()
                print("process_2:", shared_var)
                time.sleep(0.1)
    
    
    if __name__ == '__main__':  # 多进程必须要在main方法执行，作为模块内一部分去执行则报错
        shared_var = multiprocessing.Manager().list(range(0, 10))  # 不加锁时进程不安全
        lock = multiprocessing.RLock()
        mp1 = multiprocessing.Process(target=process_1, args=(shared_var, lock))
        mp2 = multiprocessing.Process(target=process_2, args=(shared_var, lock))
    
        mp1.start()
        mp2.start()
    
        mp2.join()  # 使用Manager时，缺少join时会报错无法运行

    ```

=== "Value与Array"
    
    ```python
    import multiprocessing
    import time
    
    
    def process_1(val, array):
        for i in range(5):
            val.value = i
            array[i] = i + 5  # Array不支持append
            print("process_1 val:", val.value)
            print("process_1 array:", array[:])
            time.sleep(0.1)
    
    
    def process_2(val, array):
        for i in range(5):
            print("process_2 val:", val.value)
            print("process_2 array:", array[:])
            time.sleep(0.1)
    
    
    if __name__ == '__main__':  # 多进程必须要在main方法执行，作为模块内一部分去执行则报错
        val = multiprocessing.Value('i', 777)
        array = multiprocessing.Array('i', [0, 1, 2, 3, 4])
    
        mp1 = multiprocessing.Process(target=process_1, args=(val, array))
        mp2 = multiprocessing.Process(target=process_2, args=(val, array))
    
        mp1.start()
        mp2.start()
        mp2.join()
    
        print(val.value)
        print(array[:])
    
    ```

### 🚁 进程池

python进程池使用`concurrent.futures`模块中的`ProcessPoolExecutor`类来实现，类方法与线程池的类似。

### 🚁 练习

```python
"""
有三个组装车间，分别组A、B、C三款产品，每款产品都有四个零件a1，a2，a3，a4。
零件生产商会与隔一秒生成三种产品的任一零件，并将零件发送至三个车间。
车间收到零件后，先判断是否是自己产品的零件，是则进行组装（动态加载setattr）；不是则存入库房自行认领。
组装完成后，输出至控制台。
"""
import multiprocessing
import random
import sys
import threading
import time

"""定义三种产品类 每个产品都有1234四个零件 零件动态加载"""
"""定义三个车间 用来组装产品"""
"""定义零件生产商 用来发送零件"""
"""要求使用两个进程来分别定义生产商和组装车间"""
"""要求使用三个线程来定义不同的组装车间"""


class Prod:
    # 父类
    pass


class Producer:
    """
    生产商进程，生产零件
    """
    parts = ["a1", "a2", "a3", "a4", "b1", "b2", "b3", "b4", "c1", "c2", "c3", "c4"]

    def __init__(self, queue):
        self.queue = queue  # 创建管道用于进程通信

    def make_part(self):
        """
        生产零件
        :return:
        """
        while self.parts:
            part = random.sample(self.parts, 1)[0]
            print(f"Producer生产零件：{part}")
            self.parts.remove(part)  # 不重复生产零件
            self.queue.put(part)
            time.sleep(1)  # 隔一秒生成
        print("生产结束")


class Workshop:
    warehouse = []  # 库房

    def __init__(self, queue):
        self.queue = queue  # 创建管道用于接收
        self.lock = None  # 在进程中不能先初始化线程锁

    def start(self):
        """要求使用三个线程来定义不同的组装车间"""
        self.lock = threading.RLock()
        t1 = threading.Thread(target=self.assemble, args=("A",))
        t2 = threading.Thread(target=self.assemble, args=("B",))
        t3 = threading.Thread(target=self.assemble, args=("C",))
        for t in [t1, t2, t3]:
            t.start()
        for t in [t1, t2, t3]:
            t.join()

    def assemble(self, name):
        """
        组装产品
        :param name: 车间名，如A
        :return:
        """
        # 根据传入参数动态生成子类
        inherit = type(name, (Prod,), {__doc__: f"产品子类{name}"})
        lpart = name.lower()
        # 当零件未齐全时执行
        while not all([hasattr(inherit, lpart + str(i)) for i in range(1, 5)]):
            with self.lock:
                try:
                    # 从管道接收零件
                    part = self.queue.get(True, 0.5)
                    print(f"车间{name}收到零件：{part}")
                except Exception:  # 未接收到零件时，从库房获取零件
                    if self.warehouse:
                        part = self.warehouse.pop()
                        print(f"车间{name}从库房收到零件：{part}")
                    else:
                        continue

                # 零件属于本车间时组装进类中
                if part.startswith(lpart):
                    print(f"{part}属于本车间产品，进行组装\n")
                    setattr(inherit, part, True)
                # 零件不属于本车间时存入库房
                else:
                    print(f"{part}不属于本车间产品，存入库房\n")
                    self.warehouse.append(part)

        # 停止循环时，即组装完成
        print("产品{}组装完毕".format(name), file=sys.stderr)
        # print([getattr(inherit, lpart + str(i)) for i in range(1, 5)])  # [True, True, True, True]


if __name__ == '__main__':
    queue = multiprocessing.Queue()
    producer = multiprocessing.Process(target=Producer(queue).make_part, args=())
    workshop = multiprocessing.Process(target=Workshop(queue).start, args=())

    producer.start()
    workshop.start()
    producer.join()
    workshop.join()

```
