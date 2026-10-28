#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""术语统一（以本书高频用法为准）。

只做“高置信 + 有上下文保护”的替换：
- 电气负载 / 总线发起方（Initiator）等合法义项不误改
- 术语基准：Header=包头、Receiver=接收器、Transmitter=发送器、
  Completion=完成报文、Payload=有效载荷、Credit=信用、Scrambler=加扰器

用法:
    python3 tools/normalize_terms.py --dry-run
    python3 tools/normalize_terms.py
"""
from __future__ import annotations

import argparse
import collections
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CJK = re.compile(r"[\u4e00-\u9fff]")

SAFE = [
    ("头标区", "头部区域"),
    ("头标", "包头"),
    ("完成包", "完成报文"),
    ("完成 TLP", "完成报文"),
    ("完成TLP", "完成报文"),
    ("净荷", "有效载荷"),
    ("扰码器", "加扰器"),
    ("信用额度", "信用"),
    ("上行端口", "上游端口"),
    ("下行端口", "下游端口"),
    ("接收端", "接收器"),
    ("发送端", "发送器"),
    # 标识符写法
    ("CPLD", "CplD"),
    ("CplLK", "CplLk"),
    ("D3Hot", "D3hot"),
    ("D3Cold", "D3cold"),
    ("Max Payload Size", "Max_Payload_Size"),
    ("Max Payload Size", "Max_Payload_Size"),
]

CONTEXT_RULES = [
    # (旧词, 新词, 必须包含的上下文, 禁止出现的上下文)
    ("负载", "有效载荷", r"TLP|Payload|报文|数据包", r"电气|电容|阻抗|总线"),
    ("接收方", "接收器", r"TLP|报文|链路|流控|发送", r"请求|完成方"),
    ("发送方", "发送器", r"TLP|报文|链路|流控|接收", r"请求|完成方"),
    ("发起方", "请求者", r"Requester|TLP|完成报文", r"总线|Initiator|PCI-X"),
    ("发起者", "请求者", r"Requester|TLP|完成报文", r"总线|Initiator|PCI-X"),
    ("头部", "包头", r"TLP|报文|Header", r"头部区域|设备头部"),
]


def process(text: str, stats: collections.Counter, dry: bool) -> str:
    for old, new in SAFE:
        c = text.count(old)
        if c:
            stats[f"{old}→{new}"] += c
            if not dry:
                text = text.replace(old, new)

    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if "<td" not in line and not CJK.search(line):
            continue
        for old, new, must, forbid in CONTEXT_RULES:
            if old in line and re.search(must, line) and not re.search(forbid, line):
                c = line.count(old)
                stats[f"{old}→{new}"] += c
                if not dry:
                    lines[i] = line.replace(old, new)
                line = lines[i]
    return "".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    files = sorted(glob.glob(os.path.join(ROOT, "Ch*.md"))) + [os.path.join(ROOT, "Appendix.md")]
    total = collections.Counter()
    for path in files:
        text = open(path, encoding="utf-8").read()
        stats = collections.Counter()
        new = process(text, stats, args.dry_run)
        if stats:
            total.update(stats)
        if not args.dry_run and new != text:
            open(path, "w", encoding="utf-8").write(new)
    for k, v in total.most_common():
        print(f"{k:34} {v}")
    print("total replacements:", sum(total.values()), "(dry-run)" if args.dry_run else "")


if __name__ == "__main__":
    main()
