[Pi Agent解读](https://dg-ai-notes.pages.dev/)

[解读的源码](https://github.com/buchidonggua/dg-ai-notes)

[B站原视频](https://b23.tv/G9WIM75)

垂直智能体: 只干一个领域/场景里的活，并且要把这个场景的**闭环**跑通的 Agent

## ReAct

基于大模型，思考、输出、观察（结果），当输出需要调用工具时，进入下一轮循环；否则运行结束。

Q: 为什么无需调用工具时，就循环结束并输出结果？

A: 在模型的对齐训练阶段，要么调用工具，要么给最终答复。两者都不满足时，在这轮对齐只能得到得分。  
因此久而久之，模型就学会了以上的循环。当然，完成任务不仅包括给最终回复，信息不足时回答不知道不瞎编，也是一种类型。

## 基本骨架

Session, 二开时直接操作的层级。整个生命周期反复的三个方法: 

- prompt(消息): 给 Agent 发消息（用户提示词），触发处理
- subscribe(回调): 订阅事件，Agent 处理时的每一步（吐字、调工具、结束）进行监听
- dispose(): 任务结束或异常终端，释放资源

Runtime, createAgentSession 启动时加载的四个组件: 

- ModelRuntime: 调用的大模型配置
- ResourceLoader: 加载资源，包括系统提示词、扩展、skills、AGENTS.md
- SessionManager: 对话存哪、怎么存（默认存本地）
- SettingsManager: 全局配置，包括重试次数、上下文压缩、默认模型等

Tool工具层，读写文件、查数据库等，工具来源包括: 

- 内置默认: read/bash/edit/write, 另有 grep/find/ls 内置但不默认启用
- customTools: createAgentSession({ customTools: [...] })
- 扩展注册: 在扩展里 pi.registerTool 注册

## 事件监听

- pi.on(eventName, handler): 写在扩展里。能听到全部事件，而且能动手干预（拦截、改数据）。
- session.subscribe(handler): 写在外部宿主（你的脚本、路由）里。能听到大部分事件，但只能看，不能改。

{todo}


## Agent封装为服务

{todo}

---

## 环境准备

[Pi Agent 源码](https://github.com/earendil-works/pi)

[Pi Agent 安装并接入火山引擎](https://console.volcengine.com/ark/region:cn-beijing/docs/82379/2666476?lang=zh)

```powershell
# 查看系统架构: amd64 或 arm64
$env:PROCESSOR_ARCHITECTURE

```
