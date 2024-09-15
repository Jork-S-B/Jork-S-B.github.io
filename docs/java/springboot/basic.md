内置tomcat，不用再部署war包。

项目初始化: https://start.spring.io/

## 📌 maven

管理项目依赖

- 依赖安装: `mvn install`或者idea启动
- 打包项目: `mvn package`
- 启动项目: `mvn spring-boot:run`或者idea启动: application.main()

## 📌 MVC架构模式

model: 数据模型，提供要展示的数据

- DAO，封装对是数据库的访问
- Service，负责协调业务逻辑

view: 数据展示，即前端页面

controller: 控制器，定义接口，负责接口的请求和响应

## 📌 配置

- 连接池配置: hicari, 官方默认连接池
- 日志配置: logback, 内置日志框架
- 扩展日志配置: resources/logback.xml, 包括日志级别、存储时间、最大体积、sql打印至控制台
- 自定义全局变量配置

```Java
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

// 自定义全局变量配置
@Component // 被修饰的类交给springboot管理
public class ScheduleJob{

	@Value("${var}") // 引用application.properties定义的变量
	private String tests; // 不能使用static，即常量
}
```

## 📌 flyway组件

数据库版本管理工具，迭代或者库表配置变动时，自动执行相关SQL。

个人理解: 类似Django的`python manage.py migrate`

* SQL脚本命名规范`V版本号__描述.sql`，描述也不能重复，如: resources/db.migration/V1.0__init_demo.sql
* SQL执行报错，需要将库表执行失败的记录删除，方能重新执行。

## 📌 mybatis框架

调用关系: Controller -> Service -> DAO -> mapper

实体类、DAO、xml映射

DTO（Data Transfer Object）数据传输对象，是一种设计模式，用于在不同层级或不同系统间传输数据。可以避免直接暴露实体类的细节，用来过滤和转换数据。

## 📌 lombok

定义Java类时通过注解，省去get/set方法编写。

```Java
import lombok.Data;
import lombok.NonNull;
import lombok.EqualsAndHashCode;

// @EqualsAndHashCode(callSuper = true) // 继承多个类时使用，避免实例化子类可能出现误判
@Data // 被装饰的类会自动生成get/set、toString()、equals()、hashCode()
@NoArgsConstructor // 生成一个全参数构造器
@AllArgsConstructor // 生成一个无参构造器
public class Demo {
//    @NonNull，使用该装饰器时会自动生成该参数的构造方法
    private String id;

    private String name;
}
```

## 📌 fastjson

json数据处理，json和实体类转换。

```Java
import com.alibaba.fastjson.JSONObject;

public static void main(String[] args) {
    JSONObject test = new JSONObject();
    test.put("id", "1");
    test.put("name", "test");
    Demo demo = JSONObject.toJavaObject(test, Demo.class);
    System.out.println(demo.getId());
}
```

## 📌 jwt

json web token

常见鉴权方式:

- session: 存储于服务端，但分布式部署不适用
- token: 生成token存储在redis
- jwt: 格式为header.business.signature，由服务器生成，保存至客户端  
  header: 公用配置，如编码等  
  business: 业务信息，如存放用户名、过期时间等  
  signature: 加密模块，包括密钥secret；单点登录安全要求较高的，可以让密钥动态生成，每隔数分钟重新生成。

```JAVA
public static String createToken(Demo demo) {
    // 生成token
    Date expireDate = new Date(System.currentTimeMillis() + EXPIRATION * 1000); //过期时间
    Map<String, Object> map = new HashMap<>();
    // header.business.signature
    // header
    map.put("alg", "HS256");
    map.put("typ", "JWT");
    String token = JWT.create()
            .withHeader(map) // 添加头部
            //可以将基本信息放到claims中
            // business
            .withClaim("id", demo.getId())
            .withClaim("name", demo.getName())
            .withExpiresAt(expireDate) // 超时设置,设置过期的日期
            .withIssuedAt(new Date()) // 签发时间
            // signature
            .sign(Algorithm.HMAC256(SECRET)); // SECRET加密
    return token;
}
```

## 📌 pagehelper

分页组件，在原SQL侵入limit等语句

=== "PageUtils.java"

    ```JAVA
    import com.github.pagehelper.Page;
    
    public class PageUtils {
        public static <T> PageDTO<T> setPageInfo(Page page, T obj) {
            try {
                PageDTO<T> pager = new PageDTO<>();
                pager.setList(obj);
                pager.setTotal(page.getTotal());
                pager.setPage(page.getPageNum());
                pager.setSize(page.getPageSize());
                return pager;
            } catch (Exception e) {
                throw new RuntimeException("Error saving current page number data！");
            }
        }
    }
    ```

=== "PageDTO.java"

    ```JAVA
    import lombok.Data;
    
    @Data
    public class PageDTO<T> {
        private T list;
        private long total;
        private int page;
        private int size;
    }
    ```

## 📌 定时任务

- Timer: Java自带的定时任务api
- Scheduled: Springboot自带的注解
- Quartz: 异步任务调度框架，已集成在Springboot，crontab存储在数据库中
- XXL-JOB: 分布式定时任务，基于redis实现

=== "ScheduleJob.java"

```JAVA
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.Date;

@Component
public class ScheduleJob {

    @Scheduled(cron = "0 0/1 * * * ?")
    public void Start(){
        System.out.println(new Date());
    }
}
```

## 📌 网关与拦截器

### 🚁 网关

多个微服务可能有多个域名、登录方式等，通过网关统一鉴权、请求分发、请求过滤、请求日志记录、流量控制等。

### 🚁 拦截器

- 请求拦截，对哪些接口做token验证
- 鉴权管理
- 请求分发

## 📌 响应模版定义

先定义响应状态码，配合响应拦截器`@RestControllerAdvice`，统一响应格式如: {"status":0,"message":{"成功"}}

运行时异常，则需定义异常类型处理`@ExceptionHandler`及对应的响应模版枚举值。

---

## 📌 工具类

hutools: https://doc.hutool.cn/pages/index/

参考资料：

1.[完整项目代码](https://gitee.com/Jork-S-B/springboot-practice)