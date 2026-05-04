python本身没有项目管理的模块，而通过`pip install`安装依赖时，会将依赖安装到python全局路径/安装路径下，多项目运作时存在运行环境问题。

## 📌 早期项目管理

虚拟环境 + requirements.txt

`pip freeze > requirements.txt`
通过将项目中已安装的依赖，导出为txt文件。

`pip install -r requirements.txt`
协作者执行该命令，以同步环境依赖。

### 🚁 创建并激活虚拟环境

```shell
python -m venv .venv
source .venv/bin/activate
```

而在pycharm等ide中，在设置-解释器中，添加虚拟环境后会在对应目录下生成`.venv`目录，也不用再手动激活虚拟环境。

---

通过虚拟环境隔离依赖，解决多项目运行环境问题。

但`pip install`这种方式，会将直接依赖、相关的间接依赖都安装。uninstall时，间接依赖又卸不干净。

## 📌 pyproject.toml

`pyproject.toml`是官方指定的统一的配置文件。在其成为标准前，不同的开发工具通常有各自的配置文件，如`pytest.ini`、`mypy.ini`（静态类型检查）。

如今python主流工具都支持`pyproject.toml`，同时也是`requirements.txt`更好的项目管理方式。但又带来新的问题：第三方库的版本需要手动查找。

=== "pytest.ini"

    ```ini
    [pytest]
    testpaths = tests
    
    ```

=== "mypy.ini"

    ```ini
    [mypy]
    exclude = build/
    
    ```

=== "pyproject.toml"

    ```ini
    # 将pytest、mypy等配置统一管理
    [project]
    name = "proj"
    version = "0.1.0"
    dependencies = [
        # 第三方库列表，如
        "Flask==3.1.1"
    ]
    
    [tool.mypy]
    exclude = ["build/"]
    
    [tool.pytest.ini_options]
    testpaths = ["tests"]
    
    ```

## 📌 uv

poetry、pdm、uv，底层实际还是使用pip、venv，但提供了更加用户友好的接口。

### 核心命令对比

| 操作 | pip 传统方式 | uv 正确方式 | 说明 |
|------|-------------|------------|------|
| 初始化项目 | 无 | `uv init` | 创建 pyproject.toml |
| 创建虚拟环境 | 自动创建 | `python -m venv .venv` ||
| 激活虚拟环境 | 自动激活 | `source .venv/bin/activate` ||
| 添加依赖 | 手动编辑 requirements.txt | `uv add <package>` | 自动记录到 pyproject.toml |
| 添加开发依赖 | 手动编辑 requirements-dev.txt | `uv add --dev <package>` | 自动记录到 dev 依赖 |
| 同步依赖 | `pip install -r requirements.txt` | `uv sync` | 根据 pyproject.toml 安装 |
| 运行代码 | `python main.py` | `uv run main.py` | 在虚拟环境中执行 |
| 移除依赖 | 手动编辑 requirements.txt | `uv remove <package>` | 从项目中移除 |
| 查看依赖树 | `pipdeptree` | `uv tree` | 显示依赖关系 |
| 更新锁定 | 无 | `uv lock --upgrade` | 更新依赖版本 |

=== "1.venv搭配pyproject.toml"

    ```shell
    python -m venv .venv
    # 针对shell
    source .venv/Scripts/activate
    # 针对powershell
    .venv/Scripts/activate
    edit pyproject.toml
    pip install -e .
    
    ```

=== "2.直接使用uv"

    ```shell
    # 初始化项目，创建基本的项目结构，包括 pyproject.toml 文件。
    uv init
    
    # 确保已经有初始化的pyproject.toml
    # 添加依赖如flask
    uv add flask
    
    # 协作者同步依赖
    uv sync
    
    # 运行代码
    uv run main.py
    
    # 或者按以下步骤
    # 激活虚拟环境，用传统的python xx.py运行代码
    source .venv/bin/activate
    python main.py
    ```
