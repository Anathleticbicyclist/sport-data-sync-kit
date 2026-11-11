# 高价值开源参考项目清单

> 核验日期：2026-11-11。提炼自本知识库 `02-开源项目对标矩阵.md`。
> 本文件只收高复用度项目；完整 74 条清单（含全部实验室/未接平台参考）见
> `docs\02-开源项目对标矩阵.md`，不要在本文件内补全完整矩阵。

## 目录

- [使用前更新步骤（强制）](#使用前更新步骤强制)
- [许可证标注约定](#许可证标注约定)
- [A. 跨平台聚合 / 同步参考](#a-跨平台聚合--同步参考)
- [B. FIT 解析 / 生成库](#b-fit-解析--生成库)
- [C. GPX / TCX 解析库](#c-gpx--tcx-解析库)
- [D. 格式转换工具](#d-格式转换工具)

## 使用前更新步骤（强制）

开源项目的 README、端点、鉴权方式、许可证与活跃度都会随时间变化；**参考任何项目前必须先做以下核对，不得把本清单当成过期快照直接引用**：

1. **打开仓库主页**：按本文件给出的 URL 访问，核对 README（当前支持的鉴权方式、列表/下载/上传端点、收发格式、同步方向）、最近提交时间、是否还在维护。
2. **核对许可证**：以仓库根目录 LICENSE 文件 / 仓库 About 信息为准；本清单只记录已核实的 SPDX 简称，未核实的标「未核实」。**未核实不等于无许可证**，禁止据此判定可自由商用。
3. **URL 失效重定位**：若链接打不开或仓库被改名/转移，按条目「检索关键词」（作者 + 仓库名 + 技术栈）在 GitHub / PyPI / Gitee / Codeberg 搜索重新定位；找到后重新核对 README 与 LICENSE。
4. **易过期信息以检索当日为准**：星数、最近提交、活跃度、issue 状态、许可证均可能变化，本清单不写死具体数字；引用结论时注明检索日期。
5. **代码口径核对**：开源项目的鉴权字段、请求路径、成功判据只作方法参考；接入本知识库时仍以 `platforms.md` 的本地实测口径为准，开源实现与本地实测冲突时标注「本知识库实测」。

## 许可证标注约定

- `MIT` / `GPL-2.0` / `GPL-3.0` / `Apache-2.0` / `BSD-3-Clause`：已核实 SPDX 简称（2026-11-11）。
- `未核实`：本环境未读到可确认的 LICENSE；`NOASSERTION` 归入「未核实」。
- 许可证与合规结论需在引入代码前由调用方重新核对。

## A. 跨平台聚合 / 同步参考

> 这一组是"接入方法与如何调用"的参考基石：看它们怎么拿鉴权、怎么调列表/下载/上传、支持什么格式与方向。

## B. FIT 解析 / 生成库

### B1. garmin/fit-python-sdk

- **URL**：https://github.com/garmin/fit-python-sdk
- **检索关键词**：garmin fit-python-sdk；Python；Garmin 官方 FIT SDK
- **可借鉴方法**：官方 Profile 消息号、字段号、基数类型、缩放与开发者字段定义；解析/生成 FIT 的字段语义基准。
- **方向 / 格式**：FIT 解析/生成；与方向无关。
- **许可证**：未核实（NOASSERTION，引入代码前必须核对仓库 LICENSE 与官方使用条款）。

### B2. dtcooper/python-fitparse

- **URL**：https://github.com/dtcooper/python-fitparse
- **检索关键词**：dtcooper python-fitparse；Python；FIT 解析
- **可借鉴方法**：流式/消息级解析；record/session/lap/activity 读取与字段映射参考；端序与定义消息处理参考。
- **方向 / 格式**：FIT 解析。
- **许可证**：MIT（已核实）。

### B3. nbr23/python-fitparse

- **URL**：https://github.com/nbr23/python-fitparse
- **检索关键词**：nbr23 python-fitparse；Python；python-fitparse fork
- **可借鉴方法**：上游 fork 的后续维护与解析兼容性；FIT 解析兜底处理参考。
- **方向 / 格式**：FIT 解析。
- **许可证**：MIT（已核实）。

### B4. polyvertex/fitdecode

- **URL**：https://github.com/polyvertex/fitdecode
- **检索关键词**：polyvertex fitdecode；Python；FIT 解码
- **可借鉴方法**：FIT 解码为结构化记录；未知开发者字段跳过、端序判定等容错处理参考。
- **方向 / 格式**：FIT 解码。
- **许可证**：MIT（已核实）。

### B5. tormoder/fit

- **URL**：https://github.com/tormoder/fit
- **检索关键词**：tormoder fit；Go；FIT 库
- **可借鉴方法**：Go 语言 FIT 模型与消息定义；跨语言解析字段对照参考。
- **方向 / 格式**：FIT 解析/生成。
- **许可证**：MIT（已核实）。

### B6. muktihari/fit

- **URL**：https://github.com/muktihari/fit
- **检索关键词**：muktihari fit；Go；FIT 库
- **可借鉴方法**：Go FIT 读写与 Profile 映射；消息结构与字段缩放参考。
- **方向 / 格式**：FIT 解析/生成。
- **许可证**：BSD-3-Clause（已核实）。

## C. GPX / TCX 解析库

### C1. tkrajina/gpxpy

- **URL**：https://github.com/tkrajina/gpxpy
- **检索关键词**：tkrajina gpxpy；Python；GPX 解析生成
- **可借鉴方法**：GPX trk/trkseg/trkpt 层级读写、时间与坐标字段处理、轨迹清洗（去重/抽稀）参考。
- **方向 / 格式**：GPX 解析/生成。
- **许可证**：Apache-2.0（已核实）。

### C2. alenrajsp/tcxreader

- **URL**：https://github.com/alenrajsp/tcxreader
- **检索关键词**：alenrajsp tcxreader；Python；TCX 读取
- **可借鉴方法**：TCX Activity/Lap/Trackpoint 模型读取；心率/功率(TPX)/速度字段映射参考。
- **方向 / 格式**：TCX 解析。
- **许可证**：MIT（已核实）。

### C3. thomthom/fastgpx

- **URL**：https://github.com/thomthom/fastgpx
- **检索关键词**：thomthom fastgpx；C++ / Python 绑定；GPX 高性能实验解析
- **可借鉴方法**：大文件 GPX 流式/高性能解析思路；逐点读取性能参考。
- **方向 / 格式**：GPX 解析。
- **许可证**：MIT（已核实）。

## D. 格式转换工具

### D1. GPSBabel/gpsbabel

- **URL**：https://github.com/GPSBabel/gpsbabel
- **检索关键词**：GPSBabel gpsbabel；C++ CLI；GPS 轨迹格式互转
- **可借鉴方法**：FIT/GPX/TCX 等多格式互转的字段映射与坐标系处理；命令行批量转换参考。注意各格式能力差异（TCX 无温度、GPX 原生无速度），见 `formats.md`。
- **方向 / 格式**：格式互转；CLI。
- **许可证**：GPL-2.0（已核实）。

---

**收录统计**：A 组 19 个，B 组 6 个，C 组 3 个，D 组 1 个，合计 29 个高复用项目。其余项目（含实验室平台参考、未核实清单）完整条目见本知识库 `02-开源项目对标矩阵.md`。
### A1. jorge-huxley/intervalssync

- **URL**：https://github.com/jorge-huxley/intervalssync
- **检索关键词**：jorge-huxley intervalssync；Python；多源同步 Intervals.icu
- **可借鉴方法**：双数据源活动同步到 Intervals.icu；token 手动配置；列表拉取 → 按时间/距离比对 → 上传活动的流水线；双向链路组织参考。
- **方向 / 格式**：源→Intervals.icu；FIT/GPX 视源而定。
- **许可证**：MIT（已核实）。

### A2. Tyan66666/WanSync

- **URL**：https://github.com/Tyan66666/WanSync
- **检索关键词**：Tyan66666 WanSync；Dart / Flutter；运动平台聚合同步
- **可借鉴方法**：Android 工程结构与多平台适配层组织；列表/下载/上传模块拆分参考。
- **方向 / 格式**：多平台聚合；以仓库 README 为准。
- **许可证**：GPL-3.0（已核实）。

### A3. yihong0618/running_page

- **URL**：https://github.com/yihong0618/running_page
- **检索关键词**：yihong0618 running_page；Python JS；多平台跑步数据拉取展示
- **可借鉴方法**：多平台 OAuth/API 拉取活动、归一化到本地/静态页的数据模型；各平台拉取与字段映射参考价值高。
- **方向 / 格式**：多源拉取；GPX/FIT 轨迹。
- **许可证**：MIT（已核实）。

### A4. alexandcote/intervals-icu-cli

- **URL**：https://github.com/alexandcote/intervals-icu-cli
- **检索关键词**：alexandcote intervals-icu-cli；TypeScript Node；Intervals.icu 命令行
- **可借鉴方法**：个人 API Key（HTTP Basic）调用 Intervals.icu 活动接口；CLI 参数化拉取/上传参考。
- **方向 / 格式**：双向（按 README）；FIT/GPX。
- **许可证**：MIT（已核实）。

### A5. ntrance/wahoo-garmin-fit-bridge

- **URL**：https://github.com/ntrance/wahoo-garmin-fit-bridge
- **检索关键词**：ntrance wahoo-garmin-fit-bridge；Python；Wahoo Garmin FIT 桥接
- **可借鉴方法**：Wahoo OAuth2 鉴权 → 下载 FIT → 桥接 Garmin；单源单目标 FIT 透传链路参考。
- **方向 / 格式**：Wahoo → Garmin；FIT。
- **许可证**：MIT（已核实）。

### A6. czdanika/onelapfit-sync

- **URL**：https://github.com/czdanika/onelapfit-sync
- **检索关键词**：czdanika onelapfit-sync；Python；顽鹿 迈金 Intervals.icu
- **可借鉴方法**：顽鹿（迈金 OTM）token 直连拉取活动，同步到 Intervals.icu；迈金列表/下载调用参考。
- **方向 / 格式**：迈金 → Intervals.icu；FIT。
- **许可证**：MIT（已核实）。

### A7. just-nobody/onelap-fit-export

- **URL**：https://github.com/just-nobody/onelap-fit-export
- **检索关键词**：just-nobody onelap-fit-export；Python；顽鹿 FIT 导出
- **可借鉴方法**：顽鹿活动列表与 FIT 导出流程；token 使用方式参考。
- **方向 / 格式**：迈金导出；FIT。
- **许可证**：MIT（已核实）。

### A8. tcgoetz/GarminDB

- **URL**：https://github.com/tcgoetz/GarminDB
- **检索关键词**：tcgoetz GarminDB；Python；Garmin 全量拉取本地数据库
- **可借鉴方法**：Garmin 鉴权、活动全量拉取、本地落库与增量比对；Garmin 列表/下载调用与字段模型参考。
- **方向 / 格式**：Garmin → 本地；FIT。
- **许可证**：GPL-2.0（已核实）。

### A9. xballoy/coros-api

- **URL**：https://github.com/xballoy/coros-api
- **检索关键词**：xballoy coros-api；Python；高驰 Coros 非官方 API
- **可借鉴方法**：高驰鉴权与活动拉取；非官方库的端点组织与错误处理参考。
- **方向 / 格式**：高驰拉取；FIT。
- **许可证**：MIT（已核实）。

### A10. tgmerritt/wahoo-skill

- **URL**：https://github.com/tgmerritt/wahoo-skill
- **检索关键词**：tgmerritt wahoo-skill；Python；Wahoo 语音助手技能
- **可借鉴方法**：Wahoo OAuth2 token 存取与活动读取；OAuth 回调与刷新处理参考。
- **方向 / 格式**：Wahoo 拉取；FIT。
- **许可证**：MIT（已核实）。

### A11. JayQueue/MyWhoosh2Garmin

- **URL**：https://github.com/JayQueue/MyWhoosh2Garmin
- **检索关键词**：JayQueue MyWhoosh2Garmin；Python；MyWhoosh Garmin
- **可借鉴方法**：MyWhoosh 账号密码换 token 拉活动，桥接 Garmin；账号密码登录 → token 的链路参考。
- **方向 / 格式**：MyWhoosh → Garmin；FIT。
- **许可证**：GPL-3.0（已核实）。

### A12. mywhoosh-community/mywhoosh-api

- **URL**：https://github.com/mywhoosh-community/mywhoosh-api
- **检索关键词**：mywhoosh-community mywhoosh-api；Python；社区 API 文档
- **可借鉴方法**：MyWhoosh 社区整理的接口与字段说明；登录、活动列表、下载文件的调用方式参考。
- **方向 / 格式**：MyWhoosh 拉取；以仓库为准。
- **许可证**：MIT（已核实）。

### A13. DaThabe/XingzheExport

- **URL**：https://github.com/DaThabe/XingzheExport
- **检索关键词**：DaThabe XingzheExport；Python；行者 GPX 导出
- **可借鉴方法**：行者 Cookie/session 鉴权，活动列表与 GPX 导出；行者接口调用参考。
- **方向 / 格式**：行者导出；GPX。
- **许可证**：Apache-2.0（已核实）。

### A14. H3llK33p3r/zepp-fit-extractor

- **URL**：https://github.com/H3llK33p3r/zepp-fit-extractor
- **检索关键词**：H3llK33p3r zepp-fit-extractor；Python；Zepp FIT 提取
- **可借鉴方法**：Zepp 活动数据提取为 FIT；移动端/账号态导出思路参考。
- **方向 / 格式**：Zepp 提取；FIT。
- **许可证**：Apache-2.0（已核实）。

### A15. timschneeb/KomootGPX

- **URL**：https://github.com/timschneeb/KomootGPX
- **检索关键词**：timschneeb KomootGPX；Python；Komoot GPX 导出
- **可借鉴方法**：Komoot Basic（email + token）鉴权，行程列表与 GPX 下载；Komoot 调用参考。
- **方向 / 格式**：Komoot 导出；GPX。
- **许可证**：GPL-3.0（已核实）。

### A16. bjonnh/Kompy

- **URL**：https://github.com/bjonnh/Kompy
- **检索关键词**：bjonnh Kompy；Python；PyPI kompy；Komoot 非官方库
- **可借鉴方法**：Komoot 非官方 Python 库封装；活动/路线接口组织参考。PyPI 包名 `kompy` 可在 PyPI 检索。
- **方向 / 格式**：Komoot；以仓库 README 为准。
- **许可证**：未核实。

### A17. dwmer0308-a11y/magene-fit-strava-fix

- **URL**：https://github.com/dwmer0308-a11y/magene-fit-strava-fix
- **检索关键词**：dwmer0308-a11y magene-fit-strava-fix；Python；迈金 FIT 修复
- **可借鉴方法**：迈金 FIT 坐标（GCJ-02）与时间字段修复思路；上传前清洗参考。
- **方向 / 格式**：迈金 FIT 处理；FIT。
- **许可证**：未核实。

### A18. kylin2005-art/sports-data-sync-web

- **URL**：https://github.com/kylin2005-art/sports-data-sync-web
- **检索关键词**：kylin2005-art sports-data-sync-web；Web；运动数据同步前端
- **可借鉴方法**：同步任务列表、平台凭证展示等前端结构参考；不提供后端接入方法。
- **方向 / 格式**：Web 展示；无后端链路。
- **许可证**：未核实（NOASSERTION，引入前核对）。

### A19. Anathleticbicyclist/sync-igpsport-magene-onelap-xingzhe-data-to-outbase

- **URL**：https://github.com/Anathleticbicyclist/sync-igpsport-magene-onelap-xingzhe-data-to-outbase
- **检索关键词**：sync-igpsport-magene-onelap-xingzhe-data-to-outbase；Kotlin；多平台骑行数据同步 Outbase
- **可借鉴方法**：多源平台账号登录与活动采集 → 归一化 → 上传 Outbase 的工程分层；多平台适配层与上传链路组织参考。
- **方向 / 格式**：多平台 → Outbase 上传；FIT/GPX。
- **许可证**：MIT（已核实）。
- **备注**：作者本人前置仓库（第一方项目，非第三方开源依赖）；引用前仍按 URL 核对最新 README 与 LICENSE。

