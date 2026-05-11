## windows 安装 npm

### 使用 nvm-windows（多版本管理）

1. 卸载已有的 node.js ，避免冲突
2. 下载并安装 [nvm-windows](https://github.com/coreybutler/nvm-windows/releases) 最新的安装包
3. 以管理员身份打开 PowerShell，查看可用版本： `nvm list available` 
4. 安装最新的 LTS 版本，如： `nvm install 22.13.1`
5. 切换到最新安装的版本： `nvm use 22.13.1`
6. 验证安装： `node -v`

## pnpm 

pnpm 是一个快速、节省磁盘空间的包管理器。在 windows 环境下有多种安装方式。

### 通过 npm 安装 

管理员身份打开 PowerShell 并执行：`npm install -g pnpm`

### 使用独立安装脚本

管理员身份打开 PowerShell 并执行，脚本会自动下载 pnpm 并添加到用户 PATH。

```powershell
# 设置允许执行远程脚本
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
# 运行安装脚本
iwr https://get.pnpm.io/install.ps1 -useb | iex

```