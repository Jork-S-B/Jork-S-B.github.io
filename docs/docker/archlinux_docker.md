
参考：[steamdeck docker 安装](https://www.jianshu.com/p/6fd003295994)

## 📌 签名未受信任

pacman安装时出现报错：

> `error: glibc: signature from "GitLab CI Package Builder <ci-package-builder-1@steamos.cloud>" is unknown trust`

解决方案：

```shell
# 重置密钥
pacman-key --init
pacman-key --populate

```
