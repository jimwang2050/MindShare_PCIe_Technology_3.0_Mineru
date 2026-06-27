# Ch18_Optional_Features

| EN | ZH |
|----|----|
| ## Configuration Improvements | ## 配置改进 |
| A few configuration registers were added to improve software visibility and control of devices. | 添加了一些配置寄存器，以改善软件对设备的可见性和控制。 |

## Internal Error Reporting

| EN | ZH |
| --- | --- |
| This is intended to provide a standardized way of reporting internal problems for devices like switches that don't have a driver to handle that for them. | 这旨在为那些没有驱动程序来处理内部问题的设备（如交换机）提供一种标准化的内部问题报告方式。 |
| It also adds the capability to track multiple TLP headers when they result in errors instead of just one as before. | 它还增加了跟踪多个TLP报头的能力（当它们导致错误时），而不是像以前那样只跟踪一个。 |
| This topic is covered in the section on errors called "Internal Errors" on page 667. | 此主题在第667页名为"Internal Errors"的错误部分中介绍。 |

## Resizable BARs / 可调整大小的 BAR

| EN | ZH |
|---|---|
| This new set of extended configuration registers allows devices that use a large amount of local memory to report whether they can work with smaller amounts and, if so, what sizes are acceptable. Software that knows to look for them can find the new registers, shown in Figure 20‐20 on page 912, and program them to give the appropriate memory size for the platform based on the competing requirements of system memory and other devices. | 这组新的扩展配置寄存器使得使用大量本地内存的设备能够报告它们是否可以使用较小的内存量，如果可以，哪些大小是可接受的。知道查找这些寄存器的软件可以找到这些新寄存器（如图 20‐20 第 912 页所示），并根据系统内存和其他设备之间的竞争需求对它们进行编程，以给出适合平台的内存大小。 |
| A few rules apply to the use of these registers: | 这些寄存器的使用遵循几条规则： |
| 1. To avoid confusion, a BAR size should only be changed when the Memory Enable bit has been cleared in the Command register. | 1. 为避免混淆，BAR 大小只应在命令寄存器中的存储器使能位被清除时更改。 |
| 2. The spec strongly recommends that Functions not advertise BARs that are bigger than they can effectively use. | 2. 规范强烈建议函数不应通告大于其有效使用范围的 BAR。 |
| 3. To ensure optimal performance, software should allocate the biggest BAR size that will work for the system. | 3. 为确保最佳性能，软件应分配对系统可行的最大 BAR 大小。 |

Figure 20‐20: Resizable BAR Registers / 图 20‐20：可调整大小的 BAR 寄存器 | 图20‐20：可调整大小的 BAR 寄存器

<img src="images/part06_f0802c9e5a80c315ef54b4caefb39a2552c55b3cf7a7f428e1977f37004f5d6a.jpg" width="700" alt="">

## Capability Register / 能力寄存器

| EN | ZH |
|---|---|
| This register simply reports which BAR sizes will work for this Function. Bits 4 to 23 are used for this and the values are as shown here: | 该寄存器仅报告哪些 BAR 大小适用于该功能。位 4 到位 23 用于此目的，其值如下所示： |
| • Bit 4 - 1MB BAR size will work for this Function | • 位 4 - 1MB BAR 大小适用于该功能 |
| • Bit 5 - 2MB | • 位 5 - 2MB |
| • Bit 6 - 4MB | • 位 6 - 4MB |
| • Bit 23 - 512GB will work for this Function | • 位 23 - 512GB 适用于该功能 |

Figure 20-21: Resizable BAR Capability Register | 图20-21：可调整大小BAR能力寄存器
<img src="images/part06_c42c2330033239a0ab8e4131f5ec10ec912e7e512606e0753c7b7d128ee7a071.jpg" width="700" alt="">

## Control Register

| EN | ZH |
| --- | --- |
| The BAR Index field in this register reports to which BAR this size refers (0 to 5 are possible). The Number of Resizable BARs field is only defined for Control Register zero and is reserved for all the others. It tells how many of the six possible BARs actually have an adjustable size. Finally, the BAR Size field is programmed by software to specify the desired size the BAR indicated by the BAR Index field (0 = 1MB, 1=2MB, 2=4MB, ..., 19=512GB). | 该寄存器中的BAR Index字段指示此大小对应于哪个BAR（可取0到5）。Number of Resizable BARs字段仅为控制寄存器0定义，其余寄存器保留。它指示六个可能的BAR中有多少个实际具有可调整大小。最后，BAR Size字段由软件编程，以指定BAR Index字段所指示的BAR的期望大小（0=1MB，1=2MB，2=4MB，...，19=512GB）。 |

Figure 20‐22: Resizable BAR Control Register | 图20‐22：可调整大小BAR控制寄存器  
<img src="images/part06_42bf9a29173342c26de98486d6e42bd79800d8d24142e1b7d08dbf44d33b0d18.jpg" width="700" alt="">

| EN | ZH |
| --- | --- |
| Once the Resizable values have been programmed, then enumeration software will be able to work as it normally does: writing all F's to each BAR and reading it back will report the size that was selected. Note that if the size value is changed, the contents of the BAR will be lost and will need to reprogrammed if it was previously set up. Figure 20‐23 on page 914 highlights the BAR registers in the configuration header space for a Type 0 header. | 一旦可调整大小值被编程后，枚举软件就能像往常一样工作：向每个BAR写入全F并回读将报告所选择的大小。注意，如果修改了大小值，BAR的内容将丢失，如果之前已设置好，则需要重新编程。第914页的图20-23展示了类型0配置头空间中的BAR寄存器。 |

Figure 20‐23: BARs in a Type0 Configuration Header | 图20‐23：Type0配置头中的BAR  
<img src="images/part06_bf5642ad8ee7bab529f8d109c732bdbc9185d3392acba41074c0bbe132d75e17.jpg" width="700" alt="">

| EN | ZH |
|---|---|
| ## Simplified Ordering Table | ## 简化排序表 |
| This change simplifies the Transaction Ordering Table by reducing the number of entries in the table. Essentially, it no longer distinguishes between completions for reads or completions for non‑posted writes. The motivation for this was to reduce the number of cases that needed to be tested. For more on this, see the section called "The Simplified Ordering Rules Table" on page 288. | 此更改通过减少表中的条目数量简化了事务排序表。本质上，它不再区分针对读取的完成报文和针对非发布写入的完成报文。这样做的动机是为了减少需要测试的情形数量。更多信息请参见第288页的"简化排序规则表"一节。 |
| Appendices | 附录 |

| EN | ZH |
|---|---|
| # Appendix A: | # 附录 A： |

| EN | ZH |
|---|---|
| # Debugging PCIe Traffic with LeCroy Tools | # 使用LeCroy工具调试PCIe流量 |
| Christoper Webb, LeCroy Corporation | Christoper Webb, LeCroy Corporation |

| EN | ZH |
|---|---|
| ## Overview | ## 概述 |
| The transition of IO bus architecture from PCI to PCI Express had a large impact on developers with respect to types of tools required for validation and debug. | IO总线架构从PCI到PCI Express的过渡，对开发人员在验证和调试所需工具类型方面产生了重大影响。 |
| With parallel buses such as PCI, a waveform view of the signals shows enough information for the developer to interpret the state of the bus. A user could visually examine a waveform and mentally decode the type of transactions, how much data is transferred, and even the content of that transfer. | 对于PCI这样的并行总线，信号的波形视图可为开发人员提供足够的信息来解释总线状态。用户可以直观地检查波形，在脑中解码出事务类型、传输的数据量，甚至传输的内容。 |
| Since PCI Express packet traffic is both encoded and scrambled, examining a waveform view of the traffic provides very little information about the state of the link. The speed of the link can be inferred from the width of the bit times, and the width of the link can be inferred by the number of active lanes. However, the user cannot visually interpret the symbol alignment, let alone the packets themselves. | 由于PCI Express包流量既经过编码又经过加扰，检查流量的波形视图几乎无法提供有关链路状态的信息。链路的速率可以从位时间的宽度推断，链路的宽度可以从活动通道的数量推断。然而，用户无法直观地解读符号对齐，更不用说数据包本身了。 |
| A new class of tools evolved to help developers visualize the state of their now serial links. These tools perform the de‑serialization, decoding, and de‑scrambling for the users. At first glance this would seem to be enough for the developer. But for PCI Express specifically, other complications such as flow control credits, lane‑to‑lane skew, polarity inversion, and lane reversal must also be comprehended by these tools as part of understanding PCIe protocol. | 一类新工具应运而生，帮助开发人员可视化其串行链路的状态。这些工具为用户执行解串、解码和解扰。乍一看，这对开发人员来说似乎足够了。但具体到PCI Express，这些工具还必须理解流控信用、通道间偏移、极性反转和通道反转等其他复杂问题，作为理解PCIe协议的一部分。 |
| Both pre‑ and post‑silicon debug share a common need for tools. In this appen dix chapter, we describe some of the product offerings available for debugging PCI Express interconnects, both from a pre and post silicon perspective. | 硅前和硅后调试对工具有着共同的需求。在本附录章节中，我们将从硅前和硅后两个角度介绍一些可用于调试PCI Express互连的产品。 |

| EN | ZH |
|---|---|
| ## Pre-silicon Debugging | ## 硅前调试 |

## RTL Simulation Perspective

| EN | ZH |
|---|---|
| In RTL simulation, looking at a waveform view of an FPGA or an ASIC signal is the most common way to debug. By showing internal state machine states, monitoring IO as it moves through the device, or seeing the state of control signals; a waveform view is quite powerful. But, as we discussed above, a PCI express link is not understandable when shown as a waveform. Additional processing or decoding must be done to make sense of this new link. To augment the simulation tools, a PCI Express Bus Monitor is typically added to address this need. | 在RTL仿真中，查看FPGA或ASIC信号的波形视图是最常见的调试方式。通过显示内部状态机状态、监测IO在器件中的移动过程，或观察控制信号的状态，波形视图非常强大。但如前所述，PCI Express链路以波形形式呈现时是无法理解的。必须进行额外的处理或解码才能理解这种新型链路。为增强仿真工具的能力，通常会添加一个PCI Express总线监视器来满足这一需求。 |

## PCI Express RTL Bus Monitor

| EN | ZH |
|---|---|
| A PCI Express Bus monitor is a piece of code which users insert in their RTL simulation to help monitor the state of their PCIe link. At minimum, this monitor will output text based log files with information about link state changes and types of packet activity. More complex monitors will perform real time compliance checking. A number of vendors provide purchasable IP which perform this exact function. The emphasis however is typically on compliance. Less functionality is provided with respect to visualization of things such as flow control credits, link utilization, or link training debug. | PCI Express 总线监视器是一段用户插入其 RTL 仿真中的代码，用于帮助监视其 PCIe 链路的状态。该监视器至少会输出基于文本的日志文件，其中包含关于链路状态变化和报文活动类型的信息。更复杂的监视器会执行实时一致性检查。多家供应商提供可购买的 IP 来实现此功能。然而，其重点通常在于一致性检查。在流控信用量、链路利用率或链路训练调试等可视化方面提供的功能较少。 |

## RTL vector export to PETracer Application

| EN | ZH |
|---|---|
| LeCroy has partnered with a number of the leading PCIe verification IP vendors to create tools to further enhance the visualization and analysis of pre‑silicon PCIe traffic. This involves using the vendors Bus Monitor to export raw symbol traffic into the same PETracer application used by the dedicated PCIe Analyzer hardware. SimPASS PE is LeCroy's solution to supporting this export. | LeCroy 与多家领先的 PCIe 验证 IP 供应商合作，开发了相关工具，以进一步增强硅前 PCIe 流量的可视化和分析能力。这一过程利用供应商的总线监视器（Bus Monitor）将原始符号流量导出到与专用 PCIe 分析仪硬件相同的 PETracer 应用程序中。SimPASS PE 是 LeCroy 支持此导出的解决方案。 |
| More information about LeCroy's PETracer application and its features are described in the section "As a last resort, a flying lead probe shown in Figure 5 on page 924 may be used to attach the protocol analyzer to the system under test. This involves soldering a resistive tap circuit and connector pins to the PCIe traces. This circuitry is typically soldered to the AC coupling caps of the PCIe link as they are often the only place to access the traces. Once the probe circuitry is soldered to the PCB, the analyzer probe can be connected and removed as needed. This approach can be used on virtually any PCIe link, however the robustness of the connection is limited by the skill of the technician adding the probe." on page 924. | 有关 LeCroy 的 PETracer 应用程序及其功能的更多信息，请参见第 924 页关于"作为最后的手段，可使用图 5 所示的飞线探头将协议分析仪连接到被测系统。这需要将电阻抽头电路和连接器引脚焊接到 PCIe 走线上。该电路通常焊接到 PCIe 链路的交流耦合电容上，因为这些电容往往是唯一可以接触到走线的地方。一旦探头电路焊接到 PCB 上，分析仪探头便可根据需要连接和移除。该方法几乎可用于任何 PCIe 链路，但连接的牢固程度受限于添加探头之技术人员的技术水平。"的章节。 |

| EN | ZH |
|----|----|
| ## Post-Silicon Debug | ## 硅后调试 |

| EN | ZH |
|---|---|
| ## Oscilloscope | ## 示波器 |
| Use of an oscilloscope for debugging a PCIe link is typically focused on the electrical validation of the link. The most common usage is examining an eye pattern with a mask overlay for determining electrical compliance. A lesser known compliance check is to examine the entry and exit of electrical idle state to see if the link goes to the common mode voltage within the required time periods after an electrical idle ordered set is transmitted. These are 2 examples of PCIe compliance checking which are best performed using an oscilloscope such as shown in Figure 1 on page 920. | 使用示波器调试 PCIe 链路通常侧重于链路的电气验证。最常见的用途是检查带有模板覆盖的眼图以确定电气合规性。一个不太为人知的合规性检查是检查电气空闲状态的进入和退出，以查看链路在传输电气空闲有序集后是否在规定时间内达到共模电压。这是 PCIe 合规性检查的两个示例，最好使用示波器（如第 920 页图 1 所示）来执行。 |
| With the addition of dynamic link training for 8.0 GT/s operation, devices must now train the transmitter emphasis during the Recovery.EQ LTSSM sub‐state. The goal is to set the transmitter EQ to provide the best signal eye to the receiver. Monitoring this dynamic equalization process is another example where the use of an oscilloscope is quite powerful. With a real time oscilloscope, the user can capture this process and see the impact on the waveform as transmitter settings are changed. This allows the user to verify that the transmitter is indeed acting on the coefficient change requests, but it also allows the user to determine if the receiver has properly chosen the correct setting. | 随着 8.0 GT/s 操作引入动态链路训练，器件现在必须在 Recovery.EQ LTSSM 子状态期间训练发送器均衡。目标是设置发送器 EQ 以向接收器提供最佳信号眼图。监控此动态均衡过程是使用示波器非常强大的另一个例子。使用实时示波器，用户可以捕获此过程并查看随着发送器设置更改而对波形的影响。这允许用户验证发送器确实正在响应系数更改请求，同时也允许用户确定接收器是否正确选择了正确的设置。 |
| For logical debug of the link, the oscilloscope is most useful when the link is x1 or x2 as you are limited by the number channels the scope can acquire. The first method of examining PCIe traffic is a waveform view. As with the RTL waveform viewer, there is little to understand about the state of the link without SW help to perform 8b/10b decoding and de‐scrambling. Fortunately, more advanced oscilloscopes have SW packages that perform these duties. For this to work properly, the scope must have deep capture buffers and must see the SKIP ordered sets so that they can decipher the byte alignment and synchronize the de‐scrambler LFSR. | 对于链路的逻辑调试，当链路为 x1 或 x2 时示波器最为有用，因为您受限于示波器可获取的通道数量。检查 PCIe 流量的第一种方法是波形视图。与 RTL 波形查看器一样，如果没有软件帮助执行 8b/10b 解码和解扰，则很难了解链路的状态。幸运的是，更高级的示波器具有执行这些任务的软件包。为了使其正常工作，示波器必须具有深度的捕获缓冲区，并且必须看到 SKIP 有序集，以便它们能够解读字节对齐并同步解扰器 LFSR。 |
| The LeCroy Oscilloscope can overlay PCIe symbols right onto the waveform for enhanced visibility of the traffic. An additional text based listing of the packet symbols can be displayed on the screen as an additional method of examining the waveform. | LeCroy 示波器可以将 PCIe 符号直接叠加在波形上，以提高流量的可视性。额外的基于文本的包符号列表可以显示在屏幕上，作为检查波形的另一种方法。 |
| LeCroy recently announced a SW package called ProtoSync for their oscilloscope line which allows the user to export the captured waveform into the PETracer application. This is the same SW package that the protocol analyzer uses which includes a wide range of post processing capabilities described below. The PETracer software can run independently on the scope hardware, often on a second monitor. This allows time correlated comparison of the physical layer data presented by the scope waveform alongside the logic layer presentation of data presented by the PETracer software. | LeCroy 最近为其示波器产品线宣布了一个名为 ProtoSync 的软件包，允许用户将捕获的波形导出到 PETracer 应用程序中。这与协议分析器使用的软件包相同，包括下面描述的各种后处理功能。PETracer 软件可以独立运行在示波器硬件上，通常在第二个显示器上运行。这允许将示波器波形呈现的物理层数据与 PETracer 软件呈现的逻辑层数据进行时间相关比较。 |
| Capture of the 8.0 GT/s dynamic link equalization on the oscilloscope and exporting this traffic to the PETracer application is a prime example where this solution is most powerful. The user can navigate PETracer to the link training packet where the TX coefficient change request has been sent, then identify where this coefficient change was applied in the scope SW. The user can then measure the time it takes for the coefficient change to be applied and compare this to the timing required in the PCIe spec. | 在示波器上捕获 8.0 GT/s 动态链路均衡并将此流量导出到 PETracer 应用程序是该方案最强大的典型示例。用户可以导航 PETracer 到已发送 TX 系数更改请求的链路训练包，然后识别在示波器软件中应用此系数更改的位置。然后用户可以测量应用系数更改所需的时间，并将其与 PCIe 规范中要求的时序进行比较。 |

Figure A‐1: LeCroy Oscilloscope with ProtoSync Software Option | 图A‐1：带ProtoSync软件选项的LeCroy示波器

<img src="images/part06_29c03ac8ed87bcc30aa8073ee4d78d555bd2904b6b29b0695d925e5c28e279d5.jpg" width="700" alt="">

## Protocol Analyzer

| EN | ZH |
|---|---|
| A growing trend in debugging PCIe links is to use a dedicated protocol analysis tool. What separates a protocol analyzer from a logic analyzer is that it is built to support a specific protocol such as PCIe. From a hardware perspective, a PCIe protocol analyzer is optimized for acquiring and storing PCIe traffic. This starts from the dedicated PCIe interposer probes, continues to the cabling choice, and carries through into the internal hardware components. For recovering PCIe traffic, specialized clock and data recovery circuits are used which can handle the electrical idle transitions, spread spectrum modulation, as well as handle the run lengths found in 128b/130b encoding. Sophisticated equalization circuits are used to recover the signal eye prior to deserialization. Without comprehending the complexities of PCIe recovery, the Analyzer hardware would not be optimized for recovering complex traffic such as speed switching, dynamic link widths, and low power states such as L0s. | 调试PCIe链路的一个日益增长的趋势是使用专用的协议分析工具。协议分析仪与逻辑分析仪的区别在于，它是为支持特定协议（如PCIe）而构建的。从硬件角度看，PCIe协议分析仪针对采集和存储PCIe流量进行了优化。这从专用的PCIe中介层探针开始，延续到线缆选择，并贯穿到内部硬件组件。为恢复PCIe流量，使用了专门的时钟与数据恢复电路，这些电路能够处理电气空闲转换、扩频调制，以及128b/130b编码中的游程长度。在解串之前，采用精密的均衡电路来恢复信号眼图。如果不理解PCIe恢复的复杂性，分析仪硬件就无法针对恢复复杂流量（如速率切换、动态链路宽度以及L0s等低功耗状态）进行优化。 |
| In addition to choosing appropriate hardware components for recovering PCIe traffic, a protocol analyzer includes logic circuitry which is PCIe specific. This logic must infer the state of the PCIe link and follow it during various LTSSM state changes. Once the link state is being properly followed, dedicated packet inspection circuits perform data matching against incoming packets to look for events programmed by the user. These matchers are used for filtering of traffic as well as performing the trigger functionality needed for stopping the traffic capture. A mixture of these traffic filters as well as deep trace buffers (often 4GB to 8GB in size) allow the user to capture significantly longer traffic scenarios than would be possible without a protocol analyzer. | 除了选择合适的硬件组件来恢复PCIe流量外，协议分析仪还包含PCIe专用的逻辑电路。这些逻辑必须推断PCIe链路的状态，并在各种LTSSM状态变化期间跟踪该状态。一旦正确跟踪了链路状态，专用的报文检测电路就会对传入的报文执行数据匹配，以查找用户编程的事件。这些匹配器用于流量过滤以及执行停止流量捕获所需的触发功能。这些流量过滤器与深度追踪缓冲区（通常为4GB至8GB）的结合，使用户能够捕获比没有协议分析仪时长得多的流量场景。 |
| Finally, the most important piece of a protocol analyzer is the software GUI. By optimizing the traffic views, post processing reports, and hardware controls with a dedicated PCI Express software tool; a very comprehensive set of PCI express specific analysis can be performed. | 最后，协议分析仪最重要的部分是软件GUI。通过使用专用的PCI Express软件工具优化流量视图、后处理报告和硬件控制，可以执行非常全面的PCI Express特定分析。 |

## Logic Analyzer

| EN | ZH |
|---|---|
| Some logic analyzers offer PCIe specific software packages. | 某些逻辑分析仪提供专用于 PCIe 的软件包。 |
| This software will read the PCI express capture from the logic analyzer hardware and perform some amount of post processing of this data. | 该软件从逻辑分析仪硬件读取 PCI Express 捕获数据，并对这些数据执行一定量的后处理。 |
| This analysis includes the basics such as decoding, de-scrambling, and decoding of the traffic. | 这种分析包括基本功能，例如解码、解扰以及对流量进行解码。 |
| These SW tools do not perform many of the rich post processing features offered by dedicated protocol analyzer software, however. | 然而，这些软件工具无法执行专用协议分析仪软件所提供的许多丰富的后处理功能。 |

## Using a Protocol Analyzer Probing Option / 使用协议分析仪探测选项

| EN | ZH |
|---|---|
| To record your PCIe traffic you must first find the best method for probing it. PCIe started as an add-in card form factor for desktop PC's and servers, but has since proliferated into a dizzying array of standard and non-standard form factors. For the standard form factors, the best probe option is a dedicated interposer. | 要记录您的PCIe流量，必须首先找到最佳的探测方法。PCIe最初以台式PC和服务器的插件卡形式出现，但此后已扩展到令人眼花缭乱的各种标准和非标准外形规格。对于标准外形规格，最佳探测选项是专用内插器。 |
| An Interposer is a dedicated piece of hardware which includes probe circuitry required for passing a copy of the PCIe traffic to the Analyzer hardware for capture and analysis. These interposers are designed specifically for the mechanical and electrical environments for which they are placed. The most common interposer is a "Slot Interposer" such as shown in Figure 2 on page 922. This interposer is used for probing standard CEM compliant PCIe add-in cards. | 内插器是一种专用硬件，其中包含探测电路，用于将PCIe流量的副本传递到分析仪硬件进行捕获和分析。这些内插器针对其所处的机械和电气环境专门设计。最常见的内插器是"插槽内插器"，如第922页图2所示。该内插器用于探测符合CEM标准的标准PCIe插件卡。 |
| Care should be taken when selecting an interposer as the probe circuitry varies by vendor and by requirements imposed by the max PCIe link speed. For example, a Gen3 slot interposer should contain probe circuitry which allows the dynamic link training process to pass properly through the probe. The LeCroy Gen3 slot interposer uses linear circuits to maintain the shape of the waveform as it passes through the probe. This allows pre-emphasis of the transmitter to be dynamically changed during link training while allowing the receiver to quantify the impact of a new setting (either positive or negative impact). | 选择内插器时应谨慎，因为探测电路因供应商以及最大PCIe链路速度所施加的要求而异。例如，Gen3插槽内插器应包含允许动态链路训练过程正常通过探测器的探测电路。LeCroy Gen3插槽内插器使用线性电路来保持波形通过探测器时的形状。这使得发送器的预加重可以在链路训练期间动态改变，同时允许接收器量化新设置的影响（正面或负面影响）。 |

Figure A-2: LeCroy PCI Express Slot Interposer x16 | 图A-2：LeCroy PCI Express插槽内插板x16
<img src="images/part06_a824c247f5e1832ba1a0dbda8bbb952b76f4d98b36a17a519855edf0c26c7b6b.jpg" width="700" alt="">

| EN | ZH |
|---|---|
| LeCroy also offers a family of other dedicated interposers for form factors such as ExpressCard, XMC, Mini Card, Express Module, AMC, etc. Some of these interposers are shown in Figure 3 on page 923. For a complete list of these interposers please refer to the LeCroy website: www.lecroy.com as this list is constantly growing. | LeCroy还提供一系列其他专用内插器，适用于ExpressCard、XMC、Mini Card、Express Module、AMC等外形规格。其中一些内插器如第923页图3所示。有关这些内插器的完整列表，请参阅LeCroy网站：www.lecroy.com，因为该列表在不断增长。 |

Figure A-3: LeCroy XMC, AMC, and Mini Card Interposers | 图A-3：LeCroy XMC、AMC和Mini Card内插板
<img src="images/part06_3f1f3177d7c3580d03ba2a269ede7721fdde0649868789d2a6b3c7a14db806fc.jpg" width="700" alt="">

| EN | ZH |
|---|---|
| For debugging PCIe links which cannot benefit from a dedicated interposer, a mid-bus probe shown in Figure 4 on page 923 is the next best option. A mid-bus probe involves placement of an industry standard probe geometry on the PCB. Each PCIe lane is routed to a pair of pads on the footprint which can be probed using a mid-bus probe head. These probes use spring pins or C clips for providing solder free mechanical attachment between the system under test and the protocol analyzer. | 对于无法使用专用内插器进行调试的PCIe链路，第923页图4所示的中总线探测器是次优选择。中总线探测器涉及在PCB上放置工业标准的探测几何图形。每条PCIe通道被路由到焊盘图案上的一对焊盘，可使用中总线探测头进行探测。这些探测器使用弹簧针或C型夹来提供待测系统与协议分析仪之间的免焊接机械连接。 |

Figure A-4: LeCroy PCI Express Gen3 Mid-Bus Probe | 图A-4：LeCroy PCI Express Gen3总线中间探头
<img src="images/part06_aed82c2e0e0bf42268178501d60cb2b67f960d5425e46a46c4614d4e07e33693.jpg" width="700" alt="">

| EN | ZH |
|---|---|
| As a last resort, a flying lead probe shown in Figure 5 on page 924 may be used to attach the protocol analyzer to the system under test. This involves soldering a resistive tap circuit and connector pins to the PCIe traces. This circuitry is typically soldered to the AC coupling caps of the PCIe link as they are often the only place to access the traces. Once the probe circuitry is soldered to the PCB, the analyzer probe can be connected and removed as needed. This approach can be used on virtually any PCIe link, however the robustness of the connection is limited by the skill of the technician adding the probe. | 作为最后手段，可使用第924页图5所示的飞线探测器将协议分析仪连接到待测系统。这涉及将电阻抽头电路和连接器引脚焊接到PCIe走线上。该电路通常焊接到PCIe链路的交流耦合电容上，因为这些电容通常是唯一可以接触到走线的地方。一旦探测电路焊接到PCB上，分析仪探头即可根据需要连接和移除。这种方法几乎可用于任何PCIe链路，但连接的可靠性受限于添加探测器的技术人员的技能。 |

Figure A-5: LeCroy PCI Express Gen2 Flying Lead Probe | 图A-5：LeCroy PCI Express Gen2飞线探头
<img src="images/part06_e0acc98dd94fc30917b013f3fa880ff6d4fe74690d210017a30826eba95c6b7b.jpg" width="700" alt="">

| EN | ZH |
|---|---|
| ## Viewing Traffic Using the PETracer Application | ## 使用 PETracer 应用程序查看流量 |

| EN | ZH |
|---|---|
| The primary way to view PCI Express traffic with the LeCroy PETracer application is the CATC Trace view. This view takes each recorded packet and breaks it down into different packet fields to highlight the important values contained in this packet. A mixture of colors and text are used to visually categorize and explain the purpose of each packet. Errors are highlighted in red such as shown in Figure 6 on page 925. Warnings are highlighted in yellow making it easy to identify areas of traffic or fields in a packet which are non‑compliant. | 使用LeCroy PETracer应用程序查看PCI Express流量的主要方式就是CATC Trace视图。该视图获取每个记录的报文，并将其分解为不同的报文字段，以突出显示该报文中包含的重要值。它混合使用颜色和文本来直观地对每个报文进行分类并解释其用途。错误以红色高亮显示，如第925页图6所示。警告以黄色高亮显示，便于识别流量区域或报文中不符合规范的字段。 |

Figure A-6: TLP Packet with ECRC Error | 图A-6：含ECRC错误的TLP数据包  
<img src="images/part06_f3e8b4f925f7ce5f9643abfcc72742fb65a76e3ab12cb80a2a8c566723277857.jpg" width="700" alt="">

| EN | ZH |
|---|---|
| In addition to decoding and visually breaking down each packet, a hierarchical display allows logical grouping of related packets. For example, in "Link Level" mode, TLP packets are grouped with their respective ACK packet. Each TLP is identified as either implicitly or explicitly ACK'd or NAK'd. An example of a ACK DLLP is shown in Figure 7 on page 925 along with the ACK'd TLP. | 除了解码和直观分解每个报文外，分层显示还可以对相关报文进行逻辑分组。例如，在"Link Level"模式下，TLP报文与其对应的ACK报文分组在一起。每个TLP被标识为隐式或显式ACK'd或NAK'd。第925页图7显示了一个ACK DLLP及其对应的ACK'd TLP的示例。 |

Figure A-7: "Link Level" Groups TLP Packets with their Link Layer Response | 图A-7："链路级别"将TLP数据包与其链路层响应分组  
<img src="images/part06_43b8b3cb9fa74ebf5301ea58b79b5983ba93e4ba6f20884125f2f8199d058563.jpg" width="700" alt="">

| EN | ZH |
|---|---|
| In "Split-Level" mode shown in Figure 8 on page 926, the CATC Trace view combines split transactions. For example, a single TLP read can be grouped with 1 or more completion TLPs to logically show large data transfers as a single line in the trace. The amount of data, starting address, as well as performance metrics are provided for each split level transaction. This allows the user to bypass the details of how large memory transactions are broken into multiple TLP packets and rather focus on the contents of the data. If the user wishes to see the details of the split transaction, the hierarchical display can show the link level and/or packet level breakdown of all the packets which make up this split transaction. This "drill-down" approach to traffic analysis allows the user to start from a high level view of what's happening on the bus and drill down only in the areas of traffic which are interesting to the user. | 在"Split-Level"模式下（如第926页图8所示），CATC Trace视图将拆分事务组合在一起。例如，单个TLP读取请求可以与一个或多个完成TLP分组在一起，从而在逻辑上将大数据传输显示为跟踪中的单一行。每个拆分级事务都提供了数据量、起始地址以及性能指标。这使用户可以绕过大内存事务如何被拆分为多个TLP报文的细节，而专注于数据内容本身。如果用户希望查看拆分事务的详细信息，分层显示可以展示构成该拆分事务的所有报文的链路级和/或报文级分解。这种"向下钻取"的流量分析方法允许用户从总线运行情况的高级视图开始，仅在自己感兴趣的流量区域进行深入分析。 |

Figure A-8: "Split Level" Groups Completions with Associated Non-Posted Request | 图A-8："拆分级别"将完成与关联的非投递请求分组  
<img src="images/part06_699bc3cab83166595fc0510017c197434f2f8de24a18d2e3c63d35088df90ce7.jpg" width="700" alt="">

| EN | ZH |
|---|---|
| The CATC trace view also supports "Compact-View" shown in Figure 9 on page 927. In this view, packets which are sent repeatedly are collapsed into a single cell. This is very useful for collapsing Training Sequences or Flow Control Initialization packets. The software algorithms which perform this collapse are smart enough to collapse any SKIP ordered sets as well. This creates a very compact view of the link training process allowing the user to examine changes in the link training packets without scrolling through hundreds of packets. | CATC跟踪视图还支持"Compact-View"（如第927页图9所示）。在此视图中，重复发送的报文被折叠为单个单元格。这对于折叠训练序列或流控初始化报文非常有用。执行该折叠操作的软件算法足够智能，也可以折叠任何SKIP有序集。这将创建一个非常紧凑的链路训练过程视图，使用户无需滚动浏览数百个报文即可检查链路训练报文中的变化。 |

Figure A-9: "Compact View" Collapses Related Packets for Easy Viewing of Link Training | 图A-9："紧凑视图"折叠相关数据包以便于查看链路训练  
<img src="images/part06_6557f747b954daf86767a3c0fcec6605bd1f0203374312f9dd0f6292a29d92f5.jpg" width="700" alt="">

| EN | ZH |
|----|-----|
| ## LTSSM Graphs | ## LTSSM 状态图 |
| To further enhance the "drill-down" traffic viewing approach, the PETracer application includes an LTSSM graph view as shown in Figure 10 on page 928. When this graph is invoked, the SW parses through the trace to find the link training sections and infers the state of the Link Training and Status State Machine (LTSSM). The result is a graph which breaks down the LTSSM state transitions in a very high level view. This graph allows the user to immediately see if the link went into a recovery state. If so, the user can easily identify which side of the link initiated the recovery, how many times it entered recovery, and even if the link speed or link width decreased because of the recovery. | 为了进一步增强"下钻"查看流量的方法，PETracer 应用程序包含一个 LTSSM 图视图，如图 10（第 928 页）所示。当调用此图时，软件会解析跟踪记录以查找链路训练部分，并推断链路训练与状态机 (LTSSM) 的状态。结果是一张以高层视图展示 LTSSM 状态转换的图表。该图允许用户立即查看链路是否进入了恢复状态。如果是，用户可以轻松识别链路的哪一侧发起了恢复、进入恢复的次数，甚至恢复是否导致链路速率或链路宽度降低。 |
| The LTSSM graph is also an active link back into the trace file. For example, if the user clicks on the entry to recovery, the trace file will be navigated to that location in the trace file. This would allow the user to perhaps see if the recovery was caused by repeated NAKs or for some other reason such as loss of block alignment. | LTSSM 图还是一个返回到跟踪文件的活动链接。例如，如果用户单击进入恢复的条目，跟踪文件将导航到该位置。这将使用户能够查看恢复是否是由重复的 NAK 或其他原因（如块对齐丢失）引起的。 |
| In short, when users are debugging issues related to link training, speed change, or low power state transitions, the LTSSM is affected. By examining the LTSSM graph, the user can easily identify whether these link state changes occurred, where they occurred, and navigate directly to them for faster analysis. | 简而言之，当用户调试与链路训练、速率变化或低功耗状态转换相关的问题时，LTSSM 会受到影响。通过检查 LTSSM 图，用户可以轻松识别这些链路状态变化是否发生、发生在何处，并直接导航到这些位置以进行更快的分析。 |

Figure A-10: LTSSM Graph Shows Link State Transitions Across the Trace | 图A-10：LTSSM图显示跟踪中的链路状态转换

<img src="images/part06_b9d2a45ca3b6be6c171b3cea02fb2d722016aed7eb27a49532b9bb55940e5f65.jpg" width="700" alt="">

## Flow Control Credit Tracking

| EN | ZH |
|----|----|
| Flow control credit tracking is particularly problematic in PCI express. The flow control update packets do not show the number of credits each endpoint has, rather it shows how many credits in total have been used. This means that each endpoint must keep a running counter of credits for each type. There are a number of scenarios where credits can be lost, and if this occurs, the link will eventually be unable to transmit data due to lack of credits. Such problems are very difficult to identify and debug. | 在PCI Express中，流控信用量跟踪尤其成问题。流控更新报文不显示每个端点拥有多少信用量，而是显示总共已使用了多少信用量。这意味着每个端点必须为每种类型维护一个信用量的运行计数器。存在多种可能导致信用量丢失的场景，如果发生这种情况，链路最终将因缺乏信用量而无法传输数据。这类问题非常难以识别和调试。 |
| The LeCroy PETracer application has a credit tracking SW tool shown in Figure 11 on page 929 to aid in this debug. If the trace contains FC-Init packets, it will walk through the trace and show the amount of remaining credits per virtual channel buffer type after each TLP and FC-Update. | LeCroy PETracer应用具有一个信用量跟踪软件工具，如图11（第929页）所示，用于辅助此类调试。如果跟踪中包含FC-Init报文，它将遍历跟踪并在每个TLP和FC-Update之后显示每个虚通道缓冲区类型的剩余信用量。 |
| FC-Init packets are sent once after link training. Because of this, the PETracer application has the ability for the user to set initial credit values at some point in the trace and the SW will calculate the relative credit values for the remaining packets. Even if the initial credit values are set improperly by the user, having the ability to see the relative credits is often enough to catch a flow control issue. | FC-Init报文在链路训练后发送一次。因此，PETracer应用允许用户在跟踪中的某个点设置初始信用量值，软件将计算剩余报文的相对信用量值。即使初始信用量值被用户设置不当，能够查看相对信用量通常也足以捕获流控问题。 |

Figure A-11: Flow Control Credit Tracking | 图A-11：流控信用量跟踪  
<img src="images/part06_62a40c1a02e34fb74c289c3d851725d2d0fff9eb590b5a215795fcd7ddffb5f3.jpg" width="700" alt="">

## Bit Tracer

| EN | ZH |
|---|---|
| Some debug situations are not solved by a drill down approach to examining the traffic. For example if the link settings are incorrect, the recording is often unreadable. What if a device is not properly scrambling the traffic, or the 10 bit symbols are sent in reverse order? For this scenario, a tool which focuses on analysis between the waveform view of the scope and the CATC Trace view is needed. This is where the BitTracer view shown in Figure 12 on page 930 is most powerful. | 某些调试场景无法通过逐层下钻检查流量来解决。例如，如果链路设置不正确，记录通常无法读取。如果设备未能正确加扰流量，或者10位符号以相反顺序发送，该怎么办？针对这种情况，需要一种能够在示波器波形视图与CATC Trace视图之间进行分析的工具。这正是第930页图12所示的BitTracer视图最为强大的地方。 |
| The BitTracer view allows the user to see raw traffic exactly as it was seen on the link. The software allows the user to see the traffic as 10 bit symbols, scrambled bytes, or unscrambled bytes. Invalid symbols and incorrect running disparity are highlighted in red. | BitTracer视图允许用户查看链路上原始流量的精确形态。该软件允许用户以10位符号、加扰字节或未加扰字节的形式查看流量。无效符号和错误的运行不一致性以红色高亮显示。 |
| To further determine what may be wrong with the traffic, the BitTracer tool adds a powerful list of post processing features which can modify the traffic. For example, post capture; the user can invert the polarity of a given lane. Once applied, the user can see if the 10 bit symbols are now represented properly in the trace. If this cleans up the trace, it's an indication that the recording settings for the Analyzer hardware need to be changed. | 为了进一步确定流量可能存在的问题，BitTracer工具提供了一系列强大的后处理功能，可对流量进行修改。例如，在捕获后，用户可以反转给定通道的极性。应用后，用户可以查看10位符号现在是否在跟踪中正确呈现。如果这清理了跟踪，则表明分析仪硬件的记录设置需要更改。 |

Figure A-12: BitTracer View of Gen2 Traffic | 图A-12：Gen2流量的BitTracer视图
<img src="images/part06_32acbc40b344bfad018991596c20bdb96beda691ecf83baa5112b5024563895a.jpg" width="700" alt="">

| EN | ZH |
|---|---|
| In addition, the lane ordering can be modified. This is useful for determining if lane reversal is causing a bad capture. If the traffic has excessive lane to lane skew, the BitTracer software allows the user to re-align the traffic. For Gen3 traffic, this skew can be applied 1 bit at a time. This essentially allows the user to fix the 130 bit block alignment post capture. | 此外，还可以修改通道顺序。这对于判断通道反转是否导致捕获不良非常有用。如果流量存在过大的通道间偏移，BitTracer软件允许用户重新对齐流量。对于Gen3流量，可以每次1位地应用此偏移。这实质上允许用户在捕获后修复130位块对齐。 |
| After applying changes to the data, all or just a portion of the data can be exported into the standard CATC Trace view for higher level analysis. This workflow is very powerful for debugging low level issues during early bringup. Let's say for example, the user's device trains the link properly, and then suddenly applies polarity inversion to 1 lane. This is a clear violation of the spec and will cause the link to retrain. If this traffic is captured with the BitTracer tool, the user could easily identify this as the problem. Additionally, the portion of the traffic before and after the inversion could be exported into separate trace files and examined in the CATC Trace view. | 在对数据应用更改后，可以将全部或部分数据导出到标准CATC Trace视图中进行更高级别的分析。此工作流对于在早期调试过程中排查底层问题非常强大。例如，假设用户的设备正确训练了链路，然后突然对1个通道应用极性反转。这明显违反了规范，并将导致链路重新训练。如果使用BitTracer工具捕获此流量，用户可以轻松识别出此问题。此外，反转前后的流量部分可以导出到单独的跟踪文件中，并在CATC Trace视图中进行检查。 |

| EN | ZH |
|---|---|
| ## Analysis overview | ## 分析概览 |
| As you can see, different traffic views can be beneficial for debugging certain failure conditions. LeCroy supports import of PCIe traffic from many sources into its highly sophisticated PEtracer software. Whether the source is RTL simulation, an oscilloscope capture, or a dedicated protocol analyzer capture, PETracer has a rich set of traffic views and reports which allow the user to best understand the health and state of their PCIe link. | 如您所见，不同的流量视图有助于调试某些故障情况。LeCroy 支持从多种来源将 PCIe 流量导入其高度精密的 PETracer 软件。无论来源是 RTL 仿真、示波器捕获还是专用协议分析仪捕获，PETracer 都提供了丰富的流量视图和报告，使用户能够最好地了解其 PCIe 链路的状态和健康状况。 |

| EN | ZH |
|----|----|
| ## Traffic generation | ## 流量生成 |

## Pre-Silicon

| EN | ZH |
| --- | --- |
| For stimulating a PCI Express endpoint in simulation, dedicated verification IP can be purchased from a number of vendors. This IP will test for basic functionality as well as perform a number of PCIe compliance checks. It is certainly in the interest of the ASIC developer to find and fix these issues before tapeout, and this is where the value of these tools comes from. If the PCIe design is implemented in an FPGA where mask costs are not an issue, it may be more cost effective to perform these compliance checks in hardware with a dedicated traffic generation tool such as the LeCroy PETrainer or LeCroy PTC card. | 为了在仿真中激励 PCI Express 端点，可以从多家供应商处购买专用的验证 IP。该 IP 将测试基本功能，并执行多项 PCIe 合规性检查。在流片前发现并修复这些问题显然符合 ASIC 开发者的利益，而这些工具的价值正源于此。如果 PCIe 设计是在掩膜成本不成问题的 FPGA 中实现的，那么使用专用流量生成工具（如 LeCroy PETrainer 或 LeCroy PTC 卡）在硬件中执行这些合规性检查可能更具成本效益。 |

| EN | ZH |
|----|----|
| ## Post-Silicon | ## 硅后 |

## Exerciser Card

| EN | ZH |
|----|----|
| To thoroughly test the PCIe compliance and overall robustness of a PCIe design post‑silicon, a dedicated Exerciser card such as the LeCroy PETrainer shown in Figure 13 on page 932 is used. This card allows the user to generate a wide range of compliant and non‑compliant traffic. For example, if you place your PCIe card in a standard motherboard, you may be limited in the size of the TLP packets it will see. A dedicated Exerciser card can generate TLP packets across the entire legal range of packet sizes. | 为了在芯片后全面测试PCIe设计的合规性和整体稳健性，需要使用专用的Exerciser卡（例如图13（第932页）所示的LeCroy PETrainer）。该卡允许用户生成各种合规和非合规流量。例如，如果将PCIe卡置于标准主板中，其所见的TLP报文大小可能会受到限制。而专用的Exerciser卡可以生成整个合法范围内各种大小的TLP报文。 |
| Secondly, if you would like to test that a card issues a NAK in response to a TLP with a bad LCRC, it would not possible with the card connected to compliant devices. They do not transmit bad packets. An Exerciser card can create a TLP with a bad LCRC, improper header values, or end the TLP with an EDB symbol. | 其次，如果要测试某张卡是否会针对带有错误LCRC的TLP发出NAK，在连接合规设备的情况下是无法做到的——合规设备不会发送错误报文。而Exerciser卡可以创建带有错误LCRC、错误头部值的TLP，或以EDB符号结束TLP。 |
| If you would like to test that your card properly replay's a packet when it receives a NAK, this can be done with an Exerciser. Perhaps you would like to issue 4 NAKs in a row to a certain TLP so that link recovery is initiated. This behavior is all quite easy to program into the exerciser card. | 如果要测试您的卡在收到NAK时是否正确重发报文，使用Exerciser即可完成。例如，您可以对某个TLP连续发出4个NAK，从而触发链路恢复。所有这些行为都很容易编程写入Exerciser卡。 |
| The number of test cases and failure scenarios is limited only by the number of scripts you write. Once written, these scripts can be re‑used for testing new versions of your design. The Analyzer SW can record these sessions and use scripting to determine if the response was correct. A number of LeCroy customers have created large libraries of regression tests using these tools. | 测试用例和故障场景的数量仅受限于您所编写的脚本数量。脚本编写完成后，可复用于测试设计的新版本。分析仪软件可以记录这些会话，并通过脚本判断响应是否正确。许多LeCroy客户已使用这些工具创建了大量的回归测试库。 |

Figure A‐13: LeCroy Gen3 PETrainer Exerciser Card | 图A‐13：LeCroy Gen3 PETrainer训练卡  
<img src="images/part06_fe9de6f68b8c2df77585c842703d289e746b886d39f06a0ac25f2aa98dea6289.jpg" width="700" alt="">

| EN | ZH |
|----|----|
| ## PTC card | ## PTC卡 |
| The PCI SIG has published a specific list of compliance tests which all "Compliant" devices must pass. The LeCroy Protocol Test Card (PTC) is the hardware used to perform these tests at the PCI SIG Compliance workshops. Users can purchase a PTC card from LeCroy shown in Figure 14 on page 933 to pre&#8209;test their devices to ensure they will pass PCI SIG compliance testing. | PCI SIG发布了一份具体的合规性测试清单，所有"符合规范"的设备必须通过这些测试。LeCroy协议测试卡(PTC)是在PCI SIG合规性研讨会上执行这些测试所使用的硬件。用户可以从LeCroy购买PTC卡(如第933页图14所示)来预测试其设备，以确保它们能通过PCI SIG合规性测试。 |
| The LeCroy PTC is used to test root complex or endpoint devices at x1 link widths. Link speeds can be either Gen1 or Gen2. | LeCroy PTC用于在x1链路宽度下测试根复合体或端点设备。链路速率可以是Gen1或Gen2。 |

Figure A‑14: LeCroy Gen2 Protocol Test Card (PTC) | 图A‑14：LeCroy Gen2协议测试卡（PTC）

<img src="images/part06_bf64726f89e0bf3cf01f1b179e03fe051e89911e9e26b3b1af31e5b5d59e2752.jpg" width="700" alt="">

## Conclusion

| EN | ZH |
|---|---|
| Today, the PCIe developer has access to a wide range of tools to help debug their PCIe design. Thanks to the wide adoption of the PCIe standard, many of these tools are designed specifically for PCIe debug and include features which address the challenges many PCIe devices face. | 如今，PCIe 开发者可以使用多种工具来帮助调试其 PCIe 设计。得益于 PCIe 标准的广泛采用，其中许多工具专为 PCIe 调试而设计，并包含了应对众多 PCIe 设备所面临挑战的功能。 |
| For more information about the LeCroy PCIe tool offerings, please visit the LeCroy website www.lecroy.com | 有关 LeCroy PCIe 工具产品的更多信息，请访问 LeCroy 网站 www.lecroy.com |

# Appendix B: Markets & Applications for PCI Express

| EN | ZH |
|----|----|
| # Appendix B: Markets & Applications for PCI Express | # 附录 B：PCI Express 的市场与应用 |
| Akber Kazmi (Senior Director Marketing, PLX Technology, Inc.) | Akber Kazmi（PLX Technology 公司市场部高级总监） |

## Introduction

| EN | ZH |
|---|---|
| Since its definition in the early 1990s, PCI has emerged as the most successful interconnect technology ever used in computers. Originally intended for personal computer systems, the PCI architecture has expanded into virtually every computing platform category, including servers, storage, communications, and a wide range of embedded control applications. Most important, each advancement in PCI bus speed and width provided backward compatibility. | 自1990年代初定义以来，PCI已成为计算机史上最成功的互连技术。PCI架构最初面向个人计算机系统，现已扩展到几乎所有计算平台类别，包括服务器、存储、通信以及广泛的嵌入式控制应用。最重要的是，PCI总线速度和宽度的每一次提升都提供了向后兼容性。 |
| As successful as the PCI architecture was, there was a limit to what could be accomplished with a multi-drop, parallel, shared-bus interconnect technology. A number of issues -- clock skew, high pin count, trace routing restrictions in printed circuit boards (PCB), bandwidth and latency requirements, physical scalability, and the need to support Quality of Service (QoS) within a system for a wide variety of applications -- lead to the definition of the PCI Express (PCIe) architecture. | 尽管PCI架构极为成功，但多点、并行、共享总线互连技术的能力终究存在极限。诸多问题——时钟偏移、高引脚数、印制电路板(PCB)上的走线布线限制、带宽和延迟要求、物理可扩展性，以及需要在系统内为多种应用支持服务质量(QoS)——最终催生了PCI Express (PCIe)架构的定义。 |
| PCIe was the natural successor to PCI, and was developed to provide the advantages of a state-of-the-art, high-speed serial interconnect technology with a packet-based layered architecture, but maintain backward-compatibility with the large PCI software infrastructure. The key goal was to provide an optimized, universal interconnect solution for a wide variety of future platforms, including desktop, server, workstation, storage, communications, and embedded systems. | PCIe是PCI的自然继承者，其开发旨在提供一种先进的高速串行互连技术优势，采用基于数据包的分层架构，同时保持与庞大PCI软件基础设施的向后兼容性。关键目标是为各种未来平台（包括桌面、服务器、工作站、存储、通信和嵌入式系统）提供优化的通用互连解决方案。 |
| After its introduction in 2001, PCIe has gone through three generations of enhancements. In the first generation (Gen1), signaling rate was set at 2.5 GT/s and later enhanced to 5 GT/s (Gen2) and eventually 8 GT/s (Gen3). The PCIe specification allows combining of 2, 4, 8, 12, 16 or 32 lanes into a single port. However, products available today do not support 12- and 32-lane-wide ports. It is important to note that all PCIe Gen2 and Gen3 devices are required to be backward-compatible in speed with that of the previous generation. | 自2001年推出以来，PCIe已经历了三代增强。第一代(Gen1)信号速率定为2.5 GT/s，随后提升至5 GT/s (Gen2)，最终达到8 GT/s (Gen3)。PCIe规范允许将2、4、8、12、16或32条通道(Lane)组合到一个端口。然而，当前市面上的产品不支持12通道和32通道宽的端口。值得注意的是，所有PCIe Gen2和Gen3器件必须在速度上与上一代保持向后兼容。 |
| The industry has launched and has fully embraced PCIe Gen3 products, while at the same time the PCI Special Interest Group (PCI-SIG) is analyzing signaling rate (speed) for Gen4. The goal for PCIe Gen4 is to double the speed of Gen3, to 16 GT/s. | 业界已推出并全面采纳了PCIe Gen3产品，同时PCI特殊兴趣小组(PCI-SIG)正在分析Gen4的信号速率（速度）。PCIe Gen4的目标是将Gen3的速度提升一倍，达到16 GT/s。 |
| PCIe switches are available in an array of sizes, ranging from 3 to 96 lanes, and 3 to 24 ports where each port could be one, two, four, eight or 16 lanes wide. A Gen3 single lane would provide 1GB/s of bandwidth, while a 16-lane port offers 16GB bandwidth in each direction. Additionally, PCIe switch vendors, such as PLX Technology, have added features and enhancement to their products that are not part of PCIe specifications but enable them to differentiate their products and add value for the system designers. These features deliver ease of use, higher performance, fail-over, error detection, error isolation, and field-upgradability. | PCIe交换机有多种规格，通道数从3到96，端口数从3到24，每个端口可宽达1、2、4、8或16条通道。Gen3单条通道提供1GB/s的带宽，而16通道端口在每个方向上提供16GB带宽。此外，PCIe交换机供应商（如PLX Technology）在其产品中添加了不属于PCIe规范的特性和增强功能，从而使其产品差异化并为系统设计人员增加价值。这些特性提供了易用性、更高性能、故障切换、错误检测、错误隔离和现场可升级能力。 |
| On-chip features include non-transparent (NT) bridging, peer-to-peer communication, Hot-Plug, direct memory access (DMA), and error checking/recovery. Additionally debug features such as packet generation, receiver-eye measurement, traffic monitoring, and error injection in live traffic offer significant value to the designers, enabling early system bring-up. Many of these features can also be used for run-time performance improvements and monitoring. | 片内特性包括非透明(NT)桥接、对等通信、热插拔(Hot-Plug)、直接存储器访问(DMA)以及错误检查/恢复。此外，数据包生成、接收眼图测量、流量监控和在线流量错误注入等调试功能为设计人员提供了重要价值，使系统能够提早启动。其中许多特性还可用于运行时性能提升和监控。 |
| Features included in next generation of PCIe switches are: | 下一代PCIe交换机包含的特性如下： |
| NT bridging: Allows two hosts/CPUs to be connected to the same PCIe switch while electrically and logically isolated. The NT bridging functions is broadly used in systems requiring isolation of two active CPUs or two CPUs where one is active and other is passive. The NT functionality allows the exchange of heartbeat between the two host CPUs to enable fail-over if one of them fails. | NT桥接：允许两个主机/CPU连接到同一PCIe交换机，同时在电气和逻辑上保持隔离。NT桥接功能广泛用于需要隔离两个活动CPU或一个活动一个备用CPU的系统中。NT功能允许两个主机CPU之间交换心跳信号，以便在其中一个发生故障时实现故障切换。 |

## Chapter : Appendix B: Markets & Applications for PCI

| EN | ZH |
|---|---|
| DMA: An on‑chip DMA controller in a PCIe switch offers significant value to the designers as it enables them to spare CPU cycles to move data between peers and the CPU to/from I/Os. The CPU's reduced effort in moving data boosts overall performance of the system as the spared CPU cycles can be used to run applications rather than managing data I/O. | DMA：PCIe交换机中的片上DMA控制器为设计人员提供了重要价值，因为它使他们能够节省CPU周期，用于在对等设备之间以及CPU与I/O设备之间移动数据。CPU在数据移动方面的负担减轻提升了系统的整体性能，因为节省的CPU周期可用于运行应用程序，而非管理数据I/O。 |
| Error Isolation: Users can program triggers for certain error events and response by the switch. The response of switch can also be programmed to ignore, trigger a host interrupt, bring the port with errors down, or bring the entire switch down. | 错误隔离：用户可以针对特定错误事件和交换机的响应来编程触发条件。交换机的响应也可以被编程为忽略、触发主机中断、使发生错误的端口宕机，或使整个交换机宕机。 |
| Packet Generation: Generally, it is difficult to generate traffic that saturates a PCIe port without the use of expensive packet generator equipment. PCIe switches now have the ability to saturate any PCIe port with desired traffic, such as transaction layer packets, to check the performance and robustness of the system. | 报文生成：通常，在不使用昂贵的报文生成器设备的情况下，很难产生能够饱和PCIe端口的流量。PCIe交换机现在能够使用所需的流量（例如事务层报文）来饱和任何PCIe端口，以检查系统的性能和健壮性。 |

| EN | ZH |
|---|---|
| ## PCI Express IO Virtualization Solutions | ## PCI Express IO 虚拟化解决方案 |
| The PCIe technology was initially defined as a single-host interconnect technology but in last few years new standards have been developed that make PCIe suitable for multi-host systems as a switch fabric technology for data centers and enterprise IT applications. The presence of native PCIe interfaces (ports) on x86 CPUs and servers platforms has enabled designers to use PCIe as backplane and fabric technology for small to mid-size server clusters. | PCIe 技术最初被定义为单主机互连技术，但在过去几年中，新的标准已制定出来，使 PCIe 适用于作为交换网络技术用于多主机系统，以支持数据中心和企业 IT 应用。x86 CPU 和服务器平台上原生 PCIe 接口（端口）的存在，使设计人员能够将 PCIe 用作中小型服务器集群的背板和网络技术。 |
| In 2007, the PCI-SIG released the Single-Root I/O Virtualization (SR-IOV) specification that enables sharing of a single physical resource such as a network interface card or host bus adapter in a PCIe system among multiple virtual machines running on one host. This is the simplest approach to sharing resources or I/O devices among different applications or virtual machines. | 2007 年，PCI-SIG 发布了单根 I/O 虚拟化 (SR-IOV) 规范，该规范允许在一个主机上运行的多个虚拟机之间共享 PCIe 系统中的单个物理资源，例如网卡或主机总线适配器。这是在应用程序或虚拟机之间共享资源或 I/O 设备的最简单方法。 |
| The PCI-SIG followed by completing, in 2008, work on its Multi-Root I/O Virtualization (MR-IOV) specification that extends the use of PCIe technology from a single-root domain to a multi-root domain. The MR-IOV specification enables the use of a single I/O device by multiple hosts and multiple system images simultaneously, as illustrated in Figure 0-1 on page 938. This illustration shows a multi-host environment where MR-IOV capable NIC and HBA are shared across multiple servers or virtual machines via an MR-IOV switch. | 随后，PCI-SIG 于 2008 年完成了其多根 I/O 虚拟化 (MR-IOV) 规范的制定，将 PCIe 技术的应用从单根域扩展到多根域。MR-IOV 规范允许多个主机和多个系统镜像同时使用单个 I/O 设备，如图 0-1（第 938 页）所示。该图展示了一个多主机环境，其中支持 MR-IOV 的 NIC 和 HBA 通过 MR-IOV 交换机在多个服务器或虚拟机之间共享。 |

Figure 0-1:  MR-IOV Switch Usage | 图0-1：MR-IOV交换机用途
<img src="images/part06_96a163a352f0d6bdfeb152fbc9235f345889ca2e07d1390c473b1baeca0607a0.jpg" width="700" alt="">

| EN | ZH |
|---|---|
| In order to implement MR-IOV specifications, three components of the system need to be developed – MR-IOV PCIe switches, endpoints, and management software. All three of these components must be available simultaneously and work seamlessly. Unfortunately, four years after the specification was developed, there is not a single silicon vendor that has MR-IOV capable PCIe switch or end-points. PCIe switch vendors are offering solutions that provide capabilities defined for MR-IOV through vendor-defined features and utilizing available SR-IOV end-points. | 为了实现 MR-IOV 规范，需要开发系统的三个组件——MR-IOV PCIe 交换机、端点和管理软件。这三个组件必须同时可用且无缝协作。遗憾的是，在规范制定四年后，仍没有任何一家芯片供应商拥有支持 MR-IOV 的 PCIe 交换机或端点。PCIe 交换机供应商正在通过厂商自定义特性并利用现有的 SR-IOV 端点，来提供具备 MR-IOV 所定义能力的解决方案。 |

## Multi-Root (MR) PCIe Switch Solution
## 多根(MR)PCIe交换机解决方案

| EN | ZH |
|---|---|
| PCIe switch vendors have created switches that offer implementation of multihost function through non‑transparent bridging and multi‑root (MR) capabilities. These MR switches allow multiple hosts to be connected to a single switching device, which can be portioned under user control in such a way that each host will be connected to a desired set of downstream ports of the switch. | PCIe交换机供应商已开发出通过非透明桥接和多根(MR)能力实现多主机功能的交换机。这些MR交换机允许多个主机连接到单个交换设备，在用户控制下可对其进行分区，使得每个主机连接到交换机所需的一组下游端口。 |
| In the MR switches, one of the hosts acts as the master and assigns I/Os to other host ports. Each host operates independently of other hosts and controls downstream devices in its domain. Figure 0‑2 on page 939 illustrates the internal architecture of an MR switch, in which particular sets of downstream ports are associated to particular host ports under management control. | 在MR交换机中，其中一个主机充当主控，向其他主机端口分配I/O。每个主机独立于其他主机运行，并控制其域内的下游设备。第939页的图0-2展示了MR交换机的内部架构，其中特定的一组下游端口在管理控制下与特定的主机端口相关联。 |

Figure 0‑2:  MR‑IOV Switch Internal Architecture | 图0‑2：MR-IOV交换机内部架构  
<img src="images/part06_01e23cd1e85edb410102ef8a999ae1c6cf5d91d36573530905b263a357eee4ed.jpg" width="700" alt="">

| EN | ZH |
|---|---|
| ## PCIe Beyond Chip-to-Chip Interconnect | ## 超越芯片间互连的PCIe |
| In early stages of PCIe deployments the technology was used as a chip-to-chip interconnect but now broad availability of PCIe interfaces on CPUs, chipsets and IOs and broad adoption of these components is pushing it beyond traditional applications. In a new generation of applications, PCIe is used in system backplanes, switch fabrics, cabling systems, storage/IO expansion, IO virtualization, high-performance computing (HPC), and server clusters. Figure 0-3 on page 940 illustrates use of PCIe in a data center for high performance compute application where servers in a rack are clustered through a top-of-rack (TOR) PCIe switch fabric box. The TOR PCIe switch can be connected to the network through Ethernet and to local storage and compute resources through PCIe links. | 在PCIe部署的早期阶段，该技术被用作芯片间互连，但现在CPU、芯片组和IO设备上PCIe接口的广泛可用性以及这些组件的广泛采用，正将其推向传统应用之外的领域。在新一代应用中，PCIe被用于系统背板、交换结构、布线系统、存储/IO扩展、IO虚拟化、高性能计算（HPC）和服务器集群。第940页的图0-3展示了PCIe在数据中心高性能计算应用中的使用，其中机架内的服务器通过机架顶（TOR）PCIe交换结构盒进行集群。TOR PCIe交换机可通过以太网连接到网络，并通过PCIe链路连接到本地存储和计算资源。 |
| PCIe connections out-side the box depend on PCIe copper or optical cables that the leader in the industry are introducing at lower cost. The PCIe TOR fabric is suitable for server/compute clustering and may replace InfiniBand as the ecosystem for PCIe as fabric grows. | 机箱外部的PCIe连接依赖于业界领先者正在以更低成本推出的PCIe铜缆或光缆。PCIe TOR结构适用于服务器/计算集群，随着PCIe作为互连结构的生态系统的发展，其可能取代InfiniBand。 |

Figure 0-3:  PCIe in a Data Center for HPC Applications | 图0-3：数据中心中用于HPC应用的PCIe  
<img src="images/part06_aaa3ca52e819155e9b03c643a9dcf4cfe8558adc3b6863e309b81a1ec5d98a32.jpg" width="700" alt="">

## SSD/Storage IO Expansion Boxes / SSD/存储IO扩展盒

| EN | ZH |
|---|---|
| Recently, the industry has converged towards PCIe as the unified interconnect technology for enterprise storage and solid state drive (SSD) applications. The NVM HCI, an industry consortium, has released a specification called NVM Express (NVMe) that uses PCIe to provide the bandwidth needed for SSD applications. Additionally, a T10 committee has embarked on defining SCSI over PCIe (SOP) protocol to take advantage of PCIe technology capabilities for high‑performance storage applications. Furthermore, the SATA consortium recently announced that it would use PCIe as the interconnect for its next‑generation SATA specification called SATA Express (SATAe). | 近年来，业界已趋向于将PCIe作为企业存储和固态硬盘（SSD）应用的统一互连技术。行业联盟NVM HCI发布了一项名为NVM Express（NVMe）的规范，该规范使用PCIe来提供SSD应用所需的带宽。此外，T10委员会已着手定义基于PCIe的SCSI（SOP）协议，以利用PCIe技术能力满足高性能存储应用的需求。另外，SATA联盟最近宣布，将采用PCIe作为其下一代SATA规范（称为SATA Express，简称SATAe）的互连方案。 |

| EN | ZH |
|---|---|
| ## PCIe in SSD Modules for Servers | ## 服务器SSD模块中的PCIe |
| Traditionally, enterprise SSD modules have shipped with SAS, SATA and Fibre Channel interfaces but due to the above-mentioned developments, a large majority of SSD controller, module and system suppliers have introduced products with PCIe interfaces. Most SSD controllers peak their performance and capacity due to a heavy load of managing flash. In high-performance applications, multiple SSD controllers (or ASICs) are used and aggregated through a PCIe switch. Figure 0-4 on page 941 shows a basic usage of a PCIe switch in an SSD add-in card that applies to any card or module form factor. | 传统上，企业级SSD模块采用SAS、SATA和光纤通道接口，但由于上述发展，绝大多数SSD控制器、模块和系统供应商已推出带有PCIe接口的产品。由于管理闪存的繁重负载，大多数SSD控制器的性能和容量已达到顶峰。在高性能应用中，多个SSD控制器（或ASIC）通过PCIe交换机进行聚合使用。第941页的图0-4展示了PCIe交换机在SSD附加卡中的基本应用，适用于任何卡或模块形态。 |

Figure 0-4:  PCIe Switch Application in an SSD Add-In Card | 图0-4：SSD插件卡中的PCIe交换机应用
<img src="images/part06_ee09497ae91f0c372cb1e5b1789454ff566cf497563f6a3015a06f2498251497.jpg" width="700" alt="">

| EN | ZH |
|---|---|
| For large data center applications, the SSD add-in cards are installed in server motherboards as shown in Figure 0-5 on page 941 and IO expansion boxes (Figure 6) aggregated through PCIe switches. In server motherboard designs, PCIe switches are utilized to create more ports/slots that accommodate additional SSD modules to support the application's needs. | 在大型数据中心应用中，SSD附加卡安装在服务器主板（如第941页图0-5所示）和通过PCIe交换机聚合的IO扩展盒（图6）中。在服务器主板设计中，利用PCIe交换机创建更多端口/插槽，以容纳额外的SSD模块来满足应用需求。 |

Figure 0-5:  Server Motherboard Use PCIe Switches | 图0-5：使用PCIe交换机的服务器主板
<img src="images/part06_45025c5c26c2077c2b463bbfdb015444fe94580e8ecded23a65f5e8088c33341.jpg" width="700" alt="">

| EN | ZH |
|---|---|
| In addition to providing connectivity, PCIe switches can be used for providing redundancy and failover through NT bridging and MR functionality. The MR switches support 1+N failover capability, in which one server/host communicates with N number of servers to check the heartbeat and initiate a failover if one of them fails. One of the servers illustrated in Figure 0-6 on page 942 can be used as backup for the others in 1+N failover scheme. | 除了提供连接性，PCIe交换机还可用于通过NT桥接和MR功能提供冗余和故障转移。MR交换机支持1+N故障转移能力，即一个服务器/主机与N个服务器通信以检查心跳，并在其中一个服务器发生故障时启动故障转移。在第942页图0-6所示的服务器中，其中一个可用作1+N故障转移方案中其他服务器的备份。 |

Figure 0-6:  Server Failover in 1 + N Failover Scheme | 图0-6：1+N故障切换方案中的服务器故障切换
<img src="images/part06_6f95d94991a43d3c77b8aed65c0196e1eab7f6737eaa5cd57a177cbb98f5d425.jpg" width="700" alt="">

## Conclusion

| EN | ZH |
|---|---|
| PCIe interconnect technology has become a serious contender for many high-end applications beyond chip-to-chip interconnect and is expected to be utilized in external I/O sharing, server clustering, I/O expansion and TOR switching. | PCIe互连技术已成为许多高端应用的有力竞争者，其应用范围已超越芯片间互连，预计将被用于外部I/O共享、服务器集群、I/O扩展和TOR交换。 |
| The current 8 GT/s and next-generation (Gen4) 16 GT/s line rates, the ability to aggregate multiple lanes in single high-bandwidth ports, fail-over capabilities, embedded DMA for data transfers, and IO sharing/virtualization provide capabilities that are at least equal to, if not superior to, interfaces such as InfiniBand and Ethernet. | 当前的8 GT/s和下一代(Gen4)16 GT/s速率、在单个高带宽端口中聚合多条通道的能力、故障切换能力、用于数据传输的嵌入式DMA以及I/O共享/虚拟化所提供的性能至少不逊于(即便不是优于)InfiniBand和Ethernet等接口。 |

# Implementing Intelligent Adapters and Multi‐Host Systems With PCI Express Technology

| EN | ZH |
|---|---|
| # Implementing Intelligent Adapters and Multi‐Host Systems With PCI Express Technology | # 使用PCI Express技术实现智能适配器与多主机系统 |
| Jack Regula, Danny Chi, Tim Canepa (PLX Technology, Inc. ) | Jack Regula, Danny Chi, Tim Canepa (PLX Technology, Inc. ) |

## Introduction

| EN | ZH |
|---|---|
| Intelligent adapters, host failover mechanisms and multiprocessor systems are three usage models that are common today, and expected to become more prevalent as market requirements for next generation systems. Despite the fact that each of these was developed in response to completely different market demands, all share the common requirement that systems that utilize them require multiple processors to co‑exist within the system. This appendix outlines how PCI Express can address these needs through non‑transparent bridging. | 智能适配器、主机故障切换机制和多处理器系统是当今常见的三种使用模型，并且随着下一代系统的市场需求，预计将变得更加普遍。尽管每一种模型都是为了应对完全不同的市场需求而开发的，但它们都有一个共同的要求：使用这些模型的系统需要多个处理器在系统内共存。本附录概述了PCI Express如何通过非透明桥接来满足这些需求。 |
| Because of the widespread popularity of systems using intelligent adapters, host failover and multihost technologies, PCI Express silicon vendors must provide a means to support them. This is actually a relatively low risk endeavor; given that PCI Express is software compatible with PCI, and PCI systems have long implemented distributed processing. The most obvious approach, and the one that PLX espouses, is to emulate the most popular implementation used in the PCI space for PCI Express. This strategy allows system designers to use not only a familiar implementation but one that is a proven methodology, and one that can provide significant software reuse as they migrate from PCI to PCI Express.This paper outlines how multiprocessor PCI Express systems will be implemented using industry standard practices established in the PCI paradigm. We first, however, will define the different usage models, and review the successful efforts in the PCI community to develop mechanisms to accommodate these requirements. Finally, we will cover how PCI Express systems will utilize non‑transparent bridging to provide the functionality needed for these types of systems. | 由于使用智能适配器、主机故障切换和多主机技术的系统广泛普及，PCI Express硅片供应商必须提供支持这些技术的手段。这实际上是一项风险相对较低的工作，因为PCI Express在软件上与PCI兼容，而PCI系统早已实现了分布式处理。最明显的方法，也是PLX所倡导的方法，是在PCI Express中仿效PCI领域最流行的实现方式。这一策略使系统设计者不仅可以使用熟悉的实现方式，而且是一种经过验证的方法学，并且在他们从PCI迁移到PCI Express时可以显著重用现有软件。本文概述了如何利用PCI范式中建立的行业标准实践来实现多处理器PCI Express系统。不过，我们首先将定义不同的使用模型，并回顾PCI社区为开发满足这些需求的机制所做的成功努力。最后，我们将介绍PCI Express系统如何利用非透明桥接来提供这些类型系统所需的功能。 |