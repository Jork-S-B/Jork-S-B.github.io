## LLM应用开发框架

- LangChain/LangGraph: 类似dify，通⽤的 LLM 编排与集成框架，擅⻓“⼯具调⽤/⼯作流/代理”的落地与⽣产化。
- LlamaIndex: 以“数据到智能”为核⼼的 RAG （检索增强⽣成）平台，擅⻓数据接⼊、索引、检索与查询引擎。
- AutoGen: 多智能体协作框架，擅⻓复杂、开放式任务的“角色分工+对话式协作”。

## ui_autotest_agent

基于AutoGen的多智能体协作平台

=== "基本工作流"

    ```text
    用户请求 (FastAPI) 
        ↓
    编排服务 (Orchestrator)
        ↓
    智能体工厂 (AgentFactory)
        ↓
    智能体执行 (AutoGen Runtime)
        ↓
    流式响应收集 (Collector)
        ↓
    SSE 推送给前端
    ```

=== "完整数据流"

```text
    1. 用户触发操作
        ↓
    2. 前端调用 API (POST /upload-and-analyze)
        ↓
    3. 后端创建会话和消息队列
        ↓
    4. 后端启动后台任务 (process_page_analysis_task)
        ↓
    5. 前端建立 SSE 连接 (GET /stream/{session_id})
        ↓
    6. EventSourceResponse 开始推送事件流
        ↓
    7. 后台任务调用智能体 (AutoGen)
        ↓
    8. 智能体产生消息 → message_callback
        ↓
    9. message_callback → message_queue.put()
        ↓
    10. event_generator 从队列获取消息
        ↓
    11. yield SSE 格式消息 → 客户端
        ↓
    12. 前端 EventSource 监听事件
        ↓
    13. 更新 React 状态 → UI 渲染
        ↓
    14. 显示实时进度和思考链
```

### AutoGen核心概念

- Agent: 核心执行单元，每个智能体都应具备: 唯一标识、订阅主题、消息处理函数。
- Runtime: 智能体的运行时执行环境，负责管理智能体的生命周期、处理消息的路由与分发、协调智能体间的通信。
- Topic: 消息路由的机制，每个智能体都可以订阅主题、发布消息，也是智能体间的通信机制。
- Message: 智能体间通信的载体。

智能体设计准则

- 单一职责
- 消息类型明确
- 具备错误处理

??? note "base_url"

    OpenAI 或 AutoGen ，只需提供 base_url ，SDK 会自动追加 /chat/completions

    - 完整url: `https://ark.cn-beijing.volces.com/api/v3/chat/completions`
    - 配置: `UI_TARS_BASE_URL: str = "https://ark.cn-beijing.volces.com/api/v3"`

### MidScene.js

角色: 基于 AI 的 UI 元素识别和操作库，集成在 Playwright 之上。

作用: 基于视觉语言模型（VLM）的 Web 自动化测试框架，它的核心作用是用自然语言驱动浏览器操作。

如何协同：`MidScene.js` -> 视觉模型 -> 返回大致坐标或选择器 -> `MidScene.js` 驱动 Playwright 执行浏览器操作。

另外，无python版本的sdk。

??? note "大模型分类"

    - 通用大模型/文本大模型，如`Deepseek`
    - 视觉语言模型（VLM），如`Qwen-VL`，阿里云通义千问视觉模型，可以以图像、文本、检测框作为输入，并以文本和检测框作为输出。
    - 专业大模型，如`UI-TARS`，微软开源的针对GUI/UI自动化训练的模型。

### SSE

Server-Sent Events ， HTML5 标准，允许服务器向浏览器推送实时事件流，类似大模型的流式输出。

核心特点

- 单向通信: 服务器 → 客户端（浏览器）
- 长连接: 基于 HTTP 的持久连接
- 自动重连: 客户端断开后自动重连
- 事件类型: 支持自定义事件类型
- 简单轻量: 比 WebSocket 更简单易用


??? note "SSE vs WebSocket vs HTTP 轮询"

    | 特性 | SSE | WebSocket | HTTP 轮询 |
    |------|-----|-----------|----------|
    | 通信方向 | 单向 (服务器→客户端) | 双向 | 单向 (客户端→服务器) |
    | 协议 | HTTP/HTTPS | WebSocket (ws://) | HTTP/HTTPS |
    | 实时性 | 实时推送 | 实时推送 | 延迟高 |
    | 复杂度 | 简单 | 中等 | 简单 |
    | 适用场景 | 实时通知、进度推送 | 聊天、游戏 | 低频更新 |

标准消息格式

```
event: <事件类型>
id: <消息 ID>
data: <JSON 数据>

```
