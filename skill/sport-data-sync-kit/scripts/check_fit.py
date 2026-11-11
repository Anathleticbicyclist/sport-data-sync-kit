#!/usr/bin/env python3
"""FIT 文件魔数与 CRC16 校验小工具（纯标准库，无第三方依赖）。

用途：下载/清洗/改写 FIT 后做确定性校验，回答两个问题：
  1. 字节流是不是合法 FIT（魔数、文件头长度、数据区长度）；
  2. 文件尾 2 字节 CRC16 是否与正文一致（任何字节被改过却没重算 CRC，这里会报 FAIL）。

用法：
    python check_fit.py <file.fit> [file2.fit ...]

退出码：
    0  所有被检文件均为合法 FIT 且 CRC 校验通过；
    1  存在非 FIT、魔数不符、长度异常或 CRC 不一致的文件。

口径来源：本项目实测规范（知识库 04-运动数据规范-FIT-GPX-TCX.md §1.2 / §1.8）。
注意：本脚本只做结构与 CRC 校验，不校验消息定义/字段语义；解析异常时按规范兜底原样返回。
"""

import struct
import sys
from pathlib import Path

# Garmin FIT 官方 16 项 CRC16 小表（初值 0x0000），见规范 §1.8。
CRC_TABLE = [
    0x0000, 0xCC01, 0xD801, 0x1400, 0xF001, 0x3C00, 0x2800, 0xE401,
    0xA001, 0x6C00, 0x7800, 0xB401, 0x5000, 0x9C01, 0x8801, 0x4400,
]

FIT_MAGIC = b".FIT"


def fit_crc(data: bytes) -> int:
    """按 Garmin FIT CRC16 算法计算（覆盖传入的全部字节）。"""
    crc = 0
    for byte in data:
        tmp = CRC_TABLE[crc & 0x0F]
        crc >>= 4
        crc ^= tmp ^ CRC_TABLE[byte & 0x0F]
        tmp = CRC_TABLE[crc & 0x0F]
        crc >>= 4
        crc ^= tmp ^ CRC_TABLE[(byte >> 4) & 0x0F]
    return crc & 0xFFFF


def classify(head: bytes) -> str:
    """按文件头猜测格式：FIT / GPX / TCX / 未知。"""
    if len(head) >= 12 and head[8:12] == FIT_MAGIC:
        return "FIT"
    sample = head[:300]
    if b"TrainingCenterDatabase" in sample:
        return "TCX"
    stripped = sample.lstrip()
    if stripped.startswith(b"<?xml") or b"<gpx" in sample:
        return "GPX"
    return "未知"


def check_fit(path: Path) -> tuple[bool, str]:
    raw = path.read_bytes()
    if len(raw) < 14:
        return False, f"长度 {len(raw)} < 14，不足以构成 FIT 文件头"

    header_size = raw[0]
    if header_size not in (12, 14):
        return False, f"文件头长度字段 header[0]={header_size} 非法（应为 12 或 14）"

    if raw[8:12] != FIT_MAGIC:
        return False, f"魔数不符：bytes[8:11]={raw[8:12]!r}（应为 b'.FIT'）"

    data_size = struct.unpack_from("<I", raw, 4)[0]
    expected_total = header_size + data_size + 2
    if len(raw) != expected_total:
        return False, (
            f"长度不一致：文件 {len(raw)} 字节，按头推算 {expected_total} "
            f"（头 {header_size} + 数据区 {data_size} + CRC 2）"
        )

    body = raw[:-2]
    stored_crc = struct.unpack_from("<H", raw, len(raw) - 2)[0]
    computed_crc = fit_crc(body)
    if stored_crc != computed_crc:
        return False, (
            f"CRC16 不一致：文件尾存 0x{stored_crc:04X}，重算 0x{computed_crc:04X}"
            "（改过字节后必须重算文件尾 CRC）"
        )

    return True, (
        f"OK：{len(raw)} 字节，头 {header_size}B，数据区 {data_size}B，"
        f"CRC16=0x{computed_crc:04X} 一致"
    )


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1

    all_ok = True
    for arg in argv[1:]:
        p = Path(arg)
        if not p.exists():
            print(f"[缺失] {p}")
            all_ok = False
            continue
        raw_head = p.read_bytes()[:300]
        kind = classify(raw_head)
        if kind == "FIT":
            ok, msg = check_fit(p)
        elif kind in ("GPX", "TCX"):
            ok, msg = True, f"XML 文本格式（{kind}），无文件尾 CRC，跳过 CRC 校验"
        else:
            ok, msg = False, "无法识别为 FIT/GPX/TCX（检查下载是否被 HTML/错误页替换）"
        all_ok = all_ok and ok
        print(f"[{'PASS' if ok else 'FAIL'}] {p.name} ({kind}) — {msg}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
