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