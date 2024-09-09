## 📌 重定向

|           命令           | 说明                           |
|:----------------------:|:-----------------------------|
| echo '新建文件' > new.txt  | 输出重定向，覆盖文件内容                 |
| echo '追加文本' >> new.txt | 输出重定向，但不覆盖文件内容，追加文本          |
|  cat << EOF > new.txt  | 输入内容直至EOF(Ctrl + D)时结束，并保存文件 |

## 📌 文件权限

-rwxr-xr-x

* 第一个字符：代表文件类型。- 表示普通文件，d 表示目录，l 表示符号链接等。
* 接下来的三组rwx：分别代表所有者（owner）、用户组（group）和其他用户（others）的权限。

读（r=4），写（w=2），执行（x=1）。

所以，`chmod 755`表示设置权限为：

1. 文件所有者可读可写可执行；
2. 与文件所有者同属一个用户组的其他用户可读可执行；
3. 其它用户组可读可执行。

## 📌 系统相关

|       命令        | 说明                           |
|:---------------:|:-----------------------------|
|    free -h	     | 查看内存，-h 以易读方式显示文件大小          |
|     df -h	      | 查看文件系统级别的磁盘占用                |
|   du -d 1 -h	   | 查看当前目录使用空间                   |
|    lsof -n	     | 查看端口占用，-n作用是禁止域名转换，即不进行DNS解析 |
| telnet ip port	 | 相当于ping ip，`ctrl+[`退出        |
|  kill -9 pid	   | 强制杀进程                        |
|   top -u user   | top实时监控系统性能，-u指定用户启动的进程      |
|   top -p pid    | -u -p不能一起用                   |
|     ps -aux     | 比`ps -ef`多打印内存、CPU使用率等指标     |

## 📌 文件类型

* \- 普通文件（文本文件、二进制文件、压缩文件、电影、图片等）
* d 目录文件
* b 设备文件（块设备）：存储设备硬盘、U盘/dev/sda、/dev/sda1
* c 设备文件（字符设备）：打印机、终端/dev/tty
* l 链接文件，软连接
* s 套接字文件
* p 管道文件

### 🚁 软链接

建软链接，/home/whm是实际地址，./whm相当于快捷方式  
ln -s /home/whm ./whm

### 🚁 排序

将排序后的结果保存为新文件  
其他参数：-u去重；-n按数字排序；-r倒序；-k按指定列排序；-o 在原件排序  
sort -u xxx.txt | sort > new.txt

### 🚁 统计

统计字符数、单词数、行数  
wc file

统计行数  
wc -l file

### 🚁 显示行号

显示行号，-ba表示空白行也加行号  
nl -ba xxx.txt > new.txt

### 🚁 文件拼接

按列拼接，分隔符为','  
paste -d ',' xxx.txt new.txt

### 🚁 比较

|  命令  | 说明             |
|:----:|:---------------|
| cmp  | 比较两个文件内容是否相同   |
| diff | 	比较两个文件内容是否有差异 |
| comm | 比较两个已排序文件的内容差异 |

## 📌 加解压

|             命令             | 说明                               |
|:--------------------------:|:---------------------------------|
|      gzip -8 xxx.txt       | gzip方式压缩，压缩级别为8                  |
|       gzip -d xx.gz        | 	gz解压                            |
|  tar -zcvf xx.tar.gz ./*   | 当前路径下的文件压缩至xx.tar.gz             |
|    tar -zxvf xx.tar.gz     | tar解压                            |
|     zip -r xx.zip ./*      | 当前路径下的文件压缩至xx.zip                |
|   unzip -o -j ${jarname}   | 解压jar包，-o overrize，-d解压时创建一个新的目录 |
| jar xvf ${jarname} xxx.txt | 仅解压jar包的xxx.txt                  |
|       compress file        | 压缩为.Z文件，解压用`uncompress`          |

## 📌 base64

解码则是使用`base64 -d`  
echo ‘Hello World!’ | base64

## 📌 vi/vim

|      命令       | 说明                  |
|:-------------:|:--------------------|
|   u/ctrl+r    | 撤销/取消撤销             |
| ctrl+f/ctrl+b | PageDown/PageUp     |
|      w/b      | 下一单词/上一单词           |
|       e       | 词尾，与w类似             |
|      f/F      | 行内搜索                |
|      2dd      | dd删除一行，2dd则删除2行     |
|  :set number  | 显示行号                |
| :%s/xxx/whm/g | 查找xxx并替换为whm，与sed类似 |

!!! note "补充"

    s-switch，表示替换；g-global，表示整个文档；`/`-分隔符，可以改用其他符号如`#`。

## 📌 查找和替换

### 🚁 grep

|                命令                 | 说明                           |
|:---------------------------------:|:-----------------------------|
|        grep -v '\--' *.sql        | 	-v排除关键字，不显示--开头的行           |
| grep -n -i 'exception' -B 5 *.log | -B前5行，-n打印行数，搭配more -行数定位至行数 |
|    grep -P '${regex}' file.txt    | -P匹配正则表达式，-o只输出匹配内容          |

### 🚁 sed

|                     命令                     | 说明                         |
|:------------------------------------------:|:---------------------------|
| sed -i 's#http://ns1#https://ns1#/g' *.txt | 	使用#作为分隔符，将文本里http替换为https |
|            sed -n 10p file.txt             | 输出文件第10行                   |
|       sed -r '${regex}' -n file.txt        | -r匹配正则表达式，-n只输出匹配内容        |

### 🚁 find

在当前目录及子目录，找内容包含关键字的文件  
find ./ -name '*.log' | xargs grep -i 'keyword'

找到前1天有修改过的文件并复制  
find ./ -type f -mtime -1 -exec cp {} ./tmp/ \;

### 🚁 tr

打印的内容转为大写  
cat file.txt | tr 'a-z' 'A-Z'

删除文件内的“Snail”字符并另存为new.txt  
cat file.txt | tr -d "Snail" > new.txt

其他参数

* -c 反选
* -s 缩减连续重复的字符成指定的单个字符
* -t 削减长度

### 🚁 cut

截取指定字符并输出；—complement：取反操作  
echo A-B-xxx-xx | cut -d '-' -f 1-2 # 打印A-B

### 🚁 awk

默认分割符为空格，通过-F或者`OFS/FS='|'`来指定分割符

列出修改时间为11月9号的文件  
ls -lrt | grep -i "11月 9" | awk '{print $NF}'

同理，统计修改时间为11月9号的文件数量  
ls -lrt | grep -i "11月 9" | wc -l

|           命令            | 说明                                 |
|:-----------------------:|:-----------------------------------|
|    awk '{print $NF}'    | 	$NF代表该记录字段数目，即最后一列；$(NF-1)则是倒数第二列 |
|    awk '{print $NR}'    | $NR代表已读取的记录数，即行号，从1开始              |
|       awk '{$n}'        | 当前记录的第n个字段；$0代表完整的记录               |
| awk 'NR == 10' file.txt | 打印文件第10行                           |

## 📌 shell基础

* $0-脚本名称；$1-第一个传参，$2-第二个传参；$#-脚本传参个数
* $@-所有传参，空格分隔；$*-所有传参组成的字符串，空格分隔
* `$var`跟`${var}`基本等价，但后者比较安全。
* `if [ ! -d ./xxx ];then`，用于判断目录是否存在

=== "killCpu.sh"

    ```shell
    #!/bin/bash
    if [ $# != 1 ] ; then
      echo "USAGE: $0 <CPUs>"
      exit 1;
    fi
    for i in `seq $1`
    do
      echo -ne " 
    i=0; 
    while true
    do
    i=i+1; 
    done" | /bin/sh &
      pid_array[$i]=$! ;
    done
     
    for i in "${pid_array[@]}"; do
      echo 'kill ' $i ';';
    done
    
    # 运行：bash killCpu.sh {线程数}
    # 新增线程，通过死循环逐渐增加占用率到100%；运行会打印线程pid，kill -9 pid退出。
    ```

=== "slice.sh"

    ```shell
    # 字符串切片
    str=/home/123456.txt
    echo ${str: (-1)}  # 打印字符串最后1位，这里必须带括号
    echo ${str%?}  # 去掉字符串最后1位的结果
    echo ${str%??}  # 去掉字符串最后2位的结果
    echo ${str%\.*}  # 去掉字符串最后的'.'及后面的部分，即提取文件名
    echo ${str##*/}  # 去掉最后一个斜杠及前面的部分，即提取文件名+后缀
    
    # 出现错误时追加到日志文件
    # 1表示标准输出，2表示标准错误输出，2>&1表示将标准错误输出重定向标准输出，只打印错误日志；&表示“等同于”的意思
    echo ${str: -1} 2>&1 | tee -a error.log
    
    # 将命令的标准输出及标准错误都删除
    # /dev/null特殊的设备文件，该文件接收到的任何数据都会丢弃
    echo ${str: -1} > /dev/null 2>&1
    # 或者
    echo ${str: -1} &> /dev/null 
    
    ```

=== "update.sh"

    ```shell
    #!/bin/bash
    
    password=pw
    srcPath="编译后的文件路径"
    
    # 假如该文件路径为/xx/svr/update.sh
    cd $(dirname $0)  # dirname指令返回上一级菜单绝对路径；$0则是本文件，即dirname update.sh，结果为/xx/svr
    
    # 拉取最新代码包
    up_program(){
        /usr/bin/expect <<-EOF
        # spawn，在linux系统中创建新进程的过程，是linux进程管理的基础。
        spawn scp username@xx.com:${srcPath}/$1.jar ./
        set timeout 30
        expect "Password"
        set timeout 30
        send ${password}
        set timeout 30
        send "exit\r"  # \r回车 \b退格
        expect eof
    EOF
    }
    
    up_program $(basename $(pwd))  # basename只打印文件名，不包括后缀；$()是命令替换，即basename /xx/svr，结果为svr
    
    ```

=== "sqlcheck.sh"

    ```shell
    #!/bin/bash
    stty erase ^h	# 设置read命令时可使用退格删除字符
    read -n 10 -p "please enter version:" branch_path	# -p打印文本提示，-n限制输入字符数为10
    # branch_path=20240909

    # 检查sql文件最后一行是否缺少分号
    i=0
    while read sqlfile
    do
        # 获取文件最后一行
        nr_file=`awk '{if(!NF || /^#/){next}}1' "${sqlfile}"|grep -i -v -E "^set|^--|^\/\*"|sed '/^\r/d'|tail -1|sed 's/[[:space:]]*$//' `
    
        if [ "${nr_file:(-1)}" != ";" ];then
        # "${nr_file:(-1)}"截取最后一位
            error_result[i]="${sqlfile}"
            let i++
        fi
    done <<< "$(find . -regex "${branch_path}" |xargs -i find {} -type f -name "*DML.sql")"
    # 特殊语法，表示"Here String"，是将一个字符串作为标准输入传递给一个命令。在此是将find命令的输出作为字符串传递给一个while循环。以便对每个文件执行操作。
    
    OIDIFS=${IFS}
    IES=$'\n'
    if [ "${error_result[*]}" != "" ];then
    echo "以下文件最后一行缺少分号，请补充" >> result.txt
        for error_result in "${error_result[*]}"
        do
        echo "${error_result}" >> result.txt
        done
    fi
    
    ```

=== "get_versioninfo.sh"

    ```shell
    #!/bin/bash
    if[ $# = 0 ]; then
        echo "please input jarname"
        exit
    else
        keyword=$1
    fi
    namespace="namespace"
    nodes=`kubectl get pod -n ${namespace} | grep -i "${keyword}" | awk '{print $1}'| sort`
    
    for node in ${nodes}
    do
    # 判断是否为war包
    if [[ "${node}" == *war* ]] ; then
        war_name=`echo ${node} | cut -d '-' -f 1`
        echo "${node}:"
        kubectl -n ${namespace} exec -it ${node} -- cat /${war_name}/versionInfo.txt
    elif [[ "${node}" != *controller* ]] ; then
      # sed 's/\\r//g'` 删掉回车符
        jarpath=`kubectl exec -it ${node} -n ${namespace} -- find ./ -name "*.jar" | sed 's/\\r//g'`
        for jarpath in ${jarpath}
        do
            jarname=`echo "${jarpath##*/}"| sed 's/\\r//g'`
            echo "${node}:"
            # 解压后打印版本信息
            kubectl exec -it ${node} -n ${namespace} -- jar xvf ${jarname} VersionInfo.txt
            kubectl exec -it ${node} -n ${namespace} -- cat VersionInfo.txt
        done
    fi
    done
    ```

=== "get_versioninfo_csv.sh"

    ```shell
    #!/bin/bash
    namespace="namespace"
    nodes=`kubectl get pod -n ${namespace} | grep 'svr' |awk '{if(NR>1) print $1}'| sort`
    warnode=`kubectl get pod -n ${namespace} | grep -v -E 'svr|controller' |awk '{if(NR>1) print $1}'| sort`
    
    # 先获取jar包的信息
    alnode=''
    echo "jarname","date","branch","md5" >VersionInfo.csv
    for node in ${nodes}
    do
        if [[ "${node}" != *controller* ]] && [[ "${node}" != *war* ]] ;then
          # 避免重复写入
            if [ "${node%-*}" != "${alnode}" ];then
                # 获取容器内iar包的路径
                jarpath=`kubectl exec -it ${node} -n ${namespace} -- find ./ -name "* jar" | sed 's/\\r//g'`
                jarname=`echo "${jarpath##*/}"| sed 's/\\r//g'`
    
          # 解压jar包获取各字段信息，并写入CSV
                kubectl exec -it ${node} -n ${namespace} -- jar xvf ${jarname} VersionInfo.txt
                Compiledate=`kubectl exec -it ${node} -n ${namespace} -- cat VersionInfo.txt | grep DATE | awk -F "DATE: " '{print $2}' | sed 's/\\r//g'`
                BRANCH=`kubectl exec -it ${node} -n ${namespace} -- cat VersionInfo.txt | grep BRANCH | awk -F "BRANCH: " '{print $2}' | sed 's/\\r//g'`
                MD5=`kubectl exec -it ${node} -n ${namespace} -- md5sum ${jarname} | awk '{print $1}' | sed 's/\\r//g'`
    
                echo "${jarname}","${Compiledate}","${BRANCH}","${MD5}" >>VersionInfo.csv
                alnode="${node%-*}"
            fi
        fi
    done
    
    # 在取war包的信息
    alnode=''
    for node in ${war_node}
    do
    if [ "${node%-*}" != "${alnode}" ];then
        war_name=`echo ${node} | cut -d '-' -f 1`
    
        Compiledate=`kubectl -n ${namespace} exec -it ${node} -- cat /${war_name}/VersionInfo.txt | grep DATE | awk -F "DATE: " '{print $2}' | sed 's/\\r//g'`
        BRANCH=`kubectl -n ${namespace} exec -it ${node} -- cat /${war_name}/VersionInfo.txt | grep BRANCH | awk -F "BRANCH: " '{print $2}' | sed 's/\\r//g'`
    
        echo "${war_name}","${Compiledate}","${BRANCH}" >>VersionInfo.csv
        alnode="${node%-*}"
    fi
    done
    ```

---

