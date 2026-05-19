## 修改默认编码

在claude code执行powershell命令时，输出中文会返回乱码，导致重试浪费token。

通过修改编码格式为utf-8，以解决上述问题。

打开powershell，输入`Notepad dollarprofile`，输入下述代码后保存文件即可。

```powershell
#Fix Chinese encoding for AI agents
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

```
