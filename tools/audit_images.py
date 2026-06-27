#!/usr/bin/env python3
"""Audit image/table retention: compare source vs output chunks."""
from pathlib import Path

TEMP = Path("/Users/jianmingwang/Downloads/00_study/02_work/01_book/pcie_cxl/MindShare_PCIe_Technology_3.0_mineru_v2/MindShare_PCI_Express_Technology_3.0_temp")
START, END = 1, 300

total_src_img = 0
total_out_img = 0
total_src_tbl = 0
total_out_tbl = 0
missing_list = []
ok_list = []

print(f"{'chunk':<15} {'src_img':>8} {'out_img':>8} {'src_tbl':>8} {'out_tbl':>8}  status")
print("-" * 60)

for n in range(START, END + 1):
    cid = f"chunk{n:04d}"
    src = TEMP / f"{cid}.md"
    out = TEMP / f"output_{cid}.md"

    if not src.exists():
        continue

    src_text = src.read_text(encoding="utf-8")
    out_text = out.read_text(encoding="utf-8") if out.exists() else ""

    si = src_text.count("images/")
    oi = out_text.count("images/")
    st = src_text.count("<table>")
    ot = out_text.count("<table>")

    total_src_img += si
    total_out_img += oi
    total_src_tbl += st
    total_out_tbl += ot

    if si != oi:
        missing_list.append((cid, si, oi, st, ot, "IMG"))
        print(f"{cid:<15} {si:>8} {oi:>8} {st:>8} {ot:>8}  ❌ IMG loss: {si-oi}")
    elif st != ot:
        missing_list.append((cid, si, oi, st, ot, "TBL"))
        print(f"{cid:<15} {si:>8} {oi:>8} {st:>8} {ot:>8}  ❌ TBL loss: {st-ot}")
    else:
        ok_list.append(cid)

print("-" * 60)
print(f"\n📊 汇总:")
print(f"  源图片总数: {total_src_img}")
print(f"  输出图片总数: {total_out_img}")
print(f"  图片留存率: {total_out_img/total_src_img*100:.1f}%" if total_src_img > 0 else "  N/A")
print(f"  源表格总数: {total_src_tbl}")
print(f"  输出表格总数: {total_out_tbl}")
print(f"  OK chunks: {len(ok_list)}")
print(f"  问题 chunks: {len(missing_list)}")

if missing_list:
    print(f"\n❌ 需要修复的 chunks ({len(missing_list)}):")
    for cid, si, oi, st, ot, kind in missing_list:
        print(f"  {cid}: {'IMG' if kind=='IMG' else 'TBL'} ({'src='+str(si)+' out='+str(oi) if kind=='IMG' else 'src='+str(st)+' out='+str(ot)})")
