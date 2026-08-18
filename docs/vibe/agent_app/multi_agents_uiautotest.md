由于AutoGen后续更新倾向微软云服务(Microsoft Azure)生态，多agent协同的应用采用`LangGraph`似乎更合适。

## LangGraph

- 状态`state`: 相当于共享变量
- 边`edges`: 根据当时状态决定下一步，类似流程控制
- 节点`nodes`: 节点对应可执行的方法，用于输入输出、执行代码等

基本结构: 入口 -> 边 -> 节点 -> 条件边 -> 多分支结构 -> end

通过`@tool`被装饰的普通函数，会被转换为`langchain`工具。添加为`Toolnode`后由agent分发调用。

??? note "关于LangGraph引入skill"

    先分类区分本质，使用llm思考本身的skill还是用节点+边；使用`@tool`帮llm完成它做不了的事，如去重、格式转换、上传等。

    用例设计这种本身依赖大模型思考能力的，示例如下

    1. 读spec文档节点
    2. 生成测试设计/测试点提取
    3. 人工复核
    4. 复核不通过，手动修改或根据用户输入意见，回到节点2
    5. 复核通过，进入节点6
    6. 文本用例生成

    关于文本用例不采纳的原因分类

    1. 用例粒度太细，冗余重复-最高频
    2. 部分异常场景不切实际，如网络中断
    3. 用例步骤描述笼统：需测试规范、输入内容优化
    4. US内容描述不清晰：需手动调整内容，如表格转markdown 
    5. 工具能力不足，缺多模态模型，无法理解图片

## Playwright

目标页url传给llm，headless模式启动Playwright进行扫描。

AOM降噪 + 语义链: Accessibility Object Model (AOM) 为主（返回结构化信息），DOM树为辅。

- Accessibility Tree，无障碍树，F12-elements-Accessibility选项卡
- 属性DOM树扫描

??? "调试"

    - `await self.page.pause()`  # 通过Playwright方法，打开 Inspector 窗口
    - vscode软件的调试

        1. launch.json: `uv run test`相关命令交给ai生成该文件
        2. Ctrl+Shift+P，输入 `Python: Select Interpreter` ，选择项目虚拟环境
        3. 设置断点，启动调试

    - Trace Viewer

        1. 启用tracing: `pytest --tracing=retain-on-failure`，或者pytest.ini中配置 `addopts = --tracing=retain-on-failure`
        2. `playwright show-trace {test-results/<test-name>-<timestamp>/trace}.zip`

## 后续流程

1. 通过上述步骤，获取目标元素定位表达式。
2. 基于已有的ui自动化代码示例(PageObject + testcases)，让agent学习并生成。
3. 自愈功能，通过装饰器实现。当目标元素定位表达式变化，agent会尝试更新对应的po代码。

## 已知问题

- 获取目标元素定位表达式，效果不理想。项目复杂度越来越高，ai开始根据UI框架（如elementui、ant-design等）写定制化的定位表达式，偏离原本“结构关系锚定+语义化”的设计初衷。
- ai生成的用例方法名不合规范，中英掺杂；当时采用最直接的方法: 通过硬编码字典进行映射。
- ui自动化agent应用的通病，简单的增删改通过count断言的，但复杂业务、中间件检查相关的断言如何生成

最终沉淀: [📌 驱动ai进行ui自动化](/python/autotest/selenium/#aiui)

## 通过skill实现自动化

多个skill协同，人工把控输入输出的质量，达到最终目标。

--- 

todo: 以下内容需进一步补充

### 用例设计skill

1. US转spec文档，交给ai提取测试功能点
2. 根据测试设计方法、测试用例规范，结合人工复核的测试功能点，生成文本用例

### api自动化生成skill

1. 基于接口文档，根据功能点提取、风险识别、设计方法生成测试设计
2. 人工审查后，结合测试规范生成文本用例
3. 让ai学习示例代码，用例转代码

### ui自动化生成skill

1. 根据页面url识别元素生成测试设计
2. 人工审查后，根据测试设计解析元素、场景、数据，生成文本用例和po代码
3. 生成代码及测试数据.json
