# 运动数据格式规范：FIT / GPX / TCX

> 核验日期：2026-11-11　｜　维护人：运动数据同步项目
> 定位：**结论先行**的工程规范。主体以 Garmin / TopoGrafix 官方与开源解析库为准；
> 凡标注「【本知识库实测】」的口径来自内部实测文档（未随本仓库发布）；与官方标准冲突时以实测为准并已注明。

---

## 0. 结论速览（一句话版）

| 维度 | FIT | GPX 1.1 | TCX v2 |
|---|---|---|---|
| 本质 | 二进制、定长记录、紧凑 | XML、文本、自描述 | XML、Garmin 私有、层级强 |
| 时间基准 | uint32 秒，**纪元 1989-12-31T00:00:00Z** | ISO 8601 文本（带 Z 或偏移） | ISO 8601 文本（通常带 Z） |
| 距离单位 | 厘米（uint32，÷100 = 米） | 米（`<ele>`/distance 文本） | 米（`DistanceMeters`） |
| 速度单位 | mm/s 或增强速度 mm/s（÷1000 = m/s） | 原生 GPX 无速度字段，靠扩展 | `Speed m/s`（TPX 扩展） |
| 心率 | record.field 6，uint8 bpm | extensions→`<gpxtpx:hr>` | `<HeartRateBpm><Value>` |
| 功率 | record.field（uint16 W） | extensions→`<power>`（Garmin/Cluetrust） | `<Extensions><TPX><Watts>` |
| 坐标 | semicircles（sint32），WGS-84 | 十进制度，WGS-84 | 十进制度，WGS-84 |
| 校验 | 文件尾 2 字节 CRC16 | 无（XML well-formed 即合法） | 无 |
| 本知识库痛点 | 修改字段后**必须重算 CRC**；时区三形态；GCJ-02 偏移 | 时区写 Z 还是 +08:00 | 能力最窄，不支持温度 |

**本知识库三条铁律**（来自实测）：
1. 改了 FIT 任意字节（含时区平移、坐标纠偏），**必须重算文件尾 CRC16**，否则平台判文件无效。
2. 时区不看文件"长什么样"，**用记录真实开始时间当锚**对齐（见第 5 章锚点法），三种文件形态一把吃掉。
3. 迈金（Magene）GPS 坐标是 **GCJ-02（火星坐标）**，上传前必须 `FIT 处理逻辑` 转回 WGS-84。

---

## 1. FIT 规范

### 1.1 文件整体结构

一个 FIT 文件自顶向下为四段（Garmin 官方：File Header → Data Records → 2 字节 CRC）：

```
┌──────────────────────────────┐ 偏移 0
│ 文件头 File Header (12 或 14B)│ 14 字节为推荐
├──────────────────────────────┤
│ 定义消息 Definition Mesg │ 每条记录 = 记录头 + 内容
│ 数据消息 Data Mesg（成对出现）│ 按"本地消息号"复用定义
│ … 所有数据记录 … │
├──────────────────────────────┤
│ CRC16（2 字节，小端） │ 文件末尾
└──────────────────────────────┘
```

- 数据记录区**不包含**文件头与 CRC，其长度写在文件头第 4–7 字节（小端 uint32）。
- 合法 FIT 必须自含：`file_id`(mesg 0) 的定义+数据、其后每个数据消息前要有对应定义消息、末尾 2 字节 CRC。

### 1.2 文件头（File Header）字节表

| 字节偏移 | 字段 | 长度 | 说明 |
|---|---|---|---|
| 0 | Header Size | 1 | **本头长度**，最小 12（legacy），推荐 14 |
| 1 | Protocol Version | 1 | SDK 协议版本 |
| 2–3 | Profile Version | 2 | 小端，如 2130 = 21.30 |
| 4–7 | Data Size | 4 | 小端，数据记录区字节数 |
| 8–11 | Data Type | 4 | ASCII `.FIT` = `0x2E 0x46 0x49 0x54` |
| 12–13 | Header CRC | 2 | 仅 14 字节头时存在；为字节 0–11 的 CRC，可置 0x0000 |

> **【本知识库实测】`isFit` 判据**：长度 ≥ 14 **且** `bytes[8]=='.'`(0x2E) **且** `bytes[9]=='F'`(0x46)。
> （完整魔数是 bytes[8..11] = `.FIT`，本知识库取前两字节即可拦截绝大多数非 FIT 响应，实测 OSS 直链、迈金/iGP 下载均在偏移 8 命中 `.FIT`。）
> ⚠️ **文件头长度 = `header[0]` 直接读**（它就是 12 或 14）；不要做位运算。
> **真正的坑在"记录头"**：每条消息的头字节里，**本地消息号取低 4 位 `hdr & 0x0F`，绝不能 `hdr >> 4` 取高 4 位**——高 4 位装的是 normal/compressed、定义/数据、开发者数据标志位，取错会把消息号解析成 0–15 之外的乱值。

### 1.3 记录头与大端/小端

- 每条数据前有 1 字节**记录头（Record Header）**：
  - bit7=0 普通头；bit7=1 压缩时间戳头（compressed timestamp，低 5 位是时间增量）。
  - bit6：0=定义消息，1=数据消息。
  - bit5：开发者数据标志（Developer Data Flag）。
  - **bit0–bit3：本地消息号（Local Message Type）= `hdr & 0x0F`**。
- **大端/小端不由文件全局决定，而由每条定义消息的 Architecture 字节决定**：定义消息第 2 字节 `0 = 小端`、`1 = 大端`。该定义及后续同一本地号的数据消息都按此字节序解析。一个文件内不同消息可以混端。
- 全局消息号（Global Mesg Num）在定义消息第 2–3 字节，其端序也由 Architecture 字节决定。

### 1.4 全局消息号（mesg_num）速查

| mesg_num | 名称 | 作用 |
|---|---|---|
| 0 (0x00) | file_id | 每个活动文件**第一个**必出现：type/manufacturer/product/serial/time_created |
| 12 (0x0C) | sport | 运动类型定义（sport 字段 0 = 骑行/跑步/…） |
| 18 (0x12) | session | 一次活动的汇总（总时长/总距离/平均心率等） |
| 19 (0x13) | lap | 分段（自动圈/手动圈）汇总 |
| 20 (0x14) | **record** | **逐点轨迹**：位置、距离、高度、心率、功率、踏频等（最核心） |
| 34 (0x22) | **activity** | 活动根消息，引用 session，含时间戳 |
| 49 (0x31) | file_creator | 生成软件/设备 |
| 206 (0xCE) | field_description | 开发者字段的自描述（名称/单位/基数类型） |
| 207 (0xCF) | dev_data_id | 开发者数据所属 app 标识 |

> 完整表以 FIT SDK 自带 `Profile.xlsx / Profile.csv` 为准。

### 1.5 关键字段号与缩放（record / session / lap / activity）

**时间戳是跨消息公共字段**：所有消息都用 **field 253 = `timestamp`**（uint32，UTC 秒，FIT 纪元）。
**field 5 = `local_timestamp`**（本地钟面秒，与 timestamp 同基数类型；两字段差值 = 时区偏移，见第 5 章）。

| 字段名 | 常见 field# | 基数类型 | 缩放/偏移 | 物理单位 |
|---|---|---|---|---|
| timestamp | **253** | uint32 | — | 秒（UTC，FIT 纪元） |
| local_timestamp | **5** | uint32 | — | 秒（本地钟面） |
| position_lat | 2 | sint32 | ×(180/2³¹) | 度（semicircles） |
| position_long | 3 | sint32 | ×(180/2³¹) | 度（semicircles） |
| altitude / enhanced_altitude | 5 / 78 等 | uint16/uint32 | raw/5 − 500 | 米 |
| heart_rate | 6 | uint8 | — | bpm（次/分） |
| cadence | 7 | uint8 | — | rpm（踏频/步频） |
| power | 见 Profile | uint16 | — | W（瓦） |
| speed / enhanced_speed | 见 Profile | uint16/uint32 | raw/1000 | m/s |
| temperature | 见 Profile | sint8 | — | °C |
| sport | session/sport 消息内 | enum | — | 0=骑行 1=跑步 …（见 Profile） |

**距离字段**：record.distance 为累计距离，**存的是厘米（raw/100 = 米）**；session/lap 的 `total_distance` 存米（缩放 100）。
（缩放依据：Garmin 官方示例 record 输出 `distance: 510 (cm)`、`speed: 2800 (mm/s)`。）

> ⚠️ 字段号不要求在定义消息里按升序出现，但**数据消息里字段的字节顺序必须严格等于定义消息声明的顺序**。
> 实现上应"读定义消息拿到 field_def_num→size→base_type 三元组，再按此布局拆数据"，**不要硬编码字段号偏移**。

### 1.6 时间戳纪元（FIT Epoch）

- **FIT 时间 = 自 1989-12-31T00:00:00Z 起的 uint32 秒数**。
- 与 Unix 时间（1970-01-01）换算：`unix_s = fit_s + 631065600`（1989-12-31 与 1970-01-01 之差）。
- **【本知识库实测】** 取一份迈金导出的 FIT 做定向字节检索：某活动 `01:14:46 UTC`（北京时间 09:14:46）对应纯 UTC 的 FIT 秒数（大端命中某字节偏移）；同一时刻的本地钟面值 = UTC 秒数 + 28800。这证明迈金文件里写的是**纯 UTC 数值**。

### 1.7 开发者字段（Developer Fields）

- 当定义消息头 bit5=1 时，定义消息尾部多一段"开发者字段定义"（每字段 3 字节）。
- 必须配套出现 `dev_data_id`(207) 与 `field_description`(206) 消息，把"开发者数据索引 + 字段号"映射到可读字段名与单位。
- 解析器遇未知开发者字段应**跳过**（按 size 跳字节），不要报错。

### 1.8 CRC16 算法与"改完必重算"

- 文件**末尾 2 字节**为 CRC16，**小端**，覆盖范围 = 从文件头第 0 字节到数据记录区结束（即不含这 2 字节本身）。
- 多项式/查表（Garmin 官方给的 16 项小表，初值 0x0000）：
 `0x0000,0xCC01,0xD801,0x1400,0xF001,0x3C00,0x2800,0xE401,0xA001,0x6C00,0x7800,0xB401,0x5000,0x9C01,0x8801,0x4400`。
- **铁律：任何字节被修改（时区平移、坐标纠偏、字段清理）后，必须整段重算并覆写末尾 CRC。**
 【本知识库实测】FIT 处理逻辑均为"协议级原地改字节 + 重算 CRC"；漏掉 CRC 是平台报"文件数据无效"的高频原因之一。

---

## 2. GPX 规范（GPX 1.1）

### 2.1 命名空间与层级

- 根元素命名空间：`http://www.topografix.com/GPX/1/1`（schema：`https://www.topografix.com/GPX/1/1/gpx.xsd`）。
- 轨迹层级：`<gpx><trk><trkseg><trkpt>…</trkpt></trkseg></trk></gpx>`。
  - 一个文件可有多条 `<trk>`；一条 `<trk>` 可有多段 `<trkseg>`（暂停会分段）；`<trkseg>` 由一串 `<trkpt>` 组成。
- `<trkpt>` 用**属性**给坐标：`<trkpt lat="36.123" lon="120.456">`，子元素给其余信息。

### 2.2 `<trkpt>` 常用字段

| 字段 | 形式 | 单位/说明 |
|---|---|---|
| lat / lon | 属性 | 十进制度，**WGS-84** |
| `<ele>` | 子元素 | 米（海拔） |
| `<time>` | 子元素 | ISO 8601 文本 |
| `<hdop>` `<vdop>` | 子元素 | 精度 |
| `<extensions>` | 子元素 | 心率/功率/温度/速度等扩展挂这里 |

**扩展字段（心率/功率/温度）**——GPX 本体不含，靠 Garmin TrackPointExtension：
- 命名空间 `http://www.garmin.com/xmlschemas/TrackPointExtension/v2`
- `<gpxtpx:TrackPointExtension><gpxtpx:hr>145</gpxtpx:hr><gpxtpx:cad>88</gpxtpx:cad><gpxtpx:atemp>21</gpxtpx:atemp></gpxtpx:TrackPointExtension>`
- 功率：`<power>240</power>`（Cluetrust/Garmin 约定，单位瓦）。

### 2.3 时区写法（ISO 8601）

- **两种合法写法**：
  - **UTC 带 Z**：`<time>2026-11-11T01:14:46Z</time>`
  - **带偏移**：`<time>2026-11-11T09:14:46+08:00</time>`
- 两种都表达同一时刻；**禁止写"裸本地时间不带 Z/不带偏移"**（如 `2026-11-11T09:14:46`），那是歧义来源。
- 【本知识库实测】行者 GPX 处理：上传时 **-8h 回 UTC（写 Z）**，再按目标平台口径决定是否 +8；避免 GPX 里出现偏移与实际时刻不符。

---

## 3. TCX 规范（Training Center XML v2）

### 3.1 结构与 schema

- schema：`https://www8.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd`
- 命名空间：`http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2`
- 层级（强嵌套）：
 `TrainingCenterDatabase → Activities → Activity(id=运动类型) → Lap(StartTime 属性) → Track → Trackpoint`

### 3.2 关键字段

| 层级 | 字段 | 说明 |
|---|---|---|
| Activity | `Sport` 属性 | Cycling/Running/… |
| Lap | `StartTime` 属性；`TotalTimeSeconds`、`DistanceMeters`、`Calories`、平均/最大心率 | 圈汇总 |
| Trackpoint | `<Time>`、`<Position><LatitudeDegrees>/<LongitudeDegrees>`、`<AltitudeMeters>`、`<DistanceMeters>`、`<HeartRateBpm><Value>`、`<Cadence>` | 逐点 |
| Trackpoint 扩展 | `<Extensions><TPX><Speed>`(m/s)、`<Watts>`(功率)、`<RunCadence>` | 速度/功率/跑步步频 |

### 3.3 与 FIT/GPX 的能力差异

| 能力 | FIT | GPX 1.1 | TCX v2 |
|---|---|---|---|
| 心率 | ✅ record | ✅ extensions/hr | ✅ 原生 `<HeartRateBpm>` |
| 功率 | ✅ 原生 | ✅ extensions/power | ⚠️ 仅在 TPX `<Watts>` 扩展里 |
| 速度 | ✅ 原生 | ❌ 原生无（靠扩展） | ⚠️ 仅 TPX `<Speed>` |
| 温度 | ✅ 原生 | ✅ extensions/atemp | ❌ **不支持温度**（Strava 文档明确） |
| 坐标基准 | semicircles / WGS-84 | 度 / WGS-84 | 度 / WGS-84 |

> 结论：**TCX 适合"活动/圈汇总"表达，逐点丰富度不如 FIT；功率/速度必须进 `<Extensions><TPX>`，温度在 TCX 里无处安放**——跨格式转换时温度只能丢弃或降级到 GPX/FIT。

---

## 4. 单位规范

### 4.1 基本单位约定（跨格式统一内部单位）

| 量 | 内部标准单位 | 说明 |
|---|---|---|
| 距离 | **米 (m)** | FIT 存厘米要 ÷100；TCX/GPX 本就是米 |
| 高程 | **米 (m)** | FIT enhanced_altitude: raw/5 − 500 |
| 速度 | **m/s** | 展示可换 km/h、mph |
| 功率 | **瓦 (W)** | 各格式一致 |
| 心率 | **bpm** | 各格式一致 |
| 踏频 | **rpm / 步频 spm** | 骑行 rpm，跑步 spm |
| 坐标 | **十进制度 (WGS-84)** | 内部统一用度；FIT semicircles 先转度 |

### 4.2 换算公式

```
速度： km/h = m/s × 3.6
 m/s = km/h ÷ 3.6
 mph = m/s × 2.23694 ≈ km/h ÷ 1.60934

配速： 配速 min/km = 1000 ÷ (m/s × 60)
 即 pace(min/km) = 16.6667 ÷ speed(m/s)
 反推：speed(m/s) = 1000 ÷ (配速秒/公里)
 例：30 km/h = 8.333 m/s = 12.0 min/km（=3分20秒/公里）

FIT 坐标：deg = semicircles × 180.0 / 2^31
 （1 semicircle ≈ 180/2147483648 ≈ 8.3819e-8 度）

FIT 距离：m = raw_cm / 100
FIT 速度：m/s = raw_mm_per_s / 1000
FIT 高程：m = raw / 5 − 500
```

### 4.3 坐标系：WGS-84 与 GCJ-02

- **WGS-84**：GPS 原始坐标系，国际通用，FIT/GPX/TCX 标准均为 WGS-84。
- **GCJ-02（"火星坐标"）**：中国境内地图服务商（高德/腾讯）对 WGS-84 施加的非线性加密偏移，同一真实点偏移约 **百米级（几十~700 米）**，境外不偏移。
- **【本知识库实测】迈金（Magene）码表输出的 GPS 坐标是 GCJ-02**，若直接当 WGS-84 上传，轨迹在地图上会整体偏移 ~500 米。项目内 `util/FIT 处理逻辑`（被引用 44 处）负责 **GCJ-02 → WGS-84** 纠偏后再上传；黑鸟下载端已在内部转过 WGS-84，无需二次处理。
- 边界：**GCJ-02↔WGS-84 是单向近似变换**（加密不可逆，官方只给近似反向）；只在中国境内数据需要处理，境外坐标近似等于 WGS-84，不要重复纠偏。

---

## 5. 时间规范

### 5.1 UTC vs 本地时间

- **timestamp（field 253）**：UTC 秒，所有平台解析的"真实时刻"基准。
- **local_timestamp（field 5）**：本地钟面秒（不带时区含义）。
- **差值含义**：`local_timestamp − timestamp = 时区偏移秒`（CST=UTC+8 时 = +28800）。
  - 差值 = 28800：规范分离（文件同时写了 UTC 和本地）。
  - 差值 = 0：文件**没做分离**——要么纯 UTC，要么"本地钟面冒充 UTC"，二者数值相同无法区分，这正是歧义根源。

### 5.2 各平台展示口径差异（【本知识库实测】）

- **iGPSPORT**：把 FIT 里的 timestamp 数值**当本地钟面直接显示**。给它纯 UTC 文件（数值=01:14），它就显示 01:14，比实际骑行（09:14）**早 8 小时**。→ 上传前需把数值"加成本地钟面"（+28800）。
- **迈金（Magene）**：导出的 FIT 是**纯 UTC 正确**的（实测某样本的 UTC 秒数对应 01:14:46 UTC）。
- **行者**：文件常写"local_timestamp == timestamp"（本地冒充 UTC）形态。

### 5.3 文件三种形态与归一

| 形态 | timestamp 实测 | local_timestamp | 归一动作（目标 iGP） |
|---|---|---|---|
| ① 纯 UTC（迈金常见） | 01:14:46（UTC 钟面） | 不存在 | **+28800** 让 iGP 按本地读成 09:14 |
| ② 本地冒充 UTC | 09:14:46（本地钟面） | 等于 timestamp (=0) | shift=0，**不动**（数值已是本地钟面） |
| ③ 规范分离 | 01:14:46 | 09:14:46 (差 28800) | **+28800**（与 iGP 直读 UTC+8 口径一致） |

> 教训（实测 11.5/11.6）：**靠"local_timestamp 在不在 / 相不相等"判断会漏判或误判**——同一来源（迈金）会混着出这三种形态，字段法不可靠。

### 5.4 锚点法（推荐判据，实测 11.8）

**不看文件形态，直接和"这条记录真实的开始时间"对齐。**

锚点来源：`本地状态层.startTimeMs`（由列表接口 `start_riding_time` 以 `Asia/Shanghai` 解析得到，是真实开始时刻的 epoch 毫秒，UTC 正确）。

```
target = startTimeMs / 1000 + 28800 # 本地钟面（CST）对应的秒值
ts = activity(mesg 34) 里 timestamp(field 253) 的秒值
shift = target − ts # 需要平移的秒数
```

**三条护栏（必须实现）：**
1. **幂等**：平移后 `ts == target`；再次处理时 `shift == 0`，绝不叠加成 +16h。
2. **量程异常即不动**：`|shift| > 12h`、或 `shift` 不是 3600 的整数倍 → 判定锚点/解析异常，**原样返回并打日志**（宁可不改，不能改错）。
3. **锚缺失兜底**：`startTimeMs <= 0`（列表没给开始时间）→ 退回字段法：无 local_timestamp 或 local==timestamp → +28800；否则不动。

平移只动 **(mesg=34 activity, field=5 local_timestamp) 与相关 timestamp 序列**（`FIT 处理逻辑.shift`），**改完必重算 CRC**。

---

## 6. 记录规范（层级与脏数据边界）

### 6.1 session / lap / record 层级关系

```
activity (34) ← 一次运动的根，1 个
 └─ session (18) ← 汇总（通常 1 个；多运动可多个）
 ├─ lap (19) × N ← 自动/手动圈汇总（每圈一个）
 └─ record (20) × M ← 逐点轨迹（秒级/秒内多点）
```

- **record**：逐点原始轨迹（位置/距离/心率/功率…），是地图与曲线的数据源。
- **lap**：圈汇总（该圈距离/时长/平均心率/起止点）。
- **session**：整次汇总（总距离/总时长/平均功率…）。
- 消费方应：**画轨迹用 record，算圈/汇总用 lap/session**；三者数值应自洽（record 末点距离 ≈ session.total_distance）。

### 6.2 空轨迹 / 0 里程 / extra 为空

- **空轨迹、0 里程**：室内台/暂停无 GPS 记录时 record 可能无位置或 distance=0。属合法数据，**不要当成坏文件丢弃**；上传时允许 0 里程室内记录。
- **`extra` 为空、列表显示 `0.0km`**【本知识库实测 9.2】：这是列表映射的字段缺口（iGP 列表返回 `rideDistance`/`totalMovingTime` 点分 `startTime`，本地映射漏了），**只影响列表显示与文件名生成，不影响下载字节**。不要据此判文件无效。
- **文件名前缀**（`XingZhe_`/`gcn_`/`kp_` 等）：来自 `本地状态层` 对记录来源的兜底命名，**不是文件内容问题**。

### 6.3 第三方上传记录（kp_ 前缀）的归属边界

- **【本知识库实测 第九节】** `kp_` 前缀的 Keep 导入记录（活动 id 已脱敏），在 iGP 侧被标记为**归属他人**；用真实 token 直连服务端：
  - 返回 **HTTP 403**，body `{"code":1002,"message":"不能下载他人运动记录","data":null}`；
  - 同账号普通记录返回 200 + OSS 直链。
- 处理边界：
 1. 这**不是客户端回归、不是 token 问题、不是文件问题**，修下载常量也下不来（会变成一次真实 403）。
 2. 客户端应把 **403 / code=1002 原文透出**为"无权限下载他人记录"，并按"无权限跳过"计数，**不记为同步失败**；不要统一糊成"文件数据无效"（会误导排查方向）。
 3. 历史上从未成功落盘过此类记录，属于平台侧权限边界，正常现象。
- **下载文件大小阈值**【本知识库实测】：App 内对 **<100 字节**的下载结果判无效——短记录会被拦。这是既有设计，失败文案应区分"下载为空"与"文件过短"。

---

## 7. 出处（官方/开源规范来源）

> 标注每条引用了哪部分；未能核实到的写"未核实"。URL 于 2026-11-11 核验可达。

### FIT
- Garmin FIT Protocol（文件结构、文件头字节表、定义消息、Architecture 端序、record 示例 distance=510cm/speed=2800mm/s、CRC 表、dev_data_id=207/field_description=206）：
 `https://developer.garmin.com/fit/articles/fit-protocol/fit_protocol.html`
- Garmin FIT Protocol 镜像页：`https://developer.garmin.com/fit/protocol/`
- Garmin「Working with Date Time Values」（FIT 纪元 = 1989-12-31T00:00:00Z）：
 `https://developer.garmin.com/fit/articles/cookbook/datetime.html`
- Garmin「Decoding FIT Activity Files」（所有消息 timestamp 用 field 253）：
 `https://developer.garmin.com/fit/articles/cookbook/decoding_activity_files.html`
- garmin-fit-sdk（PyPI，is_fit：12/14 字节头、bytes 8–11 = `.FIT`）：
 `https://pypi.org/project/garmin-fit-sdk/`
- fitparse（Rust，record 字段集与基数类型：position_lat/long sint32、altitude uint16、heart_rate uint8、distance uint32、speed uint16、power uint16、temperature sint8）：
 `https://docs.rs/fitparse/latest/fitparse/fittypes/struct.FitMessageRecord.html`

### GPX
- GPX 1.1 Schema（TopoGrafix 官方，命名空间、trk/trkseg/trkpt 结构、extensions）：
 `https://www.topografix.com/GPX/1/1/gpx.xsd`　｜　`https://www.topografix.com/gpx/1/1/`
- Garmin TrackPointExtension v2（hr/cad/atemp 扩展）：
 `https://www8.garmin.com/xmlschemas/TrackPointExtensionv2.xsd`
- Garmin TrackStatsExtension（Ascent/Descent/MaxElevation）：
 `https://www8.garmin.com/xmlschemas/TrackStatsExtension.xsd`
- Strava 上传文档（GPX 扩展取 hr/cad/atemp；TCX 取功率、不支持温度）：
 `https://developers.strava.com/docs/uploads/`

### TCX
- TrainingCenterDatabase v2 schema（Garmin 官方）：
 `https://www8.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd`

### 单位 / 坐标系
- open-gnss 格式对照（FIT semicircles、distance cm、speed mm/s、enhanced_altitude 0.2m 分辨率；GPX 7 位小数）：
 `https://logiqx.github.io/open-gnss/formats.html`
- GCJ-02 为中国境内地图加密偏移（本知识库实测口径，见下）：未单独引用外部权威页，以项目内 FIT 处理逻辑行为与实测为准。

### 本知识库实测来源（非外部规范）
- 内部实测文档（未随本仓库发布）：FIT/时间/坐标处理链、FIT 处理逻辑只改对应消息字段并重算 CRC、死代码清单。
- 内部实测文档（未随本仓库发布）：三种文件形态、锚点法与三条护栏、迈金纯 UTC 实测样本；kp_ 403 code=1002、0.0km/extra 为空、<100 字节阈值。
