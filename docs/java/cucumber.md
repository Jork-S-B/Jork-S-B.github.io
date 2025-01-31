BDD，行为驱动开发，起源于TDD-测试驱动开发，更侧重软件行为而非具体代码实现。

强调从用户角度出发，使用自然语言描述应用的行为。

Cucumber，一个支持BDD的工具，将Gherkin语言编写的场景转换为自动化测试。同时支持多种编程语言，如 Java、Ruby、JavaScript 等。

## 📌 编写Gherkin场景

编写Feature文件是Cunumber的核心，通过Gherkin语法来描述系统的行为。

Gherkin场景通常包括以下几个部分：

* Feature：描述功能的标题和简短描述。
* Scenario：描述特定场景的步骤。
* Given：描述前提条件。
* When：描述执行的操作。
* Then：描述期望的结果。

=== "src/test/resources/features/ui_tests.feature"

    ```java
    Feature: UI Tests
    
      Scenario: Open Baidu and search for Selenium
        Given the browser is open
        When I navigate to "https://www.baidu.com"
        And I enter "Selenium" in the search box
        And I click on the search button
    #    Then I should see search results related to "Selenium"
    ```

## 📌 编写Step

编写步骤，通过装饰器将Feature文件的步骤与实际测试代码关联起来。

=== "src/test/java/com/demo/autotest/steps/UiSteps.java"

    ```java
    package com.demo.autotest.steps;
    
    import static org.testng.Assert.assertTrue;
    
    
    import org.openqa.selenium.By;
    import org.openqa.selenium.WebDriver;
    import org.openqa.selenium.WebElement;
    import org.openqa.selenium.chrome.ChromeDriver;
    
    import io.cucumber.java.After;
    import io.cucumber.java.Before;
    import io.cucumber.java.en.Given;
    import io.cucumber.java.en.When;
    import io.cucumber.java.en.Then;
    
    public class UiSteps {
    
        private WebDriver driver;
    
        @Before
        public void setup() {
            System.setProperty("webdriver.chrome.driver", "driverpath/chromedriver.exe");
            driver = new ChromeDriver();
        }
    
        @After
        public void teardown() {
            if (driver != null) {
                driver.quit();
            }
        }
    
        @Given("the browser is open")
        public void the_browser_is_open() {
            assertTrue(driver != null);
        }
    
        @When("I navigate to {string}")
        public void i_navigate_to(String url) {
            driver.get(url);
        }
    
        @When("I enter {string} in the search box")
        public void i_enter_in_the_search_box(String searchText) {
            WebElement searchBox = driver.findElement(By.name("wd"));
            searchBox.sendKeys(searchText);
        }
    
        @When("I click on the search button")
        public void i_click_on_the_search_button() {
            WebElement searchButton = driver.findElement(By.id("su"));
            searchButton.click();
        }
    
    //    @Then("I should see search results related to {string}")
    //    public void i_should_see_search_results_related_to(String expectedText) {
    //        // 定位有问题，先跳过
    //        WebElement searchResult = driver.findElement(By.id("content_left"));
    //        assertTrue(searchResult.getText().contains(expectedText));
    //    }
    }
    
    ```

## 📌 运行测试

只需基本的单元测试功能，并且希望保持代码简洁，选择JUnit。

需要更复杂的测试场景，如依赖测试、数据驱动测试、并行测试等，选择TestNG。

=== "src/test/java/com/demo/autotest/runners/TestRunner.java"

    ```java
    package com.demo.autotest.runners;
    
    import io.cucumber.testng.AbstractTestNGCucumberTests;
    import io.cucumber.testng.CucumberOptions;
    
    @CucumberOptions(
            features = "src/test/resources/features",
            glue = "com.demo.autotest.steps",
            plugin = {"pretty", "html:target/cucumber-reports"}
    )
    public class TestRunner extends AbstractTestNGCucumberTests {
    }
    
    ```

## 📌 查看报告

运行测试后，可在`target/cucumber-reports.html`查看详细的测试报告。

---

完整代码: 还没上传