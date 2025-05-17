## 📌 Playwright

为现代web应用程序提供可靠的端到端测试。

端到端: 用于验证整个应用程序从开始到结束的流程是否符合预期。

其核心目标是模拟真实用户的操作行为，确保各个组件、系统模块、外部依赖（如数据库、API、第三方服务等）协同工作正常。

### 🚁 对比Selenium

|  功能   | Playwright                    | Selenium              |
|:-----:|:------------------------------|:----------------------|
| 浏览器管理 | 自带浏览器二进制文件                    | 依赖`WebDriver`和本地浏览器安装 |
| 等待机制  | 智能等待机制，自动等待元素就绪               | 需手动添加`WebDriverWait`  |
| 请求拦截  | 支持拦截和修改网络请求（route API），模拟响应数据 | 不直接支持                 |
| 并发支持  | 支持多个浏览器上下文                    | 每个会话共享全局状态            |
| 移动端模拟 | 支持设备模拟                        | 依赖 Appium 扩展支持        |

## 📌 快速使用

pip install playwright

playwright install # 安装自带浏览器和ffmpeg

```python
from playwright.sync_api import sync_playwright

pw = sync_playwright().start()
driver = pw.chromium.launch(headless=False)
page = driver.new_page()
page.goto("https://www.baidu.com")
page.fill("input[name='wd']", "playwright")
page.wait_for_timeout(2000)  # 暂停2秒

```

## 📌 元素定位与操作

* id
* text: 文本
* tag name: 标签名，单独使用重复率太高
* css: 包括简单选择器、复合选择器
* xpath

query_selector: 找单个元素

query_selector_all: 找一组元素，返回列表

=== "示例"

    ```python
    # id选择器，找不到元素时报错：TimeoutError: Timeout 3000ms exceeded.
    page.locator("id=username").fill("admin", timeout=3000)  # fill方法会覆盖原文本
    # 同上
    page.locator("#username").fill("admin")
    
    # 文本选择器
    page.locator("text=提交").click()
    
    # 标签名选择器
    print(page.locator("p").text_content())
    # 找一组元素，返回列表
    print(page.query_selector_all("p").text_content())
    ```

=== "css选择器"

    ```python
    # css简单选择器
    page.locator(".pn").fill("admin")
    
    # css复合选择器-并列选择器，连写
    page.locator("input#username")
    
    # css复合选择器-后代选择器，空格分隔
    page.locator("div input#username")
    
    # css复合选择器-直接子代选择器，>分隔
    page.locator("div>input#username")
    
    # css复合选择器-通用选择器，*
    page.locator("div>*")
    
    # css复合选择器-群组选择器，,分隔
    page.locator("#username, #password,a")
    
    # css复合选择器-属性选择器，[=][*=][^=][$=]
    # [*=]: 包含，模糊匹配
    page.locator("input[name*='nam']")
    # [^=]: 以xx开头
    # [$=]: 以xx结尾
    page.locator("input[name^='user']")
    page.locator("input[name$='name']")
    
    # 伪类选择器
    # :nth-child(): 匹配元素下的第n个子元素，不区分子元素类型。
    # :nth-of-type(): 匹配元素下的第n个子元素，要求同个元素类型。
    # :not(): 否定选择器，匹配所有不匹配的元素。
    # .nth(): 匹配元素下的第n个元素，n为数字，即索引下标。
    page.locator("div>:nth-of-type(2)")
    
    ```

## 📌 常用方法

get_attribute: 获取属性值，如`get_attribute('id')`

bounding_box: 获取元素在页面中的位置和尺寸信息

is_displayed / is_hidden: 判断元素是否可见，判断是否隐藏

is_enabled: 判断元素是否可用，如检查属性是否带`disabled`、`readonly`等

screenshot: 截图，默认png，`page.screenshot(path='./1.png')`；返回`bytes`字节流，搭配`ddddocr`识别简单的验证码。

```python
ele = page.locator(".img='verifycode'")  # 假设这是图片验证码的元素
ele_bytes = ele.screenshot(path="./code.png")
ocr = ddddocr.DdddOcr(show_ad=False)
code = ocr.classification(ele_bytes)

ele = page.locator(".img='verifycode2'")  # 假设这是算术验证码的元素
ele_bytes = ele.screenshot(path="./codecalc.png")
res = ocr.classification(ele_bytes)  # 如：10+15=？
res = res.split("=")[0]
code = eval(res)

```

### 🚁 浏览器控制

获取窗口大小: `page.viewport_size()`, 返回字典

设置窗口大小: `page.set_viewport_size()`

前进: `page.go_forward()`

后退: `page.go_back()`

刷新: `page.reload()`

当前url: `page.url`

标题: `page.title()`

```python
# 浏览器窗口最大化
driver = pw.chromium.launch(headless=False, args=["--start-maximized"])
page = driver.new_page(no_viewport=True)

```

### 🚁 单选/多选/下拉

is_checked: 判断元素是否被选中，适用于`checkbox`、`radio`多选/单选项目。

is_selected: 判断元素是否被选中，适用于`select`下拉框。

select_option: 选择下拉框的选项，多选时用,分隔。

```python
ele = page.locator("select")
ele.select_option(index=(0, 3), value="option2", label="选项3")

```

### 🚁 键盘操作

```python
key = "Enter"
key2 = "Control+a"
key3 = "Backspace"
page.keyboard.press(key)

```

### 🚁 鼠标操作

鼠标悬停: `page.hover()`

鼠标双击: `page.dbclick()`

鼠标右键点击: `page.click(button="right")`

鼠标右键点击: `ele1.drag_to(ele2)`

鼠标滚轮: `page.mouse.wheel(0, 100)`


