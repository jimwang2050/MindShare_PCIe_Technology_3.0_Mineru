# Ch05_TLP_Elements

## Chapter 5: TLP Elements | 第5章：TLP元素

<table>
<tr>
<td width="50%">
Table 5-7: Completion Header Fields (Continued) | 表5-7：完成头字段（续）
</td>
<td width="50%" style="background-color:#e8e8e8">
表5-7：完成报文头字段（续）
</td>
</tr>
</table>

<table><tr><td>Field Name</td><td>Header Byte/Bit</td><td>Function</td></tr><tr><td>Compl. Status [2:0] (Completion Status Code)</td><td>Byte 6 Bit 7:5</td><td>These bits indicate status for this Completion.000b = Successful Completion (SC)001b = Unsupported Request (UR)010b = Config Req Retry Status (CRS)100b = Completer abort (CA)All other codes are reserved. See "Summary of Completion Status Codes" on page 200.</td></tr><tr><td>BCM (Byte Count Modified)</td><td>Byte 6 Bit 4</td><td>This is only used by PCI-X Completers and indicates that the Byte Count field reports only the first payload rather than the total payload remaining. See "Using The Byte Count Modified Bit" on page 201.</td></tr><tr><td>Byte Count [11:0]</td><td>Byte 6 Bit 3:0Byte 7 Bit 7:0</td><td>Byte count remaining to satisfy a read request, as derived from the original request Length field. See "Data Returned For Read Requests:" on page 201 for special cases caused by multiple completions.</td></tr><tr><td>Requester ID [15:0]</td><td>Byte 8 Bit 7:0Byte 9 Bit 7:0</td><td>Copied from the Request for use as the return address (target) for this Completion.Byte 8, 7:0 = Requester Bus #Byte 9, 7:3 = Requester Device #Byte 9, 2:0 = Requester Function #</td></tr><tr><td>Tag [7:0]</td><td>Byte 10 Bit 7:0</td><td>This must be the Tag value received with the Request. Requester associates this Completion with a pending Request based on the Tag.</td></tr><tr><td>Lower Address [6:0]</td><td>Byte 11 Bit 6:0</td><td>The lower 7 bits of address for the first data returned for a read request. Calculated from Request Length and Byte Enables, it assists buffer management by showing how many bytes can be transferred before reaching the next Read Completion Boundary. See "Calculating Lower Address Field" on page 200.</td></tr></table>

## Summary of Completion Status Codes. | 完成状态码概述。

<table>
<tr>
<td width="50%">
000b (SC) Successful Completion: the Request was serviced properly.
</td>
<td width="50%" style="background-color:#e8e8e8">
000b (SC) 成功完成：请求已被正确处理。
</td>
</tr>
<tr>
<td width="50%">
001b (UR) Unsupported Request: Request is not legal or was not recognized by the Completer. This is an error condition but how the Completer responds depends on the spec revision to which it was designed. Before the 1.1 spec, this were considered an uncorrectable error, but for 1.1 and later it's treated as an Advisory Non-Fatal Error. See the "Unsupported Request (UR) Status" on page 663 for details.
</td>
<td width="50%" style="background-color:#e8e8e8">
001b (UR) 不支持的请求：请求不合法，或完成者无法识别该请求。这是一个错误条件，但完成者如何响应取决于其所遵循的规范版本。在 1.1 规范之前，这被视为不可纠正错误，但对于 1.1 及更高版本，它被视为咨询性非致命错误。详见第 663 页的"不支持的请求 (UR) 状态"。
</td>
</tr>
<tr>
<td width="50%">
010b (CRS) Configuration Request Retry Status: Completer is temporarily unable to service a configuration request, and the request should be attempted again later.
</td>
<td width="50%" style="background-color:#e8e8e8">
010b (CRS) 配置请求重试状态：完成者暂时无法处理配置请求，请求应在稍后重新尝试。
</td>
</tr>
<tr>
<td width="50%">
100b (CA) Completer Abort: Completer should have been able to service the request but has failed for some reason. This is an uncorrectable error.
</td>
<td width="50%" style="background-color:#e8e8e8">
100b (CA) 完成者中止：完成者本应能够处理该请求，但因某种原因失败了。这是一个不可纠正错误。
</td>
</tr>
<tr>
<td width="50%">
Calculating The Lower Address Field. This field is set up by the Completer to reflect the byte-aligned address of the first enabled byte of data being returned in the Completion payload. Hardware calculates this by considering both the DW start address and the Byte Enable pattern in the First DW Byte Enable field provided in the original request.
</td>
<td width="50%" style="background-color:#e8e8e8">
低位地址字段的计算。此字段由完成者设置，用于反映完成报文中返回的、第一个被使能字节数据的字节对齐地址。硬件通过综合考虑原始请求中提供的 DW 起始地址和首个 DW 字节使能字段中的字节使能模式来计算此值。
</td>
</tr>
<tr>
<td width="50%">
For Memory Read Requests, the address is an offset from the DW start address:
</td>
<td width="50%" style="background-color:#e8e8e8">
对于存储器读请求，该地址是 DW 起始地址的偏移量：
</td>
</tr>
<tr>
<td width="50%">
If the First DW Byte Enable field is 1111b, all bytes are enabled in the first DW and the offset is 0. This field matches the DW-aligned start address.
</td>
<td width="50%" style="background-color:#e8e8e8">
如果首个 DW 字节使能字段为 1111b，则第一个 DW 中的所有字节均被使能，偏移量为 0。此字段与 DW 对齐的起始地址一致。
</td>
</tr>
<tr>
<td width="50%">
If the First DW Byte Enable field is 1110b, the upper three bytes are enabled in the first DW and the offset is 1. This field is the DW start address + 1.
</td>
<td width="50%" style="background-color:#e8e8e8">
如果首个 DW 字节使能字段为 1110b，则第一个 DW 中的高三位字节被使能，偏移量为 1。此字段为 DW 起始地址 + 1。
</td>
</tr>
<tr>
<td width="50%">
If the First DW Byte Enable field is 1100b, the upper two bytes are enabled in the first DW and the offset is 2. This field is the DW start address + 2.
</td>
<td width="50%" style="background-color:#e8e8e8">
如果首个 DW 字节使能字段为 1100b，则第一个 DW 中的高两位字节被使能，偏移量为 2。此字段为 DW 起始地址 + 2。
</td>
</tr>
<tr>
<td width="50%">
If the First DW Byte Enable field is 1000b, only the upper byte is enabled in the first DW and the offset is 3. This field is the DW start address + 3.
</td>
<td width="50%" style="background-color:#e8e8e8">
如果首个 DW 字节使能字段为 1000b，则第一个 DW 中仅高位字节被使能，偏移量为 3。此字段为 DW 起始地址 + 3。
</td>
</tr>
<tr>
<td width="50%">
Once calculated, the lower 7 bits are placed in the Lower Address field of the Completion header to facilitate the case in which the read completion is smaller than the entire payload and needs to stop at the first RCB. Breaking a transaction must be done on RCBs, and the number of bytes transferred to reach the first one is based on start address.
</td>
<td width="50%" style="background-color:#e8e8e8">
计算完成后，低 7 位被放入完成报文头中的低位地址字段，以便在读完成小于整个有效载荷并需要在第一个 RCB 处停止时使用。事务拆分必须在 RCB 边界进行，到达第一个 RCB 所传输的字节数取决于起始地址。
</td>
</tr>
<tr>
<td width="50%">
For AtomicOp Completions, the Lower Address field is reserved. For all other Completion types, it's set to zero.
</td>
<td width="50%" style="background-color:#e8e8e8">
对于 AtomicOp 完成报文，低位地址字段为保留字段。对于所有其他完成类型，该字段设为零。
</td>
</tr>
<tr>
<td width="50%">
Using The Byte Count Modified Bit. This bit is only set by PCI-X Completers, but they could exist in a PCIe topology if a bridge from PCIe to PCI-X is used. Rules for its assertion include:
</td>
<td width="50%" style="background-color:#e8e8e8">
字节计数修改位 (Byte Count Modified Bit) 的使用。此位仅由 PCI-X 完成者设置，但如果使用了从 PCIe 到 PCI-X 的桥接器，则它们可能存在于 PCIe 拓扑中。其置位规则包括：
</td>
</tr>
<tr>
<td width="50%">
1. It's only set by a PCI-X Completer if a read request is going to be broken into multiple completions.
</td>
<td width="50%" style="background-color:#e8e8e8">
1. 仅当读请求将被拆分为多个完成报文时，PCI-X 完成者才会置位该位。
</td>
</tr>
<tr>
<td width="50%">
2. It's only set for the first Completion of the series, and only then to indicate that the first Completion contains a Byte Count field that reflects the first Completion payload rather than the total remaining (as it normally would). The Requester understands that, even though the Byte Count appears to show that this is the last Completion for this request, this Completion will instead be followed by others to satisfy the original request as required.
</td>
<td width="50%" style="background-color:#e8e8e8">
2. 它仅在系列中的第一个完成报文中置位，此时仅用于指示第一个完成报文包含的字节计数字段反映的是第一个完成报文的有效载荷，而非（通常情况下的）剩余总量。请求者明白，即使字节计数看起来显示这是该请求的最后一个完成报文，实际上该完成报文后面还会跟随其他完成报文，以按要求满足原始请求。
</td>
</tr>
<tr>
<td width="50%">
3. For subsequent Completions in the series, the BCM bit must be deasserted and the Byte Count field will reflect the total remaining count as it normally would.
</td>
<td width="50%" style="background-color:#e8e8e8">
3. 对于该系列中后续的完成报文，BCM 位必须取消置位，字节计数字段将按正常方式反映剩余总量。
</td>
</tr>
<tr>
<td width="50%">
4. Devices receiving Completions with the BCM bit set must interpret this case properly.
</td>
<td width="50%" style="background-color:#e8e8e8">
4. 接收到 BCM 位置位的完成报文的设备必须正确解释这种情况。
</td>
</tr>
<tr>
<td width="50%">
5. The Lower Address field is set by the Completer during completions with data to reflect the address of the first enabled byte of data being returned
</td>
<td width="50%" style="background-color:#e8e8e8">
5. 在带数据的完成报文中，低位地址字段由完成者设置，用于反映所返回数据的第一个被使能字节的地址。
</td>
</tr>
</table>

## Data Returned For Read Requests:

<table>
<tr>
<td width="50%">
A read request may require multiple completions to be fulfilled, but total data transfer must eventually equal the size of original request, or a Completion Timeout error will probably result.
</td>
<td width="50%" style="background-color:#e8e8e8">
一个读请求可能需要多个完成报文才能完成，但总的数据传输量最终必须等于原始请求的大小，否则将可能导致完成超时错误。
</td>
</tr>
<tr>
<td width="50%">
A given Completion can only service one Request.
</td>
<td width="50%" style="background-color:#e8e8e8">
一个给定的完成报文只能服务于一个请求。
</td>
</tr>
<tr>
<td width="50%">
IO and Configuration reads are always 1 DW, and will always be satisfied with a single Completion
</td>
<td width="50%" style="background-color:#e8e8e8">
IO和配置读总是一个DW，并且总是通过一个完成报文来满足。
</td>
</tr>
<tr>
<td width="50%">
A Completion with a Status Code other than SC (successful) terminates a transaction.
</td>
<td width="50%" style="background-color:#e8e8e8">
带有非SC(成功)状态码的完成报文将终止一个事务。
</td>
</tr>
<tr>
<td width="50%">
The Read Completion Boundary (RCB) must be observed when handling a read request with multiple completions. The RCB is 64 bytes or 128 bytes for the Root Complex, since it is allowed to modify the size of packets flowing between its ports, and the value used is visible in a configuration register.
</td>
<td width="50%" style="background-color:#e8e8e8">
在处理带有多个完成报文的读请求时，必须遵守读完成边界(RCB)。对于根复合体，RCB可以是64字节或128字节，因为它允许修改在其端口之间流动的数据包大小，并且所使用的值在配置寄存器中可见。
</td>
</tr>
<tr>
<td width="50%">
Bridges and endpoints may implement a bit for selecting the RCB size (64 or 128 bytes) under software control.
</td>
<td width="50%" style="background-color:#e8e8e8">
桥和端点可以通过软件控制实现一个位来选择RCB大小(64或128字节)。
</td>
</tr>
<tr>
<td width="50%">
Completions that are entirely within an aligned RCB boundary must complete in one transfer, since the transfer won't reach the RCB, which is the only place it can legally stop early.
</td>
<td width="50%" style="background-color:#e8e8e8">
完全位于对齐的RCB边界内的完成报文必须在一个传输中完成，因为该传输不会到达RCB，而RCB是唯一可以合法提前停止的地方。
</td>
</tr>
<tr>
<td width="50%">
Multiple Completions for a single read request must return data in increasing address order.
</td>
<td width="50%" style="background-color:#e8e8e8">
针对单个读请求的多个完成报文必须以地址递增的顺序返回数据。
</td>
</tr>
</table>

## Receiver Completion Handling Rules: | 接收器完成报文处理规则：

<table>
<tr>
<td width="50%">
1. A received Completion that doesn't match a pending request is an Unexpected Completion and treated as an error.
</td>
<td width="50%" style="background-color:#e8e8e8">
1. 接收到的完成报文若与任何待处理请求不匹配，则视为意外完成报文（Unexpected Completion），并按错误处理。
</td>
</tr>
<tr>
<td width="50%">
2. Completions with a completion status other than SC or CRS will be handled as errors and buffer space associated with them will be released.
</td>
<td width="50%" style="background-color:#e8e8e8">
2. 完成状态不是SC（成功完成）或CRS（配置重试状态）的完成报文将按错误处理，与之关联的缓冲空间将被释放。
</td>
</tr>
<tr>
<td width="50%">
3. When the Root Complex receives a CRS status during a configuration cycle, the request is terminated. What happens next is implementation specific, but if the Root supports it, the action is defined by the setting of its CRS Software Visibility bit in the Root Control register.
</td>
<td width="50%" style="background-color:#e8e8e8">
3. 当根复合体在配置周期中收到CRS状态时，该请求即告终止。后续行为取决于具体实现，但如果根复合体支持，则其行为由根控制寄存器（Root Control register）中的CRS软件可见位（CRS Software Visibility bit）的设置决定。
</td>
</tr>
<tr>
<td width="50%">
— If CRS Software Visibility is not enabled, the Root will reissue the config request for an implementation‑specific number of times before giving up and concluding the target has a problem.
</td>
<td width="50%" style="background-color:#e8e8e8">
— 若CRS软件可见位未使能，根复合体将重新发起配置请求，重试次数取决于具体实现，之后放弃并认定目标设备存在问题。
</td>
</tr>
<tr>
<td width="50%">
If CRS Software Visibility is enabled, software designed to support it will always read both bytes of the Vendor ID field first. If the hardware then receives a CRS for that Request, it returns the value 0001h for the Vendor ID. This value, reserved for this use by the PCI‑SIG, doesn't correspond to any valid Vendor ID and informs software about this event. This allows software to go on to some other task while waiting for the target to become ready (which could take as long as 1 second after reset) rather than being stalled. Any other config read or write will simply be automatically retried by the Root as a new Request for the design‑specific number of iterations.
</td>
<td width="50%" style="background-color:#e8e8e8">
若CRS软件可见位已使能，支持该功能的软件将始终首先读取Vendor ID字段的两个字节。若硬件随后对该请求收到CRS，则返回Vendor ID值0001h。该值由PCI-SIG为此用途保留，不对应任何有效Vendor ID，用于通知软件此事件。这样软件可以在等待目标设备就绪（复位后可能长达1秒）的同时转去处理其他任务，而不是停滞等待。任何其他配置读或写操作将被根复合体简单地作为新请求自动重试，重试次数取决于设计实现。
</td>
</tr>
<tr>
<td width="50%">
4. A CRS status in response to a request other than configuration is illegal and may be reported as a Malformed TLP.
</td>
<td width="50%" style="background-color:#e8e8e8">
4. 对非配置请求返回CRS状态是非法的，可报告为畸形TLP（Malformed TLP）。
</td>
</tr>
<tr>
<td width="50%">
5. Completions with status = reserved code are treated as if the code was UR.
</td>
<td width="50%" style="background-color:#e8e8e8">
5. 完成状态为保留编码的完成报文按UR（不支持的请求）编码处理。
</td>
</tr>
<tr>
<td width="50%">
6. If a Read Completion or an AtomicOp Completion is received with a status other than SC, no data is included with the completion and the Requester must consider this Request terminated. How the Requester handles this case is implementation‑specific.
</td>
<td width="50%" style="background-color:#e8e8e8">
6. 若接收到的读完成（Read Completion）或AtomicOp完成的状态不是SC，则完成报文中不含数据，请求方必须将该请求视为已终止。请求方如何处理此情况取决于具体实现。
</td>
</tr>
<tr>
<td width="50%">
7. In the event multiple completions are being returned for a read request, a completion status other than SC ends the transaction. Device handling of data received prior to the error is implementation‑specific.
</td>
<td width="50%" style="background-color:#e8e8e8">
7. 若一个读请求返回多个完成报文，则非SC的完成状态将终止该事务。设备如何处理出错前已接收的数据取决于具体实现。
</td>
</tr>
<tr>
<td width="50%">
8. For compatibility with PCI, a Root Complex may be required to synthesize a read value of all "1's" when a configuration cycle ends with a completion indicating an Unsupported Request. This is analogous to a PCI Master Abort that happens when enumeration software attempts to read from devices that are not present.
</td>
<td width="50%" style="background-color:#e8e8e8">
8. 为与PCI兼容，当配置周期以指示不支持的请求（Unsupported Request）的完成报文结束时，根复合体可能需要合成全"1"的读值。这类似于当枚举软件尝试从不存在设备读取时发生的PCI主设备中止（Master Abort）。
</td>
</tr>
</table>

## Message Requests

<table>
<tr>
<td width="50%">
Message Requests replace many of the interrupt, error, and power management sideband signals used on PCI and PCI-X. All Message Requests use the 4DW header format, but not all of the fields are used in every Message type. Fields in bytes 8 through 15 are not defined for some Messages and are reserved for those cases. Messages are treated much like posted Memory Write transactions but their routing can be based on address, ID, and in some cases the routing can be implicit. The routing subfield (Byte 0, bits 2:0) in the packet header indicates which routing method is used and which additional header registers are defined. The general Message Request header format is shown in Figure 5-11 on page 203.
</td>
<td width="50%" style="background-color:#e8e8e8">
消息请求取代了PCI和PCI-X上使用的许多中断、错误和电源管理边带信号。所有消息请求使用4DW头部格式，但并非所有字段在每个消息类型中都使用。对于某些消息，字节8至15的字段未被定义，在这些情况下为保留字段。消息的处理方式与发布的内存写事务非常相似，但其路由可以基于地址、ID，在某些情况下路由可以是隐式的。数据包头部的路由子字段（字节0，位2:0）指示使用哪种路由方法以及定义了哪些额外的头部寄存器。通用消息请求头部格式如图5-11所示（第203页）。
</td>
</tr>
</table>

Figure 5-11: 4DW Message Request Header Format | 图5-11：4DW消息请求头格式

<table><tr><td colspan="19">4DW Header for Messages</td><td></td></tr><tr><td rowspan="2"></td><td colspan="3">+0</td><td colspan="6">+1</td><td colspan="5">+2</td><td colspan="4">+3</td><td></td></tr><tr><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>0</td><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>0</td><td>7</td><td>6</td><td>5</td></tr><tr><td>Byte 0</td><td colspan="2">Fmt0 x 1</td><td>Type1</td><td>0</td><td>rr</td><td>r</td><td>R</td><td>TC</td><td>R</td><td>Attr</td><td>R</td><td>TH0</td><td>TD</td><td>EP</td><td>Attr0</td><td>0</td><td>0</td><td>Length</td><td></td></tr><tr><td>Byte 4</td><td colspan="12">Requester ID</td><td colspan="4">Tag</td><td colspan="2">MessageCode</td><td></td></tr><tr><td>Byte 8</td><td colspan="18">Bytes 8-11 Vary with Message Code Field</td><td></td></tr><tr><td>Byte 12</td><td colspan="18">Bytes 12-15 Vary with Message Code Field</td><td></td></tr></table>

<table>
<tr>
<td width="50%">
Message Request Header Fields.
</td>
<td width="50%" style="background-color:#e8e8e8">
消息请求头部字段。
</td>
</tr>
</table>

Table 5-8: Message Request Header Fields | 表5-8：消息请求头字段

<table><tr><td>Field Name</td><td>Header Byte/Bit</td><td>Function</td></tr><tr><td>Fmt [2:0](Format)</td><td>Byte 0 Bit 7:5</td><td>Packet Format. Always a 4DW header001b = Message Request without data011b = Message Request with data</td></tr><tr><td>Type [4:0]</td><td>Byte 0 Bit 4:0</td><td>TLP packet type field. Set to:Bit 4:3:10b = MsgBit 2:0 (Message Routing Subfield)000b = Implicitly Routed to RC (Root Complex)001b = Routed by address010b = Routed by ID011b = Implicitly Broadcast from RC100b = Local; terminate at receiver101b = Gather &amp; route to RC0thers = Reserved, treated as Local</td></tr><tr><td>TC [2:0](Traffic Class)</td><td>Byte 1 Bit 6:4</td><td>TC is always zero for most Message Requests, ensuring that they don't interfere with high-priority packets.</td></tr><tr><td>Attr [2](Attributes)</td><td>Byte 1 Bit 2</td><td>Indicates whether ID-based Ordering is to be used for this TLP. To learn more, see "ID Based Ordering (IDO)" on page 301.</td></tr><tr><td>TH(TLP Processing Hints)</td><td>Byte 1 Bit 0</td><td>Reserved, except as noted.</td></tr><tr><td>TD</td><td>Byte 2 Bit 7</td><td>If = 1, indicates the presence of a digest field (1 DW) at the end of the TLP (preceding LCRC and END)</td></tr><tr><td>EP</td><td>Byte 2 Bit 6</td><td>If = 1, indicates the data payload (if present) is poisoned.</td></tr></table>

## Chapter 5: TLP Elements | 第5章：TLP元素


Table 5‐8: Message Request Header Fields (Continued) | 表5‐8：消息请求头字段（续）

<table><tr><td>Field Name</td><td>Header Byte/Bit</td><td>Function</td></tr><tr><td>Attr [1:0](Attributes)</td><td>Byte 2 Bit 5:4</td><td>Except as noted, these are always reserved in Message Requests.</td></tr><tr><td>AT [1:0](Address Type)</td><td>Byte 2 Bit 3:2</td><td>Address Type is reserved for Messages and must be zero, but Receivers are not required or even encouraged to check this.</td></tr><tr><td>Length [9:0]</td><td>Byte 2 Bit 1:0Byte 3 Bit 7:0</td><td>Indicates data payload size in DW. For Message Requests, this field is always 0 (no data) or 1 (one DW of data)</td></tr><tr><td>Requester ID [15:0]</td><td>Byte 4 Bit 7:0Byte 5 Bit 7:0</td><td>Identifies the Requester sending the message.Byte 4, 7:0 = Requester Bus #Byte 5, 7:3 = Requester Device #Byte 5, 2:0 = Requester Function #</td></tr><tr><td>Tag [7:0]</td><td>Byte 6 Bit 7:0</td><td>Since all Message Requests are posted and don't receive Completions, no tag is assigned to them. These bits should be zero.</td></tr><tr><td>Message Code [7:0]</td><td>Byte 7 Bit 7:0</td><td>This field contains the code indicating the type of message being sent.0000 0000b = Unlock Message0001 0000b = Lat. Tolerance Reporting0001 0010b = Optimized Buffer Flush/Fill0001 xxxxb = Power Mgt. Message0010 0xxxb = INTx Message0011 00xxb = Error Message0100 xxxxb = Ignored Messages0101 0000b = Set Slot Power Message0111 111xb = Vendor-Defined Messages</td></tr><tr><td>Address [63:32]</td><td>Byte 8 Bit 7:0Byte 9 Bit 7:0Byte 10 Bit 7:0Byte 11 Bit 7:0</td><td>If address routing was selected for the message (see Type 4:0 field above), then this field contains the upper 32 bits of the 64 bit starting address.Otherwise, this field is not used.</td></tr><tr><td>Address [31:2]</td><td>Byte 12 Bit 7:0Byte 13 Bit 7:0Byte 14 Bit 7:0Byte 15 Bit 7:2</td><td>If address routing is selected (see Type field above), then this field contains the lower part of the 64-bit starting address.If ID routing is selected, Bytes 8 and 9 form the target ID.Otherwise, this field is not used.</td></tr></table>

<table>
<tr>
<td width="50%">
Message Notes: The following tables specify the message coding used for each of the nine message groups, and is based on the message code field listed in Table 5‐8 on page 204. The defined message groups include:
</td>
<td width="50%" style="background-color:#e8e8e8">
消息说明：以下各表给出了九个消息组各自使用的消息编码，其依据为第204页表5-8中所列的消息代码字段。已定义的消息组包括：
</td>
</tr>
<tr>
<td width="50%">
1. INTx Interrupt Signaling
</td>
<td width="50%" style="background-color:#e8e8e8">
1. INTx中断信令
</td>
</tr>
<tr>
<td width="50%">
2. Power Management
</td>
<td width="50%" style="background-color:#e8e8e8">
2. 电源管理
</td>
</tr>
<tr>
<td width="50%">
3. Error Signaling
</td>
<td width="50%" style="background-color:#e8e8e8">
3. 错误信令
</td>
</tr>
<tr>
<td width="50%">
4. Locked Transaction Support
</td>
<td width="50%" style="background-color:#e8e8e8">
4. 锁定事务支持
</td>
</tr>
<tr>
<td width="50%">
5. Slot Power Limit Support
</td>
<td width="50%" style="background-color:#e8e8e8">
5. 插槽功率限制支持
</td>
</tr>
<tr>
<td width="50%">
6. Vendor-Defined Messages
</td>
<td width="50%" style="background-color:#e8e8e8">
6. 供应商自定义消息
</td>
</tr>
<tr>
<td width="50%">
7. Ignored Messages (related to Hot-Plug support in spec revision 1.1)
</td>
<td width="50%" style="background-color:#e8e8e8">
7. 忽略的消息（与规范修订版1.1中的热插拔支持相关）
</td>
</tr>
<tr>
<td width="50%">
8. Latency Tolerance Reporting (LTR)
</td>
<td width="50%" style="background-color:#e8e8e8">
8. 延迟容忍度报告 (LTR)
</td>
</tr>
<tr>
<td width="50%">
9. Optimized Buffer Flush and Fill (OBFF)
</td>
<td width="50%" style="background-color:#e8e8e8">
9. 优化的缓冲区刷新与填充 (OBFF)
</td>
</tr>
<tr>
<td width="50%">
INTx Interrupt Messages. Many devices are capable of using the PCI 2.3 Message Signaled Interrupt (MSI) method of delivering interrupts, but older devices may not support it. For these cases, PCIe defines a "virtual wire" alternative in which devices simulate the assertion and deassertion of the PCI interrupt pins (INTA-INTD) by sending Messages. The interrupting device sends the first Message to inform the upstream device that an interrupt has been asserted. Once the interrupt has been serviced, the interrupting device sends a second Message to communicate that the signal has been released. For more on this protocol, refer to the section called "Virtual INTx Signaling" on page 805 for details.
</td>
<td width="50%" style="background-color:#e8e8e8">
INTx中断消息。许多设备能够使用PCI 2.3的消息信令中断 (MSI) 方法来传递中断，但较旧的设备可能不支持此方法。针对这些情况，PCIe定义了一种"虚拟线路"替代方案，设备通过发送消息来模拟PCI中断引脚 (INTA-INTD) 的置位和撤销。中断设备发送第一条消息以通知上游设备中断已被置位。中断被服务后，中断设备发送第二条消息以通告该信号已被释放。关于此协议的更多细节，请参阅第805页的"虚拟INTx信令"一节。
</td>
</tr>
</table>

Table 5‐9: INTx Interrupt Signaling Message Coding | 表5‐9：INTx中断信令消息编码

<table><tr><td>INTx Message</td><td>Message Code 7:0</td><td>Routing 2:0</td></tr><tr><td>Assert_INTA</td><td>0010 0000b</td><td rowspan="8">100b(Local - Terminate at Rx)</td></tr><tr><td>Assert_INTB</td><td>0010 0001b</td></tr><tr><td>Assert_INTC</td><td>0010 0010b</td></tr><tr><td>Assert_INTD</td><td>0010 0011b</td></tr><tr><td>Deassert_INTA</td><td>0010 0100b</td></tr><tr><td>Deassert_INTB</td><td>0010 0101b</td></tr><tr><td>Deassert_INTC</td><td>0010 0110b</td></tr><tr><td>Deassert_INTD</td><td>0010 0111b</td></tr></table>

<table>
<tr>
<td width="50%">
Rules regarding the use of INTx Messages:
</td>
<td width="50%" style="background-color:#e8e8e8">
关于INTx消息使用的规则：
</td>
</tr>
<tr>
<td width="50%">
1. They have no data payload and so the Length field is reserved.
</td>
<td width="50%" style="background-color:#e8e8e8">
1. 它们没有数据载荷，因此Length字段为保留字段。
</td>
</tr>
<tr>
<td width="50%">
2. They're only issued by Upstream Ports. Checking this rule for received packets is optional but, if checked, violations will be handled as Malformed TLPs.
</td>
<td width="50%" style="background-color:#e8e8e8">
2. 它们只能由上游端口发出。对接收到的包检查此规则是可选的，但如果检查，违规将按畸形TLP处理。
</td>
</tr>
<tr>
<td width="50%">
3. They're required to use the default traffic class TC0. Receivers must check for this and violations will be handled as Malformed TLPs.
</td>
<td width="50%" style="background-color:#e8e8e8">
3. 它们必须使用默认流量类TC0。接收方必须对此进行检查，违规将按畸形TLP处理。
</td>
</tr>
<tr>
<td width="50%">
4. Components at both ends of the Link must track the current state of the four virtual interrupts. If the logical state of one interrupt changes at the Upstream Port, it must send the appropriate INTx message.
</td>
<td width="50%" style="background-color:#e8e8e8">
4. 链路两端的组件必须跟踪四个虚拟中断的当前状态。如果某个中断在上游端口处的逻辑状态发生变化，则必须发送相应的INTx消息。
</td>
</tr>
<tr>
<td width="50%">
5. INTx signaling is disabled when the Interrupt Disable bit of the Command Register is set = 1 (as would be the case for physical interrupt lines).
</td>
<td width="50%" style="background-color:#e8e8e8">
5. 当命令寄存器的中断禁用位被设置为1时，INTx信令被禁用（这与物理中断线的情况相同）。
</td>
</tr>
<tr>
<td width="50%">
6. If any virtual INTx signals are active when the Interrupt Disable bit is set in the device, the Upstream Port must send corresponding Deassert_INTx messages.
</td>
<td width="50%" style="background-color:#e8e8e8">
6. 如果设备中设置了中断禁用位时仍有任何虚拟INTx信号处于有效状态，则上游端口必须发送相应的Deassert_INTx消息。
</td>
</tr>
<tr>
<td width="50%">
7. Switches must track the state of the four INTx signals independently for each Downstream Port and combine the states for the Upstream Port.
</td>
<td width="50%" style="background-color:#e8e8e8">
7. 交换机必须针对每个下游端口独立跟踪四个INTx信号的状态，并为上游端口组合这些状态。
</td>
</tr>
<tr>
<td width="50%">
8. The Root Complex must track the state of the four INTx lines independently and convert them into system interrupts in an implementation-specific way.
</td>
<td width="50%" style="background-color:#e8e8e8">
8. 根复合体必须独立跟踪四个INTx线路的状态，并以特定于实现的方式将其转换为系统中断。
</td>
</tr>
</table>

## PCI Express Technology | PCI Express 技术

<table>
<tr>
<td width="50%">
9. They use the routing type "Local-Terminate at Receiver" to allow a Switch to remap the designated interrupt pin when necessary (see "Mapping and Collapsing INTx Messages" on page 808). Consequently, the Requester ID in an INTx message may be assigned by the last transmitter.
</td>
<td width="50%" style="background-color:#e8e8e8">
9. 它们使用"Local-Terminate at Receiver"路由类型，以允许交换机在必要时重新映射指定的中断引脚（参见第808页"INTx 消息的映射与折叠"）。因此，INTx 消息中的请求者 ID 可能由最后一个发送器分配。
</td>
</tr>
<tr>
<td width="50%">
Power Management Messages. PCI Express is compatible with PCI power management, and adds hardware-based Link power management as well. Messages are used to convey some of this information, but to learn how the overall PCIe power management protocol works, refer to Chapter 16, entitled "Power Management," on page 703. Table 5-10 on page 208 summarizes the four power management message types.
</td>
<td width="50%" style="background-color:#e8e8e8">
电源管理消息。PCI Express 兼容 PCI 电源管理，并增加了基于硬件的链路电源管理。消息用于传递部分此类信息，但若要了解 PCIe 电源管理协议的整体工作原理，请参阅第703页第16章"电源管理"。第208页的表5-10总结了四种电源管理消息类型。
</td>
</tr>
</table>

Table 5-10: Power Management Message Coding | 表5-10：电源管理消息编码

<table><tr><td>Power Management Message</td><td>Message Code 7:0</td><td>Routing 2:0</td></tr><tr><td>PM_Active_State_Nak</td><td>0001 0100b</td><td>100b</td></tr><tr><td>PM_PME</td><td>0001 1000b</td><td>000b</td></tr><tr><td>PM_Turn_Off</td><td>0001 1001b</td><td>011b</td></tr><tr><td>PME_TO_Ack</td><td>0001 1011b</td><td>101b</td></tr></table>

<table>
<tr>
<td width="50%">
Power Management Message Rules:
</td>
<td width="50%" style="background-color:#e8e8e8">
电源管理消息规则：
</td>
</tr>
<tr>
<td width="50%">
1. Power Management Messages don't have a data payload, so the Length field is reserved.
</td>
<td width="50%" style="background-color:#e8e8e8">
1. 电源管理消息没有数据载荷，因此长度字段保留。
</td>
</tr>
<tr>
<td width="50%">
2. They're required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs.
</td>
<td width="50%" style="background-color:#e8e8e8">
2. 它们必须使用默认流量类 TC0。接收器必须检查此项，并将违规作为畸形 TLP 处理。
</td>
</tr>
<tr>
<td width="50%">
3. PM_Active_State_Nak is sent from a Downstream Port after it observes a request from the Link neighbor to change the Link power state to L1 but it has chosen not to do so (Local - Terminate at Receiver routing).
</td>
<td width="50%" style="background-color:#e8e8e8">
3. PM_Active_State_Nak 由下游端口发送，当它观察到链路邻居请求将链路电源状态更改为 L1 但选择不这样做时（Local - Terminate at Receiver 路由）。
</td>
</tr>
<tr>
<td width="50%">
4. PM_PME is sent upstream by the component requesting a Power Management Event (Implicitly Routed to the Root Complex).
</td>
<td width="50%" style="background-color:#e8e8e8">
4. PM_PME 由请求电源管理事件的组件向上游发送（隐式路由到根复合体）。
</td>
</tr>
<tr>
<td width="50%">
5. PM_Turn_Off is sent downstream to all endpoints (Implicitly Broadcast from the Root Complex routing).
</td>
<td width="50%" style="background-color:#e8e8e8">
5. PM_Turn_Off 向下游发送到所有端点（从根复合体隐式广播路由）。
</td>
</tr>
<tr>
<td width="50%">
6. PME_TO_Ack is sent upstream by endpoints. For switches with multiple Downstream Ports, this message won't be forwarded upstream until all Downstream Ports have received it (Gather and Route to the Root Complex routing).
</td>
<td width="50%" style="background-color:#e8e8e8">
6. PME_TO_Ack 由端点向上游发送。对于具有多个下游端口的交换机，此消息在所有下游端口都收到之前不会向上游转发（汇聚并路由到根复合体路由）。
</td>
</tr>
<tr>
<td width="50%">
Error Messages. Error Messages are sent upstream (Implicitly Routed to the Root Complex) by enabled components that detect errors. To assist software in knowing how to service the error, the Error Message identifies the requesting agent in the Requester ID field of the message header. Table 5-11 on page 209 describes the three error message types.
</td>
<td width="50%" style="background-color:#e8e8e8">
错误消息。错误消息由检测到错误的已启用组件向上游发送（隐式路由到根复合体）。为帮助软件了解如何处理错误，错误消息在消息头的请求者 ID 字段中标识请求代理。第209页的表5-11描述了三种错误消息类型。
</td>
</tr>
</table>

Table 5-11: Error Message Coding | 表5-11：错误消息编码

<table><tr><td>Error Message</td><td>Message Code 7:0</td><td>Routing 2:0</td></tr><tr><td>ERR_COR (Correctable)</td><td>0011 0000b</td><td rowspan="3">000b</td></tr><tr><td>ERR_NONFATAL (Uncorrectable, Non-fatal)</td><td>0011 0001b</td></tr><tr><td>ERR_FATAL (Uncorrectable, Fatal)</td><td>0011 0011b</td></tr></table>

<table>
<tr>
<td width="50%">
Error Signaling Message Rules:
</td>
<td width="50%" style="background-color:#e8e8e8">
错误信令消息规则：
</td>
</tr>
<tr>
<td width="50%">
1. They're required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs.
</td>
<td width="50%" style="background-color:#e8e8e8">
1. 它们必须使用默认流量类 TC0。接收器必须检查此项，并将违规作为畸形 TLP 处理。
</td>
</tr>
<tr>
<td width="50%">
2. They don't have a data payload, so the Length field is reserved.
</td>
<td width="50%" style="background-color:#e8e8e8">
2. 它们没有数据载荷，因此长度字段保留。
</td>
</tr>
<tr>
<td width="50%">
3. The Root Complex converts Error Messages into system-specific events.
</td>
<td width="50%" style="background-color:#e8e8e8">
3. 根复合体将错误消息转换为系统特定事件。
</td>
</tr>
<tr>
<td width="50%">
Locked Transaction Support. The Unlock Message is used as part of the Locked transaction protocol defined for PCI and still available to Legacy Devices. The protocol begins with a Memory Read Locked Request. When that Request is seen by Ports along the path to the target device, they implement an atomic read-modify-write protocol by locking out other Requesters from using VC0 until the Unlock Message is received. This Message is sent to the target to release all the Ports in the path to it and finish the Locked Transaction sequence. Table 5-12 on page 209 summarizes the coding for this message.
</td>
<td width="50%" style="background-color:#e8e8e8">
锁定事务支持。Unlock 消息用作 PCI 定义的锁定事务协议的一部分，传统设备仍可使用该协议。该协议以存储器读锁定请求开始。当通往目标设备路径上的端口看到该请求时，它们通过锁定其他请求者使其无法使用 VC0 来实现原子读-修改-写协议，直到收到 Unlock 消息。此消息发送到目标以释放通往它的路径中的所有端口，并完成锁定事务序列。第209页的表5-12总结了此消息的编码。
</td>
</tr>
</table>

Table 5-12: Unlock Message Coding | 表5-12：解锁消息编码

<table><tr><td>Unlock Message</td><td>Message Code 7:0</td><td>Routing 2:0</td></tr><tr><td>Unlock</td><td>0000 0000b</td><td>011b</td></tr></table>

<table>
<tr>
<td width="50%">
PCI Express Technology
</td>
<td width="50%" style="background-color:#e8e8e8">
PCI Express 技术
</td>
</tr>
</table>

## Unlock Message Rules

<table>
<tr>
<td width="50%">
1. They're required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs.
</td>
<td width="50%" style="background-color:#e8e8e8">
1. 它们必须使用默认流量类别TC0。接收者必须检查此项，并将违规视为畸形TLP处理。
</td>
</tr>
<tr>
<td width="50%">
2. They don't have a data payload, and the Length field is reserved.
</td>
<td width="50%" style="background-color:#e8e8e8">
2. 它们没有数据载荷，Length字段为保留。
</td>
</tr>
<tr>
<td width="50%">
Set Slot Power Limit Message. This is sent from a Downstream Port to the device plugged into the slot. This power limit is stored in the endpoint in its Device Capabilities Register. Table 5-13 summarizes the message coding.
</td>
<td width="50%" style="background-color:#e8e8e8">
Set Slot Power Limit消息。该消息从下游端口发送到插入槽位的设备。该功率限制存储在端点设备的Device Capabilities寄存器中。表5-13总结了消息编码。
</td>
</tr>
</table>

Table 5-13: Slot Power Limit Message Coding | 表5-13：插槽功耗限制消息编码

<table><tr><td>Slot Power Limit Message</td><td>Message Code 7:0</td><td>Routing 2:0</td></tr><tr><td>Set_Slot_Power_Limit</td><td>0101 0000b</td><td>100b</td></tr></table>

<table>
<tr>
<td width="50%">
**Set\_Slot\_Power\_Limit Message Rules:**
</td>
<td width="50%" style="background-color:#e8e8e8">
**Set\_Slot\_Power\_Limit 消息规则：**
</td>
</tr>
<tr>
<td width="50%">
1. They're required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs.
</td>
<td width="50%" style="background-color:#e8e8e8">
1. 此类消息必须使用默认流量类TC0。接收方必须对此进行检查，并将违规情况作为畸形TLP处理。
</td>
</tr>
<tr>
<td width="50%">
2. The data payload is 1 DW and so the Length field is set to one. Only the lower 10 bits of the 32-bit data payload are used for slot power scaling; the upper payload bits must be set to zero.
</td>
<td width="50%" style="background-color:#e8e8e8">
2. 数据负载为1个DW，因此长度字段设置为1。32位数据负载中仅低10位用于插槽功率调节；高位负载位必须设置为零。
</td>
</tr>
<tr>
<td width="50%">
3. This message is sent automatically anytime the Data Link Layer transitions to DL_Up status or if a configuration write to the Slot Capabilities Register occurs while the Data Link Layer is already reporting DL_Up status.
</td>
<td width="50%" style="background-color:#e8e8e8">
3. 每当数据链路层转换到DL_Up状态，或者在数据链路层已报告DL_Up状态时对插槽能力寄存器进行配置写入时，此消息都会自动发送。
</td>
</tr>
<tr>
<td width="50%">
4. If the card in the slot already consumes less power than the power limit specified, it's allowed to ignore the Message.
</td>
<td width="50%" style="background-color:#e8e8e8">
4. 如果插槽中的卡已消耗的功率低于指定的功率限制，则允许忽略此消息。
</td>
</tr>
<tr>
<td width="50%">
**Vendor-Defined Message 0 and 1.** These are intended to allow expansion of the PCIe messaging capabilities either by the spec or by vendor-specific extensions. The header for them is shown in Figure 5-12 on page 211, and the codes are given in Figure 5-14 on page 211.
</td>
<td width="50%" style="background-color:#e8e8e8">
**厂商定义消息0和1。** 这两种消息旨在允许通过规范或厂商特定扩展来扩展PCIe消息传递能力。其头部格式如图5-12（第211页）所示，编码如图5-14（第211页）所示。
</td>
</tr>
</table>

Figure 5-12: Vendor-Defined Message Header | 图5-12：厂商定义消息头

<table><tr><td rowspan="2"></td><td colspan="2">+0</td><td colspan="5">+1</td><td colspan="5">+2</td><td colspan="2">+3</td></tr><tr><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>0</td><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td></tr><tr><td>Byte 0</td><td>Fmt0 x 1</td><td>Type1</td><td>0</td><td>r</td><td>r</td><td>r</td><td>R</td><td>TC</td><td>R</td><td>Attr</td><td>R</td><td>TH</td><td>TDP</td><td>Attr</td></tr><tr><td>Byte 4</td><td colspan="11">Requester ID</td><td colspan="3">Tag</td></tr><tr><td>Byte 8</td><td colspan="11">Target BDF if ID Routing used,otherwise Reserved</td><td colspan="3">Vendor ID</td></tr><tr><td>Byte 12</td><td colspan="14">For Vendor Definition</td></tr></table>

Table 5-14: Vendor-Defined Message Coding | 表5-14：厂商定义消息编码

<table><tr><td>Vendor-Defined Message</td><td>Message Code 7:0</td><td>Routing 2:0</td></tr><tr><td>Vendor Defined Message 0</td><td>0111 1110b</td><td rowspan="2">000b, 010b, 011b, 100b</td></tr><tr><td>Vendor Defined Message 1</td><td>0111 1111b</td></tr></table>

<table>
<tr>
<td width="50%">
**Vendor-Defined Message Rules:**
</td>
<td width="50%" style="background-color:#e8e8e8">
**厂商定义消息规则：**
</td>
</tr>
<tr>
<td width="50%">
1. A data payload may or may not be included with either type.
</td>
<td width="50%" style="background-color:#e8e8e8">
1. 两种类型的消息可以包含也可以不包含数据负载。
</td>
</tr>
<tr>
<td width="50%">
2. Messages are distinguished by the Vendor ID field.
</td>
<td width="50%" style="background-color:#e8e8e8">
2. 消息通过Vendor ID字段来区分。
</td>
</tr>
<tr>
<td width="50%">
3. Attribute bits [2] and [1:0] are not reserved.
</td>
<td width="50%" style="background-color:#e8e8e8">
3. 属性位[2]和[1:0]不是保留位。
</td>
</tr>
<tr>
<td width="50%">
4. If the Receiver doesn't recognize the Message:
</td>
<td width="50%" style="background-color:#e8e8e8">
4. 如果接收方不识别该消息：
</td>
</tr>
<tr>
<td width="50%">
- Type 1 Messages are silently discarded
</td>
<td width="50%" style="background-color:#e8e8e8">
- 类型1消息将被静默丢弃
</td>
</tr>
<tr>
<td width="50%">
- Type 0 Messages are treated as an Unsupported Request error condition
</td>
<td width="50%" style="background-color:#e8e8e8">
- 类型0消息将被视为不支持的请求错误条件
</td>
</tr>
<tr>
<td width="50%">
**Ignored Messages.** Listing an entire category of Messages that are to be ignored sounds a little strange without the context for it. These were formerly Hot Plug Signaling messages that supported devices that had Hot Plug indicators and push buttons on the add-in card itself rather than on the system board. This Message type was defined through spec rev 1.0a, but this option was no longer supported beginning with the 1.1 spec release, so the details are only included here for reference. As the name now suggests, Transmitters are strongly encouraged not to send these messages, and Receivers are strongly encouraged to ignore them if they are seen. If they're still going to be used anyway, they must conform to the 1.0a spec details.
</td>
<td width="50%" style="background-color:#e8e8e8">
**已忽略的消息。** 在没有上下文的情况下，将一整类消息列为应被忽略的消息听起来有些奇怪。这些消息以前是热插拔信令消息，用于支持那些将热插拔指示灯和按钮置于附加卡本身而非系统板上的设备。此类消息类型在规范修订版1.0a中定义，但从1.1版规范发布开始，此选项不再受支持，因此此处仅包含其细节作为参考。正如其名称所示，强烈建议发送方不要发送这些消息，强烈建议接收方在看到这些消息时将其忽略。如果仍然要使用它们，则必须符合1.0a版规范的详细规定。
</td>
</tr>
</table>

Table 5-15: Hot Plug Message Coding | 表5-15：热插拔消息编码

<table><tr><td>Error Message</td><td>Message Code 7:0</td><td>Routing 2:0</td></tr><tr><td>Attention_Indicator_On</td><td>0100 0001b</td><td>100b</td></tr><tr><td>Attention_Indicator_Blink</td><td>0100 0011b</td><td>100b</td></tr><tr><td>Attention_Indicator_Off</td><td>0100 0000b</td><td>100b</td></tr><tr><td>Power_Indicator_On</td><td>0100 0101b</td><td>100b</td></tr><tr><td>Power_Indicator_Blink</td><td>0100 0111b</td><td>100b</td></tr><tr><td>Power_Indicator_Off</td><td>0100 0100b</td><td>100b</td></tr><tr><td>Attention_Button_Pressed</td><td>0100 1000b</td><td>100b</td></tr></table>

<table>
<tr>
<td width="50%">
**Hot Plug Message Rules:**
</td>
<td width="50%" style="background-color:#e8e8e8">
**热插拔消息规则：**
</td>
</tr>
<tr>
<td width="50%">
- They are driven by a Downstream Port to the card in the slot.
</td>
<td width="50%" style="background-color:#e8e8e8">
- 它们由下游端口驱动发送给插槽中的卡。
</td>
</tr>
<tr>
<td width="50%">
- The Attention Button Message is driven upstream by a slot device.
</td>
<td width="50%" style="background-color:#e8e8e8">
- Attention Button 消息由插槽设备向上游驱动发送。
</td>
</tr>
<tr>
<td width="50%">
**Latency Tolerance Reporting Message.** LTR Messages are used to optionally report acceptable read/write service latencies for a device. To learn more about this power management technique, see the section called "LTR (Latency Tolerance Reporting)" on page 784.
</td>
<td width="50%" style="background-color:#e8e8e8">
**延迟容忍报告消息。** LTR消息用于可选地报告设备可接受的读/写服务延迟。要了解有关此电源管理技术的更多信息，请参阅第784页的"LTR（延迟容忍报告）"一节。
</td>
</tr>
</table>

Figure 5-13: LTR Message Header | 图5-13：LTR消息头

<table><tr><td rowspan="2"></td><td colspan="2">+0</td><td colspan="5">+1</td><td colspan="5">+2</td><td colspan="2">+3</td></tr><tr><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>0</td><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td></tr><tr><td rowspan="2">Byte 0</td><td rowspan="2">Fmt0</td><td rowspan="2">Type1</td><td rowspan="2">0</td><td rowspan="2">1</td><td rowspan="2">0</td><td rowspan="2">0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>R</td><td>TC</td><td>R</td><td>Attr</td><td>R</td><td>TH</td><td>TDP</td><td>Attr</td></tr><tr><td>Byte 4</td><td colspan="11">Requester ID</td><td colspan="2">Tag</td><td>Message Code0 0 0 1 0 0 0 0</td></tr><tr><td>Byte 8</td><td colspan="14">Reserved</td></tr><tr><td>Byte 12</td><td colspan="11">No-Snoop Latency</td><td colspan="3">Snoop Latency</td></tr></table>

Table 5-16: LTR Message Coding | 表5-16：LTR消息编码

<table><tr><td>Latency Tolerance Reporting Message</td><td>Message Code 7:0</td><td>Routing 2:0</td></tr><tr><td>LTR</td><td>0001 0000</td><td>100</td></tr></table>

<table>
<tr>
<td width="50%">
**LTR Message Rules:**
</td>
<td width="50%" style="background-color:#e8e8e8">
**LTR 消息规则：**
</td>
</tr>
<tr>
<td width="50%">
1. They're required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs.
</td>
<td width="50%" style="background-color:#e8e8e8">
1. 此类消息必须使用默认流量类TC0。接收方必须对此进行检查，并将违规情况作为畸形TLP处理。
</td>
</tr>
<tr>
<td width="50%">
2. They don't have a data payload, and the Length field is reserved.
</td>
<td width="50%" style="background-color:#e8e8e8">
2. 它们没有数据负载，长度字段为保留字段。
</td>
</tr>
<tr>
<td width="50%">
**Optimized Buffer Flush and Fill Messages.** OBFF Messages are used to report platform power status to Endpoints and facilitate more effective system power management. To learn more about this technique, see the discussion called "OBFF (Optimized Buffer Flush and Fill)" on page 776.
</td>
<td width="50%" style="background-color:#e8e8e8">
**优化缓冲刷新与填充消息。** OBFF消息用于向端点报告平台电源状态，并促进更有效的系统电源管理。要了解有关此技术的更多信息，请参阅第776页的"OBFF（优化缓冲刷新与填充）"讨论。
</td>
</tr>
</table>

Figure 5-14: OBFF Message Header | 图5-14：OBFF消息头

<table><tr><td rowspan="2"></td><td colspan="2">+0</td><td colspan="5">+1</td><td colspan="5">+2</td><td colspan="2">+3</td></tr><tr><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>0</td><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td></tr><tr><td>Byte 0</td><td>Fmt0</td><td>Type1</td><td>0</td><td>1</td><td>0</td><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Byte 4</td><td colspan="8">Requester ID</td><td colspan="4">Tag</td><td>Message Code0</td><td>0</td></tr><tr><td>Byte 8</td><td colspan="14">Reserved</td></tr><tr><td>Byte 12</td><td colspan="13">Reserved</td><td>OBFFCode</td></tr></table>

Table 5-17: LTR Message Coding | 表5-17：LTR消息编码

<table><tr><td>Optimized Buffer Flush/Fill Message</td><td>Message Code 7:0</td><td>Routing 2:0</td></tr><tr><td>OBFF</td><td>0001 0010</td><td>100</td></tr></table>

<table>
<tr>
<td width="50%">
PCI Express Technology
</td>
<td width="50%" style="background-color:#e8e8e8">
PCI Express 技术
</td>
</tr>
</table>

## OBFF Message Rules

<table>
<tr>
<td width="50%">
1. They're required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs.
</td>
<td width="50%" style="background-color:#e8e8e8">
1. 它们必须使用默认流量类别TC0。接收者必须检查此项，并将违规视为畸形TLP处理。
</td>
</tr>
<tr>
<td width="50%">
2. They don't have a data payload, and the Length field is reserved.
</td>
<td width="50%" style="background-color:#e8e8e8">
2. 它们没有数据载荷，Length字段为保留。
</td>
</tr>
<tr>
<td width="50%">
3. The Requester ID must be set to the Transmitting Port's ID.
</td>
<td width="50%" style="background-color:#e8e8e8">
3. 请求者ID必须设置为发送端口的ID。
</td>
</tr>
</table>