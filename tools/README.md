# Translation Pipeline Tools

## Pipeline Overview

```
PDF (原始) → MinerU → 6个 part/ → merge_parts.py → book.md
                                                          ↓
                                                    chunk_book.py
                                                          ↓
                                                   chunk*.md (1360)
                                                          ↓
                                              translate (sub-agents)
                                                          ↓
                                              output_chunk*.md (Markdown tables)
                                                          ↓
                                         convert_to_html_format.py
                                                          ↓
                                   output_chunk*.md (HTML tables, PCIe6.2模板)
                                                          ↓
                                            build_chapters.py
                                                          ↓
                                              chapters/Ch*.md
                                                          ↓
                                               GitHub Push
```

## Tools

| # | Tool | Purpose |
|---|------|---------|
| 1 | `merge_parts.py` | Merge 6 MinerU parts → single book.md (normalize image paths) |
| 2 | `chunk_book.py` | Split book.md → 1360 chunk*.md files (12000 chars each) |
| 3 | `translate_batch.py` | Orchestrate sub-agent translation (chunk → output_chunk) |
| 4 | `translate_one.py` | Build prompt for a single chunk translation sub-agent |
| 5 | `convert_to_html_format.py` | Convert Markdown bilingual tables → HTML `<table>` format |
| 6 | `build_chapters.py` | Merge output_chunk*.md → chapter files |
| 7 | `audit_images.py` | Compare image/table counts between source and output |

## Format Specification (PCIe6.2模板)

### Section Header
```markdown
## Section Title | 中文小节标题
```

### Bilingual Content (HTML table)
```html
<table>
<tr>
<td width="50%">
English text here.
</td>
<td width="50%" style="background-color:#e8e8e8">
中文翻译内容。
</td>
</tr>
</table>
```

### Figures
```markdown
![](images/part01_xxx.jpg)
Figure X-Y: Caption in English
```

### Technical Tables
Keep as original HTML `<table>` or markdown, outside the bilingual table.

## Chapter Boundaries

| Chapter | Chunks | Status |
|---------|--------|--------|
| Ch01: Front Matter & Introduction | 0001-0086 | ✅ |
| Ch02: PCIe Architecture Overview | 0087-0152 | ✅ |
| Ch03: Configuration Overview | 0153-0189 | ✅ |
| Ch04: Address Space & Transaction Routing | 0190-0276 | ✅ |
| Ch05: TLP Elements | 0277-0289 | ✅ |
| Ch06: Flow Control | 0290-0324 | ✅ |
| Ch07: Quality of Service | 0325-0367 | ✅ |
| Ch08: Transaction Ordering | 0368-0395 | ✅ |
| Ch09: DLLP Elements | 0396-0411 | ✅ |
| Ch10: Ack/Nak Protocol | 0412-0481 | ✅ |
| Ch11: Physical Layer - Logical (Gen1/Gen2) | 0482-0569 | ⚠️ |
| Ch12: Physical Layer - Logical (Gen3) | 0570-0661 | 🔄 |
| Ch13: Physical Layer - Electrical | 0662-0891 | ⏳ |
| Ch14: Link Initialization & Training | 0892-1004 | ⏳ |
| Ch15: Error Detection and Handling | 1005-1088 | ⏳ |
| Ch16: Power Management | 1089-1187 | ⏳ |
| Ch17: Interrupt Support | 1188-1246 | ⏳ |
| Ch18: Optional Features | 1247-1287 | ⏳ |
| Ch19: Hot Plug and Power Budgeting | 1288-1325 | ⏳ |
| Ch20: Updates for Spec Rev 2.1 | 1326-1340 | ⏳ |
| Appendix | 1341-1360 | ⏳ |

## Usage

### Convert Markdown tables to HTML format:
```bash
python3 tools/convert_to_html_format.py
```

### Build chapters:
```bash
python3 tools/build_chapters.py
```

### Audit image/table retention:
```bash
python3 tools/audit_images.py
```
