## Windows 10

=== "关闭window自更新.bat"

    ```
    @rem 声明采用UTF-8编码
    chcp 65001

    @rem 授权，终止服务
    sc config wuauserv start= disabled
    sc stop wuauserv

    @rem /q安静模式，不要求确认
    rd /s /q C:\Users\q7299\AppData\Local\Temp
    rd /s /q C:\Users\q7299\AppData\Local\Netease\CloudMusic\Temp
    rd /s /q C:\Users\q7299\AppData\Local\NVIDIA\DXCache
    rd /s /q C:\Users\q7299\AppData\Local\NVIDIA\GLCache

    @rem pause运行后停留窗口
    @rem pause 
    ```

=== "开启window自更新.bat"

    ```
    # window商店需要开启自动更新才能使用
    @rem 声明采用UTF-8编码
    @rem chcp 65001

    @rem 授权，启动服务
    sc config wuauserv start= auto
    sc start wuauserv
    net start wuauserv
    pause
    ```

## Windows 11

ps1 + taskschd.msc

定时计划配置: 

1. 修改ps脚本执行策略，从网络或本地自建的ps脚本默认无法运行，因此需修改策略。

    ```PowerShell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```

2. taskschd.msc 打开任务计划程序，创建任务。

    - 设置触发器: 用户登录时触发/启动时触发
    - 设置操作: `powershell.exe -ExecutionPolicy Bypass -File "C:\你的路径\DisableUpdates.ps1"`
    - -ExecutionPolicy Bypass，相当于sudo

=== "disableUpdate.ps1"

    ```PowerShell
    ```

=== "enableUpdate.ps1"

    ```PowerShell
    ```