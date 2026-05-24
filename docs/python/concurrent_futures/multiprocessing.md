```python
"""
subprocess: 调用外部函数的多进程
multiprocessing: 启动内部函数的多进程
"""
import subprocess

p = subprocess.Popen("Python -V", stdout=subprocess.PIPE)
print(p.stdout.readlines())
```

## 📌 进程间通信

当多个进程同时调用共享资源如全局变量时，各进程会先进行一次深拷贝再执行操作，进程间不会互相影响。但进程间相互隔离，无法直接访问。

实现进程间通信的方式: 管道、共享存储器系统、消息传递系统、信号量（共享内存、信号、队列）

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

## 📌 进程池

python进程池使用`concurrent.futures`模块中的`ProcessPoolExecutor`类来实现，类方法与线程池的类似。