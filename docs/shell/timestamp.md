
```shell
#!/bin/bash
startTime=`date +%s`
sleep 5
#do something here
endTime=`date +%s`
sumTime=$(( $endTime - $startTime ))
echo "Total run $sumTime seconds"

# 或者用time命令
time sh xxx.sh 
time ls -lrt
# 返回3个时间数据：
# real 该命令的总耗时, 包括user和sys及io等待, 时间片切换等待等等
# user 该命令在用户模式下的CPU耗时,也就是内核外的CPU耗时,不含IO等待这些时间
# sys  该命令在内核中的CPU耗时,不含IO,时间片切换耗时.
```


---