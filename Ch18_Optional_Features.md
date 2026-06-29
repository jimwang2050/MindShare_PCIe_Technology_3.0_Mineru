# Ch18_Optional_Features

| EN | ZH |
|----|----|

## The Previous Chapter | 上一章

| EN | ZH |
|----|----|
| The previous chapter describes the different ways that PCIe Functions can generate interrupts. | 前一章描述了PCIe功能产生中断的不同方式。 |
| The old PCI model used pins for this, but sideband signals are undesirable in a serial model so support for the inband MSI (Message Signaled Interrupt) mechanism was made mandatory. | 旧的PCI模型使用引脚来实现此功能，但边带信号在串行模型中不可取，因此强制支持带内MSI（消息 signaled 中断）机制。 |
| The PCI INTx# pin operation can still be emulated using PCIe INTx messages for software backward compatibility reasons. | 出于软件向后兼容的原因，仍可使用PCIe INTx消息来模拟PCI INTx#引脚操作。 |
| Both the PCI legacy INTx# method and the newer versions of MSI/MSI-X are described. | 描述了PCI传统INTx#方法以及较新版本的MSI/MSI-X。 |

## This Chapter | 本章

| EN | ZH |
| --- | --- |
| This chapter describes the four types of resets defined for PCIe: cold reset, warm reset, hot reset, and function-level reset. The use of a side-band reset PERST# signal to generate a system reset is discussed, and so is the in-band TS1 used to generate a Hot Reset. | 本章描述了为PCIe定义的四种复位类型：冷复位（cold reset）、温复位（warm reset）、热复位（hot reset）和功能级复位（function-level reset）。讨论了使用边带复位信号PERST#产生系统复位，以及使用带内TS1产生热复位（Hot Reset）。 |

| EN | ZH |
|---|---|
| ## The Next Chapter | ## 下一章 |
| The next chapter describes the PCI Express hot plug model. A standard usage model is also defined for all devices and form factors that support hot plug capability. | 下一章描述PCI Express热插拔模型。还为所有支持热插拔能力的设备和外形因子定义了一个标准的使用模型。 |
| Power is an issue for hot plug cards, too, and when a new card is added to a system during runtime, it's important to ensure that its power needs don't exceed what the system can deliver. | 功耗对于热插拔卡也是一个问题，当在运行时向系统添加新卡时，确保其功耗需求不超过系统可提供的功耗非常重要。 |
| A mechanism was needed to query and control the power requirements of a device, Power Budgeting provides this. | 需要一种机制来查询和控制设备的功耗需求，电源预算机制(Power Budgeting)提供了这一功能。 |

| EN | ZH |
|---|---|
| ## Two Categories of System Reset | ## 系统复位之两类 |
| The PCI Express spec describes four types of reset mechanisms. Three of these were part of the earlier revisions of the PCIe spec and are collectively referred to now as Conventional Resets, and two of them are called Fundamental Resets. The fourth category and method, added with the 2.0 spec revision, is called the Function Level Reset. | PCI Express 规范描述了四种复位机制。其中三种属于早期 PCIe 规范修订版的一部分，现统称为常规复位（Conventional Reset），另外两种称为基本复位（Fundamental Reset）。第四种类别与方法在 2.0 规范修订版中加入，称为功能级复位（Function Level Reset）。 |

## 18.2 Conventional Reset | 18.2 传统复位

| EN | ZH |
|----|----|
| Conventional Reset | 常规复位 |

## 18.2.1 Fundamental Reset | 18.2.1 基本复位

| EN | ZH |
|---|---|
| A Fundamental Reset is handled in hardware and resets the entire device, reinitializing every state machine and all the hardware logic, port states and configuration registers. The exception to this rule is a group of some configuration register fields that are identified as "sticky", meaning they retain their contents unless all power is removed. This makes them very useful for diagnosing problems that require a reset to get a Link working again, because the error status survives the reset and is available to software afterwards. If main power is removed but Vaux is available, that will also maintain the sticky bits, but if both main power and Vaux are lost, the sticky bits will be reset along with everything else. | 基本复位由硬件处理，将整个设备复位，重新初始化所有状态机及全部硬件逻辑、端口状态和配置寄存器。此规则的一个例外是一组被标识为"sticky"的配置寄存器字段，这意味着除非所有电源都被移除，否则它们会保留其内容。这使得它们对于诊断需要复位才能使链路重新工作的问题非常有用，因为错误状态在复位后仍然存在，并且之后可供软件使用。如果主电源被移除但Vaux可用，这也会维持sticky位，但如果主电源和Vaux都丢失，则sticky位将随其他所有内容一起被复位。 |
| A Fundamental Reset will occur on a system-wide reset, but it can also be done for individual devices. | 基本复位会在系统级复位时发生，但也可以针对单个设备执行。 |
| Two types of Fundamental Reset are defined: | 定义了两种类型的基本复位： |
| Cold Reset: The result when the main power is turned on for a device. Cycling the power will cause a cold reset. | 冷复位(Cold Reset)：设备主电源打开时的结果。断电再上电将导致冷复位。 |
| Warm Reset (optional): Triggered by a system-specific means without shutting off main power. For example, a change in the system power status might be used to initiate this. The mechanism for generating a Warm Reset is not defined by the spec, so the system designer will choose how this is done. | 暖复位(Warm Reset)（可选）：通过系统特定的方式触发，无需关闭主电源。例如，系统电源状态的变化可用于发起此复位。规范未定义生成暖复位的机制，因此系统设计者将选择如何实现。 |

## When a Fundamental Reset occurs: | 当发生基础复位时：

| EN | ZH |
|---|---|
| For positive voltages, receiver terminations are required to meet the Z parameter. At 2.5 GT/s, this is no less than 10 KΩ. At the higher speeds it must be no less than 10 KΩ for voltages below 200mv, and 20 KΩ for voltages above 200mv. These are the values when the terminations are not powered. | 对于正电压，接收器端接须满足 Z 参数。在 2.5 GT/s 下，该值不小于 10 KΩ。在更高速率下，当电压低于 200mv 时必须不小于 10 KΩ，当电压高于 200mv 时必须不小于 20 KΩ。这些是端接未上电时的取值。 |
| • Similarly for negative voltages, the Z<sub>RX‐HIGH‐IMP‐DC‐NEG</sub> parameter, the value is a minimum of 1 KΩ in every case. | • 类似地，对于负电压，Z<sub>RX‐HIGH‐IMP‐DC‐NEG</sub> 参数的值在任何情况下最小为 1 KΩ。 |
| Transmitter terminations are required to meet the output impedance Z<sub>TX‐DIFF‐DC</sub> from 80 to 120 Ω for Gen1 and max of 120 Ω for Gen2 and Gen3, but may place the driver in a high impedance state. | 发送器端接须满足输出阻抗 Z<sub>TX‐DIFF‐DC</sub>：Gen1 为 80 至 120 Ω，Gen2 和 Gen3 最大为 120 Ω，但可将驱动器置于高阻态。 |
| • The transmitter holds a DC common mode voltage between 0 and 3.6 V. | • 发送器保持 DC 共模电压在 0 至 3.6 V 之间。 |

| EN | ZH |
|---|---|
| ## When exiting from a Fundamental Reset: | ## 退出基础复位时： |
| The receiver single‐ended terminations must be present when receiver terminations are enabled so that Receiver Detect works properly (40-60Ω for Gen1 and Gen2, and 50Ω +/– 20% for Gen3. By the time Detect is entered, the common-mode impedance must be within the proper range of 50Ω +/– 20%. | 接收器端接使能时，接收器单端端接必须存在，以便接收器检测(Receiver Detect)正常工作(Gen1和Gen2为40-60Ω，Gen3为50Ω ±20%)。进入检测(Detect)状态时，共模阻抗必须处于50Ω ±20%的适当范围内。 |
| must re‐enable its receiver terminations Z of 100Ω within 5 ms of Fundamental Reset exit, making it detectable by the neighbor's transmitter during training. | 必须在退出基础复位后5ms内重新使能其100Ω接收器端接Z，使其在训练期间可被相邻发送器检测到。 |
| • The transmitter holds a DC common mode voltage between 0 and 3.6 V. | • 发送器保持0至3.6V的直流共模电压。 |
| Two methods of delivering a Fundamental Reset are defined. First, it can be signaled with an auxiliary side‐band signal called PERST# (PCI Express Reset). Second, when PERST# is not provided to an add‐in card or component, a Fundamental Reset is generated autonomously by the component or add‐in card when the power is cycled. | 定义了两种提供基础复位的方法。第一，可通过称为PERST#(PCI Express复位)的辅助边带信号来指示。第二，当未向附加卡或组件提供PERST#时，在电源循环时由组件或附加卡自主生成基础复位。 |

## PERST# Fundamental Reset Generation | PERST# 基础复位生成

| EN | ZH |
|---|---|
| A central resource device such as a chipset in the PCI Express system provides this reset. For example, the IO Controller Hub (ICH) chip in Figure 18-1 on page 836 may generate PERST# based on the status of the system power supply 'POWERGOOD' signal, since this indicates that the main power is turned on and stable. If power is cycled off, POWERGOOD toggles and causes PERST# to assert and deassert, resulting in a Cold Reset. The system may also provide a method of toggling PERST# by some other means to accomplish a Warm Reset. | PCI Express系统中的中央资源设备（如芯片组）提供此复位。例如，第836页图18-1中的I/O控制器集线器（ICH）芯片可根据系统电源'POWERGOOD'信号的状态产生PERST#，因为该信号指示主电源已开启并稳定。如果电源循环关闭，POWERGOOD信号翻转，导致PERST#置位和去置位，从而产生冷复位（Cold Reset）。系统也可以通过其他方式切换PERST#来实现热复位（Warm Reset）。 |
| The PERST# signal feeds all PCI Express devices on the motherboard including the connectors and graphics controller. Devices may choose to use PERST# but are not required to do so. PERST# also feeds the PCIe-to-PCI-X bridge shown in the figure. Bridges always forward a reset on their primary (upstream) bus to their secondary (downstream) bus, so the PCI-X bus sees RST# asserted. | PERST#信号供给主板上的所有PCI Express设备，包括连接器和图形控制器。设备可以选择使用PERST#，但并非必须。PERST#也供给图中所示的PCIe到PCI-X桥接器。桥接器始终将其主（上游）总线上的复位转发到其次（下游）总线，因此PCI-X总线上会看到RST#被置位。 |

## Autonomous Reset Generation | 自主复位生成

| EN | ZH |
|---|---|
| A device must be designed to generate its own reset in hardware upon application of main power. The spec doesn't describe how this would be done, so a self-reset mechanism can be built into the device or added as external logic. For example, an add-in card that detects Power-On may use that event to generate a local reset to its device. The device must also generate an autonomous reset if it detects its power go outside of the limits specified. | 设备必须设计为在主电源施加时在硬件中生成自己的复位信号。规范未描述具体实现方式，因此可以将自复位机制内置于设备中，或作为外部逻辑添加。例如，检测到上电的插卡可以利用该事件为其设备生成本地复位。如果设备检测到其电源超出规定限值，也必须生成自主复位。 |

## Link Wakeup from L2 Low Power State | 链路从 L2 低功耗状态唤醒

| EN | ZH |
|---|---|
| As an example of the need for an autonomous reset, a device whose main power has been turned off as part of a power management policy may be able to request a return to full power if it was designed to signal a wakeup. When power is restored, the device must be reset. The power controller for the system may assert the PERST# pin to the device, as shown in Figure 18‐1 on page 836, but if it doesn't, or if the device doesn't support PERST#, the device must autonomously generate its own Fundamental Reset when it senses main power reapplied. | 作为自主复位需求的示例，作为电源管理策略的一部分其主电源已被关闭的设备，如果被设计为能够发出唤醒信号，则其可以请求恢复到全功率状态。当电源恢复时，设备必须被复位。系统的电源控制器可能会向设备断言 PERST# 引脚，如图 18‐1（第 836 页）所示，但如果电源控制器未这样做，或者设备不支持 PERST#，则设备在检测到主电源重新施加时必须自主生成其自己的 Fundamental Reset。 |

Figure 18‐1: PERST# Generation | 图18‐1：PERST#生成  
<img src="images/part05_267333619166f2703f188335aac497d9fd1d446b17fb69c9d0e5b6d706809c28.jpg" width="700" alt="">

## 18.2.2 Hot Reset (In-band Reset) | 18.2.2 热复位（带内复位）

| EN | ZH |
|---|---|
| A Hot Reset is propagated in-band from one link neighbor to another by sending several TS1s (whose contents are shown in Figure 18-2) with bit 0 of symbol 5 asserted. These TS1s are sent on all Lanes, using the previously negotiated Link and Lane numbers, for 2 ms. Once it's been sent, the Transmitter and Receiver of the Hot Reset will both end up in the Detect LTSSM state (see "Hot Reset State" on page 612). | 热复位通过带内方式从一个链路邻居传播到另一个链路邻居，其方法是发送多个TS1有序集（其内容如图18-2所示），并且符号5的位0被置位。这些TS1在所有通道上发送，使用先前协商的链路号和通道号，持续2毫秒。一旦发送完成，热复位的发送器和接收器都将进入Detect LTSSM状态（参见第612页的"热复位状态"）。 |

Figure 18-2: TS1 Ordered-Set Showing the Hot Reset Bit | 图18-2：显示热复位位的TS1有序集

<img src="images/part05_e02be89e991ca432a39565fc5dba292e740f6716908555ed1450a0325fe099df.jpg" width="700" alt="">

| EN | ZH |
|---|---|
| A hot reset is initiated in software by setting the Secondary Bus Reset bit in a bridge's Bridge Control configuration register, as shown in Figure 18-5 on page 840. Consequently, only devices containing bridges, like the Root Complex or a Switch, can do this. A Switch that receives hot reset on its Upstream Port must broadcast it to all of its Downstream Ports and reset itself. All devices downstream of a switch that receive the hot reset will reset themselves. | 热复位由软件通过设置桥接器的Bridge Control配置寄存器中的Secondary Bus Reset位来发起，如图18-5（第840页）所示。因此，只有包含桥接器的设备，如根复合体或交换机，才能执行此操作。在上游端口接收到热复位的交换机必须将其广播到其所有下游端口，并复位自身。交换机下游所有接收到热复位的设备都将复位自身。 |

## Response to Receiving Hot Reset | 接收热复位的响应

| EN | ZH |
|---|---|
| The device's LTSSM goes through the Recovery and Hot Reset state, and then back to the Detect state, where it starts the Link Training process. | 设备的LTSSM历经恢复与热复位状态，然后返回检测状态，并在该状态下开始链路训练过程。 |
| All of the device's state machines, hardware logic, port states and configuration registers (except sticky registers) initialize to their default conditions. | 设备的所有状态机、硬件逻辑、端口状态和配置寄存器（粘滞寄存器除外）均初始化为其默认条件。 |

| EN | ZH |
|---|---|
| ## Switches Generate Hot Reset on Downstream Ports | ## 交换机在下行端口上产生热复位 |
| A Switch generates a hot reset on all of its Downstream Ports when: | 交换机在以下情况下对其所有下行端口产生热复位： |
| • It receives a hot reset on its Upstream Port | • 在其上行端口上接收到热复位 |
| For a Switch or Bridge Upstream Port, if the Data Link Layer reports a DL\_Down state, the effect is very similar to a hot reset. This can happen when the Upstream Port has lost its connection with an upstream device due to an error that is not recoverable by the Physical Layer or Data Link Layer. | 对于交换机或桥接器的上行端口，如果数据链路层报告DL\_Down状态，其效果与热复位非常相似。当上行端口因物理层或数据链路层无法恢复的错误而丢失与上游设备的连接时，可能发生此情况。 |
| Software sets the 'Secondary Bus Reset' bit of the Bridge Control configuration register associated with the Upstream Port, as shown in Figure 18‐3 on page 838. | 软件设置与上行端口相关联的桥接器控制配置寄存器的'Secondary Bus Reset'位，如第838页图18-3所示。 |

Figure 18‐3: Switch Generates Hot Reset on One Downstream Port | 图18‐3：交换机在一个下游端口上生成热复位
<img src="images/part05_ac4424b8e666fe39ee27dcf4ac43ce22c1d80f810b316aed7173b41441cdfb53.jpg" width="700" alt="">
Bridges Forward Hot Reset to the Secondary Bus

| EN | ZH |
|---|---|
| If a bridge such as a PCI Express‐to‐PCI(‐X) bridge detects a hot reset on its Upstream Port, it must assert the PRST# signal on its secondary PCI(‐X) bus, as illustrated in Figure 18‐4 on page 839. | 如果桥接器（如PCI Express到PCI(-X)桥接器）在其上行端口上检测到热复位，它必须在其次级PCI(-X)总线上断言PRST#信号，如第839页图18-4所示。 |

| EN | ZH |
|---|---|
| ## Software Generation of Hot Reset | ## 热复位(Hot Reset)的软件生成 |
| Software generates a Hot Reset on a specific port by writing a 1 followed by 0 to the 'Secondary Bus Reset' bit in the Bridge Control register of that associated port's configuration header (see Figure 18-5 on page 840). Consider the example shown in Figure 18-3 on page 838. Software sets the 'Secondary Bus Reset' register of Switch A's left Downstream Port, causing it to send TS1 Ordered Sets with the Hot Reset bit set. Switch B receives this Hot Reset on its Upstream Port and forwards it to all its Downstream Ports. | 软件通过在相应端口的配置头部的桥控制(Bridge Control)寄存器中的'Secondary Bus Reset'位先写入1再写入0，在特定端口上生成热复位(Hot Reset)(参见第840页图18-5)。考虑第838页图18-3所示的例子。软件设置交换机A左侧下行端口(Downstream Port)的'Secondary Bus Reset'寄存器，使其发送设置了热复位(Hot Reset)位的TS1有序集(Ordered Sets)。交换机B在其上行端口(Upstream Port)接收此热复位(Hot Reset)并将其转发至其所有下行端口(Downstream Port)。 |

Figure 18-4: Switch Generates Hot Reset on All Downstream Ports | 图18-4：交换机在所有下游端口上生成热复位

<img src="images/part05_544ddba1052f9bea5da80c6c54d2bda121a65e3b76ef07f07f04ddf10a341677.jpg" width="700" alt="">

| EN | ZH |
|---|---|
| If software sets the Secondary Bus Reset bit of a Switch's Upstream Port, then the switch generates a hot reset on all of its Downstream Ports, as shown in Figure 18-4 on page 839. Here, software sets the Secondary Bus Reset bit in Switch C's Upstream Port, causing it to send TS1s with the Hot Reset bit set on all its Downstream Ports. The PCIe-to-PCI bridge receives this Hot Reset and forwards it on to the PCI bus by asserting PRST#. | 如果软件设置交换机上行端口(Upstream Port)的Secondary Bus Reset位，则交换机将在其所有下行端口(Downstream Port)上生成热复位(Hot Reset)，如图18-4(第839页)所示。此处，软件设置交换机C上行端口(Upstream Port)中的Secondary Bus Reset位，使其在所有下行端口(Downstream Port)上发送设置了热复位(Hot Reset)位的TS1。PCIe到PCI桥接收此热复位(Hot Reset)并通过断言PRST#将其转发到PCI总线。 |
| Setting the Secondary Bus Reset bit causes a Port's LTSSM to transition to the Recovery state (for more on the LTSSM, see "Overview of LTSSM States" on page 519) where it generates the TS1s with the Hot Reset bit set. The TS1s are generated continuously for 2 ms and then the Port exits to the Detect state where it is ready to start the Link training process. | 设置Secondary Bus Reset位会导致端口的LTSSM转换到Recovery状态(有关LTSSM的更多信息，请参见第519页的"LTSSM状态概述")，并在该状态下生成设置了热复位(Hot Reset)位的TS1。TS1持续生成2ms，然后端口退出到Detect状态，准备开始链路训练(Link training)过程。 |

## PCI Express Technology | PCI Express 技术

| EN | ZH |
|----|----|
| The receiver of the Hot Reset TS1s (always downstream) will go to the Recovery state, too. When it sees two consecutive TS1s with the Hot Reset bit set, it goes to the Hot Reset state for a 2ms timeout and then exits to Detect. Both Upstream and Downstream Ports are initialized and end up in the Detect state, ready to begin Link training. If the downstream device is also a Switch or Bridge, it forwards the Hot Reset to its Downstream Ports as well, as shown in Figure 18-3 on page 838. | 热复位 TS1 的接收方（始终是下游）也将进入 Recovery 状态。当它看到连续两个设置了 Hot Reset 位的 TS1 时，会进入 Hot Reset 状态并持续 2ms 超时，然后退出到 Detect 状态。上游端口和下游端口均被初始化，最终处于 Detect 状态，准备开始链路训练。如果下游设备也是一个交换机或桥接器，它还会将热复位转发给其下游端口，如第 838 页的图 18-3 所示。 |

Figure 18-5: Secondary Bus Reset Register to Generate Hot Reset | 图18-5：用于生成热复位的次级总线复位寄存器

<img src="images/part05_5f36bbf2b146b6702c694fece8b578d7199248c4cba06826a582e175106f0951.jpg" width="700" alt="">

## Software Can Disable the Link | 软件可以禁用链路

| EN | ZH |
| :--- | :--- |
| Software can also disable a Link, forcing it to go into Electrical Idle and remain there until further notice. The reason for mentioning that at this point is that disabling the Link also has the effect of causing a Hot Reset on downstream components. Disabling is accomplished by setting the Link Disable bit in the Link Control Register of the Downstream Port, shown in Figure 18-6 on page 841. That causes the Port to go to the Recovery LTSSM state and begin sending TS1s with the Disable bit set. Since this can only be controlled for Downstream Ports if the Link has been disabled, this bit is reserved for Upstream Ports (such as Endpoints or Switch Upstream Ports). | 软件也可以禁用一条链路，使其进入电气空闲状态并保持该状态，直至另行通知。在此提及该点的原因是禁用链路还会导致下游组件上发生热复位。通过在向下游端口的链路控制寄存器中设置链路禁用位来实现禁用，如图18-6（第841页）所示。这会导致该端口进入Recovery LTSSM状态，并开始发送设置了Disable位的TS1。由于此功能只能在链路已被禁用的前提下对下游端口进行控制，因此该位对上游端口（如端点或交换机的上游端口）而言为保留位。 |

Figure 18-6: Link Control Register | 图18-6：链路控制寄存器

<img src="images/part05_caf069e9ea76648b307af6b281ae9604dfaf4305fe1bc7d1d5f121ad2508f4c9.jpg" width="700" alt="">

| EN | ZH |
| :--- | :--- |
| When the Upstream Port recognizes incoming TS1s with the Disabled bit set, its Physical Layer signals LinkUp=0 (false) to the Link Layer and all the Lanes go to Electrical Idle. After a 2ms timeout, an Upstream Port will go to Detect, but a Downstream Port will remain in the Disabled LTSSM state until directed to exit from it (such as by clearing the Link Disable bit), so the Link will remain disabled and will not attempt training until then. | 当上游端口识别到进入的TS1中设置了Disabled位时，其物理层向链路层发出LinkUp=0（假）信号，所有通道进入电气空闲状态。经过2ms超时后，上游端口将进入Detect状态，但下游端口将保持在Disabled LTSSM状态，直到被指示退出该状态（例如通过清除链路禁用位），因此链路将保持禁用状态，且在此之前不会尝试训练。 |

---

| EN | ZH |
|---|---|
| # Part part06 — `mindshare_part06_p0901-1057` | # 第06部分 — `mindshare_part06_p0901-1057` |

Figure 18‐7: TS1 Ordered‐Set Showing Disable Link Bit | 图18‐7：显示禁用链路位的TS1有序集
<img src="images/part06_280af5ed1cdc6b43ac8562ec897fb535910678f2c54921c3ccae916ec866e8cc.jpg" width="700" alt="">

## 18.3 Function Level Reset (FLR) | 18.3 功能级复位（FLR）

| EN | ZH |
|----|-----|
| The FLR capability allows software to reset just one Function within a multifunction device without affecting the Link that is shared by them all. Its implementation is strongly recommended but isn't required, so software would need to confirm its availability before attempting to use it by examining the Device Capabilities register, as shown in Figure 18-8 on page 843. If the Function-Level Reset Capability bit is set, then an FLR can be initiated by simply setting the Initiate Function-Level Reset bit in the Device Control Register as shown in Figure 18-9 on page 843. | FLR功能允许软件仅复位多功能设备中的单个功能，而不影响它们所共享的链路。强烈建议但非必须实现该功能，因此软件在使用前需通过检查设备能力寄存器（Device Capabilities register）来确认其可用性，如图18-8（第843页）所示。若功能级复位能力位（Function-Level Reset Capability bit）被置位，则只需设置设备控制寄存器（Device Control Register）中的发起功能级复位位（Initiate Function-Level Reset bit）即可发起FLR，如图18-9（第843页）所示。 |

Figure 18-8: Function-Level Reset Capability | 图18-8：功能级复位能力

Figure 18-9: Function-Level Reset Initiate Bit | 图18-9：功能级复位发起位
<img src="images/part06_a97cecf61c37d9c691fd8a564fa09dcf19c60336fb45f5d284d8d8125cbf36e9.jpg" width="700" alt="">

<img src="images/part06_47559ccd168332b4ba513e5542fb8fe1a293972e253b351ea1c9f6831a888a7f.jpg" width="700" alt="">

| EN | ZH |
|----|-----|
| The spec mentions a few examples that motivate the addition of FLR: | 规范中提到了几个促成FLR增加的示例： |
| 1. It can happen that software controlling a Function encounters a problem and is no longer operating correctly. Preventing data corruption necessitates a reset of that Function, but if other Functions within that device are still working properly it would nice to be able to reset just the one having trouble. | 1. 控制某个功能的软件可能遇到问题而无法正常运行。为防止数据损坏，需要复位该功能，但如果该设备内的其他功能仍在正常工作，最好能仅复位出现故障的那个功能。 |
| 2. In a virtualized environment, where applications can migrate from one piece of hardware to another, it's important that when an application is moved off a Function that the Function doesn't retain any information about what it was doing. This prevents information used by one application that might be considered confidential from becoming visible to the new one running on that Function. The simplest way to clean up after migrating the previous application is simply to reset the Function. | 2. 在虚拟化环境中，应用程序可以从一个硬件迁移到另一个硬件。当应用程序移出一个功能时，该功能不应保留其正在执行的任何信息，这一点非常重要。这可以防止某一应用程序所使用的可能被视为机密的信息，对运行在该功能上的新应用程序可见。迁移完前一应用程序后，清理的最简单方法就是直接复位该功能。 |
| 3. When software is rebuilding a software stack for a Function, it is sometimes necessary to first put the Function into an uninitialized state. As before, avoiding a reset of all Functions sharing the Link is desirable. | 3. 当软件为某个功能重建软件栈时，有时需要先将该功能置于未初始化状态。与之前一样，最好避免复位共享链路的所有功能。 |
| Another feature doesn't appear in the list of cases in the spec but is still a motivating factor in its own right. While a conventional reset will re-initialize everything within the device, it does not require that all external activity, such as traffic on a network interface, must cease right away. FLR adds this requirement and is the only reset that does. | 另一个未出现在规范示例列表中但仍然是一个推动因素的特性是：传统复位会重新初始化设备内所有内容，但并不要求所有外部活动（如网络接口上的流量）必须立即停止。FLR增加了这一要求，并且是唯一这样做的复位类型。 |
| FLR resets the Function's internal state and registers, making it quiescent, but doesn't affect any sticky bits, or hardware-initialized bits, or link-specific registers like Captured Power, ASPM Control, Max\_Payload\_Size or Virtual Channel registers. If an outstanding Assert INTx interrupt message was sent, a corresponding Deassert INTx message must be sent, unless that interrupt was shared by another Function internally that still has it asserted. All external activity for that Function is required to cease when an FLR is received. | FLR复位功能的内部状态和寄存器，使其进入静默状态，但不会影响任何粘滞位、硬件初始化位或链路特定的寄存器，如捕获电源（Captured Power）、ASPM控制（ASPM Control）、最大有效载荷大小（Max\_Payload\_Size）或虚通道（Virtual Channel）寄存器。如果已发送了未决的断言INTx中断消息（Assert INTx），则必须发送相应的解除断言INTx消息（Deassert INTx），除非该中断由内部另一功能共享且该功能仍保持断言状态。当收到FLR时，要求该功能的所有外部活动必须停止。 |

| EN | ZH |
|---|---|
| ## Time Allowed | ## 允许的时间 |
| A Function must complete an FLR within 100ms. However, software may need to delay initiating an FLR if there are any outstanding split completions that haven't yet been returned (indicated by the fact that the Transactions Pending bit remains set in the Device Status register). In that case, software must either wait for them to finish before initiating the FLR, or wait 100ms after FLR before attempting to re-initialize the Function. If this isn't managed, a potential data corruption problem arises: a Function may have split transactions outstanding but a reset causes it to lose track of them. If they are returned later they could be mistaken for responses to new requests that have been issued since the FLR. To avoid this problem, the spec recommends that software should: | 一个功能必须在100ms内完成FLR。然而，如果有任何尚未返回的未完成拆分完成报文（由设备状态寄存器中的Transactions Pending位仍保持置位指示），软件可能需要延迟发起FLR。在这种情况下，软件必须在发起FLR之前等待它们完成，或者在FLR后等待100ms再尝试重新初始化该功能。如果未加管理，可能会产生潜在的数据损坏问题：一个功能可能有未完成的拆分事务，但复位导致其丢失对这些事务的跟踪。如果这些完成报文稍后返回，它们可能被误认为是针对FLR后发出的新请求的响应。为避免此问题，规范建议软件应： |
| 1. Coordinate with other software that might access the Function to ensure it doesn't attempt access during the FLR. | 1. 与可能访问该功能的其他软件协调，确保其在FLR期间不尝试访问。 |
| 2. Clear the entire Command register, thereby quiescing the Function. | 2. 清除整个命令寄存器，从而使功能静止。 |
| 3. Ensure that previously-requested Completions have been returned by polling the Transactions Pending bit in the Device Status register until it's cleared or waiting long enough to be sure the Completions won't ever be returned. How long would be long enough? If Completion Timeouts are being used, wait for the timeout period before sending the FLR. If Completion Timeouts are disabled, then wait at least 100ms. | 3. 确保先前请求的完成报文已返回，通过轮询设备状态寄存器中的Transactions Pending位直到其被清除，或等待足够长的时间以确保完成报文不会再返回。多长才算足够长？如果使用了完成超时，在发送FLR之前等待超时周期。如果完成超时被禁用，则至少等待100ms。 |
| 4. Initiate the FLR and wait 100ms. | 4. 发起FLR并等待100ms。 |
| 5. Set up the Function's configuration registers and enable it for normal operation. | 5. 设置功能的配置寄存器并使其能够正常操作。 |
| When the FLR has completed, regardless of the timing, the Transaction Pending bit must be cleared. | 当FLR完成时，无论时间如何，必须清除Transaction Pending位。 |

## 18.3.2 Behavior During FLR | 18.3.2 FLR 期间的行为

| EN | ZH |
|----|----|
| The spec writers chose to describe the behavior of a Function reset in fairly broad terms so as not to preclude any internal steps that designers might wish to take. The following behaviors are listed in the spec: | 规范编写者选择以相当宽泛的术语描述功能复位的行为，以免限制设计者可能希望采取的任何内部步骤。规范中列出了以下行为： |
| The Function must not appear to an external interface as though it was an initialized adapter with an active host. The steps to ensure that all activity on external interfaces is terminated will be design specific. An example would be a network adapter that must not respond to requests that would require an active host during this time. | 功能不得在外部接口上表现为一个已初始化且具有活动主机的适配器。确保所有外部接口上的活动终止的步骤将因设计而异。例如，网络适配器在此期间不得响应需要活动主机的请求。 |
| The Function must not retain any software-readable state that might include secret information left behind by some previous use of the Function. For example, any internal memory must be cleared or randomized. | 功能不得保留任何可能包含先前使用该功能所遗留秘密信息的软件可读状态。例如，任何内部存储器必须被清除或随机化。 |
| • The Function must be configurable as normal by the next driver. | • 下一个驱动程序必须能够正常配置该功能。 |
| • The Function must return a completion for the configuration write that caused the FLR and then initiate the FLR. | • 功能必须返回一个完成报文以响应导致FLR的配置写入，然后启动FLR。 |
| **While an FLR is in progress:** | **当FLR正在进行时：** |
| Any requests that arrive are allowed to be silently discarded without logging them or signaling an error. Flow control credits must be updated to maintain the link operation, though. | 允许静默丢弃到达的任何请求，无需记录或发出错误信号。不过，必须更新流控信用以维持链路的运行。 |

## PCI Express Technology | PCI Express 技术

| EN | ZH |
|---|---|
| Incoming completions can be treated as Unexpected Completions or silently discarded without logging them or signaling an error. | 传入的完成报文可被视为意外完成报文或被静默丢弃，无需记录或发出错误信号。 |
| The FLR itself must be completed within the time described above, but further initialization after that could take longer. If a configuration Request comes in before initialization is completed, the Function must return a completion with CRS (Configuration Retry Status) status. Once a completion is returned with any other status, a CRS status will not be legal again until the Function is reset again. | FLR 本身必须在上述时间内完成，但后续的进一步初始化可能需要更长时间。如果在初始化完成前收到配置请求，该功能必须返回带有 CRS（配置重试状态）状态的完成报文。一旦以任何其他状态返回完成报文，在该功能再次被复位之前，CRS 状态将不再合法。 |

## 18.4 Reset Exit | 18.4 复位退出

| EN | ZH |
| --- | --- |
| After exiting the reset state, Link Training and Initialization must begin within 20 ms. Devices may exit the reset state at different times, since reset signaling is asynchronous, but must begin training within this time. | 退出复位状态后，链路训练与初始化必须在20毫秒内开始。由于复位信令是异步的，设备可能在不同时间退出复位状态，但必须在此时间内开始训练。 |
| To allow reset components to perform internal initialization, system software must wait for at least 100 ms from the end of a reset before attempting to send Configuration Requests to them. If software initiates a configuration request to a device after the 100 ms wait time, but the device still hasn't finished its self-initialization, it returns a Completion with status CRS. Since configuration Requests can only be initiated by the CPU, the Completion will be returned to the Root Complex. In response, the Root may re-issue the configuration Request automatically or make the failure visible to software. The spec also states that software should only use 100ms wait periods if CRS Software Visibility has been enabled, since long timeouts or processor stalls may otherwise result. | 为了允许复位组件执行内部初始化，系统软件必须在复位结束后至少等待100毫秒，然后才能尝试向其发送配置请求。如果软件在100毫秒等待时间后向设备发起配置请求，但设备尚未完成其自身初始化，则设备会返回一个状态为CRS的完成报文。由于配置请求只能由CPU发起，该完成报文将返回给根复合体。作为响应，根复合体可以自动重新发起配置请求，或将失败状态呈现给软件。规范还指出，仅当启用了CRS软件可见性后，软件才应使用100毫秒等待周期，否则可能导致长时间超时或处理器停滞。 |
| Devices are allowed a full 1.0 second (-0%/+50%) after a reset before they must give a proper response to a configuration request. Consequently, the system must be careful to wait that long before deciding that an unresponsive device is broken. This value is inherited from PCI and the reason for this lengthy delay may be that some devices implement configuration space as a local memory that must be initialized before it can be seen correctly by configuration software. Its initialization may involve copying the necessary information from a slow serial EEPROM, and so it might take some time. | 设备在复位后被允许有完整的1.0秒（-0%/+50%）的时间，之后才必须对配置请求给出正确响应。因此，系统必须谨慎等待这么长时间，然后才能判定无响应的设备已损坏。该值继承自PCI，如此长延迟的原因可能是某些设备将配置空间实现为本地存储器，必须先对其进行初始化，配置软件才能正确读取。其初始化可能涉及从慢速串行EEPROM复制必要信息，因此可能需要一些时间。 |