
```python
'''
-s 输出打印信息到控制台，关闭捕捉
-v 显示具体的用例执行的详细信息
-q 简化输出信息
--reruns=1 失败用例重跑，次数为1
--alluredir=file_dir 指定报告的数据源文件目录路径
'''

# 方式1，运行全部用例
run_info = ['-v', '-s', '-q', '--reruns', 1, '--alluredir', file_dir]
# 方式2，运行上次失败的用例
run_info = ['--lf', '-s', '-q', '--reruns', 1, '--alluredir', file_dir]

# 方式3，运行指定模块
run_info = ['-vs', 'testCompare.py', '--alluredir', file_dir]
# 方式4，运行指定目录
run_info = ['-vs', './testcase', '--alluredir', file_dir]
# 方式5，运行指定方法
run_info = ['-vs', './testcase/testCompare.py::TestMyCompare::test_01_regex', '--alluredir', file_dir]

# -m 通过标记来执行
# 方式6，运行带指定标签的用例，搭配`@pytest.mark.标签名`使用
run_info = ['-m', 'smoke or level0', '-s', '-q', '--alluredir', file_dir]
# '-m', 'smoke not level0'，表示带smoke但非level0标签

pytest.main(run_info)
```

[参考的这一篇博客](https://www.cnblogs.com/lfr0123/p/15907200.html)

---
