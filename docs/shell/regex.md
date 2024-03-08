
```shell
# shell脚本匹配正则表达式，除了shell的正则表达式判定，还有awk、sed、grep
# grep -P '${regex}' file.txt  # -P匹配正则表达式，-o只输出匹配内容
# sed -r '${regex}' -n file.txt  # -r匹配正则表达式，-n只输出匹配内容

newip='192.168.1.100'
regex='^(\d{1,3}.){3}\d{1,3}$'
if [[ "$newip" =~ $regex ]];then
  echo "正则匹配ip地址"
fi

```

---