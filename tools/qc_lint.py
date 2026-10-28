#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""翻译质量门禁：一次扫描结构、双语覆盖、标题编号、图表、术语与文本异常。

用法:
    python3 tools/qc_lint.py            # 打印摘要并写入 tools/qc_report.json
    python3 tools/qc_lint.py --baseline # 额外写入 tools/qc_baseline.json

退出码恒为 0（仅用于报告），是否阻断由调用方决定。
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import re
from typing import Dict, List, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CJK = re.compile(r"[\u4e00-\u9fff]")
LATIN_WORD = re.compile(r"[A-Za-z]{3,}")


def chapter_files() -> List[str]:
    return sorted(glob.glob(os.path.join(ROOT, "Ch*.md"))) + [os.path.join(ROOT, "Appendix.md")]


def plain(html: str) -> str:
    """去标签、去多余空白，保留行内代码内容。"""
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def bilingual_rows(text: str) -> List[Tuple[int, str, str]]:
    """返回 (行号, 英文, 中文) —— 仅限左右各 50% 的双语行。"""
    rows = []
    for m in re.finditer(r"<tr\b[^>]*>(.*?)</tr>", text, re.I | re.S):
        cells = re.findall(r"<td\b([^>]*)>(.*?)</td>", m.group(1), re.I | re.S)
        if len(cells) != 2:
            continue
        if not all('width="50%"' in attrs for attrs, _ in cells):
            continue
        rows.append((text.count("\n", 0, m.start()) + 1, plain(cells[0][1]), plain(cells[1][1])))
    return rows


def scan() -> Dict:
    files = chapter_files()
    report: Dict[str, object] = {
        "files": len(files),
        "structure": collections.defaultdict(list),
        "bilingual": collections.defaultdict(list),
        "headings": collections.defaultdict(list),
        "captions": collections.defaultdict(list),
        "images": collections.defaultdict(list),
        "terms": {},
        "text": collections.defaultdict(list),
    }
    corpus: Dict[str, str] = {}
    term_pairs = {
        "Header": ["包头", "头标", "报头"],
        "Requester": ["请求者", "请求方", "发起者", "发起方"],
        "Completer": ["完成者", "完成方", "响应者", "响应方"],
        "Receiver": ["接收器", "接收端", "接收方"],
        "Transmitter": ["发送器", "发送端", "发送方"],
        "Payload": ["有效载荷", "负载", "净荷"],
        "Upstream": ["上游", "上行"],
        "Downstream": ["下游", "下行"],
        "Completion": ["完成报文", "完成包", "完成TLP"],
        "Tag": ["标签", "标记"],
        "Scrambler": ["加扰器", "扰码器"],
        "Credit": ["信用", "信用额度"],
    }
    counters = collections.defaultdict(collections.Counter)
    total_bilingual = 0

    for path in files:
        name = os.path.basename(path)
        text = open(path, encoding="utf-8").read()
        corpus[name] = text

        # --- 结构 ---
        opens, closes = len(re.findall(r"<table\b", text, re.I)), len(re.findall(r"</table>", text, re.I))
        if opens != closes:
            report["structure"]["table_unbalanced"].append((name, opens, closes))
        h1 = [l.strip() for l in text.splitlines() if l.startswith("# ")]
        valid_h1 = [h for h in h1 if re.match(r"^#\s+(\d+|Appendix\s+[A-D]|索引)", h)]
        if h1 and len(valid_h1) != len(h1):
            report["structure"]["h1_count"].append((name, len(h1), h1[:4]))
        if not any(re.match(r"^#\s+\d", h) for h in h1) and name != "Appendix.md":
            report["structure"]["chapter_title_missing"].append(name)
        if "<br" in text:
            report["structure"]["br_tags"].append((name, text.count("<br")))

        rows = bilingual_rows(text)
        total_bilingual += len(rows)
        for lineno, en, zh in rows:
            if not en:
                continue
            if not CJK.search(zh) and len(LATIN_WORD.findall(zh)) > 4:
                report["bilingual"]["en_only"].append((name, lineno, en[:70], zh[:70]))
            elif not zh:
                report["bilingual"]["empty"].append((name, lineno, en[:70]))

        # --- 标题 ---
        heads = [(i + 1, l.strip()) for i, l in enumerate(text.splitlines()) if re.match(r"^#{1,4} ", l.strip())]
        nums = []
        for lineno, h in heads:
            body = re.sub(r"^#+\s*", "", h)
            if h.startswith("## ") and "|" not in body:
                if CJK.search(body):
                    report["headings"]["cn_only"].append((name, lineno, body[:80]))
                else:
                    report["headings"]["en_only"].append((name, lineno, body[:80]))
            if h.count("|") > 1:
                report["headings"]["multi_pipe"].append((name, lineno, body[:100]))
            if re.match(r"^99\.", body):
                report["headings"]["placeholder"].append((name, lineno, body[:80]))
            m = re.match(r"^(\d+(?:\.\d+)+)\s", body)
            if m:
                nums.append(m.group(1))
        for dup, cnt in collections.Counter(nums).items():
            if cnt > 1:
                report["headings"]["duplicate_number"].append((name, dup, cnt))

        # --- 图表 ---
        figs = re.findall(r"^Figure\s+\d+-\d+\s*[:：][^\n]*", text, re.M)
        tabs = re.findall(r"^Table\s+\d+-\d+\s*[:：][^\n]*", text, re.M)
        report["captions"]["fig_total"] = report["captions"].get("fig_total", 0) + len(figs)
        report["captions"]["tab_total"] = report["captions"].get("tab_total", 0) + len(tabs)
        report["captions"]["fig_no_cn"] = report["captions"].get("fig_no_cn", 0) + sum(1 for x in figs if "| 图" not in x)
        report["captions"]["tab_no_cn"] = report["captions"].get("tab_no_cn", 0) + sum(1 for x in tabs if "| 表" not in x)
        for m in re.finditer(r"^(Figure|Table)\s+\d+-\d+[^\n]*\n<img", text, re.M):
            report["captions"]["caption_img_noblank"].append((name, text.count("\n", 0, m.start()) + 1))

        # --- 图片 ---
        for src in re.findall(r'<img[^>]*src="([^"]+)"', text):
            if not os.path.exists(os.path.join(ROOT, src)):
                report["images"]["missing"].append((name, src))

        # --- 文本异常 ---
        for m in re.finditer(r"<td\b[^>]*>(.*?)</td>", text, re.I | re.S):
            t = plain(m.group(1))
            if len(t) > 150 and re.search(r"[a-z,]$", t) and not re.search(r"[.!?)]$", t):
                report["text"]["truncated"].append((name, text.count("\n", 0, m.start()) + 1, t[-70:]))
        report["text"]["page_refs"] = report["text"].get("page_refs", 0) + len(re.findall(r"on page \d+|第\s*\d+\s*页", text))

        # --- 术语 ---
        for term, variants in term_pairs.items():
            for v in variants:
                counters[term][v] += text.count(v)

    total = "\n".join(corpus.values())
    report["bilingual"]["total_cells"] = total_bilingual
    report["text"]["non_ascii_hyphen"] = total.count("\u2010") + total.count("\u2011")
    report["text"]["cjk_latin_adjacent"] = len(re.findall(r"[\u4e00-\u9fff][A-Za-z]|[A-Za-z0-9][\u4e00-\u9fff]", total))
    report["terms"] = {k: dict(v) for k, v in counters.items() if len([x for x in v.values() if x]) > 1}

    # 重复段落
    seen = collections.defaultdict(list)
    for name, text in corpus.items():
        for m in re.finditer(r"<td\b[^>]*>(.*?)</td>", text, re.I | re.S):
            t = plain(m.group(1))
            if len(t) > 120:
                seen[t].append(name)
    report["text"]["duplicated_paragraphs"] = [
        {"files": v, "text": k[:90]} for k, v in seen.items() if len(v) > 1
    ]
    report["text"]["duplicate_count"] = sum(len(v) - 1 for v in seen.values() if len(v) > 1)
    return report


def summarize(report: Dict) -> None:
    b = report["bilingual"]
    print(f"文件数: {report['files']}   双语单元格: {b['total_cells']}")
    print(f"右栏未译: {len(b['en_only'])}   空右栏: {len(b['empty'])}")
    print(f"重复 H1: {len(report['structure']['h1_count'])}   缺章标题: {len(report['structure']['chapter_title_missing'])}")
    print(f"标题缺中文: {len(report['headings']['cn_only'])}   缺英文: {len(report['headings']['en_only'])}")
    print(f"占位编号: {len(report['headings']['placeholder'])}   重号: {len(report['headings']['duplicate_number'])}   多管道: {len(report['headings']['multi_pipe'])}")
    c = report["captions"]
    print(f"图注: {c['fig_total']} (缺中文 {c['fig_no_cn']})   表注: {c['tab_total']} (缺中文 {c['tab_no_cn']})")
    print(f"图注紧贴 <img>: {len(c['caption_img_noblank'])}   断链图: {len(report['images']['missing'])}")
    print(f"截断段落: {len(report['text']['truncated'])}   重复段落: {report['text']['duplicate_count']}")
    print(f"页码引用: {report['text']['page_refs']}   非ASCII连字符: {report['text']['non_ascii_hyphen']}")
    print(f"中英相邻: {report['text']['cjk_latin_adjacent']}")
    mixed = {k: v for k, v in report["terms"].items()}
    if mixed:
        print("术语混用:")
        for k, v in mixed.items():
            print(f"  {k}: {v}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", action="store_true", help="同时写入基线文件")
    args = parser.parse_args()
    report = scan()
    out = os.path.join(ROOT, "tools", "qc_report.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
    if args.baseline:
        with open(os.path.join(ROOT, "tools", "qc_baseline.json"), "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
    summarize(report)
    print(f"\n报告: {out}")


if __name__ == "__main__":
    main()
