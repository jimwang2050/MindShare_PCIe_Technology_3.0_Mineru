#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""排版统一：表格模板、图注空行、连字符、表头。

用法:
    python3 tools/normalize_layout.py --dry-run
    python3 tools/normalize_layout.py
"""
from __future__ import annotations

import argparse
import collections
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLE_STYLE = ('<table style="border:1px solid #ddd;border-collapse:collapse;width:100%" '
               'cellpadding="4" cellspacing="0" rules="all" frame="border">')


def process(text: str, stats: collections.Counter, dry: bool) -> str:
    # 1) 去掉 EN/中文 表头（信息冗余，且只有部分表有）
    def drop_thead(m):
        block = m.group(0)
        if "<th" in block and len(block) < 600:
            stats["remove thead"] += 1
            return ""
        return block
    text = re.sub(r"<thead\b.*?</thead>", drop_thead, text, flags=re.I | re.S)

    # 2) 统一表格外框
    def table_tag(m):
        tag = m.group(0)
        if tag.strip() != TABLE_STYLE:
            stats["normalize table"] += 1
        return TABLE_STYLE
    text = re.sub(r"<table\b[^>]*>", table_tag, text, flags=re.I)

    # 3) 统一单元格边框（保留底色与 padding）
    c = text.count("border:2px solid #000")
    if c:
        stats["border 2px->1px"] += c
        text = text.replace("border:2px solid #000", "border:1px solid #ddd")
    c = text.count("border:1px solid #000")
    if c:
        stats["border 1px black->ddd"] += c
        text = text.replace("border:1px solid #000", "border:1px solid #ddd")

    # 4) 图注/表注与图片之间补空行
    text, n = re.subn(r"^((?:Figure|Table)\s+\d+-\d+[^\n]*)\n(<img)", r"\1\n\n\2", text, flags=re.M)
    stats["caption blank line"] += n

    # 5) 图注行尾空格
    text, n = re.subn(r"^((?:Figure|Table)\s+\d+-\d+[^\n]*?)[ \t]+$", r"\1", text, flags=re.M)
    stats["caption trailing space"] += n

    # 6) 非 ASCII 连字符统一
    c = text.count("\u2010") + text.count("\u2011")
    if c:
        stats["hyphen normalize"] += c
        text = text.replace("\u2010", "-").replace("\u2011", "-")

    # 7) 缺少边框的单元格补齐
    text, n1 = re.subn(r'<td width="50%">', '<td width="50%" style="border:1px solid #ddd;">', text)

    def add_border(m):
        return f'<td{m.group(1)} style="border:1px solid #ddd;{m.group(2)}"'

    text, n2 = re.subn(r'<td(\s+width="50%") style="(?!border)([^"]*)"', add_border, text)
    stats["bare td"] += n1 + n2
    return text


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
        total.update(stats)
        if not args.dry_run and new != text:
            open(path, "w", encoding="utf-8").write(new)
    for k, v in total.most_common():
        print(f"{k:28} {v}")
    print("(dry-run)" if args.dry_run else "written")


if __name__ == "__main__":
    main()
