facebook-wda，通过http协议与webdriveragent通信

```python
from wda import Client

c = Client('http://localhost:8100')

# 屏幕截图
c.screenshot('screenshot.png')

session = c.session('com.apple.mobilesafari')

# 元素定位方式
# 支持回调函数调用
session(name='Search Wikipedia').tap()
session.type_text('Appium')

# xpath
session.xpath('//XCUIElementTypeButton[@name="Your Button Name"]')

# predicate，ios原生支持的定位方式，使用多个匹配条件来准确定位某一元素
session(predicate='name == "通知"').click()

# xpath与predicate的组合，效率更高
session(classChain='**/XCUIElementTypeTable/*[`name == "通知"`]').click()

```