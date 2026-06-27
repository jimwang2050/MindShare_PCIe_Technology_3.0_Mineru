#!/usr/bin/env python3
"""Fix cross-chapter heading numbers - strip wrong chapter prefixes."""
import re
from pathlib import Path

ROOT = Path("/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_mineru_v2")
CHAPTERS = {"Ch01":1,"Ch02":2,"Ch03":3,"Ch04":4,"Ch05":5,"Ch06":6,"Ch07":7,"Ch08":8,"Ch09":9,"Ch10":10,"Ch11":11,"Ch12":12,"Ch13":13,"Ch14":14,"Ch15":15,"Ch16":16,"Ch17":17,"Ch18":18,"Ch19":19,"Ch20":20}

fixed = 0
for ch_name, ch_num in CHAPTERS.items():
    for ch_path in list(ROOT.glob(f"{ch_name}*.md")):
        text = ch_path.read_text(encoding="utf-8")
        new_text = text
        changed = False
        for line in text.split("\n"):
            s = line.strip()
            m = re.match(r'^##\s+(\d+)\.', s)
            if m:
                hdr_ch = int(m.group(1))
                if hdr_ch != ch_num and hdr_ch != 99:
                    cleaned = re.sub(r'^(##\s+)\d+\.\d+(\.\d+)?\s+', r'\1', s)
                    cleaned = re.sub(r'(\|\s*)\d+\.\d+(\.\d+)?\s+', r'\1', cleaned)
                    new_text = new_text.replace(s, cleaned)
                    changed = True
                    fixed += 1
        if changed:
            ch_path.write_text(new_text, encoding="utf-8")

print(f"Fixed {fixed} cross-chapter heading numbers")
