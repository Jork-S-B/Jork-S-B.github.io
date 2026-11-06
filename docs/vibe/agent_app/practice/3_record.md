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

!!! note "反馈回路/反馈循环的设计"

    1. agent内部层面: 思考、执行、观察
    2. 单元测试/调试层面: 调试结果回传，修正在运行，配合有界重试
    3. 突变测试+定时任务，不宜放在反馈回路中；那人工定期地把报错批量交给ai处理？

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
- explore: 探索任务，优选上下文空间较大、成本低的苦力模型即可

搭配`mattpocock skills`使用时，还需**代码review** agent。LLM-as-Judge，模型配置需要使用不同厂商的LLM，否则通过率容易虚高。

```
帮我配置一个 review agent；参考: https://pi.dev/packages/pi-subagents-lite 
用于 skill: code-review，不要修改skill.md，而在agent.md中说明调用时机。

```

另外，后续`research`任务调用 explore 子agent。

* 产物: 原工单补充answer

后续引入`codegraph`，agent.md长度估计不短，超过**100行**建议通过`/writing-for-agent`（也是matt-pocock的skill）重构

## 6.骨架搭建

`/grill-with-docs`，在模型聪明区(1m上下文，聪明区约200k，也有说256k-来自openai的文章)能理清思路时使用

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

* 产物: mermaid格式的dag依赖图

### research任务

- 大模型的上下文管理和注意力机制尤为关键，冗余的上下文会让模型变笨；还有，大模型的注意力呈U型，即首尾上下文的权重比较大。
- 探索任务的上下文开销占用都会比较大，因此需要用 subagent 去探索，把有效的信息给到主 Agent，避免上下文过长。
- codegraph mcp，相比ai编程工具常规的grep/read，反复搜代码仓更高效。

```
同样修改agent.md: research/探索任务后续都采用 subagent + codegraph mcp 进行，尤其针对 /implement 、 /code-review
```

## 8.阶段总结

### 8.1.git commit清理与改造

清理以确保给ai更好的生成环境、重构以保证代码质量。

改造`/implement`涉及分支管理的内容

- ticket - 在worktree管理，单次提交可包括多个工单，工单拆细是为了更好的利用模型聪明区
- spec - 对应feature分支
- 个人功能分支先 `rebase` main 跟紧主干（修改合并历史），合并 PR 时选择 `Squash` 压成一个提交进主分支。
- 不必合并前检查，提示词约束即可，避免拖慢反馈循环，写入`agent.md`。

整理当前分支为主分支

- commit 数较多，按 pr 粒度合并处理，通过 subagent 串行执行。
- 搭配`/writing-for-agent`，提交信息是写给 agent 看的
- main分支设置为保护分支，防止直接合并。

!!! note "Harness护栏"

    [Harness Engineering](https://www.runoob.com/ai-agent/harness-engineering.html)

    整个实操过程，本质是搭建Harness护栏。

    1. SDD-规格驱动开发，ai思考+人工审查定好规格，包括设计、技术架构等，才有后续的开发。
    2. 开发过程中的反馈循环，agent层面的审查/评测+反馈，以及人工层面的验收、方向把控。
    3. 上下文工程，包括仓库内部上下文的管理、agent单次任务上下文的管理；避免agent.md过长，而是提供一个稳定、小巧的入口点，让ai按需读取。
    4. 熵管理-垃圾回收，定期扫描偏差、更新质量等级、发起针对性重构 PR。

### 8.2.文档清理

当前阶段的SDD，会把规格文档保留为业务资产；但对于 Ai First **个人**开发场景，代码才是唯一真源，规格文档、注释可能反而是干扰（尤其随着时间推移）。

- adr 保留，决策、意图与架构等顶层设计要保留（在代码中无法探索到），并时常维护。
- spec、ticket 细节文档清理掉，不重复维护。
- 调研、调试时的临时原型、脚本等中间产物，无长期价值。

文档清理这一步需拆分任务，读文档内容的任务占用模型上下文空间较多。

当前阶段的模型，似乎直接给答案，后续就顺着答案思路走。有时可以先提问让ai探索，再根据探索结果提问或引导。

### 8.3.测试清理与重构

单元测试的清理，测试质量不高（当前ai编写的单元测试通过率虚高），不维护（过期、断链）会拖慢反馈循环。
