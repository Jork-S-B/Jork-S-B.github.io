## openspec

```shell
# 通过npm安装
npm install -g @fission-ai/openspec@latest

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

/gstack:browse "竞品/技术方案调研"     ← 新增：浏览器调研，事实沉淀
/superpowers:brainstorm                # 头脑风暴
/gstack:design-review                  ← 新增：设计稿/方案评审，提前获取反馈
/superpowers:write-plan                # 编写实施计划

## 二、TDD开发
# /opsx:apply → 不要该命令，改用superpowers
/superpowers:test-driven-development   # TDD模式开发
/superpowers:execute-plan              # 执行计划

## 三、反馈优化闭环（gstack 核心循环）
/gstack:qa                            ← 新增：QA自动化验证，获取质量反馈
/gstack:review                        ← 新增：代码审查，发现潜在问题
/gstack:browse "功能验收"             ← 新增：浏览器真实环境验收
# 根据反馈修正 → 重新执行步骤二/三（闭环迭代）

## 四、验证与归档
/opsx:validate                         # 规格验证
/opsx:archive                          # 归档

## 五、复盘沉淀
/gstack:retro                          ← 新增：回顾总结，沉淀经验教训
/gstack:document-generate              ← 新增：生成文档，知识入库

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
                    │     superpowers (头脑风暴/写计划) │
                    └──────────┬──────────────────────┘
                                │ 开发
                    ┌──────────▼──────────────────────┐
                    │     TDD / execute-plan           │
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
                    │  再次沉淀，反哺下一轮规划          │
                    └─────────────────────────────────┘

关键变化：
- 调研前置：/gstack:browse 在 brainstorm 前做事实调研，避免闭门造车
- 反馈内循环：qa → review → browse验收 形成快速迭代，不通过就回退开发
- 复盘外循环：每个周期结束用 retro + document-generate 沉淀经验，反哺下一轮规划

```