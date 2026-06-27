## 第 5 章：TLP 组成元素

表 5‐7：完成报文 Header 字段（续）

<table><tr><td>字段名称</td><td>Header 字节/位</td><td>功能</td></tr><tr><td>Compl. Status [2:0]（完成状态码）</td><td>Byte 6 Bit 7:5</td><td>这些位指示本次完成报文的状态。000b = 成功完成 (SC)001b = 不支持的请求 (UR)010b = 配置请求重试状态 (CRS)100b = 完成方中止 (CA)所有其他编码均为保留。请参阅第 200 页的“完成状态码汇总”。</td></tr><tr><td>BCM（Byte Count Modified，字节计数值已修改）</td><td>Byte 6 Bit 4</td><td>此位仅由 PCI-X 完成方使用，指示 Byte Count 字段仅报告第一个数据负载，而非剩余的总数据负载。请参阅第 201 页的“使用 Byte Count Modified 位”。</td></tr><tr><td>Byte Count [11:0]（字节计数）</td><td>Byte 6 Bit 3:0Byte 7 Bit 7:0</td><td>满足一次读请求所剩余的字节计数，由原始请求的 Length 字段推导而来。对于由多次完成报文所导致的特殊情况，请参阅第 201 页的“读请求所返回的数据：”。</td></tr><tr><td>Requester ID [15:0]（请求者 ID）</td><td>Byte 8 Bit 7:0Byte 9 Bit 7:0</td><td>从请求报文中复制而来，用作本次完成报文的返回地址（目标）。Byte 8，7:0 = Requester Bus #Byte 9，7:3 = Requester Device #Byte 9，2:0 = Requester Function #</td></tr><tr><td>Tag [7:0]（标签字段）</td><td>Byte 10 Bit 7:0</td><td>此值必须与请求中所收到的 Tag 值一致。请求者根据此 Tag 将本次完成报文与未完成的请求相关联。</td></tr><tr><td>Lower Address [6:0]（低位地址）</td><td>Byte 11 Bit 6:0</td><td>读请求所返回的首个数据的低 7 位地址。由请求的 Length 和 Byte Enables 计算得出，通过显示在到达下一个读完成边界之前可传输多少字节来辅助缓冲区管理。请参阅第 200 页的“计算 Lower Address 字段”。</td></tr></table>

## Completion 状态码汇总。

- 000b (SC) Successful Completion: 请求已被正确处理。

001b (UR) Unsupported Request: 请求不合法或 Completer 无法识别。这属于错误状态,但 Completer 如何响应取决于其设计所遵循的规范版本。在 1.1 规范之前,这被视为不可校正错误 (Uncorrectable Error);而对于 1.1 及以后版本,则作为提示性非致命错误 (Advisory Non-Fatal Error) 处理。详见第 663 页 "Unsupported Request (UR) Status"。

010b (CRS) Configuration Request Retry Status: Completer 暂时无法处理配置请求,该请求应在稍后重试。

100b (CA) Completer Abort: Completer 本应能够处理该请求,但因某种原因失败。这属于不可校正错误 (Uncorrectable Error)。

### Lower Address 字段的计算

此字段由 Completer 设置,用以反映 Completion 有效负载中返回的首个使能字节的字节对齐地址。硬件在计算时需同时考虑 DW 起始地址与原始请求中 First DW Byte Enable 字段所给出的字节使能模式。

对于 Memory Read 请求,该地址为相对于 DW 起始地址的偏移:

- 若 First DW Byte Enable 字段为 1111b,则第一个 DW 中所有字节均使能,偏移为 0。该字段与按 DW 对齐的起始地址一致。

- 若 First DW Byte Enable 字段为 1110b,则第一个 DW 中的高三字节使能,偏移为 1。该字段为 DW 起始地址 + 1。

- 若 First DW Byte Enable 字段为 1100b,则第一个 DW 中的高两字节使能,偏移为 2。该字段为 DW 起始地址 + 2。

- 若 First DW Byte Enable 字段为 1000b,则第一个 DW 中仅最高字节使能,偏移为 3。该字段为 DW 起始地址 + 3。

一旦计算完成,其低 7 位将被填入 Completion 包头的 Lower Address 字段,以适应读完成报文小于整个有效负载且需在首个 RCB 处停止的情况。事务必须按 RCB 边界拆分,而到达第一个 RCB 所传输的字节数则取决于起始地址。

对于 AtomicOp 完成报文,Lower Address 字段为保留。对于所有其他类型的完成报文,该字段置零。

### Byte Count Modified 位的使用

此位仅由 PCI-X Completer 设置,但在通过 PCIe 到 PCI-X 桥接器时,PCI-X Completer 可存在于 PCIe 拓扑之中。其置位规则包括:

1. 仅当读请求将被拆分为多个完成报文时,PCI-X Completer 才会置位此位。

2. 此位仅针对系列中的第一个 Completion 置位,且仅用于指示该第一个 Completion 中的 Byte Count 字段反映的是第一个 Completion 的有效负载,而不是(通常所表示的)剩余总量。Requester 理解:尽管 Byte Count 看似表明这是该请求的最后一个 Completion,但按实际需要,后续还会有其他 Completion 跟随以满足原始请求。

3. 对于该系列中后续的 Completion,BCM 位必须撤销置位,Byte Count 字段将如通常那样反映剩余的总字节数。

4. 收到 BCM 位置位的 Completion 的设备必须正确解析这种情况。

5. 在带数据的完成报文中,Lower Address 字段由 Completer 设置,用以反映所返回数据的首个使能字节的地址。

## 读请求所返回的数据:

1. 一个读请求可能需要多个 Completion 报文才能完成,但最终传输的数据总量必须等于原始请求的大小,否则可能导致 Completion Timeout 错误。

2. 给定的单个 Completion 报文只能服务于一个请求 (Request)。

3. IO 和 Configuration 读请求始终为 1 DW,且始终由单个 Completion 报文满足。

4. 状态码 (Status Code) 不是 SC(成功)的 Completion 报文将终止该事务 (transaction)。

5. 处理需要多个 Completion 报文的读请求时,必须遵守读完成边界 (Read Completion Boundary, RCB)。根复合体 (Root Complex) 的 RCB 为 64 字节或 128 字节,因为它允许修改其端口之间传输的报文大小,所使用的值可在配置寄存器中查看。

6. 网桥和端点在软件控制下可以实现用于选择 RCB 大小(64 或 128 字节)的位。

7. 完全位于对齐的 RCB 边界内的 Completion 报文必须单次传输完成,因为该传输不会跨越 RCB,而 RCB 是允许提前合法停止的唯一位置。

8. 单个读请求的多个 Completion 报文必须按地址递增的顺序返回数据。

## 接收器完成报文处理规则：

1. 收到的完成报文若与挂起的请求不匹配，则属于意外完成报文 (Unexpected Completion)，并按错误处理。

2. 完成状态 (Completion Status) 不是 SC 或 CRS 的完成报文将按错误处理，并释放与其关联的缓冲区空间。

3. 当根复合体 (Root Complex) 在配置周期 (Configuration Cycle) 期间收到 CRS 状态时，该请求即被终止。后续如何处理属于实现方式相关 (implementation‐specific)，但如果根复合体支持此特性，则其行为由 Root Control 寄存器中 CRS Software Visibility 位的设置决定。

   — 如果未启用 CRS Software Visibility，根复合体将重新发起该配置请求若干次（次数由实现方式决定），之后放弃并判定目标设备存在故障。

   如果启用了 CRS Software Visibility，为支持该特性的软件将始终先读取 Vendor ID 字段的两个字节。如果硬件随后为该请求接收到 CRS，则返回 Vendor ID 的值 0001h。该值由 PCI‐SIG 为此用途保留，不对应任何有效的 Vendor ID，用于告知软件发生了此事件。这使得软件可以在等待目标设备就绪（复位后最长可能需要 1 秒）期间转去处理其他任务，而不会被阻塞。对该目标设备的任何其他配置读或写将由根复合体自动重试，作为新的请求重发设计特定次数。

4. 对配置请求之外的请求返回 CRS 状态是非法的，可报告为畸形 TLP (Malformed TLP)。

5. 状态为保留编码 (reserved code) 的完成报文按状态编码为 UR 的情况处理。

6. 如果收到的读完成报文 (Read Completion) 或原子操作完成报文 (AtomicOp Completion) 的状态不是 SC，则该完成报文不包含数据，请求者 (Requester) 必须认为该请求已终止。请求者如何处理此情况属于实现方式相关。

7. 在为读请求返回多个完成报文的情况下，状态不为 SC 的完成报文将结束该事务。在此错误之前已收到的数据如何处理由设备自行决定，属于实现方式相关。

8. 为保持与 PCI 兼容，根复合体 (Root Complex) 在配置周期以表明不支持请求 (Unsupported Request) 的完成报文结束时，可能需要合成一个全 “1” 的读返回值。这与 PCI 主设备中止 (Master Abort) 类似：当枚举软件尝试读取不存在的设备时，会发生 PCI 主设备中止。

---

## Message Requests

Message Requests 取代了 PCI 和 PCI-X 中使用的许多中断、错误和电源管理边带信号。所有 Message Request 都使用 4DW Header 格式,但并非所有字段在每种 Message 类型中都被使用。Byte 8 至 Byte 15 中的字段在某些 Message 中未定义,并在这些情况下被保留(Reserved)。Message 在处理方式上与 Posted Memory Write 事务类似,但其路由可以基于地址、ID 寻址,在某些情况下也可以进行隐式路由。包头中的 Routing 子字段(Byte 0,bits 2:0)指示所使用的路由方法以及哪些附加 Header 寄存器被定义。通用的 Message Request Header 格式如图 5-11(第 203 页)所示。

Figure 5-11: 4DW Message Request Header Format

<table><tr><td colspan="19">4DW Header for Messages</td><td></td></tr><tr><td rowspan="2"></td><td colspan="3">+0</td><td colspan="6">+1</td><td colspan="5">+2</td><td colspan="4">+3</td><td></td></tr><tr><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>0</td><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>0</td><td>7</td><td>6</td><td>5</td></tr><tr><td>Byte 0</td><td colspan="2">Fmt0 x 1</td><td>Type1</td><td>0</td><td>rr</td><td>r</td><td>R</td><td>TC</td><td>R</td><td>Attr</td><td>R</td><td>TH0</td><td>TD</td><td>EP</td><td>Attr0</td><td>0</td><td>0</td><td>Length</td><td></td></tr><tr><td>Byte 4</td><td colspan="12">Requester ID</td><td colspan="4">Tag</td><td colspan="2">MessageCode</td><td></td></tr><tr><td>Byte 8</td><td colspan="18">Bytes 8-11 Vary with Message Code Field</td><td></td></tr><tr><td>Byte 12</td><td colspan="18">Bytes 12-15 Vary with Message Code Field</td><td></td></tr></table>

## Message Request Header Fields(消息请求包头字段).

Table 5‐8: Message Request Header Fields(消息请求包头字段)

<table><tr><td>Field Name</td><td>Header Byte/Bit</td><td>Function</td></tr><tr><td>Fmt [2:0](Format 字段(格式))</td><td>Byte 0 Bit 7:5</td><td>Packet Format(报文格式)。Always a 4DW header(始终为 4DW 包头)001b = Message Request without data(不带数据的消息请求)011b = Message Request with data(带数据的消息请求)</td></tr><tr><td>Type [4:0]</td><td>Byte 0 Bit 4:0</td><td>TLP packet type field(TLP 报文类型字段)。Set to(设置为):Bit 4:3:10b = Msg(消息)Bit 2:0 (Message Routing Subfield)(消息路由子字段)000b = Implicitly Routed to RC (Root Complex)(隐式路由至 RC(根复合体))001b = Routed by address(按地址路由)010b = Routed by ID(按 ID 路由)011b = Implicitly Broadcast from RC(从 RC 隐式广播)100b = Local; terminate at receiver(本地;在接收器终止)101b = Gather &amp; route to RC(收集并路由至 RC)0thers = Reserved, treated as Local(保留,视为本地)</td></tr><tr><td>TC [2:0](Traffic Class 字段(流量类))</td><td>Byte 1 Bit 6:4</td><td>TC is always zero for most Message Requests, ensuring that they don't interfere with high-priority packets(对于大多数消息请求,TC 始终为零,以确保不会干扰高优先级报文)。</td></tr><tr><td>Attr [2](Attr 字段(属性))</td><td>Byte 1 Bit 2</td><td>Indicates whether ID-based Ordering is to be used for this TLP(指示此 TLP 是否使用 IDO (基于 ID 的排序))。To learn more, see "ID Based Ordering (IDO)" on page 301(欲了解更多,请参见第 301 页的"ID Based Ordering (IDO)")。</td></tr><tr><td>TH(TLP Processing Hints)</td><td>Byte 1 Bit 0</td><td>Reserved, except as noted(除特别说明外,保留)。</td></tr><tr><td>TD 位 (中毒数据)</td><td>Byte 2 Bit 7</td><td>If = 1, indicates the presence of a digest field (1 DW) at the end of the TLP (preceding LCRC (链路 CRC) and END)(若 = 1,表示在 TLP 末尾(位于 LCRC (链路 CRC) 和 END 之前)存在摘要字段(1 DW))</td></tr><tr><td>EP 位 (中毒)</td><td>Byte 2 Bit 6</td><td>If = 1, indicates the data payload (if present) is poisoned(若 = 1,表示数据有效负载(若存在)被中毒)。</td></tr></table>

## Chapter 5: TLP 组成元素

Table 5‐8: Message Request Header Fields (Continued)

<table><tr><td>Field Name</td><td>Header Byte/Bit</td><td>Function</td></tr><tr><td>Attr [1:0](Attributes)</td><td>Byte 2 Bit 5:4</td><td>Except as noted, these are always reserved in Message Requests.</td></tr><tr><td>AT [1:0](Address Type)</td><td>Byte 2 Bit 3:2</td><td>Address Type is reserved for Messages and must be zero, but Receivers are not required or even encouraged to check this.</td></tr><tr><td>Length [9:0]</td><td>Byte 2 Bit 1:0Byte 3 Bit 7:0</td><td>Indicates data payload size in DW. For Message Requests, this field is always 0 (no data) or 1 (one DW of data)</td></tr><tr><td>Requester ID [15:0]</td><td>Byte 4 Bit 7:0Byte 5 Bit 7:0</td><td>Identifies the Requester sending the message.Byte 4, 7:0 = Requester Bus #Byte 5, 7:3 = Requester Device #Byte 5, 2:0 = Requester Function #</td></tr><td>Tag [7:0]</td><td>Byte 6 Bit 7:0</td><td>Since all Message Requests are posted and don’t receive Completions, no tag is assigned to them. These bits should be zero.</td></tr><tr><td>Message Code [7:0]</td><td>Byte 7 Bit 7:0</td><td>This field contains the code indicating the type of message being sent.0000 0000b = Unlock Message0001 0000b = Lat. Tolerance Reporting0001 0010b = Optimized Buffer Flush/Fill0001 xxxxb = Power Mgt. Message0010 0xxxb = INTx Message0011 00xxb = Error Message0100 xxxxb = Ignored Messages0101 0000b = Set Slot Power Message0111 111xb = Vendor-Defined Messages</td></tr><tr><td>Address [63:32]</td><td>Byte 8 Bit 7:0Byte 9 Bit 7:0Byte 10 Bit 7:0Byte 11 Bit 7:0</td><td>If address routing was selected for the message (see Type 4:0 field above), then this field contains the upper 32 bits of the 64 bit starting address.Otherwise, this field is not used.</td></tr><tr><td>Address [31:2]</td><td>Byte 12 Bit 7:0Byte 13 Bit 7:0Byte 14 Bit 7:0Byte 15 Bit 7:2</td><td>If address routing is selected (see Type field above), then this field contains the lower part of the 64-bit starting address.If ID routing is selected, Bytes 8 and 9 form the target ID.Otherwise, this field is not used.</td></tr></table>

Message Notes: The following tables specify the message coding used for each of the nine message groups, and is based on the message code field listed in Table 5‐8 on page 204. The defined message groups include:

1. INTx Interrupt Signaling

2. Power Management

3. Error Signaling

4. Locked Transaction Support

5. Slot Power Limit Support

6. Vendor‐Defined Messages

7. Ignored Messages (related to Hot‐Plug support in spec revision 1.1)

8. Latency Tolerance Reporting (LTR)

9. Optimized Buffer Flush and Fill (OBFF)

INTx Interrupt Messages. Many devices are capable of using the PCI 2.3 Message Signaled Interrupt (MSI) method of delivering interrupts, but older devices may not support it. For these cases, PCIe defines a “virtual wire” alternative in which devices simulate the assertion and deassertion of the PCI interrupt pins (INTA‐INTD) by sending Messages. The interrupting device sends the first Message to inform the upstream device that an interrupt has been asserted. Once the interrupt has been serviced, the interrupting device sends a second Message to communicate that the signal has been released. For more on this protocol, refer to the section called “Virtual INTx Signaling” on page 805 for details.

Table 5‐9: INTx Interrupt Signaling Message Coding

<table><tr><td>INTx Message</td><td>Message Code 7:0</td><td>Routing 2:0</td></tr><tr><td>Assert_INTA</td><td>0010 0000b</td><td rowspan="8">100b(Local - Terminate at Rx)</td></tr><tr><td>Assert_INTB</td><td>0010 0001b</td></tr><tr><td>Assert_INTC</td><td>0010 0010b</td></tr><tr><td>Assert_INTD</td><td>0010 0011b</td></tr><tr><td>Deassert_INTA</td><td>0010 0100b</td></tr><tr><td>Deassert_INTB</td><td>0010 0101b</td></tr><tr><td>Deassert_INTC</td><td>0010 0110b</td></tr><tr><td>Deassert_INTD</td><td>0010 0111b</td></tr></table>

Rules regarding the use of INTx Messages:

1. They have no data payload and so the Length field is reserved.

2. They’re only issued by Upstream Ports. Checking this rule for received packets is optional but, if checked, violations will be handled as Malformed TLPs.

3. They’re required to use the default traffic class TC0. Receivers must check for this and violations will be handled as Malformed TLPs.

4. Components at both ends of the Link must track the current state of the four virtual interrupts. If the logical state of one interrupt changes at the Upstream Port, it must send the appropriate INTx message.

5. INTx signaling is disabled when the Interrupt Disable bit of the Command Register is set = 1 (as would be the case for physical interrupt lines).

6. If any virtual INTx signals are active when the Interrupt Disable bit is set in the device, the Upstream Port must send corresponding Deassert\_INTx messages.

7. Switches must track the state of the four INTx signals independently for each Downstream Port and combine the states for the Upstream Port.

8. The Root Complex must track the state of the four INTx lines independently and convert them into system interrupts in an implementation‐specific way.

## PCI Express Technology

9. 它们使用路由类型"在接收器处本地终结(Local-Terminate at Receiver)",以便交换机在必要时重新映射指定的中断引脚(参见第 808 页的"映射与合并 INTx 消息")。因此,INTx 消息中的请求者 ID(Requester ID)可由最后一个发送器分配。

电源管理消息。PCI Express 与 PCI 电源管理兼容,并增加了基于硬件的链路(Link)电源管理。消息用于传递其中一些信息,但要了解整体 PCIe 电源管理协议的工作原理,请参阅第 703 页第 16 章"电源管理"。第 208 页的表 5-10 总结了四种电源管理消息类型。

表 5-10:电源管理消息编码

<table><tr><td>电源管理消息</td><td>消息代码 7:0</td><td>路由 2:0</td></tr><tr><td>PM_Active_State_Nak</td><td>0001 0100b</td><td>100b</td></tr><tr><td>PM_PME</td><td>0001 1000b</td><td>000b</td></tr><tr><td>PM_Turn_Off</td><td>0001 1001b</td><td>011b</td></tr><tr><td>PME_TO_Ack</td><td>0001 1011b</td><td>101b</td></tr></table>

电源管理消息规则:

1. 电源管理消息没有数据有效负载,因此 Length 字段(长度)为保留。

2. 它们必须使用默认流量类别 TC0。接收器必须检查这一点,并将违规情况视为格式错误的 TLP(Malformed TLPs)。

3. PM_Active_State_Nak 由下游端口(Downstream Port)在观察到来自链路邻居的、要求将链路(Link)电源状态切换到 L1 (低功耗休眠)的请求,但其选择不执行该切换时发送(在接收器处本地终结路由)。

4. PM_PME 由请求电源管理事件(PME, 电源管理事件)的组件向上游发送(隐式路由至根复合体(Root Complex))。

5. PM_Turn_Off 由根复合体向下游发送至所有端点(隐式广播自根复合体路由)。

6. PME_TO_Ack 由端点向上游发送。对于具有多个下游端口(Downstream Port)的交换机,在所有下游端口均收到该消息之前,该消息不会被转发到上游(汇聚并路由至根复合体路由)。

错误消息。错误消息(Error Messages)由检测到错误的已使能组件向上游发送(隐式路由至根复合体)。为帮助软件了解如何处理该错误,错误消息在消息包头的请求者 ID(Requester ID)字段中标识请求代理。第 209 页的表 5-11 描述了三种错误消息类型。

表 5-11:错误消息编码

<table><tr><td>错误消息</td><td>消息代码 7:0</td><td>路由 2:0</td></tr><tr><td>ERR_COR(可纠正)</td><td>0011 0000b</td><td rowspan="3">000b</td></tr><tr><td>ERR_NONFATAL(不可纠正,非致命)</td><td>0011 0001b</td></tr><tr><td>ERR_FATAL(不可纠正,致命)</td><td>0011 0011b</td></tr></table>

错误信令消息规则:

1. 它们必须使用默认流量类别 TC0。接收器必须检查这一点,并将违规情况视为格式错误的 TLP(Malformed TLPs)。

2. 它们没有数据有效负载,因此 Length 字段(长度)为保留。

3. 根复合体(Root Complex)将错误消息转换为系统特定的事件。

锁定事务支持。Unlock 消息用作 PCI 中定义且仍可供传统设备(Legacy Devices)使用的锁定事务协议的一部分。该协议以 Memory Read Locked 请求(请求)开始。当路径上的端口看到指向目标设备的该请求时,它们通过将其他请求者排除在使用 VC0 (虚通道)之外来实现原子的读-修改-写协议,直至收到 Unlock 消息。此消息被发送到目标设备,以释放路径上的所有端口并完成锁定事务序列。第 209 页的表 5-12 总结了此消息的编码。

表 5-12:Unlock 消息编码

<table><tr><td>Unlock 消息</td><td>消息代码 7:0</td><td>路由 2:0</td></tr><tr><td>Unlock</td><td>0000 0000b</td><td>011b</td></tr></table>

## PCI Express 技术


---

## Unlock 消息规则：

1. 必须使用默认流量类别 TC0。接收器必须检查此项，并将违规情况作为畸形 TLP（Malformed TLPs）处理。

2. 它们没有数据负载，Length 字段 (长度) 保留。

Set Slot Power Limit 消息。该消息由下游端口 (Downstream Port) 发送到插入插槽 (Slot) 中的设备。此功率限制存储在端点的 Device Capabilities Register 中。表 5‐13 总结了消息编码。

Table 5‐13: Slot Power Limit Message Coding

<table><tr><td>Slot Power Limit Message</td><td>Message Code 7:0</td><td>Routing 2:0</td></tr><tr><td>Set_Slot_Power_Limit</td><td>0101 0000b</td><td>100b</td></tr></table>

## Set\_Slot\_Power\_Limit Message Rules:

1. 此类消息必须使用默认的流量类 TC0。接收器必须对该字段进行检查,并将违规情况作为 Malformed TLP 处理。

2. 数据有效载荷为 1 DW,因此 Length 字段设为 1。32 位数据有效载荷中仅低 10 位用于插槽功率定标,高位的载荷比特必须置 0。

3. 当数据链路层 (Data Link Layer) 转换到 DL\_Up 状态时,或者在数据链路层已经处于 DL\_Up 状态期间对 Slot Capabilities Register 发生配置写操作时,本消息都会自动发送。

4. 如果插槽中插卡的实际功耗已经低于所指定的功率上限,则允许忽略该消息。

Vendor‐Defined Message 0 and 1. 这些消息旨在通过规范本身或厂商特定的扩展来扩展 PCIe 的消息传送能力。其报文头如图 5‐12(第 211 页)所示,编码如图 5‐14(第 211 页)所示。

Figure 5‐12: Vendor‐Defined Message Header

<table><tr><td rowspan="2"></td><td colspan="2">+0</td><td colspan="5">+1</td><td colspan="5">+2</td><td colspan="2">+3</td></tr><tr><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>0</td><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td></tr><tr><td>Byte 0</td><td>Fmt0 x 1</td><td>Type1</td><td>0</td><td>r</td><td>r</td><td>r</td><td>R</td><td>TC</td><td>R</td><td>Attr</td><td>R</td><td>TH</td><td>TDP</td><td>Attr</td></tr><tr><td>Byte 4</td><td colspan="11">Requester ID</td><td colspan="3">Tag</td></tr><tr><td>Byte 8</td><td colspan="11">Target BDF if ID Routing used,otherwise Reserved</td><td colspan="3">Vendor ID</td></tr><tr><td>Byte 12</td><td colspan="14">For Vendor Definition</td></tr></table>

Table 5‐14: Vendor‐Defined Message Coding

<table><tr><td>Vendor-Defined Message</td><td>Message Code 7:0</td><td>Routing 2:0</td></tr><tr><td>Vendor Defined Message 0</td><td>0111 1110b</td><td rowspan="2">000b, 010b, 011b, 100b</td></tr><tr><td>Vendor Defined Message 1</td><td>0111 1111b</td></tr></table>

Vendor‐Defined Message Rules:

1. 这两类消息可以附带数据有效载荷,也可以不附带。

2. 消息之间通过 Vendor ID 字段加以区分。

3. Attr 字段位 [2] 与 [1:0] 不属于保留位。

4. 如果接收器无法识别该消息:

• Type 1 消息将被静默丢弃

• Type 0 消息将被视为 Unsupported Request 错误

Ignored Messages. 单独列出"应被忽略的消息"这一整类消息,如果不结合上下文来看会显得有些奇怪。这些消息原本是 Hot Plug Signaling 消息,用于支持那些在插卡自身(而非系统板上)带有热插拔指示灯和按键的设备。该消息类型在规范修订版 1.0a 中定义,但从 1.1 版规范开始就不再支持,因此此处仅给出相关细节以供参考。正如字面意思所示,强烈建议发送器不要发送这些消息,同时强烈建议接收器在看到这些消息时将其忽略。如果仍然要使用,则必须遵循 1.0a 规范中的细节。

Table 5‐15: Hot Plug Message Coding

<table><tr><td>Error Message</td><td>Message Code 7:0</td><td>Routing 2:0</td></tr><tr><td>Attention_Indicator_On</td><td>0100 0001b</td><td>100b</td></tr><tr><td>Attention_Indicator_Blink</td><td>0100 0011b</td><td>100b</td></tr><tr><td>Attention_Indicator_Off</td><td>0100 0000b</td><td>100b</td></tr><tr><td>Power_Indicator_On</td><td>0100 0101b</td><td>100b</td></tr><tr><td>Power_Indicator_Blink</td><td>0100 0111b</td><td>100b</td></tr><tr><td>Power_Indicator_Off</td><td>0100 0100b</td><td>100b</td></tr><tr><td>Attention_Button_Pressed</td><td>0100 1000b</td><td>100b</td></tr></table>

Hot Plug Message Rules:  
• 它们由下游端口 (Downstream Port) 驱动,发往插槽中的插卡。  
• Attention Button Message 由插槽设备向上游方向驱动。

Latency Tolerance Reporting Message. LTR 消息用于可选地上报设备可接受的读/写服务延迟。要进一步了解该电源管理技术,请参见第 784 页" LTR (Latency Tolerance Reporting)"一节。

Figure 5‐13: LTR Message Header

<table><tr><td rowspan="2"></td><td colspan="2">+0</td><td colspan="5">+1</td><td colspan="5">+2</td><td colspan="2">+3</td></tr><tr><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>0</td><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td></tr><tr><td rowspan="2">Byte 0</td><td rowspan="2">Fmt0</td><td rowspan="2">Type1</td><td rowspan="2">0</td><td rowspan="2">1</td><td rowspan="2">0</td><td rowspan="2">0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>R</td><td>TC</td><td>R</td><td>Attr</td><td>R</td><td>TH</td><td>TDP</td><td>Attr</td></tr><tr><td>Byte 4</td><td colspan="11">Requester ID</td><td colspan="2">Tag</td><td>Message Code0 0 0 1 0 0 0 0</td></tr><tr><td>Byte 8</td><td colspan="14">Reserved</td></tr><tr><td>Byte 12</td><td colspan="11">No-Snoop Latency</td><td colspan="3">Snoop Latency</td></tr></table>

Table 5‐16: LTR Message Coding

<table><tr><td>Latency Tolerance Reporting Message</td><td>Message Code 7:0</td><td>Routing 2:0</td></tr><tr><td>LTR</td><td>0001 0000</td><td>100</td></tr></table>

LTR Message Rules:

1. 此类消息必须使用默认的流量类 TC0。接收器必须对该字段进行检查,并将违规情况作为 Malformed TLP 处理。

2. 它们没有数据有效载荷,Length 字段为保留。

Optimized Buffer Flush and Fill Messages. OBFF 消息用于向端点上报平台电源状态,以便实现更有效的系统电源管理。要进一步了解该技术,请参见第 776 页" OBFF (Optimized Buffer Flush and Fill)"一节。

Figure 5‐14: OBFF Message Header

<table><tr><td rowspan="2"></td><td colspan="2">+0</td><td colspan="5">+1</td><td colspan="5">+2</td><td colspan="2">+3</td></tr><tr><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>0</td><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td></tr><tr><td>Byte 0</td><td>Fmt0</td><td>Type1</td><td>0</td><td>1</td><td>0</td><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Byte 4</td><td colspan="8">Requester ID</td><td colspan="4">Tag</td><td>Message Code0</td><td>0</td></tr><tr><td>Byte 8</td><td colspan="14">Reserved</td></tr><tr><td>Byte 12</td><td colspan="13">Reserved</td><td>OBFFCode</td></tr></table>

Table 5‐17: LTR Message Coding

<table><tr><td>Optimized Buffer Flush/Fill Message</td><td>Message Code 7:0</td><td>Routing 2:0</td></tr><tr><td>OBFF</td><td>0001 0010</td><td>100</td></td></tr></table>

## PCI Express 技术


---

## OBFF 报文规则:

1. 它们必须使用默认的流量类别 TC0。接收器必须检查这一点,并将违规情况作为 Malformed TLP(畸形 TLP)处理。

2. 它们不携带数据净荷,Length 字段为保留。

3. Requester ID 必须设置为发送端口的 ID。


---