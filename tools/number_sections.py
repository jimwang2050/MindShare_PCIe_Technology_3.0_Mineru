#!/usr/bin/env python3
"""Add section numbering (N.N) to all ## headings in output chunks.

Maps: ## Title | 中文  →  ## N.N Title | N.N 中文
"""
import re
from pathlib import Path

TEMP = Path("/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_mineru_v2/MindShare_PCI_Express_Technology_3.0_temp")

# Chapter definitions: (chapter_num, start_chunk, end_chunk)
CHAPTERS = [
    (1, 1, 86),     # Ch01: Front Matter & Introduction
    (2, 87, 152),   # Ch02: PCIe Architecture Overview
    (3, 153, 189),  # Ch03: Configuration Overview
    (4, 190, 276),  # Ch04: Address Space & Transaction Routing
    (5, 277, 289),  # Ch05: TLP Elements
    (6, 290, 324),  # Ch06: Flow Control
    (7, 325, 367),  # Ch07: Quality of Service
    (8, 368, 395),  # Ch08: Transaction Ordering
    (9, 396, 411),  # Ch09: DLLP Elements
    (10, 412, 481), # Ch10: Ack/Nak Protocol
    (11, 482, 569), # Ch11: Physical Layer - Logical (Gen1/Gen2)
    (12, 570, 661), # Ch12: Physical Layer - Logical (Gen3)
    (13, 662, 891), # Ch13: Physical Layer - Electrical
    (14, 892, 1004),# Ch14: Link Initialization & Training
    (15, 1005, 1088),# Ch15: Error Detection and Handling
    (16, 1089, 1187),# Ch16: Power Management
    (17, 1188, 1246),# Ch17: Interrupt Support
    (18, 1247, 1287),# Ch18: Optional Features
    (19, 1288, 1325),# Ch19: Hot Plug and Power Budgeting
    (20, 1326, 1340),# Ch20: Updates for Spec Rev 2.1
    (21, 1341, 1360),# Appendix
]


def is_skip_heading(text: str) -> bool:
    """Check if this heading should NOT be numbered."""
    lower = text.lower()
    # Skip chapter titles and navigation
    if any(x in lower for x in ['previous chapter', 'this chapter', 'next chapter']):
        return True
    if lower.startswith('chapter ') and ':' in lower:
        return True
    if lower.startswith('part '):
        return True
    if lower.startswith('appendix'):
        return True
    return False


def add_numbering(text: str, ch_num: int, sec_num: int) -> str:
    """Add section numbering to a heading: Title → N.N Title"""
    def strip_num(s):
        prev = None
        while prev != s:
            prev = s
            s = re.sub(r'^\d+\.\d+\s+', '', s)
            s = re.sub(r'^\d+\.\s+', '', s)
        return s.strip()

    # Preserve existing | format
    if ' | ' in text:
        parts = text.split(' | ', 1)
        en_clean = strip_num(parts[0])
        cn_clean = strip_num(parts[1])
        return f"{ch_num}.{sec_num} {en_clean} | {ch_num}.{sec_num} {cn_clean}"
    else:
        en_clean = strip_num(text)
        return f"{ch_num}.{sec_num} {en_clean}"


def main():
    fixed = 0
    total_headings = 0

    for ch_num, start, end in CHAPTERS:
        sec_num = 0

        for n in range(start, end + 1):
            f = TEMP / f"output_chunk{n:04d}.md"
            if not f.exists():
                continue

            text = f.read_text(encoding="utf-8")
            lines = text.split("\n")
            new_lines = []
            changed = False

            for line in lines:
                s = line.strip()
                if s.startswith("## ") and "## EN | ZH" not in s:
                    heading = s[3:].strip()
                    # Skip non-content headings
                    if is_skip_heading(heading):
                        new_lines.append(line)
                        continue

                    # Strip any existing number prefixes (including duplicates)
                    while True:
                        prev = heading
                        heading = re.sub(r'^\d+\.\d+\s+', '', heading)
                        heading = re.sub(r'^\d+\.\s+', '', heading)
                        if heading == prev:
                            break

                    # Add numbering
                    sec_num += 1
                    numbered = add_numbering(heading, ch_num, sec_num)
                    new_lines.append(f"## {numbered}")
                    if numbered != line:
                        changed = True
                    total_headings += 1
                else:
                    new_lines.append(line)

            if changed:
                f.write_text("\n".join(new_lines), encoding="utf-8")
                fixed += 1

        print(f"  Ch{ch_num:02d}: {sec_num} headings numbered")

    print(f"\n✅ Total: {total_headings} headings numbered in {fixed} chunks")


if __name__ == "__main__":
    main()
