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
    # 1. 停止并禁用核心更新服务
    Stop-Service -Name wuauserv -Force
    Set-Service -Name wuauserv -StartupType Disabled

    # 2. 停止并禁用更新 Orchestrator 服务（负责强制重启和安装）
    Stop-Service -Name UsoSvc -Force
    Set-Service -Name UsoSvc -StartupType Disabled

    # 3. 【关键步骤】清除服务的自动恢复操作，防止系统自动重启它们
    #    参数说明：reset= 86400 表示重置失败计数为1天（可自行调整）
    #    actions 表示失败后不执行任何操作
    sc.exe failure wuauserv reset= 86400 actions= run/0
    sc.exe failure UsoSvc reset= 86400 actions= run/0

    # 4. （可选）停止并禁用 Windows Update Medic Service（另一个隐藏的保护服务）
    #    该服务是Windows 10/11的新机制，用于修复更新组件
    Stop-Service -Name WaaSMedicSvc -Force -ErrorAction SilentlyContinue
    Set-Service -Name WaaSMedicSvc -StartupType Disabled -ErrorAction SilentlyContinue

    ```

=== "enableUpdate.ps1"

    ```PowerShell
    # 1. 恢复 Windows Update 主服务 (wuauserv)
    #    默认启动类型为“手动(触发器启动)” - 即 Manual (Trigger Start)
    Set-Service -Name wuauserv -StartupType Manual
    Start-Service -Name wuauserv -ErrorAction SilentlyContinue

    # 2. 恢复 Update Orchestrator 服务 (UsoSvc) - 负责强制更新
    Set-Service -Name UsoSvc -StartupType Manual
    Start-Service -Name UsoSvc -ErrorAction SilentlyContinue

    # 3. 恢复 Windows Update Medic Service (WaaSMedicSvc) - 隐藏的“医生”服务
    #    该服务默认启动类型为“手动”，用于修复更新组件，建议恢复
    Set-Service -Name WaaSMedicSvc -StartupType Manual
    Start-Service -Name WaaSMedicSvc -ErrorAction SilentlyContinue

    # 4. 恢复服务失败时的默认恢复操作（取消“无操作”设置）
    #    默认行为：第一次失败重启服务，第二次失败重启，第三次失败重启（间隔可参考）
    #    参数 reset= 86400 表示重置失败计数为1天，actions= 指定失败后的操作
    sc.exe failure wuauserv reset= 86400 actions= restart/5000/restart/10000/restart/60000
    sc.exe failure UsoSvc reset= 86400 actions= restart/5000/restart/10000/restart/60000
    # WaaSMedicSvc 默认恢复操作也类似，但通常不需要修改，这里恢复为默认空（系统默认）
    # 如果之前修改过，可以重置：
    sc.exe failure WaaSMedicSvc reset= 86400 actions= restart/5000/restart/10000/restart/60000

    ```