#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重建章节标题结构与编号。

流程：
1. 删除流水线占位块、空表、重复/畸形标题
2. 规范每个文件的 H1（章 / 附录块）
3. 按标题层级重新编号（章内 N.x，附录 B.x）
4. 旧编号（含 99.x 占位、跨章串号）全部清除

用法:
    python3 tools/rebuild_numbering.py --dry-run
    python3 tools/rebuild_numbering.py
"""
from __future__ import annotations

import argparse
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHAPTER_TITLES = {
    1: ("Background", "背景"),
    2: ("PCIe Architecture Overview", "PCIe 架构概览"),
    3: ("Configuration Overview", "配置概述"),
    4: ("Address Space & Transaction Routing", "地址空间与事务路由"),
    5: ("TLP Elements", "TLP 元素"),
    6: ("Flow Control", "流控"),
    7: ("Quality of Service", "服务质量"),
    8: ("Transaction Ordering", "事务排序"),
    9: ("DLLP Elements", "DLLP 元素"),
    10: ("Ack/Nak Protocol", "Ack/Nak 协议"),
    11: ("Physical Layer — Logical (Gen1 and Gen2)", "物理层 — 逻辑子层（Gen1 与 Gen2）"),
    12: ("Physical Layer — Logical (Gen3)", "物理层 — 逻辑子层（Gen3）"),
    13: ("Physical Layer — Electrical", "物理层 — 电气"),
    14: ("Link Initialization & Training", "链路初始化与训练"),
    15: ("Error Detection and Handling", "错误检测与处理"),
    16: ("Power Management", "电源管理"),
    17: ("Interrupt Support", "中断支持"),
    18: ("System Reset", "系统复位"),
    19: ("Hot Plug and Power Budgeting", "热插拔与功率预算"),
    20: ("Updates for Spec Revision 2.1", "规范 2.1 版更新"),
}

APPENDIX_TITLES = {
    "A": ("Appendix A: Analysis Tools and Test Equipment", "附录A 分析工具与测试设备"),
    "B": ("Appendix B: Markets & Applications for PCI Express", "附录B 面向 PCI Express 的市场与应用"),
    "C": ("Appendix C: Implementing Intelligent Adapters and Multi-Host Systems", "附录C 智能适配器与多主机系统"),
    "D": ("Appendix D: Locked Transactions", "附录D 锁定事务"),
}

# 不参与编号的导览/广告类标题
SKIP_NUMBER = {
    "The Previous Chapter", "Previous Chapter", "This Chapter", "The Next Chapter", "Next Chapter",
    "PCI Express Technology", "PCI Express 3.0 Technology", "PCI Express 3.0 技术",
}

# 显式修复：旧标题 -> 新标题（None 表示删除）
HEADING_FIXES = {
    "## DLLP的接收处理": "## DLLP Receive Handling | DLLP 的接收处理",
    "## Ack/Nak 协议处理的错误情况": "## Error Situations Handled by Ack/Nak | Ack/Nak 协议处理的错误情况",
    "## 有序集示例 - SOS（Skip Ordered Set，跳过有序集）": "## Ordered Set Example — SOS (Skip Ordered Set) | 有序集示例 — SOS（跳过有序集）",
    "## Scrambling (扰码)": "## Scrambling | 扰码",
    "## 处于 Configuration.Lanenum.Wait 状态期间": "## During Configuration.Lanenum.Wait | 处于 Configuration.Lanenum.Wait 状态期间",
    "## 进入恢复状态的原因": None,
    "## Exit to \"Configuration State\" — 退出到“配置状态”": "## Exit to \"Configuration State\" | 退出到“配置状态”",
    "## Loopback.Exit — 环回.退出": "## Loopback.Exit | 环回退出",
    "## 第14章：链路初始化和训练": None,
    "## 软件错误调查的示例流程": "## Example Flow of Software Error Investigation | 软件错误调查的示例流程",
    "## MSI-X 能力结构 (Capability Structure)": "## MSI-X Capability Structure | MSI-X 能力结构",
    "## MSI 可能导致错误": None,
    "## This Chapter ## 本章": "## This Chapter | 本章",
    "## 规范要求：": None,
    "## Tx\\_L0s.FTS.": "## Tx_L0s.FTS | Tx_L0s.FTS 状态",
    "## Rx\\_L0s.Entry.": "## Rx_L0s.Entry | Rx_L0s.Entry 状态",
    "## Exit to \"Rx\\_L0s.FTS\"": "## Exit to \"Rx_L0s.FTS\" | 退出到 \"Rx_L0s.FTS\"",
    "## Rx\\_L0s.FTS.": "## Rx_L0s.FTS | Rx_L0s.FTS 状态",
    "## GT | s Operation": "## GT/s Operation | GT/s 操作",
    "## 17.5 Memory Synchronization When Interrupt Handler Entered | 17.5 进入中断处理程序时的内存同步 |": None,
    "### Bilingual Translation": None,
    "## 示例：在 PCI Express 基础系统中实现智能适配器": None,
    "## 示例：在PCI Express系统中实现主机故障切换": None,
    "## – Transitioned to Electrical Idle": "## Transitioned to Electrical Idle | 转换到电气空闲",
    "## After a 2ms timeout:": "## After a 2ms Timeout | 经过 2ms 超时后",
    "## 5.2.3.3 Header Type | Format Field Encodings | 5.2.3.3 头类型 | 格式字段编码":
        "## 5.2.3.3 Header Type / Format Field Encodings | 5.2.3.3 头类型 / 格式字段编码",
    "## 5.2.3.4 Digest | ECRC Field | 5.2.3.4 摘要 | ECRC 字段":
        "## 5.2.3.4 Digest / ECRC Field | 5.2.3.4 摘要 / ECRC 字段",
    "## PCI Express 3.0 Technology": "## PCI Express 3.0 Technology | PCI Express 3.0 技术",
    "## PCI Express Technology": "## PCI Express Technology | PCI Express 技术",
    "## N": "## Index N | 索引 N",
    "## O": "## Index O | 索引 O",
    "## P": "## Index P | 索引 P",
    "## Q": "## Index Q | 索引 Q",
    "## S": "## Index S | 索引 S",
    "## T": "## Index T | 索引 T",
    "## U": "## Index U | 索引 U",
    "## V": "## Index V | 索引 V",
    "## W": "## Index W | 索引 W",
}

NUM_RE = re.compile(r"^\d+(?:\.\d+)*\s+")
BLOCK_RE = re.compile(r"^#\s+(?:(\d+)\s|([A-D])\b)")
APPENDIX_H1 = re.compile(r"^Appendix\s+([A-D])\b")
SUBLABEL = re.compile(
    r"^(?:During|Exit|Entering|After|If\s|Phase\s|–|•|Upstream Lanes|Downstream Lanes|"
    r"Equalization Notes|Confirming Link|Link Number Negotiation|Lane Number Negotiation|"
    r"Link Configuration Example|Spec requirements|Software Generation|Time Allowed|"
    r"Other characteristics|Special Case|Polling\.|Detect\.|Configuration\.|Recovery\.|L0s|L1\.|L2\.|Loopback\.|Tx[\\_]|Rx[\\_]|"
    r"Hot Reset|Disabled|Scenario|Option)")


def split_bilingual(body: str):
    parts = [p.strip() for p in body.split("|")]
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], "|".join(parts[1:]).strip()


def strip_number(text: str) -> str:
    return NUM_RE.sub("", text).strip()


def clean_heading_body(body: str) -> str:
    parts = [p.strip() for p in body.split("|")]
    parts = [p for p in parts if p]
    if len(parts) <= 2:
        return " | ".join(parts)
    # 多段：末段是外章编号则丢弃，否则并入标题
    last, first = parts[-1], parts[0]
    m_last = re.match(r"^(\d+(?:\.\d+)*)", last)
    m_first = re.match(r"^(\d+(?:\.\d+)*)", first)
    if m_last and not m_first:
        parts = parts[:-1]
    elif m_last and m_first and m_last.group(1).split(".")[0] != m_first.group(1).split(".")[0]:
        parts = parts[:-1]
    else:
        parts = [parts[0], " / ".join(parts[1:])]
    return " | ".join(parts)


def dedup_key(body: str) -> str:
    en, cn = split_bilingual(body)
    t = strip_number(en or cn)
    return re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "", t).lower()


def normalize_h1(lines, path):
    name = os.path.basename(path)
    m = re.match(r"Ch(\d+)_", name)
    source = "\n".join(lines)

    if name == "Appendix.md":
        out = []
        for line in lines:
            if line.strip() == "# Appendix":
                out.append("# 索引 | Index")
            elif re.match(r"^## [N-W] \| [N-W]$", line.strip()):
                out.append("## " + line.strip()[3])
            else:
                out.append(line)
        return out

    # 删除流水线占位块与只有表头的空表（逐表判断，避免跨表误删）
    def drop_useless(m):
        block = m.group(0)
        if "no translatable content" in block:
            return "\n"
        if "<td" not in block and "<th" in block:
            return "\n"
        return block

    source = re.sub(r"<table\b.*?</table>", drop_useless, source, flags=re.I | re.S)
    # 删除占位 H1
    source = re.sub(r"^#\s*Ch\d+_[^\n]*\n+", "", source, flags=re.M)
    # 删除 “Chapter : Appendix X” 类残留标题
    source = re.sub(r"^#{1,3}\s+Chapter :[^\n]*\n+", "", source, flags=re.M)

    if m and int(m.group(1)) == 1:
        source = source.replace("# Background | 背景", "# 1 Background | 1 背景", 1)
        # 前置内容全部降为 H2，并加上 front matter 标题
        head, _, tail = source.partition("# 1 Background | 1 背景")
        head = re.sub(r"^#\s+", "## ", head, flags=re.M)
        tail = re.sub(r"^#\s+", "## ", tail, flags=re.M)
        source = "# 0 前言与目录 | Front Matter\n" + head + "# 1 Background | 1 背景" + tail
        return source.splitlines()

    ch = int(m.group(1)) if m else None

    if ch == 20:
        # 附录 A 的两级标题合并为一个 H1
        source = re.sub(
            r"# Appendix A: \| 附录 A：\s*\n+\s*# Debugging PCIe Traffic with LeCroy Tools \| 使用LeCroy工具调试PCIe流量",
            "# " + APPENDIX_TITLES["A"][0] + " | " + APPENDIX_TITLES["A"][1],
            source)
        source = re.sub(
            r"# Appendix B: Markets & Applications for PCI Express(\s*\|[^\n]*)?",
            "# " + APPENDIX_TITLES["B"][0] + " | " + APPENDIX_TITLES["B"][1], source)
        source = re.sub(
            r"# Implementing Intelligent Adapters and Multi[‐-]Host Systems With PCI Express Technology",
            "# " + APPENDIX_TITLES["C"][0] + " | " + APPENDIX_TITLES["C"][1], source)
        source = re.sub(
            r"# Appendix D: Locked Transactions(\s*\|[^\n]*)?",
            "# " + APPENDIX_TITLES["D"][0] + " | " + APPENDIX_TITLES["D"][1], source)
        # 去掉重复的章标题 H1 与 “Chapter : Appendix X” 残留
        source = re.sub(r"^#\s+20\b[^\n]*\n+", "", source, flags=re.M)
        source = re.sub(r"^#\s+Chapter :[^\n]*\n+", "", source, flags=re.M)
        source = "# 20 " + CHAPTER_TITLES[20][0] + " | 20 " + CHAPTER_TITLES[20][1] + "\n" + source
        out = [l for l in source.splitlines()
               if not re.match(r"^#\s+Chapter :", l)]
        return out

    if ch and ch in CHAPTER_TITLES:
        en, cn = CHAPTER_TITLES[ch]
        title = f"# {ch} {en} | {ch} {cn}"
        lines = [l for l in source.splitlines() if not re.match(r"^#\s+", l)]
        # 保留文件开头的说明性内容，把标题放在最前面
        return [title, ""] + lines
    return source.splitlines()


def rebuild(lines, path):
    name = os.path.basename(path)
    lines = normalize_h1(lines, path)
    out = []
    block = None          # 章号或附录字母
    numbered = False
    counters = {2: 0, 3: 0, 4: 0}
    recent = []
    seen_h1 = set()
    seen_blocks = set()
    removed = 0
    for raw in lines:
        line = raw.rstrip("\n")
        stripped = line.strip()

        if stripped in HEADING_FIXES:
            repl = HEADING_FIXES[stripped]
            if repl is None:
                removed += 1
                continue
            line = repl
            stripped = repl

        m1 = re.match(r"^#\s+(.*)$", stripped)
        if m1:
            body = clean_heading_body(m1.group(1))
            if body in seen_h1:
                removed += 1
                continue
            seen_h1.add(body)
            hm = re.match(r"^(\d+)\b", body)
            am = APPENDIX_H1.match(body)
            if hm and int(hm.group(1)) <= 20:
                block = hm.group(1)
                numbered = block != "0"
            elif am:
                block, numbered = am.group(1), True
            else:
                block, numbered = None, False
            if block and block in seen_blocks:
                removed += 1
                continue
            if block:
                seen_blocks.add(block)
            counters = {2: 0, 3: 0, 4: 0}
            recent = []
            out.append(f"# {body}")
            continue

        mh = re.match(r"^(#{2,4})\s+(.*)$", stripped)
        if not mh:
            out.append(line)
            continue

        marks, body = mh.group(1), clean_heading_body(mh.group(2))
        en, cn = split_bilingual(body)
        if re.match(r"^(Chapter\s+\d+\s*:|Appendix\s+[A-D]\s*:)", en) or re.match(r"^第\s*\d+\s*章", cn):
            removed += 1
            continue
        key = dedup_key(body)
        if key and key in recent:
            removed += 1
            continue
        recent = (recent + [key])[-3:]

        if not numbered:
            out.append(f"{marks} {body}")
            continue

        old = re.match(r"^(\d+(?:\.\d+)+)\s+(.*)$", en)
        if old:
            level = min(max(old.group(1).count(".") + 1, 2), 4)
            en = strip_number(en)
        elif SUBLABEL.match(en) or (cn and SUBLABEL.match(cn)):
            # 状态机子标签：保留为不编号的 H3，避免污染目录
            sub = strip_number(en) if en else strip_number(cn)
            subcn = strip_number(cn) if cn else ""
            text = f"{sub} | {subcn}" if subcn and subcn != sub else sub
            out.append(f"### {text}")
            continue
        else:
            level = min(max(len(marks), 2), 4)
        if re.match(r"^D[0-3]\b", en):
            level = 2
        # 缺少上级编号时自动上提，避免出现 x.0.y
        while level > 2 and counters[level - 1] == 0:
            level -= 1
        cn_clean = strip_number(cn) if cn else ""

        if re.sub(r"^\d+(\.\d+)*\s*", "", en).strip() in SKIP_NUMBER:
            out.append(f"{marks} {strip_number(en)}" + (f" | {cn_clean}" if cn_clean else ""))
            continue

        counters[level] += 1
        for d in range(level + 1, 5):
            counters[d] = 0
        num = block + "." + ".".join(str(counters[d]) for d in range(2, level + 1))
        head = f"{marks} {num} {strip_number(en)}"
        if cn_clean:
            head += f" | {num} {cn_clean}"
        out.append(head)

    print(f"{name:46} removed={removed}")
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    files = sorted(glob.glob(os.path.join(ROOT, "Ch*.md"))) + [os.path.join(ROOT, "Appendix.md")]
    for path in files:
        lines = open(path, encoding="utf-8").read().splitlines()
        new = rebuild(lines, path)
        if not args.dry_run:
            open(path, "w", encoding="utf-8").write("\n".join(new) + "\n")


if __name__ == "__main__":
    main()
