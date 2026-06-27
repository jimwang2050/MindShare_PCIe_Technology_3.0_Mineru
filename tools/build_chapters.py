#!/usr/bin/env python3
"""Merge bilingual output_chunk*.md files into chapter markdown files.

Chapter boundaries determined from source chunk analysis.
Output format: bilingual EN+ZH two-column tables.
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
    ("Ch12_Physical_Layer_Logical_Gen3", 570, 661),
    ("Ch13_Physical_Layer_Electrical", 662, 891),
    ("Ch14_Link_Initialization_Training", 892, 1004),
    ("Ch15_Error_Detection_Handling", 1005, 1088),
    ("Ch16_Power_Management", 1089, 1187),
    ("Ch17_Interrupt_Support", 1188, 1246),
    ("Ch18_Optional_Features", 1247, 1287),
    ("Ch19_Hot_Plug_Power_Budgeting", 1288, 1325),
    ("Ch20_Updates_Spec_Rev_2.1", 1326, 1340),
    ("Appendix", 1341, 1360),
]

def merge_chapter(name, start, end):
    """Merge output chunks for a chapter."""
    lines = []
    total_chunks = 0
    available_chunks = 0
    missing = []
    empty = []

    for n in range(start, end + 1):
        chunk_id = f"chunk{n:04d}"
        out_file = TEMP_DIR / f"output_{chunk_id}.md"
        total_chunks += 1

        if not out_file.exists():
            missing.append(chunk_id)
            continue

        text = out_file.read_text(encoding="utf-8").strip()
        if not text:
            empty.append(chunk_id)
            continue

        available_chunks += 1
        lines.append(text)

    if missing:
        print(f"  ⚠️  Missing: {len(missing)} chunks ({missing[0]}..{missing[-1]})")
    if empty:
        print(f"  ⚠️  Empty: {len(empty)} chunks")

    if lines:
        # Add chapter header comment
        # Fix image paths: chapters/ is a subdirectory, images/ is at repo root
        import re
        body_fixed = re.sub(
            r'(<img\s+src=")images/',
            r'\1../images/',
            "\n\n".join(lines)
        )
        header = f"# {name}\n\n"
        out_path = OUT_DIR / f"{name}.md"
        out_path.write_text(header + body_fixed, encoding="utf-8")
        size_kb = out_path.stat().st_size / 1024
        pct = available_chunks / total_chunks * 100
        status = "✅" if available_chunks == total_chunks else "⚠️"
        print(f"  {status} {name}.md — {available_chunks}/{total_chunks} chunks ({pct:.0f}%), {size_kb:.1f} KB")
        return available_chunks == total_chunks
    else:
        print(f"  ❌ {name} — NO content to merge!")
        return False

def main():
    print(f"Merging bilingual chapters from {TEMP_DIR}")
    print(f"Output directory: {OUT_DIR}\n")

    results = []
    for name, start, end in CHAPTERS:
        print(f"[{name}] chunks {start}-{end}:")
        complete = merge_chapter(name, start, end)
        results.append((name, complete))
        print()

    complete_count = sum(1 for _, c in results if c)
    partial_count = sum(1 for _, c in results if not c)
    print(f"\n✅ {complete_count} complete, ⚠️ {partial_count} partial/incomplete")
    print(f"Output: {OUT_DIR}")

if __name__ == "__main__":
    main()
