#!/usr/bin/env python3
"""Translate chunks in batches using sub-agent orchestration.

For each batch (default 8), spawns N parallel sub-agents via the Agent tool.
Each agent translates ONE chunk and writes output_chunk<NNNN>.md.

Usage:
    python3 tools/translate_batch.py --start 1 --end 50 --concurrency 8
    python3 tools/translate_batch.py --start 1 --end 1360 --concurrency 8
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_mineru_v2")
TEMP_DIR = ROOT / "MindShare_PCI_Express_Technology_3.0_temp"


def skip_tiny_chunks(start: int, end: int, min_size: int = 300) -> list[str]:
    """Filter out tiny chunks (likely page headers/footers/non-content)."""
    kept = []
    skipped = 0
    for n in range(start, end + 1):
        cid = f"chunk{n:04d}"
        src = TEMP_DIR / f"{cid}.md"
        if not src.exists():
            continue
        size = src.stat().st_size
        if size < min_size:
            # Pre-fill empty translation
            out = TEMP_DIR / f"output_{cid}.md"
            out.write_text("", encoding="utf-8")
            skipped += 1
        else:
            kept.append(cid)
    print(f"Kept: {len(kept)}, Skipped (tiny <{min_size}B): {skipped}")
    return kept


def make_subagent_prompt(chunk_id: str) -> str:
    """Build the per-chunk translation prompt for a sub-agent."""
    src = TEMP_DIR / f"{chunk_id}.md"
    if not src.exists():
        return None
    text = src.read_text(encoding="utf-8")
    if not text.strip():
        return None

    # Get terms and neighbor context
    sys.path.insert(0, "/Users/jianmingwang/.claude/skills/translate-book/scripts")
    try:
        from chunk_context import get_neighbor_context
        from glossary import print_terms_for_chunk
        neighbor_ctx = get_neighbor_context(str(TEMP_DIR), f"{chunk_id}.md")
        term_table = print_terms_for_chunk(str(TEMP_DIR), f"{chunk_id}.md")
    except Exception as e:
        neighbor_ctx = ""
        term_table = ""
        print(f"  warn: glossary/context for {chunk_id}: {e}", file=sys.stderr)

    if not term_table.strip():
        term_table = "(no glossary terms apply)"

    return f"""Translate the file `{src.absolute()}` to Chinese (zh) and write the result to `{TEMP_DIR}/output_{chunk_id}.md`.

Follow the 18-rule zh-en-translation skill principles:
1. 忠实原意 — preserve negation/condition/scope/passive
2. 保留结构 — keep headings/numbering/tables/code/formulas/Markdown intact
3. 保留不译项 — don't translate code, command, var, file, API, register, protocol field
4. 术语一致 — use the glossary terms (see below)
5. 风格自然 — Chinese engineering document style
6. 只输出译文 — no commentary, no meta
7-11. 格式与图片、HTML 属性安全
12-14. shall/must→应/必须; may→可以/可; should→应/建议
15-16. 数字/单位/十六进制保留
17-18. CUSTOM + 术语表 + 邻居上下文

术语表 (原文 / 别名 / 译文):
{term_table}

邻居上下文 (只读):
{neighbor_ctx}

Read the source file, translate, write to output_{chunk_id}.md. Output ONLY the translated markdown content — no explanations, no START/END markers."""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--concurrency", type=int, default=8)
    parser.add_argument("--min-size", type=int, default=300)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    chunks = skip_tiny_chunks(args.start, args.end, args.min_size)
    print(f"Range: chunk{args.start:04d}..chunk{args.end:04d}, kept {len(chunks)} chunks")
    print(f"Concurrency: {args.concurrency}")

    if args.dry_run:
        for c in chunks[:5]:
            print(f"  sample: {c}")
        return

    # Print prompts for the user to dispatch via Agent tool
    print(f"\n=== {len(chunks)} chunks ready to translate ===")
    print(f"Run with:  python3 tools/translate_batch.py --start {args.start} --end {args.end} --concurrency {args.concurrency}")
    print(f"\nDispatch via Agent tool — each call translates one chunk.")
    print(f"First 3 sample prompts:\n")

    for c in chunks[:3]:
        prompt = make_subagent_prompt(c)
        if prompt:
            print(f"--- {c} ---")
            print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
            print()


if __name__ == "__main__":
    main()
