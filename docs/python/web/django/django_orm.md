在Django的MVT架构中，Model（模型）负责数据的存储和检索。模型定义了数据的结构和行为，通常是与数据库交互的部分。

## 📌 字段类型

### 🚁 AutoField

未显式的指定主键时，默认会生成一个自增的id字段，在库表里是bigint类型。

或者指定主键`UUIDField`/`ShortUUIDField`。

`id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)`

### 🚁 CharField

不能超过255个字符；长文本时需使用`TextField`，在库表里是varchar类型。

`EmailField`/`URLField`，本质也是varchar。

| 属性                                 | 说明                       |
|:-----------------------------------|:-------------------------|
| max_length                         | 最大长度                     |
| validators=[MinLengthValidator(6)] | 最小长度，min_length需要搭配验证器使用 |
| unique=True                        | 唯一字段                     |
| null=True                          | 可空字段                     |
| blank=True                         | 仅表单提交验证时可为空              |
| default=1                          | 默认值，支持传函数，不支持lambda或者推导式 |

```python
username = models.CharField("用户名", max_length=20)
password = models.CharField("密码", max_length=20, validators=[MinLengthValidator(6)])
email = models.CharField("邮箱", max_length=50, unique=True, blank=True)
```

### 🚁 DateTimeField

* `DateTimeField`：年月日时分秒
* `DateField`：年月日
* `TimeFiel`：时分秒
* 属性`auto_now_add`与`auto_now`，前者仅记录首次入库时间

```python
createtime = models.DateTimeField("创建时间", auto_now_add=True)  # 年月日时分秒
updatetime = models.DateTimeField("更新时间", auto_now=True)
birthday = models.DateField("生日")
```

### 🚁 IntegerField

其他的整型：BigIntegerField、PositiveIntergerField、SamllIntegerField、PositiveSamllIntergerField

```python
# 通过IntegerField实现枚举字段
state = models.IntegerField("状态", choices=[
    (0, '失效'),
    (1, '生效'),
]
```

### 🚁 BooleanField

布尔类型，默认值为None。NullBooleanField则是可空类型。

!!! note "补充"
    
    创建或修改表模型，需要执行migrate同步到库表。

    python manage.py makemigrations  # 创建数据库迁移脚本

    python manage.py migrate  # 执行迁移脚本，迁移应用的数据库表定义（更新表模型）


## 📌 外键

* 一对多
* 多对一
* 多对多，会建中间表存储关联信息

=== "models.py"
    
    ```python
    class LearningUser(models.Model):
        """
        用户表
        """
        # 不指定主键，默认会生成一个自增的id字段（在库表里是bigint类型）
        # 或者指定主键UUIDField/ShortUUIDField
        username = models.CharField("用户名", max_length=20)  # CharField不能超过255个字符；长文本使用TextField
        # Model中定义min_length需要搭配验证器使用
        password = models.CharField("密码", max_length=20, validators=[MinLengthValidator(6)])
        # blank=True，仅表单提交时可为空
        email = models.CharField("邮箱", max_length=50, unique=True, blank=True)  # 有EmailField，但本质也是varchar；URLField与之类似
        # auto_now_add仅首次入库时记录时间
        createtime = models.DateTimeField("创建时间", auto_now_add=True)  # 年月日时分秒
        # updatetime = models.DateTimeField("更新时间", auto_now=True)
        # birthday = models.DateField("生日")  # 年月日，TimeField则是时分秒
        state = models.IntegerField("状态", choices=[
            (0, '失效'),
            (1, '生效'),
        ], default=1)  # default支持传函数，不支持lambda或者推导式
    
        # 其他类似的整型还有：BigIntegerField、PositiveIntergerField、SamllIntegerField、PositiveSamllIntergerField
        # is_active = models.BooleanField()  # 默认值为None；NullBooleanField则是可空类型
    
        class Meta:
            db_table = "leaning_user"  # 指定表名
            ordering = ["-createtime"]  # 指定表默认排序
    
    
    class Article(models.Model):
        """
        文章表
        """
        title = models.CharField("标题", max_length=50)
        content = models.TextField("内容")
        # 设置的外键关联如果是其他APP的，则指定app名，appname:modelname
        # 当外键关联自身，则使用self
        author = models.ForeignKey(LearningUser, on_delete=models.CASCADE, related_name="articles")  # 外键，也是一对多
        """
        on_delete可选值：
        CASCADE, 级联
        PROTECT, 受保护，被外键引用时不能被删除
        SET_NULL, 同步设置null=True
        SET_DEFAULT, 同步设置default=''
        SET(), 通过set()方法指定值或方法
        DO_NOTHING
        """
        tags = models.ManyToManyField("Tag", related_name="articles")  # 多对多，会建中间表存储关联信息
    
    
    class UserExtend(models.Model):
        """
        扩展信息表，一对一
        """
        birthday = models.DateField("生日")  # 年月日，TimeField则是时分秒
        updatetime = models.DateTimeField("更新时间", auto_now=True)
        user = models.OneToOneField(LearningUser, on_delete=models.CASCADE, related_name="extend")
    ```
    
=== "views.py"

    ```python
    def foreign_key_example(request):
        user = LearningUser.objects.get(username='whm')
        article = Article(title='测试文章', content='测试内容', author=user)
        article.save()
        # uas = user.article_set.all()  # 若指定了related_name，则使用related_name也可以
        uas = user.articles.filter(title__contains='测试文章')
        tmp = ''.join([f"<p>标题：{ua.title}， 内容：{ua.content}， 作者：{ua.author.username}</p>" for ua in uas])
        return HttpResponse(tmp)
    ```
    
## 📌 查询

* 查询单体：`Model.objects.get(username='whm')`
* 查询所有：`Model.objects.all()`
* 查询带排序：`Model.objects.order_by("-createtime")`，代表降序；或者在建表时Meta类中指定ordering，根据什么字段进行默认排序
* 反向查询，即`!=`：`Model.objects.exclude(username='whm')`
* 查询带条件：`Model.objects.filter(username='whm')`

=== "filter的查询表达式"

    ```python
    def query_example(request):
        user = LearningUser.objects.filter(username='whm')  # 精确查询，与__exact等价
        user = LearningUser.objects.filter(username__ne='whm')  # 反向查找（!=），但使用exclude更直观
        user = LearningUser.objects.filter(username__iexact='WHM')  # 精确查询但忽略大小写
        user = LearningUser.objects.filter(username__regex=r'^wh')  # 正则查询，大小写敏感，同理i-xx时忽略大小写
        user = LearningUser.objects.filter(username__contains='h')  # 大小写敏感，同理icontains时忽略大小写
        user = LearningUser.objects.filter(username__startswith='wh')  # 大小写敏感，同理i-xx时忽略大小写；类似的还有endswith
        user = LearningUser.objects.filter(username__in=['whm', 'whm2'])
        user = LearningUser.objects.filter(username__isnull=False)  # 查非空
        """
        还有__gt-大于，__gte-大于等于，__lt-小于，__lte-小于等于
        查询指定某天；类似的还有：__year-年，__month-月，__day-日，__week-周，__week_day-星期几，__quarter-季度，
        __time-时间，__hour-小时，__minute-分钟，__second-秒
        或者搭配__gte，如__year__gte=2024
        """
        user = LearningUser.objects.filter(createtime__date=date(2024, 7, 5))
    
        # 如果设置TIME_ZONE = False，则无需make_aware
        start = make_aware(datetime.now().replace(year=2024, month=7, day=1))
        end = make_aware(datetime(year=2024, month=7, day=5, hour=23, minute=59, second=59))
        user = LearningUser.objects.filter(createtime__range=(start, end))  # between ... and ...
    
        # 关联查询
        user = LearningUser.objects.filter(articles__title__contains='测试')
    
        for u in user:
            print(u.username, u.state, u.email, u.createtime)
    
        return HttpResponse(user.query)  # 打印执行的SQL
    ```
    
### 🚁 聚合与分组

* 仅聚合：`Model.objects.aggregate()`
* 聚合并分组：`Model.objects.annotate()`

=== "aggregate"

    ```python
    def aggregate_example(request):
        # res = LearningUser.objects.aggregate(models.Count('username', distinct=True))
        # 其他聚合函数：Avg、Max、Min、Sum等
        # select count(username) from LearningUser where username='whm';
        res = LearningUser.objects.filter(username='whm').aggregate(models.Count('username'))
        return HttpResponse(res['username__count'])
    ```

=== "annotate"

    ```python
    def group_by_example(request):
        # select username, sum(id) total from LearningUser group by username;
        res = LearningUser.objects.annotate(total=models.Sum('id')).values("username", "total")
        return HttpResponse(res)
    ```

### 🚁 Q表达式

搭配filter()使用，支持逻辑运算符“与”、“或”、“非”，以进行复合查询。

```python
def q_expression_example(request):
    # &-与 |-或 ~-非
    user = LearningUser.objects.filter(models.Q(username='whm') | models.Q(username='whm2'))
    tmp = ''.join([f"<p>{u.username}, {u.state}, {u.email}, {u.createtime}</p>" for u in user])
    return HttpResponse(tmp)
```

## 📌 F表达式

* 通过F表达式，在数据库层面执行字段的计算、更新或比较，而无需将数据加载到Python内存中。
* 搭配update()使用如`update(stock=F('stock') - quantity)`，确保原子性，避免竞态条件。

=== "批量拼接字符串"

    ```python
    def f_expression_example(request):
        # author_id = LearningUser.objects.get(username='whm').id
        # article = Article.objects.filter(author_id=author_id)
    
        # 以上可简化为__语法引用外键
        # article = Article.objects.filter(author__username='whm')
    
        # 优化查询性能用select_related()，预先从数据库中获取关联表的数据，以减少数据库查询的次数，从而提高查询性能
        article = Article.objects.select_related('author').filter(author__username='whm')
    
        # 使用F表达式批量拼接字符串
        article.update(content=Concat(models.F('content'), models.Value('F表达式批量修改')))
        tmp = ''.join([f"<p>标题：{ua.title}， 内容：{ua.content}， 作者：{ua.author.username}</p>" for ua in article])
    
        # F表达式也可放在filter，如filter(name=F("username"))，判断俩字段内容是否一致
        return HttpResponse(tmp)
    ```

=== "字段比较"

    ```python
    # 找到所有column1比column2大的记录
    results = Model.objects.filter(column1__gt=F('column2'))
    ```

=== "改变输出字段类型"
    
    ```python
    from django.db.models import F, DecimalField
    # 相乘可能超长
    total_price = Model.objects.aggregate(total=Sum(F('price') * F('quantity'), output_field=DecimalField()))
    ```

## 📌 表单

Form的字段类型基本与Model一致，但有些属性不相同。

=== "form.py"

    ```python
    class RegisterForm(forms.Form):
        username = forms.CharField(label="用户名")
        password = forms.CharField(label="密码", min_length=6, error_messages={"min_length": "密码不能少于6位"},
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
        confirm_pw = forms.CharField(label="确认密码", min_length=6, error_messages={"min_length": "密码不能少于6位"},
                                     widget=forms.PasswordInput(attrs={'class': 'form-control'}))
        email = forms.EmailField(label="邮箱")
        """
        其他字段类型还有FloatField、IntegerField、DecimalField、FileField、ImageField、URLField、IPAddressField、SlugField、ChoiceField、
        MultipleChoiceField、ModelChoiceField、ModelMultipleChoiceField、FilePathField、DateField、DateTimeField、TimeField、
        DurationField、GenericIPAddressField、SplitDateTimeField、ComboField、MultiValueField、IPAddressField、FileField、ImageField、URLField
        """
        # 使用正则验证
        phone = forms.CharField(label="手机号", validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式不正确')])
    
        # 针对某个字段自定义验证
        def clean_phone(self):
            phone = self.cleaned_data.get("phone")
            # 伪代码，数据库重复校验
            if phone == "12345678910":
                raise forms.ValidationError("手机号重复")
            return phone
    
        # 对多个字段进行校验
        def clean(self):
            cleaned_data = super().clean()
            pwd1 = cleaned_data.get("password")
            pwd2 = cleaned_data.get("confirm_pw")
            if pwd1 != pwd2:
                raise forms.ValidationError("两次密码不一致")
            return cleaned_data
    ```


=== "views.py"

    ```python
    @require_http_methods(['GET', 'POST'])
    def form_example(request):
        if request.method == 'GET':
            form = RegisterForm()
            return render(request, 'form_example.html', context={'form': form})
        else:
            form = RegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                return HttpResponse(f"用户名：{username}， 密码：{password}， 邮箱：{email}， 手机号：{phone}")
            else:
                # form.errors 带html标签
                # form.errors.get_json_data() 转为字典，json.loads()
                # form.errors.as_json() 转为字符串，json.dumps()
                errors = form.errors.get_json_data()
                errormsg = ";".join([f"{key}: {value[0].get('message')}" for key, value in errors.items()])
                return HttpResponse('校验不通过，' + errormsg)
    ```


=== "form_example.html"

    ```html
    <form action="" method="POST">
        {{ form }}
        {% csrf_token %} <!-- 403 csrf验证失败 -->
        <input type="submit" value="提交">
    </form>
    ```

### 🚁 ModelForm

通过继承ModelForm，实现表单与模型之间的自动绑定。

```python
class RegisterModelForm(forms.ModelForm):
    class Meta:
        model = LearningUser
        # 继承所有字段
        # fields = "__all__"
        # 只需要部分字段
        fields = ["username", "password", "email"]
        # 或者忽略部分字段
        exclude = ["createtime"]
        # 指定错误提示
        error_messages = {
            "username": {
                "required": "用户名不能为空"
            }
        }
```

---

参考资料：

1.[完整项目代码](https://gitee.com/Jork-S-B/django-practice)