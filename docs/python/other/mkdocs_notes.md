# mkdocs使用记录

mkdocs：基于Python的文档生成工具，用于快速、简单的生成网站。

---

### mkdocs常用命令

|            命令             | 说明                          |
|:-------------------------:|:----------------------------|
|       `mkdocs new`        | 生成站点目录及配置文件；如已经有相同的目录可以不用执行 |
| `mkdocs serve -a ip:port` | 在本地运行，预览生成的html；默认8000端口    |
|      `mkdocs build`       | md转html文件，生成的文件在./site目录下   |

!!! tip

    需要先cd至存放mkdocs.yml的目录

---

### Material for MkDocs

[点击这里跳转至官方使用文档](https://squidfunk.github.io/mkdocs-material/getting-started/)

mkcocs-material是mkdocs的主题之一 ，在mkdocs.yml中配置。下列是可能有用的组件示例。

\# todo，mkdocs-material可以直接通过Github action部署到github page。

---

### 🚁 带tab页的代码块

=== "预览"

    ``` c++
    #include <iostream>

    int main(void) {
      std::cout << "Hello world!" << std::endl;
      return 0;
    }
    ```

=== "mkdocs.yml配置"

    ```yaml
    markdown_extensions:
        # 可切换tab页的代码块扩展
        - pymdownx.superfences
        - pymdownx.tabbed:
            alternate_style: true
    ```

=== "code.md"

    ```
    === "Hello world!"

        ``` c++
        #include <iostream>
    
        int main(void) {
          std::cout << "Hello world!" << std::endl;
          return 0;
        }
        ```
    ```

---

### 🚁 带tab页的提示框

!!! example "示例"

    === "示例1-无序列表"

        ``` markdown
        * Sed sagittis eleifend rutrum
        * Donec vitae suscipit est
        * Nulla tempor lobortis orci
        ```

    === "示例2-无序列表"

        ``` markdown
        1. Sed sagittis eleifend rutrum
        2. Donec vitae suscipit est
        3. Nulla tempor lobortis orci
        ```

    === "mkdocs.yml配置"

        ```yaml
        markdown_extensions:
            # 可切换tab页的代码块扩展
            - pymdownx.superfences
            - pymdownx.tabbed:
                alternate_style: true
            # 提示框扩展
            - admonition
            - pymdownx.details
            - pymdownx.superfences
        ```

    === "code.md"

        ```
        !!! example "示例"

            === "示例1-无序列表"
        
                ``` markdown
                * Sed sagittis eleifend rutrum
                * Donec vitae suscipit est
                * Nulla tempor lobortis orci
                ```
        
            === "示例2-无序列表"
        
                ``` markdown
                1. Sed sagittis eleifend rutrum
                2. Donec vitae suscipit est
                3. Nulla tempor lobortis orci
                ```
        ```

---

### 🚁 默认折叠展示的提示框

??? question "示例"

    === "示例"

        提示框类型还有note、tip、success、fail、question、warning等。[参考链接](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#admonition-icons-fontawesome)
         
    === "code.md"

        ```
        ??? question

            提示框类型还有note、tip、success、fail、question、warning等。
        ```

---

### 🚁 正文中使用emoji表情

=== "示例"

    :heart:
    :smile:
    :laughing:
    :blush:
    :smiley:
    :relaxed:
    :smirk:
    :heart_eyes:
    :kissing_heart:
    :kissing_closed_eyes:
    :flushed:
    :relieved:
    :satisfied:
    :grin:
    :wink:

    [官网使用文档](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/#search)
    提供了图标、emoji表情的搜索功能

=== "mkdocs.yml配置"

    ```yaml
    markdown_extensions:
    # emoji等图标的扩展
    - attr_list
    - pymdownx.emoji:
        emoji_index: !!python/name:material.extensions.emoji.twemoji
        emoji_generator: !!python/name:material.extensions.emoji.to_svg
    ```

=== "code.md"

    ```markdown
    :heart:
    :smile:
    :laughing:
    :blush:
    :smiley:
    :relaxed:
    :smirk:
    :heart_eyes:
    :kissing_heart:
    :kissing_closed_eyes:
    :flushed:
    :relieved:
    :satisfied:
    :grin:
    :wink:
    ```

---

### 🚁 本文使用的配置

=== "mkdocs.yaml"

    ```yaml
    site_name: 站点名称
    site_url: 站点 URL 链接
    site_author: 站点作者
    site_description: 站点描述
    
    nav: # 导航栏菜单配置举例
      - Home: index.md  # 文件实际位置为./docs/index.md
      - User Guide:
          - Writing your docs: user-guide/writing-your-docs.md
          - Styling your docs: user-guide/styling-your-docs.md
    
    # 搜索栏右侧git链接
    repo_url: https://gitee.com/Jork-S-B/myblog
    repo_name: 'mypage'
    
    theme:
        # favicon: logo.png  # 网站logo，默认从./docs/logo.png读取
        icon:
            logo: fontawesome/solid/face-smile-wink  # site_name左侧图标
            repo: fontawesome/brands/git-alt  # git链接图标
        name: 'material'  # 设置mkdocs-material主题，需要先pip install mkdocs-material
        language: zh
        features:
            - navigation.footer  # 设置上一页和下一页
            - navigation.top  # 一键回顶部
            - navigation.tabs  # 顶部显示导航顶层nav
            - navigation.instant  # 点击内部链接时，不用全部刷新页面
            - content.code.copy  # 代码块复制按钮
        palette:
            # 切换样式方案及按钮
            - media: "(prefers-color-scheme: light)"
              scheme: default
              primary: teal
              toggle:
                icon: material/lightbulb
                name: 切换至深色模式
    
            - media: "(prefers-color-scheme: dark)"
              scheme: slate
              primary: black
              toggle:
                icon: material/lightbulb-outline
                name: 切换至浅色模式
    
    extra_css:
      - stylesheets/extra.css  # 自定义css文件
    
    markdown_extensions:
        # emoji等图标的扩展
        - attr_list
        - pymdownx.emoji:
            emoji_index: !!python/name:material.extensions.emoji.twemoji
            emoji_generator: !!python/name:material.extensions.emoji.to_svg
        # 可切换tab页的代码块扩展
        - pymdownx.superfences
        - pymdownx.tabbed:
            alternate_style: true
        # 提示框扩展
        - admonition
        - pymdownx.details
        - pymdownx.superfences
        # 表格扩展
        - tables
    
    plugins:
        # 图片放大插件，需要先pip install mkdocs-glightbox
        - glightbox
        - search:
        # 中文搜索插件，需要pip install jieba
            separator: '[\s\u200b\-]'
            lang:
              - en  # 英文搜索时按单词搜
              - zh  # 搜中文时输入关键字后删掉1位能查到
    ```
=== "stylesheets/extra.css"

    ```css
    .md-grid {
      max-width: 1555px;
    }
    ```

---
最后更新: 2024/01/31 19:54