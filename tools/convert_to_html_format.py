#!/usr/bin/env python3
"""Convert markdown two-column tables to HTML two-column format (PCIe6.2 template style).

Format change:
  | EN | ZH |      →    <table><tr><td width="50%">EN</td><td width="50%" style="background-color:#e8e8e8">ZH</td></tr></table>
  |:---|:---|
  | text | 中文  |

Headings inside tables → moved outside as ## Title | 中文标题
"""
import re
from pathlib import Path

TEMP = Path("/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_mineru_v2/MindShare_PCI_Express_Technology_3.0_temp")
START, END = 301, 1270  # Newly translated chunks (markdown table format)


def convert_md_table_to_html(content: str) -> str:
    """Convert markdown table blocks to HTML table format."""
    result = []
    i = 0
    lines = content.split("\n")

    while i < len(lines):
        line = lines[i]

        # Check if this is the start of a markdown table (EN|ZH pattern)
        if line.strip().startswith("| EN | ZH |") and i + 1 < len(lines) and lines[i + 1].strip().startswith("|:---|"):
            # Collect all table rows
            table_rows = []
            i += 2  # skip header + separator
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_rows.append(lines[i])
                i += 1

            # Convert to HTML table
            html_parts = []
            for row in table_rows:
                # Parse row: | content | content |
                row = row.strip()
                # Remove leading/trailing |
                row_content = row[1:-1] if row.startswith("|") and row.endswith("|") else row[1:] if row.startswith("|") else row

                # Split by | but handle escaped pipes within cells
                cells = []
                current = ""
                depth = 0
                for ch in row_content:
                    if ch == "|" and depth == 0:
                        cells.append(current.strip())
                        current = ""
                    else:
                        current += ch
                cells.append(current.strip())

                if len(cells) >= 2:
                    en = cells[0].strip()
                    zh = cells[1].strip()

                    # Check if it's a heading
                    heading_match = re.match(r'^(#{1,6})\s+(.+)$', en)
                    if heading_match:
                        # Move heading outside table as: ## Title | 中文标题
                        zh_clean = re.sub(r'^#{1,6}\s+', '', zh).strip()
                        result.append(f"\n{heading_match.group(1)} {heading_match.group(2)} | {zh_clean}\n")
                    else:
                        # Regular row → HTML table row
                        html_parts.append(f"""<tr>
<td width="50%">
{en}
</td>
<td width="50%" style="background-color:#e8e8e8">
{zh}
</td>
</tr>""")

            if html_parts:
                result.append('<table>\n' + '\n'.join(html_parts) + '\n</table>')
        else:
            result.append(line)
            i += 1

    return "\n".join(result)


def main():
    # Convert each output chunk from markdown tables to HTML tables
    converted = 0
    had_images = 0
    had_tables = 0

    for n in range(START, END + 1):
        out_file = TEMP / f"output_chunk{n:04d}.md"
        if not out_file.exists():
            continue

        text = out_file.read_text(encoding="utf-8")

        # Check if it has images or tables
        has_images = "images/" in text
        has_tables = "| EN | ZH |" in text

        if has_tables:
            new_text = convert_md_table_to_html(text)
            # Replace markdown image syntax with simple img tag format (keep path)
            # Actually keep ![]() as is - GitHub renders it fine
            out_file.write_text(new_text, encoding="utf-8")
            converted += 1

        if has_images:
            had_images += 1
        if has_tables:
            had_tables += 1

    print(f"✅ Converted: {converted} chunks to HTML table format")
    print(f"📷 Chunks with images: {had_images}")
    print(f"📋 Chunks with tables: {had_tables}")

    # Also run image audit
    print(f"\n--- Image/Table Audit ---")
    total_src_img = 0
    total_out_img = 0
    total_src_tbl = 0
    total_out_tbl = 0
    missing = []

    for n in range(START, END + 1):
        cid = f"chunk{n:04d}"
        src = TEMP / f"{cid}.md"
        out = TEMP / f"output_{cid}.md"

        src_text = src.read_text(encoding="utf-8") if src.exists() else ""
        out_text = out.read_text(encoding="utf-8") if out.exists() else ""

        si = src_text.count("images/")
        oi = out_text.count("images/")
        st = src_text.count("<table>")
        ot = out_text.count("<table>")  # count our new HTML tables too

        total_src_img += si
        total_out_img += oi
        total_src_tbl += st
        total_out_tbl += ot

        if si != oi:
            missing.append((cid, si, oi))

    print(f"Source images: {total_src_img}")
    print(f"Output images: {total_out_img}")
    print(f"Retention: {total_out_img/total_src_img*100:.1f}%" if total_src_img else "N/A")

    if missing:
        print(f"\n❌ {len(missing)} chunks with missing images:")
        for cid, si, oi in missing:
            print(f"  {cid}: src={si} out={oi}")


if __name__ == "__main__":
    main()
