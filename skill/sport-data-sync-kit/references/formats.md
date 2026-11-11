# 格式规范：FIT / GPX / TCX

> 提炼自本知识库 `04-运动数据规范-FIT-GPX-TCX.md`（核验日期 2026-11-11）。
> 标注「本知识库实测」的口径来自项目实测文档，与官方标准冲突时以实测为准；未闭环项标「待真机验证」。

## 目录

- [0. 结论速览](#0-结论速览)
- [1. FIT 结构与解析要点](#1-fit-结构与解析要点)
- [2. GPX 结构与扩展](#2-gpx-结构与扩展)
- [3. TCX 结构与能力边界](#3-tcx-结构与能力边界)
- [4. 单位规范与换算](#4-单位规范与换算)
- [5. 坐标系：WGS-84 与 GCJ-02](#5-坐标系wgs-84-与-gcj-02)
- [6. 记录层级与脏数据边界](#6-记录层级与脏数据边界)

## 0. 结论速览

| 维度 | FIT | GPX 1.1 | TCX v2 |
|---|---|---|---|
| 本质 | 二进制、定长记录、紧凑 | XML、文本、自描述 | XML、Garmin 私有、层级强 |
| 时间基准 | uint32 秒，纪元 1989-12-31T00:00:00Z | ISO 8601 文本（带 Z 或偏移） | ISO 8601 文本（通常带 Z） |
| 距离单位 | 厘米（uint32，÷100 = 米） | 米（`<ele>`/distance 文本） | 米（`DistanceMeters`） |
| 速度单位 | mm/s 或增强速度 mm/s（÷1000 = m/s） | 原生 GPX 无速度字段，靠扩展 | `Speed m/s`（TPX 扩展） |
| 心率 | record.field 6，uint8 bpm | extensions→`<gpxtpx:hr>` | `<HeartRateBpm><Value>` |
| 功率 | record.field（uint16 W） | extensions→`<power>`（Garmin/Cluetrust） | `<Extensions><TPX><Watts>` |
| 坐标 | semicircles（sint32），WGS-84 | 十进制度，WGS-84 | 十进制度，WGS-84 |
| 校验 | 文件尾 2 字节 CRC16 | 无（XML well-formed 即合法） | 无 |

**三条铁律（本知识库实测）**：

1. 改了 FIT 任意字节（含时区平移、坐标纠偏），**必须重算文件尾 CRC16**，否则平台判文件无效。
2. 时区不看文件"长什么样"，用记录真实开始时间当锚对齐（见 `timezone.md`）。
3. 迈金（Magene）GPS 坐标是 **GCJ-02（火星坐标）**，上传前必须转回 WGS-84。

## 1. FIT 结构与解析要点

### 1.1 文件整体结构

自顶向下四段：File Header → Definition Mesg / Data Mesg 成对记录区 → 文件尾 2 字节 CRC16。

- 数据记录区**不含**文件头与 CRC，长度写在文件头第 4–7 字节（小端 uint32）。
- 合法 FIT 必须自含：`file_id`(mesg 0) 的定义+数据；其后每个数据消息前有对应定义消息；末尾 2 字节 CRC。

### 1.2 文件头字节表

| 字节偏移 | 字段 | 长度 | 说明 |
|---|---|---|---|
| 0 | Header Size | 1 | **本头长度**，最小 12（legacy），推荐 14 |
| 1 | Protocol Version | 1 | SDK 协议版本 |
| 2–3 | Profile Version | 2 | 小端，如 2130 = 21.30 |
| 4–7 | Data Size | 4 | 小端，数据记录区字节数 |
| 8–11 | Data Type | 4 | ASCII `.FIT` = `0x2E 0x46 0x49 0x54` |
| 12–13 | Header CRC | 2 | 仅 14 字节头时存在；为字节 0–11 的 CRC，可置 0x0000 |

- **【本知识库实测】`isFit` 判据**：长度 ≥14 且 `bytes[8]=='.'`(0x2E) 且 `bytes[9]=='F'`(0x46)。完整魔数是 bytes[8..11]=`.FIT`，取前两字节即可拦截绝大多数非 FIT 响应。
- **文件头长度 = `header[0]` 直接读**（12 或 14），不要做位运算。
- **记录头本地消息号取低 4 位 `hdr & 0x0F`**，绝不能 `hdr >> 4` 取高 4 位；高 4 位装的是 normal/compressed、定义/数据、开发者数据标志位。

### 1.3 记录头与字节序

- 记录头 1 字节：bit7=1 压缩时间戳头（低 5 位是时间增量）；bit6：0=定义消息，1=数据消息；bit5=开发者数据标志；bit0–3=本地消息号。
- **大端/小端不由文件全局决定**，而由每条定义消息的 Architecture 字节决定：定义消息第 2 字节 `0=小端`、`1=大端`。该定义及后续同一本地号的数据消息都按此字节序解析；一个文件内不同消息可混端。
- 全局消息号在定义消息第 2–3 字节，端序也由 Architecture 字节决定。

### 1.4 全局消息号速查

| mesg_num | 名称 | 作用 |
|---|---|---|
| 0 (0x00) | file_id | 每个活动文件**第一个**必出现：type/manufacturer/product/serial/time_created |
| 12 (0x0C) | sport | 运动类型定义 |
| 18 (0x12) | session | 一次活动汇总（总时长/总距离/平均心率等） |
| 19 (0x13) | lap | 分段（自动圈/手动圈）汇总 |
| 20 (0x14) | **record** | **逐点轨迹**：位置、距离、高度、心率、功率、踏频等（最核心） |
| 34 (0x22) | **activity** | 活动根消息，引用 session，含时间戳 |
| 49 (0x31) | file_creator | 生成软件/设备 |
| 206 (0xCE) | field_description | 开发者字段自描述（名称/单位/基数类型） |
| 207 (0xCF) | dev_data_id | 开发者数据所属 app 标识 |

完整表以 FIT SDK 自带 `Profile.xlsx / Profile.csv` 为准。

### 1.5 关键字段号与缩放

- 时间戳是跨消息公共字段：所有消息用 **field 253 = `timestamp`**（uint32，UTC 秒，FIT 纪元）。
- **field 5 = `local_timestamp`**（本地钟面秒，与 timestamp 同基数类型；差值 = 时区偏移，见 `timezone.md`）。

| 字段名 | 常见 field# | 基数类型 | 缩放/偏移 | 物理单位 |
|---|---|---|---|---|
| timestamp | 253 | uint32 | — | 秒（UTC，FIT 纪元） |
| local_timestamp | 5 | uint32 | — | 秒（本地钟面） |
| position_lat | 2 | sint32 | ×(180/2³¹) | 度（semicircles） |
| position_long | 3 | sint32 | ×(180/2³¹) | 度（semicircles） |
| altitude / enhanced_altitude | 5 / 78 等 | uint16/uint32 | raw/5 − 500 | 米 |
| heart_rate | 6 | uint8 | — | bpm |
| cadence | 7 | uint8 | — | rpm（踏频/步频） |
| power | 见 Profile | uint16 | — | W（瓦） |
| speed / enhanced_speed | 见 Profile | uint16/uint32 | raw/1000 | m/s |
| temperature | 见 Profile | sint8 | — | °C |

- **距离字段**：record.distance 为累计距离，存厘米（raw/100 = 米）；session/lap 的 `total_distance` 存米（缩放 100）。
- 字段号不要求在定义消息里按升序出现，但**数据消息里字段字节顺序必须严格等于定义消息声明的顺序**。实现上"读定义消息拿 field_def_num→size→base_type 三元组，再按此布局拆数据"，不要硬编码字段号偏移。

### 1.6 时间戳纪元

- FIT 时间 = 自 **1989-12-31T00:00:00Z** 起的 uint32 秒数。
- 与 Unix 时间换算：`unix_s = fit_s + 631065600`。
- **【本知识库实测】** 某迈金样本：`01:14:46 UTC`（北京时间 09:14:46）对应纯 UTC 的 FIT 秒数（大端命中某字节偏移）；本地钟面值 = UTC 秒数 + 28800。迈金文件里写的是纯 UTC 数值。

### 1.7 开发者字段（Developer Fields）

- 定义消息头 bit5=1 时，定义消息尾部多一段开发者字段定义（每字段 3 字节）。
- 必须配套出现 `dev_data_id`(207) 与 `field_description`(206)，把"开发者数据索引 + 字段号"映射到可读字段名与单位。
- 解析器遇未知开发者字段应**跳过**（按 size 跳字节），不要报错。

### 1.8 CRC16 铁律

- 文件**末尾 2 字节**为 CRC16，**小端**，覆盖范围 = 文件头第 0 字节到数据记录区结束（不含这 2 字节本身）。
- 多项式/查表（Garmin 官方 16 项小表，初值 0x0000）：
 `0x0000,0xCC01,0xD801,0x1400,0xF001,0x3C00,0x2800,0xE401,0xA001,0x6C00,0x7800,0xB401,0x5000,0x9C01,0x8801,0x4400`。
- **任何字节被修改（时区平移、坐标纠偏、字段清理）后，必须整段重算并覆写末尾 CRC。** 漏掉 CRC 是平台报"文件数据无效"的高频原因之一。
- 确定性校验见 `scripts/check_fit.py`。

## 2. GPX 结构与扩展

### 2.1 命名空间与层级

- 根元素命名空间：`http://www.topografix.com/GPX/1/1`（schema：`https://www.topografix.com/GPX/1/1/gpx.xsd`）。
- 轨迹层级：`<gpx><trk><trkseg><trkpt>…</trkpt></trkseg></trk></gpx>`。一个文件可多条 `<trk>`；一条 `<trk>` 可多段 `<trkseg>`（暂停会分段）。
- `<trkpt>` 用**属性**给坐标：`<trkpt lat="36.123" lon="120.456">`，子元素给其余信息。

### 2.2 `<trkpt>` 常用字段

| 字段 | 形式 | 单位/说明 |
|---|---|---|
| lat / lon | 属性 | 十进制度，WGS-84 |
| `<ele>` | 子元素 | 米（海拔） |
| `<time>` | 子元素 | ISO 8601 文本 |
| `<hdop>` `<vdop>` | 子元素 | 精度 |
| `<extensions>` | 子元素 | 心率/功率/温度/速度等扩展挂这里 |

扩展字段靠 Garmin TrackPointExtension（命名空间 `http://www.garmin.com/xmlschemas/TrackPointExtension/v2`）：

```xml
<gpxtpx:TrackPointExtension>
 <gpxtpx:hr>145</gpxtpx:hr><gpxtpx:cad>88</gpxtpx:cad><gpxtpx:atemp>21</gpxtpx:atemp>
</gpxtpx:TrackPointExtension>
```

功率：`<power>240</power>`（Cluetrust/Garmin 约定，单位瓦）。

### 2.3 时区写法（ISO 8601）

- 两种合法写法：UTC 带 Z（`2026-11-11T01:14:46Z`）；带偏移（`2026-11-11T09:14:46+08:00`）。两者表达同一时刻。
- **禁止写"裸本地时间不带 Z/不带偏移"**（如 `2026-11-11T09:14:46`），那是歧义来源。
- 【本知识库实测】行者 GPX 处理：上传时 -8h 回 UTC（写 Z），再按目标平台口径决定是否 +8；避免 GPX 里出现偏移与实际时刻不符。

## 3. TCX 结构与能力边界

### 3.1 结构与 schema

- schema：`https://www8.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd`；命名空间 `http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2`。
- 层级（强嵌套）：`TrainingCenterDatabase → Activities → Activity(id=运动类型) → Lap(StartTime 属性) → Track → Trackpoint`。

### 3.2 关键字段

| 层级 | 字段 | 说明 |
|---|---|---|
| Activity | `Sport` 属性 | Cycling/Running/… |
| Lap | `StartTime`；`TotalTimeSeconds`、`DistanceMeters`、`Calories`、平均/最大心率 | 圈汇总 |
| Trackpoint | `<Time>`、`<Position><LatitudeDegrees>/<LongitudeDegrees>`、`<AltitudeMeters>`、`<DistanceMeters>`、`<HeartRateBpm><Value>`、`<Cadence>` | 逐点 |
| Trackpoint 扩展 | `<Extensions><TPX><Speed>`(m/s)、`<Watts>`(功率)、`<RunCadence>` | 速度/功率/跑步步频 |

### 3.3 能力差异

| 能力 | FIT | GPX 1.1 | TCX v2 |
|---|---|---|---|
| 心率 | ✅ record | ✅ extensions/hr | ✅ 原生 `<HeartRateBpm>` |
| 功率 | ✅ 原生 | ✅ extensions/power | ⚠️ 仅 TPX `<Watts>` 扩展 |
| 速度 | ✅ 原生 | ❌ 原生无（靠扩展） | ⚠️ 仅 TPX `<Speed>` |
| 温度 | ✅ 原生 | ✅ extensions/atemp | ❌ **不支持温度** |
| 坐标基准 | semicircles / WGS-84 | 度 / WGS-84 | 度 / WGS-84 |

TCX 适合"活动/圈汇总"表达，逐点丰富度不如 FIT；功率/速度必须进 `<Extensions><TPX>`，温度在 TCX 里无处安放——跨格式转换时温度只能丢弃或降级到 GPX/FIT。

## 4. 单位规范与换算

### 4.1 内部统一单位

| 量 | 内部标准单位 | 说明 |
|---|---|---|
| 距离 | 米 (m) | FIT 存厘米要 ÷100；TCX/GPX 本就是米 |
| 高程 | 米 (m) | FIT enhanced_altitude: raw/5 − 500 |
| 速度 | m/s | 展示可换 km/h、mph |
| 功率 | 瓦 (W) | 各格式一致 |
| 心率 | bpm | 各格式一致 |
| 踏频 | rpm / 步频 spm | 骑行 rpm，跑步 spm |
| 坐标 | 十进制度 (WGS-84) | FIT semicircles 先转度 |

### 4.2 换算公式

```
速度： km/h = m/s × 3.6
 m/s = km/h ÷ 3.6
 mph = m/s × 2.23694 ≈ km/h ÷ 1.60934

配速： 配速 min/km = 1000 ÷ (m/s × 60)
 即 pace(min/km) = 16.6667 ÷ speed(m/s)
 反推：speed(m/s) = 1000 ÷ (配速秒/公里)
 例：30 km/h = 8.333 m/s = 12.0 min/km（3分20秒/公里）

FIT 坐标：deg = semicircles × 180.0 / 2^31
 （1 semicircle ≈ 180/2147483648 ≈ 8.3819e-8 度）
FIT 距离：m = raw_cm / 100
FIT 速度：m/s = raw_mm_per_s / 1000
FIT 高程：m = raw / 5 − 500
```

## 5. 坐标系：WGS-84 与 GCJ-02

- **WGS-84**：GPS 原始坐标系，国际通用，FIT/GPX/TCX 标准均为 WGS-84。
- **GCJ-02（"火星坐标"）**：中国境内地图服务商（高德/腾讯）对 WGS-84 施加的非线性加密偏移，同一真实点偏移约百米级（几十~700 米），境外不偏移。
- **【本知识库实测】迈金码表输出的 GPS 坐标是 GCJ-02**；直接当 WGS-84 上传，轨迹在地图上整体偏移约 500 米。项目内 `FIT 处理逻辑` 负责 GCJ-02 → WGS-84 纠偏后再上传；黑鸟下载端已在内部转过 WGS-84，无需二次处理。
- 边界：GCJ-02↔WGS-84 是单向近似变换（加密不可逆，官方只给近似反向）；只在中国境内数据需要处理，境外坐标近似等于 WGS-84，不要重复纠偏。

## 6. 记录层级与脏数据边界

### 6.1 session / lap / record 层级

```
activity (34) ← 一次运动的根，1 个
 └─ session (18) ← 汇总（通常 1 个；多运动可多个）
 ├─ lap (19) × N ← 自动/手动圈汇总（每圈一个）
 └─ record (20) × M ← 逐点轨迹（秒级/秒内多点）
```

- 画轨迹用 record，算圈/汇总用 lap/session；三者数值应自洽（record 末点距离 ≈ session.total_distance）。

### 6.2 空轨迹 / 0 里程 / extra 为空

- **空轨迹、0 里程**：室内台/暂停无 GPS 记录时 record 可能无位置或 distance=0，属合法数据，不要当坏文件丢弃；上传时允许 0 里程室内记录。
- **`extra` 为空、列表显示 `0.0km`**【本知识库实测】：列表映射字段缺口（iGP 列表返回 `rideDistance`/`totalMovingTime`/点分 `startTime`，本地映射漏了），只影响列表显示与文件名生成，不影响下载字节，不要据此判文件无效。
- **文件名前缀**（`XingZhe_`/`gcn_`/`kp_` 等）来自文件名生成器对记录来源的兜底命名，不是文件内容问题。

### 6.3 第三方上传记录（kp_ 前缀）的归属边界

- **【本知识库实测】** `kp_` 前缀的 Keep 导入记录（活动 id 已脱敏），在 iGP 侧被标记为归属他人；真实 token 直连服务端返回 **HTTP 403**，body `{"code":1002,"message":"不能下载他人运动记录","data":null}`；同账号普通记录返回 200 + OSS 直链。
- 处理边界：
 1. 这不是客户端回归、不是 token 问题、不是文件问题。
 2. 客户端应把 403 / code=1002 原文透出为"无权限下载他人记录"，按"无权限跳过"计数，**不记为同步失败**；不要统一糊成"文件数据无效"。
 3. 此类记录历史上从未成功落盘过，属平台侧权限边界。
- **下载文件大小阈值**【本知识库实测】：App 内对 **<100 字节**的下载结果判无效；短记录会被拦。失败文案应区分"下载为空"与"文件过短"。
