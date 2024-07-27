
git操作前先配置ssh公钥

## 📌 常用命令

```shell
# 设置提交人和邮箱信息  
git config --global user.name "Jork_S_B"  
git config --global user.email "Jork_S_B@163.com"

# 添加所有修改到暂存区  
git add --all

# 查看状态  
git status

# 提交，-m设置注释  
git commit -m "test"

# 将本地的master分支推送到远程仓库origin中，并-u设置为默认跟踪分支  
git push -u origin master

# 从远程仓库同步代码  
git -C ./dir pull | tee -a | grep -i -E "xx|xxx"
```

## 📌 github token

快速生成token：https://github.com/settings/tokens/new


### 🚁 误push时，删掉某些文件的提交记录

执行前先备份，会删掉对应文件。另外删不掉gitee动态🙂。

方式一（推荐）：https://cloud.tencent.com/developer/article/1665810

方式二：

```shell
# 切换到自己的本地分支  
git check master

# 查看历史提交记录  
git log
 
# 回退到之前指定版本  
git reset --hard 29b4ebb37aad1f57039428806875f6b5e672eee5

# 执行git push origin+要push的远程分支名 --force，强制提交本地代码到远程分支  
git push origin master --force
 
# 同步本地与远程分支  
git pull
```