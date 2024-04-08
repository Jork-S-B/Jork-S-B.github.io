## 📌 动态关联

1. `Environment`Tab页中创建环境，并切换至对应环境
2. `Tests`Tab页中声明变量
3. 请求体中，以`{{token}}`的格式，引用全局变量作为参数值

```JavaScript
// 2. `Tests`Tab页中声明变量
var jsonData = pm.response.json()
pm.environment.set("token",jsonData.token)

```

## 📌 断言

`Tests`Tab页中加入断言语句，或者点击右侧`Snippets`代码片段，快速添加断言。

```JavaScript
// 断言：响应状态码
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// 断言：返回数据中包含的内容
pm.test("Body matches string", function () {
    pm.expect(pm.response.text()).to.include("success");
});

// 断言：返回的JSON内容检查
pm.test("Your test name", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.msg).to.eql("success");
});

```

## 📌 参数化

1. 准备测试数据文件，将需要参数化的数据，以`[{用例1,用例2,...}]`的格式，保存为JSON文件。
2. 请求体中，以`{{username}}`的格式，引用文件中的变量作为参数值。
3. 断言语句/代码中，以`data.参数名`的格式，引用文件中的变量作为参数值。data是Postman内置对象，无需声明。
4. 新建`Collection`，在`Run`选择数据文件以及其他设置，批量运行。


---