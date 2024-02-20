```python
# 生成allure报告的数据源文件，json格式；--clean是每次清空
# 格式：allure generate {数据源文件目录} -o {报告的目录}
os.system(f'allure generate {data_dir} -o {report_dir} --clean')
# 本地运行
os.system(f'allure open -h {ip} -p {port} {allure_report}')
```

[参考的这一篇博客](https://www.cnblogs.com/yxm-yxwz/p/16638703.html)

---
最后更新: 2024/02/07 21:25