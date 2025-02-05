
```python
'''
-s 输出打印信息到控制台，关闭捕捉
-v 显示具体的用例执行的详细信息
-q 简化输出信息
--reruns=1 失败用例重跑，次数为1
--alluredir=file_dir 指定报告的数据源文件目录路径，需要安装allure-pytest
--clean-alluredir 清掉allure报告中的用例执行记录
'''

today = datetime.datetime.now().strftime('%Y%m%d')
data_dir = os.path.join(REPORT_PATH, today, 'data')
report_dir = os.path.join(REPORT_PATH, today, 'report')
    
# 方式1，运行全部用例
run_info = ['-v', '-s', '-q', '--reruns=1', '--alluredir', data_dir]
# 方式2，运行上次失败的用例
run_info = ['--lf', '-s', '-q', '--reruns=1', '--alluredir', data_dir]

# 方式3，运行指定模块
run_info = ['-vs', 'testCompare.py', '--alluredir', data_dir]
# 方式4，运行指定目录
run_info = ['-vs', './testcase', '--alluredir', data_dir]
# 方式5，运行指定方法
run_info = ['-vs', './testcase/testCompare.py::TestMyCompare::test_01_regex', '--alluredir', data_dir]

# -m 通过标记来执行
# 方式6，运行带指定标签的用例，搭配`@pytest.mark.标签名`，并且在pytest.ini注册标签以启用
run_info = ['-m', 'smoke or level0', '-s', '-q', '--alluredir', data_dir]
# '-m', 'smoke not level0'，表示带smoke但非level0标签

pytest.main(run_info)

# 生成allure报告的数据源文件，json格式；--clean是每次清空
# 格式：allure generate {数据源文件目录} -o {报告的目录}
os.system(f'allure generate {data_dir} -o {report_dir} --clean')
# 本地运行
os.system(f'allure open -h {ip} -p {port} {report_dir}')

```

!!! note "补充"

    * 放测试用例的目录应当为Python Package，而非Directory。
    * pytest搜索规则/用例命名规则: 

    1.文件名如`test_*.py`或`*_test.py`，注意有下划线。

    2.文件中的类以Test开头。

    3.文件中的方法名以test_开头。

---

参考资料：

[pytest-标记用例](https://www.cnblogs.com/lfr0123/p/15907200.html)

[pytest+allure详解](https://www.cnblogs.com/Neeo/articles/11832655.html#allure)

