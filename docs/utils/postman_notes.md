## 📌 动态关联

1. `Environment`Tab页中创建环境，并切换至对应环境
2. `Tests`Tab页中声明变量
3. 接口以`{{token}}`的方式作为参数值

```JavaScript
// 2. `Tests`Tab页中声明变量
var jsonData = pm.response.json()
pm.environment.set("token",jsonData.token)
```