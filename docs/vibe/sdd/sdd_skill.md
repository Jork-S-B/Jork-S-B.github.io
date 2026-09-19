## 适用场景结论

从0到1，选`superpowers`，体验比`mattpocock skills`较好。

原因是前者定义计划更细致，后者更倾向用户自己作为调度者把控流程，自动化程度较低。

然而在小改动方面，`mattpocock skills`更方便更轻量。

---

`openspec`适合团队协作、大型项目的场景。它的规格文档里除了ADR，还包含了变更记录，属于重要的上下文信息。

## mattpocock skills

项目地址: https://github.com/mattpocock/skills

My agent skills that I use every day to do real engineering - not vibe coding.

程序员实用**工具集**

```bash
# 快速安装
npx skills@latest add mattpocock/skills

# 仓库初始化
/setup-matt-pocock-skills
# 选择仓库管理方式: 基于github或者本地md文件

```
### 按工作流使用

1. **对齐需求** — 每次想改动代码前，先跑 `/grill-me`（非代码）或 `/grill-with-docs`（代码相关，还会顺带沉淀 `CONTEXT.md`和 ADR-架构决策记录）
2. **生成 spec** — `/to-spec` 把对齐后的对话直接转成 spec 发到 issue tracker
3. **拆分任务** — `/to-tickets` 把计划拆成可验证、可独立交付的 tracer-bullet tickets（大型规划用 `/wayfinder` 生成决策地图）
4. **实现** — `/implement` 按 spec/tickets 驱动 `/tdd`（红-绿，没有重构）和 `/code-review`（重构，包括编码标准、满足规格）
5. **排错** — 代码不工作时用 `/diagnosing-bugs` 的分阶段门控调试循环
6. **定期维护架构** — 每隔几天跑一次燃烧token `/improve-codebase-architecture`，扫描代码库的深化机会并生成 HTML 报告（注意它是“巡检”而非“抢救”）

- `grill-me`, 使用时需关注本次讨论的范围，不然容易无休止讨论，被牵着鼻子走。
- 1至4步，是核心的工作流程。明确的小改动不需要使用，模糊的需求用grill，复杂需求用to-spec，再复杂有多个功能点用to-tickets。根据复杂度灵活组合。

### 技能清单速览

- **Engineering（用户手动调用）**: `ask-matt`（不知道用哪个技能时的路由器）、`grill-with-docs`、`triage`（多人协作时使用，分类属于需求、bug、建议等，需要搭配初始化使用）、`improve-codebase-architecture`、`setup-matt-pocock-skills`、`to-spec`、`to-tickets`、`implement`、`wayfinder`
- **Engineering（模型自动调用）**: `prototype`、`diagnosing-bugs`、`research`、`tdd`、`domain-modeling`、`codebase-design`、`code-review`、`resolving-merge-conflicts`、`wizard`

`wayfinder`, 在grill使用后还说不清需求，或者想边做边看效果时使用。产出决策地图 + tickets(包括依赖、优先级等)，再逐项细分进行grill, research 或 prototype

`research`, 探索并把代码仓相关内容，引入agent上下文。

`prototype`, 原型驱动开发，通过该技能快速出原型图。

其他技能补充说明: 

`teach`, 基于agent教学，需要提供上下文信息。产物: 分章节生成html，包含重点和题目等。
`handoff`, 把当前任务上下文压缩并持久化，交给下一个agent。

---

## openspec

```shell
# 通过npm安装
npm install -g @fission-ai/openspec@latest

```

---

### 通过openspec优化skill

```shell
# 步骤1: 探索需求
/openspec-explore "idea"

# 步骤2: 生成规范文档
/openspec-propose

# 步骤3: 应用变更至skill
/openspec-apply

```

## superpowers

```shell
# 通过官方marketplace安装
/plugin install superpowers@claude-plugins-official

```

## gstack

打开claude code，复制下面这一段给claude执行

```shell
Install gstack: run git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup then add a "gstack" section to CLAUDE.md that says to use the /browse skill from gstack for all web browsing, never use mcp__claude-in-chrome__* tools, and lists the available skills: /office-hours, /plan-ceo-review, /plan-eng-review, /plan-design-review, /design-consultation, /design-shotgun, /design-html, /review, /ship, /land-and-deploy, /canary, /benchmark, /browse, /connect-chrome, /qa, /qa-only, /design-review, /setup-browser-cookies, /setup-deploy, /setup-gbrain, /retro, /investigate, /document-release, /document-generate, /codex, /cso, /autoplan, /plan-devex-review, /devex-review, /careful, /freeze, /guard, /unfreeze, /gstack-upgrade, /learn. Then ask the user if they also want to add gstack to the current project so teammates get it.

```

## openspec + superpowers 工作流

```shell
openspec init

claude

/opsx:propose "idea"

功能或需求不合适时，手动修改spec或者ai交互进行修改

# /opsx:apply
# 不要该命令，改用superpowers

/superpowers:brainstorm
/superpowers:write-plan

# tdd模式开发
/superpowers:execute-plan

# 验证与归档
/opsx:validate
/opsx:archive

```

## openspec + superpowers + gstack 工作流

```shell
## 初始化
openspec init
claude

## 一、需求定义与方案设计
/opsx:propose "idea"
# 功能或需求不合适时，手动修改spec或者ai交互进行修改

/gstack:browse "竞品/技术方案调研"     ← 新增: 浏览器调研，事实沉淀
/superpowers:brainstorm                # 头脑风暴
/gstack:design-review                  ← 新增: 设计稿/方案评审，提前获取反馈
/superpowers:write-plan                # 编写实施计划

## 二、TDD开发
# /opsx:apply → 不要该命令，改用superpowers
/superpowers:test-driven-development   # TDD模式开发
/superpowers:execute-plan              # 执行计划

## 三、反馈优化闭环（gstack 核心循环）
/gstack:qa                            ← 新增: QA自动化验证，获取质量反馈
/gstack:review                        ← 新增: 代码审查，发现潜在问题
/gstack:browse "功能验收"             ← 新增: 浏览器真实环境验收
# 根据反馈修正 → 重新执行步骤二/三（闭环迭代）

## 四、验证与归档
/opsx:validate                         # 规格验证
/opsx:archive                          # 归档

## 五、复盘沉淀
/gstack:retro                          ← 新增: 回顾总结，沉淀经验教训
/gstack:document-generate              ← 新增: 生成文档，知识入库

---
闭环机制说明

                    ┌─────────────────────────────────┐
                    │         事实沉淀层               │
                    │  (browse调研 / retro复盘 / doc)  │
                    └──────────┬──────────────────────┘
                                │ 输入
                    ┌──────────▼──────────────────────┐
                    │     openspec (需求定义)          │
                    │     /opsx:propose               │
                    └──────────┬──────────────────────┘
                                │ 规划
                    ┌──────────▼──────────────────────┐
                    │    superpowers (头脑风暴/写计划) │
                    └──────────┬──────────────────────┘
                                │ 开发
                    ┌──────────▼──────────────────────┐
                    │    TDD / execute-plan           │
                    └──────────┬──────────────────────┘
                                │ 输出
                    ┌──────────▼──────────────────────┐
                    │         反馈优化层 ←── 闭环核心   │
                    │  (qa / review / browse验收)      │
                    │  ┌─ 发现问题 → 返回开发 ──┐       │
                    │  │   (迭代至通过)         │      │
                    │  └────────────────────────┘      │
                    └──────────┬──────────────────────┘
                                │ 通过
                    ┌──────────▼──────────────────────┐
                    │     validate / archive           │
                    │     retro / document-generate    │
                    │         ↓                        │
                    │     再次沉淀，反哺下一轮规划       │
                    └─────────────────────────────────┘

关键变化: 
- 调研前置: /gstack:browse 在 brainstorm 前做事实调研，避免闭门造车
- 反馈内循环: qa → review → browse验收 形成快速迭代，不通过就回退开发
- 复盘外循环: 每个周期结束用 retro + document-generate 沉淀经验，反哺下一轮规划

```