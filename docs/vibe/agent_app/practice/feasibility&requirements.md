使用的skill: [sdd_skill](/vibe/sdd/sdd_skill)

## 初始化

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

## 可行性分析

Feasibility Analysis

产物: FSR-Feasibility Study Report，可行性研究报告

`grill-me`, 使用时可在提示词中明确本次讨论的范围/目的，防止无休止讨论。同时在问题跑偏时，及时介入纠正。

## 需求分析

Requirements Analysis

产物: PRD-Product Requirements Document，产品需求文档(或者SRS-Software Requirements Specification, 软件需求规格说明书)

1. 前期不用定太细，有些需求是边做边浮现出来的。
2. 需求逐条评审
3. 竞品分析与功能调整，输出{游戏设计文档gdd}

## 技术选型

本质给ai搭建一个良好的反馈回路(思考、执行、反馈的循环)，目前效率低的点是工具调用、跑代码、执行命令的地方，因此从技术选型的方向考虑。

ai的单元测试覆盖率不可信，引入`突变测试`(运算符取反，预期会有错误，否则说明测试质量不高)，尤其在项目的圈复杂度快速膨胀的时候。

- 突变测试通过定时任务运行，不宜放在反馈回路中。
- 技术选型提示词加入"AI First 技术栈"，效果更好些。
- `dependcy-cruiser`，画模块内依赖关系的开源项目。ai持续进化的背景下，细节可以少抓，但顶层架构的方向还是需把握的。
- js项目的突变测试参考`stryker.js`

## mattpocock skills

`grill-with-docs`, 在模型聪明区(1m上下文，聪明区约200k)能理清思路时使用

`wayfinder`, 具体实现有迷雾，想边做边看效果时使用。产出: 决策地图 + tickets(包括依赖、优先级等)，再逐项细分进行grill, research 或 prototype

- 可以让ai梳理wayfinder的目标，前提清除迷雾为主，不让ai自由发挥。目标不要定太远，决策不对就及时调整。
- 要求输出: 可选目标的依赖关系图 DAG
- todo: tickets任务产出的新的上下文如何管理

!!! note "上下文管理"

    - 继续对话，在聪明区内、下一轮预计不超出则继续
    - /new，当上下文没用，或上下文内容有错误则新开窗口
    - /compact，在当前上下文窗口压缩，但压缩后恢复到能继续工作，可能模型还得research
    - /handoff，当前上下文压缩后持久化为文件，可交给另一个模型