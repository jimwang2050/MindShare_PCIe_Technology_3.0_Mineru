# DLLP 元素

## 上一章

上一章讨论了PCI Express拓扑中事务的排序要求。这些规则继承自PCI,而Producer/Consumer(生产者/消费者)编程模型是其中许多规则的驱动因素,因此这里对其机制进行了描述。原始规则还考虑了必须避免的潜在的死锁(deadlock)条件,但并未包含任何手段来避免可能导致性能问题的情况。

## 本章内容

本章介绍另一大类数据包——数据链路层包 (DLLP)。我们将描述 DLLP 包类型的使用方式、格式和定义，以及其相关字段的详细信息。DLLP 用于支持 ACK/Nak 协议、电源管理、流控机制，甚至可用于厂商定义的目的。

## 下一章

下一章将介绍数据链路层的一项关键功能：一种基于硬件的自动机制，用于确保 TLP 跨链路的可靠传输。ACK DLLP 确认 TLP 已正确接收，而 Nak DLLP 则指示发生了传输错误。我们将描述在未检测到任何 TLP 或 DLLP 错误时的正常运行规则，以及与 TLP 和 DLLP 错误相关的错误恢复机制。

## 概述

数据链路层可以被视为管理较低层级链路协议的层次。其主要职责是确保设备之间传输的TLP的完整性，但它也在TLP流控、链路初始化和电源管理方面发挥作用，并在其上方的事务层与其下方的物理层之间传递信息。

## PCI Express 技术

在执行这些任务的过程中，数据链路层与其对端交换称为数据链路层包（DLLP）的报文。DLLP 在各设备的数据链路层之间进行通信。图 9-1（第 308 页）展示了设备之间交换 DLLP 的过程。

图 9-1: 数据链路层发送 DLLP
![](images/part03_c46d5e7c504582fae8e8d0a0f82ecd87129121c996919ba721010b23121fec66.jpg)

## DLLP 是本地流量

DLLP (数据链路层包) 具有简单的包格式，且长度固定，总共 8 字节（包括帧字节）。与 TLP (事务层包) 不同，DLLP 不携带任何目标或路由信息，因为它们仅用于相邻节点之间的通信，完全不参与路由。此外，事务层也看不到 DLLP，因为它们不属于该层所交换的信息的一部分。

## 接收端对DLLP的处理

当接收DLLP时，适用以下几条规则：

1. 它们在接收端立即被处理。换句话说，它们的流不能被控制，不像TLP那样(DLLP不受流控约束)。

2. 它们会被检查错误：首先在物理层进行检查，然后在数据链路层进行检查。包中包含的16位CRC通过计算应有的CRC值并与接收到的值进行比较来校验。未能通过此校验的DLLP将被丢弃。链路将如何从这种错误中恢复？DLLP仍会周期性到达，下一个同类型且校验成功的DLLP将更新缺失的信息。

3. 与TLP不同，DLLP没有确认协议。相反，规范定义了超时机制以便从失败的DLLP中恢复。

4. 如果没有错误，则确定DLLP类型并将其传递给相应的内部逻辑进行管理：

— Ack/Nak通知TLP状态

— 流控通知可用的缓冲区空间

— 电源管理设置

— 厂商特定信息

## 发送 DLLP

## 概述

这些包产生于数据链路层，并被传递至物理层。如果使用 8b/10b 编码（Gen1 和 Gen2 模式），则在此层级上发送包之前，DLLP（数据链路层包）的两端都将添加帧定界符号。在 Gen3 模式下，会在 DLLP 的前端添加一个两字节的 SDP 令牌，但不会在 DLLP 的末尾添加 END。第 310 页的图 9-2 展示了传输中的一个通用（Gen1/Gen2）DLLP，其中显示了帧定界符号及包的一般内容。

图 9-2：通用数据链路层包格式
![](images/part03_a0b69fd3472e6ba2599f0071c57184de764d0a48ad7a778898ed5ab9f89957f6.jpg)

## DLLP 包大小固定为 8 字节

无论是 8b/10b 编码还是 128b/130b 编码，数据链路层包（DLLP）始终为 8 字节长，由以下组成部分构成：

1. 一个 1 DW 核心（4 字节），包含一个一字节的 DLLP 类型字段和三个附加的属性字节。属性内容因 DLLP 类型而异。

2. 一个 2 字节的 CRC 值，基于 DLLP 核心内容计算得出。需要指出的是，此 CRC 与附加到 TLP 上的 LCRC 不同。该 CRC 仅为 16 位大小，其计算方式也与 TLP 中 32 位的 LCRC 不同。此 CRC 被附加到 DLLP 核心之后，然后将这 6 个字节传递给物理层。

3. 如果使用 8b/10b 编码，则会在包的起始和结束位置分别添加一个 DLLP 起始（SDP）控制符号和一个结束正确（END）控制符号。与通常情况一样，在传输之前，物理层将这些字节编码为 10 位符号用于传输。

4. 在 Gen3 模式下，当使用 128b/130b 编码时，会在包的前端添加一个 2 字节的 SDP Token，从而构成 8 字节的包，并且没有 END 符号或 Token。

注意，DLLP 从不会有数据有效载荷；所有信息均由包的核心四字节承载。

## DLLP 包类型

已定义的 DLLP 共有四组，分别涉及 ACK/Nak、电源管理、流控，此外还有一个厂商特定版本。其中一些 DLLP 有若干变体。表 9-1（第 311 页）总结了每种变体及其 DLLP 类型字段编码。

表 9-1：DLLP 类型

<table><tr><td>DLLP 类型</td><td>类型字段编码</td><td>用途</td></tr><tr><td>Ack (TLP 确认)</td><td>0000 0000b</td><td>TLP 传输完整性</td></tr><tr><td>Nak (TLP 否定确认)</td><td>0001 0000b</td><td>TLP 传输完整性</td></tr><tr><td>PM_Enter_L1</td><td>0010 0000b</td><td>电源管理</td></tr><tr><td>PM_Enter_L23</td><td>0010 0001b</td><td>电源管理</td></tr><tr><td>PM_Active_State_Request_L1</td><td>0010 0011b</td><td>电源管理</td></tr><tr><td>PM_Request_Ack</td><td>0010 0100b</td><td>电源管理</td></tr><tr><td>厂商特定</td><td>0011 0000b</td><td>厂商定义</td></tr><tr><td>InitFC1-P</td><td>0100 0xxxb</td><td>TLP 流控 (xxx = VC 编号)</td></tr><tr><td>InitFC1-NP</td><td>0101 0xxxb</td><td>TLP 流控</td></tr><tr><td>InitFC1-Cpl</td><td>0110 0xxxb</td><td>TLP 流控</td></tr><tr><td>InitFC2-P</td><td>1100 0xxxb</td><td>TLP 流控</td></tr><tr><td>InitFC2-NP</td><td>1101 0xxxb</td><td>TLP 流控</td></tr><tr><td>InitFC2-Cpl</td><td>1110 0xxxb</td><td>TLP 流控</td></tr><tr><td>UpdateFC-P</td><td>1000 0xxxb</td><td>TLP 流控</td></tr><tr><td>UpdateFC-NP</td><td>1001 0xxxb</td><td>TLP 流控</td></tr><tr><td>UpdateFC-Cpl</td><td>1010 0xxxb</td><td>TLP 流控</td></tr><tr><td>保留</td><td>其他</td><td>保留</td></tr></table>

## ACK/Nak DLLP格式

设备用于确认(ACK)或否认(Nak)接收TLP的DLLP格式如图9-3所示,其字段在"ACK/Nak DLLP字段"(第313页)中有描述。关于这些如何用于处理ACK/Nak协议的更多讨论,请参阅第10章——题为"ACK/Nak协议",见第317页。

图9-3:ACK或Nak DLLP格式  
![](images/part03_f17461775429bb7cd84d13bc3dec9d37f6e4a72b5bed76b2b4269047daa09460.jpg)

表9-2:ACK/Nak DLLP字段

<table><tr><td>字段名称</td><td>头字节/位</td><td>DLLP功能</td></tr><tr><td>DLLP类型</td><td>字节0, [7:0]</td><td>指示DLLP的类型:0000 0000b = ACK0001 0000b = Nak</td></tr><tr><td>AckNak_Seq_Num</td><td>字节2, [3:0]字节3, [7:0]</td><td>如果接收到正确的TLP:如果传入的序列号 = NEXT_RCV_SEQ(与预期的匹配),则调度携带该编号的ACK DLLP。如果传入的序列号早于NEXT_RCV_SEQ计数(接收到重复的TLP),则调度携带NEXT_RCV_SEQ - 1的ACK DLLP(实际上,这是最后一个正确TLP的编号)。对于接收到有问题的TLP:如果TLP有错误,或其序列号大于NEXT_RCV_SEQ,则调度携带NEXT_RCV_SEQ - 1的Nak DLLP。</td></tr><tr><td>16位CRC</td><td>字节4, [7:0]字节5, [7:0]</td><td>此16位CRC保护此DLLP的内容。计算基于ACK/Nak的字节0-3。</td></tr></table>

## 电源管理 DLLP 格式

电源管理 DLLP 信息如图 9-4 所示，其字段描述见表 9-3 (第 314 页)。关于这些数据包在电源管理中的使用的更多信息，请参阅第 16 章"电源管理"(第 703 页)。

图 9-4: 电源管理 DLLP 格式  
![](images/part03_183802acbcce55b0de64cd8c09e982d43c85c7db1a8912272e6fda8105e4b2b8.jpg)

表 9-3: 电源管理 DLLP 字段

<table><tr><td>字段名称</td><td>头部字节/位</td><td>DLLP 功能</td></tr><tr><td>DLLP 类型</td><td>字节 0, [7:0]</td><td>指示 DLLP 类型。对于电源管理 DLLP:<br/>0010 0000b = PM_Enter_L1<br/>0010 0001b = PM_Enter_L23<br/>0010 0011b = PM_Active_State_Request_L1<br/>0010 0100b = PM_Request_Ack</td></tr><tr><td>16 位 CRC</td><td>字节 4, [7:0]<br/>字节 5, [7:0]</td><td>用于保护 DLLP 内容的 16 位 CRC。基于字节 0-3 进行计算，无论这些字段是否被使用。</td></tr></table>

## 流控 DLLP 格式

与许多其他串行传输总线类似，PCIe 通过使用基于信用的流控方案来提高传输效率。该主题在第 6 章（标题为"流控"，第 215 页）中有详细阐述。DLLP 用于传递流控信用信息。多种不同的 DLLP 用于初始化流控信用。另一类更新 DLLP 用于在接收器缓冲区空间回收时管理运行时的信用管理。有两种流控初始化 DLLP，分别称为 InitFC1 和 InitFC2，以及一种流控更新 DLLP，称为 UpdateFC。

所有三种变体的包格式如图 9-5（第 315 页）所示，而表 9-4（第 315 页）描述了其中包含的字段。

图 9-5: 流控 DLLP 格式
![](images/part03_940c6bec3506e8ca08d228126a03402fb96c706db13e7d2a8f81e391e4f0ccde.jpg)

表 9-4: 流控 DLLP 字段

<table><tr><td>字段名称</td><td>头部字节/位</td><td>DLLP 功能</td></tr><tr><td rowspan="3">DLLP 类型</td><td>Byte 0, [7:4]</td><td>此代码指示 FC DLLP 的类型：0100b = InitFC1-P (Posted 请求)0101b = InitFC1-NP (Non-Posted 请求)0110b = InitFC1-Cpl (完成报文)0101b = InitFC2-P (Posted 请求)1101b = InitFC2-NP (Non-Posted 请求)1110b = InitFC2-Cpl (完成报文)1000b = UpdateFC-P (Posted 请求)1001b = UpdateFC-NP (Non-Posted 请求)1010b = UpdateFC-Cpl (完成报文)</td></tr><tr><td>Byte 0, [3]</td><td>必须为 0b，作为流控编码的一部分。</td></tr><tr><td>Byte 0, [2:0]</td><td>VC ID。指示要使用这些信用更新的虚通道（VC 0-7）。</td></tr><tr><td>HdrFC</td><td>Byte 1, [5:0]Byte 2, [7:6]</td><td>包含指定虚通道的头部存储信用计数。每个信用代表 1 个头部 + 可选的 TLP Digest (ECRC) 的存储空间。</td></tr><tr><td>DataFC</td><td>Byte 2, [3:0]Byte 3, [7:0]</td><td>包含指定虚通道的数据存储信用计数。每个信用代表 16 字节。</td></tr><tr><td>16-bit CRC</td><td>Byte 4, [7:0]Byte 5, [7:0]</td><td>保护此 DLLP 内容的 16 位 CRC。计算基于字节 0-3，无论是否使用了所有字段。</td></tr></table>

## 厂商自定义 DLLP 格式

最后一种定义的 DLLP 类型用于厂商自定义用途。因此，规范仅定义了 DLLP 类型字段（0011 0000b），其余内容可供厂商自定义使用。

图 9-6：厂商自定义 DLLP 格式

<table><tr><td rowspan="2"></td><td>+0</td><td>+1</td><td>+2</td><td>+3</td></tr><tr><td>7|6|5|4|3|2|1|0</td><td>7|6|5|4|3|2|1|0</td><td>7|6|5|4|3|2|1|0</td><td>7|6|5|4|3|2|1|0</td></tr><tr><td>Byte 0</td><td>0 0 1 1 0 0 0 0</td><td colspan="3">厂商自定义</td></tr><tr><td>Byte 4</td><td colspan="2">16 位 CRC</td><td colspan="2"></td></tr></table>