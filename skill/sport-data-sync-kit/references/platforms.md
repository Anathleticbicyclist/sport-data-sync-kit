# 平台对接速查

> 提炼自本知识库 `05-各平台对接备忘.md`（代码基线：当前发布版本，核验日期 2026-11-11）。
> 本文件只整理本 App 已接平台的实测/代码实证接口事实；实验室与未接平台只写公开入口线索，接口细节一律标「未核实/待真机验证」，不臆造路径、字段、错误码。
> 事实源优先级：已接平台接口事实以本地实证（反编译字节码基线 + 实测 md）为准；另一套源码镜像为旧版本，仅作语义参考。

## 目录

- [全局通用机制](#全局通用机制)
- [前置总表](#前置总表)
- [双向平台卡片](#双向平台卡片)
- [仅上传平台卡片](#仅上传平台卡片)
- [仅下载 / 半自动平台卡片](#仅下载--半自动平台卡片)
- [实验室 / 未接平台](#实验室--未接平台)
- [待实测项汇总](#待实测项汇总)

## 全局通用机制

- **同步去重记忆键**：`{源short}_{活动id}_to_{目标short}`，存 `synced_ids`；success / skipped 分支写记忆键，**pending 分支不写**。
- **UploadResult 五参**：`success / targetId / message / skipped / pending`；全仓仅 Outbase 会按文案显式置 pending，iGP 异步分支、迈金虽语义异步入库却编码为 `success=true/pending=false`。
- **下载有效性判定**：`isFit(bytes)` = 长度 ≥14 且 `bytes[8]=='.'`、`bytes[9]=='F'`；<100 字节判无效。
- **登录检测**：启动对已登录平台串行发真实校验请求，条间 **300ms**；佳明/Wahoo/高驰等失效后保留凭证不清除。

## 前置总表

接入状态：**双向**（可作来源也可作目标）/ **仅上传** / **仅下载** / **半自动** / **实验室**。

| 平台 | short | 状态 | 鉴权方式 | 下载格式 | 上传格式 | 主要限制 |
|---|---|---|---|---|---|---|
| iGPSPORT 国内 | `igp` | 双向 | WebView 取 localStorage token（令牌）；`凭证键` | FIT（两段式：先换 URL 再取文件） | GPX 或 FIT（按文件头选扩展名） | 异步解析；`code∈{200,0}` 判成功，data 为空也成功；他人记录 403；分页 pageNo 须 ≥1 |
| iGPSPORT 国际 | `igpen` | 双向 | 同上；`凭证键` | FIT（两段式） | GPX 或 FIT | 同国内；域名走 `prod.en.igpsport.com` |
| 行者 | `xz` | 双向 | Cookie `sessionid`+`凭证键` | GPX / FIT（目标=iGP 优先 GPX） | 强制 FIT | 成功须 `code==0 && workout_id>0`；9006/文件已上传→跳过；时区双轨易叠加 ±16h |
| 迈金（顽鹿 OTM） | `mg` | 双向 | token 直带 `Authorization`；`凭证键` | FIT（GCJ-02→WGS-84） | 强制 FIT | 分页只认 query string；字段名必须 `jilu0`；`success_count≥1` 判成功；异步入库；refreshToken 不回写 |
| 黑鸟单车 | `bb` | 双向 | Cookie；`凭证键` | FIT（内部已转 WGS-84） | 强制 FIT（官方 gpx2fit） | 自研 FIT 黑鸟解析不了；上传成功谓词未逐条复核（待实测） |
| 百锐腾 | `br` | 仅上传 | WebView 注入登录态；`凭证键` | 无下载分支 | FIT | 走 WebView 开网页上传；列表页出现该源是历史 UI 遗留 |
| 捷安特 | `gt` | 仅上传 | token；`凭证键` | 无下载分支 | FIT（纯 API） | 仅上传目标；细节谓词待真机验证 |
| Outbase | `ob` | 仅上传 | Cookie `sessionId/session_id` + 网关域 cookie；`凭证键` | 无下载分支 | FIT（GPX 走官方 gpx2fit，Keep 源走自研 FIT 处理逻辑） | 唯一置 pending 的平台；`ec==0` 或 `message=="SUCCESS"`；按条控速；上传前 warmUp 预热 |
| 佳明国际 | `gm` | 双向 | WebView ticket → `DI token 交换方法` 换 DI token；`凭证键` | FIT（DI Token 直连 connectapi） | FIT + 设备伪装（`FIT 处理逻辑`） | 上传前 `令牌校验方法`；COM 不走明文直登；429 账号风控；佳明源强制串行 |
| 佳明中国 | `gcn` | 双向 | 同 DI token 链路；另支持账号口令明文直登（**仅 CN**）；`凭证键` | FIT（DI Token 直连 connectapi.cn） | FIT + 设备伪装 | 明文直登仅 `佳明中国区`；`refreshDiToken` 24h 冷却；刷新失败 COM/CN 均保留凭证 |
| 高驰中国 | `cscn` | 双向 | token + cookie；`凭证键` | FIT | FIT（OSS + fit/import） | 阿里云 OSS STS 直传 + `x-oss-security-token`；带 md5 |
| 高驰国际 | `cs` | 双向 | token + cookie；`凭证键` | FIT | FIT（OSS + fit/import） | 同 CN；海外域名 teamapi/training/teameu |
| Wahoo | `wo` | 双向 | OAuth2（code → token）；`凭证键` | FIT | FIT | 401 刷 token 重试一次；授权令牌有 10 枚上限，本端复用已有令牌 |
| MyWhoosh | `mw` | 仅下载 | 账号密码换 token；`凭证键` | FIT | 无上传分支 | 仅作来源；上传能力未接入 |
| Zwift | `zf` | 仅下载 | Keycloak 风格令牌；`凭证键` | FIT（S3 直链 + API 兜底） | 无上传分支 | 试用账号无 FIT 文件；bucket/key 取自活动记录 |
| Intervals.icu | `icu` | 双向 | 个人 API Key（Basic）；`凭证键` | FIT / GPX | FIT / GPX | 个人 key；课表同步另走 `上传路由` |
| Keep | `kp` | 仅下载（源）；作目标=**半自动** | token / password；`凭证键` | GPX | 半自动：生成文件 + 引导手动导入 | 不真正上传；导入 iGP 后的记录在 iGP 侧可能被判归属他人（403） |
| 咕咚 | `cd` | 仅下载 | 账号密码重登；`凭证键` | GPX | 无上传分支 | 启动检测可账号密码重登；接口细节待真机验证 |
| Zepp | `zp` | 仅下载 | token；`zepp` 系凭证（见本地状态层） | GPX | 无上传分支 | 接口细节未逐条复核（待实测） |
| Komoot | `kt` | 双向 | 内部 API，Basic（email + token）；`凭证键` | GPX | GPX / FIT | 201 新建 / 202 重复；400/401/403 分支；运动类型映射表在客户端 |
| 松拓 Suunto | `su` | 双向 | Cloud API OAuth2；`凭证键` | GPX / FIT | FIT | OAuth 回调 `localhost:8080/suunto-callback`；列表 limit=50 + offset 分页；请求头带 Subscription-Key |
| 两步路 | `2b` | 仅下载（实验级） | 浏览捕获模式（缓存库） | 轨迹（浏览捕获） | 无上传分支 | 实验级；非标准 API 对接，待真机验证 |
| CyCity | `cyc` | 双向 | 账号密码登录换 token；`凭证键` | FIT | FIT（两步：uploadImportData → import） | 域名 `cycity.cc`；两步串接 |
| 本地文件夹 | `local` | 双向（导出目标 / 本地来源） | 无网络鉴权 | 本地落盘读取 | FIT / GPX 直接落盘 | `对应平台客户端`；纯本地文件操作 |
| Strava | `st` | 实验室（仅来源） | 实验室对接组件，用户自填 clientId/secret；`实验室凭证键` | 未核实/待真机验证 | 无上传接入 | 公开 OAuth 入口见实验室节 |
| Polar | `po` | 实验室（仅来源） | 同上实验室对接组件；`实验室凭证键` | 未核实/待真机验证 | 无上传接入 | 公开 OAuth 入口见实验室节 |
| Fitbit | `fb` | 实验室（仅来源） | 同上；`实验室凭证键` | 未核实/待真机验证 | 无上传接入 | 公开 OAuth 入口见实验室节 |
| Withings | `wi` | 实验室（仅来源） | 同上；`实验室凭证键` | 未核实/待真机验证 | 无上传接入 | 公开 OAuth 入口见实验室节 |
| TrainingPeaks | `tp` | 实验室（仅来源） | 同上；`实验室凭证键` | 未核实/待真机验证 | 无上传接入 | 公开 OAuth 入口见实验室节 |

## 双向平台卡片

### iGPSPORT 国内 — `igp`

- **鉴权**：WebView 打开登录页 `login.passport.igpsport.cn`，读 `localStorage['persist:app-store']` 的 `global.token`（令牌），再调 API 校验；无效清缓存重登（最多 2 次）；另有原生短信登录通道。Prefs：`凭证键`。
- **列表**：`GET {BASE_CN}/web-gateway/web-analyze/activity/queryMyActivity`，`BASE_CN=https://prod.zh.igpsport.com/service`；参数在 query string：`pageNo` / `pageSize=20` / `reqType=0` / `sort=1`。服务端最新在前；`code=0`、`totalRows` / `totalPage`；`pageNo=0` 服务端 `code=1003` 空响应。
- **下载**：两段式——先调 `getDownloadUrl`（`/web-gateway/web-analyze/activity/getDownloadUrl`）换 OSS 直链，再按直链取 FIT。OSS 直链形如 `igp-zh.oss-cn-hangzhou.aliyuncs.com/*.fit`。第三方 OSS 导入的 `kp_` 记录可能判归属他人 → HTTP 403 `{"code":1002,"message":"不能下载他人运动记录"}`，按无权限跳过。
- **上传**：三步——①`getSignedUrl`（`/service/sportg/third-party-server/oss/getSignedUrl?fileExtension=.`）→ ②OSS PUT 直传（**不带 Content-Type**，仅 403/400 才带）→ ③`uploadByOss`（`/service/web-gateway/web-analyze/activity/uploadByOss`）。
- **成功判据**：`code∈{200,0}` 即成功；**异步解析，`data` 为空也判成功**。异步分支 `pending=false`，回 ACK 即写记忆键，平台侧解析失败会被永久跳过。
- **时区**：`iGP 时区平移方法` 按"当天/历史"分治——同一天不动，历史 `FIT 处理逻辑.shift(+28800)`；与设置页三选一配套。
- **已知坑**：列表把"跳过 N 条"直接当 `pageNo`，无 `(skip/size)+1` 换算；跳过=0 → `pageNo=0` 必失败。字段名缺口（`rideDistance` / `totalMovingTime` / 点分 `startTime`）只影响显示与文件名，不影响下载字节。

### iGPSPORT 国际 — `igpen`

- 同国内链路；国际登录入口 `https://prod.en.igpsport.com/`；Prefs：`凭证键`；列表/下载/上传同国内三步，国际域名 `prod.en.igpsport.com`；`code∈{200,0}` 判成功，异步解析。国际站个别记录是否同样存在归属 403，待真机验证。

### 行者 — `xz`

- **鉴权**：`CookieManager` 取 `sessionid` + `凭证键`，`会话校验方法` 校验；Prefs：`凭证键`。
- **列表**：`GET https://www.imxingzhe.com/api/v1/pgworkout/?offset=&limit=`，Cookie 鉴权；请求头带 `Referer: https://www.imxingzhe.com/xingzhe/workouts/list`；offset 游标分页。
- **下载**：`downloadGpxOrFit(cred, id, preferGpx)`；GPX / FIT 均可，**目标=iGP 时优先 GPX**；FIT 分支内挂 `FIT 处理逻辑.normalize`。时间归一化：按 FIT 内 `local_timestamp - timestamp` 差值决定是否平移；**以字节码基线为准**：`delta==0 → 原样`、`delta≠0 → shift(+28800)`。
- **上传**：`POST https://www.imxingzhe.com/api/v1/fit/upload/`；字段名 `fit_file` + `md5`；强制 FIT。成功判据：`code==0 && workout_id>0`；返回 `9006` / "文件已上传" → 记为跳过。
- **已知坑**：时区是"下载端归一化 + 上传端用户开关"双轨，改任一端都可能叠加成 ±16h；行者时区修正须保持"不调整"。行者 GPX 上传时先 `FIT 处理逻辑.fixGpxTime(-8)` 回 UTC，再按目标时区 +8。

### 迈金（顽鹿 OTM）— `mg`

- **鉴权**：token 直接进 `Authorization` 头（非 令牌 封装）；Prefs：`凭证键`（access）/ `凭证键`。
- **登录/刷新**：账号密码 `POST https://otm.onelap.cn/api/login`，响应 `data` 内取 `token` + `refreshToken`；刷新 `POST https://otm.onelap.cn/api/token`，body `{"token": 旧 refreshToken, "from":"web", "to":"web"}`，响应**只解析 `data.token`（新 access）**，不读取/回写新 `refreshToken`。JWT：解 payload `exp`；实测 access ≈48h、refresh ≈58 天；无 exp/解析失败返回 null。
- **列表**：`POST https://otm.onelap.cn/api/otm/ride_record/list`。**分页参数只认 query string**；`page` / `limit` 放进 JSON body 会被服务端忽略（body 版 `current_page` 恒为 1）；`?page=pageNo&limit=size`（body 空 `{}`）才生效。返回 `code=200`、`total` / `total_pages` / `pagination.has_more` / `current_page`；最新在前。HTTP 401 或 body `code=401` → 抛"迈金登录已过期，请重新登录"。
- **下载**：两段：`/api/otm/ride_record/analysis/` → `/api/otm/ride_record/analysis/fit_content/`；FIT；经 `FIT 处理逻辑` 做 GCJ-02 → WGS-84，受全局开关 + 任务开关控制。
- **上传**：`https://otm.onelap.cn/api/otm/ride_record/upload/fit`；字段名**必须是 `jilu0`**（改名字段服务端不收）；`Authorization` 直接带 token。成功判据：HTTP 200 且 `success_count >= 1`。异步入库约 15–20s；当前 `pending=false`，回 ACK 即写记忆键。
- **已知坑**：除启动检测一处 `<1h` exp 预检外，列表/下载/上传前均无主动刷新；401 后仅按异常文案含"过期"/"401"被动刷一次并重试一次；**上传链路无刷新、无重放**。refreshToken 不回写；服务端是否轮换 refreshToken 待真机抓包验证。早期版本曾把 HTTP 403 也并入重登分支，非鉴权类 403 会被误报成"请重新登录"。

### 黑鸟单车 — `bb`

- **鉴权**：Cookie；Prefs：`凭证键`。
- **列表**：`GET https://www.blackbirdsport.com/api/records?lastRecordId=`（游标分页，`lastRecordId` 续接）；`GET /api/user` 取用户。
- **下载**：内部已转 WGS-84 并构建标准 FIT；记录内文件字段 `fit_file_url` / `downloadUrl`。
- **上传**：`https://www.blackbirdsport.com/api/records/upload`；**强制 FIT**，走官方 gpx2fit；**自研 FIT 黑鸟解析不了**。成功分支 `success=1`；具体谓词未逐条复核（待实测）。

### 佳明国际 — `gm`

- **鉴权**：WebView 取 ticket → `DI token 交换方法` 换 DI token，不走账号密码；域名 `connectapi.garmin.com` / `connect.garmin.com` / `diauth.garmin.com`；Prefs：`凭证键`。
- **列表/下载**：DI token 直连 connectapi；下载 FIT。
- **上传**：FIT + 设备伪装（`FIT 处理逻辑`）；上传前 `令牌校验方法`。查重预检：上传前拉目标端列表，按 `开始时间|时长` 建键，命中不下载不上传。
- **已知坑**：COM 刷新失败**保留原凭证、不自动明文重登**；429 为账号级风控（密码错/两步验证/真风控），命中即停止后续通道；不存在"10 枚令牌上限"（那是 Wahoo）。佳明源下载强制串行（风控）。

### 佳明中国 — `gcn`

- **鉴权**：DI token 链路同国际；另支持账号口令本地直登；域名 `connectapi.garmin.cn` / `sso.garmin.cn`；Prefs：`凭证键`。
- **列表/下载**：DI Token 直连 `connectapi.garmin.cn`；下载 FIT。
- **上传**：FIT + `FIT 处理逻辑` 设备伪装；上传前 `令牌校验方法`。
- **已知坑**：**明文直登仅 `佳明中国区`**，COM 直接跳过明文块，不得把 CN 兜底放开到 COM。`refreshDiToken` 有 24h 冷却标记，冷却期跳过刷新。旧 `本地状态层` 类在当前版本已全量删除、无残留，不要凭印象复活。

### 高驰中国 — `cscn`

- **鉴权**：token + cookie + region；Prefs：`凭证键`。
- **列表/下载**：FIT；CN 域名 `teamcnapi.coros.com` / `trainingcn.coros.com`。
- **上传**：OSS 两步/三步：`/api/proxy/oss/sts?bucket=` 取 STS → 阿里云 OSS PUT（`x-oss-security-token`、`.oss-cn-beijing.aliyuncs.com/`）→ `/activity/fit/import`；带 `md5`。成功分支 `success=1`（谓词待复核）。OSS 签名头/`x-amz-content-sha256` 细节见内部实现；region 决定域名路由，待真机回归。

### 高驰国际 — `cs`

- 同 CN；INT 域名 `teamapi.coros.com` / `training.coros.com`，欧洲 `teameuapi.coros.com` / `trainingeu.coros.com`；上传 OSS STS → OSS PUT → `/activity/fit/import`，带 md5。海外 OSS bucket 差异待真机验证。

### Wahoo — `wo`

- **鉴权**：OAuth2 回调 code → `鉴权辅助组件` 换 token；`/oauth/token` 刷新；Prefs：`凭证键`。
- **列表**：`GET https://api.wahooligan.com/v1/workouts?page=`；校验 `/v1/user`。
- **下载**：`GET /v1/workouts/{id}`，FIT；下载前先刷 refreshToken。
- **上传**：首步 `POST https://api.wahooligan.com/v1/workout_file_uploads` 创建上传任务；随后 `GET /v1/workout_file_uploads/{id}` 轮询任务状态；FIT。
- **已知坑**：401 时刷 token 重试一次。授权令牌有 **10 枚上限**；本端优先复用已有令牌避免新建超限。成功谓词待逐条复核。

### Intervals.icu — `icu`

- **鉴权**：个人 API Key，HTTP Basic；Prefs：`凭证键`。
- **列表**：`GET https://intervals.icu/api/v1/athlete/0/activities?oldest=`；校验同接口。
- **下载**：`GET /api/v1/activity/{id}`，FIT / GPX。
- **上传**：`POST /api/v1/athlete/0/activities`（带 `external_id=`），FIT / GPX。
- **已知坑**：课表（workout）同步另走 `上传路由`（Intervals.icu 课表 → IGP/其他平台 workout JSON），不在活动上传链路。

### Komoot — `kt`

- **鉴权**：内部 API，HTTP Basic（email + token）；Prefs：`凭证键`（另有凭证键字段）。
- **列表**：`GET https://api.komoot.de/v007/users/`；校验同域。
- **下载**：`GET /v007/tours/{id}`，GPX。
- **上传**：`/v007/tours/?data_type=gpx&sport=` 或 `?data_type=fit&name=`。成功判据：**201 新建 / 202 重复**；400/401/403 分支。运动类型：客户端内置 komoot sport 名映射表（`mtb_advanced` / `hike` / `e_mtb` 等）。Basic 凭据组合为 `email:token`；UA 伪装 Firefox；202 记为跳过。

### 松拓 Suunto — `su`

- **鉴权**：Cloud API OAuth2；authorize `https://cloudapi-oauth.suunto.com/oauth/authorize?response_type=code&client_id=`，token `https://cloudapi-oauth.suunto.com/oauth/token`，回调 `https://localhost:8080/suunto-callback`；带 refreshToken 刷新。Prefs：`凭证键`。
- **列表**：`GET https://cloudapi.suunto.com/v3/workouts/?filter-by-modification-time=false&limit=50&offset=`；校验 `limit=1&offset=0`。统一经 `buildRequest` 加请求头：`Authorization: 令牌 token`、`Ocp-Apim-Subscription-Key`、`Accept: application/json`、`User-Agent: 本工具/发布版本 (Android)`。
- **下载**：`/v3/workouts/{id}` 与 `/v2/workout/exportGpx/{id}`；`download(gpx=false)` 取 FIT。
- **上传**：两步——①`POST https://cloudapi.suunto.com/v2/upload`（JSON 初始化，返回 `uploadUrl` / `uploadId`）；②`PUT` FIT 字节到 `uploadUrl`（`/v2/upload/{uploadId}`）。无 `uploadUrl` 抛"Suunto上传失败: 无uploadUrl"。

### CyCity — `cyc`

- **鉴权**：账号密码登录换 token；`POST https://cycity.cc/api/auth/mobile/login`；Prefs：`凭证键`。
- **列表**：`GET https://cycity.cc/api/mobile/cycling/rideRecordsPage?pageNum=&pageSize=`；校验 `pageNum=1&pageSize=1`。
- **下载**：`POST …/cycling/exportFitFile?rideId=`（带 RequestBody），FIT。
- **上传**：两步：①`POST …/cycling/uploadImportData`（JSON body）→ ②`POST …/cycling/import`（MultipartBody 表单 part）；FIT。两步串接，失败点在两步之间的表现待真机验证。

### 本地文件夹 — `local`

- 无网络鉴权；扫描本地 / MediaStore 轨迹；`对应平台客户端` 直接落盘，FIT / GPX；落盘目录与命名走文件名生成器。

## 仅上传平台卡片

### 百锐腾 — `br`

- **鉴权**：WebView 捕获 cookie/token；Prefs：`凭证键`。
- **列表/下载**：无下载分支；列表页出现该源是历史 UI 遗留。
- **上传**：`WebView 网页上传入口`——注入登录态开网页上传；FIT；另有 `FIT 处理逻辑` 造 FIT。非纯 API 对接，依赖 WebView 页面结构；站点切换见 `本地状态层`；接口细节待真机验证。

### 捷安特 — `gt`

- **鉴权**：token；Prefs：`凭证键`。
- **列表/下载**：无下载分支。
- **上传**：登录 `https://ridelife.giant.com.cn/index.php/api/login`；校验 `/index.php/api/fit_list`；上传 `/index.php/api/upload_fit`；FIT，纯 API。成功分支 `success=1`；上传字段名/错误码文案未核实，待真机抓包。

### Outbase — `ob`

- **鉴权**：Cookie `sessionId` / `session_id` + 网关域 `melon-gateway.immomo.com` cookie；Prefs：`凭证键`。
- **列表/下载**：无下载分支；上传前 `warmUp` 调上传列表接口做会话预校验。
- **上传**：主 `https://melon-gateway.immomo.com/zeusfit/api/h5/sport/upload/fit`；另 CDN 通道 `https://melon-gateway.immomo.com/zeusfit/resource/h5/upload`；列表 `…/zeusfit/api/h5/sport/upload/list`。FIT；GPX 走官方 gpx2fit，Keep 源走自研 `FIT 处理逻辑`；带 md5。
- **成功判据**：`ec==0` 或 `message=="SUCCESS"`。**全仓唯一显式置 pending 的平台**——component2 布尔为真且文案含"成功"且含"待处理"时 `pending=true`。不同渠道带不同参数；上传后按条控速，属风控敏感平台。
- **已知坑**：success 与 pending 同时为真时，调用方先命中 `getSuccess` 分支写记忆键，pending 分支走不到。

## 仅下载 / 半自动平台卡片

### MyWhoosh — `mw`

- **鉴权**：账号密码换 token；登录 `https://services.mywhoosh.com/http-service/api/login`；Prefs：`凭证键`。
- **列表**：`POST https://service14.mywhoosh.com/v2/rider/profile/activities`，**JSON body**；校验同接口。
- **下载**：`POST …/rider/profile/download-activity-file`，**JSON body**，FIT。
- **上传**：无上传分支。成功/失败谓词与字段映射待真机验证。

### Zwift — `zf`

- **鉴权**：Keycloak 风格令牌；`https://secure.zwift.com/auth/realms/zwift/tokens/access/codes` 登录/刷新；Prefs：`凭证键`。
- **列表**：域名 `us-or-rly101.zwift.com` / `us.zwift.com`；活动记录字段 `activities` / `id` / `activityId`。
- **下载**：记录内含 `fitFileBucket` / `fitFileKey`，拼 **S3 直链**下载；直链不可用时 API 兜底。
- **上传**：无上传分支。试用账号无 FIT 文件；bucket/key 缺失时兜底路径表现待真机验证。

### Keep — `kp`

- **鉴权**：token / password；Prefs：`凭证键`。
- **列表**：`GET https://api.gotokeep.com/pd/v3/stats/detail?dateUnit=all&type=`。
- **下载**：`GET https://api.gotokeep.com/pd/v3/cyclinglog`，轨迹转 **GPX**，上传端再转 FIT。
- **上传（目标）**：**半自动**——生成文件并弹窗引导手动导入，不做真正 API 上传。半自动分支以 `success=true` 构造结果并进 success 分支写记忆键，用户并未真正完成上传。
- **已知坑**：Keep 源 + 目标∉{迈金,黑鸟,iGP} 时，上传前先用自研 `FIT 处理逻辑` 预转 FIT。Keep 导入 iGP 的记录可能在 iGP 侧被判归属他人（kp_ 前缀，403）。

### 咕咚 — `cd`

- **鉴权**：账号密码；启动检测可账号密码重登；Prefs：`凭证键`。
- **列表/下载**：基址 `https://api.codoon.com`；轨迹转 GPX。登录请求内嵌 Basic 客户端凭证。
- **上传**：无上传分支。列表/下载字段与错误码未逐条核实，待真机验证。

### Zepp — `zp`

- **鉴权**：账号/token；Prefs：`凭证键`，另有坐标开关 `凭证键`。
- **列表/下载**：轨迹转 GPX（GPX 模板 `from zepp -`）。
- **上传**：无上传分支。接口路径、字段、错误码未逐条复核，**未核实/待真机验证**。

### 两步路 — `2b`

- **鉴权**：浏览捕获模式（缓存库），非标准 API 登录。
- **列表/下载**：站点线索 `https://www.2bulu.com/track/t-{id}`；登录校验 `https://www.2bulu.com/community/queryList.htm`；记录前缀 `2bulu_`。
- **上传**：无上传分支。**实验级**，依赖页面/缓存捕获；接口契约与稳定性待真机验证。

## 实验室 / 未接平台

> 以下平台走 `实验室对接组件`，**用户自填开发者 clientId/secret**，当前仅作"来源"，无上传接入。下表入口 URL 取自字节码基线常量（公开 OAuth/API 线索）；**请求字段、分页、错误码、成功判据一律未核实/待真机验证**，不得据此直接对接。凭证 Prefs 前缀：`实验室凭证键`。回调地址统一 `http://localhost:8080/callback`（Suunto 自建链路除外）。

| 平台 | short | 公开入口线索 | 调研结论 |
|---|---|---|---|
| Strava | `st` | Authorize `https://www.strava.com/oauth/authorize`；Token `https://www.strava.com/oauth/token`；活动 `https://www.strava.com/api/v3/athlete/activities`；上传 `https://www.strava.com/api/v3/uploads` | 实验室仅来源；本端未实现上传；细节未核实/待真机验证 |
| Polar | `po` | Authorize `https://flow.polar.com/oauth2/authorization`；Token `https://polarremote.com/v2/oauth2/token`；练习 `https://www.polaraccesslink.com/v3/exercises` | 实验室仅来源；细节未核实/待真机验证 |
| Fitbit | `fb` | Authorize `https://www.fitbit.com/oauth2/authorize`；Token `https://api.fitbit.com/oauth2/token`；活动列表 `https://api.fitbit.com/1/user/-/activities/list.json` | 实验室仅来源；细节未核实/待真机验证 |
| Withings | `wi` | Authorize `https://account.withings.com/oauth2_user/authorize2`；Token `https://account.withings.com/oauth2/token`；活动 `https://api.health.nokia.com/v2/workouts` | 实验室仅来源；细节未核实/待真机验证 |
| TrainingPeaks | `tp` | Authorize `https://oauth.trainingpeaks.com/oauth/authorize`；Token `https://oauth.trainingpeaks.com/oauth/token`；训练 `https://api.trainingpeaks.com/v1/workouts` | 实验室仅来源；细节未核实/待真机验证 |

## 待实测项汇总

- 黑鸟/捷安特/高驰/Wahoo/Intervals.icu/CyCity 上传成功谓词未逐条复核。
- 咕咚/Zepp/两步路接口字段待真机抓包。
- 实验室五家全部待真机验证。
- iGP/迈金异步回包的回调语义、pending 打标范围需接口方确认。
- 本备忘未覆盖：课表同步（`上传路由`）、热力图、轨迹合并/贴纸、码表子功能。
