## 📌 使用脚本将鉴权后的token写入header

1. 目标接口或者目录，设置前置操作，选择全局脚本或者自定义脚本
2. 编写脚本，JavaScript语言，内置变量与函数跟postman类似

```javascript
const authUrl = 'https://xxx.com/xxx';
const authParams = {
  method: 'POST',
  url: authUrl,
  header: {
    "Content-Type": "application/json",
  },
  body: {
    mode: 'raw',
    raw: JSON.stringify({
      "SecretId": "xxx",
      "Key": "xxx"
    })
  }
};

pm.sendRequest(authParams, function (err, response) {
  const responseData = response.json()
  console.log(responseData);

  if (responseData.success && responseData.data) {
    // 将 data 字段按行分割成数组
    const headersArray = responseData.data.split('\n');
    const headers = {};

    // 遍历，解析键值对
    headersArray.forEach(header => {
      const [key, value] = header.split(':');
      if (key && value) {
        headers[key] = value
      }
    });

    // 设置请求头
    pm.request.headers.add({ key: 'key', value: headers['key'] });
    pm.request.headers.add({ key: 'rand', value: headers['rand'] });
    pm.request.headers.add({ key: 'version', value: headers['version'] });;
  }
});

```