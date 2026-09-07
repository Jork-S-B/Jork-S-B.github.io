## 1.模型选择

客观数据

[DeepSWE](https://deepswe.datacurve.ai/): 衡量AI解决真实软件工程问题的基准测试。

DeepSWE score, 右上角区间内的模型most efficient

---

[DesignArena](https://www.designarena.ai/leaderboard/code): 由社区用户盲测的AI设计排行榜，包括h5、网站设计、游戏UI设计等。

代码分类 Preference vs Speed    
Top-left quadrant shows models with low cost and high ratings

---

[Artificial Analysis](https://artificialanalysis.ai/?cost=intelligence-vs-cost-per-task)

Intelligence Index vs. Cost per Intelligence Index Task  
Artificial Analysis Intelligence Index · Weighted average cost (USD) per Artificial Analysis Intelligence Index task  
Most attractive quadrant，区间内的模型更具性价比。

---

202609: 

- 主力编码模型: GLM 5.3 Flash
- 顾问模型(WebUI设计规范): KIMI K3

## 2.编码agent选型

分类，自动化程度由低到高。

缺少类似大模型的Benchmark客观数据，更多的是个人主观评价。

### 2.1.人机协作编码agent

ide/编辑器 + agent插件，常见的如: Cursor、Trae、Kiro

基本都是vscode套壳，其中Zed比较特殊，由Rust原生打造。

适用场景: 老项目、需要人工介入

### 2.2.ADE

- CLI: Claude Code、Codex Cli、Pi Agent、OpenCode
- GUI：Codex、Deepseek Harness

相较于Claude Code、Codex这种封装好完整Agent Harness的工具，Pi Agent只提供最小核心，Harness交给用户。

DSH也是提供完整Agent Harness，但每个模块都可插播可拼装。

省心选择: GPT套餐 + Codex + Mac

### 2.3.办公Agent

基于Agent包装GUI，常见的如: Workbuddy、TraeWork

### 2.4.智能助理

开箱即用的数字员工，自带预设技能 + 自进化宣传，常见的如: Hermes、小龙虾

这里的自进化，本质还是上下文的记忆工程，短期内确实可以自进化，但上下文的大小、模型的聪明区、模型的注意力机制等限制，东西塞的越多越容易出幻觉。