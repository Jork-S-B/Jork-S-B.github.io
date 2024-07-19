Django默认模版引擎为DjangoTemplates-DTL，当然也可修改为jinja2等其他引擎。

## 📌 DTL语法

* 注释：`{# 注释 #}`
* 传入变量：`{{ 变量 }} 输出，如 {{ user.name }}`
* 局部变量：`{% with user=users.0 %} {% endwith %}`
* for循环：`{% for 变量 in 列表 %} {% empty %} {% endfor %}`
* 条件分支：`{% if 条件 %} {% else %} {% endif %}`
* url反转：`{% url 'app:url_name' 参数 %}`
* 模板过滤器：`{{ 变量|过滤器 }}`
* 模板继承：`{% extends 'nav.html' %}`
* 模板引用：`{% include '模板名' %}`

!!! note "补充"

    在视图层应减少模板中的复杂逻辑。

### 🚁 for循环

* 不存在`continue`或`break`，可使用`empty`/`forloop.last`/`forloop.first`方法判断。
* `forloop.counter0`/`forloop.counter`，打印当前循环次数，前者从0开始，后者从1开始。
* `forloop.revcounter0`/`forloop.revcounter`，倒序打印，前者从len开始，后者从len-1开始。
* 如需倒序遍历，则在for循环语句后使用`|reversed`。存在额外的性能开销，django 3.0已弃用。

```html

<section>
    <h2>User Information</h2>
    <ul>
        {% for user in users %}
        <li>Id: {{ forloop.counter0 }} - Name: {{ user.name }} - Age: {{ user.age }}</li>
        {% endfor %}
    </ul>
</section>
```

### 🚁 条件分支

if语句如果有符号如`>-大于`，前后必须要有空格。

```html
{% if special_message %}
<section>
    <p>{{ special_message }}</p>
</section>
{% endif %}
```

### 🚁 url反转

=== "example.html"

    ```html
    <a href="{% url 'learn:book_id_path' book_id=pk.age %}">View Detail - url反转，使用关键字参数</a>
    <a href="{% url 'learn:book_id_get' %}?id={{ pk.age }}&name={{ pk.name }}">View Detail - get请求</a>
    ```

=== "views.py"

    ```python
    def query_by_book_id(request):
        # 简单的get请求: http://127.0.0.1:8383/learn/book?id=1&name=123
        book_id = request.GET.get('id')
        book_name = request.GET.get('name')
        tmp = reverse("learn:book_id_get")  # 路由反转，`命名空间:路由名称`的格式
        return HttpResponse(f"book_id is {book_id}, book_name is {book_name}, reverse_url is {tmp}")
    
    def book_id_path(request, book_id):
        # 简单的路径参数: http://127.0.0.1:8383/learn/book/1
        # 路由反转
        tmp = reverse("learn:book_id_path", kwargs={"book_id": book_id})  # 该url需要有可变参数，否则报错
        return HttpResponse(f"book_id is {book_id}, reverse_url is {tmp}")
    ```

=== "urls.py"

    ```python
    # 指定命名空间，避免路由名称重名
    app_name = "learn"
    
    urlpatterns = [
        path('book', views.query_by_book_id, name="book_id_get"),
        path('book/<int:book_id>', views.book_id_path, name="book_id_path"),  # 设置要求为整型，输入非整型返回404
        """
        path类型还支持：
            str（默认值，不能包含斜杠）
            slug（-、_、数字、字母拼接的字符串）
            uuid
            path（非空的英文字符串，包括斜杠）
        """
    ] 
    ```

### 🚁 模板过滤器

* 与python内置方法类似的过滤器：`capfirst`/`lower`/`upper`/`join`/`length`/`slice`/`cut`
* `truncatechars`：字符串超过指定长度时以...展示。`truncatechars_html`与之类似，但保留html标签，不计入长度。
* `date:"Y/m/d H:i:s"`：日期格式转换
* `default:"No Data"`：设置默认值
* `default_if_none:"None"`：None时显示默认值
* `first`/`last`/`random`
* `floatformat:2`：浮点数格式化，小数点后保留2位
* `safe`/`striptags`：保留/删除html标签

=== "example.html"

    ```html
    <div class="content">
        <p>
            {# capfirst首字母大写，与capitalize()类似 #}
            {{ users.0.name|capfirst }}
        </p>
        <p>
            {# cut清除指定字符，与strip()类似 #}
            {# truncatechars超过指定长度时以...展示 #}
            {# 类似的还有truncatechars_html（保留html标签，且不计入长度）#}
            {{ special_message|cut:" "|truncatechars:"14" }}
        </p>
        <p>
            {# 模板过滤器，日期格式转换 #}
            {{ current_time|date:"Y/m/d H:i:s" }}
        </p>
        <p>
            {# 模板过滤器，默认值 #}
            {{ null|default:"No Data" }}
        </p>
        <p>
            {# 模板过滤器，None时显示默认值 #}
            {{ None|default_if_none:"None" }}
        </p>
        <p>
            {# 模板过滤器，first/last/random #}
            {{ users|first }}
            <br>
            {{ users|last }}
            <br>
            {{ users|random }}
        </p>
        <p>
            {# 模板过滤器，float格式化 #}
            {{ float|floatformat:2 }}
        </p>
        <p>
            {# 模板过滤器，允许html标签 #}
            {{ html|safe }}
        </p>
        <p>
            {# 模板过滤器，删除html标签 #}
            {{ html|striptags }}
        </p>
    </div>
    ```

=== "views.py"

    ```python
    context = {
        "site_name": "whm_learn",
        "users": [
            {"name": "whm", "age": 18},
            {"name": "whm2", "age": 19},
            {"name": "whm3", "age": 20},
        ],
        "special_message": " special _ message ",
        "current_year": datetime.now().year,
        "current_time": datetime.now(),
        "float": 123.4569999,
        "html": """
            <h1><a href="#">baidu</a></h1>
        """,
    }
    
    def template_filter(request):
        return render(request, 'template_filter.html', context=context)
    ```

### 🚁 模板继承

* 父模板通过如`{% block body %}`标签定义块，子模板通过`{% extends body %}`继承父模板，并重写块。
* 若父模版的内容也要保留，则子模板通过`{{ block.super }}`继承。

=== "nav.html"

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{% block title %}{% endblock %}-whm</title>
        {% block head %}{% endblock %}
    </head>
    <body>
    
    {% block body %}这是nav.html父模版的内容{% endblock %}
    
    <hr>
    <footer>
        {# 可接收子模板传参 #}
        <p>&copy; {{ current_year }} whm-django-practice</p>
    </footer>
    </body>
    </html>
    ```

=== "children.html"

    ```html
    {% extends 'nav.html' %}
    {% block title %}children{% endblock %}
    {% block body %}
    <div class="content">
        <p>block.super：{{ block.super }}</p>
        {% with pk=users.0 %}
            <p>pk = {{ pk.name }}</p>
    </div>
    {% endblock %}
    ```

## 📌 加载静态资源

1. `settings.py`配置`STATICFILES_DIRS`，模版文件中通过`{% load static %}`即可加载静态资源。
2. 不想每个模版都写`{% load static %}`，那么接着在`settings.py`配置`TEMPLATES`
   加载插件: `'builtins': ['django.templatetags.static']`。
3. 模版文件中加载CSS或JS：`<link rel="stylesheet" href="{% static 'style.css' %}">`
4. 额外的静态资源如用户上传的图片，`settings.py`配置`MEDIA_URL`和`MEDIA_ROOT`，并在`urls.py`
   追加`urlpatterns = [ ... ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`

---

参考资料：

1.[完整项目代码](https://gitee.com/Jork-S-B/django-practice)

2.[Django模板语言（DTL）](https://www.cnblogs.com/nixindecat/p/10526983.html)
