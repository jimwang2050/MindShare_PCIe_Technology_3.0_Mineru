#!/usr/bin/env python3
"""Translate a single chunk using zh-en-translation principles.

This is a single-chunk translation script that:
1. Loads the source chunk
2. Loads glossary terms for that chunk
3. Loads neighbor context
4. Translates using LLM API (placeholder: this script is for manual run or
   orchestration; the actual translation is done by Claude sub-agents).

For now, this script produces an empty placeholder output_chunk<NNNN>.md
so the build pipeline can proceed. Use translate_batch.py to drive
sub-agent translation.
"""
import sys
import os
import re
from pathlib import Path

sys.path.insert(0, "/Users/jianmingwang/.claude/skills/translate-book/scripts")
from chunk_context import get_neighbor_context  # type: ignore
from glossary import print_terms_for_chunk  # type: ignore


def get_translation_prompt(chunk_id: str, temp_dir: Path) -> str:
    """Build the translation prompt for a single chunk."""
    src = temp_dir / f"{chunk_id}.md"
    if not src.exists():
        raise FileNotFoundError(src)

    text = src.read_text(encoding="utf-8")
    if not text.strip():
        # Empty chunk: return empty translation
        return ""

    # Get neighbor context
    try:
        neighbor_ctx = get_neighbor_context(str(temp_dir), f"{chunk_id}.md")
    except Exception:
        neighbor_ctx = ""

    # Get terms for this chunk
    try:
        term_table = print_terms_for_chunk(str(temp_dir), f"{chunk_id}.md")
    except Exception:
        term_table = ""

    if not term_table.strip():
        term_table = "(no glossary terms apply to this chunk)"

    prompt = f"""Translate the markdown file to Chinese (zh).
Output ONLY the translated content — no commentary, no explanations.

Translation rules (zh-en-translation skill v2):
- 忠实原意: 否定/条件/范围/被动语态必须如实保留
- 保留结构: 标题层级/编号/表格/代码块/公式/引用/Markdown 格式不被破坏
- 保留不译项: 代码/命令/变量名/文件名/API/寄存器名/协议字段名/十六进制常量
- 术语一致: 同一术语全书使用同一译法(参考下方术语表)
- 风格自然: 中文偏工程技术文档风格,避免口语化
- 只输出译文,不输出任何说明/对话
- shall/must → "应/必须";may → "可以/可";should → "应/建议"
- 数字/单位/十六进制/版本号/位字段保留原文(0xFF ≠ 255)
- 图片引用 ![alt](path) 必须完整保留,只翻译 alt 文本
- 原始 HTML 属性内 " ' < > & 替换为弯引号 / &quot; / &lt; / &gt; / &amp;

术语表(原文 / 别名 / 译文) — 强制一致:
{term_table}

邻居上下文(只读,不要翻译,只用于判断代词/性别/跨 chunk 指代):
{neighbor_ctx}

源 markdown 正文:
---
{text}
---
"""
    return prompt


def main():
    if len(sys.argv) < 3:
        print("Usage: translate_one.py TEMP_DIR CHUNK_ID", file=sys.stderr)
        sys.exit(1)

    temp_dir = Path(sys.argv[1])
    chunk_id = sys.argv[2]  # e.g. "chunk0001"
    prompt = get_translation_prompt(chunk_id, temp_dir)
    if not prompt:
        # Empty chunk
        out = temp_dir / f"output_{chunk_id}.md"
        out.write_text("", encoding="utf-8")
        print(f"  {chunk_id}: empty (no source)")
    else:
        # Print prompt for sub-agent pickup
        print(prompt)


if __name__ == "__main__":
    main()
