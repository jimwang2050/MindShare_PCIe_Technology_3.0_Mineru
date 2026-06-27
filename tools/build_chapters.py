#!/usr/bin/env python3
"""Merge translated output_chunk*.md files into chapter markdown files.

Chapter boundaries determined from source chunk analysis.
"""
from pathlib import Path

ROOT = Path("/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_mineru_v2")
TEMP_DIR = ROOT / "MindShare_PCI_Express_Technology_3.0_temp"
OUT_DIR = ROOT / "chapters"
OUT_DIR.mkdir(exist_ok=True)

# Chapter definitions: (name, start_chunk, end_chunk)
CHAPTERS = [
    ("Ch01_Front_Matter_and_Introduction", 1, 86),
    ("Ch02_PCIe_Architecture_Overview", 87, 152),
    ("Ch03_Configuration_Overview", 153, 189),
    ("Ch04_Address_Space_and_Transaction_Routing", 190, 276),
    ("Ch05_TLP_Elements", 277, 289),
    ("Ch06_Flow_Control", 290, 324),
    ("Ch07_Quality_of_Service", 325, 367),
    ("Ch08_Transaction_Ordering", 368, 395),
    ("Ch09_DLLP_Elements", 396, 411),
    ("Ch10_AckNak_Protocol", 412, 481),
    ("Ch11_Physical_Layer_Logical_Gen1_Gen2", 482, 569),
    # Ch12: chunks 570-661 (partially translated; 570-608 done, 609+ pending)
]

def merge_chapter(name, start, end):
    """Merge output chunks for a chapter."""
    lines = []
    missing = []
    empty = []

    for n in range(start, end + 1):
        chunk_id = f"chunk{n:04d}"
        out_file = TEMP_DIR / f"output_{chunk_id}.md"

        if not out_file.exists():
            missing.append(chunk_id)
            continue

        text = out_file.read_text(encoding="utf-8").strip()
        if not text:
            empty.append(chunk_id)
            continue

        lines.append(text)

    if missing:
        print(f"  ⚠️  Missing: {len(missing)} chunks ({missing[0]}..{missing[-1]})")
    if empty:
        print(f"  ⚠️  Empty: {len(empty)} chunks")

    if lines:
        out_path = OUT_DIR / f"{name}.md"
        out_path.write_text("\n\n".join(lines), encoding="utf-8")
        size_kb = out_path.stat().st_size / 1024
        print(f"  ✅ {name}.md — {len(lines)} chunks merged, {size_kb:.1f} KB")
        return True
    else:
        print(f"  ❌ {name} — NO content to merge!")
        return False

def main():
    print(f"Merging chapters from {TEMP_DIR}")
    print(f"Output directory: {OUT_DIR}\n")

    success = 0
    for name, start, end in CHAPTERS:
        print(f"[{name}] chunks {start}-{end}:")
        if merge_chapter(name, start, end):
            success += 1
        print()

    print(f"\n✅ {success}/{len(CHAPTERS)} chapters built successfully")
    print(f"Output: {OUT_DIR}")

if __name__ == "__main__":
    main()
