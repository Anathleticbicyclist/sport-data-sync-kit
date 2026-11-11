# THIRD_PARTY.md — 第三方开源项目、规范与解析库致谢清单

> 核验日期：2026-11-11　｜　适用范围：多平台运动数据同步项目及配套 `sport-data-sync-kit` 技能
> 配套清单：开源项目完整对照（含检索关键词、鉴权方式、同步方向、可复用度与局限）见 `02-开源项目对标矩阵.md`；FIT/GPX/TCX 规范出处见 `04-运动数据规范-FIT-GPX-TCX.md`。

## 0. 口径与统计

- 本次共盘点 **21 个**点名运动平台，收录项目 / 仓库 / 依赖条目 **75 条**。
- 许可证口径：**已核实 40 条**（表内列出 SPDX 简称）；**未核实 35 条**（表三，含 NOASSERTION 自定义许可、根目录无 LICENSE 文件、404 / 待复核仓库）。
- **「未核实」不等于「无许可证」，更不等于「公有领域」**；引入其代码前必须重新打开仓库 LICENSE / About 信息核对。
- 易过期信息（星数、最近提交、活跃度、许可证归属）以检索当日为准；本清单不写死星数与提交哈希。
- 各运动平台数据版权归原平台所有；本知识库与参考工具仅用于用户**个人数据的迁移与备份**，不得用于商业用途或批量数据爬取。

---

## 一、平台鸣谢

感谢以下运动平台提供数据记录与存储服务，各平台开放的数据接口是数据自由流动的前提。

| 平台 | 官网 | 说明 |
|------|------|------|
| iGPSPORT（迹驰） | https://www.igpsport.com | 专业骑行码表品牌，骑行数据记录与云端存储 |
| 行者 | https://www.imxingzhe.com | 国内骑行运动 APP，骑行记录、路线规划与社交 |
| 迈金（OneLap） | https://www.onelap.cn | 智能骑行设备与室内训练平台 |
| 黑鸟单车 | https://www.blackbirdsport.com | 骑行运动社区与记录平台 |
| 百锐腾（Bryton） | https://www.brytonsport.com | 专业骑行码表品牌，GPS 骑行数据记录 |
| 佳明（Garmin） | https://www.garmin.com | 全球 GPS 运动手表 / 码表品牌，国际与中国双区服务 |
| 高驰（COROS） | https://www.coros.com | 专业运动手表品牌，中国与国际双区数据服务 |
| Wahoo | https://www.wahoo.com | 骑行训练设备品牌，开放开发者平台 |
| 捷安特（Giant） | https://www.giant.com.cn | 自行车品牌，骑行数据服务 |
| Intervals.icu | https://intervals.icu | 专业训练数据分析平台，支持第三方导入 |
| Outbase | https://outbase.cn | 户外运动数据聚合平台，多品牌设备接入 |
| Keep | https://www.gotokeep.com | 国内运动健身 APP，室内外运动记录 |
| 咕咚（Codoon） | https://www.codoon.com | 老牌运动社交 APP，跑步 / 骑行 / 健身记录 |
| Zepp（华米 / Amazfit） | https://www.zepp.com | 智能穿戴设备与运动健康平台 |
| Komoot | https://www.komoot.com | 欧洲户外路线规划与导航平台 |
| Suunto（松拓） | https://www.suunto.com | 芬兰专业户外运动手表品牌 |

> 平台商标、活动记录与接口数据版权归各平台所有；本清单仅为对接参考，不代表与上述平台存在官方合作或授权关系。

---

## 二、已核实许可证的开源项目（40 条）

> 许可证为 2026-11-11 核对仓库 LICENSE / About 信息所得 SPDX 简称；引入代码前仍应按表内 URL 复核最新许可证文本。

### 2.1 平台同步工具与聚合参考

| # | 项目 | URL | 许可证 | 引用部分 |
|---|---|---|---|---|
| 1 | jorge-huxley/intervalssync | https://github.com/jorge-huxley/intervalssync | MIT | iGPSPORT/百锐腾 ↔ Intervals.icu 双向同步、国内/国际区后端、课表与功率区间回传、CLI 去重参考 |
| 2 | DaThabe/XingzheExport | https://github.com/DaThabe/XingzheExport | Apache-2.0 | 行者网页 Cookie(SessionId) 模拟 API、GPX/TCX 导出字段结构参考 |
| 3 | Harry-Chen/xingzhe-gpx-processor | https://github.com/Harry-Chen/xingzhe-gpx-processor | MIT | 行者 GPX 心率/功率/踏频合并写法参考 |
| 4 | Tyan66666/WanSync | https://github.com/Tyan66666/WanSync | GPL-3.0 | OneLap → Strava/行者/Intervals.icu/Outbase 移动端同步、GCJ-02→WGS84 转换、独立去重、本地凭证存储参考 |
| 5 | just-nobody/onelap-fit-export | https://github.com/just-nobody/onelap-fit-export | MIT | 迈金国际后端登录取 token、活动列表、OSS 直链下载、FIT 完整性校验参考 |
| 6 | czdanika/onelapfit-sync | https://github.com/czdanika/onelapfit-sync | MIT | OnelapFit 登录签名(nonce/timestamp/sign)、FIT 下载与 GPX 路线上传全流程参考 |
| 7 | alexandcote/intervals-icu-cli | https://github.com/alexandcote/intervals-icu-cli | MIT | Intervals.icu 官方 API Key 接入、活动/健康/日历/课表 JSON 操作参考 |
| 8 | LetsLearntocodeforfun/Apollo-Running | https://github.com/LetsLearntocodeforfun/Apollo-Running | MIT | Garmin/Intervals.icu 本地优先同步、FIT/GPX/TCX 导入产品形态参考 |
| 9 | tcgoetz/GarminDB | https://github.com/tcgoetz/GarminDB | GPL-2.0 | 佳明 Connect 账号下载、活动解析入本地 SQLite 框架参考 |
| 10 | erocathanh/garmin-tracklog-sync | https://github.com/erocathanh/garmin-tracklog-sync | MIT | 佳明网页接口批量拉取 GPX tracklog 思路参考 |
| 11 | ntrance/wahoo-garmin-fit-bridge | https://github.com/ntrance/wahoo-garmin-fit-bridge | MIT | Wahoo/iGP/COROS/Karoo → Garmin 自托管 Docker 桥接、2FA token 复用、去重与 Dry-run 参考 |
| 12 | xballoy/coros-api | https://github.com/xballoy/coros-api | MIT | COROS Training Hub 邮箱密码登录、多格式(FIT/TCX/GPX/KML/CSV)批量导出、Bruno 接口文档参考 |
| 13 | futoshita/Coros-Training-Hub-Exporter | https://github.com/futoshita/Coros-Training-Hub-Exporter | MIT | COROS 活动与训练日历导出早期实现参考 |
| 14 | tgmerritt/wahoo-skill | https://github.com/tgmerritt/wahoo-skill | MIT | Wahoo Fitness Cloud API OAuth2、workout 拉取与 FIT 下载解析参考 |
| 15 | JayQueue/MyWhoosh2Garmin | https://github.com/JayQueue/MyWhoosh2Garmin | GPL-3.0 | MyWhoosh 本地 FIT 清洗（补功率/心率均值、去温度）后上传 Garmin 流程参考 |
| 16 | embeddedc/mw2gc | https://github.com/embeddedc/mw2gc | GPL-3.0 | MyWhoosh FIT 文件改进以适配 Garmin Connect 上传参考 |
| 17 | mywhoosh-community/mywhoosh-api | https://github.com/mywhoosh-community/mywhoosh-api | MIT | MyWhoosh 非官方 API 整理文档参考 |
| 18 | mywhoosh-community/mywhoosh-mcp-server | https://github.com/mywhoosh-community/mywhoosh-mcp-server | Apache-2.0 | MyWhoosh MCP 服务封装形态参考 |
| 19 | zhenyan666666/codoon-campus-run | https://github.com/zhenyan666666/codoon-campus-run | MIT | （用途不同，仅登记）Frida/模拟器与咕咚 App 交互研究 |
| 20 | H3llK33p3r/zepp-fit-extractor | https://github.com/H3llK33p3r/zepp-fit-extractor | Apache-2.0 | Zepp apptoken 抓取、批量活动资源下载与重建 FIT 参考 |
| 21 | T4ASICK/amazfit-biodata-exporter | https://github.com/T4ASICK/amazfit-biodata-exporter | MIT | Zepp/Amazfit 健康指标导出到第三方端点参考 |
| 22 | timschneeb/KomootGPX | https://github.com/timschneeb/KomootGPX | GPL-3.0 | Komoot 轨迹/亮点批量下载 GPX 参考 |
| 23 | janthomas89/komoot-api-client | https://github.com/janthomas89/komoot-api-client | MIT | Komoot 非官方 API 客户端结构参考（已归档） |
| 24 | Kub-AT/suunto-movescount-exporter | https://github.com/Kub-AT/suunto-movescount-exporter | MIT | Suunto 旧 Movescount 活动导出历史参考 |
| 25 | GPSBabel/gpsbabel | https://github.com/GPSBabel/gpsbabel | GPL-2.0 | FIT/GPX/TCX/KML 等轨迹格式互转本地工具链 |
| 26 | yihong0618/running_page | https://github.com/yihong0618/running_page | MIT | 咕咚/Keep/Garmin-CN/Strava/NRC/COROS 等多平台采集、GPX 备份、Strava↔Garmin 双向同步与个人主页架构参考 |
| 27 | Anathleticbicyclist/sync-igpsport-magene-onelap-xingzhe-data-to-outbase | https://github.com/Anathleticbicyclist/sync-igpsport-magene-onelap-xingzhe-data-to-outbase | MIT | 作者本人前置仓库；iGP/行者/迈金/黑鸟/捷安特/佳明/高驰/Wahoo/MyWhoosh/Zwift/Keep/咕咚/Zepp/Komoot/Suunto/百锐腾/CyCity 等多平台采集 → Outbase 上传链路与基础架构参考 |

### 2.2 FIT 解析 / 生成库

| # | 项目 | URL | 许可证 | 引用部分 |
|---|---|---|---|---|
| 28 | dtcooper/python-fitparse | https://github.com/dtcooper/python-fitparse | MIT | ANT/Garmin FIT 只读解析库 |
| 29 | nbr23/python-fitparse | https://github.com/nbr23/python-fitparse | MIT | python-fitparse 活跃维护 fork |
| 30 | polyvertex/fitdecode | https://github.com/polyvertex/fitdecode | MIT | Python3 FIT 解码库 |
| 31 | tormoder/fit | https://github.com/tormoder/fit | MIT | Go 语言 FIT 解码/编码库 |
| 32 | muktihari/fit | https://github.com/muktihari/fit | BSD-3-Clause | Go 语言 FIT V2 编解码库 |
| 33 | fitfile / tcgoetz/GarminDB | https://github.com/tcgoetz/GarminDB ；https://pypi.org/project/fitfile/ | GPL-2.0（GarminDB；fitfile 单包未独立核实） | GarminDB 生态 FIT 解析模块 |

### 2.3 GPX / TCX 解析库

| # | 项目 | URL | 许可证 | 引用部分 |
|---|---|---|---|---|
| 34 | tkrajina/gpxpy | https://github.com/tkrajina/gpxpy | Apache-2.0 | GPX 解析/生成标准库 |
| 35 | alenrajsp/tcxreader | https://github.com/alenrajsp/tcxreader | MIT | Garmin TCX 容错读取库 |
| 36 | thomthom/fastgpx | https://github.com/thomthom/fastgpx | MIT | 高性能 GPX 解析实验库 |

### 2.4 本知识库直接依赖库

| # | 项目 | URL | 许可证 | 引用部分 |
|---|---|---|---|---|
| 37 | square/okhttp | https://github.com/square/okhttp | Apache-2.0 | HTTP 客户端（所有网络请求） |
| 38 | Kotlin/kotlinx.coroutines | https://github.com/Kotlin/kotlinx.coroutines | Apache-2.0 | Kotlin 异步协程库 |
| 39 | material-components/material-components-android | https://github.com/material-components/material-components-android | Apache-2.0 | Material Design Android 组件库（维护模式） |
| 40 | androidx/androidx | https://github.com/androidx/androidx | Apache-2.0 | AndroidX Jetpack 扩展库 |

---

## 三、未核实 / 待复核项目（35 条）

> 以下条目在本次环境中未读到可确认的 LICENSE（含 NOASSERTION 自定义许可、根目录无 LICENSE 文件、仓库 404 / 链接待复核）。**许可证状态以重新检索当日仓库为准**；在核实前不得据此判断可自由商用。完整字段（鉴权、格式、方向、局限）见矩阵 §6.3。

| # | 项目 | URL | 状态 / 许可证 | 引用部分 |
|---|---|---|---|---|
| 1 | kvnZero/IGPSPORT2Xingzhe | https://github.com/kvnZero/IGPSPORT2Xingzhe | 未核实（无 LICENSE） | iGPSPORT → 行者脚本、行者登录密码算法参考 |
| 2 | mxdneu/xingzhe-batch-export-gpx | https://github.com/mxdneu/xingzhe-batch-export-gpx | 未核实 | 行者 GPX 批量导出早期脚本 |
| 3 | sky1wu/Magene2Strava | https://github.com/sky1wu/Magene2Strava | 未核实 | 迈金/Onelap → Strava 本地 Web 面板 |
| 4 | 101letters/OnelapSync_Lite | https://github.com/101letters/OnelapSync_Lite | 未核实 | OneLap 登录下载 FIT + Strava 上传轻量脚本 |
| 5 | moruoxian/SyncOnelapToXoss | https://github.com/moruoxian/SyncOnelapToXoss | 未核实 | OneLap → Xoss/捷安特/iGP/Strava 多目标同步 |
| 6 | dwmer0308-a11y/magene-fit-strava-fix | https://github.com/dwmer0308-a11y/magene-fit-strava-fix | 未核实（无根 LICENSE） | 迈金 FIT GCJ-02→WGS84 转换算法（本知识库已移植） |
| 7 | jeromecornet/magpx | https://github.com/jeromecornet/magpx | 待复核 | 迈金 GPX 路线上传 payload 参考 |
| 8 | HclX/BlackbirdSportsUploader | https://github.com/HclX/BlackbirdSportsUploader | 未核实 | 黑鸟 BLE 取设备 FIT、转专有 XML 上传 |
| 9 | Tyan66666/wansync-cli | https://github.com/Tyan66666/wansync-cli | 未核实 | WanSync CLI 形态，服务器定时同步 |
| 10 | kylin2005-art/sports-data-sync-web | https://github.com/kylin2005-art/sports-data-sync-web | 未核实（NOASSERTION） | 佳明跨区与多平台自托管工作台参考 |
| 11 | lucadavidde/garmin-gpx-sync | https://github.com/lucadavidde/garmin-gpx-sync | 未核实 | 佳明 GPX 定时增量下载 |
| 12 | MattW2/wahoo-connector | https://github.com/MattW2/wahoo-connector | 未核实（NOASSERTION，已归档） | Wahoo FIT 后台下载守护 |
| 13 | cptchloroplast/fitness | https://github.com/cptchloroplast/fitness | 未核实 | Wahoo → Garmin 个人脚本 |
| 14 | XuHandsome/workouts_page | https://github.com/XuHandsome/workouts_page | 404 待复核；未核实 | Keep keep_to_gpx.py 集成参考（DeepWiki 索引） |
| 15 | ipconfiger/CodoonAccess | https://github.com/ipconfiger/CodoonAccess | 未核实 | 咕咚早期 SDK 片段（历史线索） |
| 16 | FloatingMaple/GetCodoonData2.0 | https://github.com/FloatingMaple/GetCodoonData2.0 | 未核实 | 咕咚网页数据抓取统计早期脚本 |
| 17 | micw/hacking-mifit-api | https://github.com/micw/hacking-mifit-api | 未核实（无根 LICENSE） | Zepp/小米运动内部 API 逆向参考（本知识库已参考） |
| 18 | bjonnh/Kompy | https://pypi.org/project/Kompy/ ；GitHub 404 待复核 | 未核实 | Komoot 双向 API 封装参考（本知识库已参考） |
| 19 | henrydatei/suunto-mcp | https://github.com/henrydatei/suunto-mcp | 404 待复核；未核实 | Suunto OAuth2 授权与下载流程参考（本知识库已参考） |
| 20 | guiguoz/opensportsync | https://github.com/guiguoz/opensportsync | 未核实 | Suunto Ambit USB OTG 日志导出 |
| 21 | alexbr/movescount-batch-exporter | https://github.com/alexbr/movescount-batch-exporter | 未核实 | 旧 Movescount 批量导出脚本 |
| 22 | RmThrt/BrTrainingPlan | https://github.com/RmThrt/BrTrainingPlan | 未核实 | Bryton Active 课表注入脚本 |
| 23 | barrald/strava-uploader | https://github.com/barrald/strava-uploader | 未核实 | RunKeeper → Strava 上传工具 |
| 24 | strava/go.strava | https://github.com/strava/go.strava | 未核实（已归档） | Strava V3 Go 官方客户端库 |
| 25 | dee4life2005/CycleUploader | https://github.com/dee4life2005/CycleUploader | 未核实 | 多平台 FIT/TCX/GPX 上传老工具 |
| 26 | garmin/fit-python-sdk | https://github.com/garmin/fit-python-sdk | 未核实（NOASSERTION，Garmin 自定义许可） | 官方 Python FIT 编解码 |
| 27 | garmin/fit-java-sdk | https://github.com/garmin/fit-java-sdk | 未核实（NOASSERTION） | 官方 Java FIT 编解码 |
| 28 | garmin/fit-javascript-sdk | https://github.com/garmin/fit-javascript-sdk | 未核实（NOASSERTION） | 官方 JS FIT 编解码 |
| 29 | garmin/fit-swift-sdk | https://github.com/garmin/fit-swift-sdk | 未核实（NOASSERTION） | 官方 Swift FIT 编解码 |
| 30 | garmin/fit-objective-c-sdk | https://github.com/garmin/fit-objective-c-sdk | 未核实（NOASSERTION） | 官方 ObjC FIT 编解码 |
| 31 | garmin/fit-sdk-tools | https://github.com/garmin/fit-sdk-tools | 未核实（NOASSERTION） | 官方 FIT CSV/校验/生成工具链 |
| 32 | ggps（PyPI） | https://pypi.org/project/ggps/ | 未核实 | Garmin 导出 GPX/TCX 解析工具集 |
| 33 | ben-29/workouts_page | https://github.com/ben-29/workouts_page | 未核实（本次 403 待复核） | running_page 多运动类型 fork |
| 34 | robiningelbrecht/statistics-for-strava | https://github.com/robiningelbrecht/statistics-for-strava | 未核实 | 自托管 Strava 分析仪表盘（文件导入模式） |
| 35 | Anathleticbicyclist/sports-data-sync-multiplatform | https://github.com/Anathleticbicyclist/sports-data-sync-multiplatform | 未核实（无根 LICENSE；含反编译 smali_source 与 APK 产物） | 作者本人开发体验版；多平台双向互传链路参考（许可证未核实，复用前自行评估法律风险） |

> 备注：第 6、17、18、19 项在本知识库开发过程中被直接参考或移植，但其开源许可证未在本次环境核实；若对外分发或商用，须先补齐 LICENSE 核对或移除对应移植代码。

---

## 四、公开规范、Schema 与官方文档来源

> 格式字段号、单位换算、时间纪元、扩展结构以官方规范为准；本知识库实测口径与规范冲突处，在知识库文档中标注「本知识库实测」。

### 4.1 FIT（Garmin 官方协议）

- FIT Protocol 规范：https://developer.garmin.com/fit/articles/fit-protocol/fit_protocol.html
- FIT Protocol 镜像页：https://developer.garmin.com/fit/protocol/
- FIT 时间纪元与 datetime 定义：https://developer.garmin.com/fit/articles/cookbook/datetime.html
- 活动文件解码指南：https://developer.garmin.com/fit/articles/cookbook/decoding_activity_files.html
- Garmin 官方 FIT SDK（Python 包）：https://pypi.org/project/garmin-fit-sdk/
- fitparse 消息记录类型参考：https://docs.rs/fitparse/latest/fitparse/fittypes/struct.FitMessageRecord.html

### 4.2 GPX

- GPX 1.1 Schema：https://www.topografix.com/GPX/1/1/gpx.xsd
- GPX 1.1 规范页：https://www.topografix.com/gpx/1/1/
- TrackPointExtension v2 Schema：https://www8.garmin.com/xmlschemas/TrackPointExtensionv2.xsd
- TrackStatsExtension Schema：https://www8.garmin.com/xmlschemas/TrackStatsExtension.xsd

### 4.3 TCX

- TrainingCenterDatabase v2 Schema：https://www8.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd

### 4.4 平台开放文档与格式对照

- Strava 上传文档：https://developers.strava.com/docs/uploads/
- 轨迹格式单位 / 分辨率对照：https://logiqx.github.io/open-gnss/formats.html

---

## 五、合规与更新须知

1. **重新核对许可证**：本清单许可证状态为 2026-11-11 快照；复用任何开源代码前，先按 URL 打开仓库 LICENSE / About 信息复核，GPL 系列（GPL-2.0 / GPL-3.0）的传染性义务须单独评估。
2. **规范版权**：FIT 协议、GPX/TCX Schema、各扩展 Schema 的版权归 Garmin / Topografix 等对应标准组织；本知识库仅按规范做个人数据格式转换。
3. **平台数据边界**：活动记录、轨迹、账号凭证均属用户本人与对应平台；工具仅用于个人数据迁移、备份与自有设备记录整合，不得抓取、转售或公开分发他人数据。
4. **失效链接处理**：URL 失效时按矩阵 §一 的「重新检索操作步骤」，以作者 + 仓库名 + 技术栈在 GitHub / PyPI / Gitee / Codeberg 重新定位，并在更新本清单时回填新地址与许可证状态。
5. **未闭环项**：标注「待真机验证 / 未核实」的接口细节、字段语义与许可证，均未在本环境登录平台或读取 LICENSE 原文核实，不得作为对外承诺依据。

---

*本清单由知识库调研整理生成（2026-11-11）；开源项目明细与检索关键词见 `02-开源项目对标矩阵.md`，规范字段出处见 `04-运动数据规范-FIT-GPX-TCX.md`。*
