## 📌 动态关联

```JavaScript
var jsonData = pm.response.json()
pm.environment.set("token",jsonData.token)

{{token}}  // 使用token
```