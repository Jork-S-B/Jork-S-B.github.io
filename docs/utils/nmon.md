安装与运行忽略

## 📌 收集并生成nmon报告

nmon -s 20 -c 3 -f -m /usr/local/nmon_output

* -s 20: 每20秒采集一次数据
* -c 3: 采集3次，即总共采集1分钟
* -f: 生成报告文件名中包含文件创建的时间，如"{主机名}_161127_2159.nmon"
* -m: 输出报告文件存放路径

## 📌 分析nmon报告

`NMON Visualizer`加载生成的nmon文件

或者`xlsm+宏`打开nmon文件