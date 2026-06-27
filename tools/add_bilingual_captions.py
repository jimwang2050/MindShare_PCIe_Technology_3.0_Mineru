#!/usr/bin/env python3
"""Add Chinese translations to Figure/Table captions in all output chunks.

Process:
1. Extract all English-only Figure/Table captions from output chunks
2. Collect them in a batch for translation
3. Apply translations back to output files
"""
import re
import json
from pathlib import Path

TEMP = Path("/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_mineru_v2/MindShare_PCI_Express_Technology_3.0_temp")


def extract_captions():
    """Extract all English-only Figure/Table captions from output chunks."""
    captions = {}  # (original_text, type) -> [chunk_n, ...]

    for n in range(1, 1361):
        f = TEMP / f"output_chunk{n:04d}.md"
        if not f.exists():
            continue

        text = f.read_text(encoding="utf-8")
        for line in text.split("\n"):
            stripped = line.strip()
            # Match: "Figure X-Y: description" without | (already bilingual)
            # or "<img ...>" lines - skip those
            if stripped.startswith("Figure ") and "|" not in stripped and not stripped.startswith("Figure "):
                captions.setdefault(stripped, []).append(n)
            elif stripped.startswith("Table ") and "|" not in stripped and not stripped.startswith("<table"):
                captions.setdefault(stripped, []).append(n)

    return captions


def build_translation_list(captions):
    """Build a deduplicated list of captions to translate."""
    items = []
    for caption in captions:
        # Determine type
        if caption.startswith("Figure "):
            items.append(("figure", caption))
        elif caption.startswith("Table "):
            items.append(("table", caption))
    return items


def generate_translation_prompt(items):
    """Generate a prompt to translate all captions in one batch."""
    lines = []
    for i, (ctype, caption) in enumerate(items):
        lines.append(f"{i+1}. [{ctype}] {caption}")

    prompt = f"""Translate these Figure and Table captions from English to Chinese.
Output format: each line as "ID|Chinese translation"

Context: These are technical book captions for PCI Express Technology 3.0 book.
Keep the figure/table number intact, only translate the description.
Example: "Figure 3-9: Example Configuration Read Access" → "图 3-9：配置读访问示例"
Example: "Table 2-1: PCIe Bandwidth Summary" → "表 2-1：PCIe带宽汇总"

Input:
{chr(10).join(lines)}

Output each line as: NUMBER|中文翻译
"""
    return prompt


def apply_translations(translations, captions_map):
    """Apply translated captions back to output files.

    translations: dict mapping original caption -> chinese caption
    captions_map: dict mapping original caption -> [chunk_n, ...]
    """
    replaced = 0
    for orig, chunks in captions_map.items():
        if orig not in translations:
            continue
        cn = translations[orig]
        bilingual = f"{orig} | {cn}"

        for n in chunks:
            f = TEMP / f"output_chunk{n:04d}.md"
            text = f.read_text(encoding="utf-8")
            # Replace the original line with bilingual
            # Be careful to only replace standalone lines
            new_text = text.replace(f"\n{orig}\n", f"\n{bilingual}\n")
            if new_text != text:
                f.write_text(new_text, encoding="utf-8")
                replaced += 1
            else:
                # Try start of file
                new_text = text.replace(f"{orig}\n", f"{bilingual}\n", 1)
                if new_text != text:
                    f.write_text(new_text, encoding="utf-8")
                    replaced += 1

    return replaced


def main():
    print("Step 1: Extracting captions from output chunks...")
    captions = extract_captions()
    items = build_translation_list(captions)

    # Deduplicate
    unique_items = {}
    for i, (ctype, caption) in enumerate(items):
        key = caption
        if key not in unique_items:
            unique_items[key] = (ctype, caption)

    unique_list = list(unique_items.values())
    print(f"Found {len(unique_list)} unique captions to translate")
    print(f"  Figures: {sum(1 for c,_ in unique_list if c=='figure')}")
    print(f"  Tables: {sum(1 for c,_ in unique_list if c=='table')}")

    # Print the translation prompt for sub-agent
    print("\nStep 2: Translation prompt for sub-agent:")
    prompt = generate_translation_prompt(unique_list)
    print(prompt[:2000] + "..." if len(prompt) > 2000 else prompt)

    # Save items for later use
    output = {"items": [{"type": c, "en": cap, "chunks": captions[cap]} for cap, (c, _) in unique_items.items()]}
    json_path = TEMP / "captions_to_translate.json"
    json_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved to {json_path}")

    return unique_list, captions


if __name__ == "__main__":
    main()
