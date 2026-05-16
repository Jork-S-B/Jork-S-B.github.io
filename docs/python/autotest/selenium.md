## 📌 元素定位方式

* id: 标签的id属性
* name: 标签的name属性
* class_name: 标签的class属性
* tag_name: html标签的类型
* link_text: 超链接文本
* partial_link_text: 超链接文本的模糊匹配
* css_selector: 相对万金油的定位方法，定位语法麻烦
* xpath: 有自己的独特语法，基于文件系统树状结构定位

调用方法如：`find_element_by_xpath`或者`find_element(By.XPATH,xpath)`

## 📌 行为链

ActionChains，实现简单的交互行为，如鼠标悬停move_to_element、拖拽drag_and_drop、点击click，键盘输入send_keys，以及内容菜单交互perform等。

## 📌 等待

```python
time.sleep(timeout)  # 强制等待
driver.implicitly_wait(timeout)  # 隐式等待，等待页面加载完成
WebDriverWait(driver, timeout, poll_frequency=poll_frequency, ignored_exceptions=None)  # 显式等待，等待某个元素加载完
# ignored_exceptions：超时后的抛出的异常信息，默认抛出NoSuchElementExeception异常

# WebDriverWait与until()或until_not()搭配使用
WebDriverWait(driver, 10).until(lambda x: x.find_element(by='xpath', value=value), message=f'找不到元素')
```

## 📌 WebDriver

|                           方法                           | 补充说明                           |
|:------------------------------------------------------:|:-------------------------------|
| `drvier.switch_to.window(diver.window_handles[index])` | 切换窗口或标签页                       |
|                `drvier.switch_to.alert`                | 切换至JS弹框，再调用accept、dismiss等方法交互 |
|               `drvier.switch_to.frame()`               | 切换至指定frame                     |
|             `drvier.save_screenshot(path)`             | 截图                             |

## 📌 xpath

通过结构关系锚定唯一元素，而不是直接复制xpath表达式。

|           表达式            | 补充说明                    |
|:------------------------:|:------------------------|
|     `following::div`     | 获取节点后的所有div             |
| `following-sibling::div` | 取该节点的后一个兄弟节点            |
| `preceding-sibling::div` | 取该节点的前一个兄弟节点            |
|  `//i/*[name()="svg"]`   | 从根节点开始匹配，匹配所有i标签下的svg标签 |
| `button[not(@disabled)]` | 匹配不包含disable属性的按钮       |
|  `contains(.,"{text}")`  | 匹配包含text文本的任意标签         |

!!! tip

    浏览器F12->Console调试，输入`setTimeout(function(){debugger;},1000)`，表示过1秒后进入调试模式，在排查元素定位、元素覆盖时有用。

    2025/5/18: setTimeout(()=>{debugger;},1000)，同理，效果一样。

## 📌 chromedriver

chromedriver和chrome浏览器大版本号保持一致即可。

114及更早版本: https://chromedriver.storage.googleapis.com/index.html

130以上版本: https://googlechromelabs.github.io/chrome-for-testing

---

参考资料:

1.[selenium中文文档](https://python-selenium-zh.readthedocs.io/zh-cn/latest/)

2.[谷歌浏览器驱动下载指路](https://blog.csdn.net/m0_54958293/article/details/134663146)