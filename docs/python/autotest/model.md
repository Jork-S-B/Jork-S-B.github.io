## 📌 POM

Page Object Model，在自动化测试中，将页面元素（元素定位）、元素操作（例如点击/输入）、业务逻辑分离，实现“高内聚低耦合”，通过该方式，让测试代码更清晰、可维护及可重用。

具体实现：

* 页面类(Page Class)，每个页面（或页面的一部分）被抽象为一个类，包含页面元素和元素相关的操作方法。
* 页面元素(Web Elements)，在页面类中，各种页面元素（如按钮、文本框等）作为类的属性被定义。
* 操作方法(Actions)，在页面类中，定义各种操作方法，模拟用户对页面元素的操作如点击、输入文本等。

## 📌 关键字驱动

将测试步骤抽象为关键字，通过关键字构建测试用例，使设计用例时聚焦于业务逻辑，方便非技术人员参与用例设计。

## 📌 简单示例

=== "pages/base_page.py"

    ```python
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    class BasePage:
        def __init__(self, driver):
            self.driver = driver
    
        def find_element(self, by, value):
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((by, value))
            )
    
        def click(self, by, value):
            element = self.find_element(by, value)
            element.click()
    
        def send_keys(self, by, value, text):
            element = self.find_element(by, value)
            element.send_keys(text)
    
    ```

=== "pages/search_page.py"

    ```python
    from pages.base_page import BasePage
    
    class SearchPage(BasePage):
        SEARCH_INPUT = (By.NAME, 'q')
        SEARCH_BUTTON = (By.XPATH, '//*[@id="search-form"]/button')
    
        def enter_search_query(self, query):
            self.send_keys(*self.SEARCH_INPUT, query)
    
        def click_search_button(self):
            self.click(*self.SEARCH_BUTTON)
    
    ```

=== "keywords/search_keywords.py"

    ```python
    from pages.search_page import SearchPage
    
    class SearchKeywords:
        def __init__(self, driver):
            self.search_page = SearchPage(driver)
    
        def perform_search(self, query):
            self.search_page.enter_search_query(query)
            self.search_page.click_search_button()

    ```

=== "conftest.py"

    ```python
    import pytest
    from selenium import webdriver
    
    @pytest.fixture(scope='function')
    def driver():
        driver = webdriver.Chrome()
        yield driver
        driver.quit()
    
    ```

=== "tests/test_search.py"

    ```python
    import pytest
    from keywords.search_keywords import SearchKeywords
    
    def test_search(driver):
        search_keywords = SearchKeywords(driver)
        driver.get('https://www.example.com')
        search_keywords.perform_search('pytest')
        assert 'pytest' in driver.title
    ```

---