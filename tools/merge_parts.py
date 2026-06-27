#!/usr/bin/env python3
"""Merge 6 MinerU part outputs into a single markdown file for translate-book.

Output:
  - book.md (concatenated markdown, with normalized image paths)

Notes:
  - Each part has its own images/ directory; we copy them all into a single
    images/ and rewrite ![](images/...) paths to use a part-prefixed name
    (e.g. images/p01_bd6316ec...) so they don't collide.
"""
import re
import shutil
from pathlib import Path

ROOT = Path("/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_mineru_v2")
PARTS = sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith("mindshare_part"))

merged_md = ROOT / "book.md"
merged_imgs = ROOT / "images"
merged_imgs.mkdir(exist_ok=True)

# Clean old images dir
for f in merged_imgs.iterdir():
    if f.is_file():
        f.unlink()

# Copy each part's images with a part-prefix, and build the merged markdown
all_text = []
for part in PARTS:
    md_files = list(part.glob("*.md"))
    if not md_files:
        print(f"⚠️  {part.name}: no .md found")
        continue
    md_file = md_files[0]
    text = md_file.read_text(encoding="utf-8")

    # Find all image references
    img_refs = re.findall(r'!\[[^\]]*\]\((images/[^)]+)\)', text)
    pnum = part.name.split("_")[1]  # "part01" → "p01"

    # Copy images and rewrite paths
    for ref in img_refs:
        src = part / ref
        if src.exists():
            dst_name = f"{pnum}_{src.name}"
            dst = merged_imgs / dst_name
            shutil.copy2(src, dst)
            text = text.replace(f"({ref})", f"(images/{dst_name})")

    # Add part separator
    sep = f"\n\n---\n\n# Part {pnum} — `{part.name}`\n\n"
    all_text.append(sep + text)
    print(f"  ✓ {part.name}: {md_file.stat().st_size:,} bytes, {len(img_refs)} images")

merged_md.write_text("\n".join(all_text), encoding="utf-8")
print(f"\n✅ Merged: {merged_md} ({merged_md.stat().st_size:,} bytes, {len(list(merged_imgs.iterdir()))} images)")
