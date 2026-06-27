#!/usr/bin/env python3
"""Chunk the merged book.md using translate-book's split_markdown_structured.

This bypasses the PDF→HTMLZ→Markdown conversion (since we already have
clean markdown from MinerU) and goes straight to chunked input.
"""
import sys
from pathlib import Path

sys.path.insert(0, "/Users/jianmingwang/.claude/skills/translate-book/scripts")
from convert import split_markdown_structured, create_manifest  # type: ignore

ROOT = Path("/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_mineru_v2")
TEMP_DIR = ROOT / "MindShare_PCI_Express_Technology_3.0_temp"
TEMP_DIR.mkdir(exist_ok=True)
CHUNKS = TEMP_DIR  # write chunks to the temp dir root (where translate-book expects them)

# Clean existing chunks
for f in CHUNKS.glob("chunk*.md"):
    f.unlink()
# Clean old chunks/ subdir
old_chunks = TEMP_DIR / "chunks"
if old_chunks.exists():
    for f in old_chunks.glob("*"):
        if f.is_file():
            f.unlink()
    old_chunks.rmdir()

book_md = ROOT / "book.md"
print(f"Splitting {book_md.name} ({book_md.stat().st_size:,} bytes)...")

chunk_files = split_markdown_structured(book_md, CHUNKS, target_size=12000)
create_manifest(CHUNKS, chunk_files, book_md)

# Write config.txt
config = TEMP_DIR / "config.txt"
config.write_text(f"""# Translation Configuration
input_file={book_md.absolute()}
input_lang=en
output_lang=zh
conversion_method=mineru_v4_standard

# Book Metadata
original_title=MindShare PCI Express Technology 3.0
creator=Mike Jackson, Ravi Budruk
publisher=MindShare, Inc.
source_language=en
target_language=zh
""", encoding="utf-8")

print(f"\n✅ Split into {len(chunk_files)} chunks")
print(f"   Chunks dir: {CHUNKS}")
print(f"   Config: {config}")
