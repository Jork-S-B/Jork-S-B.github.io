单元测试框架，类似于Junit。

* TestCase: 测试用例
* TestSuite: 测试套件，用来加载用例并控制执行顺序。可通过多个TestSuite对象来做并行执行。
* TestLoader: 用例加载器
* TestRunner: 执行用例和套件，并返回执行结果；默认是`TextTestRunner`，可自定义如`HTMLTestRunner`生成HTML格式的报告
* TestResult: 测试结果

## 📌 测试套件

使用测试套件时，通过代码顺序控制用例加载顺序，而不是根据ASCII码顺序。

=== "通过TestCase实例回调执行用例" 
    
    ```python
    if __name__ == '__main__':
        case = MyClass("test_xx_01")  # 假设MyClass继承自unittest.TestCase
        result = MyResult()  # 假设MyResult继承自unittest.TestResult
        case(result)
    ```

=== "通过addTest加载测试用例"
    
    ```python
    import unittest
    from pathlib import Path
    
    if __name__ == '__main__':
        path = Path(".").resolve().as_posix()  # 当前路径的绝对路径
        suite = unittest.TestSuite()
        loader = unittest.TestLoader()
        # suite.addTest(testcase_01)  # 加载单个用例
        # unittest执行时，实际上会将用例方法名作为TestCase构造方法传参进行实例化
        # suite.addTest(MyClass("xxx_01"))  # 同上，也是加载单个用例
        
        # suite.addTest(loader.loadTestsFromTestCase(TestCaseDemo))  # 加载用例类
        # suite.addTests(unittest.makeSuite(MyClass))  # 同上，也是加载用例类
        
        # suite.addTest(loader.loadTestsFromModule(testcase))  # 加载用例模块(.py)
        
        suite.addTest(loader.discover(path, pattern="test*.py"))  # 加载用例目录
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
        """
        `verbosity`参数表示输出的详细程度：
        0-不输出；
        1-输出每个用例执行结果，默认值；
        2-输出每个用例执行结果、详细的错误信息及执行时间等
        """
    ```

## 📌 unittest.main()

unittest.main(defaultTest="MyClass.xxx_01", verbosity=2)  
执行本模块MyClass类的xxx_01方法

## 📌 跳过用例

* `@unittest.skip`
* `@unittest.skipIf`
* `@unittest.skipUnless`

## 📌 数据驱动

用例有多种测试场景/数据需要执行时使用

TODO

## 📌 断言

`assertEqual`  
比较的是两个对象的内容

`assertIs`  
比较的是两个对象的指向地址

`assertTrue`  
断言是否为True

---

参考资料：

1.[unittest-单元测试框架](https://docs.python.org/zh-cn/3/library/unittest.html)

2.[unittest最详细的解说](https://www.cnblogs.com/daxiong2014/p/10449184.html)
