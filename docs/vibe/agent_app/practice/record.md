使用的skill: [sdd_skill](/vibe/sdd/sdd_skill)

## 1.初始化

```bash
# 仓库初始化
/setup-matt-pocock-skills

# 选择仓库管理方式: Local markdown
```

??? tip "git代码提交规范"

    - feat: feature，代表新功能
    - fix: 修复bug
    - chore: 杂务，如修改readme、skill等

    其他的还有

    - docs
    - style
    - refactor: 代码重构
    - test

## 2.可行性分析

Feasibility Analysis

以`/grill-me`为主, 使用时可在提示词中明确本次讨论的范围/目的，防止无休止讨论。同时在问题跑偏时，及时介入纠正。

* 产物: FSR-Feasibility Study Report，可行性研究报告

## 3.需求分析

Requirements Analysis

- 前期不用定太细，有些需求是边做边浮现出来的。
- 需求逐条评审

* 产物: PRD-Product Requirements Document，产品需求文档(或者SRS-Software Requirements Specification, 软件需求规格说明书)

## 3.1.竞品分析&设计文档

让大模型调研类似的产品，根据需求做调整

* 产物: 游戏设计文档-gdd，或者单纯就设计文档

## 4.架构设计&技术选型

本质给ai搭建一个良好的反馈回路(思考、执行、反馈的循环)，目前效率低的点是工具调用、跑代码、执行命令的地方，因此从技术选型的方向考虑。

另外，ai的单元测试覆盖率不可信，引入`突变测试`(运算符取反，预期会有错误，否则说明测试质量不高)，尤其在项目的圈复杂度快速膨胀的时候。

- 架构设计、技术选型的提示词加入"AI First 技术栈"，效果更好些；否则通常是通用方案。
- 突变测试通过**定时任务**运行，不宜放在反馈回路中。js项目的突变测试参考`stryker.js`
- `dependcy-cruiser`，画模块内依赖关系的开源项目。ai持续进化的背景下，细节可以少抓，但顶层架构的方向还是需把握的。

* 产物: 包含架构设计、技术选型的概要设计文档

## 5.清除迷雾

### 5.1.wayfinder拆工单

具体实现方案有迷雾，想边做边看效果时使用。产出: 决策地图 + tickets(包括依赖、优先级等)，再逐项细分进行grill, research 或 prototype

- 可以让ai梳理wayfinder的目标，前提清除迷雾为主，不让ai自由发挥。目标不要定太远，决策不对就及时调整。
- 要求输出: 可选目标的依赖关系图 DAG
- tickets任务产出的新的上下文如何管理: 每个ticket或任务，控制在模型的聪明区内

* 产物: 各种类型的工单

!!! note "上下文管理"

    - 继续对话，在聪明区内、下一轮预计不超出则继续
    - /new，当上下文没用，或上下文内容有错误则新开窗口
    - /compact，在当前上下文窗口压缩，但压缩后恢复到能继续工作，可能模型还得research
    - /handoff，当前上下文压缩后持久化为文件，可交给另一个模型

### 5.2.搭配subagent清工单

Pi Agent默认无子agent功能，通过扩展来实现该功能。

https://pi.dev/packages/pi-subagents-lite

包含2个子agent: 

- general: 通用任务
- explore: 探索任务，需要上下文较大的苦力模型

搭配`mattpocock skills`使用时，还需**代码review** agent。LLM-as-Judge，模型配置需要使用不同厂商的LLM，否则通过率容易虚高。

```
帮我配置一个 review agent https://pi.dev/packages/pi-subagents-lite 用于 skill: code-review
调用时机: 不要修改skill，而在agent.md中说明调用时机。
另外，后续`research`任务调用 explore 子agent。

```

* 产物: 原工单补充answer

后续引入`codegraph`，agent.md长度估计不短，需要通过`/writing-for-agent`精简

## 6.骨架搭建

`/grill-with-docs`，在模型聪明区(1m上下文，聪明区约200k)能理清思路时使用

```
/grill-with-docs 确认xx文档中的工具链可行性，完成仓库骨架搭建（可编译运行，且写测试用例跑通，提供可手动执行的cli命令）。
```

1. 搭配`/to-spec`，产出adr文档
2. 搭配`/to-tickets`，产出可验收的工单，需关注工单切分的粒度。
3. 搭配`/implement`，每个工单编码并人工验收效果；或者`/implement-spec`，所有工单完成后再验收。

* 产物: 可编译运行的代码脚手架

## 7.方向把控

模型反讲&进展跟踪

依旧细节少抓，但把控方向。随着大模型上下文的增长，我们心里需要有大概的锚点，防止模型跑偏带来的修复成本。

```
根据 fsr.md 里程碑，然后 read scratch 目录下已经完成的内容，帮我画图: 从目前到里程碑，中间还有哪些目标节点的DAG依赖图
要求: 按 /ask-matt 里的描述，按 wayfinder, grill-with-docs, to-spec 的粒度拆分，且标注应使用哪个对应的skill推进目标

```