
## 📌 自定义测试套件
```python
suite.addTest(case)  # 单个用例加载到套件
suite.addTest(loader.loadTestsFromTestCase(TestCaseDemo))  # 用例类加载到套件
suite.addTest(loader.loadTestsFromModule(testcase))  # 用例模块(.py)加载到套件
suite.addTest(loader.discover(case_path, pattern='testcase*.py'))  # 指定路径加载，默认加载该路径下所有test开头的用例
```

## 📌 断言

`assertEqual`  # 比较的是两个对象的内容

`assertIs`  # 比较的是两个对象的指向地址

`assertTrue`  # 断言是否为True


## 📌 unittest.main()

`unittest.main(verbosity=2)`

`verbosity`参数表示输出的详细程度：

0-不输出；

1-输出每个用例执行结果；

2-输出每个用例执行结果、详细的错误信息及执行时间等

---

参考资料：

[unittest-单元测试框架](https://docs.python.org/zh-cn/3/library/unittest.html)

[unittest最详细的解说](https://www.cnblogs.com/daxiong2014/p/10449184.html)
