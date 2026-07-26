# 目录设计

```text
apiauto
|-api  # 继承基类，根据项目需求定义接口类。
├─base  # 通用基类，继承为项目基类，配置域名或自定义功能。
├─common  # 公共方法，包括鉴权、requests、断言、日志清理等。
├─config  # 配置管理，`test.yaml/sit.yaml`，存数据库配置、项目对应的域名、管理员账号等，与`fixture`、`pytest_addoption`搭配实现bash命令快捷多环境切换。
├─report  # 报告与集成
├─testdata  # yaml/json/excel格式，支持参数化。
├─testcases  # 测试用例目录
└─utils  # 工具封装，包括日志记录、db、redis、yaml/json/excel读写、faker仿真造数、变量替换等。
```

## common

### 1.鉴权

通过第三方OCR平台（如超级鹰）识别验证码

- 单点登录: 返回cookies，适用于跨系统认证
- 普通登录: 返回token字符串，适用于单系统认证
- App登录: app测试环境验证码固定为1

!!! tip "其他方式"

    - 开源OCR: DDDDOCR
    - 验证码存Redis是行业标准，缺OCR能力时，考虑连Redis获取

### 2.requests

- 鉴权注入: 根据登录类型（单点/普通/App登录）获取认证并注入请求头，支持传自定义cookie。
- 请求类型`get/post`封装
- 路由拼接: 域名+url
- 请求前后日志记录
- 响应转换装饰器: 不同响应类型转字典dict

=== "响应转换装饰器"

    ```python
    def reponse_to_dict(func):
        """多响应类型转换"""

        def inner(*args, **kwargs):
            try:
                res: Response = func(*args, **kwargs)
                if res.text.startswith("<?xml"):
                    result = xmltodict.parse(res.text)
                    return result
                elif res.text.startswith("{"):
                    return res.json()
                else:
                    return res.text
            except Exception as e:
                logger.error(f"响应数据类型转换失败，失败原因为{e}")

        return inner
    ```

### 3.断言

- 数据提取: jsonpath/正则表达式

## testcase

测试用例: 数据驱动+参数化，实现测试数据与代码分离。

```python
@pytest.mark.parametrize("handle_order_data,order_type",
    [(OperationFiles.open_json(r"\data\handle_order_wechat"), "wechat"),
        (OperationFiles.open_json(r"\data\handle_order_bank"), "bank"),])
def test_place_order(self, handle_order_data, order_type):
    # 测试用例实现
    response = self.client.post_order(handle_order_data, order_type)
    # 断言
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert response.json()["msg"] == "success"
```

## utils

变量替换，基于`String.Template`的占位符替换实现，可改写成不定参数`**kwargs`的版本。

=== "String.Template"

    ```python
    # -*- coding: utf-8 -*-

    import json
    from string import Template

    def replace_template(dict, context):
        """模版替换"""
        for key in dict.keys():
            target = dict.get(key)
            string = Template(json.dumps(target))
            value = string.substitute(**context)
            obj = json.loads(value)
            dict.update({key: obj})
        return dict


    def replace_template_key(template, key_name, value):
        """
        单个参数模板替换 new_value = replace_template_key(policy_add_data, "today", datetime.datetime.today().date())
        :param template: 原模板信息 字典格式
        :param key_name: 需要替换的参数占位符 例如模板中是： ${name}，这里填入 name 即可
        :param value: 替换占位符的新值
        """

        template_key = f"${{{key_name}}}"
        updated_template = {}

        for k, v in template.items():
            if isinstance(v, str) and key_name in v:
                updated_template[k] = v.replace(template_key, str(value))

            else:
                updated_template[k] = v
        return updated_template

    if __name__ == '__main__':
        # 模版替换示例
        template_dict = {
            "user_info": {
                "name": "${username}",
                "age": "${age}",
                "city": "北京"
            },
            "config": {
                "timeout": "${timeout_value}"
            }
        }

        context = {
            "username": "张三",
            "age": "25",
            "timeout_value": "30"
        }

        result = replace_template(template_dict, context)
        print(result)

        policy_add_data = {
            "policy_name": "测试_${today}",
            "description": "这是关于${today}的测试",
            "value": 100
        }

        result = replace_template_key(policy_add_data, "today", "2024-01-15")
        print(result)

    ```

=== "**kwargs"

    ```python
    # -*- coding: utf-8 -*-

    import json
    from string import Template

    def replace_template2(dict, **kwargs):
        """模版变量替换"""
        for key in dict.keys():
            target = dict.get(key)
            string = Template(json.dumps(target))
            value = string.substitute(**kwargs)
            obj = json.loads(value)
            dict.update({key: obj})
        return dict

    if __name__ == '__main__':
        # 模版替换示例
        template_dict = {
            "user_info": {
                "name": "${username}",
                "age": "${age}",
                "city": "北京"
            },
            "config": {
                "timeout": "${timeout_value}"
            }
        }

        context = {
            "username": "张三",
            "age": "25",
            "timeout_value": "30"
        }

        result = replace_template2(template_dict, **context)
        print(result)

        policy_add_data = {
            "policy_name": "测试_${today}",
            "description": "这是关于${today}的测试",
            "value": 100
        }

        result = replace_template2(policy_add_data, today="2024-01-15")
        print(result)

    ```

## report

=== "allure报告分层"

    ```python
    @allure.epic("XX系统")    # 项目级别
    @allure.feature("XX模块")          # 模块级别
    @allure.story("XX功能")            # 功能级别
    with allure.step("XX步骤"):     # 步骤级别

    ```

# pytest配置与上下文管理

## pytest.ini


pytest常用命令参数

```bash
python testcases\test_project\test_xx_order.py::TestOrderManager  # 常规执行

-s/--capture=no: 输出print的信息
-v/--verbose: 可以输出用例更加详细的执行信息，比如用例所在的文件及用例名称等
--tb=short: 缩短报错回溯信息
-q: 简化输出信息
-m: 运行指定标记的用例集
-k: 根据关键字模糊搜索用例名称
--html=./report/report.html: 生成html报告
--self-contained-html: 所有资源嵌入到单个HTML

```

=== "pytest.ini"

    ```ini
    [pytest]
    filterwarnings =
        ignore::UserWarning  # 忽略告警
    markers = smoke  # 标记冒烟用例
    # addopts = -v -s --html=./report/report.html --self-contained-html  # pytest运行参数也可放在pytest.ini中
    ```        

=== "pyproject.toml"

    ```toml
    [tool.pytest.ini_options]
    filterwarnings = "ignore::UserWarning"
    markers = "smoke"
    addopts = "-v -s --html=./report/report.html --self-contained-html"
    ```        

!!! tip "如何只执行marker用例"

    === "1.标记用例"

        ```python
        import pytest

        @pytest.mark.slow
        def test_long_running():
            # 执行时间较长的测试
            pass

        @pytest.mark.smoke
        def test_critical_function():
            # 验证核心功能的测试
            pass
        ```

    === "2.执行指定标记的用例"

        ```shell
        # `pytest.ini`需注册自定义markers
        pytest -m "slow and smoke"  # 支持 and、or、not 运算符

        ```

## conftest.py

fixture: 定义测试用的共享资源。scope参数值可选（作用域从小到大）：function、class、module、package、session。

### 重试机制

解决异步场景下数据同步延迟

=== "重试机制装饰器"

    ```python
    def retry_on_assertion(max_attempts=5, interval=2):
        """
        重试机制装饰器，用于防止数据同步慢导致断言失败
        使用时to_assert方法的参数-errorMsg不能为空
        :param max_attempts: 最大尝试次数
        :param interval: 重试间隔时间(秒)
        """

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None
                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except AssertionError as e:
                        last_exception = e
                        if attempt < max_attempts - 1:
                            time.sleep(interval)
                        else:
                            raise e
                raise last_exception

            return wrapper

        return decorator
    ```

### 并行执行

采用`--dist loadscope`策略，将同一模块用例分配到同一worker串行执行，避免数据竞争。

??? note "--dist的分发模式"

    | 模式 | 命令示例 | 行为说明 | 适用场景 |
    |:---|:---|:---|:---|
    | **load（默认）** | `pytest -n 4` | 将待测用例随机轮询分配给空闲 worker | 用例间**无任何依赖**，追求最大并行效率 |
    | **loadscope** | `pytest -n auto --dist=loadscope --dist-scope=class` | 按**模块**（函数）或**类**（方法）分组，整组分配给同一 worker | 模块/类级别有 `session`/`module` 级 fixture，需共享资源 |
    | **loadfile** | `pytest -n 4 --dist=loadfile` | 按**测试文件**分组，同一文件的用例在同一个 worker 执行 | 文件内有共享的 fixture 或全局变量 |
    | **loadgroup** | `pytest -n 4 --dist=loadgroup` | 按 `@pytest.mark.xdist_group(name="...")` 标记分组 | 需要**精细控制**哪些用例必须在同一 worker 执行 |

#### 📌 Q1: -s（--capture=no）失效 / 多worker日志交织

-s/--capture=no: 输出print的信息

并行执行时，各worker往终端打印print信息，输出错乱，严重时会导致 Terminal 卡死。

解决方案:

1. 本地调试/并行模式时，使用 -rP 参数替代 -s: `pytest -n 4 -rX`，显示失败用例的print（按 Worker 汇总好再打印）。
2. 按 Worker 进程拆分日志文件

=== "conftest.py"

    ```python
    import os
    import logging
    import pytest
    from datetime import datetime

    # 全局日志格式
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_LEVEL = logging.DEBUG

    def pytest_configure(config):
        # 获取当前 Worker ID (如果是主控则设为'master')
        worker_id = os.environ.get('PYTEST_XDIST_WORKER', 'master')
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # logs/worker_gw0_20260726.log (按日期切分，方便归档)
        date_str = datetime.now().strftime("%Y%m%d")
        log_file = os.path.join(log_dir, f"{worker_id}_{date_str}.log")

        # 配置根日志记录器
        # 清除可能存在的旧 handler，防止重复打印（尤其在并行重启时）
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        
        # 创建文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        
        # 添加至根记录器
        logging.root.addHandler(file_handler)
        logging.root.setLevel(LOG_LEVEL)

        # （可选）关闭 requests 库自带的 urllib3 大量无用 DEBUG 日志，减少干扰
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)

        logging.info(f"=== Worker {worker_id} 日志初始化完成 ===")

        # 执行结果
        # logs/master.log（主控汇总）
        # logs/gw0.log（Worker 0 的详细抓包）
        # logs/gw1.log（Worker 1 的详细抓包）
    ```

=== "base_api.py"

    ```python
    class BaseApi:
        def __init__(self, base_url=None):
            self.base_url = base_url
            # 从根日志记录器获取子记录器，会自动关联到 conftest.py 中配置的 FileHandler
            self.logger = logging.getLogger("api_client")
            self.session = requests.Session()
            
            # 默认请求头（可自定义）
            self.session.headers.update({
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": "AutoTest/1.0"
            })

        ...
        
    ```

#### 📌 Q2: session级fixture被每个worker独立执行

官方的解决方案是使用文件锁(FileLock)进行跨进程通信，确保昂贵的初始化工作（如获取 token、启动服务）只由第一个 worker 执行，其他 worker 等待并读取结果。

=== "conftest.py"

    ```python
    import json
    import pytest
    from filelock import FileLock

    @pytest.fixture(scope="session")
    def shared_resource(tmp_path_factory, worker_id):
        """一个在xdist并行下也只执行一次的fixture"""
        # 1. 非并行模式，直接返回
        if worker_id == "master":
            return produce_expensive_data()

        # 2. 并行模式：所有worker共享的临时目录
        root_tmp_dir = tmp_path_factory.getbasetemp().parent
        # 用这个文件来存放共享数据
        fn = root_tmp_dir / "shared_data.json"

        # 3. 使用文件锁，保证只有一个worker能进入临界区
        with FileLock(str(fn) + ".lock"):
            if fn.is_file():
                # 数据已存在，直接读取
                data = json.loads(fn.read_text())
            else:
                # 第一个worker执行昂贵的初始化
                data = produce_expensive_data()
                fn.write_text(json.dumps(data))
        return data
    ```

!!! tip "注意"

    当同个类用例间需要传递变量（如系统生成的订单号、sku等），可以存入类变量，而非FileLock，实在不行考虑Redis。
    
    - 违背自动化独立性原则：用例之间无依赖，可独立运行。
    - 同属一个业务流e2e场景，应考虑合并为一个用例。

#### 📌 Q3: 并行模式如何实现数据隔离

“数据工厂”的核心是将测试数据的创建逻辑与测试用例本身解耦，并确保每个用例或 worker 获得独立、隔离的数据。

```python
import pytest
from faker import Faker

fake = Faker()

@pytest.fixture
def order_data_factory():
    """返回一个创建订单数据的工厂函数"""
    def _create_order_data(overrides=None):
        # 每次调用都生成全新的、隔离的数据
        data = {
            "order_id": f"ORD_{fake.uuid4()}",  # 全局唯一订单号
            "user_id": fake.random_int(min=1000, max=9999),
            "amount": round(fake.random_number(digits=2), 2),
            "channel": fake.random_element(elements=("WeChat", "TikTop")),
            "timestamp": fake.iso8601()
        }
        if overrides:
            data.update(overrides)
        return data
    return _create_order_data

# ============ 在测试用例中使用 ============
def test_create_order(order_data_factory):
    # 用例1：生成默认数据
    order1 = order_data_factory()
    print(order1)
    # 输出: {'order_id': 'ORD_xxx', 'user_id': 1234, ...}

def test_callback(order_data_factory):
    # 用例2：生成带有特定字段的数据，互不影响
    order2 = order_data_factory(overrides={"channel": "WeChat", "amount": 99.99})
    print(order2)
    # 输出: {'order_id': 'ORD_yyy', 'channel': 'WeChat', 'amount': 99.99, ...}
```

### 多环境切换

基于 pytest_addoption 和 fixture，结合 test.yaml / sit.yaml / prod.yaml 配置文件，通过命令行参数 --apienv 动态切换运行环境。

=== "conftest.py"

    ```python
    # conftest.py
    import pytest
    import yaml
    from pathlib import Path

    GLOBAL_ENV = {"env": "test"}

    def pytest_addoption(parser):
        """添加命令行参数 --apienv"""
        api_group = parser.getgroup("ApiGroup")
        api_group.addoption(
            "--apienv",
            default="test",
            help="设置运行环境: test 或 sit 或 prod"
        # 如果还需要 apiproject，可以继续添加
        # api_group.addoption("--apiproject", default="admin", help="项目名")
        )

    @pytest.fixture(scope="session")
    def pytest_configure(config: Config):
        """拿到命令行参数值"""
        api_env = config.getoption("--apienv")
        # api_project = config.getoption("--apiproject")
        GLOBAL_ENV.update({"env": api_env})
        # GLOBAL_ENV.update({"project": api_project})

    # 后续在基类中读取 GLOBAL_ENV, 根据env参数值获取对应的配置文件

    ```

=== "Jenkinsfile"

    ```
    pipeline {
        agent any

        parameters {
            choice(
                name: 'API_ENV',
                choices: ['test', 'sit', 'prod'],
                description: '选择要运行的测试环境'
            )
            // 可添加其他参数，如项目名
        }

        stages {
            stage('Checkout') {
                steps {
                    checkout scm
                }
            }

            stage('Setup') {
                steps {
                    sh 'pip install -r requirements.txt'  // 安装依赖
                }
            }

            stage('Run Tests') {
                steps {
                    script {
                        // 根据环境决定标记表达式（prod只执行smoke）
                        def markExpr = (params.API_ENV == 'prod') ? 'smoke' : ''
                        // 构建 pytest 命令
                        sh """
                            pytest --apienv=${params.API_ENV} -m "${markExpr}" -s -v --html=./report/report.html --self-contained-html
                            // 并行执行
                            // pytest --apienv=${params.API_ENV} -m "${markExpr}"  -n auto --dist=loadscope --dist-scope=class -rX -v --html=./report/report.html --self-contained-html
                        """
                    }
                }
            }

            stage('Publish Report') {
                steps {
                    publishHTML([
                        reportDir: '.',
                        reportFiles: './report/report.html',
                        reportName: 'Test Report'
                    ])
                    // 或者使用 JUnit 格式
                    // junit './report/test-results.xml'
                }
            }
        }

        post {
            always {
                cleanWs()  // 可选：清理工作空间
            }
        }
    }
    ```


