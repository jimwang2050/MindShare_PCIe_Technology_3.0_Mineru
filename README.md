# MindShare PCI Express Technology 3.0 — 中英对照翻译

> **MindShare PCI Express Technology 3.0** 英文原版的中英对照双语翻译项目。
> 由 Mike Jackson 和 Ravi Budruk 著，MindShare, Inc. 出版。

## 📚 章节列表

| 章节 | 文件 | 内容 | 大小 |
|:---|:---|:---|---:|
| Ch01 | [Ch01_Front_Matter_and_Introduction.md](Ch01_Front_Matter_and_Introduction.md) | 前言、版权、目录、PCI/PCI-X 背景介绍 | 416 KB |
| Ch02 | [Ch02_PCIe_Architecture_Overview.md](Ch02_PCIe_Architecture_Overview.md) | PCIe 架构概述（分层、TLP、带宽） | 173 KB |
| Ch03 | [Ch03_Configuration_Overview.md](Ch03_Configuration_Overview.md) | 配置机制（CF8h/CFCh、ECAM、枚举） | 93 KB |
| Ch04 | [Ch04_Address_Space_and_Transaction_Routing.md](Ch04_Address_Space_and_Transaction_Routing.md) | 地址空间与事务路由（BAR、路由） | 191 KB |
| Ch05 | [Ch05_TLP_Elements.md](Ch05_TLP_Elements.md) | TLP 元素（Header 格式、类型） | 53 KB |
| Ch06 | [Ch06_Flow_Control.md](Ch06_Flow_Control.md) | 流控（信用机制、初始化） | 67 KB |
| Ch07 | [Ch07_Quality_of_Service.md](Ch07_Quality_of_Service.md) | QoS/VC（流量类、仲裁、等时） | 99 KB |
| Ch08 | [Ch08_Transaction_Ordering.md](Ch08_Transaction_Ordering.md) | 事务排序（排序规则、IDO） | 56 KB |
| Ch09 | [Ch09_DLLP_Elements.md](Ch09_DLLP_Elements.md) | DLLP 元素（类型、格式） | 19 KB |
| Ch10 | [Ch10_AckNak_Protocol.md](Ch10_AckNak_Protocol.md) | Ack/Nak 协议（重传、超时） | 144 KB |
| Ch11 | [Ch11_Physical_Layer_Logical_Gen1_Gen2.md](Ch11_Physical_Layer_Logical_Gen1_Gen2.md) | 物理层逻辑 Gen1/Gen2（8b/10b、条带化） | 132 KB |
| Ch12 | [Ch12_Physical_Layer_Logical_Gen3.md](Ch12_Physical_Layer_Logical_Gen3.md) | 物理层逻辑 Gen3（128b/130b、加扰） | 204 KB |
| Ch13 | [Ch13_Physical_Layer_Electrical.md](Ch13_Physical_Layer_Electrical.md) | 物理层电气（差分信号、均衡、眼图） | 430 KB |
| Ch14 | [Ch14_Link_Initialization_Training.md](Ch14_Link_Initialization_Training.md) | 链路初始化与训练（LTSSM） | 227 KB |
| Ch15 | [Ch15_Error_Detection_Handling.md](Ch15_Error_Detection_Handling.md) | 错误检测与处理（AER、错误分类） | 218 KB |
| Ch16 | [Ch16_Power_Management.md](Ch16_Power_Management.md) | 电源管理（ASPM、L0s/L1/L2） | 165 KB |
| Ch17 | [Ch17_Interrupt_Support.md](Ch17_Interrupt_Support.md) | 中断支持（INTx、MSI、MSI-X） | 105 KB |
| Ch18 | [Ch18_Optional_Features.md](Ch18_Optional_Features.md) | 可选特性（LTR、OBFF、TPH、FLR、DPA） | 78 KB |
| Ch19 | [Ch19_Hot_Plug_Power_Budgeting.md](Ch19_Hot_Plug_Power_Budgeting.md) | 热插拔与功率预算 | 113 KB |
| Ch20 | [Ch20_Updates_Spec_Rev_2.1.md](Ch20_Updates_Spec_Rev_2.1.md) | Spec 2.1 修订更新 | 89 KB |
| Appendix | [Appendix.md](Appendix.md) | 附录（索引、术语表） | 56 KB |

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
<img src="images/xxx.jpg" width="700" alt="">
Figure X-Y: English Description | 图X-Y：中文描述
```

图片位于对应的 Figure 标题下方，图片路径相对于仓库根目录的 `images/` 文件夹。

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

## 📋 管线流程

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
