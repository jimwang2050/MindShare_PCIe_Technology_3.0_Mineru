#!/usr/bin/env python3
"""Merge bilingual output_chunk*.md files into chapter markdown files.

Chapter boundaries determined from source chunk analysis.
Output format: bilingual EN+ZH two-column tables.
"""
from pathlib import Path

ROOT = Path("/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_mineru_v2")
TEMP_DIR = ROOT / "MindShare_PCI_Express_Technology_3.0_temp"
OUT_DIR = ROOT  # Write chapters to repo root, not chapters/ subdir

# Chapter definitions: (name, start_chunk, end_chunk)
CHAPTERS = [
    # Our Ch01 = Front Matter + Chapter 1 (Background): chunks 1-82
    ("Ch01_Front_Matter_and_Introduction", 1, 82),
    # Ch02 starts at chunk 83 ("Chapter 2: PCIe Architecture Overview")
    ("Ch02_PCIe_Architecture_Overview", 83, 133),
    # Ch03 starts at chunk 134 ("Chapter 3: Configuration Overview")
    ("Ch03_Configuration_Overview", 134, 179),
    # Ch04 starts at chunk 180 ("Chapter 4: Address Space & Transaction Routing")
    ("Ch04_Address_Space_and_Transaction_Routing", 180, 244),
    # Ch05 starts at chunk 245 ("Chapter 5: TLP Elements")
    ("Ch05_TLP_Elements", 245, 289),
    # Ch06 starts at chunk 290 ("# 6 Flow Control")
    ("Ch06_Flow_Control", 290, 324),
    # Ch07 starts at chunk 325 ("# Quality of Service")
    ("Ch07_Quality_of_Service", 325, 367),
    # Ch08 starts at chunk 368 ("# Transaction Ordering")
    ("Ch08_Transaction_Ordering", 368, 395),
    # Ch09 starts at chunk 396 ("# DLLP Elements"), Ch10 at 412 ("# 10 Ack/Nak Protocol")
    ("Ch09_DLLP_Elements", 396, 411),
    ("Ch10_AckNak_Protocol", 412, 473),
    # Ch11 starts at chunk 474 ("Chapter 11: Physical Layer - Logical")
    ("Ch11_Physical_Layer_Logical_Gen1_Gen2", 474, 558),
    # Ch12 starts at chunk 559 ("Chapter 12: Physical Layer - Logical (Gen3)")
    ("Ch12_Physical_Layer_Logical_Gen3", 559, 615),
    # Ch13 starts at chunk 616 ("Chapter 13: Physical Layer - Electrical")
    ("Ch13_Physical_Layer_Electrical", 616, 686),
    # Ch14 starts at chunk 687 ("Chapter 14: Link Initialization & Training")
    ("Ch14_Link_Initialization_Training", 687, 908),
    # Ch15 starts at chunk 909 ("Chapter 15: Error Detection and Handling")
    ("Ch15_Error_Detection_Handling", 909, 984),
    # Ch16 starts at chunk 985 ("Chapter 16: Power Management")
    ("Ch16_Power_Management", 985, 1077),
    # Ch17 starts at chunk 1078 ("Chapter 17: Interrupt Support")
    ("Ch17_Interrupt_Support", 1078, 1130),
    # Ch18 starts at chunk 1131 ("Chapter 18: System Reset")
    ("Ch18_Optional_Features", 1131, 1154),
    # Ch19 starts at chunk 1155 ("Chapter 19: Hot Plug and Power Budgeting")
    ("Ch19_Hot_Plug_Power_Budgeting", 1155, 1210),
    # Ch20 starts at chunk 1211 ("Chapter 20: Updates for Spec Revision 2.1")
    ("Ch20_Updates_Spec_Rev_2.1", 1211, 1340),
    # Appendix
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
        import re
        # Reorder: move <img> to be BELOW the preceding Figure caption
        # Pattern: <img...>\nFigure X-Y:...  →  Figure X-Y:...\n<img...>
        body = "\n\n".join(lines)
        body = re.sub(
            r'(<img[^>]*>)\s*\n\s*(Figure\s+\d+[‑-]\d+.*?)(?=\n|$)',
            r'\2\n\1',
            body
        )
        header = f"# {name}\n\n"
        out_path = OUT_DIR / f"{name}.md"
        out_path.write_text(header + body, encoding="utf-8")
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
