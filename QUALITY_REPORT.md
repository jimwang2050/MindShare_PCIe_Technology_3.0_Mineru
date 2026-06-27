# MindShare PCIe Technology 3.0 — 翻译质量报告

## 翻译规则

| 规则 | 规范 |
|:---|:---|
| 正文格式 | HTML `<table>` 两列：EN 左 / ZH 右（灰色背景） |
| 标题格式 | `## N.N Title | N.N 中文标题` |
| 章节编号 | PDF TOC 提取，ch.section.subsection |
| 图片 | `<img src="images/xxx.jpg" width="700">` |
| Figure 标题 | `Figure X-Y: EN | 图X-Y：中文`（在上），`<img>`（在下，空一行）|
| 源表格/代码 | 保留英文原样，在双语表格外部 |
| 术语 | shall→应, must→必须, may→可以, TLP→TLP |

## 已完成修复

- 格式：纯中文 → Markdown 两列 → HTML 表格
- 图片：`![]()` → `<img>`
- Figure/Table 标题双语化（593 个）
- 标题格式统一 `## EN | CN`（484 chunks）
- 章节编号：PDF TOC 层级编号（414 个标题）
- 修复 49 个跨章节编号错误
- 章节边界对齐 PDF TOC
- 修复 Figure 4-1 重复问题
- 目录结构优化，图片路径修复

## 遗留问题

1. **Figure/Table 匹配**：MinerU 提取的部分图片与标题不匹配
2. **Appendix/Ch20 截断**：`## N | N` 和 `## M | M` 为 chunk 边界截断
3. **翻译质量**：sub-agent 质量参差，部分段落翻译腔较重
