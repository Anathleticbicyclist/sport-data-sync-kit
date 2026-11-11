# AGENTS.md — 给编码 Agent 的仓库使用说明

本仓库是「运动健康数据同步」领域的知识库与可安装 Skill，供编码 Agent 在接入运动平台、解析 / 转换 / 校验 FIT/GPX/TCX 文件、排查同步问题时按需读取。

## 仓库结构

```
sport-data-sync-kit/
├── README.md                 # 项目简介、Skill 调用方式、挂载提示、上手步骤、免责声明
├── AGENTS.md                 # 本文件
├── LICENSE                   # MIT（本仓库自有内容）
├── THIRD_PARTY.md            # 第三方开源项目 / 规范 / 解析库致谢与许可证归属
├── .gitignore
├── docs/                     # 知识库文档（Markdown）
│   ├── 00-知识库索引.md
│   ├── 01-代码导览方法论.md
│   ├── 02-开源项目对标矩阵.md   # 矩阵总册：更新说明、分册目录、统计口径
│   ├── 02a-平台对标-国内与综合.md
│   ├── 02b-平台对标-海外与穿戴.md
│   ├── 02c-专题解析库与致谢清单.md
│   ├── 03-踩坑录-版本回归主线与开发陷阱.md
│   ├── 04-运动数据规范-FIT-GPX-TCX.md
│   ├── 05-各平台对接备忘.md
│   └── 06-UI与开发栈梳理.md
└── skill/
    └── sport-data-sync-kit/  # 可安装 Skill 文件夹
        ├── SKILL.md
        ├── references/
        │   ├── formats.md
        │   ├── timezone.md
        │   ├── platforms.md
        │   ├── pitfalls.md
        │   └── opensource.md
        └── scripts/
            └── check_fit.py
```

## 如何使用本 Skill

1. **挂载**：把 `skill/sport-data-sync-kit/` 整个文件夹复制到所用编码 Agent 的 Skills 目录（具体路径见 README 第 3 节与对应工具官方文档）。文件夹必须整体保留，不要拆散 `references/` 与 `scripts/`。
2. **触发**：当任务涉及运动平台接入 / 鉴权、活动列表与下载、FIT/GPX/TCX 解析生成与清洗、字段映射与单位换算、时区与开始时间判定、跨平台上传入库、同步失败或版本回归排查时，先读 `SKILL.md` 的七步工作流，再按导航读取对应 `references/` 文件。
3. **确定性校验**：下载或改写 FIT 后运行：

   ```bash
   python scripts/check_fit.py <file.fit> [file2.fit ...]
   ```

   - 退出码 `0`：全部通过（魔数、文件头长度、数据区长度、文件尾 CRC16 一致）。
   - 退出码 `1`：存在非 FIT、魔数不符、长度异常或 CRC 不一致。
   - GPX/TCX 会被识别并跳过 CRC 校验。改过字节的 FIT 报 CRC 不一致时，先重算文件尾 CRC16 再校验。脚本为纯标准库，无第三方依赖。

## 口径与边界

- 文档结论分三档标注：「本项目实测」「待真机验证 / 待核实」「未核实」。未在真机登录平台验证的接口细节、字段语义、错误码，对接前必须真机回归，**不要凭文档补造端点、字段或成功判据**。
- 引用第三方开源项目前，先按 `references/opensource.md` 第一节的「使用前更新步骤」核对仓库 README、最近提交与 LICENSE；星数、活跃度、许可证均为易过期信息。
- 本仓库**不包含**任何受版权保护的反编译源码、补丁树、安装包、签名材料、用户凭证或个人运动样本；逆向方法仅作学习研究用途。
- 各运动平台名称、商标与数据版权归各自平台所有；知识库内容仅用于个人数据的迁移与备份参考。
- 第三方项目的许可证以其仓库 LICENSE 为准，`THIRD_PARTY.md` 不代为更改。
