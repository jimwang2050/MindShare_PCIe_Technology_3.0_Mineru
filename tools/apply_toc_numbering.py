#!/usr/bin/env python3
"""Precise section numbering from PDF TOC."""
import json, re, fitz
from pathlib import Path

TEMP = Path("/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_mineru_v2/MindShare_PCI_Express_Technology_3.0_temp")

# Extract PDF TOC
doc = fitz.open("/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCI Express Technology 3.0.pdf")
toc = doc.get_toc()
doc.close()

# Build numbering map: (level3_title) -> (num, page)
# This captures the hierarchical structure
chapter = 0
sec_count = {}
sub_count = {}
toc_map = {}  # title_lower -> (number, page, display_title)
skip_titles = {"general"}  # too generic, skip matching

for level, title, page in toc:
    title = title.strip()
    norm = title.lower().strip()

    # Detect chapters
    m = re.match(r'Chapter\s+(\d+):?\s*(.*)', title)
    if m and level <= 2:
        chapter = int(m.group(1))
        sec_count[chapter] = 0
        sub_count[chapter] = {}
        continue

    # Skip front matter
    if chapter == 0:
        continue
    if title.startswith("Part ") or title in ("Appendices", "Glossary"):
        continue

    # Appendix handling
    if title.startswith("Appendix "):
        chapter = 99
        sec_count[chapter] = 0
        sub_count[chapter] = {}
        continue

    # Don't map "General" headings (too ambiguous across chapters)
    if norm in skip_titles:
        continue

    if level == 3:
        sec_count[chapter] = sec_count.get(chapter, 0) + 1
        s = sec_count[chapter]
        sub_count[chapter] = {}
        num = f"{chapter}.{s}"
        toc_map[norm] = (num, page)
    elif level == 4:
        s = sec_count.get(chapter, 0)
        sub_count[chapter][s] = sub_count[chapter].get(s, 0) + 1
        sb = sub_count[chapter][s]
        num = f"{chapter}.{s}.{sb}"
        toc_map[norm] = (num, page)
    elif level == 2 and chapter == 99:
        sec_count[99] = sec_count.get(99, 0) + 1
        toc_map[norm] = (f"99.{sec_count[99]}", page)

print(f"TOC map: {len(toc_map)} entries")

# Apply to output chunks
applied = 0
for n in range(1, 1361):
    f = TEMP / f"output_chunk{n:04d}.md"
    if not f.exists(): continue

    text = f.read_text(encoding="utf-8")
    new_text = text
    changed = False

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped.startswith("## ") or "EN | ZH" in stripped:
            continue

        en_text = stripped[3:].strip()
        cn_text = ""
        if " | " in en_text:
            parts = en_text.split(" | ", 1)
            en_text = parts[0].strip()
            cn_text = parts[1].strip()

        norm = en_text.lower().strip()

        if norm in toc_map:
            num, page = toc_map[norm]
            new_line = f"## {num} {en_text}"
            if cn_text:
                new_line += f" | {num} {cn_text}"
            new_text = new_text.replace(line, new_line, 1)
            changed = True
            applied += 1

    if changed:
        f.write_text(new_text, encoding="utf-8")

print(f"Applied: {applied} headings numbered")
print(f"Done!")
