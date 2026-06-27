# Ch20_Updates_Spec_Rev_2.1

## 20.1 Rules Related To PCI Express Endpoints | 20.1 与PCI Express端点相关的规则

<table>
<tr>
<td width="50%">
Native PCI Express Endpoints do not support lock. A PCI Express Endpoint must treat a MRdLk Request as an Unsupported Request.
</td>
<td width="50%" style="background-color:#e8e8e8">
原生PCI Express端点不支持锁定。PCI Express端点应将MRdLk请求视为不支持的请求。
</td>
</tr>
</table>

## 20.2 Glossary | 20.2 术语表

## 20.3 128b/130b Encoding | 20.3 128b/130b编码

<table>
<tr>
<td width="50%">
This isn't encoding in the same sense as 8b/10b. Instead, the transmitter sends information in Blocks that consist of 16 raw bytes in a row, preceded by a 2-bit Sync field that indicates whether the Block is to be considered as a Data Block or an Ordered Set Block. This scheme was introduced with Gen3, primarily to allow the Link bandwidth to double without doubling the clock rate. It provides better bandwidth utilization but sacrifices some benefits that 8b/10b provided for receivers.
</td>
<td width="50%" style="background-color:#e8e8e8">
这与8b/10b意义上的编码不同。发送方以数据块(Block)形式发送信息，每个数据块由连续的16个原始字节组成，前面有一个2位的同步字段，指示该数据块应被视为数据块还是有序集块。该方案随Gen3引入，主要是为了允许链路带宽翻倍而无需将时钟频率加倍。它提供了更好的带宽利用率，但牺牲了8b/10b为接收器提供的一些优势。
</td>
</tr>
</table>

## 20.4 8b/10b Encoding | 20.4 8b/10b编码

<table>
<tr>
<td width="50%">
Encoding scheme developed many years ago that's used in many serial transports today. It was designed to help receivers recover the clock and data from the incoming signal, but it also reduces available bandwidth at the receiver by 20%. This scheme is used with the earlier versions of PCIe: Gen1 and Gen2.
</td>
<td width="50%" style="background-color:#e8e8e8">
多年前开发的编码方案，目前仍用于许多串行传输中。它旨在帮助接收器从输入信号中恢复时钟和数据，但也使接收器的可用带宽减少了20%。该方案用于早期版本的PCIe：Gen1和Gen2。
</td>
</tr>
</table>

## 20.5 ACK/NAK Protocol | 20.5 ACK/NAK协议

<table>
<tr>
<td width="50%">
The Acknowledge/Negative Acknowledge mechanism by which the Data Link Layer reports whether TLPs have experienced any errors during transmission. If so, a NAK is returned to the sender to request a replay of the failed TLPs. If not, an ACK is returned to indicate that one or more TLPs have arrived safely.
</td>
<td width="50%" style="background-color:#e8e8e8">
数据链路层用于报告TLP在传输过程中是否遇到错误的确认/否认机制。如果存在错误，则向发送方返回NAK以请求重发失败的TLP。如果没有错误，则返回ACK以指示一个或多个TLP已安全到达。
</td>
</tr>
</table>

## 20.6 ACPI | 20.6 ACPI

<table>
<tr>
<td width="50%">
Advanced Configuration and Power Interface. Specifies the various system and device power states.
</td>
<td width="50%" style="background-color:#e8e8e8">
高级配置与电源接口。指定各种系统和设备电源状态。
</td>
</tr>
</table>

## 20.7 ACS | 20.7 ACS

<table>
<tr>
<td width="50%">
Access Control Services.
</td>
<td width="50%" style="background-color:#e8e8e8">
访问控制服务。
</td>
</tr>
</table>

## 20.8 ARI | 20.8 ARI

<table>
<tr>
<td width="50%">
Alternative Routing-ID Interpretation; optional feature that allows Endpoints to have more Functions that the 8 allowed normally.
</td>
<td width="50%" style="background-color:#e8e8e8">
可选功能，允许端点拥有比通常允许的8个更多的功能。
</td>
</tr>
</table>

## 20.9 ASPM | 20.9 ASPM

<table>
<tr>
<td width="50%">
Active State Power Management: When enabled, this allows hardware to make changes to the Link power state from L0 to L0s or L1 or both.
</td>
<td width="50%" style="background-color:#e8e8e8">
启用时，允许硬件将链路电源状态从L0更改为L0s或L1或两者。
</td>
</tr>
</table>

## 20.10 AtomicOps | 20.10 AtomicOps

<table>
<tr>
<td width="50%">
Atomic Operations; three new Requests added with the 2.1 spec revision. These carry out multiple operations that are guaranteed to take place without interruption within the target device.
</td>
<td width="50%" style="background-color:#e8e8e8">
2.1规范修订版新增的三个请求。它们执行多个操作，保证在目标设备内不中断地完成。
</td>
</tr>
</table>

## 20.11 Bandwidth Management | 20.11 带宽管理

<table>
<tr>
<td width="50%">
Hardware-initiated changes to Link speed or width for the purpose of power conservation or reliability.
</td>
<td width="50%" style="background-color:#e8e8e8">
硬件发起的链路速度或宽度更改，以节省功耗或提高可靠性。
</td>
</tr>
</table>

## 20.12 BAR | 20.12 BAR

<table>
<tr>
<td width="50%">
Base Address Register. Used by Functions to indicate the type and size of their local memory and IO space.
</td>
<td width="50%" style="background-color:#e8e8e8">
基址寄存器。功能(Function)用于指示其本地存储器和IO空间的类型和大小。
</td>
</tr>
</table>

## 20.13 Beacon | 20.13 Beacon

<table>
<tr>
<td width="50%">
Low-frequency in-band signal used by Devices whose main power has been shut off to signal that an event has occurred for which they need to have the power restored. This can be sent across the Link when the Link is in the L2 state.
</td>
<td width="50%" style="background-color:#e8e8e8">
主电源已关闭的设备用来发送信号的带内低频信号，指示发生了需要恢复供电的事件。当链路处于L2状态时，可以通过链路发送此信号。
</td>
</tr>
</table>

## 20.14 BER | 20.14 BER

<table>
<tr>
<td width="50%">
Bit Error Rate or Ratio; a measure of signal integrity based on the number of transmission bit errors seen within a time period.
</td>
<td width="50%" style="background-color:#e8e8e8">
误码率或误码比；基于一段时间内观察到的传输误码数量来衡量信号完整性的指标。
</td>
</tr>
</table>

## 20.15 Bit Lock | 20.15 位锁定

<table>
<tr>
<td width="50%">
The process of acquiring the transmitter's precise clock frequency at the receiver. This is done in the CDR logic and is one of the first steps in Link Training.
</td>
<td width="50%" style="background-color:#e8e8e8">
在接收器处获取发送器精确时钟频率的过程。这由CDR逻辑完成，是链路训练的第一步。
</td>
</tr>
</table>

## 20.16 Block | 20.16 数据块

<table>
<tr>
<td width="50%">
The 130-bit unit sent by a Gen3 transmitter, made up of a 2-bit Sync Field followed by a group of 16 bytes.
</td>
<td width="50%" style="background-color:#e8e8e8">
Gen3发送器发送的130位单元，由2位同步字段后跟16字节组成。
</td>
</tr>
</table>

## 20.17 Block Lock | 20.17 数据块锁定

<table>
<tr>
<td width="50%">
Finding the Block boundaries at the Receiver when using 128b/130b encoding so as to recognize incoming Blocks. The process involves three phases. First, search the incoming stream for an EIEOS (Electrical Idle Exit Ordered Set) and adjust the internal Block boundary to match it. Next, search for the SDS (Start Data Stream) Ordered Set. After that, the receiver is locked into the Block boundary.
</td>
<td width="50%" style="background-color:#e8e8e8">
在使用128b/130b编码时，在接收器处查找数据块边界以识别传入的数据块。该过程涉及三个阶段。首先，在传入的数据流中搜索EIEOS(电气空闲退出有序集)并调整内部数据块边界以匹配它。接下来，搜索SDS(启动数据流有序集)。之后，接收器锁定到数据块边界。
</td>
</tr>
</table>

## 20.18 Bridge | 20.18 桥

<table>
<tr>
<td width="50%">
A Function that acts as the interface between two buses. Switches and the Root Complex will implement bridges on their Ports to enable packet routing, and a bridge can also be made to connect between different protocols, such as between PCIe and PCI.
</td>
<td width="50%" style="background-color:#e8e8e8">
充当两个总线之间接口的功能。交换机和根复合体将在其端口上实现桥以实现数据包路由，并且还可以在不同协议之间建立桥，例如PCIe和PCI之间。
</td>
</tr>
</table>

## 20.19 Byte Striping | 20.19 字节条带化

<table>
<tr>
<td width="50%">
Spreading the output byte stream across all available Lanes. All available Lanes are used whenever sending bytes.
</td>
<td width="50%" style="background-color:#e8e8e8">
将输出字节流扩展到所有可用通道。发送字节时使用所有可用通道。
</td>
</tr>
</table>

## 20.20 CC | 20.20 CC

<table>
<tr>
<td width="50%">
Credits Consumed: Number of credits already used by the transmitter when calculating Flow Control.
</td>
<td width="50%" style="background-color:#e8e8e8">
已消耗的信用量：发送方在计算流控时已使用的信用数量。
</td>
</tr>
</table>

## 20.21 CDR | 20.21 CDR

<table>
<tr>
<td width="50%">
Clock and Data Recovery logic used to recover the Transmitter clock from the incoming bit stream and then sample the bits to recognize patterns. For 8b/10b, that pattern, found in the COM, FTS, and EIEOS symbols, allows the logic to acquire Symbol Lock. For 128b/130b the EIEOS sequence is used to acquire Block Lock by going through the three phases of locking.
</td>
<td width="50%" style="background-color:#e8e8e8">
用于从输入比特流中恢复发送器时钟，然后对比特进行采样以识别模式的时钟和数据恢复逻辑。对于8b/10b，在COM、FTS和EIEOS符号中找到的模式允许逻辑获取符号锁定。对于128b/130b，EIEOS序列用于通过三个锁定阶段获取数据块锁定。
</td>
</tr>
</table>

## 20.22 Character | 20.22 字符

<table>
<tr>
<td width="50%">
Term used to describe the 8-bit values to be communicated between Link neighbors. For Gen1 and Gen2, these are a mix of ordinary data bytes (labeled as D characters) and special control values (labeled as K characters). For Gen3 there are no control characters because 8b/10b encoding is no longer used. In that case, the characters all appear as data bytes.
</td>
<td width="50%" style="background-color:#e8e8e8">
用于描述链路相邻节点之间通信的8位值。对于Gen1和Gen2，这些值混合了普通数据字节(标记为D字符)和特殊控制值(标记为K字符)。对于Gen3，由于不再使用8b/10b编码，因此没有控制字符，所有字符都作为数据字节出现。
</td>
</tr>
</table>

## 20.23 Credit Limit | 20.23 信用上限

<table>
<tr>
<td width="50%">
Credit Limit: Flow Control credits seen as available from the transmitter's perspective. Checked to verify whether enough credits are available to send a TLP.
</td>
<td width="50%" style="background-color:#e8e8e8">
从发送方角度看到的可用流控信用量。检查以验证是否有足够的信用发送TLP。
</td>
</tr>
</table>

## 20.24 Control Character | 20.24 控制字符

<table>
<tr>
<td width="50%">
These are special characters (labeled as "K" characters) used in 8b/10b encoding that facilitate Link training and Ordered Sets. They are not used in Gen3, where there is no distinction between characters.
</td>
<td width="50%" style="background-color:#e8e8e8">
用于8b/10b编码的特殊字符(标记为"K"字符)，有助于链路训练和有序集。在Gen3中不使用，因为那里字符之间没有区别。
</td>
</tr>
</table>

## 20.25 Correctable Errors | 20.25 可纠正错误

<table>
<tr>
<td width="50%">
Errors that are corrected automatically by hardware and don't require software attention.
</td>
<td width="50%" style="background-color:#e8e8e8">
由硬件自动纠正且无需软件关注的错误。
</td>
</tr>
</table>

## 20.26 CR | 20.26 CR

<table>
<tr>
<td width="50%">
Credits Required - this is the sum of CC and PTLP.
</td>
<td width="50%" style="background-color:#e8e8e8">
所需信用量 - 是CC和PTLP之和。
</td>
</tr>
</table>

## 20.27 CRC | 20.27 CRC

<table>
<tr>
<td width="50%">
Cyclic Redundancy Code; added to TLPs and DLLPs to allow verifying error-free transmission. The name means that the patterns are cyclic in nature and are redundant (they don't add any extra information). The codes don't contain enough information to permit automatic error correction, but provide robust error detection.
</td>
<td width="50%" style="background-color:#e8e8e8">
循环冗余校验码；添加到TLP和DLLP中以验证无差错传输。这个名称意味着这些模式是循环性质的且是冗余的(它们不添加任何额外信息)。这些码不包含足够的信息来允许自动纠错，但提供了可靠的检错能力。
</td>
</tr>
</table>

## 20.28 Cut-Through Mode | 20.28 直通模式

<table>
<tr>
<td width="50%">
Mechanism by which a Switch allows a TLP to pass through, forwarded from an ingress Port to an egress Port without storing it first to check for errors. This involves a risk, since the TLP may be found to have errors after part of it has already been forwarded to the egress Port. In that case, the end of the packet is modified in the Data Link Layer to have an LCRC value that is inverted from what it should be, and also modified at the Physical Layer to have an End Bad (EDB) framing symbol for 8b/10b encoding or an EDB token for 128b/130b encoding. The combination tells the receiver that the packet has been nullified and should be discarded without sending an ACK/NAK response.
</td>
<td width="50%" style="background-color:#e8e8e8">
交换机允许TLP通过而不先存储检查错误的机制，从入端口转发到出端口。这涉及风险，因为TLP可能在其部分已被转发到出端口后被发现有错误。在这种情况下，数据包末尾在数据链路层被修改为具有颠倒的LCRC值，并在物理层被修改为具有8b/10b编码的End Bad (EDB)帧符号或128b/130b编码的EDB令牌。这种组合告诉接收器该数据包已被作废，应丢弃而不发送ACK/NAK响应。
</td>
</tr>
</table>

## 20.29 Data Characters | 20.29 数据字符

<table>
<tr>
<td width="50%">
Characters (labeled as "D" characters) that represent ordinary data and are distinguished from control characters in 8b/10b. For Gen3, there is no distinction between characters.
</td>
<td width="50%" style="background-color:#e8e8e8">
表示普通数据的字符(标记为"D"字符)，在8b/10b中与控制字符区分。对于Gen3，字符之间没有区别。
</td>
</tr>
</table>

## 20.30 Data Stream | 20.30 数据流

<table>
<tr>
<td width="50%">
The flow of data Blocks for Gen3 operation. The stream is entered by an SDS (Start of Data Stream Ordered Set) and exited with an EDS (End of Data Stream token). During a Data Stream, only data Blocks or the SOS are expected. When any other Ordered Sets are needed, the Data Stream must be exited and only re-entered when more data Blocks are ready to send. Starting a Data Stream is equivalent to entering the L0 Link state, since Ordered Sets are only sent while in other LTSSM states, like Recovery.
</td>
<td width="50%" style="background-color:#e8e8e8">
Gen3操作的数据块流。通过SDS(启动数据流有序集)进入数据流，并通过EDS(结束数据流令牌)退出。在数据流期间，只期望数据块或SOS。当需要任何其他有序集时，必须退出数据流，只有在准备好发送更多数据块时才重新进入。启动数据流相当于进入L0链路状态，因为有序集只能在其他LTSSM状态(如Recovery)中发送。
</td>
</tr>
</table>

## 20.31 De-emphasis | 20.31 去加重

<table>
<tr>
<td width="50%">
The process of reducing the transmitter voltage for repeated bits in a stream. This has the effect of de-emphasizing the low-frequency components of the signal that are known to cause trouble in a transmission medium and thus improves the signal integrity at the receiver.
</td>
<td width="50%" style="background-color:#e8e8e8">
降低发送器电压以处理流中重复比特的过程。这具有去加重信号中低频分量的效果，这些分量已知会在传输介质中引起问题，从而改善接收器处的信号完整性。
</td>
</tr>
</table>

## 20.32 Digest | 20.32 摘要

<table>
<tr>
<td width="50%">
Another name for the ECRC (End-to-End CRC) value that can optionally be appended to a TLP when it's created in the Transaction Layer.
</td>
<td width="50%" style="background-color:#e8e8e8">
ECRC(端到端CRC)值的另一个名称，该值可以在事务层创建TLP时可选地附加到TLP。
</td>
</tr>
</table>

## 20.33 DLCMSM | 20.33 DLCMSM

<table>
<tr>
<td width="50%">
Data Link Control and Management State Machine; manages the Link Layer training process (which is primarily Flow Control initialization).
</td>
<td width="50%" style="background-color:#e8e8e8">
数据链路控制和管理状态机；管理链路层训练过程(主要是流控初始化)。
</td>
</tr>
</table>

## 20.34 DLLP | 20.34 DLLP

<table>
<tr>
<td width="50%">
Data Link Layer Packet. These are created in the Data Link Layer and are forwarded to the Physical Layer but are not seen by the Transaction Layer.
</td>
<td width="50%" style="background-color:#e8e8e8">
数据链路层数据包。在数据链路层创建并转发到物理层，但事务层看不到。
</td>
</tr>
</table>

## 20.35 DPA | 20.35 DPA

<table>
<tr>
<td width="50%">
Dynamic Power Allocation; a new set of configuration registers with the 2.1 spec revision that defines 32 power substates under the D0 device power state, making it easier for software to control device power options.
</td>
<td width="50%" style="background-color:#e8e8e8">
2.1规范修订版中定义的一组新配置寄存器，在D0设备电源状态下定义了32个电源子状态，使软件更容易控制设备电源选项。
</td>
</tr>
</table>

## 20.36 DSP (Downstream Port) | 20.36 DSP(下游端口)

<table>
<tr>
<td width="50%">
Port that faces downstream, like a Root Port or a Switch Downstream Port. This distinction is meaningful in the LTSSM because the Ports have assigned roles during some states.
</td>
<td width="50%" style="background-color:#e8e8e8">
面向下游的端口，如根端口或交换机下游端口。这种区分在LTSSM中有意义，因为端口在某些状态下具有指定的角色。
</td>
</tr>
</table>

## 20.37 ECRC | 20.37 ECRC

<table>
<tr>
<td width="50%">
End-to-End CRC value, optionally appended to a TLP when it's created in the Transaction Layer. This enables a receiver to verify reliable packet transport from source to destination, regardless of how many Links were crossed to get there.
</td>
<td width="50%" style="background-color:#e8e8e8">
端到端CRC值，在事务层创建TLP时可选择附加。这使接收器能够验证从源到目的地的可靠数据包传输，无论中间经过了多少条链路。
</td>
</tr>
</table>

## 20.38 Egress Port | 20.38 出口端口

<table>
<tr>
<td width="50%">
Port that has outgoing traffic.
</td>
<td width="50%" style="background-color:#e8e8e8">
具有传出流量的端口。
</td>
</tr>
</table>

## 20.39 Elastic Buffer | 20.39 弹性缓冲器

<table>
<tr>
<td width="50%">
Part of the CDR logic, this buffer enables the receiver to compensate for the difference between the transmitter and receiver clocks.
</td>
<td width="50%" style="background-color:#e8e8e8">
CDR逻辑的一部分，此缓冲器使接收器能够补偿发送器和接收器时钟之间的差异。
</td>
</tr>
</table>

## 20.40 EMI | 20.40 EMI

<table>
<tr>
<td width="50%">
Electro-Magnetic Interference: the emitted electrical noise from a system. For PCIe, both SSC and scrambling are used to attack it.
</td>
<td width="50%" style="background-color:#e8e8e8">
电磁干扰：系统发出的电噪声。对于PCIe，使用SSC和加扰来对抗它。
</td>
</tr>
</table>

## 20.41 Endpoint | 20.41 端点

<table>
<tr>
<td width="50%">
PCIe Function that is at the bottom of the PCI Inverted-Tree structure.
</td>
<td width="50%" style="background-color:#e8e8e8">
位于PCI倒树结构底部的PCIe功能。
</td>
</tr>
</table>

## 20.42 Enumeration | 20.42 枚举

<table>
<tr>
<td width="50%">
The process of system discovery in which software reads all of the expected configuration locations to learn which PCI-configurable Functions are visible and thus present in the system.
</td>
<td width="50%" style="background-color:#e8e8e8">
系统发现的过程，软件读取所有期望的配置位置，以了解哪些PCI可配置功能是可见的，从而存在于系统中。
</td>
</tr>
</table>

## 20.43 Equalization | 20.43 均衡

<table>
<tr>
<td width="50%">
The process of adjusting Tx and Rx values to compensate for actual or expected signal distortion through the transmission media. For Gen1 and Gen2, this takes the form of Tx De-emphasis. For Gen3, an active evaluation process is introduced to test the signaling environment and adjust the Tx settings accordingly, and optional Rx equalization is mentioned.
</td>
<td width="50%" style="background-color:#e8e8e8">
调整发送(Tx)和接收(Rx)值以补偿通过传输介质的实际或预期信号失真的过程。对于Gen1和Gen2，这采取Tx去加重的形式。对于Gen3，引入了主动评估过程来测试信号环境并相应地调整Tx设置，并提到了可选的Rx均衡。
</td>
</tr>
</table>

## 20.44 Flow Control | 20.44 流控

<table>
<tr>
<td width="50%">
Mechanism by which transmitters avoid the risk of having packets rejected at a receiver due to lack of buffer space. The receiver sends periodic updates about available buffer space and the transmitter verifies that enough is available before attempting to send a packet.
</td>
<td width="50%" style="background-color:#e8e8e8">
发送方避免数据包因接收方缺乏缓冲空间而被拒绝的机制。接收方发送关于可用缓冲空间的定期更新，发送方在尝试发送数据包前验证是否有足够的空间。
</td>
</tr>
</table>

## 20.45 FLR | 20.45 FLR

<table>
<tr>
<td width="50%">
Function-Level Reset.
</td>
<td width="50%" style="background-color:#e8e8e8">
功能级复位。
</td>
</tr>
</table>

## 20.46 Framing Symbols | 20.46 帧定界符号

<table>
<tr>
<td width="50%">
The "start" and "end" control characters used in 8b/10b encoding that indicate the boundaries of a TLP or DLLP.
</td>
<td width="50%" style="background-color:#e8e8e8">
用于8b/10b编码的"开始"和"结束"控制字符，指示TLP或DLLP的边界。
</td>
</tr>
</table>

## 20.47 Gen1 | 20.47 Gen1

<table>
<tr>
<td width="50%">
Generation 1, meaning designs created to be compliant with the 1.x version of the PCIe spec.
</td>
<td width="50%" style="background-color:#e8e8e8">
第1代，指为符合PCIe规范1.x版本而设计的设计。
</td>
</tr>
</table>

## 20.48 Gen1, Gen2, Gen3 | 20.48 Gen1, Gen2, Gen3

<table>
<tr>
<td width="50%">
Abbreviations for the revisions of the PCIe spec. Gen1 = rev 1.x, Gen2 = rev 2.x, and Gen3 = rev 3.0.
</td>
<td width="50%" style="background-color:#e8e8e8">
PCIe规范修订版的缩写。Gen1 = rev 1.x, Gen2 = rev 2.x, Gen3 = rev 3.0。
</td>
</tr>
</table>

## 20.49 Gen2 | 20.49 Gen2

<table>
<tr>
<td width="50%">
Generation 2, meaning designs created to be compliant with the 2.x version of the PCIe spec.
</td>
<td width="50%" style="background-color:#e8e8e8">
第2代，指为符合PCIe规范2.x版本而设计的设计。
</td>
</tr>
</table>

## 20.50 Gen3 | 20.50 Gen3

<table>
<tr>
<td width="50%">
Generation 3, meaning designs created to be compliant with the 3.x version of the PCIe spec.
</td>
<td width="50%" style="background-color:#e8e8e8">
第3代，指为符合PCIe规范3.x版本而设计的设计。
</td>
</tr>
</table>

## 20.51 IDO | 20.51 IDO

<table>
<tr>
<td width="50%">
ID-based Ordering; when enabled, this allows TLPs from different Requesters to be forwarded out of order with respect to each other. The goal is to improve latency and performance.
</td>
<td width="50%" style="background-color:#e8e8e8">
基于ID的排序；启用时，允许来自不同请求方的TLP相对于彼此乱序转发。目标是改善延迟和性能。
</td>
</tr>
</table>

## 20.52 Implicit Routing | 20.52 隐式路由

<table>
<tr>
<td width="50%">
TLPs whose routing is understood without reference to an address or ID. Only Message requests have the option to use this type of routing.
</td>
<td width="50%" style="background-color:#e8e8e8">
无需参考地址或ID即可理解其路由的TLP。只有消息请求可以选择使用此类路由。
</td>
</tr>
</table>

## 20.53 Ingress Port | 20.53 入口端口

<table>
<tr>
<td width="50%">
Port that has incoming traffic.
</td>
<td width="50%" style="background-color:#e8e8e8">
具有传入流量的端口。
</td>
</tr>
</table>

## 20.54 ISI | 20.54 ISI

<table>
<tr>
<td width="50%">
Inter-Symbol Interference; the effect on one bit time that is caused by the recent bits that preceded it.
</td>
<td width="50%" style="background-color:#e8e8e8">
码间干扰；由前面最近的比特对当前比特时间造成的影响。
</td>
</tr>
</table>

## 20.55 Lane | 20.55 通道

<table>
<tr>
<td width="50%">
The two differential pairs that allow a transmit and receive path of one bit between two Ports. A Link can consist of just one Lane or it may contain as many as 32 Lanes.
</td>
<td width="50%" style="background-color:#e8e8e8">
两个差分对，允许在两个端口之间进行一位的发送和接收路径。一条链路可以只包含一个通道，也可以包含多达32个通道。
</td>
</tr>
</table>

## 20.56 Lane-to-Lane Skew | 20.56 通道间偏移

<table>
<tr>
<td width="50%">
Difference in arrival times for bits on different Lanes. Receivers are required to detect this and correct it internally.
</td>
<td width="50%" style="background-color:#e8e8e8">
不同通道上比特到达时间的差异。接收器需要检测并内部纠正此问题。
</td>
</tr>
</table>

## 20.57 Legacy Endpoint | 20.57 传统端点

<table>
<tr>
<td width="50%">
An Endpoint that carries any of three legacy items forward: support for IO transactions, support for local 32-bit-only prefetchable memory space, or support for the locked transactions.
</td>
<td width="50%" style="background-color:#e8e8e8">
携带以下三种传统特性之一的端点：支持IO事务、支持仅32位本地可预取存储器空间、或支持锁定事务。
</td>
</tr>
</table>

## 20.58 LFSR | 20.58 LFSR

<table>
<tr>
<td width="50%">
Linear-Feedback Shift Register; creates a pseudo-random pattern used to facilitate scrambling.
</td>
<td width="50%" style="background-color:#e8e8e8">
线性反馈移位寄存器；创建用于加扰的伪随机模式。
</td>
</tr>
</table>

## 20.59 Link | 20.59 链路

<table>
<tr>
<td width="50%">
Interface between two Ports, made up of one or more Lanes.
</td>
<td width="50%" style="background-color:#e8e8e8">
两个端口之间的接口，由一个或多个通道组成。
</td>
</tr>
</table>

## 20.60 LTR | 20.60 LTR

<table>
<tr>
<td width="50%">
Latency-Tolerance Reporting; mechanism that allows devices to report to the system how quickly they need to get service when they send a Request. Longer latencies afford more power management options to the system.
</td>
<td width="50%" style="background-color:#e8e8e8">
延迟容忍度报告；允许设备在发送请求时向系统报告它们需要多快得到服务的机制。较长的延迟为系统提供更多电源管理选项。
</td>
</tr>
</table>

## 20.61 LTSSM | 20.61 LTSSM

<table>
<tr>
<td width="50%">
Link Training and Status State Machine; manages the training process for the Physical Layer.
</td>
<td width="50%" style="background-color:#e8e8e8">
链路训练和状态状态机；管理物理层的训练过程。
</td>
</tr>
</table>

## 20.62 Non-posted Request | 20.62 非转发请求

<table>
<tr>
<td width="50%">
A Request that expects to receive a Completion in response. For example, any read request would be non-posted.
</td>
<td width="50%" style="background-color:#e8e8e8">
期望接收完成报文作为响应的请求。例如，任何读请求都是非转发请求。
</td>
</tr>
</table>

## 20.63 Non-prefetchable Memory | 20.63 不可预取存储器

<table>
<tr>
<td width="50%">
Memory that exhibits side effects when read. For example, a status register that automatically self-clears when read. Such data is not safe to prefetch since, if the requester never requested the data and it was discarded, it would be lost to the system. This was an important distinction for PCI bridges, which had to guess about the data size on reads. If they knew it was safe to speculatively read ahead in the memory space, they could guess a larger number and achieve better efficiency. The distinction is much less interesting for PCIe, since the exact byte count for a transfer is included in the TLP, but maintaining it allows backward compatibility.
</td>
<td width="50%" style="background-color:#e8e8e8">
读取时会产生副作用的存储器。例如，读取时自动清零的状态寄存器。此类数据不适合预取，因为如果请求方从未请求过该数据且数据被丢弃，则系统将丢失该数据。这对于PCI桥来说是一个重要的区别，桥必须在读取时猜测数据大小。如果桥知道在存储器空间中推测性预读是安全的，则可以猜测更大的数量并获得更好的效率。对于PCIe来说，这种区别不太重要，因为传输的确切字节数包含在TLP中，但保持这种区别允许向后兼容。
</td>
</tr>
</table>

## 20.64 Nullified Packet | 20.64 作废的数据包

<table>
<tr>
<td width="50%">
When a transmitter recognizes that a packet has an error and should not have been sent, the packet can be "nullified", meaning it should be discarded and the receiver should behave as if it had never been sent. This problem can arise when using "cut-through" operation on a Switch.
</td>
<td width="50%" style="background-color:#e8e8e8">
当发送方识别到数据包有错误且不应被发送时，该数据包可以被"作废"，意味着应丢弃它，接收方应表现得好像它从未被发送过。当在交换机上使用"直通"操作时可能出现此问题。
</td>
</tr>
</table>

## 20.65 OBFF | 20.65 OBFF

<table>
<tr>
<td width="50%">
Optimized Buffer Flush and Fill; mechanism that allows the system to tell devices about the best times to initiate traffic. If devices send requests during optimal times and not during other times system power management will be improved.
</td>
<td width="50%" style="background-color:#e8e8e8">
优化缓冲器刷新和填充；允许系统告诉设备发起流量的最佳时间的机制。如果设备在最佳时间发送请求而不是在其他时间发送，系统电源管理将得到改善。
</td>
</tr>
</table>

## 20.66 Ordered Sets | 20.66 有序集

<table>
<tr>
<td width="50%">
Groups of Symbols sent as Physical Layer communication for Lane management. These often consist of just control characters for 8b/10b encoding. They are created in the Physical Layer of the sender and consumed in the Physical Layer of the receiver without being visible to the other layers at all.
</td>
<td width="50%" style="background-color:#e8e8e8">
作为物理层通信发送的符号组，用于通道管理。对于8b/10b编码，这些通常仅由控制字符组成。它们在发送方的物理层创建并在接收方的物理层消耗，完全不被其他层可见。
</td>
</tr>
</table>

## 20.67 PCI | 20.67 PCI

<table>
<tr>
<td width="50%">
Peripheral Component Interface. Designed to replace earlier bus designs used in PCs, such as ISA.
</td>
<td width="50%" style="background-color:#e8e8e8">
外设组件接口。旨在取代PC中使用的早期总线设计，如ISA。
</td>
</tr>
</table>

## 20.68 PCI-X | 20.68 PCI-X

<table>
<tr>
<td width="50%">
PCI eXtended. Designed to correct the shortcomings of PCI and enable higher speeds.
</td>
<td width="50%" style="background-color:#e8e8e8">
旨在纠正PCI的缺点并实现更高的速度。
</td>
</tr>
</table>

## 20.69 PME | 20.69 PME

<table>
<tr>
<td width="50%">
Power Management Event; message from a device indicating that power-related service is needed.
</td>
<td width="50%" style="background-color:#e8e8e8">
电源管理事件；来自设备的消息，指示需要与电源相关的服务。
</td>
</tr>
</table>

## 20.70 Poisoned TLP | 20.70 毒化TLP

<table>
<tr>
<td width="50%">
Packet whose data payload was known to be bad when it was created. Sending the packet with bad data can be helpful as an aid to diagnosing the problem and determining a solution for it.
</td>
<td width="50%" style="background-color:#e8e8e8">
其数据载荷在创建时已知有误的数据包。发送带有错误数据的数据包有助于诊断问题并确定解决方案。
</td>
</tr>
</table>

## 20.71 Polarity Inversion | 20.71 极性反转

<table>
<tr>
<td width="50%">
The receiver's signal polarity is permitted to be connected backwards to support cases when doing so would simplify board layout. The receiver is required to detect this condition and internally invert the signal to correct it during Link Training.
</td>
<td width="50%" style="background-color:#e8e8e8">
允许接收器的信号极性反向连接，以支持简化板级布局的情况。接收器需要检测此状况并在链路训练期间内部反转信号以纠正。
</td>
</tr>
</table>

## 20.72 Port | 20.72 端口

<table>
<tr>
<td width="50%">
Input/output interface to a PCIe Link.
</td>
<td width="50%" style="background-color:#e8e8e8">
PCIe链路的输入/输出接口。
</td>
</tr>
</table>

## 20.73 Posted Request | 20.73 转发请求

<table>
<tr>
<td width="50%">
A Request packet for which no completion is expected. There are only two such requests defined by the spec: Memory Writes and Messages.
</td>
<td width="50%" style="background-color:#e8e8e8">
不期望收到完成报文的请求数据包。规范只定义了两种此类请求：存储器写和消息。
</td>
</tr>
</table>

## 20.74 Prefetchable Memory | 20.74 可预取存储器

<table>
<tr>
<td width="50%">
Memory that has no side-effects as a result of being read. That property makes it safe to prefetch since, if it's discarded by the intermediate buffer, it can always be read again later if needed. This was an important distinction for PCI bridges, which had to guess about the data size on reads. Prefetchable space allowed speculatively reading more data and gave a chance for better efficiency. The distinction is much less interesting for PCIe, since the exact byte count for a transfer is included in the TLP, but maintaining it allows backward compatibility.
</td>
<td width="50%" style="background-color:#e8e8e8">
读取时没有副作用的存储器。该特性使其可以安全地预取，因为如果被中间缓冲器丢弃，以后需要时总可以再次读取。这对于PCI桥来说是一个重要的区别，桥必须在读取时猜测数据大小。可预取空间允许推测性地读取更多数据，并有机会获得更好的效率。对于PCIe来说，这种区别不太重要，因为传输的确切字节数包含在TLP中，但保持这种区别允许向后兼容。
</td>
</tr>
</table>

## 20.75 PTLP | 20.75 PTLP

<table>
<tr>
<td width="50%">
Pending TLP - Flow Control credits needed to send the current TLP.
</td>
<td width="50%" style="background-color:#e8e8e8">
待处理TLP - 发送当前TLP所需的流控信用量。
</td>
</tr>
</table>

## 20.76 QoS | 20.76 QoS

<table>
<tr>
<td width="50%">
Quality of Service; the ability of the PCIe topology to assign different priorities for different packets. This could just mean giving preference to packets at arbitration points, but in more complex systems, it allows making bandwidth and latency guarantees for packets.
</td>
<td width="50%" style="background-color:#e8e8e8">
服务质量；PCIe拓扑为不同数据包分配不同优先级的能力。这可能只是在仲裁点给予数据包优先权，但在更复杂的系统中，它允许为数据包做出带宽和延迟保证。
</td>
</tr>
</table>

## 20.77 Requester ID | 20.77 请求方ID

<table>
<tr>
<td width="50%">
The configuration address of the Requester for a transaction, meaning the BDF (Bus, Device, and Function number) that corresponds to it. This will be used by the Completer as the return address for the resulting completion packet.
</td>
<td width="50%" style="background-color:#e8e8e8">
事务请求方的配置地址，即对应的BDF(总线号、设备号和功能号)。完成方将使用此地址作为结果完成报文的返回地址。
</td>
</tr>
</table>

## 20.78 Root Complex | 20.78 根复合体

<table>
<tr>
<td width="50%">
The components that act as the interface between the CPU cores in the system and the PCIe topology. This can consist of one or more chips and may be simple or complex. From the PCIe perspective, it serves as the root of the inverted tree structure that backward-compatibility with PCI demands.
</td>
<td width="50%" style="background-color:#e8e8e8">
充当系统中CPU核心与PCIe拓扑之间接口的组件。可以由一个或多个芯片组成，可以简单也可以复杂。从PCIe的角度来看，它是PCI要求的倒树结构的根。
</td>
</tr>
</table>

## 20.79 Run Length | 20.79 游程长度

<table>
<tr>
<td width="50%">
The number of consecutive ones or zeros in a row. For 8b/10b encoding the run length is limited to 5 bits. For 128b/130b, there is no defined limit, but the modified scrambling scheme it uses is intended to compensate for that.
</td>
<td width="50%" style="background-color:#e8e8e8">
连续1或0的数量。对于8b/10b编码，游程长度限制为5位。对于128b/130b，没有定义的限制，但它使用的改进加扰方案旨在补偿这一点。
</td>
</tr>
</table>

## 20.80 Scrambling | 20.80 加扰

<table>
<tr>
<td width="50%">
The process of randomizing the output bit stream to avoid repeated patterns on the Link and thus reduce EMI. Scrambling can be turned off for Gen1 and Gen2 to allow specifying patterns on the Link, but it cannot be turned off for Gen3 because it does other work at that speed and the Link is not expected to be able to work reliably without it.
</td>
<td width="50%" style="background-color:#e8e8e8">
随机化输出比特流以避免链路上出现重复模式从而减少EMI的过程。对于Gen1和Gen2，可以关闭加扰以允许在链路上指定模式，但对于Gen3不能关闭，因为在该速度下加扰还执行其他工作，链路预计在没有加扰的情况下无法可靠工作。
</td>
</tr>
</table>

## 20.81 SOS | 20.81 SOS

<table>
<tr>
<td width="50%">
Skip Ordered Set - used to compensate for the slight frequency difference between Tx and Rx.
</td>
<td width="50%" style="background-color:#e8e8e8">
跳转有序集 - 用于补偿Tx和Rx之间的微小频率差异。
</td>
</tr>
</table>

## 20.82 SSC | 20.82 SSC

<table>
<tr>
<td width="50%">
Spread-Spectrum Clocking. This is a method of reducing EMI in a system by allowing the clock frequency to vary back and forth across an allowed range. This spreads the emitted energy across a wider range of frequencies and thus avoids the problem of having too much EMI energy concentrated in one particular frequency.
</td>
<td width="50%" style="background-color:#e8e8e8">
扩频时钟。通过允许时钟频率在允许范围内来回变化来减少系统中EMI的方法。这会将发射能量分布在更宽的频率范围内，从而避免过多的EMI能量集中在某一特定频率的问题。
</td>
</tr>
</table>

## 20.83 Sticky Bits | 20.83 粘滞位

<table>
<tr>
<td width="50%">
Status bits whose value survives a reset. This characteristic is useful for maintaining status information when errors are detected by a Function downstream of a Link that is no longer operating correctly. The failed Link must be reset to gain access to the downstream Functions, and the error status information in its registers must survive that reset to be available to software.
</td>
<td width="50%" style="background-color:#e8e8e8">
其值在复位后仍然存在的状态位。此特性对于在链路下游的功能检测到错误时维护状态信息很有用，而该链路可能不再正常工作。必须复位故障链路才能访问下游功能，其寄存器中的错误状态信息必须能在复位后保留，以便软件访问。
</td>
</tr>
</table>

## 20.84 Switch | 20.84 交换机

<table>
<tr>
<td width="50%">
A device containing multiple Downstream Ports and one Upstream Port that is able to route traffic between its Ports.
</td>
<td width="50%" style="background-color:#e8e8e8">
包含多个下游端口和一个上游端口的设备，能够在其端口之间路由流量。
</td>
</tr>
</table>

## 20.85 Symbol | 20.85 符号

<table>
<tr>
<td width="50%">
Encoded unit sent across the Link. For 8b/10b these are the 10-bit values that result from encoding, while for 128b/130b they're 8-bit values.
</td>
<td width="50%" style="background-color:#e8e8e8">
跨链路发送的编码单元。对于8b/10b，这些是编码产生的10位值，而对于128b/130b，它们是8位值。
</td>
</tr>
</table>

## 20.86 Symbol Lock | 20.86 符号锁定

<table>
<tr>
<td width="50%">
Finding the Symbol boundaries at the Receiver when using 8b/10b encoding so as to recognize incoming Symbols and thus the contents of packets.
</td>
<td width="50%" style="background-color:#e8e8e8">
在使用8b/10b编码时在接收器处查找符号边界，以识别传入的符号，从而识别数据包的内容。
</td>
</tr>
</table>

## 20.87 Symbol time | 20.87 符号时间

<table>
<tr>
<td width="50%">
The time it takes to send one symbol across the Link - 4ns for Gen1, 2ns for Gen2, and 1ns for Gen3.
</td>
<td width="50%" style="background-color:#e8e8e8">
跨链路发送一个符号所需的时间 - Gen1为4ns, Gen2为2ns, Gen3为1ns。
</td>
</tr>
</table>

## 20.88 TLP | 20.88 TLP

<table>
<tr>
<td width="50%">
Transaction Layer Packet. These are created in the Transaction Layer and passed through the other layers.
</td>
<td width="50%" style="background-color:#e8e8e8">
事务层数据包。在事务层创建并通过其他层传递。
</td>
</tr>
</table>

## 20.89 Token | 20.89 令牌

<table>
<tr>
<td width="50%">
Identifier of the type of information being delivered during a Data Stream when operating at Gen3 speed.
</td>
<td width="50%" style="background-color:#e8e8e8">
在Gen3速率下操作的数据流期间交付的信息类型的标识符。
</td>
</tr>
</table>

## 20.90 TPH | 20.90 TPH

<table>
<tr>
<td width="50%">
TLP Processing Hints; these help system routing agents make choices to improve latency and traffic congestion.
</td>
<td width="50%" style="background-color:#e8e8e8">
TLP处理提示；帮助系统路由代理做出选择以改善延迟和流量拥塞。
</td>
</tr>
</table>

## 20.91 UI | 20.91 UI

<table>
<tr>
<td width="50%">
Unit Interval; the time it takes to send one bit across the Link - 0.4ns for Gen1, 0.2ns for Gen2, 0.125ns for Gen3.
</td>
<td width="50%" style="background-color:#e8e8e8">
单位间隔；跨链路发送一位所需的时间 - Gen1为0.4ns, Gen2为0.2ns, Gen3为0.125ns。
</td>
</tr>
</table>

## 20.92 Uncorrectable Errors | 20.92 不可纠正错误

<table>
<tr>
<td width="50%">
Errors that can't be corrected by hardware and thus will ordinarily require software attention to resolve. These are divided into Fatal errors - those that render further Link operation unreliable, and Non-fatal errors - those that do not affect the Link operation in spite of the problem that was detected.
</td>
<td width="50%" style="background-color:#e8e8e8">
硬件无法纠正的错误，因此通常需要软件关注来解决。这些分为致命错误 - 使进一步链路操作不可靠的错误，和非致命错误 - 尽管检测到问题但不影响链路操作的错误。
</td>
</tr>
</table>

## 20.93 USP | 20.93 USP

<table>
<tr>
<td width="50%">
Upstream Port, meaning a Port that faces upstream, as for an Endpoint or a Switch Upstream Port. This distinction is meaningful in the LTSSM because the Ports have assigned roles during Configuration and Recovery.
</td>
<td width="50%" style="background-color:#e8e8e8">
上游端口，指面向上游的端口，如端点或交换机上游端口。这种区分在LTSSM中有意义，因为端口在配置和恢复期间具有指定的角色。
</td>
</tr>
</table>

## 20.94 Variables | 20.94 变量

<table>
<tr>
<td width="50%">
A number of flags are used to communicate events and status between hardware layers. These are specific to state transitions in the hardware are not usually visible to software. Some examples: — LinkUp - Indication from the Physical Layer to the Data Link Layer that training has completed and the Physical Layer is now operational. — idle_to_rlock_transitioned - This counter tracks the number of times the LTSSM has transitioned from Configuration.Idle to the Recovery.RcvrLock state. Any time the process of recognizing TS2s to leave Configuration doesn't work, the LTSSM transitions to Recovery to take appropriate steps. If it still doesn't work after 256 passes through Recovery (counter reaches FFh), then it goes back to Detect to start over. It may be that some Lanes are not working.
</td>
<td width="50%" style="background-color:#e8e8e8">
使用多个标志来在硬件层之间通信事件和状态。这些特定于硬件中的状态转换，通常对软件不可见。一些示例：— LinkUp - 从物理层到数据链路层的指示，表示训练已完成且物理层现在可操作。— idle_to_rlock_transitioned - 此计数器跟踪LTSSM从Configuration.Idle转换到Recovery.RcvrLock状态的次数。任何时候离开Configuration识别TS2的过程不起作用时，LTSSM转换到Recovery以采取适当措施。如果在经过256次Recovery后仍不起作用(计数器达到FFh)，则返回Detect重新开始。可能某些通道不工作。
</td>
</tr>
</table>

## 20.95 WAKE# | 20.95 WAKE#

<table>
<tr>
<td width="50%">
Side-band pin used to signal to the system that the power should be restored. It's used instead of the Beacon in systems where power conservation is an important consideration.
</td>
<td width="50%" style="background-color:#e8e8e8">
用于向系统发送恢复供电信号的边带引脚。在电源保护是重要考虑因素的系统中，它取代Beacon使用。
</td>
</tr>
</table>

## 20.96 Numerics | 20.96 数字索引

128b/130b 43 128b/130b Encoding 973 1x Packet Format 374, 375 3DW Header 152 3-Tap Transmitter Equalization 585 4DW Headers 152 4x Packet Format 374 8.0 GT/s 410 8b/10b 42 8b/10b Decoder 367 8b/10b Encoder 366 8b/10b Encoding 973

## 20.97 A | 20.97 A

<table>
<tr>
<td width="50%">
AC Coupling 468 ACK 318 Ack 311 ACK DLLP 75, 312 ACK/NAK DLLP 312 ACK/NAK Latency 328 ACK/NAK Protocol 318, 320, 329, 973 Ack/Nak Protocol 74 ACKD_SEQ Count 323 ACKNAK_Latency_Timer 328, 343 ACPI 711, 973 ACPI Driver 706 ACPI Machine Language 712 ACPI Source Language 712 ACPI spec 705 ACPI tables 712 ACS 973 Active State Power Management 405, 735 Address Routing 158 Address Space 121 Address Translation 958, 959 Advanced Correctable Error Reporting 690 Advanced Correctable Error Status 689 Advanced Correctable Errors 688 Advanced Error Reporting 685 Advanced Source ID Register 697 Advanced Uncorrectable Error Handling 691 Advanced Uncorrectable Error Status 691 Aggregate Bandwidth 408 Alternative Routing-ID Interpretation 909 AML 712 AML token interpreter 712 Arbitration 20, 270 Arbor 117 Architecture Overview 39 ARI 909, 974 ASL 712 ASPM 735, 742, 910, 974 ASPM Exit Latency 756, 757 Assert_INTx messages 806 Async Notice of Slot Status Change 876
</td>
<td width="50%" style="background-color:#e8e8e8">
AC Coupling — 交流耦合 468 ACK 318 Ack 311 ACK DLLP 75, 312 ACK/NAK DLLP 312 ACK/NAK 延迟 328 ACK/NAK 协议 318, 320, 329, 973 Ack/Nak Protocol 74 ACKD_SEQ 计数 323 ACKNAK_Latency_Timer 328, 343 ACPI 711, 973 ACPI 驱动 706 ACPI Machine Language 712 ACPI Source Language 712 ACPI 规范 705 ACPI 表 712 ACS 973 主动状态电源管理 405, 735 地址路由 158 地址空间 121 地址转换 958, 959 高级可校正错误报告 690 高级可校正错误状态 689 高级可校正错误 688 高级错误报告 685 高级源 ID 寄存器 697 高级不可校正错误处理 691 高级不可校正错误状态 691 聚合带宽 408 替代路由 ID 解释 909 AML 712 AML 令牌解释器 712 仲裁 20, 270 Arbor 117 架构概述 39 ARI 909, 974 ASL 712 ASPM 735, 742, 910, 974 ASPM 退出延迟 756, 757 Assert_INTx 消息 806 槽位状态变更的异步通知 876
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
AtomicOp 150 AtomicOps 897, 974 Attention Button 854, 862 Attention Indicator 854, 859 Aux_Current field 726
</td>
<td width="50%" style="background-color:#e8e8e8">
AtomicOp 150 原子操作 897, 974 注意力按钮 854, 862 注意力指示灯 854, 859 Aux_Current 字段 726
</td>
</tr>
</table>

## 20.98 B | 20.98 B

<table>
<tr>
<td width="50%">
Bandwidth 42 Bandwidth Congestion 281 Bandwidth Management 974 BAR 126, 960, 974 Base Address Registers 126 Base and Limit Registers 136 BDF 85 Beacon 483, 772, 974 BER 974 BIOS 712, 853 Bit Lock 78, 395, 507, 742, 974 Bit Tracer 929 Block 974 Block Alignment 435 Block Encoding 410 Block Lock 507, 975 Boost 476 Bridge 975 Bus 85 Bus Master 20 Bus Number register 93 Byte Count Modified 201 Byte Enables 181 Byte Striping 371, 372, 373, 975 byte striping 371 Byte Striping logic 365 Byte Un-Striping 402
</td>
<td width="50%" style="background-color:#e8e8e8">
带宽 42 带宽拥塞 281 带宽管理 974 BAR 126, 960, 974 基址寄存器 126 基址与边界寄存器 136 BDF 85 信标 483, 772, 974 BER 974 BIOS 712, 853 位锁定 78, 395, 507, 742, 974 位追踪器 929 块 974 块对齐 435 块编码 410 块锁定 507, 975 提升 476 桥 975 总线 85 总线主控 20 总线号寄存器 93 字节计数已修改 201 字节使能 181 字节条带化 371, 372, 373, 975 byte条带化 371 字节条带化逻辑 365 字节解条带化 402
</td>
</tr>
</table>

## 20.99 C | 20.99 C (索引)

<table>
<tr>
<td width="50%">
Capabilities List bit 818
</td>
<td width="50%" style="background-color:#e8e8e8">
能力列表位 818
</td>
</tr>
<tr>
<td width="50%">
Capabilities Pointer register 713
</td>
<td width="50%" style="background-color:#e8e8e8">
能力指针寄存器 713
</td>
</tr>
<tr>
<td width="50%">
Capability ID 713, 814
</td>
<td width="50%" style="background-color:#e8e8e8">
能力标识符 713, 814
</td>
</tr>
<tr>
<td width="50%">
Capability Structures 88
</td>
<td width="50%" style="background-color:#e8e8e8">
能力结构 88
</td>
</tr>
<tr>
<td width="50%">
Card Connector Power Switching Logic 854
</td>
<td width="50%" style="background-color:#e8e8e8">
卡连接器电源切换逻辑 854
</td>
</tr>
<tr>
<td width="50%">
Card Insertion 855
</td>
<td width="50%" style="background-color:#e8e8e8">
卡插入 855
</td>
</tr>
<tr>
<td width="50%">
Card Insertion Procedure 857
</td>
<td width="50%" style="background-color:#e8e8e8">
卡插入过程 857
</td>
</tr>
<tr>
<td width="50%">
Card Present 854
</td>
<td width="50%" style="background-color:#e8e8e8">
卡存在 854
</td>
</tr>
<tr>
<td width="50%">
Card Removal 855
</td>
<td width="50%" style="background-color:#e8e8e8">
卡移除 855
</td>
</tr>
<tr>
<td width="50%">
Card Removal Procedure 856
</td>
<td width="50%" style="background-color:#e8e8e8">
卡移除过程 856
</td>
</tr>
<tr>
<td width="50%">
Card Reset Logic 854
</td>
<td width="50%" style="background-color:#e8e8e8">
卡复位逻辑 854
</td>
</tr>
<tr>
<td width="50%">
CC 975
</td>
<td width="50%" style="background-color:#e8e8e8">
CC 975
</td>
</tr>
<tr>
<td width="50%">
CDR 435, 437, 975
</td>
<td width="50%" style="background-color:#e8e8e8">
CDR 435, 437, 975
</td>
</tr>
<tr>
<td width="50%">
Character 79, 366, 975
</td>
<td width="50%" style="background-color:#e8e8e8">
字符 79, 366, 975
</td>
</tr>
<tr>
<td width="50%">
CL 976
</td>
<td width="50%" style="background-color:#e8e8e8">
CL 976
</td>
</tr>
<tr>
<td width="50%">
Class driver 706
</td>
<td width="50%" style="background-color:#e8e8e8">
类驱动程序 706
</td>
</tr>
<tr>
<td width="50%">
Clock Requirements 452
</td>
<td width="50%" style="background-color:#e8e8e8">
时钟要求 452
</td>
</tr>
<tr>
<td width="50%">
Code Violation 400
</td>
<td width="50%" style="background-color:#e8e8e8">
编码违规 400
</td>
</tr>
<tr>
<td width="50%">
Coefficients 584
</td>
<td width="50%" style="background-color:#e8e8e8">
系数 584
</td>
</tr>
<tr>
<td width="50%">
Cold Reset 834
</td>
<td width="50%" style="background-color:#e8e8e8">
冷复位 834
</td>
</tr>
<tr>
<td width="50%">
COM 386
</td>
<td width="50%" style="background-color:#e8e8e8">
COM 386
</td>
</tr>
<tr>
<td width="50%">
Common-Mode Noise Rejection 452
</td>
<td width="50%" style="background-color:#e8e8e8">
共模噪声抑制 452
</td>
</tr>
<tr>
<td width="50%">
Completer 33
</td>
<td width="50%" style="background-color:#e8e8e8">
完成者 33
</td>
</tr>
<tr>
<td width="50%">
Completer Abort 664
</td>
<td width="50%" style="background-color:#e8e8e8">
完成者中止 664
</td>
</tr>
<tr>
<td width="50%">
Completion Packet 197
</td>
<td width="50%" style="background-color:#e8e8e8">
完成报文包 197
</td>
</tr>
<tr>
<td width="50%">
Completion Status 200
</td>
<td width="50%" style="background-color:#e8e8e8">
完成状态 200
</td>
</tr>
<tr>
<td width="50%">
Completion Time-out 665
</td>
<td width="50%" style="background-color:#e8e8e8">
完成超时 665
</td>
</tr>
<tr>
<td width="50%">
Completion TLP 184
</td>
<td width="50%" style="background-color:#e8e8e8">
完成TLP 184
</td>
</tr>
<tr>
<td width="50%">
Completions 196, 218
</td>
<td width="50%" style="background-color:#e8e8e8">
完成报文 196, 218
</td>
</tr>
<tr>
<td width="50%">
Compliance Pattern 537
</td>
<td width="50%" style="background-color:#e8e8e8">
合规性测试图案 537
</td>
</tr>
<tr>
<td width="50%">
Compliance Pattern - 8b/10b 529
</td>
<td width="50%" style="background-color:#e8e8e8">
合规性测试图案 - 8b/10b 529
</td>
</tr>
<tr>
<td width="50%">
Configuration 85
</td>
<td width="50%" style="background-color:#e8e8e8">
配置 85
</td>
</tr>
<tr>
<td width="50%">
Configuration Address Port 92, 93
</td>
<td width="50%" style="background-color:#e8e8e8">
配置地址端口 92, 93
</td>
</tr>
<tr>
<td width="50%">
Configuration Address Space 88
</td>
<td width="50%" style="background-color:#e8e8e8">
配置地址空间 88
</td>
</tr>
<tr>
<td width="50%">
Configuration Cycle Generation 26
</td>
<td width="50%" style="background-color:#e8e8e8">
配置周期生成 26
</td>
</tr>
<tr>
<td width="50%">
Configuration Data Port 92, 93
</td>
<td width="50%" style="background-color:#e8e8e8">
配置数据端口 92, 93
</td>
</tr>
<tr>
<td width="50%">
Configuration Headers 50
</td>
<td width="50%" style="background-color:#e8e8e8">
配置头标 50
</td>
</tr>
<tr>
<td width="50%">
Configuration Read 151
</td>
<td width="50%" style="background-color:#e8e8e8">
配置读取 151
</td>
</tr>
<tr>
<td width="50%">
Configuration Read Access 104
</td>
<td width="50%" style="background-color:#e8e8e8">
配置读取访问 104
</td>
</tr>
<tr>
<td width="50%">
Configuration Register Space 27, 89
</td>
<td width="50%" style="background-color:#e8e8e8">
配置寄存器空间 27, 89
</td>
</tr>
<tr>
<td width="50%">
Configuration Registers 90
</td>
<td width="50%" style="background-color:#e8e8e8">
配置寄存器 90
</td>
</tr>
<tr>
<td width="50%">
Configuration Request Packet 193
</td>
<td width="50%" style="background-color:#e8e8e8">
配置请求包 193
</td>
</tr>
<tr>
<td width="50%">
Configuration Requests 99, 192
</td>
<td width="50%" style="background-color:#e8e8e8">
配置请求 99, 192
</td>
</tr>
<tr>
<td width="50%">
Configuration Space 122
</td>
<td width="50%" style="background-color:#e8e8e8">
配置空间 122
</td>
</tr>
<tr>
<td width="50%">
Configuration State 520, 540
</td>
<td width="50%" style="background-color:#e8e8e8">
配置状态 520, 540
</td>
</tr>
<tr>
<td width="50%">
Configuration Status Register 676
</td>
<td width="50%" style="background-color:#e8e8e8">
配置状态寄存器 676
</td>
</tr>
<tr>
<td width="50%">
Configuration Status register 713
</td>
<td width="50%" style="background-color:#e8e8e8">
配置状态寄存器 713
</td>
</tr>
<tr>
<td width="50%">
Configuration Transactions 91
</td>
<td width="50%" style="background-color:#e8e8e8">
配置事务 91
</td>
</tr>
<tr>
<td width="50%">
Configuration Write 151
</td>
<td width="50%" style="background-color:#e8e8e8">
配置写入 151
</td>
</tr>
<tr>
<td width="50%">
Configuration.Complete 562
</td>
<td width="50%" style="background-color:#e8e8e8">
Configuration.Complete 562
</td>
</tr>
<tr>
<td width="50%">
Configuration.Idle 566
</td>
<td width="50%" style="background-color:#e8e8e8">
Configuration.Idle 566
</td>
</tr>
<tr>
<td width="50%">
Configuration.Lanenum.Accept 560
</td>
<td width="50%" style="background-color:#e8e8e8">
Configuration.Lanenum.Accept 560
</td>
</tr>
<tr>
<td width="50%">
Configuration.Lanenum.Wait 559
</td>
<td width="50%" style="background-color:#e8e8e8">
Configuration.Lanenum.Wait 559
</td>
</tr>
<tr>
<td width="50%">
Configuration.Linkwidth.Accept 558
</td>
<td width="50%" style="background-color:#e8e8e8">
Configuration.Linkwidth.Accept 558
</td>
</tr>
<tr>
<td width="50%">
Configuration.Linkwidth.Start 553
</td>
<td width="50%" style="background-color:#e8e8e8">
Configuration.Linkwidth.Start 553
</td>
</tr>
<tr>
<td width="50%">
Congestion Avoidance 897
</td>
<td width="50%" style="background-color:#e8e8e8">
拥塞避免 897
</td>
</tr>
<tr>
<td width="50%">
Continuous-Time Linear Equalization 49
</td>
<td width="50%" style="background-color:#e8e8e8">
连续时间线性均衡 49
</td>
</tr>
<tr>
<td width="50%">
Control Character 976
</td>
<td width="50%" style="background-color:#e8e8e8">
控制字符 976
</td>
</tr>
<tr>
<td width="50%">
Control Character Encoding 386
</td>
<td width="50%" style="background-color:#e8e8e8">
控制字符编码 386
</td>
</tr>
<tr>
<td width="50%">
Control Method 712
</td>
<td width="50%" style="background-color:#e8e8e8">
控制方法 712
</td>
</tr>
<tr>
<td width="50%">
Conventional Reset 834
</td>
<td width="50%" style="background-color:#e8e8e8">
常规复位 834
</td>
</tr>
<tr>
<td width="50%">
Correctable Errors 651, 976
</td>
<td width="50%" style="background-color:#e8e8e8">
可纠正错误 651, 976
</td>
</tr>
<tr>
<td width="50%">
CR 976
</td>
<td width="50%" style="background-color:#e8e8e8">
CR 976
</td>
</tr>
<tr>
<td width="50%">
CRC 976
</td>
<td width="50%" style="background-color:#e8e8e8">
CRC 976
</td>
</tr>
<tr>
<td width="50%">
CRD 383
</td>
<td width="50%" style="background-color:#e8e8e8">
CRD 383
</td>
</tr>
<tr>
<td width="50%">
Credit Allocated Count 229
</td>
<td width="50%" style="background-color:#e8e8e8">
信用量分配计数 229
</td>
</tr>
<tr>
<td width="50%">
Credit Limit counter 228
</td>
<td width="50%" style="background-color:#e8e8e8">
信用量限制计数器 228
</td>
</tr>
<tr>
<td width="50%">
CREDIT_ALLOCATED 229
</td>
<td width="50%" style="background-color:#e8e8e8">
CREDIT_ALLOCATED 229
</td>
</tr>
<tr>
<td width="50%">
Credits Consumed counter 228
</td>
<td width="50%" style="background-color:#e8e8e8">
信用量消耗计数器 228
</td>
</tr>
<tr>
<td width="50%">
Credits Received Counter 229
</td>
<td width="50%" style="background-color:#e8e8e8">
信用量接收计数器 229
</td>
</tr>
<tr>
<td width="50%">
CREDITS_RECEIVED 229
</td>
<td width="50%" style="background-color:#e8e8e8">
CREDITS_RECEIVED 229
</td>
</tr>
<tr>
<td width="50%">
CTLE 493, 494
</td>
<td width="50%" style="background-color:#e8e8e8">
CTLE 493, 494
</td>
</tr>
<tr>
<td width="50%">
Current Running Disparity 383
</td>
<td width="50%" style="background-color:#e8e8e8">
当前运行不一致性 383
</td>
</tr>
<tr>
<td width="50%">
Cursor Coefficient 584
</td>
<td width="50%" style="background-color:#e8e8e8">
游标系数 584
</td>
</tr>
<tr>
<td width="50%">
Cut-Through 354
</td>
<td width="50%" style="background-color:#e8e8e8">
直通转发 354
</td>
</tr>
<tr>
<td width="50%">
Cut-Through Mode 976
</td>
<td width="50%" style="background-color:#e8e8e8">
直通转发模式 976
</td>
</tr>
</table>

## 20.100 D | 20.100 D

<table>
<tr>
<td width="50%">
D0 709, 710, 714, 734 D0 Active 714 D0 Uninitialized 714 D1 709, 710, 716, 734 D1\_Support bit 725 D2 709, 710, 717, 734 D2\_Support bit 725 D3 709, 710, 719 D3cold 721, 734 D3hot 719, 734 Data Characters 976 Data Link Layer 55, 72 Data Link Layer Packet 72 Data Link Layer Packet Format 310 Data Link Layer Packets 73 Data Poisoning 660 Data Register 731 Data Stream 977 Data\_Scale field 729 Data\_Select field 729 DC Common Mode 462 DC Common Mode Voltage 466 DC Common-Mode Voltage 467 Deadlock Avoidance 303 Deassert\_INTx messages 806 Debugging PCIe Traffic 917 Decision Feedback Equalization 495 De-emphasis 450, 468, 469, 471, 476, 977 De-Scrambler 367 Deserializer 395 De-Skew 399 Detect State 519, 522 Detect.Active 524 Detect.Quiet 523 Device 85 Device Capabilities 2 Register 899 Device Capabilities Register 873 Device Context 709 Device Core 59 Device core 55 Device Driver 706 device driver 853 Device Layers 54 Device PM States 713 device PM states 709 Device Status Register 681 Device-Specific Initialization (DSI) bit 727 DFE 493, 495, 497 Differential Driver 389 Differential Receiver 393, 435, 451 Differential Signaling 463 Differential Signals 44 Differential Transmitter 451 Digest 180, 977 Direct Address Translation 949
</td>
<td width="50%" style="background-color:#e8e8e8">
D0 709, 710, 714, 734 D0 Active 714 D0 Uninitialized 714 D1 709, 710, 716, 734 D1\_Support位 725 D2 709, 710, 717, 734 D2\_Support位 725 D3 709, 710, 719 D3cold 721, 734 D3hot 719, 734 数据字符 976 数据链路层 55, 72 数据链路层报文 72 数据链路层报文格式 310 数据链路层报文 73 数据中毒 660 数据寄存器 731 数据流 977 Data\_Scale字段 729 Data\_Select字段 729 DC共模 462 DC共模电压 466 DC共模电压 467 死锁避免 303 去断言INTx消息 806 PCIe流量调试 917 决策反馈均衡 495 去加重 450, 468, 469, 471, 476, 977 解扰器 367 解串器 395 去偏移 399 检测状态 519, 522 Detect.Active 524 Detect.Quiet 523 设备 85 设备能力2寄存器 899 设备能力寄存器 873 设备上下文 709 设备核心 59 设备核心 55 设备驱动 706 设备驱动 853 设备层 54 设备PM状态 713 设备PM状态 709 设备状态寄存器 681 设备特定初始化(DSI)位 727 DFE 493, 495, 497 差分驱动器 389 差分接收器 393, 435, 451 差分信令 463 差分信号 44 差分发送器 451 摘要 180, 977 直接地址转换 949
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Disable State 521, 613 Discrete Time Linear Equalizer 493 Discrete-Time Linear Equalizer 494 Disparity 383 Disparity Error Detection 400 DLCMSM 977 DLE 493, 494 DLL 437 DLLP 73, 170, 238, 308, 311, 977 DLLP Elements 307 DMA 937 DPA 910, 977 Driver Characteristics 489 DSI bit 727 DSP 977 D-State Transitions 722 Dual Simplex 363 Dual-Simplex 40 Dual-Star Fabric 957 Dynamic Bandwidth Changes 618 Dynamic Link Speed Changes 619 Dynamic Link Width Changes 629 Dynamic Power Allocation 910
</td>
<td width="50%" style="background-color:#e8e8e8">
禁用状态 521, 613 离散时间线性均衡器 493 离散时间线性均衡器 494 不一致 383 不一致错误检测 400 DLCMSM 977 DLE 493, 494 DLL 437 DLLP 73, 170, 238, 308, 311, 977 DLLP元素 307 DMA 937 DPA 910, 977 驱动器特性 489 DSI位 727 DSP 977 D状态转换 722 双单工 363 双单工 40 双星结构 957 动态带宽变化 618 动态链路速率变化 619 动态链路宽度变化 629 动态功耗分配 910
</td>
</tr>
</table>

## 20.101 E | 20.101 E

<table>
<tr>
<td width="50%">
ECRC 63, 180, 978 ECRC Generation and Checking 657
</td>
<td width="50%" style="background-color:#e8e8e8">
ECRC 63, 180, 978 ECRC 生成与检查 657
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
EDB 373, 387
</td>
<td width="50%" style="background-color:#e8e8e8">
EDB 373, 387
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Egress Port 978
</td>
<td width="50%" style="background-color:#e8e8e8">
Egress Port 978
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
EIE 387
</td>
<td width="50%" style="background-color:#e8e8e8">
EIE 387
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
EIEOS 389, 739, 740
</td>
<td width="50%" style="background-color:#e8e8e8">
EIEOS 389, 739, 740
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
EIOS 388, 737
</td>
<td width="50%" style="background-color:#e8e8e8">
EIOS 388, 737
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Elastic Buffer 366, 435, 978
</td>
<td width="50%" style="background-color:#e8e8e8">
弹性缓冲 366, 435, 978
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Electrical Idle 388, 736, 738, 741
</td>
<td width="50%" style="background-color:#e8e8e8">
电气空闲 388, 736, 738, 741
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Electrical Idle Exit Ordered Set 389
</td>
<td width="50%" style="background-color:#e8e8e8">
电气空闲退出有序集 389
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Electrical Idle Ordered Set 388
</td>
<td width="50%" style="background-color:#e8e8e8">
电气空闲有序集 388
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
EMI 77, 978
</td>
<td width="50%" style="background-color:#e8e8e8">
EMI 77, 978
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Encoding 410
</td>
<td width="50%" style="background-color:#e8e8e8">
编码 410
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
END 373, 387
</td>
<td width="50%" style="background-color:#e8e8e8">
END 373, 387
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Endpoint 978
</td>
<td width="50%" style="background-color:#e8e8e8">
端点 978
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
End-to-End CRC 180
</td>
<td width="50%" style="background-color:#e8e8e8">
端到端 CRC 180
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Enhanced Configuration Access Mechanism 96
</td>
<td width="50%" style="background-color:#e8e8e8">
增强配置访问机制 96
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Enumeration 51, 104, 978
</td>
<td width="50%" style="background-color:#e8e8e8">
枚举 51, 104, 978
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Equalization 474, 978
</td>
<td width="50%" style="background-color:#e8e8e8">
均衡 474, 978
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Equalization - Phase 0 578
</td>
<td width="50%" style="background-color:#e8e8e8">
均衡 - 阶段 0 578
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Equalization - Phase 1 581
</td>
<td width="50%" style="background-color:#e8e8e8">
均衡 - 阶段 1 581
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Equalization - Phase 2 583
</td>
<td width="50%" style="background-color:#e8e8e8">
均衡 - 阶段 2 583
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Equalization - Phase 3 586
</td>
<td width="50%" style="background-color:#e8e8e8">
均衡 - 阶段 3 586
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Equalization Control 513
</td>
<td width="50%" style="background-color:#e8e8e8">
均衡控制 513
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Equalization Control Registers 579
</td>
<td width="50%" style="background-color:#e8e8e8">
均衡控制寄存器 579
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Equalizer 475
</td>
<td width="50%" style="background-color:#e8e8e8">
均衡器 475
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Equalizer Coefficients 479
</td>
<td width="50%" style="background-color:#e8e8e8">
均衡器系数 479
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Error Classifications 651
</td>
<td width="50%" style="background-color:#e8e8e8">
错误分类 651
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Error Handling 282, 699
</td>
<td width="50%" style="background-color:#e8e8e8">
错误处理 282, 699
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Error Isolation 937
</td>
<td width="50%" style="background-color:#e8e8e8">
错误隔离 937
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Error Messages 209, 668
</td>
<td width="50%" style="background-color:#e8e8e8">
错误消息 209, 668
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
ESD 459
</td>
<td width="50%" style="background-color:#e8e8e8">
ESD 459
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
ESD standards 448
</td>
<td width="50%" style="background-color:#e8e8e8">
ESD 标准 448
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Exerciser Card 931
</td>
<td width="50%" style="background-color:#e8e8e8">
测试卡 931
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Extended Configuration Space 89
</td>
<td width="50%" style="background-color:#e8e8e8">
扩展配置空间 89
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Eye Diagram 486
</td>
<td width="50%" style="background-color:#e8e8e8">
眼图 486
</td>
</tr>
</table>

## 20.102 F | 20.102 F

<table>
<tr>
<td width="50%">
Failover 942, 944, 952
</td>
<td width="50%" style="background-color:#e8e8e8">
故障转移 942, 944, 952
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
FC Initialization 223
</td>
<td width="50%" style="background-color:#e8e8e8">
FC初始化 223
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
FC Initialization Sequence 223
</td>
<td width="50%" style="background-color:#e8e8e8">
FC初始化序列 223
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
FC_Init1 224
</td>
<td width="50%" style="background-color:#e8e8e8">
FC_Init1 224
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
FC_Init2 225
</td>
<td width="50%" style="background-color:#e8e8e8">
FC_Init2 225
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
FC_Update 238
</td>
<td width="50%" style="background-color:#e8e8e8">
FC_Update 238
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
First DW Byte Enables 178, 181
</td>
<td width="50%" style="background-color:#e8e8e8">
首个双字字节使能 178, 181
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Flow Control 72, 76, 215, 217, 299, 928, 978
</td>
<td width="50%" style="background-color:#e8e8e8">
流控 72, 76, 215, 217, 299, 928, 978
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Flow Control Buffer 217, 229
</td>
<td width="50%" style="background-color:#e8e8e8">
流控缓冲区 217, 229
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Flow Control Buffers 217
</td>
<td width="50%" style="background-color:#e8e8e8">
流控缓冲区 217
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Flow Control Credits 216, 219
</td>
<td width="50%" style="background-color:#e8e8e8">
流控信用量 216, 219
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Flow Control Elements 227, 231
</td>
<td width="50%" style="background-color:#e8e8e8">
流控元素 227, 231
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Flow Control Initialization 227, 230, 237
</td>
<td width="50%" style="background-color:#e8e8e8">
流控初始化 227, 230, 237
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Flow Control Packet 239
</td>
<td width="50%" style="background-color:#e8e8e8">
流控报文 239
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Flow Control Packet Format 314
</td>
<td width="50%" style="background-color:#e8e8e8">
流控报文格式 314
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Flow Control Update Frequency 239
</td>
<td width="50%" style="background-color:#e8e8e8">
流控更新频率 239
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Flow Control Updates 237
</td>
<td width="50%" style="background-color:#e8e8e8">
流控更新 237
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
FLR 842, 844, 845, 978
</td>
<td width="50%" style="background-color:#e8e8e8">
FLR 842, 844, 845, 978
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Flying Lead Probe 924
</td>
<td width="50%" style="background-color:#e8e8e8">
飞线探针 924
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Format Field 179
</td>
<td width="50%" style="background-color:#e8e8e8">
格式字段 179
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Framing Symbols 171, 979
</td>
<td width="50%" style="background-color:#e8e8e8">
帧定界符 171, 979
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
FTS 387
</td>
<td width="50%" style="background-color:#e8e8e8">
FTS 387
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
FTS Ordered Set 388
</td>
<td width="50%" style="background-color:#e8e8e8">
FTS有序集 388
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
FTSOS 388
</td>
<td width="50%" style="background-color:#e8e8e8">
FTSOS 388
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Function 85
</td>
<td width="50%" style="background-color:#e8e8e8">
功能 85
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Function Level Reset 842, 843
</td>
<td width="50%" style="background-color:#e8e8e8">
功能级复位 842, 843
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Function PM State Transitions 722
</td>
<td width="50%" style="background-color:#e8e8e8">
功能电源管理状态转换 722
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Function State Transition Delays 724
</td>
<td width="50%" style="background-color:#e8e8e8">
功能状态转换延迟 724
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Fundamental Reset 834
</td>
<td width="50%" style="background-color:#e8e8e8">
基础复位 834
</td>
</tr>
</table>

## 20.103 G | 20.103 G

<table>
<tr>
<td width="50%">
Gen1 43, 77, 979<br>
Gen2 43, 77, 979<br>
Gen3 44, 77, 407, 979<br>
Gen3 products 936
</td>
<td width="50%" style="background-color:#e8e8e8">
Gen1 第43、77、979页<br>
Gen2 第43、77、979页<br>
Gen3 第44、77、407、979页<br>
Gen3 产品 第936页
</td>
</tr>
</table>

## 20.104 H | 20.104 H

<table>
<tr>
<td width="50%">
handler 712
</td>
<td width="50%" style="background-color:#e8e8e8">
处理程序 712
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Hardware Based Fixed Arbitration 256
</td>
<td width="50%" style="background-color:#e8e8e8">
基于硬件的固定仲裁 256
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Hardware Fixed VC Arbitration 257
</td>
<td width="50%" style="background-color:#e8e8e8">
硬件固定虚通道仲裁 257
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Hardware-Fixed Port Arbitration 265
</td>
<td width="50%" style="background-color:#e8e8e8">
硬件固定端口仲裁 265
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Header Type 0 29
</td>
<td width="50%" style="background-color:#e8e8e8">
标头类型 0 29
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Header Type 1 28
</td>
<td width="50%" style="background-color:#e8e8e8">
标头类型 1 28
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Header Type/Format Field 178
</td>
<td width="50%" style="background-color:#e8e8e8">
标头类型/格式字段 178
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
High Speed Signaling 451
</td>
<td width="50%" style="background-color:#e8e8e8">
高速信令 451
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
host/PCI bridge 94
</td>
<td width="50%" style="background-color:#e8e8e8">
主机/PCI桥 94
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Hot Plug 847, 852
</td>
<td width="50%" style="background-color:#e8e8e8">
热插拔 847, 852
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Hot Plug Controller 863
</td>
<td width="50%" style="background-color:#e8e8e8">
热插拔控制器 863
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Hot Plug Elements 852
</td>
<td width="50%" style="background-color:#e8e8e8">
热插拔元素 852
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Hot Plug Messages 211
</td>
<td width="50%" style="background-color:#e8e8e8">
热插拔消息 211
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Hot Reset 839
</td>
<td width="50%" style="background-color:#e8e8e8">
热复位 839
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Hot Reset State 521, 612
</td>
<td width="50%" style="background-color:#e8e8e8">
热复位状态 521, 612
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Hot-Plug 116, 853
</td>
<td width="50%" style="background-color:#e8e8e8">
热插拔 116, 853
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Hot-Plug Controller 853, 864
</td>
<td width="50%" style="background-color:#e8e8e8">
热插拔控制器 853, 864
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
hot-plug primitives 874
</td>
<td width="50%" style="background-color:#e8e8e8">
热插拔原语 874
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Hot-Plug Service 852
</td>
<td width="50%" style="background-color:#e8e8e8">
热插拔服务 852
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Hot-Plug System Driver 852
</td>
<td width="50%" style="background-color:#e8e8e8">
热插拔系统驱动程序 852
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
HPC Applications 940
</td>
<td width="50%" style="background-color:#e8e8e8">
HPC 应用 940
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Hub Link 32
</td>
<td width="50%" style="background-color:#e8e8e8">
集线器链路 32
</td>
</tr>
</table>

## 20.105 I | 20.105 I

<table>
<tr>
<td width="50%">
ID Based Ordering 301
</td>
<td width="50%" style="background-color:#e8e8e8">
基于ID的排序 301
</td>
</tr>
<tr>
<td width="50%">
ID Routing 155
</td>
<td width="50%" style="background-color:#e8e8e8">
ID路由 155
</td>
</tr>
<tr>
<td width="50%">
ID-based Ordering 301, 909, 979
</td>
<td width="50%" style="background-color:#e8e8e8">
基于ID的排序 301, 909, 979
</td>
</tr>
<tr>
<td width="50%">
IDL 387
</td>
<td width="50%" style="background-color:#e8e8e8">
IDL 387
</td>
</tr>
<tr>
<td width="50%">
IDO 301, 302, 909, 979
</td>
<td width="50%" style="background-color:#e8e8e8">
IDO 301, 302, 909, 979
</td>
</tr>
<tr>
<td width="50%">
IEEE 1394 Bus Driver 711
</td>
<td width="50%" style="background-color:#e8e8e8">
IEEE 1394总线驱动 711
</td>
</tr>
<tr>
<td width="50%">
Ignored Messages 211
</td>
<td width="50%" style="background-color:#e8e8e8">
被忽略的消息 211
</td>
</tr>
<tr>
<td width="50%">
Implicit Routing 148, 979
</td>
<td width="50%" style="background-color:#e8e8e8">
隐式路由 148, 979
</td>
</tr>
<tr>
<td width="50%">
In-band Reset 837
</td>
<td width="50%" style="background-color:#e8e8e8">
带内复位 837
</td>
</tr>
<tr>
<td width="50%">
Infinite Credits 221
</td>
<td width="50%" style="background-color:#e8e8e8">
无限信用 221
</td>
</tr>
<tr>
<td width="50%">
Infinite Flow Control Credits 219
</td>
<td width="50%" style="background-color:#e8e8e8">
无限流控信用 219
</td>
</tr>
<tr>
<td width="50%">
Ingress Port 979
</td>
<td width="50%" style="background-color:#e8e8e8">
入口端口 979
</td>
</tr>
<tr>
<td width="50%">
InitFC1-Cpl 312
</td>
<td width="50%" style="background-color:#e8e8e8">
InitFC1-Cpl 312
</td>
</tr>
<tr>
<td width="50%">
InitFC1-NP 311
</td>
<td width="50%" style="background-color:#e8e8e8">
InitFC1-NP 311
</td>
</tr>
<tr>
<td width="50%">
InitFC1-P DLLP 311
</td>
<td width="50%" style="background-color:#e8e8e8">
InitFC1-P DLLP 311
</td>
</tr>
<tr>
<td width="50%">
InitFC2-Cpl 312
</td>
<td width="50%" style="background-color:#e8e8e8">
InitFC2-Cpl 312
</td>
</tr>
<tr>
<td width="50%">
InitFC2-NP 312
</td>
<td width="50%" style="background-color:#e8e8e8">
InitFC2-NP 312
</td>
</tr>
<tr>
<td width="50%">
InitFC2-P 312
</td>
<td width="50%" style="background-color:#e8e8e8">
InitFC2-P 312
</td>
</tr>
<tr>
<td width="50%">
Intelligent Adapters 943, 944, 951
</td>
<td width="50%" style="background-color:#e8e8e8">
智能适配器 943, 944, 951
</td>
</tr>
<tr>
<td width="50%">
Internal Error Reporting 911
</td>
<td width="50%" style="background-color:#e8e8e8">
内部错误报告 911
</td>
</tr>
<tr>
<td width="50%">
Interrupt Disable 803
</td>
<td width="50%" style="background-color:#e8e8e8">
中断禁用 803
</td>
</tr>
<tr>
<td width="50%">
Interrupt Latency 829
</td>
<td width="50%" style="background-color:#e8e8e8">
中断延迟 829
</td>
</tr>
<tr>
<td width="50%">
interrupt latency 829
</td>
<td width="50%" style="background-color:#e8e8e8">
中断延迟 829
</td>
</tr>
<tr>
<td width="50%">
Interrupt Line Register 802
</td>
<td width="50%" style="background-color:#e8e8e8">
中断线寄存器 802
</td>
</tr>
<tr>
<td width="50%">
Interrupt Pin Register 801
</td>
<td width="50%" style="background-color:#e8e8e8">
中断引脚寄存器 801
</td>
</tr>
<tr>
<td width="50%">
Interrupt Status 804
</td>
<td width="50%" style="background-color:#e8e8e8">
中断状态 804
</td>
</tr>
<tr>
<td width="50%">
Inter-symbol Interference 469
</td>
<td width="50%" style="background-color:#e8e8e8">
码间干扰 469
</td>
</tr>
<tr>
<td width="50%">
INTx Interrupt Messages 206
</td>
<td width="50%" style="background-color:#e8e8e8">
INTx中断消息 206
</td>
</tr>
<tr>
<td width="50%">
INTx Interrupt Signaling 206
</td>
<td width="50%" style="background-color:#e8e8e8">
INTx中断信令 206
</td>
</tr>
<tr>
<td width="50%">
INTx Message Format 807
</td>
<td width="50%" style="background-color:#e8e8e8">
INTx消息格式 807
</td>
</tr>
<tr>
<td width="50%">
INTx# Pins 800
</td>
<td width="50%" style="background-color:#e8e8e8">
INTx#引脚 800
</td>
</tr>
<tr>
<td width="50%">
INTx# Signaling 803
</td>
<td width="50%" style="background-color:#e8e8e8">
INTx#信令 803
</td>
</tr>
<tr>
<td width="50%">
IO 126
</td>
<td width="50%" style="background-color:#e8e8e8">
IO 126
</td>
</tr>
<tr>
<td width="50%">
IO Address Spaces 122
</td>
<td width="50%" style="background-color:#e8e8e8">
IO地址空间 122
</td>
</tr>
<tr>
<td width="50%">
IO Range 141
</td>
<td width="50%" style="background-color:#e8e8e8">
IO范围 141
</td>
</tr>
<tr>
<td width="50%">
IO Read 151
</td>
<td width="50%" style="background-color:#e8e8e8">
IO读 151
</td>
</tr>
<tr>
<td width="50%">
IO Requests 184
</td>
<td width="50%" style="background-color:#e8e8e8">
IO请求 184
</td>
</tr>
<tr>
<td width="50%">
IO Virtualization 937
</td>
<td width="50%" style="background-color:#e8e8e8">
IO虚拟化 937
</td>
</tr>
<tr>
<td width="50%">
IO Write 151
</td>
<td width="50%" style="background-color:#e8e8e8">
IO写 151
</td>
</tr>
<tr>
<td width="50%">
ISI 979
</td>
<td width="50%" style="background-color:#e8e8e8">
ISI 979
</td>
</tr>
<tr>
<td width="50%">
Isochronous Packets 279
</td>
<td width="50%" style="background-color:#e8e8e8">
等时包 279
</td>
</tr>
<tr>
<td width="50%">
Isochronous Support 272
</td>
<td width="50%" style="background-color:#e8e8e8">
等时支持 272
</td>
</tr>
<tr>
<td width="50%">
Isochronous Transaction Support 272
</td>
<td width="50%" style="background-color:#e8e8e8">
等时事务支持 272
</td>
</tr>
</table>

## 20.106 J | 20.106 J

<table>
<tr>
<td width="50%">
Jitter 485, 487
</td>
<td width="50%" style="background-color:#e8e8e8">
抖动 485, 487
</td>
</tr>
</table>

## 20.107 L | 20.107 L

<table>
<tr>
<td width="50%">
L0 State 500, 520, 568 L0s 744 L0s Receiver State Machine 605 L0s State 520, 603, 744 L0s Transmitter State Machine 603 L1 ASPM 736, 747 L1 ASPM Negotiation 748 L1 ASPM State 747 L1 State 520, 607, 760 L2 State 521, 609, 767 L2/L3 Ready 767 L2/L3 Ready state 763, 764 Lane 40, 78, 365, 979 Lane # 511 Lane Number Negotiation 543, 547 Lane Reversal 507 Lane-Level Encoding 410 Lane-to-Lane de-skew 78 Lane-to-Lane Skew 979 Last DW Byte Enables 178, 181 Latency Tolerance Reporting 910 LCRC 63, 325, 329 LeCroy 922, 923, 933 LeCroy Tools 917 Legacy Endpoint 816, 979 Legacy Endpoints 972 LFSR 980
</td>
<td width="50%" style="background-color:#e8e8e8">
L0 状态 500, 520, 568 L0s 744 L0s 接收器状态机 605 L0s 状态 520, 603, 744 L0s 发送器状态机 603 L1 ASPM 736, 747 L1 ASPM 协商 748 L1 ASPM 状态 747 L1 状态 520, 607, 760 L2 状态 521, 609, 767 L2/L3 就绪 767 L2/L3 就绪状态 763, 764 通道 40, 78, 365, 979 通道编号 511 通道编号协商 543, 547 通道反转 507 通道级编码 410 通道间去偏斜 78 通道间偏移 979 最后双字字节使能 178, 181 延迟容忍度报告 910 LCRC 63, 325, 329 LeCroy 922, 923, 933 LeCroy 工具 917 传统端点 816, 979 传统端点 972 LFSR 980
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Link 40, 980 Link # 511 Link Capabilities 2 Register 640 Link Capability Register 743 Link Configuration - Failed Lane 549 Link Control 841 Link Data Rate 509 Link data rate 78 Link Equalization 577 Link Errors 683 Link Flow Control-Related Errors 666 Link Number Negotiation 542, 546 Link Power Management 733 Link Status Register 641 Link Training and Initialization 78 Link Training and Status State Machine (LTSSM) 518 Link Upconfigure Capability 512 Link Width 507 Link width 78 Link Width Change 570 Link Width Change Example 630 Lock 964 Locked Reads 66 Locked Transaction 209
</td>
<td width="50%" style="background-color:#e8e8e8">
链路 40, 980 链路编号 511 链路能力 2 寄存器 640 链路能力寄存器 743 链路配置 - 失败的通道 549 链路控制 841 链路数据速率 509 链路数据速率 78 链路均衡 577 链路错误 683 链路流控相关错误 666 链路编号协商 542, 546 链路电源管理 733 链路状态寄存器 641 链路训练和初始化 78 链路训练和状态状态机 (LTSSM) 518 链路升级配置能力 512 链路宽度 507 链路宽度 78 链路宽度变化 570 链路宽度变化示例 630 锁定 964 锁定读 66 锁定事务 209
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Locked Transactions 963 Logic Analyzer 921 Logical Idle Sequence 370 Loopback Master 615 Loopback Slave 616 Loopback State 521, 613 Loopback.Active 617 Loopback.Entry 614 Loopback.Exit 618 Low-priority VC Arbitration 255 LTR 784, 910, 980 LTR Messages 786 LTR Registers 784 LTSSM 507, 518, 839, 927, 980
</td>
<td width="50%" style="background-color:#e8e8e8">
锁定事务 963 逻辑分析仪 921 逻辑空闲序列 370 回环主设备 615 回环从设备 616 回环状态 521, 613 回环.激活 617 回环.进入 614 回环.退出 618 低优先级 VC 仲裁 255 LTR 784, 910, 980 LTR 消息 786 LTR 寄存器 784 LTSSM 507, 518, 839, 927, 980
</td>
</tr>
</table>

## 20.108 M | 20.108 M

<table>
<tr>
<td width="50%">
Malformed TLP 666
</td>
<td width="50%" style="background-color:#e8e8e8">
畸形TLP 666
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Memory Address Space 122
</td>
<td width="50%" style="background-color:#e8e8e8">
存储器地址空间 122
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Memory Read 150
</td>
<td width="50%" style="background-color:#e8e8e8">
存储器读 150
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Memory Read Lock 150
</td>
<td width="50%" style="background-color:#e8e8e8">
存储器读锁定 150
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Memory Request Packet 188
</td>
<td width="50%" style="background-color:#e8e8e8">
存储器请求报文 188
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Memory Requests 188
</td>
<td width="50%" style="background-color:#e8e8e8">
存储器请求 188
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Memory Write 150
</td>
<td width="50%" style="background-color:#e8e8e8">
存储器写 150
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Memory Writes 69
</td>
<td width="50%" style="background-color:#e8e8e8">
存储器写 69
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Message 151
</td>
<td width="50%" style="background-color:#e8e8e8">
消息 151
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Message Address Register 816
</td>
<td width="50%" style="background-color:#e8e8e8">
消息地址寄存器 816
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Message Address register 816, 818
</td>
<td width="50%" style="background-color:#e8e8e8">
消息地址寄存器 816, 818
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Message Control Register 814
</td>
<td width="50%" style="background-color:#e8e8e8">
消息控制寄存器 814
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Message Control register 814, 818
</td>
<td width="50%" style="background-color:#e8e8e8">
消息控制寄存器 814, 818
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Message Data register 817, 818
</td>
<td width="50%" style="background-color:#e8e8e8">
消息数据寄存器 817, 818
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Message Request Packet 203
</td>
<td width="50%" style="background-color:#e8e8e8">
消息请求报文 203
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Message Requests 70, 203
</td>
<td width="50%" style="background-color:#e8e8e8">
消息请求 70, 203
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Message Writes 70
</td>
<td width="50%" style="background-color:#e8e8e8">
消息写 70
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Messages 148
</td>
<td width="50%" style="background-color:#e8e8e8">
消息 148
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Mid-Bus Probe 923
</td>
<td width="50%" style="background-color:#e8e8e8">
总线中间探测 923
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
MindShare Arbor 117
</td>
<td width="50%" style="background-color:#e8e8e8">
MindShare Arbor 117
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Miniport Driver 706
</td>
<td width="50%" style="background-color:#e8e8e8">
微型端口驱动 706
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
MMIO 123
</td>
<td width="50%" style="background-color:#e8e8e8">
MMIO 123
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Modified Compliance Pattern 537
</td>
<td width="50%" style="background-color:#e8e8e8">
修改的一致性测试码型 537
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Modified Compliance Pattern - 8b/10b 532
</td>
<td width="50%" style="background-color:#e8e8e8">
修改的一致性测试码型 - 8b/10b 532
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
MR-IOV 937, 939
</td>
<td width="50%" style="background-color:#e8e8e8">
MR-IOV 937, 939
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
MSI Capability Register 812
</td>
<td width="50%" style="background-color:#e8e8e8">
MSI能力寄存器 812
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
MSI Configuration 817
</td>
<td width="50%" style="background-color:#e8e8e8">
MSI配置 817
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Multicast 893, 896
</td>
<td width="50%" style="background-color:#e8e8e8">
多播 893, 896
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Multicast Capabilities 163
</td>
<td width="50%" style="background-color:#e8e8e8">
多播能力 163
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Multicast Capability Registers 889
</td>
<td width="50%" style="background-color:#e8e8e8">
多播能力寄存器 889
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Multi-casting 888
</td>
<td width="50%" style="background-color:#e8e8e8">
多播 888
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Multi-Function Arbitration 272
</td>
<td width="50%" style="background-color:#e8e8e8">
多功能仲裁 272
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Multi-Host System 96
</td>
<td width="50%" style="background-color:#e8e8e8">
多主机系统 96
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Multi-Host Systems 943
</td>
<td width="50%" style="background-color:#e8e8e8">
多主机系统 943
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Multiple Message Capable field 818
</td>
<td width="50%" style="background-color:#e8e8e8">
Multiple Message Capable字段 818
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Multiple Messages 820
</td>
<td width="50%" style="background-color:#e8e8e8">
多消息 820
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Multi-Root 938
</td>
<td width="50%" style="background-color:#e8e8e8">
多根 938
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Multi-Root Enumeration 114
</td>
<td width="50%" style="background-color:#e8e8e8">
多根枚举 114
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Multi-Root System 97, 116
</td>
<td width="50%" style="background-color:#e8e8e8">
多根系统 97, 116
</td>
</tr>
</table>