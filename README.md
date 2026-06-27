# MindShare PCI Express Technology 3.0 — 中英对照翻译

> **MindShare PCI Express Technology 3.0** 英文原版的中英对照双语翻译项目。
> 由 Mike Jackson 和 Ravi Budruk 著，MindShare, Inc. 出版。

## 📚 章节列表

| 章节 | 文件 | 内容 | 页码 |
|:---|:---|:---|---:|
| Ch01 | [Ch01_Front_Matter_and_Introduction.md](Ch01_Front_Matter_and_Introduction.md) | 前言、版权、目录、PCI/PCI-X 背景介绍 | pp 1-99 |
| Ch02 | [Ch02_PCIe_Architecture_Overview.md](Ch02_PCIe_Architecture_Overview.md) | PCIe 架构概述（分层、TLP、带宽） | pp 100-145 |
| Ch03 | [Ch03_Configuration_Overview.md](Ch03_Configuration_Overview.md) | 配置机制（CF8h/CFCh、ECAM、枚举） | pp 146-181 |
| Ch04 | [Ch04_Address_Space_and_Transaction_Routing.md](Ch04_Address_Space_and_Transaction_Routing.md) | 地址空间与事务路由（BAR、路由） | pp 182-229 |
| Ch05 | [Ch05_TLP_Elements.md](Ch05_TLP_Elements.md) | TLP 元素（Header 格式、类型） | pp 230-275 |
| Ch06 | [Ch06_Flow_Control.md](Ch06_Flow_Control.md) | 流控（信用机制、初始化） | pp 276-305 |
| Ch07 | [Ch07_Quality_of_Service.md](Ch07_Quality_of_Service.md) | QoS/VC（流量类、仲裁、等时） | pp 306-345 |
| Ch08 | [Ch08_Transaction_Ordering.md](Ch08_Transaction_Ordering.md) | 事务排序（排序规则、IDO） | pp 346-367 |
| Ch09 | [Ch09_DLLP_Elements.md](Ch09_DLLP_Elements.md) | DLLP 元素（类型、格式） | pp 368-377 |
| Ch10 | [Ch10_AckNak_Protocol.md](Ch10_AckNak_Protocol.md) | Ack/Nak 协议（重传、超时） | pp 378-421 |
| Ch11 | [Ch11_Physical_Layer_Logical_Gen1_Gen2.md](Ch11_Physical_Layer_Logical_Gen1_Gen2.md) | 物理层逻辑 Gen1/Gen2（8b/10b、条带化） | pp 422-467 |
| Ch12 | [Ch12_Physical_Layer_Logical_Gen3.md](Ch12_Physical_Layer_Logical_Gen3.md) | 物理层逻辑 Gen3（128b/130b、加扰） | pp 468-507 |
| Ch13 | [Ch13_Physical_Layer_Electrical.md](Ch13_Physical_Layer_Electrical.md) | 物理层电气（差分信号、均衡、眼图） | pp 508-565 |
| Ch14 | [Ch14_Link_Initialization_Training.md](Ch14_Link_Initialization_Training.md) | 链路初始化与训练（LTSSM） | pp 566-707 |
| Ch15 | [Ch15_Error_Detection_Handling.md](Ch15_Error_Detection_Handling.md) | 错误检测与处理（AER、错误分类） | pp 708-763 |
| Ch16 | [Ch16_Power_Management.md](Ch16_Power_Management.md) | 电源管理（ASPM、L0s/L1/L2） | pp 764-853 |
| Ch17 | [Ch17_Interrupt_Support.md](Ch17_Interrupt_Support.md) | 中断支持（INTx、MSI、MSI-X） | pp 854-893 |
| Ch18 | [Ch18_Optional_Features.md](Ch18_Optional_Features.md) | 可选特性（LTR、OBFF、TPH、FLR、DPA） | pp 894-907 |
| Ch19 | [Ch19_Hot_Plug_Power_Budgeting.md](Ch19_Hot_Plug_Power_Budgeting.md) | 热插拔与功率预算 | pp 908-947 |
| Ch20 | [Ch20_Updates_Spec_Rev_2.1.md](Ch20_Updates_Spec_Rev_2.1.md) | Spec 2.1 修订更新 | pp 948-1057 |
| Appendix | [Appendix.md](Appendix.md) | 附录（索引、术语表） | pp 948-1057 |

## 📖 格式说明

### 翻译格式

全书采用 **中英对照 HTML 表格** 格式：

```html
<table>
<tr>
<td width="50%">
English original text paragraph.
</td>
<td width="50%" style="background-color:#e8e8e8">
中文翻译段落。
</td>
</tr>
</table>
```

### 标题格式

```markdown
## Section Title | 中文小节标题
```

### 图片

```html
Figure X-Y: English Description | 图X-Y：中文描述

<img src="images/xxx.jpg" width="700" alt="">
```

- Figure 标题在上，`<img>` 在下一行，中间空一行
- 图片路径相对于仓库根目录 `images/`

### 技术术语保留

- 寄存器名、信号名、代码、十六进制值、位域保持英文原文
- 协议字段名（TLP、DLLP、LTSSM 状态等）保持英文
- 首次出现的关键术语标注 `EN（中文）`

## 🛠 工具集

`tools/` 目录包含翻译管线工具：

| 工具 | 用途 |
|:---|:---|
| `build_chapters.py` | 将 output chunks 合并为章节文件 |
| `convert_to_html_format.py` | Markdown 表格 → HTML 表格格式 |
| `fix_figures_tables.py` | 修复图片/表格引用和格式 |
| `fix_headings.py` | 标题 EN\|CN 双语化 |
| `add_bilingual_captions.py` | Figure/Table 标题双语化 |
| `audit_images.py` | 检查图片引用完整性 |
| `README.md` | 工具说明 |

## 📦 目录结构

```
/
├── Ch01_*.md ~ Ch21_Appendix.md   ← 中英对照章节
├── images/                          ← 书中插图（489张）
│   └── partXX_*.jpg
├── figures_legacy/                  ← 早期版本截图（605张）
│   ├── embedded/                    ← 独立裁剪图片
│   │   ├── pageXXXX_imgX.png
│   │   └── pageXXXX_imgX_tight.png  ← 紧凑裁剪版
│   ├── chapter_*/page/              ← 整页截图
│   └── chapter_pages.json           ← 页码映射
├── tools/                           ← 翻译管线工具
├── MindShare_PCI_Express_Technology_3.0_temp/  ← 翻译工作目录
│   ├── chunk*.md                    ← 源切片
│   ├── output_chunk*.md             ← 翻译输出
│   ├── glossary.json                ← 术语表
│   └── config.txt                   ← 配置
└── book.md                          ← MinerU 合并原文
```

## 🖼️ 图片提取与处理策略

### 数据来源

本书图片有两种来源：

| 来源 | 生成方式 | 数量 | 命名 | 特点 |
|:---|:---|---:|:---|:---|
| **MinerU 提取** | MinerU V4 自动从 PDF 提取内嵌图片 | 489 张 | `partXX_<sha256>.jpg` | 内容准确、文件名散列 |
| **早期版截图** | 早期翻译项目从 PDF 截取的页面/图片 | 605 张 | `pageXXXX_imgX[_tight].png` | 含紧凑裁剪版（`_tight`） |

### Figure 匹配策略

由于 MinerU 提取是自动化的，部分图片与 Figure 标题的匹配存在以下问题：

1. **装饰性图片被误标为 Figure**：PDF 中的背景图、装饰元素被 MinerU 提取并赋予了 Figure 标题
2. **Figure 标题重复**：同一 Figure 编号被 MinerU 分配到多个 chunk 中
3. **图片位置偏移**：图片在 chunk 中的位置与正文引用位置不完全对齐

**处理原则**：
- 以 PDF TOC 中的 List of Figures 为准确定正确的 Figure 标题
- 每个 Figure 编号只保留一个正确的标题和配图
- 错误的 Figure 标题和配图直接删除（正文引用保留）
- 优先使用 MinerU 提取的 `images/` 图片；`figures_legacy/` 提供备用参考

### Figure 格式

```
Figure X-Y: English Description | 图X-Y：中文描述
                              ← 空行
<img src="images/xxx.jpg" width="700" alt="">
```

- Figure 标题使用双语（EN | CN）
- `<img>` 标签在标题下方，空一行分隔，确保 GitHub 渲染分行显示
- 技术表格和代码块保留英文原样，独立于双语表格之外

### 紧凑裁剪（Tight Crop）

`figures_legacy/embedded/` 目录中包含 `_tight.png` 后缀的紧凑裁剪版图片。这些图片去除了周围空白区域，内容更紧凑。目前作为备用参考，未被自动引用。

### 验证工具

```bash
# 审计图片留存率：对比源 chunks 与输出 chunks 的图片引用数
python3 tools/audit_images.py

# 检查 Figure/Table 标题是否双语化
grep -c '| 图' chapters/*.md

# 检查 <img> 标签格式
grep -c '<img src=' chapters/*.md
```

## 章节编号策略

```mermaid
graph LR
    A[PDF 原版] --> B[MinerU 提取]
    B --> C[merge_parts.py]
    C --> D[book.md]
    D --> E[chunk_book.py]
    E --> F[1360 chunks]
    F --> G[Sub-agent 翻译]
    G --> H[HTML 格式转换]
    H --> I[build_chapters.py]
    I --> J[21 章中英对照]
```

## 📄 许可

本翻译仅供学习和研究使用。原著版权归 MindShare, Inc. 所有。
