## 📌 造仿真数据

1. 右击线程组->添加取样器->OS进程取样器，并进行配置
2. 添加后置处理器->JSON提取器，并进行配置
3. 在请求报文中使用提取出来的变量，格式为`${变量名}`

=== "demo.py"

    ```python
    import json
    from faker import Faker
    from faker.providers import BaseProvider
    
    
    # 自定义数据
    class CustomFaker(BaseProvider):
        def prodid(self):
            # 假设是从库表或接口获取到的订购产品id
            prod_list = ["prodid1", "prodid2", "prodid3"]
            return self.random_element(prod_list)
    
    
    faker = Faker(locale='zh_CN')
    faker.add_provider(CustomFaker)
    result = {
        "id_num": faker.ssn(),
        "name": faker.name(),
        "phone": faker.phone_number(),
        "email": faker.email(),
        "address": faker.address(),
        "birthday": faker.date_of_birth().strftime("%Y-%m-%d"),
        "prodid": faker.prodid()
    }
    
    # print(json.dumps(result,ensure_ascii=False))  # JMeter中执行python反而这一行结果乱码
    print(json.dumps(result))

    ```

=== "OS进程取样器配置示例"

    ![img.png](image/Snipaste_2024-06-15_23-42-26.jpg)

=== "JSON提取器配置示例"

    ![img.png](image/Snipaste_2024-06-15_23-50-54.jpg)

=== "报文中使用变量示例"

    ```json
    {
        "name":"${name}",
        "id_num":"${id_num}",
        "phone":"${phone}"
    }
    
    ```

## 📌 响应报文的汉字乱码

解决方案:

1. 打开JMeter目录的`bin/jmeter.properties`文件
2. 搜索关键字: `#sampleresult.default.encoding=ISO-8859-1`
3. 在该行下方新增: `sampleresult.default.encoding=UTF-8`
4. 重启JMeter

其他解决方案参考: [解决Jmeter响应报文中文乱码的问题-3种解决办法](https://blog.csdn.net/u013302168/article/details/126366082﻿)

## 📌 使用插件

1. 下载插件: https://jmeter-plugins.org/downloads/old/
2. 解压后把`lib`文件夹扔到JMeter目录，重启JMeter。之后便可使用阶梯加压线程组、响应时间折线图、TPS折线图等组件。

## 📌 使用代理服务器录制脚本

参考资料: [jmeter代理服务器录制脚本教程（入门篇）](https://blog.csdn.net/weixin_42614544/article/details/109514086)

## 📌 使用自带函数

工具->函数助手对话框，找需要用的函数。

=== "示例"

    ```json
    {
        "id":"${__Random(100,105)}",  // 从100至105的序列中随机取数
        "phone":"${__chooseRandom(1.0.1,1.0.2,1.0.3)}"  // 从该列表中随机取数
    }
    ```

## 📌 调外部jar包方法

1. jar包需要放JMeter目录的`lib\ext`目录下
2. jar包里调用的第三方jar包也要放到`lib`和`lib/ext`里
3. 记得重启JMeter，添加前置处理器: BeanShell PreProcessor，然后写脚本

=== "BeanShell PreProcessor"

    ```java
    import xx.Util;
    
    String sp = "18" + Integer.toString(${__Random(000000000,999999999,)});
    log.info("==================phonenum is" + sp);
    vars.put("phone",sp);
    String code = Util.encrypt(sp);
    
    // 存入变量，在脚本文本中通过${phone}引用，不能跨线程
    vars.put("phone",code);

    // 记录日志
    log.info("==================phonenum is" + vars.get("phone"));

    // props能跨线程，是hashtable对象
    props.put("phone",code);  // 在脚本文本中通过${__P(phone)}引用
    ```

参考资料: [jmeter引用jar包的3种方式](https://www.cnblogs.com/uncleyong/p/11475577.html)

## 📌 报告分析

参考资料:

https://blog.csdn.net/m0_61066945/article/details/136062323

https://blog.csdn.net/qq_24394093/article/details/90732577
