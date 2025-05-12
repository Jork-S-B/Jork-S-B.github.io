## 📌 闭包

闭包：允许内部函数访问其外部函数（父函数）的局部变量，即使外部函数已退出执行，只要内部函数还被引用，这些局部变量就会继续存在。

=== "累加器闭包"

    ```python
    def counter(start=0):
        count = start
    
        def increment(step=1):
            nonlocal count  # 通过nonlocal关键字访问并修改外部函数的局部变量count
            count += step
            return count
    
        return increment
    
    # 创建一个从1开始计数的累加器闭包
    counter_1 = counter(1)
    
    # 使用闭包进行累加操作
    print(counter_1())  # 输出: 2
    print(counter_1())  # 输出: 3
    print(counter_1(2))  # 输出: 5

    ```

=== "闭包陷阱示例"

    ```python
    def create_multipliers():
        multipliers = []
    
        for i in range(5):
            def multiplier(n):
                return n * i  # 实际上所有闭包都共享同一个循环结束时的i值（此处为4）
    
            multipliers.append(multiplier)
    
        return multipliers
    
    multipliers_list = create_multipliers()
    print(multipliers_list[0](3))  # 输出: 12
    print(multipliers_list[1](3))  # 输出: 12
    
    ```

=== "解决闭包陷阱"

    ```python
    def create_fixed_multipliers():
        multipliers = []
    
        for i in range(5):
            # 改为一个立即执行的匿名函数（lambda表达式）来捕获循环变量的当前值
            multipliers.append(lambda n, factor=i: n * factor)
    
        return multipliers
    
    fixed_multipliers_list = create_fixed_multipliers()
    print(fixed_multipliers_list[0](3))  # 输出: 0
    print(fixed_multipliers_list[1](3))  # 输出: 3
    
    ```

## 📌 装饰器

装饰器本质上是一种设计模式，利用闭包的特性（还有嵌套函数）来修改原函数的行为，而无需改动原代码。

通过接收函数作为参数，对原函数包装后返回一个新的函数，这个返回的新函数就是一个闭包。

=== "装饰器示例"

    ```python
    import functools
    import tracemalloc
    
    def my_decorator(func):  # 1.接收函数func
        # Python装饰器在实现的时候，被装饰后的函数其实已经是另外一个函数了（函数名等函数属性会发生改变）
        @functools.wraps(func)
        # 为了消除上述影响，functools包中提供了一个叫wraps的decorator来消除这样的副作用
        def wrapper(*args, **kwargs):  # 2.定义内部函数，在该函数中对 func 的调用前后插入额外逻辑
            print('这里调用装饰器my_decorator')
            return func(*args, **kwargs)
        return wrapper  # 3.将wrapper函数作为返回值进行传递
    
    
    # 带参数的装饰器
    def show_memory(flag=True):
        def decorator(func):
            @functools.wraps(func)
            def inner(*args, **kwargs):
                if flag:
                    # 开启内存分配跟踪
                    tracemalloc.start()
                    ret = func(*args, **kwargs)
                    current, peak = tracemalloc.get_traced_memory()
                    print(f'当前内存使用量为 {current / 1024 / 1024}MB; 峰值为 {peak / 1024 / 1024}MB')
                    tracemalloc.stop()
                else:
                    ret = func(*args, **kwargs)
                return ret
            return inner
        return decorator
    
    
    @show_memory(flag=False)
    @my_decorator
    def example():
        print('Called example function')
    
    
    if __name__ == '__main__':
        # 没有wraps装饰器时打印：wrapper None
        print(example.__name__, example.__doc__)  # 打印：example None
        example()

    ```

=== "类装饰器"
    
    ```python
    import time
    
    class TimeProfiler:
        def __init__(self, func):
            self.func = func
        
        # 通过编写__call__方法实现类装饰器
        def __call__(self, *args, **kwargs):
            start_time = time.time()
            result = self.func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"{self.func.__name__} 运行耗时: {elapsed_time:.6f} 秒")
    
            return result
    
    @TimeProfiler
    def slow_function(n):
        time.sleep(n)
        return n * n
    
    # 调用被装饰的函数
    slow_function(2.5)  # 输出类似: "slow_function 运行耗时: 2.500000 秒"
    
    ```

## 📌 柯里化

柯里化：将接受多个参数的函数，转换成一系列接收一个参数的函数的技术，这些单参数函数最终累积所有参数并返回原函数的计算结果。

🎬 一些适用场景：

* 当函数在特定上下文中的参数固定，其他参数需要根据具体情况变化时。如`base_url`和`headers`固定，`url`和`params`不固定时。
* 当需要对一组具有相似行为，但参数数量或类型不同的函数，进行统一处理时。
* 函数组合、延迟计算
* 类型安全与约束检查

=== "使用functools.partial实现"

    ```python
    from functools import partial

    def add(a, b, c):
        return a + b + c
    
    # 使用functools.partial进行柯里化
    curried_add = partial(add, 1)  # add函数作为参数进行传递
    
    # 传入剩余参数
    result = curried_add(2, 3)
    print(result)  # 输出: 6
    ```

=== "自定义函数实现"

    ```python
    def curry(func, *args, **kwargs):
        def curried(*more_args, **more_kwargs):
            combined_args = args + more_args
            combined_kwargs = {**kwargs, **more_kwargs}
            if len(combined_args) + len(combined_kwargs) == func.__code__.co_argcount:
                return func(*combined_args, **combined_kwargs)
            else:
                return curry(func, *combined_args, **combined_kwargs)
        return curried

    def add(a, b, c):
        return a + b + c

    curried_add = curry(add, 1)
    
    # 传入剩余参数
    result = curried_add(2, 3)
    print(result)  # 输出: 6
    ```