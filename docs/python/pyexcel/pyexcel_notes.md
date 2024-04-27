## 📌 openpyxl==3.0.10

* 仅支持xlsx文件，读写xls文件可使用`xlwings`或`pandas`等库。
* 读取带筛选的excel文件报错：`Value must be either numerical or a string containing a wildcard`；降级为`openpyxl==3.0.10`即可。
* 保存excel文件，打开报错问题：`发现“xx.xlsx”中的部分内容有问题。是否让我们尽量尝试恢复？...`；降级为`openpyxl==3.0.10`即可。

---

参考资料：[Python操作Excel库总结](https://zhuanlan.zhihu.com/p/353669230)
