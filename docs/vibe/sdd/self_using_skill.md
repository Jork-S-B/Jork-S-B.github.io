## mattpocock skills

My agent skills that I use every day to do real engineering - not vibe coding.

程序员实用工具集

项目地址: https://github.com/mattpocock/skills

## learn-by-building

ai编程时，不懂就问的skill

```
# 快速安装
npx skills add chaojiwudibing/learn-by-building
```

项目地址: https://github.com/chaojiwudibing/learn-by-building

## Garden Skills

包括5个技能

- web-video-presentation 网页视频 / 演示
- web-design-engineer 设计 / 前端
- gpt-image-2 图像生成 / Prompt
- beautiful-article 任意素材 → 一篇精美的文章
- kb-retriever 检索 / 本地知识库

项目中文readme: https://github.com/ConardLi/garden-skills/blob/main/README.zh-CN.md

### web-video-presentation

下载压缩包，windows手动安装skill，通过符号链接避免"多agent工具多份skill代码"

mklink /D "C:\Users\q7299\.claude\skills\web-video-presentation" "F:\Administrator\Downloads\skills\web-video-presentation"

---

skill内部流程

1. 文章转口播稿
2. 口播稿转开发大纲
3. 每步视觉演示
4. 步骤与口播节奏对齐

但如何保证产出稳定性？

1. 划定边界
2. 设检查点
3. 自检
4. 修复

#### 设计哲学

一个成熟的`harness`,包含六个核心。

目标: 把模型能力/工具能力/人的判断，组织成一条稳定可控的生产流程。

1. 上下文管理: 模型到底看到了什么

    类似skill的按需读取策略(渐进式披露)，运行到某个阶段读对应的、最需要的文档信息，避免被无关内容干扰。

2. 工具系统: 模型到底能做什么

    本skill中主要是读写，但多agent并行开发需要考虑冲突问题。

    - 隔离机制: 1.按章节独立文件夹、CSS前缀；2.全局变量兜底，控制主题、风格、间距

3. 执行与编排: 模型下一步该做什么

    分步执行: 由预设的任务作为起点，步骤 + 人工检查节点组合。

    人工检查节点包括: 初稿审批、素材选择、后续并行开发还是mvp版本(mvp版本为后续的开发提供基准参考)、分支选择等。

4. 状态与记忆: 系统如何跨步骤保持连续性

    持久化开发大纲，将检查点关键决策文档记录，作为开发持续记忆，避免上下文信息不对称。
    
    本skill额外的特色设计: `script.md`把握叙事节奏、`article.md`把握信息密度。

5. 评估与观测: 系统怎么知道自己做得对不对

    如何避免agent自评失真？

    - 自检、修复、汇报: 1.Agent Teams, 由独立的Reviewer Agent审查，但该模式token花费高；2.SubAgent, 由子代理审查，评估效果次之。

6. 约束与恢复: 出错了怎么办，怎么避免跑偏

    节奏不对、ai味太浓这类问题如何处理？如何从某个步骤重做而非全部推倒？

    - 最小切片原则: 定位反馈修复的点在哪一层，只改最小切片。

??? "Agent Teams & SubAgent"

- SubAgent, 主Agent任务分发，子Agent执行任务将结果传回，各子Agent之间不干扰（也不讨论），适合结果导向型任务。
- Agent Teams, 组长+组员，每个组员都是独立会话（token花费高），共享任务列表，适合需要交互反馈的任务。

#### 实操

1. Claude Code
2. MiniMax-M2.7，需要带视觉的模型，需处理视频、音频合成。
3. CC-Switch，快速切换模型配置
4. mmx-cli，agent口播音频合成阶段适用。
5. 安装该skill
6. Agent Teams + tmux, 适合多章节并行开发。

tmux, 开源终端管理器，多窗口展示agent会话。

claude的实验性功能: Agent Teams，`setting.json`设置如下

```JSON
{
    "env":{
        "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
    },
    "teammateMode": "tmux",
}
```

