# Sport Data Sync Kit

> 运动健康数据管理与跨平台同步的工程知识库，外加一个可挂载到编码 Agent 的 Skill（`sport-data-sync-kit`）。
> 核验日期：2026-11-11　｜　自有内容许可：MIT（见 [LICENSE](LICENSE)）

## 这是什么

本仓库沉淀了多平台运动数据同步项目在逆向分析、格式规范化、跨平台对接与回归排查中积累的方法论与实测口径，覆盖：

- 运动平台接入与鉴权、活动列表 / 下载 / 上传 / 入库判重；
- FIT / GPX / TCX 解析、字段映射、单位换算、清洗与 CRC 校验；
- UTC / 本地时间判据、活动开始时间锚点法与时区护栏；
- 版本升级导致旧功能回归的定位方法，以及高频踩坑清单；
- 全网运动数据同步开源项目、聚合器与解析库的对标矩阵。

仓库分两部分：

- `docs/`：Markdown 知识库，供人阅读与 Agent 检索；
- `skill/sport-data-sync-kit/`：可整体安装的 Agent Skill（`SKILL.md` + `references/` + `scripts/`）。

> 本仓库**不包含**任何受版权保护的反编译源码、补丁树、安装包、签名材料、账号凭证或个人运动样本；相关方法仅作学习研究与个人数据迁移备份参考。

## 目录结构

```text
sport-data-sync-kit/
├── README.md                  # 本文件：简介、Skill 安装与调用、各智能体挂载速查
├── AGENTS.md                  # 给编码 Agent 的仓库使用说明
├── LICENSE                    # MIT（本仓库自有内容）
├── THIRD_PARTY.md             # 第三方开源项目 / 规范 / 解析库致谢与许可证归属
├── .gitignore
├── docs/                      # 知识库文档
│   ├── 00-知识库索引.md
│   ├── 01-代码导览方法论.md
│   ├── 02-开源项目对标矩阵.md
│   ├── 03-踩坑录-版本回归主线与开发陷阱.md
│   ├── 04-运动数据规范-FIT-GPX-TCX.md
│   ├── 05-各平台对接备忘.md
│   ├── 06-UI与开发栈梳理.md
│   └── agent-mount-research.md   # 各编码智能体挂载机制调研全表（含核实状态）
└── skill/
    └── sport-data-sync-kit/       # 可安装 Skill 文件夹
        ├── SKILL.md
        ├── references/
        │   ├── formats.md         # FIT/GPX/TCX 结构、字段、单位、CRC、坐标体系
        │   ├── timezone.md        # 时区三形态、锚点法公式与护栏、字节检索诊断
        │   ├── platforms.md       # 各平台鉴权/列表/下载/上传/成功判据/限制
        │   ├── pitfalls.md         # 回归专题、跨方向回归清单、坑位与未闭环项
        │   └── opensource.md       # 高复用开源项目：接入方法/调用方式/鉴权/方向/许可证
        └── scripts/
            └── check_fit.py       # FIT 魔数与 CRC16 校验，纯标准库
```

## 快速上手

1. 新人 / 新 Agent 先读 [`AGENTS.md`](AGENTS.md) 与 [`docs/00-知识库索引.md`](docs/00-知识库索引.md)，按索引里的阅读顺序浏览。
2. 接入某平台前：先看 `docs/05-各平台对接备忘.md` 对应卡片，再读 `docs/04-运动数据规范-FIT-GPX-TCX.md` 的格式约束。
3. 排查同步失败 / 时间偏移 / 回归损坏：先查 `docs/03-踩坑录-版本回归主线与开发陷阱.md`，再按 Skill 的 `references/pitfalls.md` 收敛。
4. 下载或改写 FIT 文件后，运行确定性校验：

   ```bash
   python skill/sport-data-sync-kit/scripts/check_fit.py <file.fit> [file2.fit ...]
   ```

   - 退出码 `0`：魔数、文件头长度、数据区长度、文件尾 CRC16 全部通过；
   - 退出码 `1`：非 FIT、魔数不符、长度异常或 CRC 不一致；GPX/TCX 会被识别并跳过 CRC 校验；
   - 改过字节的 FIT 报 CRC 不一致时，先重算文件尾 CRC16 再校验。脚本无第三方依赖。

## 安装与调用本 Skill

### Skill 是什么

`skill/sport-data-sync-kit/` 遵循开放 Agent Skills 规范：根目录 `SKILL.md` 带 `name` 与 `description` 元数据，正文是七步核心工作流；`references/` 为按需读取的参考资料；`scripts/` 为可执行脚本。支持渐进披露——Agent 启动时只加载名称与描述，任务命中后再读正文与资源。

### 通用安装（兼容开放规范的工具）

1. 把 `skill/sport-data-sync-kit/` **整个文件夹**复制到所用工具的 Skill 目录，不要拆散 `references/` 与 `scripts/`；文件夹名与 `SKILL.md` frontmatter 的 `name` 保持一致。
2. **项目级（团队共享，随 Git 提交）**：放到项目根的 `.agents/skills/sport-data-sync-kit/`。
3. **用户级（个人跨项目复用）**：放到 `~/.agents/skills/sport-data-sync-kit/`（Windows 为 `%USERPROFILE%\.agents\skills\`）。

### 各智能体挂载速查

> 下表为 2026-11 版本口径；编码工具迭代很快，**具体路径与开关以各工具官方文档为准**。完整调研、核实状态与待核实点见 [`docs/agent-mount-research.md`](docs/agent-mount-research.md)。

| 工具 | 项目级 Skill 目录 | 用户级 Skill 目录 | 规则 / 指令文件 | 官方文档 |
|---|---|---|---|---|
| OpenAI Codex CLI | `.agents/skills/` | `~/.agents/skills/` | `AGENTS.md`（项目）/ `~/.codex/AGENTS.md` | https://developers.openai.com/codex/skills |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | `CLAUDE.md` / `.claude/rules/` | https://code.claude.com/docs/en/claude-directory/ |
| GitHub Copilot | `.github/skills/`、`.claude/skills/`、`.agents/skills/` | `~/.agents/skills/` 等 | `.github/copilot-instructions.md` | https://code.visualstudio.com/docs/copilot/customization/agent-skills |
| Cursor | `.cursor/skills/`、`.agents/skills/` | `~/.cursor/skills/`、`~/.agents/skills/` | `.cursor/rules/*.mdc` | https://cursor.com/help/customization/skills |
| Windsurf | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` | `.windsurf/rules/` | https://docs.windsurf.com/windsurf/cascade/skills |
| Trae（含原 MarsCode） | `.trae/skills/`、`.agents/skills/`（需在导入设置启用） | `~/.trae/skills/` | `.trae/rules/` | https://docs.trae.ai/ide/skills |
| Augment Code | `.augment/skills/`、`.claude/skills/`、`.agents/skills/` | `~/.augment/skills/` | `.augment/rules/` | https://docs.augmentcode.com/cli/skills.md |
| Cline | `.cline/skills/`、`.agents/skills/` | `~/.cline/skills/`、`~/.agents/skills/` | `.cline/rules/` | https://docs.cline.bot/getting-started/config.md |
| Roo Code | `.roo/skills/`、`.agents/skills/` | `~/.roo/skills/` | `.roo/rules/` | https://roocodeinc.github.io/Roo-Code/features/skills/ |
| Zed AI | `.agents/skills/` | `~/.agents/skills/` | `AGENTS.md` | https://zed.dev/docs/ai/skills |
| Gemini CLI | `.gemini/skills/`、`.agents/skills/` | `~/.gemini/skills/` | `GEMINI.md` | https://geminicli.com/docs/cli/skills.md |
| Amazon Kiro | `.kiro/skills/` | `~/.kiro/skills/` | `.kiro/steering/` | https://kiro.dev/docs/cli/skills/ |
| 腾讯 CodeBuddy | `.codebuddy/skills/` | `~/.codebuddy/skills/` | `.codebuddy/rules/` | https://www.codebuddy.ai/docs/zh/cli/skills |
| Continue | 无文件夹式 Skill：把 `SKILL.md` 与 `references/` 要点拆成规则 Markdown | 同左（全局配置 `~/.continue/config.yaml`） | `.continue/rules/*.md` | https://docs.continue.dev/customize/deep-dives/rules |
| Qoder | 文件夹式 Skill 机制未在官方文档核实到，以官方文档为准 | 同左 | `.qoder/rules/`、`AGENTS.md` | https://docs.qoder.com/zh/user-guide/rules |

### 调用方式

- **触发场景**：接入或调试某运动平台、解析 / 生成 / 转换 FIT·GPX·TCX、修正活动时间偏 8h / 16h、清洗轨迹与坐标、排查"下载失败 / 上传成功但平台无记录 / 列表取不到最新记录"，或检索开源同步工具与解析库。
- **使用流程**：Agent 先读 `SKILL.md` 的七步工作流，再按导航读取对应 `references/` 文件；不要凭印象假设平台行为。
- **脚本资源**：`scripts/check_fit.py` 随 Skill 文件夹保留；在仅支持规则文件的工具中，需在规则 / 指令里写明脚本相对路径。

## 开源参考与更新须知

- 完整对标矩阵见 [`docs/02-开源项目对标矩阵.md`](docs/02-开源项目对标矩阵.md)（21 个平台、74 条项目，含 URL、检索关键词、鉴权、格式、方向、许可证状态与重新检索步骤）；Skill 内高复用条目见 `references/opensource.md`。
- **使用任何第三方项目前**，先按其 URL 或检索关键词重新核对仓库主页 README、最近提交与 LICENSE；星数、最近提交、活跃度、许可证均为易过期信息，以检索当日为准。
- 标注「未核实」不等于「无许可证」或「公有领域」；引入其代码前必须重新打开仓库 LICENSE 核对，禁止据此判断可自由商用。

## 致谢

本项目站在众多开源项目、运动数据规范与解析库的肩膀上。完整致谢清单、许可证状态与规范出处见：

- [`THIRD_PARTY.md`](THIRD_PARTY.md)：平台鸣谢、已核实许可证项目、未核实 / 待复核条目、规范 Schema 来源；
- [`docs/02-开源项目对标矩阵.md`](docs/02-开源项目对标矩阵.md)：全量项目对照与检索关键词；
- [`docs/04-运动数据规范-FIT-GPX-TCX.md`](docs/04-运动数据规范-FIT-GPX-TCX.md)：FIT / GPX / TCX 规范出处。

各运动平台名称、商标与活动数据版权归各自平台所有；第三方项目的许可证以其仓库 LICENSE 为准，本仓库不代为更改。

## 口径与免责声明

- 文档结论分三档标注：**本知识库实测** / **待真机验证 · 待核实** / **未核实**。未在真机登录平台验证的接口细节、字段语义、错误码，对接前必须真机回归，不要凭文档补造端点、字段或成功判据。
- 本仓库内容仅用于个人运动数据的迁移、备份与技术学习研究，不用于商业用途或批量数据爬取；与各平台不存在官方合作或授权关系。
- 本仓库按"现状"提供，不附带任何明示或默示担保；因使用本仓库内容产生的数据、账号或合规风险由使用者自行承担。

## 未闭环项

标「待真机验证 / 未核实」的接口细节与字段语义、个别已声明但未检索到实际调用的依赖、个别工具类引用计数冲突，均属后续真机 / 源码复核项；本仓库未补造结论。详见 `docs/03-踩坑录-版本回归主线与开发陷阱.md` 附录与 `docs/05-各平台对接备忘.md` 实验室平台小节。

## 许可证

- 本仓库自有知识库文档与 Skill 代码：[MIT](LICENSE)，Copyright (c) 2026 Anathleticbicyclist。
- 引用的第三方开源项目、规范与解析库：版权归各自所有者，许可证见 [`THIRD_PARTY.md`](THIRD_PARTY.md)。
