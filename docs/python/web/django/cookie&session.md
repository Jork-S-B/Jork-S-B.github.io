## 📌 cookie

用户信息，存储在服务端，体量小，不能超过4K

### 🚁 CSRF

跨域请求伪造，攻击原理：登录后生成的cookie，访问跨域的网站，cookie会自动发送给跨域的网站，此时跨域的网站在用户不知情情况下执行非法操作。

### 🚁 CSRF防御

在表单和cookie加入csrftoken，请求时两者匹配成功（并非一致）才执行操作。


## 📌 session

- 存储在服务端：django默认将session存储在数据库，当然也可存到缓存、文件等
- 存储在客户端：flask默认将session加密后存储在cookie

### 🚁 django修改session存储机制

修改`settings.py`中的`SESSION_ENGINE`，配置为：

- `django.contrib.sessions.backends.db`：默认方案，存储到数据库
- `django.contrib.sessions.backends.file`：存储到文件
- `django.contrib.sessions.backends.cache`：存储到缓存，前提是配置了CACHES，需要使用memcached
- `django.contrib.sessions.backends.cache_db`：先存缓存，再存数据库
- `django.contrib.sessions.backends.signed_cookies`：将session加密后存储在cookie，需要考虑安全性及容量

