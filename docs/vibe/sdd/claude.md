- Agent: 属于是广泛的概念。
- Claude Code: 相较于Agent，CC是智能体的一种具体实现形式。

## 安装Claude Code

1. 终端执行: npm install -g @anthropic-ai/claude-code
2. 安装CC插件（可选）

由于区域限制，官方api无法直接使用

- 可在~/.claude.json添加配置`"hasCompletedOnboarding": true`
- 或者在CC Switch设置并切换供应商

## Claude Cli

- /skills: 查看技能列表
- /model: 切换或查看当前使用的模型
- /init: 初始化当前目录为 Claude Code 项目
- /compact: 压缩对话历史，减少 token 使用
- /add-dir: 添加一个目录到上下文
- /todos: 显示当前任务列表（如果已通过提示词生成 TODO 清单）
- /review: 对当前打开或选中的代码进行审查（触发内置代码审查流程）
- /test: 运行测试（需项目配置了测试命令，如 npm test 或 pytest）
- /rewind: 回滚/回退会话
- /fork: 从指定会话新建分支
- /resume: 恢复至指定会话
- /new: 新建会话

或者安装可视化插件，如`Claude Code for VS Code`

### 权限

- `bypass permissions on`，自动执行命令，不进行询问（慎用，`rm -rf`也会执行，容易误删）
- 部分放行，参考: [Claude Code 权限配置完全指南：让安全操作自动放行，危险命令必须确认](https://zhuanlan.zhihu.com/p/2044730355807147165)

    - 配置以 Python 项目为主
    - Node/前端项目: 可加 Bash(node *)、Bash(npm run *)、Bash(yarn *)、Bash(pnpm *)（注意 npm run 能执行 package.json 里任意命令，信任项目才放行）。

=== "settings.local.json/settings.json"

    ```json
    {
    "permissions": {
        "allow": [
        "Edit",
        "Write",
        "Read",
        "Glob",
        "Grep",
        "TodoWrite",
        "WebSearch",
        "WebFetch",
        "Bash(gh *)",
        "Bash(git *)",
        "Bash(find *)",
        "Bash(rg *)",
        "Bash(grep *)",
        "Bash(ls *)",
        "Bash(cat *)",
        "Bash(tree *)",
        "Bash(head *)",
        "Bash(tail *)",
        "Bash(echo *)",
        "Bash(pwd)",
        "Bash(which *)",
        "Bash(wc *)",
        "Bash(diff *)",
        "Bash(sort *)",
        "Bash(uniq *)",
        "Bash(stat *)",
        "Bash(file *)",
        "Bash(du *)",
        "Bash(df *)",
        "Bash(jq *)",
        "Bash(mkdir *)",
        "Bash(touch *)",
        "Bash(cp *)",
        "Bash(pytest *)",
        "Bash(ruff *)",
        "Bash(black *)",
        "Bash(prettier *)",
        "Bash(eslint *)",
        "Bash(mypy *)",
        "Bash(python *)",
        "Bash(python3 *)",
        "Bash(pip install *)"
        ],
        "ask": [
        "Bash(git reset --hard *)",
        "Bash(rm *)",
        "Bash(mv *)",
        "Bash(chmod *)",
        "Bash(chown *)",
        "Bash(npm install *)",
        "Bash(gh repo delete *)",
        "Bash(gh pr merge *)",
        "Bash(gh release *)"
        ],
        "deny": [
        "Bash(sudo *)",
        "Bash(rm -rf /*)",
        "Bash(rm -rf ~*)",
        "Bash(git push --force*)",
        "Bash(git push *--force*)",
        "Bash(git push *-f)",
        "Bash(git push *-f *)",
        "Bash(dd *)",
        "Bash(mkfs *)",
        "Read(.env)",
        "Read(**/.env)",
        "Read(**/.env.*)",
        "Read(**/secrets/**)",
        "Read(**/*credentials*)"
        ],
        "defaultMode": "default"
    }
    }

    ```

## 使用Skill

[复习一下相关知识](/vibe/basic_nouns/#skill)

### 使用现成的Skill

github、npm、marketplace等渠道获取skill

```bash
npx skills find "ui自动化"  # 找相关的技能
npx skills add skill_name
```
### 手工/ai辅助写skill

- 全局级: `~/.claude/skills/{SkillName}`
- 项目级: `{workspace}/.claude/skills/{SkillName}`

skill必有的文件: SKILL.md

其他目录还包括: 

- References: 按需加载的目录文件
- Scripts: 可执行的脚本文件
- Templates: 可模板化的文件

??? note "设计skill的提示词"

    可能已过时，可参考一下基本骨架；自定义skill可以用`write_skill`之类的skill。

    ```
    请按以下要求设计一个 Skill，存放于 `项目根目录/.trae/skill`。

    ## 一、Skill 职责（必须覆盖）

    - **代码理解**：快速定位代码文件，理解架构设计
    - **调试记忆**：记录调试过程，避免重复踩坑
    - **学习追踪**：跟踪学习进度，建立知识体系
    - **问题排查**：标准化流程，高效解决问题
    - **与大模型协作**：AI 会先查阅 Skill 文档，给出更准确的答案

    ## 二、核心设计理念（通用优秀实践）

    ### 1. 单一职责

    - 每个模块（core / templates / examples 等）只负责一类功能
    - 每个文档都有清晰的使用场景描述

    ### 2. 易于导航

    - 根目录必须有 `SKILL.md` 作为唯一入口
    - 文档之间使用相对路径互相链接，形成知识网络
    - 在 `SKILL.md` 中提供目录导航（快速跳转到 core / templates 等）

    ### 3. 可复用性

    - 调试模板标准化（使用同一套 YAML/JSON 格式）
    - 排查流程规范化（固定步骤：定位→假设→验证→修复→记录）
    - 解决方案可复用（抽象为独立片段，用 `### 场景：xxx` 标记）

    ### 4. 持续演进

    - 遇到问题 → 创建调试记录 → 更新 `references/common-issues.md`
    - 学习新知 → 创建笔记 → 更新 `references/knowledge-graph.md`
    - 代码变化 → 更新代码索引 → 更新 `core/architecture.md`
    - 每次重要修改在文档末尾记录 `## 变更日志`（最近 3 次）

    ### 5. 输入输出明确

    - 每个 Skill / 模块必须显式定义：
    - **输入**：所需参数、格式、是否必填
    - **输出**：产物的格式（Markdown / JSON / 纯文本）
    - **触发条件**：什么样的用户问法会激活此模块
    - **不触发条件**：明确写出不应激活的场景（防止误触发）

    ### 6. 失败兜底（关键！）

    - 当信息不足时，Skill 的默认行为是：
    - 输出一个 **“缺口报告”**（缺失哪些信息、建议用户补充什么）
    - 或跳转到通用流程（如 `templates/clarification-template.md`）
    - 当依赖缺失时（例如未找到某个代码文件），禁止编造，必须报告具体缺失项

    ### 7. 示例充足（至少三类）

    每个核心模块必须提供：

    - **Happy path**：正常输入 → 正常输出
    - **Edge case**：边界值、空输入、重复请求
    - **Fail case**：错误输入、依赖缺失 → 输出缺口报告或错误提示

    ### 8. 碎片化管理（避免大文档）

    - 单个文档不超过 300 行
    - 长内容拆分为可独立引用的子文档（例如 `core/` 下按功能拆分）
    - 使用 `@include`（Trae）或 `@` 引用（Claude Code）组合小文件

    ## 三、输出目录结构（必须遵循）

    ```
    .trae/skill/
    ├── SKILL.md                # 入口文件，包含元数据、导航、总体说明
    ├── core/                   # 核心功能模块
    │   ├── code-understanding.md
    │   ├── debug-memory.md
    │   ├── learning-tracker.md
    │   └── problem-solving.md
    ├── templates/              # 可复用的模板
    │   ├── debug-record.yaml
    │   ├── issue-report.md
    │   └── clarification.md
    ├── examples/               # 完整的使用示例（happy/edge/fail）
    │   ├── example-happy.md
    │   ├── example-edge.md
    │   └── example-fail.md
    ├── references/             # 长期积累的知识库
    │   ├── common-issues.md
    │   ├── knowledge-graph.md
    │   └── architecture.md
    └── scripts/                # 可选的可执行辅助脚本（Shell/Python）
        └── locate_symbol.py
    ```

    ## 四、特殊实践（针对不同 AI 编程助手）

    ### 🔷 针对 Claude Code 的特殊实践

    1. **元数据头**：在 `SKILL.md` 顶部使用 YAML frontmatter，至少包含 `name`, `description`, `version`, `allowed-tools`。
    2. **层次结构**：项目级技能放在 `.claude/skills/`，并在 `claude.md` 中声明 `@skill-name`。
    3. **权限显式声明**：若技能需要读写文件或执行命令，在描述中写 `requires_approval: true` 并说明原因。
    4. **子技能调用**：在描述中允许 Claude 先调用 `read_file` 等内置工具，再调用本技能。
    5. **引用方式**：在 `SKILL.md` 中使用 `@core/code-understanding` 引用子模块（Claude 会识别）。
    6. **错误报告格式**：必须输出 JSON 可解析的结构化错误，例如 `{"error": "file not found", "path": "..."}`。

    ### 🔶 针对 Trae 的特殊实践

    1. **JSON Schema 校验**：在 `SKILL.md` 或独立 `schema.json` 中定义输入参数的 JSON Schema（类型、必填、默认值、枚举）。
    2. **流式输出指导**：若技能执行耗时 >2 秒，在描述中写明“应每完成一步输出一次进度，避免用户等待焦虑”。
    3. **技能链（Skill Chaining）**：在描述中明确前置技能，例如 `depends_on: code-understanding`，Trae 会自动排序执行。
    4. **`@include`** **拆分**：使用 `@include references/knowledge-graph.md` 引用大文件，保持主文档精简。
    5. **内置模板初始化**：建议用户运行 `trae skill init` 生成标准骨架，再按本提示词填充。
    6. **安全沙箱说明**：若技能涉及网络请求或文件写入，在 `SKILL.md` 中标注 `sandbox: read-only` 或 `sandbox: isolated`。

    ## 五、自检清单（设计完成后逐条确认）

    - [ ] **边界清晰**：用户问“帮我随便写段代码”时，本 Skill 会不会误触发？是否有明确的拒绝/转交场景？
    - [ ] **依赖显式化**：是否需要先执行另一个 Skill？是否需要特定格式的输入（如必须是 JSON）？
    - [ ] **碎片最小化**：是否把长文档拆成了可独立引用、可更新的小单元（每个文件 <300 行）？
    - [ ] **示例充足**：每个核心模块都包含 happy / edge / fail 三类示例。
    - [ ] **版本与演进痕迹**：是否在受影响的文件中记录了最近 3 次重要修改的原因（变更日志）？
    - [ ] **失败兜底**：当信息不足时，是否定义了“缺口报告”模板或跳转流程？
    - [ ] **平台兼容性**（若同时用于 Claude Code 和 Trae）：是否同时满足两类特殊实践？
    - [ ] **权限安全**：是否明确列出了禁止的操作（如 `rm -rf`、修改系统配置）？

    ## 六、输出要求

    请按上述目录结构，生成**完整的 Skill 文件内容**（每个文件需包含实际可用的 Markdown / YAML / 代码）。对于重复性内容（如多个模板），可以生成带占位符的通用模板，并在注释中说明如何使用。

    开始设计。
    ```

## 工作流

- Coze: 扣子，面向公网普通用户、内容创作者、产品运营的智能体开发平台。
- Dify：面向企业内部非技术人员，开源的LLM应用开发平台
- LangGraph原生: 面向技术人员 + 复杂任务。
