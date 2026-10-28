#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""去掉纸质页码引用，仅保留图/表编号。

Markdown 版没有纸质页码，"on page 125" / "第 125 页" 属于悬空引用。
规则：图/表引用保留编号，纯页码删除，并清理残留空括号与重复标点。
"""
from __future__ import annotations

import argparse
import collections
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fix(text: str, stats: collections.Counter) -> str:
    def count(pattern, repl, s, label):
        s, n = re.subn(pattern, repl, s)
        stats[label] += n
        return s

    text = count(r"[（(]\s*第\s*\d+\s*页[^）)]*[）)]", "", text, "括号页码")
    text = count(r"(Figure|Table)\s+(\d+-\d+)\s+on page\s+\d+", r"\1 \2", text, "图/表+页码")
    text = count(r"第\s*\d+\s*页的([图表])\s*(\d+-\d+)", r"\1\2", text, "第N页的图/表")
    text = count(r"第\s*\d+\s*页的?", "", text, "纯页码")
    text = count(r"\s+on page\s+\d+", "", text, "on page")
    text = count(r"[（(]\s*[）)]", "", text, "空括号")
    text = count(r"，\s*，", "，", text, "重复逗号")
    text = count(r"。\s*。", "。", text, "重复句号")
    text = count(r"：\s*：", "：", text, "重复冒号")
    text = count(r" {2,}", " ", text, "多余空格")
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
        new = fix(text, stats)
        total.update(stats)
        if not args.dry_run and new != text:
            open(path, "w", encoding="utf-8").write(new)
    for k, v in total.most_common():
        print(f"{k:16} {v}")
    print("(dry-run)" if args.dry_run else "written")


if __name__ == "__main__":
    main()
