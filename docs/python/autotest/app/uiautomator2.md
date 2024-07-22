基于Google提供的原生UIAutomator工具，提供了Python库的形式

```python
import uiautomator2 as u2

device = u2.connect_usb("")
# device = u2.connect("127.0.0.1:7555")
print(device.device_info)
device.app_start("com.tencent.mm")

device.xpath("")
device(text="").click()

```