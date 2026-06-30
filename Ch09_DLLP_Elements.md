# Ch09_DLLP_Elements

<table style="border:2px solid #000;border-collapse:collapse; width:100%;" cellpadding="4" cellspacing="0" rules="all" frame="border">
  <thead style="border:2px solid #000;">
    <tr>
      <th width="50%" style="border:2px solid #000; background:#f5f5f5;">EN</th>
      <th width="50%" style="border:2px solid #000; background-color:#e8e8e8;">中文</th>
    </tr>
  </thead>
  <tbody>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;"># DLLP Elements</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;"># DLLP 元素</td></tr>
  </tbody>
</table>


<table style="border:2px solid #000;border-collapse:collapse; width:100%;" cellpadding="4" cellspacing="0" rules="all" frame="border">
  <thead style="border:2px solid #000;">
    <tr>
      <th width="50%" style="border:2px solid #000; background:#f5f5f5;">EN</th>
      <th width="50%" style="border:2px solid #000; background-color:#e8e8e8;">中文</th>
    </tr>
  </thead>
  <tbody>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">## The Previous Chapter</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">## 前一章</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">The previous chapter discussed the ordering requirements for transactions in a PCI Express topology. These rules are inherited from PCI, and the Producer/Consumer programming model motivated many of them, so its mechanism is described here. The original rules also took into consideration possible deadlock conditions that must be avoided, but did not include any means to avoid the performance problems that could result.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">前一章讨论了PCI Express拓扑中事务的排序要求。这些规则继承自PCI，其中许多规则源自生产者/消费者编程模型，因此本文描述了其机制。原始规则还考虑了必须避免的可能死锁条件，但未包含任何避免由此可能导致的性能问题的方法。</td></tr>
  </tbody>
</table>


## This Chapter | 本章

<table style="border:2px solid #000;border-collapse:collapse; width:100%;" cellpadding="4" cellspacing="0" rules="all" frame="border">
  <thead style="border:2px solid #000;">
    <tr>
      <th width="50%" style="border:2px solid #000; background:#f5f5f5;">EN</th>
      <th width="50%" style="border:2px solid #000; background-color:#e8e8e8;">中文</th>
    </tr>
  </thead>
  <tbody>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">In this chapter we describe the other major category of packets, Data Link Layer Packets (DLLPs). We describe the use, format, and definition of the DLLP packet types and the details of their related fields. DLLPs are used to support Ack/Nak protocol, power management, flow control mechanism and can even be used for vendor-defined purposes.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">本章描述另一大类报文——数据链路层报文(DLLP)。我们阐述DLLP报文类型的使用、格式和定义及其相关字段的细节。DLLP用于支持Ack/Nak协议、电源管理、流控机制，甚至可用于供应商自定义目的。</td></tr>
  </tbody>
</table>


## The Next Chapter | 下一章

<table style="border:2px solid #000;border-collapse:collapse; width:100%;" cellpadding="4" cellspacing="0" rules="all" frame="border">
  <thead style="border:2px solid #000;">
    <tr>
      <th width="50%" style="border:2px solid #000; background:#f5f5f5;">EN</th>
      <th width="50%" style="border:2px solid #000; background-color:#e8e8e8;">中文</th>
    </tr>
  </thead>
  <tbody>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">The following chapter describes a key feature of the Data Link Layer: an automatic, hardware‑based mechanism for ensuring reliable transport of TLPs across the Link. Ack DLLPs confirm good reception of TLPs while Nak DLLPs indicate a transmission error. We describe the normal rules of operation when no TLP or DLLP error is detected as well as error recovery mechanisms associated with both TLP and DLLP errors.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">下一章描述数据链路层的一个关键特性：一种基于硬件的自动机制，用于确保TLP在链路上的可靠传输。Ack DLLP确认TLP的正确接收，而Nak DLLP指示传输错误。我们将描述未检测到TLP或DLLP错误时的正常操作规则，以及与TLP和DLLP错误相关的错误恢复机制。</td></tr>
  </tbody>
</table>


<table style="border:2px solid #000;border-collapse:collapse; width:100%;" cellpadding="4" cellspacing="0" rules="all" frame="border">
  <thead style="border:2px solid #000;">
    <tr>
      <th width="50%" style="border:2px solid #000; background:#f5f5f5;">EN</th>
      <th width="50%" style="border:2px solid #000; background-color:#e8e8e8;">中文</th>
    </tr>
  </thead>
  <tbody>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">## General</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">## 概述</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">The Data Link Layer can be thought of as managing the lower level Link protocol. Its primary responsibility is to assure the integrity of TLPs moving between devices, but it also plays a part in TLP flow control, Link initialization and power management, and conveys information between the Transaction Layer above it and the Physical Layer below it.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">数据链路层可视为管理低级链路协议。其主要职责是确保设备间传输的TLP的完整性，但它也在TLP流控、链路初始化和电源管理中发挥作用，并在其上方面的事务层和其下方的物理层之间传递信息。</td></tr>
  </tbody>
</table>


## PCI Express Technology | PCI Express 技术

<table style="border:2px solid #000;border-collapse:collapse; width:100%;" cellpadding="4" cellspacing="0" rules="all" frame="border">
  <thead style="border:2px solid #000;">
    <tr>
      <th width="50%" style="border:2px solid #000; background:#f5f5f5;">EN</th>
      <th width="50%" style="border:2px solid #000; background-color:#e8e8e8;">中文</th>
    </tr>
  </thead>
  <tbody>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">In performing these jobs, the Data Link Layer exchanges packets with its neighbor known as Data Link Layer Packets (DLLPs). DLLPs are communicated between the Data Link Layers of each device. Figure 9-1 on page 308 illustrates a DLLP exchanged between devices.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">在执行这些任务时，数据链路层与其对等层交换称为数据链路层报文（DLLP）的包。DLLP在各个设备的数据链路层之间进行通信。第308页的图9-1展示了设备之间交换的DLLP。</td></tr>
  </tbody>
</table>


Figure 9-1: Data Link Layer Sends A DLLP | 图9-1：数据链路层发送DLLP

<img src="images/part03_c46d5e7c504582fae8e8d0a0f82ecd87129121c996919ba721010b23121fec66.jpg" width="700" alt="">

## 9.1 DLLPs Are Local Traffic | 9.1 DLLP 是本地流量

<table style="border:2px solid #000;border-collapse:collapse; width:100%;" cellpadding="4" cellspacing="0" rules="all" frame="border">
  <thead style="border:2px solid #000;">
    <tr>
      <th width="50%" style="border:2px solid #000; background:#f5f5f5;">EN</th>
      <th width="50%" style="border:2px solid #000; background-color:#e8e8e8;">中文</th>
    </tr>
  </thead>
  <tbody>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">DLLPs have a simple packet format and are a fixed size, 8 bytes total, including the framing bytes.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">DLLP 具有简单的包格式，大小固定，包括帧头帧尾共 8 字节。</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">Unlike TLPs, they carry no target or routing information because they are only used for nearest-neighbor communications and don't get routed at all.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">与 TLP 不同，DLLP 不携带目标或路由信息，因为它们仅用于最近邻通信，完全不进行路由。</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">They're also not seen by the Transaction Layer since they're not part of the information exchanged at that level.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">它们也不被事务层所见，因为它们不属于该层交换的信息的一部分。</td></tr>
  </tbody>
</table>


## 9.2 Receiver handling of DLLPs | 9.2 接收器处理 DLLP
## DLLP的接收处理

<table style="border:2px solid #000;border-collapse:collapse; width:100%;" cellpadding="4" cellspacing="0" rules="all" frame="border">
  <thead style="border:2px solid #000;">
    <tr>
      <th width="50%" style="border:2px solid #000; background:#f5f5f5;">EN</th>
      <th width="50%" style="border:2px solid #000; background-color:#e8e8e8;">中文</th>
    </tr>
  </thead>
  <tbody>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">When DLLPs are received, several rules apply:</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">接收DLLP时，适用以下几条规则：</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">1. They're immediately processed at the Receiver. In other words, their flow cannot be controlled the way it is for TLPs (DLLPs are not subject to flow control).</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">1. 它们在接收端被立即处理。换言之，不能像对TLP那样控制其流量（DLLP不受流控约束）。</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">2. They're checked for errors; first at the Physical Layer, and then at the Data Link Layer. The 16-bit CRC included with the packet is checked by calculating what the CRC should be and comparing it to the received value. DLLPs that fail this check are discarded. How will the Link recover from this error? DLLPs still arrive periodically, and the next one of that type that succeeds will update the missing information.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">2. 它们会先经物理层、再经数据链路层进行错误检查。通过计算CRC应有的值并与接收值比较，来检查报文中的16位CRC。检查失败的DLLP被丢弃。链路如何从此错误中恢复？DLLP仍会周期性到达，下一个同类型且成功的DLLP将更新缺失的信息。</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">3. Unlike TLPs, there's no acknowledgement protocol for DLLPs. Instead, the spec defines time-out mechanisms to facilitate recovery from failed DLLPs.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">3. 与TLP不同，DLLP没有确认协议。相反，规范定义了超时机制以便从失败的DLLP中恢复。</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">4. If there are no errors, the DLLP type is determined and passed to the appropriate internal logic to manage:</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">4. 若无错误，则确定DLLP类型并传递给相应的内部逻辑进行管理：</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">— Ack/Nak notification of TLP status</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">— TLP状态的Ack/Nak通知</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">— Flow Control notification of buffer space available</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">— 缓冲区可用空间的流控通知</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">— Power Management settings</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">— 电源管理设置</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">— Vendor specific information</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">— 厂商特定信息</td></tr>
  </tbody>
</table>


<table style="border:2px solid #000;border-collapse:collapse; width:100%;" cellpadding="4" cellspacing="0" rules="all" frame="border">
  <thead style="border:2px solid #000;">
    <tr>
      <th width="50%" style="border:2px solid #000; background:#f5f5f5;">EN</th>
      <th width="50%" style="border:2px solid #000; background-color:#e8e8e8;">中文</th>
    </tr>
  </thead>
  <tbody>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">## Sending DLLPs</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">## 发送DLLP</td></tr>
  </tbody>
</table>


## 9.2.1 General | 9.2.1 概述

<table style="border:2px solid #000;border-collapse:collapse; width:100%;" cellpadding="4" cellspacing="0" rules="all" frame="border">
  <thead style="border:2px solid #000;">
    <tr>
      <th width="50%" style="border:2px solid #000; background:#f5f5f5;">EN</th>
      <th width="50%" style="border:2px solid #000; background-color:#e8e8e8;">中文</th>
    </tr>
  </thead>
  <tbody>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">These packets originate at the Data Link Layer and are passed to the Physical Layer. If 8b/10b encoding is in use (Gen1 and Gen2 mode), framing symbols will be added to both ends of the DLLP at this level before the packet is sent. In Gen3 mode, a SDP token of two bytes is added to the front end of the DLLP, but no END is added to the end of the DLLP. Figure 9-2 on page 310 shows a generic (Gen1/Gen2) DLLP in transit, showing the framing symbols and the general contents of the packet.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">这些数据包起源于数据链路层，并被传递到物理层。如果使用8b/10b编码（Gen1和Gen2模式），在此层级会在DLLP的两端添加帧标记符号，然后再发送数据包。在Gen3模式下，一个两字节的SDP令牌被添加到DLLP的前端，但DLLP的末尾不添加END标记。第310页的图9-2展示了一个正在传输中的通用（Gen1/Gen2）DLLP，显示了帧标记符号和数据包的一般内容。</td></tr>
  </tbody>
</table>


Figure 9-2: Generic Data Link Layer Packet Format | 图9-2：通用数据链路层数据包格式
图9-2：通用数据链路层数据包格式

<img src="images/part03_a0b69fd3472e6ba2599f0071c57184de764d0a48ad7a778898ed5ab9f89957f6.jpg" width="700" alt="">

<table style="border:2px solid #000;border-collapse:collapse; width:100%;" cellpadding="4" cellspacing="0" rules="all" frame="border">
  <thead style="border:2px solid #000;">
    <tr>
      <th width="50%" style="border:2px solid #000; background:#f5f5f5;">EN</th>
      <th width="50%" style="border:2px solid #000; background-color:#e8e8e8;">中文</th>
    </tr>
  </thead>
  <tbody>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">## DLLP Packet Size is Fixed at 8 Bytes</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">## DLLP 报文大小固定为 8 字节</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">Data Link Layer Packets are always 8 bytes long for both 8b/10b and 128b/130b and consist of the following components:</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">无论采用 8b/10b 还是 128b/130b 编码，数据链路层报文始终为 8 字节长，由以下部分组成：</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">1. A 1 DW core (4 bytes) containing the one-byte DLLP Type field and three additional bytes of attributes. The attributes vary with the DLLP type.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">1. 1 个双字核心（4 字节），包含 1 字节的 DLLP 类型字段和 3 字节的属性。属性随 DLLP 类型而变化。</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">2. A 2-byte CRC value that is calculated based on the core contents of the DLLP. It is important to point out that this CRC is different from the LCRCs added to TLPs. This CRC is only 16 bits in size and is calculated differently than the 32-bit LCRCs in TLPs. This CRC is appended to the core DLLP and then these 6 bytes are passed to the Physical Layer.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">2. 2 字节的 CRC 值，基于 DLLP 核心内容计算得出。需要指出的是，此 CRC 不同于添加到 TLP 上的 LCRC。该 CRC 仅为 16 位，其计算方式与 TLP 中的 32 位 LCRC 不同。此 CRC 附加到 DLLP 核心之后，然后将这 6 字节传递给物理层。</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">3. If 8b/10b encoding is in use, a Start of DLLP (SDP) control symbol and an End Good (END) control symbol are added to the beginning and end of the packet. As usual, before transmission the Physical Layer encodes the bytes into 10-bit symbols for transmission.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">3. 如果使用 8b/10b 编码，则会在报文开头和结尾分别添加一个 DLLP 起始（SDP）控制符号和一个结束良好（END）控制符号。通常情况下，在传输前物理层将字节编码为 10 位符号进行发送。</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">4. In Gen3 mode, when 128b/130b encoding is in use, a 2-byte SDP Token is added to the front of the packet to create the 8-byte packet and there is no END symbol or token.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">4. 在 Gen3 模式下，当使用 128b/130b 编码时，在报文前添加 2 字节的 SDP Token 以构成 8 字节报文，且没有 END 符号或 Token。</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">Note that there is never a data payload with a DLLP; all the information is carried in the core four bytes of the packet.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">注意，DLLP 从不携带数据负载；所有信息均在报文的 4 字节核心中承载。</td></tr>
  </tbody>
</table>


## 9.4 DLLP Packet Types | 9.4 DLLP包类型

<table style="border:2px solid #000;border-collapse:collapse; width:100%;" cellpadding="4" cellspacing="0" rules="all" frame="border">
  <thead style="border:2px solid #000;">
    <tr>
      <th width="50%" style="border:2px solid #000; background:#f5f5f5;">EN</th>
      <th width="50%" style="border:2px solid #000; background-color:#e8e8e8;">中文</th>
    </tr>
  </thead>
  <tbody>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">There are four groups of DLLPs defined that deal with Ack/Nak, Power Management, and Flow Control, along with one Vendor Specific version. Some of these have several variants, and Table 9-1 on page 311 summarizes each variant as well as their DLLP Type field encoding.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">定义了四组DLLP，分别处理Ack/Nak、电源管理（Power Management）和流控（Flow Control），外加一个厂商特定（Vendor Specific）版本。其中一些有多个变体，表9-1（第311页）总结了每个变体及其DLLP类型字段编码。</td></tr>
  </tbody>
</table>


Table 9-1: DLLP Types / 表9-1：DLLP类型 | 表9-1：DLLP类型

<table style="border:2px solid #000;border-collapse:collapse;width:100%" cellpadding="4" cellspacing="0" rules="all" frame="border"><tr><td style="border:2px solid #000;">DLLP Type</td><td style="border:2px solid #000;">Type Field Encoding</td><td style="border:2px solid #000;">Purpose</td></tr><tr><td style="border:2px solid #000;">Ack (TLP Acknowledge)</td><td style="border:2px solid #000;">0000 0000b</td><td style="border:2px solid #000;">TLP transmission integrity</td></tr><tr><td style="border:2px solid #000;">Nak (TLP Negative Acknowledge)</td><td style="border:2px solid #000;">0001 0000b</td><td style="border:2px solid #000;">TLP transmission integrity</td></tr><tr><td style="border:2px solid #000;">PM_Enter_L1</td><td style="border:2px solid #000;">0010 0000b</td><td style="border:2px solid #000;">Power Management</td></tr><tr><td style="border:2px solid #000;">PM_Enter_L23</td><td style="border:2px solid #000;">0010 0001b</td><td style="border:2px solid #000;">Power Management</td></tr><tr><td style="border:2px solid #000;">PM_Active_State_Request_L1</td><td style="border:2px solid #000;">0010 0011b</td><td style="border:2px solid #000;">Power Management</td></tr><tr><td style="border:2px solid #000;">PM_Request_Ack</td><td style="border:2px solid #000;">0010 0100b</td><td style="border:2px solid #000;">Power Management</td></tr><tr><td style="border:2px solid #000;">Vendor Specific</td><td style="border:2px solid #000;">0011 0000b</td><td style="border:2px solid #000;">Vendor Defined</td></tr><tr><td style="border:2px solid #000;">InitFC1-P</td><td style="border:2px solid #000;">0100 0xxxb</td><td style="border:2px solid #000;">TLP Flow Control (xxx = VC number)</td></tr><tr><td style="border:2px solid #000;">InitFC1-NP</td><td style="border:2px solid #000;">0101 0xxxb</td><td style="border:2px solid #000;">TLP Flow Control</td></tr><tr><td style="border:2px solid #000;">InitFC1-Cpl</td><td style="border:2px solid #000;">0110 0xxxb</td><td style="border:2px solid #000;">TLP Flow Control</td></tr><tr><td style="border:2px solid #000;">InitFC2-P</td><td style="border:2px solid #000;">1100 0xxxb</td><td style="border:2px solid #000;">TLP Flow Control</td></tr><tr><td style="border:2px solid #000;">InitFC2-NP</td><td style="border:2px solid #000;">1101 0xxxb</td><td style="border:2px solid #000;">TLP Flow Control</td></tr><tr><td style="border:2px solid #000;">InitFC2-Cpl</td><td style="border:2px solid #000;">1110 0xxxb</td><td style="border:2px solid #000;">TLP Flow Control</td></tr><tr><td style="border:2px solid #000;">UpdateFC-P</td><td style="border:2px solid #000;">1000 0xxxb</td><td style="border:2px solid #000;">TLP Flow Control</td></tr><tr><td style="border:2px solid #000;">UpdateFC-NP</td><td style="border:2px solid #000;">1001 0xxxb</td><td style="border:2px solid #000;">TLP Flow Control</td></tr><tr><td style="border:2px solid #000;">UpdateFC-Cpl</td><td style="border:2px solid #000;">1010 0xxxb</td><td style="border:2px solid #000;">TLP Flow Control</td></tr><tr><td style="border:2px solid #000;">Reserved</td><td style="border:2px solid #000;">Others</td><td style="border:2px solid #000;">Reserved</td></tr></table>

## 9.3.1 Ack/Nak DLLP Format | 9.3.1 Ack/Nak DLLP 格式

<table style="border:2px solid #000;border-collapse:collapse; width:100%;" cellpadding="4" cellspacing="0" rules="all" frame="border">
  <thead style="border:2px solid #000;">
    <tr>
      <th width="50%" style="border:2px solid #000; background:#f5f5f5;">EN</th>
      <th width="50%" style="border:2px solid #000; background-color:#e8e8e8;">中文</th>
    </tr>
  </thead>
  <tbody>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">The format of the DLLP used by a device to Ack (acknowledge) or Nak (negatively acknowledge) the receipt of a TLP is illustrated in Figure 9‑3, and its fields are described in "Ack/Nak DLLP Fields" on page 313. For more discussion on how these are used to handle the Ack/Nak protocol, refer to Chapter 10, entitled "Ack/Nak Protocol," on page 317.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">设备用于确认（Ack）或否定确认（Nak）TLP 接收的 DLLP 格式如图 9‑3 所示，其字段在第 313 页的"Ack/Nak DLLP 字段"中描述。关于这些字段如何用于处理 Ack/Nak 协议的更多讨论，请参阅第 317 页第 10 章"Ack/Nak 协议"。</td></tr>
  </tbody>
</table>


Figure 9‑3: Ack Or Nak DLLP Format | 图9‑3：Ack或Nak DLLP格式  

<img src="images/part03_f17461775429bb7cd84d13bc3dec9d37f6e4a72b5bed76b2b4269047daa09460.jpg" width="700" alt="">

Table 9‑2: Ack/Nak DLLP Fields | 表9‑2：Ack/Nak DLLP字段

<table style="border:2px solid #000;border-collapse:collapse;width:100%" cellpadding="4" cellspacing="0" rules="all" frame="border"><tr><td style="border:2px solid #000;">Field Name</td><td style="border:2px solid #000;">Header Byte/Bit</td><td style="border:2px solid #000;">DLLP Function</td></tr><tr><td style="border:2px solid #000;">DLLP Type</td><td style="border:2px solid #000;">Byte 0, [7:0]</td><td style="border:2px solid #000;">Indicates the type of DLLP:0000 0000b = Ack0001 0000b = Nak</td></tr><tr><td style="border:2px solid #000;">AckNak_Seq_Num</td><td style="border:2px solid #000;">Byte 2, [3:0]Byte 3, [7:0]</td><td style="border:2px solid #000;">If a good TLP was received:If incoming Sequence Number = NEXT_RCV_SEQ (matched what was expected), schedule Ack DLLP with that number.If incoming Sequence Number was earlier than NEXT_RCV_SEQ count (a duplicate TLP was received), schedule Ack DLLP with NEXT_RCV_SEQ - 1 (effectively, this is the number of the last good TLP).For a TLP received with a problem:If the TLP had an error, or its Sequence Number was higher than NEXT_RCV_SEQ, schedule a Nak DLLP with NEXT_RCV_SEQ - 1.</td></tr><tr><td style="border:2px solid #000;">16-bit CRC</td><td style="border:2px solid #000;">Byte 4, [7:0]Byte 5, [7:0]</td><td style="border:2px solid #000;">This 16-bit CRC protects the contents of this DLLP. Calculation is based on Bytes 0-3 of the Ack/Nak.</td></tr></table>

## 9.4.2 Power Management DLLP Format | 9.4.2 电源管理DLLP格式

<table style="border:2px solid #000;border-collapse:collapse; width:100%;" cellpadding="4" cellspacing="0" rules="all" frame="border">
  <thead style="border:2px solid #000;">
    <tr>
      <th width="50%" style="border:2px solid #000; background:#f5f5f5;">EN</th>
      <th width="50%" style="border:2px solid #000; background-color:#e8e8e8;">中文</th>
    </tr>
  </thead>
  <tbody>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">Power management DLLP information is shown in Figure 9-4, and its fields are described in Table 9-3 on page 314. To learn more about the use of these packets in power management, refer to Chapter 16, entitled "Power Management," on page 703.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">电源管理DLLP信息如图9-4所示，其字段在314页的表9-3中描述。要了解更多关于这些报文在电源管理中的使用，请参阅703页的第16章"电源管理"。</td></tr>
  </tbody>
</table>


Figure 9-4: Power Management DLLP Format | 图9-4：电源管理DLLP格式

<img src="images/part03_183802acbcce55b0de64cd8c09e982d43c85c7db1a8912272e6fda8105e4b2b8.jpg" width="700" alt="">

Table 9-3: Power Management DLLP Fields / 表9-3：电源管理DLLP字段 | 表9-3：电源管理DLLP字段

<table style="border:2px solid #000;border-collapse:collapse;width:100%" cellpadding="4" cellspacing="0" rules="all" frame="border"><tr><td style="border:2px solid #000;">Field Name / 字段名</td><td style="border:2px solid #000;">Header Byte/Bit / 头字节/位</td><td style="border:2px solid #000;">DLLP Function / DLLP功能</td></tr><tr><td style="border:2px solid #000;">DLLP Type / DLLP类型</td><td style="border:2px solid #000;">Byte 0, [7:0]</td><td style="border:2px solid #000;">Indicates DLLP type. For Power Management DLLPs:<br>0010 0000b = PM_Enter_L1<br>0010 0001b = PM_Enter_L2<br>0010 0011b = PM_Active_State_Request_L1<br>0010 0100b = PM_Request_Ack<br><br>指示DLLP类型。对于电源管理DLLP：<br>0010 0000b = PM_Enter_L1<br>0010 0001b = PM_Enter_L2<br>0010 0011b = PM_Active_State_Request_L1<br>0010 0100b = PM_Request_Ack</td></tr><tr><td style="border:2px solid #000;">16-bit CRC / 16位CRC</td><td style="border:2px solid #000;">Byte 4, [7:0]<br>Byte 5, [7:0]</td><td style="border:2px solid #000;">A 16-Bit CRC used to protect DLLP contents. Calculation is based on Bytes 0-3, regardless of whether fields are used.<br><br>用于保护DLLP内容的16位CRC。计算基于字节0-3，无论字段是否使用。</td></tr></table>

## 9.4.3 Flow Control DLLP Format | 9.4.3 流控 DLLP 格式

<table style="border:2px solid #000;border-collapse:collapse; width:100%;" cellpadding="4" cellspacing="0" rules="all" frame="border">
  <thead style="border:2px solid #000;">
    <tr>
      <th width="50%" style="border:2px solid #000; background:#f5f5f5;">EN</th>
      <th width="50%" style="border:2px solid #000; background-color:#e8e8e8;">中文</th>
    </tr>
  </thead>
  <tbody>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">Like many other serial transport buses, PCIe improves transport efficiency by using a credit‑based flow control scheme. This topic is covered in detail in Chapter 6, entitled "Flow Control," on page 215. DLLPs are used to communicate flow control credit information. A variety of different DLLPs initialize flow control credits. Another category of update DLLPs are used to manage the runtime credit management as receiver buffer space is recovered. There are two Flow Control Initialization DLLPs called InitFC1 and InitFC2, and one Flow Control Update DLLP called UpdateFC.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">与许多其他串行传输总线一样，PCIe 通过使用基于信用的流控方案来提高传输效率。该主题将在第 215 页的第 6 章"流控"中详细讨论。DLLP 用于传输流控信用信息。多种不同的 DLLP 用于初始化流控信用。另一类更新 DLLP 用于在接收端缓冲区空间被回收时管理运行时信用管理。有两种流控初始化 DLLP，称为 InitFC1 和 InitFC2，以及一种流控更新 DLLP，称为 UpdateFC。</td></tr>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">The packet format for all three variants is illustrated in Figure 9‑5 on page 315, while Table 9‑4 on page 315 describes the fields contained in it.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">所有三种变体的报文格式如第 315 页的图 9-5 所示，而第 315 页的表 9-4 描述了其中包含的字段。</td></tr>
  </tbody>
</table>


Figure 9‑5: Flow Control DLLP Format | 图9‑5：流控DLLP格式  

<img src="images/part03_940c6bec3506e8ca08d228126a03402fb96c706db13e7d2a8f81e391e4f0ccde.jpg" width="700" alt="">

Table 9‑4: Flow Control DLLP Fields | 表9‑4：流控DLLP字段

<table style="border:2px solid #000;border-collapse:collapse;width:100%" cellpadding="4" cellspacing="0" rules="all" frame="border"><tr><td style="border:2px solid #000;">Field Name</td><td style="border:2px solid #000;">Header Byte/Bit</td><td style="border:2px solid #000;">DLLP Function</td></tr><tr><td rowspan="3" style="border:2px solid #000;">DLLP Type</td><td style="border:2px solid #000;">Byte 0, [7:4]</td><td style="border:2px solid #000;">This code indicates the type of FC DLLP:0100b = InitFC1-P (Posted Requests)0101b = InitFC1-NP (Non-Posted Requests)0110b = InitFC1-Cpl (Completions)0101b = InitFC2-P (Posted Requests)1101b = InitFC2-NP (Non-Posted Requests)1110b = InitFC2-Cpl (Completions)1000b = UpdateFC-P (Posted Requests)1001b = UpdateFC-NP (Non-Posted Requests)1010b = UpdateFC-Cpl (Completions)</td></tr><tr><td style="border:2px solid #000;">Byte 0, [3]</td><td style="border:2px solid #000;">Must be 0b as part of flow control encoding.</td></tr><tr><td style="border:2px solid #000;">Byte 0, [2:0]</td><td style="border:2px solid #000;">VC ID. Indicates the Virtual Channel (VC 0-7) to be updated with these credits.</td></tr><tr><td style="border:2px solid #000;">HdrFC</td><td style="border:2px solid #000;">Byte 1, [5:0]Byte 2, [7:6]</td><td style="border:2px solid #000;">Contains the credit count for header storage for the specified Virtual Channel. Each credit represents space for 1 header + the optional TLP Digest (ECRC).</td></tr><tr><td style="border:2px solid #000;">DataFC</td><td style="border:2px solid #000;">Byte 2, [3:0]Byte 3, [7:0]</td><td style="border:2px solid #000;">Contains the credit count for data storage for the specified Virtual Channel. Each credit represents 16 bytes.</td></tr><tr><td style="border:2px solid #000;">16-bit CRC</td><td style="border:2px solid #000;">Byte 4, [7:0]Byte 5, [7:0]</td><td style="border:2px solid #000;">A 16-Bit CRC that protects the contents of this DLLP. Calculation is based on Bytes 0-3, regardless of whether all fields are used.</td></tr></table>

## 9.4.4 Vendor-Specific DLLP Format | 9.4.4 厂商特定 DLLP 格式

<table style="border:2px solid #000;border-collapse:collapse; width:100%;" cellpadding="4" cellspacing="0" rules="all" frame="border">
  <thead style="border:2px solid #000;">
    <tr>
      <th width="50%" style="border:2px solid #000; background:#f5f5f5;">EN</th>
      <th width="50%" style="border:2px solid #000; background-color:#e8e8e8;">中文</th>
    </tr>
  </thead>
  <tbody>
    <tr><td width="50%" style="border:2px solid #000; background:#fff;padding:4px 8px;">The last defined DLLP type is used for vendor specific purposes. Therefore only the DLLP Type field is defined by the spec (0011 0000b), leaving the remaining contents available for vendor-defined use.</td><td width="50%" style="border:2px solid #000; background-color:#e8e8e8;padding:4px 8px;">最后一种定义的DLLP类型用于厂商专用目的。因此，规范仅定义了DLLP类型字段（0011 0000b），其余内容留待厂商定义使用。</td></tr>
  </tbody>
</table>


Figure 9-6: Vendor-Specific DLLP Format | 图9-6：厂商特定DLLP格式

<table style="border:2px solid #000;border-collapse:collapse;width:100%" cellpadding="4" cellspacing="0" rules="all" frame="border"><tr><td rowspan="2" style="border:2px solid #000;"></td><td style="border:2px solid #000;">+0</td><td style="border:2px solid #000;">+1</td><td style="border:2px solid #000;">+2</td><td style="border:2px solid #000;">+3</td></tr><tr><td style="border:2px solid #000;">7|6|5|4|3|2|1|0</td><td style="border:2px solid #000;">7|6|5|4|3|2|1|0</td><td style="border:2px solid #000;">7|6|5|4|3|2|1|0</td><td style="border:2px solid #000;">7|6|5|4|3|2|1|0</td></tr><tr><td style="border:2px solid #000;">Byte 0</td><td style="border:2px solid #000;">0 0 1 1 0 0 0 0</td><td colspan="3" style="border:2px solid #000;">Vendor-Defined</td></tr><tr><td style="border:2px solid #000;">Byte 4</td><td colspan="2" style="border:2px solid #000;">16-bit CRC</td><td colspan="2" style="border:2px solid #000;"></td></tr></table>