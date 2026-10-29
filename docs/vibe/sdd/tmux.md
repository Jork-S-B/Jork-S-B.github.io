tmux, 开源终端管理器，多窗口展示agent会话。

在云服务器环境下，SSH 断开时 tmux 客户端会退出，但服务器和它下面的所有子进程会继续运行，实现会话持久。

!!! note "tmux和docker"

    - tmux 解决的核心问题是*连接持久化*和*终端复用*，让你断开 SSH 后工作不丢失。
    - Docker 解决的核心问题是*环境隔离*和*一致性*，让应用在受控的沙箱中运行。

两者都是宿主机的普通进程，核心区别是隔离级别（docker隔离级别更高）。

---

tmux 默认前缀键：`Ctrl+b`，下面写作 `Prefix`。

最常用组合：`tmux new -s work` → `Prefix d` 分离 → `tmux a -t work` 恢复。

初始的tmux需要配置`set -s escape-time 0`并重启，否则ESC可能无响应。

## 会话管理

```bash
tmux new -s 名称          # 新建并命名会话
tmux ls                   # 列出会话
tmux attach -t 名称       # 进入指定会话
tmux a -t 名称            # attach 简写
tmux detach               # 分离当前会话，或在 tmux 内按 Prefix d
tmux kill-session -t 名称 # 关闭指定会话
tmux kill-server          # 关闭所有 tmux 会话，重启服务以更新配置
tmux rename-session 新名  # 重命名当前会话
```

## 窗口 window

```bash
Prefix c        # 新建窗口
Prefix ,        # 重命名当前窗口
Prefix w        # 列出窗口并切换
Prefix n        # 下一个窗口
Prefix p        # 上一个窗口
Prefix 0-9      # 切换到指定编号窗口
Prefix &        # 关闭当前窗口
Prefix l        # 切换到上一个窗口
```

## 窗格 pane

```bash
Prefix %        # 左右分屏
Prefix "        # 上下分屏
Prefix 方向键   # 切换窗格
Prefix o        # 切换到下一个窗格
Prefix x        # 关闭当前窗格
Prefix z        # 当前窗格全屏/还原
Prefix {        # 当前窗格与前一个窗格交换位置
Prefix }        # 当前窗格与后一个窗格交换位置
Prefix Ctrl+方向键  # 调整窗格大小
```

## 复制与查看

```bash
Prefix [        # 进入复制模式，可用方向键/PageUp/PageDown 翻页
Prefix ]        # 粘贴复制内容
Prefix ?        # 查看所有快捷键
Prefix :        # 进入 tmux 命令模式
Prefix t        # 显示时钟
```

## 配置与常用命令行

```bash
tmux source-file ~/.tmux.conf   # 重载配置
tmux new-window                 # 新建窗口
tmux split-window -h            # 左右分屏
tmux split-window -v            # 上下分屏
tmux list-sessions              # 同 tmux ls
tmux list-windows               # 列出窗口
tmux list-panes                 # 列出窗格
```
