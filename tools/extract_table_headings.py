#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把被翻译成表格行的标题还原为 Markdown 标题。

早期 chunk 翻译把标题也放进了双语表格，造成章节结构缺失。
本脚本识别“标题型表格行”，就地抽成真正的标题，其余行保持原顺序。

用法:
    python3 tools/extract_table_headings.py --dry-run   # 只预览
    python3 tools/extract_table_headings.py             # 实际改写
"""
from __future__ import annotations

import argparse
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CJK = re.compile(r"[\u4e00-\u9fff]")
TABLE = re.compile(r"<table\b.*?</table>", re.I | re.S)
ROW = re.compile(r"<tr\b[^>]*>.*?</tr>", re.I | re.S)
CELL = re.compile(r"<td\b[^>]*>(.*?)</td>", re.I | re.S)
HEAD = re.compile(r"^(#{1,4})\s*(.+)$", re.S)


def text_of(html: str) -> str:
    t = re.sub(r"<[^>]+>", " ", html)
    t = re.sub(r"`([^`]*)`", r"\1", t)
    return re.sub(r"\s+", " ", t).strip()


def heading_like(en_html: str, cn_html: str):
    """判断一行是否是标题，返回 (level, en, cn, mark_level) 或 None。"""
    en_raw, cn_raw = text_of(en_html), text_of(cn_html)
    if not en_raw and not cn_raw:
        return None
    en_m, cn_m = HEAD.match(en_raw), HEAD.match(cn_raw)
    if not en_m and not cn_m:
        return None
    level = len((en_m or cn_m).group(1))
    en = en_m.group(2).strip() if en_m else en_raw
    cn = cn_m.group(2).strip() if cn_m else cn_raw
    for t in (en, cn):
        if len(t) > 90:
            return None
        if t.startswith(("•", "-", "*")):
            return None
        if re.search(r"[.;!?]$", t) and not re.match(r"^\d", t):
            return None
    return level, en, cn, bool(en_m or cn_m)


def build_heading(level: int, en: str, cn: str) -> str:
    mark = "#" * max(1, min(level, 4))
    en, cn = en.strip(" ."), cn.strip(" .")
    if en and cn and en != cn:
        return f"{mark} {en} | {cn}"
    return f"{mark} {cn or en}"


def process(text: str, dry: bool, stats: dict) -> str:
    def repl(m):
        table = m.group(0)
        open_tag = re.match(r"<table\b[^>]*>", table, re.I).group(0)
        rows = ROW.findall(table)
        out, buf = [], []
        extracted = 0

        def flush():
            if buf:
                out.append(open_tag + "\n" + "\n".join(buf) + "\n</table>")
                buf.clear()

        for row in rows:
            cells = CELL.findall(row)
            hit = heading_like(cells[0], cells[1]) if len(cells) == 2 else None
            if hit:
                level, en, cn, _ = hit
                flush()
                out.append(build_heading(level, en, cn))
                extracted += 1
            else:
                buf.append(row)
        flush()
        if not extracted:
            return table
        stats["extracted"] += extracted
        if dry:
            return table
        return "\n\n".join(out) + ("\n" if out else "")

    return TABLE.sub(repl, text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--show", action="store_true", help="打印抽取出的标题样例")
    args = parser.parse_args()
    files = sorted(glob.glob(os.path.join(ROOT, "Ch*.md"))) + [os.path.join(ROOT, "Appendix.md")]
    total = 0
    for path in files:
        stats = {"extracted": 0}
        text = open(path, encoding="utf-8").read()
        new = process(text, args.dry_run, stats)
        if stats["extracted"]:
            print(f"{os.path.basename(path):46} {stats['extracted']:4}")
            total += stats["extracted"]
        if args.show and new != text:
            for line in new.splitlines():
                if re.match(r"^#{1,4} ", line):
                    pass
        if not args.dry_run and new != text:
            open(path, "w", encoding="utf-8").write(new)
    print("total extracted:", total, "(dry-run)" if args.dry_run else "(written)")


if __name__ == "__main__":
    main()
