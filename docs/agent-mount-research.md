# 主流编码智能体「规则 / 命令 / Skills 目录 / MCP」挂载机制调研（草稿）

> 调研口径：2026 年 11 月当前版本；信息来自各工具官方文档或官方仓库文档源文件。
> 编码智能体迭代很快，README 引用时应提示用户「以官方文档为准」。
> 本文件为调研草稿，后续并入 README；标注「以官方文档为准」的条目表示未在官方文档中核实到确切路径/页面，未做推测。
>
> 本仓库自带的 Skill 文件夹结构（供对照）：
>
> ```text
> skill/sport-data-sync-kit/
> ├── SKILL.md            # 必需：元数据 + 核心指令
> ├── references/         # 可选：参考资料（formats.md / platforms.md / ...）
> └── scripts/            # 可选：可执行脚本（check_fit.py）
> ```
>
> 机制类别图例：**Rules** = 规则/指令文件；**Commands** = 斜杠命令目录；**Skills** = 文件夹式 Skill（SKILL.md + references/ + scripts/）；**MCP** = Model Context Protocol 外部工具配置；**分层** = 项目级 / 用户级（全局）双层。

## 一、对照表

| 工具 | 机制类别 | 挂载路径 / 配置方式（项目级 / 用户级） | 官方文档 URL | 备注 |
| --- | --- | --- | --- | --- |
| **OpenAI Codex CLI** | Rules（AGENTS.md）；Skills 目录；MCP；项目/用户分层 | **规则**：项目级为仓库根及各级子目录的 `AGENTS.md`（可被 `AGENTS.override.md` 覆盖）；用户级为 `~/.codex/AGENTS.md`（或 `~/.codex/AGENTS.override.md`，`CODEX_HOME` 可改目录）。**Skills**：项目级 `.agents/skills/`（从 CWD 向上扫描到仓库根）；用户级 `~/.agents/skills/`；另有管理员级 `/etc/codex/skills`。**MCP**：在 Codex 配置文件（`config.toml`）的 MCP 服务段配置，具体字段以官方文档为准。 | https://developers.openai.com/codex/guides/agents-md ；https://developers.openai.com/codex/skills | 原生支持文件夹式 Skill 与渐进披露（启动时仅载入 name/description，命中后才读完整 SKILL.md）；基于开放 Agent Skills 规范（含 scripts/、references/、assets/）；兼容 `.agents/skills/` 目录。 |
| **Claude Code** | Rules（CLAUDE.md / rules 目录）；Commands 目录；Skills 目录；MCP；项目/用户分层 | **规则**：项目级 `CLAUDE.md`（或 `.claude/CLAUDE.md`）、`.claude/rules/*.md`；用户级 `~/.claude/CLAUDE.md`、`~/.claude/rules/`；仓库已有 `AGENTS.md` 时可替代 `CLAUDE.md` 读取。**Commands**：项目级 `.claude/commands/*.md`；用户级 `~/.claude/commands/`。**Skills**：项目级 `.claude/skills/<name>/SKILL.md`；用户级 `~/.claude/skills/<name>/`。**MCP**：项目级 `.mcp.json`；用户级通过 `claude mcp add` 等方式配置（以官方文档为准）。 | https://code.claude.com/docs/en/claude-directory/ ；https://code.claude.com/docs/en/memory | Anthropic Agent Skills 原生实现；渐进披露；Skill 文件夹可带 scripts/references 等资源；规则与 Skills 分层清晰（规则常驻上下文，Skill 按需加载）。 |
| **GitHub Copilot**（VS Code 扩展 / Copilot CLI / 云端 Agent） | Rules（instructions 文件）；Skills 目录；MCP；项目/用户分层 | **规则**：用户级 `$HOME/.copilot/copilot-instructions.md`、`$HOME/.copilot/instructions/**/*.instructions.md`；项目级 `.github/copilot-instructions.md`、`.github/instructions/**/*.instructions.md`；同时识别标准位置的 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`。**Skills**：项目级 `.github/skills/`、`.claude/skills/`、`.agents/skills/`；用户级 `~/.copilot/skills/`、`~/.claude/skills/`、`~/.agents/skills/`（可用 `chat.agentSkillsLocations` 设置追加目录）。**MCP**：在 VS Code / CLI 的 MCP 设置中配置，以官方文档为准。 | https://code.visualstudio.com/docs/copilot/customization/agent-skills ；CLI 指令文件官方仓库源文件：https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions.md （CLI 落地页以 docs.github.com Copilot CLI 文档为准，检索关键词「Copilot CLI custom instructions」） | 兼容开放 Agent Skills 规范（agentskills.io），Skill 可跨 VS Code / CLI / 云端 Agent 移植；渐进披露（先读 name+description，命中后载入正文与资源）；指令文件仅 Markdown，不含脚本。 |
| **Cursor** | Rules（.cursor/rules）；Skills 目录；MCP；项目/用户分层 | **规则**：项目级 `.cursor/rules/*.mdc`（YAML frontmatter：alwaysApply / globs / description / 手动触发）；用户级规则在 Cursor Settings → General 中配置并随账号同步（本地规则目录确切路径以官方文档为准）；同时读取根目录 `AGENTS.md`、`CLAUDE.md`。**Skills**：项目级 `.cursor/skills/`、`.agents/skills/`（含 monorepo 嵌套子目录）；用户级 `~/.cursor/skills/`、`~/.agents/skills/`；兼容读取 `.claude/skills/`、`.codex/skills/`。**MCP**：在 Cursor 设置的 MCP 面板配置。 | https://cursor.com/docs/rules ；https://cursor.com/help/customization/skills | 支持文件夹式 Skill 与渐进披露；兼容开放 Agent Skills 规范；规则为单文件 `.mdc`，Skill 才支持打包脚本/模板等资源。 |
| **Windsurf**（Cascade） | Rules（.windsurf/rules）；Skills 目录；Workflows；MCP；项目/用户/企业系统级分层 | **规则**：项目级 `.windsurf/rules/`（可在工作区及子目录、向上到 Git 根目录被发现）；用户级为 `global_rules.md`（通过 Cascade 自定义面板的 Global 规则创建）；企业系统级按 OS 目录加载（如 Windows `C:\ProgramData\Windsurf\rules\*.md`）；同时识别 `AGENTS.md`。**Skills**：项目级 `.windsurf/skills/<name>/`；用户级 `~/.codeium/windsurf/skills/<name>/`；兼容发现 `.agents/skills/`、`~/.agents/skills/`，开启 Claude 配置读取后也扫描 `.claude/skills/`。**MCP**：官方文档有独立 MCP 章节，配置以官方文档为准。 | https://docs.windsurf.com/plugins/cascade/memories ；https://docs.windsurf.com/windsurf/cascade/skills | 支持文件夹式 Skill 与渐进披露；兼容 agentskills.io 规范；规则为单文件 Markdown，Workflow 为手动触发的单文件提示模板。 |
| **Trae**（国内 docs.trae.cn / 海外 docs.trae.ai；含 Trae IDE、Trae 插件、SOLO） | Rules（.trae/rules）；Skills 目录；MCP；项目/用户分层 | **规则**：项目级 `.trae/rules/`（支持至多 3 层嵌套子目录；子目录可放模块专属规则与 `AGENTS.md`）；用户级 `~/.trae/user_rules`（Windows：`%USERPROFILE%/.trae/user_rules`）；可在设置中开关导入根目录 `AGENTS.md`、`CLAUDE.md`、`CLAUDE.local.md`。**Skills**：项目级 `.trae/skills/<name>/`；用户级 `~/.trae/skills/`（Windows：`%USERPROFILE%/.trae/skills`）；兼容开放规范目录 `.agents/skills/`（需在「设置 > 技能与命令 > 导入设置」启用）。**MCP**：通过插件/MCP 管理中心配置。 | https://docs.trae.ai/ide/rules ；https://docs.trae.ai/ide/skills ；国内站：https://docs.trae.cn/ide_rules.md | 支持文件夹式 Skill（SKILL.md + examples/templates/resources）与按需加载；`.trae/skills/` 与 `.agents/skills/` 重名时优先 `.trae/skills/`；规则全量注入上下文，Skill 按需加载。 |
| **Augment Code**（IDE 插件 / Auggie CLI） | Rules（.augment/rules + guidelines）；Skills 目录；MCP；项目/用户分层 | **规则**：用户级 `~/.augment/rules/`、`~/.augment/user-guidelines.md`；项目级 `<root>/.augment/rules/`、仓库根 `.augment-guidelines`；层级规则通过各级目录的 `AGENTS.md` / `CLAUDE.md` 向上遍历发现（同目录两者并存时仅用 `AGENTS.md`）。**Skills**：项目级与用户级均扫描 `.augment/skills/`、`.claude/skills/`、`.agents/skills/`（用户级 `~/.augment/skills/` 等）；CLI 还可用 `--skill <path>` 单次加载或在 `settings.json` 的 `skills` 数组追加路径。**MCP**：以官方文档为准。 | https://docs.augmentcode.com/setup-augment/guidelines ；https://docs.augmentcode.com/cli/skills.md | Skill 遵循 agentskills.io 规范，兼容 Claude/开放目录；Skill 为文件夹打包（SKILL.md + 资源）；规则分 Always / Manual / Auto 三种触发方式；Skills 功能在部分渠道为 Public Beta。 |
| **Cline**（VS Code 扩展 / Desktop / CLI / SDK） | Rules（.cline/rules，兼容旧 `.clinerules`）；Skills 目录；Workflows/Hooks/Agents；MCP；项目/用户分层 | **规则**：项目级 `.cline/rules/`（旧布局 `.clinerules/`、根目录 `.clinerules` 仍兼容）；用户级 `~/.cline/rules/`、`~/Documents/Cline/Rules/`；识别项目根 `AGENTS.md` 与全局 `~/.agents/AGENTS.md`。**Skills**：项目级 `.cline/skills/`；用户级 `~/.cline/skills/`；兼容 `.agents/skills/`、`~/.agents/skills/`。**MCP**：全局 `~/.cline/data/settings/cline_mcp_settings.json`（`mcpServers` 键），项目级 `.cline/` 配置；也可在 Configure 面板的 MCP Servers 中编辑，支持 stdio / HTTP / SSE。 | https://docs.cline.bot/getting-started/config.md ；https://docs.cline.bot/customization/cline-rules ；https://docs.cline.bot/mcp/mcp-overview | 较新版本已支持文件夹式 Skill（含 scripts 等打包资源）与 `.agents/skills/` 开放目录；规则目录递归读取；MCP 配置跨 IDE/CLI/SDK 共享。 |
| **Roo Code**（VS Code 扩展） | Rules（.roo/rules，按模式拆分）；Skills 目录；自定义 Modes；MCP；项目/用户分层 | **规则**：用户级 `~/.roo/rules/`、`~/.roo/rules-{modeSlug}/`（Windows `%USERPROFILE%\.roo\...`）；项目级 `.roo/rules/`、`.roo/rules-{modeSlug}/`；回退单文件 `.roorules`、`.roorules-{mode}`，兼容旧 `.clinerules`；读取根目录 `AGENTS.md`（或 `AGENT.md`）。**Skills**：用户级 `~/.roo/skills/`、`~/.agents/skills/`；项目级 `.roo/skills/`、`.agents/skills/`；支持模式专属目录 `skills-{mode}/`。**MCP**：在扩展设置 / MCP 设置 JSON 中配置，以官方文档为准。 | https://roocodeinc.github.io/Roo-Code/features/custom-instructions/ ；https://roocodeinc.github.io/Roo-Code/features/skills/ | 兼容 Agent Skills 格式与 `.agents/skills/` 开放目录；渐进披露；Skill 可打包 scripts/templates/references；规则目录递归读取并按文件名排序注入。 |
| **Continue** | Rules（.continue/rules）；MCP（mcpServers）；项目/用户分层 | **规则**：项目级 `.continue/rules/*.md`（YAML frontmatter：name / globs / regex / description / alwaysApply）；用户级配置在 `~/.continue/config.yaml`（Windows `%USERPROFILE%\.continue\config.yaml`）；用户级规则目录确切路径以官方文档为准（检索关键词「Continue rules global directory」）。**MCP**：项目级 `.continue/mcpServers/`，或在 `config.yaml` 中声明 MCP 服务；密钥走 `.env`（项目级 `.continue/.env` / 全局 `~/.continue/.env`）。 | https://docs.continue.dev/customize/deep-dives/rules ；https://docs.continue.dev/guides/configuring-models-rules-tools | **不支持文件夹式 Skill**：知识需拆成 `.continue/rules/` 下的 Markdown 规则文件；规则仅作用于 Agent/Chat/Edit，不作用于自动补全；可通过 `@file` / context provider 引用外部资料。 |
| **Zed AI**（Zed Agent） | Rules（AGENTS.md）；Skills 目录；Agent Profiles；MCP；项目/用户分层 | **指令**：以 `AGENTS.md` 作为主要指令文件，分个人级与项目级（个人级确切路径以官方文档为准）。**Skills**：项目级 `.agents/skills/`；用户级 `~/.agents/skills/`；每个 Skill 为直接子目录，内含 `SKILL.md`，可选 `scripts/`、`references/`、`assets/`。**MCP**：在 Zed Agent 设置中配置 MCP 服务器。 | https://zed.dev/docs/ai/instructions ；https://zed.dev/docs/ai/skills | 兼容开放 `.agents/skills/` 目录与 Agent Skills 结构；Skill 按需调用（可斜杠命令触发）；项目 Skill 需在受信任（trusted）项目中才加载。 |
| **Gemini CLI** | Rules（GEMINI.md）；Commands 目录；Skills 目录；MCP；项目/用户分层 | **规则**：用户级 `~/.gemini/GEMINI.md`；项目/工作区 `GEMINI.md` 及各级父目录、访问文件时的 JIT 子目录扫描；可在 `.gemini/settings.json` 的 `context.fileName` 中把 `AGENTS.md` 等加入识别名单；支持 `@file.md` 导入。**Commands**：项目级 `.gemini/commands/*.toml`；用户级 `~/.gemini/commands/`。**Skills**：项目级 `.gemini/skills/` 或别名 `.agents/skills/`；用户级 `~/.gemini/skills/` 或 `~/.agents/skills/`。**MCP**：在 CLI 配置中声明 MCP 服务，以官方文档为准。 | https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md ；https://geminicli.com/docs/cli/skills.md ；https://geminicli.com/docs/cli/custom-commands.md | 兼容开放 Agent Skills 格式（与 Claude/Codex 同构的 SKILL.md 可复用）；Skill 命中前需用户批准激活；Commands 为 TOML 单文件。 |
| **Amazon Kiro**（IDE / Kiro CLI / Crew） | Rules（Steering 文件）；Skills 目录；MCP；项目/用户分层 | **Steering（规则）**：项目级 `.kiro/steering/` 下的 Markdown 文件；用户级 `~/.kiro/steering/`；冲突时项目级优先。**Skills**：项目级 `.kiro/skills/`；用户级 `~/.kiro/skills/`；同名 Skill 项目级优先。**MCP**：以官方文档为准。 | https://kiro.dev/docs/steering/ ；https://kiro.dev/docs/cli/skills/ | 支持文件夹式 Skill：`SKILL.md` + 可选 `scripts/`、`references/`、`assets/`；渐进披露（启动仅载入元数据，按需载入正文）；Steering 为纯 Markdown 规则目录。 |
| **腾讯 CodeBuddy**（IDE 插件 / CodeBuddy Code CLI） | Rules（.codebuddy/rules）；Commands 目录；Skills 目录；Hooks/Agents/插件；MCP；项目/用户分层 | **规则**：项目级 `.codebuddy/rules/`（启动/重载项目时自动扫描，适用于所有对话与内联对话）；用户级规则的确切目录以官方文档为准（可在规则/提示词管理面板配置）。**Commands**：项目级 `.codebuddy/commands/*.md`；用户级 `~/.codebuddy/commands/*.md`（子目录以冒号分层命名，如 `/frontend:build`）。**Skills**：项目级 `.codebuddy/skills/<name>/`；用户级 `~/.codebuddy/skills/<name>/`。**MCP**：CLI 内 `/mcp` 管理；全局/项目 `settings.json`（优先级 PROJECT_LOCAL > PROJECT > USER）。 | https://copilot.tencent.com/docs/plugin/操作指南/自定义规则 ；https://www.codebuddy.ai/docs/zh/cli/skills ；https://copilot.tencent.com/docs/cli/slash-commands | 支持文件夹式 Skill（SKILL.md + frontmatter，可带 scripts/资源；支持 `context: fork` 子代理执行）；Skill 与命令分离：Skill 由模型按 description 自动选择，命令由用户手动触发；兼容程度对照开放规范需以官方文档为准。 |
| **豆包 MarsCode** | 规则 / Skills（已并入 Trae，无独立体系） | 原「豆包 MarsCode 编程助手」已更名为 Trae 插件，并入 Trae 产品体系；未检索到 MarsCode 独立维护的规则/Skill 目录文档。知识挂载按 **Trae** 机制：项目级 `.trae/rules/`、`.trae/skills/` 或开放目录 `.agents/skills/`；用户级 `~/.trae/...`（详见 Trae 一行）。 | 更名说明（官方 FAQ）：https://docs.trae.com.cn/plugin/faq ；规则/Skill 路径以 Trae 官方文档为准（检索关键词「Trae rules」「Trae skills」） | 不建议在 README 中为 MarsCode 单独写路径；如遇旧版 MarsCode 插件，规则/Skill 目录以其内置设置面板与官方文档为准。 |
| **Qoder**（Qoder IDE / Qoder CLI；国内 Qoder CN 即 Lingma） | Rules（.qoder/rules + AGENTS.md）；Auto-Memory；MCP；项目/用户分层 | **规则**：项目级 `<project>/.qoder/rules/**/*.md`、`<project>/AGENTS.md`、`<project>/AGENTS.local.md`；用户级 `~/.qoder/rules/**/*.md`、`~/.qoder/AGENTS.md`；规则 frontmatter 支持 always_on / manual / model_decision / glob 等触发方式；兼容识别 `AGENTS.md`（与规则冲突时规则优先）。**国内版（Lingma）**：项目规则目录为 `.lingma/rules`（见阿里云帮助中心）。**MCP**：在受信任工作区的配置 / Hooks / MCP 设置中声明，以官方文档为准。 | https://docs.qoder.com/zh/user-guide/rules ；https://docs.qoder.com/cli/memory ；国内版（Lingma）：https://help.aliyun.com/en/lingma/rules | 已核实到规则目录与 AGENTS.md 机制；**未在官方文档中核实到独立的文件夹式 Skill（SKILL.md）机制**，标注「以官方文档为准」；当前需把知识拆成 rules Markdown 或写入 AGENTS.md。 |

## 二、分节说明

### 2.1 兼容开放 Agent Skills 规范（`.agents/skills/<name>/SKILL.md` + references/ + scripts/）的工具

以下工具可直接放置本仓库这种「Skill 文件夹」，且遵循渐进披露（先索引 name/description，命中后再读正文与资源）：

- **OpenAI Codex CLI**：`.agents/skills/`（项目）、`~/.agents/skills/`（用户）
- **Claude Code**：`.claude/skills/`（项目）、`~/.claude/skills/`（用户）；Anthropic 原生规范
- **GitHub Copilot**：`.agents/skills/` / `.github/skills/` / `.claude/skills/`（项目），`~/.agents/skills/` 等（用户）
- **Cursor**：`.agents/skills/`、`.cursor/skills/`（项目），`~/.agents/skills/`、`~/.cursor/skills/`（用户）
- **Windsurf**：`.agents/skills/`、`.windsurf/skills/`（项目），`~/.agents/skills/`、`~/.codeium/windsurf/skills/`（用户）
- **Trae**：`.agents/skills/`（需在导入设置中启用）、`.trae/skills/`（项目），`~/.trae/skills/`（用户）
- **Augment Code**：`.agents/skills/`、`.claude/skills/`、`.augment/skills/`（项目/用户）
- **Cline**：`.agents/skills/`、`.cline/skills/`（项目），`~/.agents/skills/`、`~/.cline/skills/`（用户）
- **Roo Code**：`.agents/skills/`、`.roo/skills/`（项目），`~/.agents/skills/`、`~/.roo/skills/`（用户）
- **Zed AI**：`.agents/skills/`（项目）、`~/.agents/skills/`（用户）
- **Gemini CLI**：`.agents/skills/`、`.gemini/skills/`（项目），`~/.agents/skills/`、`~/.gemini/skills/`（用户）
- **Amazon Kiro**：`.kiro/skills/`（项目）、`~/.kiro/skills/`（用户）
- **腾讯 CodeBuddy**：`.codebuddy/skills/`（项目）、`~/.codebuddy/skills/`（用户）；与开放规范的一一兼容程度以官方文档为准

### 2.2 仅支持 Rules / Commands（无文件夹式 Skill）的工具

- **Continue**：知识拆为 `.continue/rules/*.md` 规则文件；无 SKILL.md 文件夹机制。
- **Qoder**：已核实规则目录与 AGENTS.md；文件夹式 Skill 机制未在官方文档中核实到，以官方文档为准。
- 纯规则/指令文件层：Codex/Claude/Copilot/Cursor/Windsurf/Trae/Augment/Cline/Roo/Zed/Gemini/Kiro/CodeBuddy 也同时提供规则文件层，短约束放规则、多步工作流放 Skill。

### 2.3 MCP 配置概览

- 上表工具均提供 MCP 接入能力；MCP 用于挂载外部工具/数据源，与「规则文件 / Skill 文件夹」是正交的两层：规则与 Skill 提供指令与知识，MCP 提供可调用工具。
- 已核实配置位置：**Cline**（`cline_mcp_settings.json` 的 `mcpServers`）、**CodeBuddy**（`/mcp` 与 settings.json）、**Continue**（`.continue/mcpServers/` / config.yaml）。其余工具的 MCP 配置入口以各自官方文档为准。

### 2.4 本仓库 Skill 的挂载建议（供 README 草稿引用）

- 对支持开放目录的工具：将 `skill/sport-data-sync-kit/` 整个文件夹复制到项目级 `.agents/skills/sport-data-sync-kit/`（团队共享，提交 Git）；个人复用放 `~/.agents/skills/sport-data-sync-kit/`。
- 对使用私有目录的工具：复制到对应目录，如 `.claude/skills/`、`.cursor/skills/`、`.trae/skills/`、`.windsurf/skills/`、`.augment/skills/`、`.cline/skills/`、`.roo/skills/`、`.kiro/skills/`、`.codebuddy/skills/`、`.gemini/skills/`。
- 对仅支持规则的工具（如 Continue）：把 `SKILL.md` 正文与 `references/` 中的要点拆成规则 Markdown 放入对应 rules 目录；脚本类资源无法随规则自动打包，需在指令中写明脚本相对路径。
- 跨工具复用时，保持文件夹名与 SKILL.md frontmatter 的 `name` 一致（开放规范要求 name 与目录名匹配）。

## 三、核实状态清单

### 3.1 已核实官方文档 URL（本次调研中打开或取自官方文档站点）

| 工具 | 已核实文档 |
| --- | --- |
| OpenAI Codex CLI | https://developers.openai.com/codex/guides/agents-md ；https://developers.openai.com/codex/skills |
| Claude Code | https://code.claude.com/docs/en/claude-directory/ ；https://code.claude.com/docs/en/memory |
| GitHub Copilot | https://code.visualstudio.com/docs/copilot/customization/agent-skills ；CLI 指令源文件（github/docs 仓库）：https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions.md |
| Cursor | https://cursor.com/docs/rules ；https://cursor.com/help/customization/skills |
| Windsurf | https://docs.windsurf.com/plugins/cascade/memories ；https://docs.windsurf.com/windsurf/cascade/skills |
| Trae | https://docs.trae.ai/ide/rules ；https://docs.trae.ai/ide/skills ；https://docs.trae.cn/ide_rules.md |
| Augment Code | https://docs.augmentcode.com/setup-augment/guidelines ；https://docs.augmentcode.com/cli/skills.md |
| Cline | https://docs.cline.bot/getting-started/config.md ；https://docs.cline.bot/customization/cline-rules ；https://docs.cline.bot/mcp/mcp-overview |
| Roo Code | https://roocodeinc.github.io/Roo-Code/features/custom-instructions/ ；https://roocodeinc.github.io/Roo-Code/features/skills/ |
| Continue | https://docs.continue.dev/customize/deep-dives/rules ；https://docs.continue.dev/guides/configuring-models-rules-tools |
| Zed AI | https://zed.dev/docs/ai/instructions ；https://zed.dev/docs/ai/skills |
| Gemini CLI | https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md ；https://geminicli.com/docs/cli/skills.md ；https://geminicli.com/docs/cli/custom-commands.md |
| Amazon Kiro | https://kiro.dev/docs/steering/ ；https://kiro.dev/docs/cli/skills/ |
| 腾讯 CodeBuddy | https://copilot.tencent.com/docs/plugin/操作指南/自定义规则 ；https://www.codebuddy.ai/docs/zh/cli/skills ；https://copilot.tencent.com/docs/cli/slash-commands |
| 豆包 MarsCode | https://docs.trae.com.cn/plugin/faq （更名说明） |
| Qoder | https://docs.qoder.com/zh/user-guide/rules ；https://docs.qoder.com/cli/memory ；国内版 https://help.aliyun.com/en/lingma/rules |

### 3.2 标注「以官方文档为准」的条目（未核实到确切路径/落地页，未推测）

| 工具 | 待核实点 | 检索关键词 |
| --- | --- | --- |
| GitHub Copilot CLI | 指令文件在 docs.github.com 的正式落地页（当前引用为 github/docs 仓库源文件） | Copilot CLI custom instructions |
| Cursor | 用户级规则在本地文件系统的确切目录（官方文档描述为账号同步的 Settings 规则） | Cursor user rules directory |
| Continue | 用户级规则目录的确切路径（已核实全局配置为 `~/.continue/config.yaml`） | Continue rules global directory |
| Zed AI | 个人级 AGENTS.md 的确切文件路径 | Zed AGENTS.md personal global |
| 腾讯 CodeBuddy | 用户级 Rules 目录的确切路径（已核实用户级 Skills/Commands 目录） | CodeBuddy global rules directory |
| Qoder | 是否提供文件夹式 Skill（SKILL.md）机制 | Qoder agent skills SKILL.md |
| 豆包 MarsCode | 旧版插件遗留的规则/Skill 目录（产品已并入 Trae） | MarsCode 规则 Trae 插件 |
| 各工具 MCP | 除 Cline / CodeBuddy / Continue 外，其余工具 MCP 配置文件的确切字段 | `<工具名> MCP server configuration` |

## 四、调研范围与限制

- 覆盖工具共 16 个条目：Codex CLI、Claude Code、GitHub Copilot、Cursor、Windsurf、Trae（国内/海外）、Augment Code、Cline、Roo Code、Continue、Zed AI、Gemini CLI、Amazon Kiro、腾讯 CodeBuddy、豆包 MarsCode、Qoder；字节 Trae 系与 MarsCode 已按并入关系统一说明。
- 本表只核对「知识/规则挂载」与「Skill 文件夹」机制，不评测模型能力、授权方式与计费。
- 路径基于 2026 年 11 月可访问的官方文档；Windows 用户级目录多为 `%USERPROFILE%\<tool>\...`，macOS/Linux 为 `~/<tool>/...`，具体以官方文档为准。
