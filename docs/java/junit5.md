## 📌 环境搭建

配置测试运行器为JUnit

添加依赖

=== "pom.xml"

    ```xml
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter-engine</artifactId>
        <version>5.8.2</version>
        <scope>test</scope>
    </dependency>
    ```

## 📌 基本概念

测试类：使用`@Test`注解标记测试方法。

断言：使用`org.junit.jupiter.api.Assertions`类中的静态方法进行断言。

生命周期方法：

* @BeforeEach：每个测试方法前执行。
* @AfterEach：每个测试方法后执行。
* @BeforeAll：所有测试方法前执行一次。
* @AfterAll：所有测试方法后执行一次。

## 📌 高级特性

### 🚁 参数化

使用`@ParameterizedTest`注解标记参数化测试方法。

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class PracticeTest {
    @ParameterizedTest
    @ValueSource(strings = {"hello", "world"})  // 或者使用@CsvSource
    void testWithSingleString(String testValue) {
        assertTrue(testValue.length() > 0);
    }
}
```

### 🚁 动态测试

使用`@TestFactory`创建动态测试。

动态测试允许你在运行时生成多个测试实例，而不是在编译时固定测试数量。

```java
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;
import java.util.stream.Stream;  // Java 8 引入的流式处理工具
import static org.junit.jupiter.api.Assertions.assertTrue;

public class DynamicTestExample {
  @TestFactory
  Stream<DynamicTest> dynamicTests() {
      return Stream.of("hello", "world")
          .map(message -> DynamicTest.dynamicTest(message, () -> {
              assertTrue(message.length() > 0);
          }));
  }
}
```

### 🚁 测试超时

使用`@Timeout`注解标记测试方法。

---

参考资料：

[JUnit5官方文档](https://junit.org/junit5/docs/current/user-guide/)

