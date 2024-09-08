年月日时分秒  
`date +%Y%m%d%H%M%S`

## 检查命令耗时

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

## 执行SQL，记录并检查日志

=== "execsql.sh"
    
    ```shell
    #!/bin/bash
    
    getDbstr(){
        db="$1"
        case ${db} in
            db2) dbstr=user/pw@ip:port/db2 ;;
            db3) dbstr=user/pw@ip:port/db3 ;;
            *) echo "-->【`date "+%Y%m%d%H%M%S"`】ERROR:db=\"${db}\",数据库输入错误，请检查后重新输入"
            getHelp
            exit ;;
        esac
    }
    
    getHelp(){
        echo "参数说明："
        echo "------------------------------------------------------"
        echo "-f，指定sql脚本执行，多个脚本用逗号分隔"
        echo "-k，通过输入的关键字，匹配脚本名称并执行，不区分大小写"
        echo "-d，选择数据库连接串，默认为db1"
        echo "-f与-k选择一个执行即可，无参数时不执行"
        echo "------------------------------------------------------"
        echo "命令样例：-k roll -d db2"
    }
    
    dbstr=user/pw@ip:port/db1
    
    # 遍历参数校验
    while getopts ":f:d:k" params
    do
        case $params in
            f) filelist=$OPTARG ;;
            d) getDbstr $OPTARG ;;
            k) keyword=$OPTARG ;;
            *) echo "-->【`date "+%Y%m%d%H%M%S"`】ERROR:未知参数[-$OPTARG]，请检查后重新输入"
            getHelp
            exit 1 ;;
        esac
    done
    
    if [ "${filelist}" ]&&[ "${keyword}" ];then
        echo "-->【`date "+%Y%m%d%H%M%S"`】ERROR:-f与-k选择一个执行即可，请检查后重新输入"
        getHelp
        exit 1
    elfi [ "${filelist}" ];then
        file=`echo ${filelist} | tr "," " "`
    elfi [ "${keyword}" ];then
        keyword1 = `echo ${keyword} | tr "a-z" "A-Z"`
        keyword2 = `echo ${keyword} | tr "A-Z" "a-z"`
        file=`ls *${keyword1}*.sql *${keyword2}*.sql 2>/dev/null`
    fi
    
    # 遍历执行并记录日志
    log_path=./log/`date +%Y%m%d%H%M%S`
    mkdir -p ${log_path}
    for filename in $file
    do
        logname=`echo ${filename} | awk -F "." '{print $1}'`
        sqlplus ${dbstr} << ! > ${log_path}/${logname}.log
        @${filename}
        commit;
        exit;
    !
    done
    
    # 检查sql是否不规范或者日志是否报错
    spec=`grep -i -B 5 'if not exists' *.sql`
    cd ${log_path}
    error=`grep -i -E -B 5 'ORA-|SP2-' *`
    
    if [ ! "${error}" ]&&[ ! "${spec}" ];then
        echo "执行完毕，无报错。"
    else
        echo "执行完毕，报错信息如下，详情请查看日志："
        echo "${spec}"|tee -a error.log  # "${spec}",去掉双引号也可以
        echo "${error}"|tee -a error.log
    fi
    ```

---