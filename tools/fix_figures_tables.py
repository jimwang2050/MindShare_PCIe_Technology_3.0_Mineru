#!/usr/bin/env python3
"""Fix figures and tables in all output chunks:
1. Convert ![](images/xxx) to <img src="images/xxx" width="700">
2. Add Chinese translations to standalone Figure/Table captions
"""
import json
import re
from pathlib import Path

TEMP = Path("/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_mineru_v2/MindShare_PCI_Express_Technology_3.0_temp")


def extract_standalone_captions():
    """Extract unique standalone Figure/Table captions."""
    captions = {}
    for n in range(1, 1361):
        f = TEMP / f"output_chunk{n:04d}.md"
        if not f.exists():
            continue
        for line in f.read_text().split("\n"):
            s = line.strip()
            if s.startswith("Figure ") and "|" not in s and ":" in s and " on page " not in s:
                captions.setdefault(s, []).append(n)
            elif s.startswith("Table ") and "|" not in s and ":" in s and not s.startswith("<table") and " on page " not in s:
                captions.setdefault(s, []).append(n)
    return captions


def convert_markdown_images(text):
    """Convert ![](path) to <img src="path" width="700">"""
    return re.sub(
        r'!\[([^\]]*)\]\(([^)]+)\)',
        r'<img src="\2" width="700" alt="\1">',
        text
    )


def apply_captions(translations, captions_map):
    """Apply bilingual captions to output files."""
    replaced = 0
    for orig, chunks in captions_map.items():
        cn = translations.get(orig, "")
        if not cn:
            continue
        bilingual = f"{orig} | {cn}"

        for n in chunks:
            f = TEMP / f"output_chunk{n:04d}.md"
            text = f.read_text(encoding="utf-8")
            # Replace standalone line
            new_text = text.replace(f"\n{orig}\n", f"\n{bilingual}\n")
            if new_text == text:
                new_text = text.replace(f"{orig}\n", f"{bilingual}\n", 1)
            if new_text != text:
                f.write_text(new_text, encoding="utf-8")
                replaced += 1
    return replaced


def main():
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "extract"

    if mode == "extract":
        # Step 1: Extract captions for translation
        captions = extract_standalone_captions()
        print(f"Unique captions: {len(captions)}")

        # Print for sub-agent
        for i, cap in enumerate(sorted(captions.keys()), 1):
            print(f"{i}. {cap}")

        # Save mapping
        mapping = {cap: chunks for cap, chunks in captions.items()}
        (TEMP / "captions_mapping.json").write_text(
            json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"\n\n--- Translation prompt for AI ---")
        print(f"Translate these {len(captions)} Figure/Table captions to Chinese.")
        print("Output format: each line as 'ID|中文翻译'")
        print("Keep numbers/colons, only translate the description part.")
        print("Example: 'Figure 3-9: Example Read Access' → '图3-9：读访问示例'")
        print("Example: 'Table 4-9: TLP Header Format' → '表4-9：TLP头部格式'\n")

    elif mode == "convert_images":
        # Step 2: Convert ![](images) to <img> tags
        converted = 0
        for n in range(1, 1361):
            f = TEMP / f"output_chunk{n:04d}.md"
            if not f.exists():
                continue
            text = f.read_text(encoding="utf-8")
            new_text = convert_markdown_images(text)
            if new_text != text:
                f.write_text(new_text, encoding="utf-8")
                converted += 1
        print(f"Converted images in {converted} chunks")

    elif mode == "apply":
        # Step 3: Apply translations from stdin JSON
        import sys
        translations = json.load(sys.stdin)
        mapping = json.loads((TEMP / "captions_mapping.json").read_text())
        count = apply_captions(translations, mapping)
        print(f"Applied bilingual captions to {count} chunks")

    elif mode == "all":
        # Full pipeline
        print("=== Converting images to <img> tags ===")
        converted = 0
        for n in range(1, 1361):
            f = TEMP / f"output_chunk{n:04d}.md"
            if not f.exists():
                continue
            text = f.read_text(encoding="utf-8")
            new_text = convert_markdown_images(text)
            if new_text != text:
                f.write_text(new_text, encoding="utf-8")
                converted += 1
        print(f"  Converted {converted} chunks")

        # Extract captions
        print("\n=== Extracting captions ===")
        captions = extract_standalone_captions()
        print(f"  Found {len(captions)} unique captions")

        # Print for manual/AI translation
        print("\n=== Captions for translation ===")
        for i, cap in enumerate(sorted(captions.keys()), 1):
            print(f"{i}|{cap}")

        # Save mapping
        mapping = {cap: chunks for cap, chunks in captions.items()}
        (TEMP / "captions_mapping.json").write_text(
            json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"\n  Saved mapping to captions_mapping.json")


if __name__ == "__main__":
    main()
