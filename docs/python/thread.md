## 📌 进程&线程&协程

程序运行时，系统会为每个进程分配不同的内存空间；而对线程而言，除了CPU，系统不会为线程分配内存，线程之间只能共享资源。

* 线程：CPU执行的最小单元，多线程无需申请资源，子线程和父线程共享资源，通信快于进程通信。

* 进程：操作系统执行的基本单元，由系统分配资源和调度。

* 协程：微线程，只有一个线程执行，当子程序内部阻塞或者I/O等待时，在多个方法间切换执行。相比多线程，省去线程切换的开销，共享资源不需加锁，执行效率更高。


## 📌 并行与并发

* 并行：同一时刻，有多条指令在多个处理器上同时执行。

* 并发：同一时刻只能有一条指令执行，但多个进程指令被快速的轮换执行，使得在宏观上具有多个进程同时执行的效果。

## 📌 Python多线程

### 🚁 全局解释器锁GIL

Python的多线程，由于全局解释器锁GIL的存在，实际上同一时刻只有一个线程在进行，并非真正的并行，但它仍可以提高程序效率。

在多线程程序中，当一个线程阻塞时，其他线程可继续执行，以提高程序的并发性和响应性。

!!! note "总结"

    * 对于I/O密集型任务和高并发场景，建议使用协程。
    * 对于CPU密集型任务/计算密集型，建议使用进程。
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
    Lock: 原始锁，可以由任意线程解锁，不能重复上锁
    RLock: 重入锁，只能由锁定线程解锁，可以重复上锁，但也要重复解锁
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

### 🚁 进程间通信

方式有：管道、共享存储器系统、消息传递系统、信号量（共享内存、信号、队列）