# Sport Data Sync Kit

> 源自作者自研多平台运动数据同步项目的实战经验沉淀：工程知识库 + 可挂载编码 Agent 的 Skill，覆盖 FIT/GPX/TCX 规范、各平台对接与解析逻辑、时区判据、踩坑回归与开源对标。
> 核验日期：2026-11-11　｜　自有内容许可：MIT（见 [LICENSE](LICENSE)）

## 这是什么

本仓库来自作者开发自研多平台运动数据同步工具（内部代号「鸡翅幸哲迈进 OB」，Android 端，对接 iGPSPORT、行者、迈金、Outbase 等国内外运动平台）过程中踩过的坑、核实过的规范与跑通过的对接链路。它不是某一个成品 App，而是一套**可复用的经验型 Skill + 知识库**：把"一个数据同步小工具 / 工作台从哪里入手、各平台标准与解析逻辑有何不同、哪里最容易返工"整理成 Agent 可直接读取的工作指南。

**这套经验技能能帮你做什么**

- 让编码 Agent 快速掌握运动数据同步工具的开发思路：接入前核查 → 鉴权 → 列表 / 下载 → 格式校验清洗 → 时区判定 → 上传入库 → 回归验证，七步走通，少走重复弯路；
- 快速搞清各平台的标准与解析逻辑差异：鉴权方式、列表 / 分页契约、下载格式、坐标体系（GCJ-02 / WGS-84）、时间口径、上传字段与入库判重、异步成功判据；
- 支撑你通过 Agent 定制自己的数据同步工作台 / 个人数据中台：落地形态可以是命令行脚本、定时同步任务、桌面端工具，也可以是 App 内的同步模块；技能只给方法、口径与校验工具，具体产品形态由你的项目决定；
- 让数据快速、准确地在平台间流动：格式归一、时区对齐、坐标纠偏、入库判重与回归验证都有明确护栏，避免"显示成功但平台没数据""时间偏 8 小时 / 16 小时""改完字节文件失效"这类反复验证。

**覆盖范围**：21 个点名运动平台、75 条开源对标项目；格式覆盖 FIT / GPX / TCX；平台含 iGPSPORT（国内 / 国际）、行者、迈金、黑鸟、捷安特、Outbase、Intervals.icu、佳明国际 / 中国、高驰、Wahoo、MyWhoosh、Zwift、Keep、咕咚、Zepp、Komoot、Suunto、百锐腾、CyCity、Strava 等（未接 / 实验室平台在文档中标注待核实）。

仓库分两部分：

- `docs/`：Markdown 知识库，供人阅读与 Agent 检索；
- `skill/sport-data-sync-kit/`：可整体安装的 Agent Skill（`SKILL.md` + `references/` + `scripts/`）。

> 本仓库**不包含**任何受版权保护的反编译源码、补丁树、安装包、签名材料、账号凭证或个人运动样本；相关方法仅作学习研究与个人数据迁移备份参考。

## 技能能力清单

| 能力域 | 技能提供什么 | 对应参考 |
|---|---|---|
| 接入前核查 | 平台状态分级（双向 / 仅上传 / 仅下载 / 半自动 / 实验室）、同步方向与目标格式确认、跨格式能力差异 | `references/platforms.md`、`references/formats.md` |
| 鉴权与凭证 | 令牌、Cookie sessionid/csrftoken、OAuth2 code→token、个人 API Key、WebView 注入登录态、账号密码换 token；401/403 与刷新回写规则 | `references/platforms.md`、`references/pitfalls.md` |
| 列表与下载 | 列表接口、参数位置（query / body）、分页契约、下载有效性判据、403 他人记录跳过规则 | `references/platforms.md`、`references/pitfalls.md` |
| 格式解析与校验 | FIT/GPX/TCX 结构、字段号、单位换算、记录层级、脏数据边界；FIT 魔数 / 长度 / CRC16 确定性校验脚本 | `references/formats.md`、`scripts/check_fit.py` |
| 清洗与坐标纠偏 | GCJ-02→WGS-84 纠偏、空轨迹 / 0 里程合法判定、无处安放字段的丢弃 / 降级 | `references/formats.md` |
| 时区判定 | 三文件形态识别、活动开始时间锚点法、幂等 / 量程 / 锚缺失三条护栏、±16h 防叠加 | `references/timezone.md` |
| 上传与入库 | 上传路径与字段名、异步 pending 等待与核对、平台判重码、去重记忆键 | `references/platforms.md`、`references/pitfalls.md` |
| 回归与排坑 | 版本回归二分定位、跨方向回归清单、高频坑位"现象—根因—定位—修法—防范" | `references/pitfalls.md`、`docs/03-踩坑录-版本回归主线与开发陷阱.md` |
| 开源对标 | 75 条同步工具 / 聚合器 / 解析库：接入方法、鉴权、格式、方向、许可证状态与使用前更新步骤 | `references/opensource.md`、`docs/02-开源项目对标矩阵.md` |

**技能边界**：不含课表（workout）同步、热力图、轨迹合并 / 贴纸、码表子功能；这些见知识库代码导览对应章节。

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

### 一键安装：从 GitHub 拉取（复制即用）

下面三种方式任选其一；装到哪个目录，对照本页「各智能体挂载速查」表中你的工具行。跨工具通用目录为 `.agents/skills/`，只认自有目录的工具（如 `.claude/skills/`、`.cursor/skills/`）按表复制到对应位置。

**方式 A：复制话术发给你的编码智能体（让它自己下载安装）**

把下面整段粘贴到对话框，并把 `{当前工具}` 替换为你使用的工具名（如 Claude Code、Codex CLI、Cursor、Trae）：

```text
请从 GitHub 安装开放 Skill「sport-data-sync-kit」，步骤如下：
1. 仓库：https://github.com/Anathleticbicyclist/sport-data-sync-kit （main 分支，MIT）。
2. 优先执行：git clone --depth 1 https://github.com/Anathleticbicyclist/sport-data-sync-kit.git；本机没有 git 时，改下载 ZIP：https://codeload.github.com/Anathleticbicyclist/sport-data-sync-kit/zip/refs/heads/main 并解压。
3. 把仓库内 skill/sport-data-sync-kit/ 整个文件夹（必须保留 SKILL.md、references/、scripts/ 的相对结构，不要拆散）安装到当前编码工具「{当前工具}」的 Skill 目录：项目级放 <项目根>/<该工具 skills 目录>/sport-data-sync-kit/，用户级放 ~/<该工具 skills 目录>/sport-data-sync-kit/；文件夹名与 SKILL.md frontmatter 的 name 保持一致。各工具目录见仓库 README「各智能体挂载速查」表。
4. 安装后自检：确认 SKILL.md 可读、frontmatter 中 name=sport-data-sync-kit；references/ 下 5 份 md 与 scripts/check_fit.py 都在。重新加载智能体后，用一句运动数据相关任务触发（例如“帮我解析这个 FIT 并排查时区偏移”），确认技能被加载。
5. 不要安装仓库外的临时脚本、日志或二进制产物；引用第三方项目前，按 references/opensource.md 里的链接重新核对 README 与 LICENSE。
```

**方式 B：命令行 git clone（用户级，跨项目复用）**

Windows PowerShell：

```powershell
git clone --depth 1 https://github.com/Anathleticbicyclist/sport-data-sync-kit.git "$env:TEMP\sds-kit"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.agents\skills" | Out-Null
Copy-Item -Recurse "$env:TEMP\sds-kit\skill\sport-data-sync-kit" "$env:USERPROFILE\.agents\skills\sport-data-sync-kit"
```

macOS / Linux（bash）：

```bash
git clone --depth 1 https://github.com/Anathleticbicyclist/sport-data-sync-kit.git /tmp/sds-kit
mkdir -p ~/.agents/skills
cp -R /tmp/sds-kit/skill/sport-data-sync-kit ~/.agents/skills/sport-data-sync-kit
```

项目级安装（随仓库提交给团队）：把上面的目标路径换成项目根下的 `.agents/skills/sport-data-sync-kit/`；某工具只认自有目录时，按速查表对应目录复制。

**方式 C：本机无 git，下载 ZIP 解压安装（PowerShell）**

```powershell
Invoke-WebRequest "https://codeload.github.com/Anathleticbicyclist/sport-data-sync-kit/zip/refs/heads/main" -OutFile "$env:TEMP\sds-kit.zip"
Expand-Archive "$env:TEMP\sds-kit.zip" "$env:TEMP\sds-kit" -Force
Copy-Item -Recurse "$env:TEMP\sds-kit\sport-data-sync-kit-main\skill\sport-data-sync-kit" "$env:USERPROFILE\.agents\skills\sport-data-sync-kit"
```

**安装后自检清单**：

- 目录内应包含：`SKILL.md`、`references/formats.md`、`references/timezone.md`、`references/platforms.md`、`references/pitfalls.md`、`references/opensource.md`、`scripts/check_fit.py`；
- 校验脚本可运行：`python <skill 目录>/scripts/check_fit.py <file.fit>`；
- 重新加载智能体后，用触发场景（解析 FIT / 排查时区偏移 / 接入某运动平台）验证技能被调用。

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

## 调用示例（Agent 会怎么做、会产出什么）

> 以下为示意，产出不包含任何真实账号与个人数据；接入真实平台前，按文档口径完成真机回归。

**示例 1：校验 / 解析一个 FIT 文件**

输入（你对 Agent 说）：

```text
我手上有一个从运动平台导出的 FIT 文件，帮我检查它是否合法、CRC 是否一致。
```

Agent 动作：读 `references/formats.md` 的格式与脏数据边界 → 运行 `scripts/check_fit.py` → 给出判定。

示例产出：

```text
check_fit.py 结果：
  activity.fit    PASS（魔数 .FIT，头长度 12，数据区长度 41820，文件尾 CRC16 一致）
  corrupted.fit   FAIL（CRC16 不一致：正文被改过但未重算文件尾 CRC）
提示：GPX/TCX 已识别并跳过 CRC 校验；若改过 FIT 字节，先重算文件尾 CRC16 再上传。
```

**示例 2：规划一条跨平台同步链路（iGPSPORT → 迈金）**

输入：

```text
帮我设计 iGPSPORT 活动同步到迈金的方案，列出每一步要确认什么、有哪些坑。
```

Agent 动作：按七步工作流依次读 `platforms.md`（鉴权 / 列表 / 下载 / 上传 / 判重）、`timezone.md`（时间口径）、`formats.md`（格式与坐标）、`pitfalls.md`（分页、异步入库、判重）。

示例产出骨架：

```text
1. 接入核查：方向 下载 iGP → 上传迈金；目标格式 FIT；确认两边平台状态分级。
2. 鉴权：按卡片核对登录方式与令牌 / 会话存储；401/403 与刷新规则列入待办。
3. 列表/下载：列表参数位置与分页契约；下载有效性判据（长度、魔数）；403 他人记录跳过。
4. 校验清洗：FIT 魔数 / 长度 / CRC 校验；迈金坐标 GCJ-02，上传前纠偏回 WGS-84。
5. 时区：用活动开始时间锚点法判定平移量；两套平移逻辑不同时跑；验证以目标平台网页端开始时间为准。
6. 上传入库：核对上传字段名；异步入库等待后再核对落库；判重码与去重记忆键规则；重复活动记跳过。
7. 回归：按跨方向回归清单逐条跑（iGP 导出、iGP→迈金、迈金→iGP、登录态、后台链路）。
待真机项：未在真机验证的字段 / 错误码 / 成功判据，标注「待真机验证」，不臆造端点。
```

**示例 3：排查活动时间偏 8 小时**

输入：

```text
同步过去的活动在目标平台早了 8 小时，帮我判断是哪类时间问题、怎么修。
```

Agent 动作：读 `timezone.md`，先识别文件属于哪种时间形态（纯 UTC / 本地冒充 UTC / 规范分离），再用锚点法计算平移量。

示例产出骨架：

```text
诊断：以列表 startTimeMs（UTC 正确）为锚对齐记录开始时间，判定文件形态与平移量。
护栏：平移幂等（同条重传不二次叠加）；量程校验；锚缺失时按兜底规则并标注待核实。
验证：到目标平台网页端核对开始时间，不只看接口返回或本地缓存；注意不要叠加两套平移逻辑导致 ±16h。
```

**示例 4：检索可参考的开源实现**

输入：

```text
找几个可以参考的跨平台运动数据同步开源项目，说明各自鉴权方式、同步方向和许可证注意点。
```

Agent 动作：读 `references/opensource.md` 与对标矩阵，按方向 / 格式筛选候选；使用前按链接重新核对 README、最近提交与 LICENSE。

示例产出骨架：

```text
候选（摘录，许可证以仓库最新 LICENSE 为准）：
- <项目名>：鉴权 <…>；方向 <源 → 目标>；格式 <FIT/GPX/TCX>；许可证 <SPDX 或 未核实>。
提醒：标「未核实」不等于无许可证；星数 / 活跃度为易过期信息，接入前重新检索核对。
```

## 开源参考与更新须知

- 完整对标矩阵见 [`docs/02-开源项目对标矩阵.md`](docs/02-开源项目对标矩阵.md)（21 个平台、75 条项目，含 URL、检索关键词、鉴权、格式、方向、许可证状态与重新检索步骤）；Skill 内高复用条目见 `references/opensource.md`。
- **使用任何第三方项目前**，先按其 URL 或检索关键词重新核对仓库主页 README、最近提交与 LICENSE；星数、最近提交、活跃度、许可证均为易过期信息，以检索当日为准。
- 标注「未核实」不等于「无许可证」或「公有领域」；引入其代码前必须重新打开仓库 LICENSE 核对，禁止据此判断可自由商用。

## 致谢

本项目站在众多开源项目、运动数据规范与解析库的肩膀上。完整致谢清单、许可证状态与规范出处见：

- [`THIRD_PARTY.md`](THIRD_PARTY.md)：平台鸣谢、已核实许可证项目、未核实 / 待复核条目、规范 Schema 来源；
- [`docs/02-开源项目对标矩阵.md`](docs/02-开源项目对标矩阵.md)：全量项目对照与检索关键词；
- [`docs/04-运动数据规范-FIT-GPX-TCX.md`](docs/04-运动数据规范-FIT-GPX-TCX.md)：FIT / GPX / TCX 规范出处。

作者本人前置 / 体验仓库（第一方项目，非第三方开源依赖）：

- 正式版 [sync-igpsport-magene-onelap-xingzhe-data-to-outbase](https://github.com/Anathleticbicyclist/sync-igpsport-magene-onelap-xingzhe-data-to-outbase)：MIT 已核实，多平台采集 → Outbase 单向迁移。
- 开发体验版 [sports-data-sync-multiplatform](https://github.com/Anathleticbicyclist/sports-data-sync-multiplatform)：**根目录无 LICENSE，含反编译 `smali_source/` 与 APK 产物，许可证未核实**；仅作方法参考，复用 / 分发前须自行评估法律风险。

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
