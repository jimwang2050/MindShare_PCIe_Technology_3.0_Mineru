## PCI Express 简介

PCI Express 相对其前代产品的并行总线模型,是一次重大变革。作为一种串行总线,它与早期 InfiniBand 或 Fibre Channel 等串行设计有更多共同之处,但在软件层面与 PCI 保持完全向后兼容。


---

## PCI Express 技术

与许多高速串行传输协议一样,PCIe 采用双向连接,能够同时收发信息。所使用的模式称为双单工 (dual-simplex) 连接,因为每个接口都包含一条单工发送路径和一条单工接收路径,如图 2-1(第 40 页)所示。由于两个方向上的流量可以同时传输,两个设备之间的通信路径在技术上属于全双工,但规范中使用"双单工"这一术语,因为它更能准确地描述实际存在的通信信道。

图 2-1:双单工链路 (Dual-Simplex Link)
![](images/part01_65b78af38b282e69f5fdeb21d0deaaed27d55c195d68a17adf0b5efaf114013c.jpg)

设备之间这条路径的术语称为链路 (Link),由一组或多组发送与接收对组成。每一组这样的发送/接收对称为一条通道 (Lane),规范允许一条 Link 由 1、2、4、8、12、16 或 32 条通道 (Lane) 组成。通道的数量称为链路宽度 (Link Width),表示为 x1、x2、x4、x8、x16 和 x32。关于在具体设计中应选用多少通道,权衡非常简单:通道越多,链路 (Link) 的带宽越大,但成本、占板面积和功耗也会相应增加。更多相关内容,请参见第 46 页的"链路与通道"。

图 2-2:一条通道 (One Lane)
![](images/part01_d306bee7ca3c426ae22abbd7183cdcc877f14259eb84ed016a9ecf23cb33f97b.jpg)

---

## 软件向后兼容性

PCIe 最重要的设计目标之一是与 PCI 软件保持向后兼容。要推动业界从一种已经在现有系统中部署并正常运行的设计中迁移,需要满足两个条件:第一,提供一种引人注目的改进,值得用户考虑做出改变;第二,尽可能降低迁移的成本、风险和工作量。在计算机领域,帮助实现第二点的常见做法是保持针对旧模型编写的软件在新模型上仍然可用。为了在 PCIe 上实现这一点,PCI 所使用的所有地址空间要么原样保留,要么仅做简单的扩展。Memory(内存)、IO 和 Configuration(配置)空间对软件依然可见,编程方式也与以前完全相同。因此,多年前为 PCI 编写的软件(BIOS 代码、设备驱动程序等)如今仍可在 PCIe 设备上正常工作。Configuration 空间经过大幅扩展,增加了许多新寄存器以支持新增功能,但原有的寄存器仍然存在,并能通过常规方式访问(参见第 49 页的“软件兼容性特性”)。

## 串行传输


---

## 对速度的需求

当然,串行模型必须比并行设计运行得快得多才能达到相同的带宽,因为它一次只能发送一位。不过这并不困难,过去 PCIe 已能够在 2.5 GT/s 和 5.0 GT/s 下稳定工作。这些速度以及更高的速度(8 GT/s)之所以能够实现,是因为串行模型克服了并行模型的缺陷。

**克服问题。** 简单回顾一下,有几个问题会限制并行总线的性能,其中三个如图 2-3(第 42 页)所示。首先,回想一下并行总线使用公共时钟:发送器在某个时钟边沿将数据输出,接收器在下一个边沿将其锁存。该模型的一个问题是信号从发送器传输到接收器所需的时间,称为飞行时间(flight time)。飞行时间必须小于时钟周期,否则该模型将无法工作,因此缩短时钟周期具有挑战性。要做到这一点,走线必须更短、负载必须更小,但这种方式最终会变得不切实际。另一个因素是时钟到达发送方和接收方的时间差,称为时钟偏移(clock skew)。PCB 布局设计人员努力将该值最小化,因为它会消耗时序裕量,但偏移永远无法彻底消除。第三个因素是信号偏移(signal skew),它指的是

## PCI Express Technology

在给定时钟下,所有信号到达时间的差异。显然,在所有比特都就位并稳定之前,数据无法被锁存,因此我们最终必须等待最慢的那一个。

图 2‐3:并行总线的局限性
![](images/part01_cad406f51fee6b3bdd083a43706ee08ceb147b9df21159602c9b3bd68b38cc3b.jpg)

像 PCIe 这样的串行传输是如何规避这些问题的?首先,飞行时间变得无关紧要,因为用于将数据锁存到接收器中的时钟实际上已经嵌入到数据流之中,不再需要外部参考时钟。因此,无论时钟周期有多小,或信号到达接收器需要多长时间,都不再重要,因为时钟与信号一起同时到达。出于同样的原因,也不存在时钟偏移,原因同样在于锁存时钟是从数据流中恢复出来的。最后,在单条通道 (Lane) 内,信号偏移被消除,因为一次只传输一个数据比特。如果采用多通道 (Lane) 设计,信号偏移问题会重新出现,但接收器会自动对其进行校正,并且能够补偿相当大的偏移。尽管串行设计克服了并行模型的许多问题,但它们自身也带来了一系列复杂性。尽管如此,正如我们稍后将看到的,这些解决方案是可控的,能够实现高速、可靠的通信。

带宽 (Bandwidth)。PCIe 所支持的高速率与宽链路 (Link) 的组合可以产生可观的带宽 (Bandwidth) 数字,如第 43 页的表 2‐1 所示。这些数字由比特率和总线特性推导而来。其中一个特性是,与许多其他串行传输一样,PCIe 的前两代使用一种称为 8b/10b 编码 的编码过程,它基于 8 比特输入生成 10 比特输出。尽管这会带来一定的开销,但这样做有几个充分的理由,我们稍后会看到。目前,只要知道发送一个字节的数据需要传输 10 个比特就够了。第一代 (Gen1 (2.5 GT/s),即 PCIe 规范 1.x 版本) 比特率为 2.5 GT/s,除以 10 意味着单条通道 (Lane) 就能达到 0.25 GB/s 的发送速率。

## 第二章:PCIe 架构概述

需要知道的是,发送一个字节的数据需要传输 10 个比特。第一代(Gen1 或 PCIe 规范 1.x 版本)的比特率为 2.5 GT/s,除以 10 意味着单条通道 (Lane) 能够发送 0.25 GB/s。由于链路 (Link) 允许同时进行发送和接收,聚合带宽 (Bandwidth) 可达该数值的两倍,即每条通道 (Lane) 0.5 GB/s。第二代(Gen2 或 PCIe 2.x)将频率翻倍,带宽也随之翻倍。第三代(Gen3 或 PCIe 3.0)再次将带宽翻倍,但这一次规范编写者选择不将频率翻倍。出于稍后将讨论的原因,他们选择仅将频率提升至 8 GT/s,并舍弃了 8b/10b 编码,转而采用另一种称为 128b/130b 编码的编码机制(有关详细信息,请参阅第 407 页"物理层——逻辑(Gen3)"章节)。表 2-1 汇总了所有当前可能组合下可用的带宽,并显示了该配置下链路 (Link) 能够提供的峰值吞吐。

表 2-1:各链路 (Link) 宽度下 PCIe Gen1、Gen2 和 Gen3 聚合带宽

<table><tr><td>链路 (Link) 宽度</td><td>x1</td><td>x2</td><td>x4</td><td>x8</td><td>x12</td><td>x16</td><td>x32</td></tr><tr><td>Gen1 (2.5 GT/s) 带宽 (GB/s)</td><td>0.5</td><td>1</td><td>2</td><td>4</td><td>6</td><td>8</td><td>16</td></tr><tr><td>Gen2 (5.0 GT/s) 带宽 (GB/s)</td><td>1</td><td>2</td><td>4</td><td>8</td><td>12</td><td>16</td><td>32</td></tr><tr><td>Gen3 (8.0 GT/s) 带宽 (GB/s)</td><td>2</td><td>4</td><td>8</td><td>16</td><td>24</td><td>32</td><td>64</td></tr></table>

## PCIe 带宽计算

要计算上表中包含的带宽数值,可参见以下列出的计算过程。

Gen1 PCIe 带宽 = (2.5 Gb/s × 2 个方向) / 每个符号 10 bit = 0.5 GB/s。

Gen2 PCIe 带宽 = (5.0 Gb/s × 2 个方向) / 每个符号 10 bit = 1.0 GB/s。

请注意,在上述计算中,我们除以每个符号 10 bit 而不是每个字节 8 bit,这是因为 Gen1 和 Gen2 协议都要求数据包字节在发送之前使用 8b/10b 编码方案进行编码。


---

## PCI Express Technology

- Gen3 PCIe 带宽 (Bandwidth) = (8.0 Gb/s × 2 个方向) / 8 比特/字节 = 2.0 GB/s。

注意,在 Gen3 速率下,我们除以 8 比特/字节,而不是除以 10 比特/符号,因为在 Gen3 速率下,数据包 **不** 采用 8b/10b 编码,而是采用 128b/130b 编码。每 128 比特会产生额外的 2 比特开销,但其数量级不足以纳入此计算中。

> 译注:原文中的 "addition" 应为 "additional" 之误。

上述 3 个计算出的带宽数值需要乘以链路 (Link) 宽度,才能得到多通道 (Lane) 链路上的链路 (Link) 总带宽。

---

## 差分信号

每条 Lane 使用差分信号传输,发送同一信号的正、负两个版本(D+ 和 D‐),如图 2‐4(第 44 页)所示。这当然会使引脚数翻倍,但相对于单端信号传输,它具备两项对高速信号至关重要的明显优势:抗干扰能力更强、信号电压更低,从而抵消了引脚数增加的代价。

差分接收器同时接收两个信号,从正电压中减去负电压以求出两者之差,并据此判断该位的值。差分设计本身内置了抗干扰能力:成对的信号位于器件相邻引脚上,其走线也必须彼此紧邻布置,以维持合适的传输线阻抗。因此,任何影响其中一路信号的因素,通常也会以大致相同的幅度和相同的方向影响另一路。接收器观察的是两路之差,噪声并不会显著改变这一差值,所以大多数影响信号的噪声不会削弱接收器准确判别比特的能力。

图 2‐4:差分信号  
![差分信号](images/part01_19617ab8aabed3825fec312da2852c1cab58d1a4316c11531725e52085351821.jpg)


---

## No Common Clock

如前所述,PCIe 链路 (Link) 并不要求使用公共时钟,因为它采用的是源同步模型,即发送器 (Transmitter) 向接收器 (Receiver) 提供时钟,供其锁存传入数据。PCIe 链路中并不包含转发时钟 (forwarded clock)。取而代之的是,发送器借助 8b/10b 编码 (Encoding) 将时钟嵌入到数据流中。接收器随后从数据流中恢复出时钟,并用该时钟锁存传入数据。虽然听起来有点神秘,但这一过程实际上相当直接。在接收器中,一个 PLL 电路(锁相环,参见 45 页的图 2-5)将输入比特流作为参考时钟,并将其时序(即相位)与其自身以指定频率产生的输出时钟进行比较。根据比较结果,输出时钟的频率会被升高或降低,直至两者匹配。此时称 PLL 处于锁定状态,其输出(即恢复出的)时钟频率与发送数据所使用的时钟频率精确一致。PLL 会持续调整恢复时钟,因此由温度或电压变化引起的发送器时钟频率漂移始终会得到快速补偿。

关于时钟恢复有一点需要注意:PLL 为了进行相位比较,确实需要输入信号上出现跳变。如果数据长时间没有任何跳变,PLL 就有可能逐渐偏离正确频率。为避免此问题,8b/10b 编码的设计目标之一就是确保比特流中不会出现超过 5 个连续的 1 或 0(更多细节请参见 380 页的"8b/10b Encoding")。

图 2-5:简单 PLL 框图  
![](images/part01_1ac5a5952da14d3c864dfd8ae7562de4296c023562e71158e645bcfaa523de03.jpg)

一旦时钟被恢复出来,它就被用来将传入数据流的各个比特锁存到串并转换器 (deserializer) 中。有时学生会问恢复出的时钟能否用来给接收器中的所有逻辑提供时钟,但答案其实是否定的。原因之一是,接收器无法保证该参考时钟始终存在,因为链路 (Link) 的低功耗状态需要停止数据传输。因此,接收器还必须拥有自己可在本地生成的内部时钟。

---

## 基于报文包的协议 (Packet-based Protocol)

从并行传输转向串行传输,可以大幅减少传输数据所需的引脚数。PCIe 与大多数其他基于串行的协议一样,还通过消除并行总线中常见的大多数边带控制信号来减少引脚数。然而,如果没有任何控制信号来指示所接收信息的类型,接收器如何解释输入的比特呢?PCIe 中的所有事务都以称为报文包 (packet) 的定义结构进行发送。接收器找到报文包的边界,并根据已知的预期模式对报文包结构进行解码,以确定它应当如何处理。

基于报文包的协议的具体细节将在第 169 页的 “TLP 元素 (TLP Elements)” 一章中介绍,各种报文包类型及其用途的概述可在本章中找到;请参见第 72 页的 “数据链路层 (Data Link Layer)”。

## 链路与通道

如前所述,两个 PCIe 设备之间的物理连接称为链路 (Link),由一条或多条通道 (Lane) 组成。每条通道包含一组差分的发送与接收信号对,如图 2‐2(第 40 页)所示。一条通道足以满足设备之间的所有通信需求,无需其他信号。

## 可扩展的性能

然而,使用更多通道(Lane)将提升链路(Link)的性能,性能取决于其速率与链路宽度(Link width)。例如,使用多个通道可增加每个时钟周期能够发送的比特数,从而提高带宽。如前文第 43 页的表 2-1 所示,规范支持的通道数为 2 的幂次,最高 32 条通道。同时也支持 x12 链路,这可能是为了兼容早期串行设计 InfiniBand 所使用的 x12 链路宽度。允许多种链路宽度使平台设计者能够在成本与性能之间进行恰当的权衡,并可根据通道数方便地向上或向下扩展。

## 灵活的拓扑选项

由于 PCIe 所使用的传输速率非常高,链路 (Link) 必须是点对点连接,而不能像 PCI 那样采用共享总线。由于一条链路 (Link) 一次只能连接两个接口,因此在构建一个稍微复杂的系统时,就需要一种能够将连接进行扇出的方式。PCIe 通过使用交换机 (Switch) 和桥 (Bridge) 来实现这一点,从而在构建系统拓扑 (Topology)——即系统中各元件之间的连接集合——时具有充分的灵活性。系统中各元件的定义以及一些拓扑示例将在下一节中给出。


---

## 一些定义

图 2‐6(第 47 页)给出了一个简单的 PCIe 拓扑 (Topology) 示例,可用于说明本节给出的一些定义。

图 2‐6:PCIe 拓扑 (Topology) 示例
![](images/part01_34a427996186c803b2803145ff8128e9ffca6b77a36205ada2f9edbabf07d2f8.jpg)


---

## 拓扑 (Topology) 特性

在图的顶部是一个 CPU。这里要说明的一点是,CPU 被视为 PCIe 层次结构的顶端。与 PCI 一样,PCIe 仅允许简单的树形结构,这意味着不允许出现环路或其他复杂拓扑。这样做是为了保持与 PCI 软件的向后兼容性,因为 PCI 软件使用简单的配置方案来跟踪拓扑,并且不支持复杂环境。

为了保持这种兼容性,软件必须能够以与以前相同的方式生成配置周期,并且总线拓扑必须与以前看起来相同。因此,软件期望找到的所有配置寄存器仍然存在,并且其行为方式与以往完全相同。稍后,在我们有机会定义更多术语之后,我们将回到这个讨论。

---

## Root Complex

CPU 与 PCIe 总线之间的接口可能包含多个组件(处理器接口、DRAM 接口等),甚至可能由多颗芯片组成。这一组组件统称为根复合体 (RC 或 Root)。RC 位于 PCI 反向树拓扑的"根"位置,代表 CPU 与系统其余部分进行通信。不过,规范并未对其进行严格定义,而是给出了一份必需和可选功能的清单。从广义上讲,根复合体可以理解为系统 CPU 与 PCIe 拓扑之间的接口,其 PCIe Port 在配置空间中标记为"Root Port"。

---

## 交换机 (Switch) 与桥 (Bridge)

交换机 (Switch) 提供扇出或汇聚能力,允许将更多设备挂接到同一个 PCIe 端口 (Port) 上。交换机充当报文路由器的角色,并根据地址或其他路由信息识别给定报文需要走的路径。

桥 (Bridge) 提供与其他总线(如 PCI 或 PCI-X),甚至另一条 PCIe 总线的接口。第 47 页"PCIe 拓扑示例"中所示的桥有时称为"正向桥 (forward bridge)",允许将较旧的 PCI 或 PCI-X 卡插入到新系统中。反之,"反向桥 (reverse bridge)"则允许将新的 PCIe 卡插入到旧的 PCI 系统中。

## 原生 PCIe 端点与遗留 PCIe 端点

端点 (Endpoint) 是 PCIe 拓扑中既不是交换机 (Switch) 也不是桥的设备,作为总线上事务的发起者和完成者 (Completer)。它们位于树状拓扑各分支的末端,且仅实现一个上游端口 (Upstream Port)(朝向根复合体)。相比之下,交换机 (Switch) 可以有多个下游端口 (Downstream Port),但只能有一个上游端口 (Upstream Port)。那些为老旧总线(如 PCI‐X)运行而设计、但现在具备 PCIe 接口的设备,会在配置寄存器中将自己标识为"遗留 PCIe 端点 (Legacy PCIe Endpoint)",并且此类拓扑中会包含这种设备。它们会使用一些在新 PCIe 设计中已被禁止的特性,例如 IO 空间以及对 IO 事务或锁定请求 (Locked Request) 的支持。与此相反,"原生 PCIe 端点 (Native PCIe Endpoint)"则是完全为 PCIe 而设计的设备,而不是在老 PCI 设备设计上添加一个 PCIe 接口。原生 PCIe 端点 (Native PCIe Endpoint) 设备是内存映射设备(MMIO 设备)。


---

## 软件兼容性特征

保持与旧版软件兼容的一种方式是:图 2-7(第 50 页)中所示的 Endpoint 与桥的配置 Header 与 PCI 完全相同。一个区别是,现在桥常常被聚合进 Switch 与 Root 中,但旧版软件并不会感知这一差异,仍然只是把它们视为桥。在这一点上,我们只想先熟悉这些概念,不会在此处深入寄存器细节。关于配置这一相当庞大的主题的介绍,可参见第 85 页的"Configuration 概述"。

图 2-7:配置 Header  
![](images/part01_4598ae3c1199ed477d3ccef20aaef66e7b609af082432a00b29e46209ac766a4.jpg)

为了说明系统在软件中呈现的方式,请考虑图 2-8(第 51 页)中所示的拓扑示例。如前所述,Root 位于分层结构的顶端。Root 在内部可能相当复杂,但通常会实现一个内部总线结构并通过若干桥将拓扑扇出到多个端口。该内部总线在配置软件看来是 PCI 总线号 0,而各 PCIe Port 则呈现为 PCI-to-PCI 桥。这种内部结构很可能并不是真正的 PCI 总线,但在软件看来就是如此。由于该总线位于 Root 内部,其实际的逻辑设计不必遵循任何标准,可以是厂商特定的。

图 2-8:拓扑示例  
![](images/part01_72ed8540ba3dab1abb3d98bb1818bcb24326ec6e6cb2dfa7aa26bc280a051ec7.jpg)  
类似地,图 2-9(第 52 页)中所示的 Switch 的内部组织对软件而言也只是共享同一总线的若干桥的集合。这种做法的一个主要优势是,它允许事务路由沿用与 PCI 相同的方式。Enumeration(枚举,即配置软件发现系统拓扑并分配总线号与系统资源的过程)也以同样的方式进行。稍后我们会看到枚举工作方式的一些示例,但一旦枚举完成,系统中的总线号将按图 2-9(第 52 页)中所示的方式全部分配完毕。

图 2-9:系统 Enumeration 的示例结果  
![](images/part01_f638e407fa47fd789349bb4bcedad28fc44b8e09d34bb8bdc151b71785c20758.jpg)

## 系统示例

图 2-10 (第 53 页) 展示了一个面向低成本应用(如消费级台式机)的 PCIe 系统示例。系统中实现了若干 PCIe 端口以及少量扩展卡插槽,但其基本架构与老式 PCI 系统差别不大。

相比之下,图 2-11 (第 54 页) 所示的高端服务器系统则内置了其他网络接口。在 PCIe 早期发展阶段,业界曾考虑让它作为一种网络协议运行,从而取代这些较老的网络模型。毕竟,如果 PCIe 基本上是其他网络协议的简化版本,难道它不能满足所有需求吗?出于多种原因,这一构想始终未能真正获得发展动力,基于 PCIe 的系统目前通常仍需借助其他传输方式连接外部网络。

这也让我们有机会重新审视一个问题:什么构成根复合体 (Root Complex)。在本例中,标记为"Intel Processor"的模块包含了许多组件,这也是大多数现代 CPU 架构的共同特点。该处理器包含一个 x16 PCIe 端口用于连接图形设备,以及 2 条 DRAM 通道,这意味着内存控制器和部分路由逻辑已被集成到 CPU 封装内部。这些资源通常统称为"Uncore"(非核心)逻辑,以与封装内的若干 CPU 核心及其相关逻辑相区分。由于我们此前将根复合体 (Root) 描述为 CPU 与 PCIe 拓扑之间的接口,这意味着根复合体 (Root) 的部分必须位于 CPU 封装内部。如图 2-11 (第 54 页) 中的虚线所示,此处的根复合体 (Root) 由若干封装中的部分共同组成。在未来的许多系统设计中,这种情况很可能成为常态。

Figure 2‐10: Low‐Cost PCIe System  
![](images/part01_5ff8ff7874b46982636a2c89e9d372e5b202af4f26ccb619508231c3bf2581b6.jpg)

Figure 2‐11: Server PCIe System  
![](images/part01_25e684fbd36b47ce7c8b7ba7836b9a3abb02994b5d51c666d43805ed343231cb.jpg)

## 设备分层介绍

PCIe 定义了一种分层架构,如图 2‐12(第 56 页)所示。这些层在逻辑上可视为两个相互独立运行的部分,因为每一部分都包含用于出方向流量的发送侧和用于入方向流量的接收侧。这种分层方式对硬件设计者有一定优势:如果对逻辑进行合理划分,在迁移到规范的新版本时,只需修改现有设计的某一层而保持其他层不变,从而降低了迁移难度。尽管如此,必须强调的是,这些层只是定义了接口职责,设计并不要求必须按这些层进行划分才能符合规范。本节的目的是描述每一层的职责,以及完成一次数据传输所涉及的事件流。

如图 2‐12(第 56 页)所示,设备各层包括:

设备核心及与事务层的接口。核心实现设备的主要功能。若设备是端点(Endpoint),它最多可包含 8 个功能(functions),每个功能实现各自的配置空间。若设备是交换机(Switch),则交换机核心由报文路由逻辑以及用于完成该路由的内部总线组成。若设备是根复合体(Root),则根核心实现一个虚拟的 PCI 总线 0,所有芯片组内嵌的端点和虚拟桥都挂接在该总线上。

事务层 (Transaction Layer)。该层负责在发送侧创建事务层包 (TLP),在接收侧对 TLP 进行解码。该层还负责服务质量 (QoS) 功能、流控 (Flow Control) 功能以及事务排序功能。这四项事务层功能均将在本书第二部分中描述。

数据链路层 (Data Link Layer)。该层负责在发送侧创建数据链路层包 (DLLP),在接收侧进行解码。该层还负责链路的错误检测与纠正。该数据链路层功能被称为 Ack/Nak 协议。这两项数据链路层功能均将在本书第三部分中描述。

物理层 (Physical Layer)。该层负责在发送侧创建有序集 (Ordered‐Set) 报文,在接收侧对有序集报文进行解码。该层处理待发送的所有三类报文(TLP、DLLP 和有序集),并处理从链路上接收到的所有类型报文。在发送侧,报文由字节分发逻辑、加扰器、8b/10b 编码器(对应 Gen1/Gen2 协议)或 128b/130b 编码器(对应 Gen3 协议)以及报文串行化器进行处理。最终,报文以差分方式在已训练好的链路速率下、跨链路的所有通道 (Lane) 同步输出。在接收侧物理层,报文处理过程包括:串行接收差分编码比特并将其转换为数字格式,然后对输入的比特流进行解串。该过程以从 CDR(时钟数据恢复)电路中恢复出的时钟所派生的时钟频率运行。接收到的报文由弹性缓冲器、8b/10b 解码器(对应 Gen1/Gen2 协议)或 128b/130b 解码器(对应 Gen3 协议)、解扰器以及字节合路逻辑进行处理。最后,物理层的链路训练与状态机 (LTSSM) 负责链路的初始化与训练。所有这些物理层功能均将在本书第四部分中描述。

Figure 2‐12: PCI Express Device Layers  
![](images/part01_47b594d06dc401b1dd86f88ea3ba1a41b677ec3e156a5d1a5023a8ebf9bb5a74.jpg)

每个 PCIe 接口都支持上述各层的功能,包括交换机端口 (Switch Port),如图 2‐13(第 57 页)所示。在早期培训中经常出现的一个问题是:交换机端口是否需要实现所有这些层,因为它通常只是转发报文。答案是肯定的;其原因在于,要解析报文内容以决定其路由,必须深入查看报文的内部细节,而这一过程发生在事务层逻辑中。

Figure 2‐13: Switch Port Layers  
![](images/part01_e3fa1c34a3567a36d538a2d4befaf296a5a8dcf73d1b5f9156c39ec2574193d7.jpg)

原则上,每一层都与链路对端设备的对应层进行通信。上两层通过将一串比特组织为报文来实现通信,所生成的报文格式可被接收端的对应层识别。报文在到达或离开链路的过程中,会经过其他各层进行转发。物理层虽然也直接与对端设备的物理层通信,但其通信方式有所不同。

在我们深入探讨之前,先来通览一下各层之间的交互。从广义上讲,设备发出的请求或完成报文的内容,是由事务层根据设备核心逻辑(我们有时也称之为软件层,虽然规范中并未使用此术语)所提供的信息组装而成的。这些信息通常包括所期望的命令类型、目标设备的地址、请求的属性等。新创建的报文随后被存入一个称为虚通道 (Virtual Channel, VC) 的缓冲区中,直到可以传递给下一层。当报文被向下传递到数据链路层时,会附加额外的信息以便在相邻的接收端进行错误检查,并在本地保存一份副本,以便在发生传输错误时进行重传。当报文到达物理层后,会经过编码,并使用链路上的所有可用通道以差分方式发送出去。

Figure 2‐14: Detailed Block Diagram of PCI Express Device's Layers  
![](images/part01_b426a340ae362d5ecd38a466e8f6661c8d0a1467a519762768ce084a583b1bed.jpg)

接收端在物理层对输入比特进行解码,在该层检查可检测的错误,若没有错误,则将得到的报文向上转发到数据链路层。在数据链路层,报文将被检查是否存在其他错误,若没有错误则继续向上转发到事务层。报文在此被缓冲、进行错误检查,并被拆解为原始信息(命令、属性等),以便将内容交付给接收端的设备核心。接下来,让我们结合图 2‐14(第 58 页)更深入地探讨每一层为使该过程正常工作所必须完成的工作。我们从顶层开始。

---

## Device Core / Software Layer

This is the core functionality of the device, such as a network interface or hard drive controller. This isn't defined as a layer in the PCIe spec, but can be thought of in that way since it resides above the Transaction Layer and will be either the source or destination of all Requests. It provides the transmit side of the Transaction Layer with requests that include information like the transaction type, the address, amount of data to transfer, and so on. It's also the destination for information forwarded up from the Transaction Layer when incoming packets have been received.

---

## Device Core / 软件层

这是设备的核心功能,例如网络接口或硬盘控制器。它在 PCIe 规范中并未被定义为一个层,但可以这样理解,因为它位于事务层 (Transaction Layer) 之上,并将作为所有请求 (Request) 的源或目的。它为事务层的发送侧提供请求,这些请求中包含事务类型、地址、要传输的数据量等信息。当收到传入报文时,它也是事务层向上转发信息的目的地。

---

## 事务层

事务层根据软件层发来的请求生成出站报文。它也会检查入站报文,并将其中包含的信息向上转发到软件层。事务层支持 Non-Posted (无数据,需完成) 事务的分离事务协议,并将入站的完成报文 (Completion) 与先前发出的出站 Non-Posted 请求相关联。该层处理的各类事务使用 TLP(事务层报文)承载,可划分为以下四种请求类别:

1. Memory(内存)

2. IO(I/O)

3. Configuration (配置)

4. Messages(消息)

前三种在 PCI 和 PCI-X 中就已支持,而 Messages(消息)是 PCIe 新增的类型。一个事务 (Transaction) 的定义是:由 Requester 发出、用于将命令投递给目标设备的请求报文,加上目标设备随后回传的完成报文 (Completion)。请求类型列表见表 2-2(第 59 页)。

表 2-2:PCI Express 请求类型

<table><tr><td>请求类型</td><td>Non-Posted 或 Posted</td></tr><tr><td>Memory Read(内存读)</td><td>Non-Posted (无数据,需完成)</td></tr><tr><td>Memory Write(内存写)</td><td>Posted (有数据,无完成)</td></tr><tr><td>Memory Read Lock(内存读锁定)</td><td>Non-Posted (无数据,需完成)</td></tr><tr><td>IO Read(I/O 读)</td><td>Non-Posted (无数据,需完成)</td></tr><tr><td>IO Write(I/O 写)</td><td>Non-Posted (无数据,需完成)</td></tr><tr><td>Configuration Read(配置读,Type 0 与 Type 1)</td><td>Non-Posted (无数据,需完成)</td></tr><tr><td>Configuration Write(配置写,Type 0 与 Type 1)</td><td>Non-Posted (无数据,需完成)</td></tr><tr><td>Message(消息)</td><td>Posted (有数据,无完成)</td></tr></table>

如表中右列所示,这些请求还分属两大类:Non-Posted 和 Posted。对于 Non-Posted 请求,Requester 发出报文后,Completer 必须以完成报文 (Completion) 形式返回响应。读者可能已意识到这就是从 PCI-X 继承而来的分离事务协议。例如,任何读请求都将是 Non-Posted,因为所请求的数据需要通过完成报文返回。或许出乎意料的是,IO 写和 Configuration 写同样是 Non-Posted。尽管它们随命令一起携带了数据,但这些请求仍然期望从目标端收到完成报文,以确认写数据确实已无错地抵达目的地。

与之相对,Memory 写和消息 (Message) 是 Posted 的,这意味着目标设备不会向 Requester 返回完成 TLP。Posted 事务可以提升性能,因为 Requester 无需等待应答,也不必承担完成报文的开销。其代价是:Requester 无法获知写入是否完成或是否出错。该行为继承自 PCI,业界仍认为其是合理的设计,理由是失败概率较小,而性能收益相当显著。需要注意的是,即使 Posted 写不需要完成报文,它仍参与数据链路层中的 Ack/Nak 协议,以保证报文可靠交付。更多内容请参见第 10 章"Ack/Nak 协议",第 317 页。


---

## TLP (Transaction Layer Packet) 基础

所有 PCIe 请求与完成报文类型的列表见第 61 页的表 2-3。

Table 2‐3: PCI Express TLP Types

<table><tr><td>TLP Packet Types</td><td>Abbreviated Name</td></tr><tr><td>Memory Read Request</td><td>MRd</td></tr><tr><td>Memory Read Request - Locked access</td><td>MRdLk</td></tr><tr><td>Memory Write Request</td><td>MWr</td></tr><tr><td>IO Read</td><td>IORd</td></tr><tr><td>IO Write</td><td>IOWr</td></tr><tr><td>Configuration Read (Type 0 and Type 1)</td><td>CfgRd0, CfgRd1</td></tr><tr><td>Configuration Write (Type 0 and Type 1)</td><td>CfgWr0, CfgWr1</td></tr><tr><td>Message Request without Data</td><td>Msg</td></tr><tr><td>Message Request with Data</td><td>MsgD</td></tr><tr><td>Completion without Data</td><td>Cpl</td></tr><tr><td>Completion with Data</td><td>CplD</td></tr><tr><td>Completion without Data - associated with Locked Memory Read Requests</td><td>CplLk</td></tr><tr><td>Completion with Data - associated with Locked Memory Read Requests</td><td>CplDLk</td></tr></table>

TLP 在发送器的事务层产生,并在接收器的事务层终止,如图 2-15(第 62 页)所示。数据链路层和物理层会在报文穿过发送器的各层时为其添加相应部分,然后在接收器处验证这些部分在链路 (Link) 上是否被正确传输。

Figure 2‐15: TLP Origin and Destination  
![](images/part01_2d93b227db3af60a5c879a305a9ce0c208c42e8ca62960cf8ba8cfc54eee0a3f.jpg)

TLP 报文组装 (Packet Assembly)。完整的 TLP 在链路上传输时,各组成部分的示意图见图 2-16(第 63 页)。从图中可见,报文的不同部分在每一层被分别添加。为了便于识别报文的构造过程,TLP 的不同部分采用颜色编码来表示其所属的层级:红色代表事务层,蓝色代表数据链路层,绿色代表物理层。

设备核心在事务层中送出用于组装 TLP 核心段 (core section) 所需的信息。每个 TLP 都会有一个包头 (Header),尽管其中一些(例如读请求)不携带数据。还可以计算并向报文追加一个可选的端到端 CRC (ECRC) 字段。CRC 是 Cyclic Redundancy Check(循环冗余校验)的缩写(或称 Code),几乎所有串行架构都采用它,原因很简单:它易于实现,却能提供非常健壮的检错能力。CRC 还能检测"突发错误",即一连串重复的错误位,最长可检测至 CRC 值长度(PCIe 为 32 位)。由于在发送长串比特时很容易遇到这种错误,因此这一特性对串行传输非常有用。ECRC 字段在报文发送端与接收端之间的所有服务点("服务点"通常指具有 TLP 路由选项的交换机 (Switch) 或根端口 (Root Port))之间保持原样透传,这使得在目的地可以验证沿途没有任何错误。

发送时,TLP 的核心段被转发到数据链路层,由其负责追加一个序列号 (Sequence Number) 和另一个称为链路 CRC (LCRC) 的 CRC 字段。LCRC 由相邻的接收器用于检查错误,并将该检查的结果通过该链路 (Link) 上每发送一个报文就回报给发送器一次。细心的读者可能会感到疑惑:既然强制的 LCRC 检查已经验证了跨链路的无误传输,那么 ECRC 还有何用处?其原因在于,仍然存在一处不对传输错误进行检查的地方,那就是报文的路由转发设备内部。报文到达后会在一个端口上检查错误,然后进行路由检查,当从另一个端口发出时,会重新计算并添加一个新的 LCRC 值。端口之间的内部转发有可能遭遇不被常规 PCIe 协议检查到的错误,这正是 ECRC 发挥作用的地方。

最后,生成的报文被转发到物理层,在那里会向报文添加其他字符,以告知接收器后续报文的情况。对于前两代 PCIe 而言,这些字符是添加在报文首尾的控制字符。对于第三代 PCIe,不再使用控制字符,而是在块上附加其他比特,用以提供关于报文所需的必要信息。然后,报文被编码,并通过所有可用的通道 (Lane) 以差分方式在链路上传输。

Figure 2‐16: TLP Assembly  
![](images/part01_f4dc1d23b9f282c911cca51857d4c8c6af625629d3f9fa72a3c80019e0584197.jpg)


---

## PCI Express Technology

TLP 报文拆解。当相邻的接收器 (Receiver) 看到传入的 TLP 比特流时,它需要识别并移除发送器 (Transmitter) 核心逻辑为恢复原始信息所添加的各个部分。如第 64 页的图 2‐17 所示,物理层 (Physical Layer) 会校验其中是否含有正确的 Start、End 等字符,并将它们移除,然后把 TLP 的剩余部分转发给数据链路层 (Data Link Layer)。该层首先检查 LCRC 与序列号 (Sequence Number) 是否存在错误。如果没有错误,它会从 TLP 中移除这些字段,并将 TLP 转发给事务层 (Transaction Layer)。如果接收方是交换机 (Switch),报文将在事务层 (Transaction Layer) 中被解析,以在 TLP 的包头 (Header) 中查找路由信息,并确定应将报文转发到哪个端口。即便交换机并非报文的目的端,它仍被允许在发现 ECRC 错误时进行检查并报告。然而,交换机不被允许修改 ECRC,因此真正的目标设备也能检测到该 ECRC 错误。

如果目标设备具备 ECRC 校验能力并已启用该功能,就可以检查 ECRC 错误。若该设备即为目标设备且未发现错误,ECRC 字段会被移除,只留下报文的包头 (Header) 和数据部分,随后被转发到软件层 (Software Layer)。

图 2‐17:TLP 拆解  
![](images/part01_03174f5c4603b31616bc41880229c0cb55362305b782e00f7b81d9cad5ed94fe.jpg)

## Non-Posted Transactions

普通读。图 2‐18(见第 65 页)展示了一个从端点 (Endpoint) 发送到系统内存的内存读请求示例。TLP 内容的详细讨论可参见第 169 页第 5 章"TLP 元素",但任何内存读请求中的一个重要部分是目标地址。内存请求的地址可以是 32 位或 64 位,并据此确定报文路由。在本例中,请求通过两台交换机 (Switch) 进行路由转发,最终上送至本例中作为目标 (即 Root) 的根复合体 (Root Complex)。Root 解码该请求并识别出报文中的地址指向系统内存时,便取回所请求的数据。为将这些数据返回给请求者,根端口 (Root Port) 的事务层会按需生成多个完成报文 (Completion),以将全部请求数据递交给请求者。PCIe 单报文最大数据载荷为 4 KB,但设备设计时常采用更小的载荷,因此返回大量数据时可能需要多个完成报文。

Figure 2‐18: Non‐Posted Read Example
![](images/part01_5452ecadcd1bba8bce5c5ea16df4ac668fffb978f89f3c92496aaf27a82c8f74.jpg)

这些完成报文也包含路由信息以引导其返回请求者,而请求者在原始请求中包含了用于此目的的"返回地址"。该"返回地址"实际上就是请求者在 PCI 规范中所定义的 Device ID,它由三项信息组合而成:系统中的 PCI 总线号、该总线上的设备号以及该设备内的功能号。这一总线号、设备号和功能号信息(有时缩写为 BDF)就是完成报文 (Completion) 用于返回原始请求者的路由信息。与 PCI‐X 中一样,请求者可以同时有多个拆分事务在执行,并且必须能够将收到的完成报文与对应的请求相匹配。为支持此功能,原始请求中新增了一个称为 Tag 字段 (标签) 的值,该值对每个请求都是唯一的。完成者复制该事务 Tag 字段并在完成报文中使用,以便请求者能够快速识别该完成报文所服务的是哪一个请求。

最后,完成者还可以通过设置完成状态字段中的位来指示错误条件。这至少能让请求者大致了解可能发生了什么错误。请求者如何处理这些错误大多由软件决定,这已超出 PCIe 规范的范围。

锁定读。锁定内存读用于支持所谓的原子读改写 (Atomic Read‐Modify‐Write) 操作,这是处理器用于诸如测试并设置信号量等任务的一种不可打断的事务。在测试并设置进行期间,不能对信号量发起其他访问,否则可能产生竞争条件。为防止这种情况,处理器使用锁指示(例如并行前端总线上的一个独立引脚),在该锁定事务完成前阻止总线上的其他事务。此处仅给出该主题的高层介绍,关于锁定事务的更多信息,请参见第 963 页的附录 D"附录 D: 锁定事务"。

从历史的角度看,在 PCI 的早期,规范编写者曾预期 PCI 会真正取代处理器总线。因此,处理器在总线上可能用到的特性(如锁定事务)也被纳入了 PCI 规范。然而,PCI 几乎从未被这样使用过,最终大部分处理器总线支持被取消。锁定周期则保留下来用于支持一些特殊场景,而 PCIe 为兼容遗留特性沿用了该机制。或许是为了加速其弃用,新的 PCIe 设备被禁止接受锁定请求;只有那些自识别为 Legacy 设备的设备才能合法接受锁定请求。在图 2‐19(见第 67 页)所示的示例中,请求者通过发送锁定请求 (MRdLk) 来启动该流程。根据定义,此类请求只允许来自 CPU,因此在 PCIe 中只有根端口 (Root Port) 才会发起这类请求。

锁定请求依据目标内存地址在拓扑中被路由,最终到达 Legacy 端点 (Endpoint)。当报文途经每个路由设备(即所谓的服务点)时,该报文的出口端口被锁定,这意味着在该路径解锁之前,不允许其他报文沿该方向通过。

Figure 2‐19: Non‐Posted Locked Read Transaction Protocol
![](images/part01_9452f6cc0a3e8b47afb255b29595483f8984e42f10efe820b785a81645045ed1.jpg)

当完成者收到报文并解码其内容后,会收集数据并生成一个或多个带数据的锁定完成报文。这些完成报文通过请求者 ID (Requester ID) 路由回请求者,其途经的每个出口端口也会被锁定。

若完成者遇到问题,则返回不带数据的锁定完成报文(原始读请求本应带有数据,若没有则表明出现了问题),状态字段将指示相应的错误信息。请求者会据此理解为锁定未成功,因此该事务将被取消,由软件决定下一步如何处理。

IO 和配置写。图 2‐20(见第 68 页)展示了一个 Non-Posted (无数据,需完成) 的 IO 写事务。与锁定请求类似,IO 周期在合法情况下也只能以 Legacy 端点为目标。该请求基于 IO 地址通过交换机 (Switch) 进行路由,直至到达目标端点。当完成者收到请求后,它接收数据并返回单个不带数据的完成报文以确认报文已被接收。完成报文中的状态字段将报告是否发生错误,若有错误,则由请求者的软件予以处理。

若完成报文报告无错误,请求者即知晓写数据已成功送达,该完成者后续指令序列中的下一步骤现在可以执行。这恰恰概括了 Non-Posted 写的动机:与内存写不同,仅知道数据将在未来的某一时刻送达是不够的;实际上,在确认数据已经送达之前,后续步骤在逻辑上无法执行。与锁定周期类似,Non-Posted 写也只能来自处理器。

Figure 2‐20: Non‐Posted Write Transaction Protocol
![](images/part01_97842da0ea4cf92dd317251ca0abc4bdd91ddecb6ee46dbda4c34ff55e078c3a.jpg)

## Posted Writes

内存写 (Memory Writes)。内存写始终是 Posted 的,永远不会收到完成报文。一旦请求被发出,Requester 不会等待任何反馈,而是直接继续处理下一个请求,既不花费时间也不消耗带宽来返回完成报文。因此,Posted 写比非 Posted 请求更快、效率更高,并能提升系统性能。如图 2-21(第 69 页)所示,报文使用其目标内存地址在系统中路由至 Completer。一旦某条链路 (Link) 成功发送该请求,该事务在该链路上即告完成,该链路即可用于其他报文。最终,Completer 接收数据,事务才真正结束。当然,这种方式存在一个权衡:由于不发送任何 Completion 报文,也就没有任何方式将错误报告回 Requester。如果 Completer 遇到错误,它可以记录该错误并向 Root 发送一条 Message 通知系统软件,但 Requester 无法看到该错误。

图 2-21:Posted 内存写事务协议  
![](images/part01_a5e7d7dd9c99f8f39e565e11c3b7da1e32a9cd97ab756fc884933b745181b666.jpg)

消息写 (Message Writes)。值得注意的是,与之前我们看到的其他请求不同,Message 存在多种可能的路由方式,Message 内部的一个字段会指示使用哪种类型。例如,有些 Message 是针对特定 Completer 的 Posted 写请求;有些则由 Root 广播到所有 Endpoint;还有一些由 Endpoint 发出后会自动路由到 Root。如需了解更多不同路由类型的详细信息,请参阅第 4 章《地址空间与事务路由》(第 121 页)。

Message 在 PCIe 中非常有用,有助于实现降低引脚数的设计目标。Message 消除了 PCI 用来报告中断、电源管理事件和错误等信息的边带信号 (side-band signals) 的需求,因为这些信息可以通过普通数据通路以报文的形式传递。

---

## Quality of Service (QoS)

PCIe 在设计之初便已考虑对时间敏感型事务的支持,例如流式音频或视频这类应用,要求数据必须及时送达才有意义。这被称为提供服务质量 (QoS),其实现依赖于若干机制。首先,软件通过设置包内一个 3 位字段——流量类 (TC, Traffic Class),为每个包分配优先级。一般来说,为包分配编号更高的 TC 意味着在系统中获得更高的优先级。其次,硬件为每个端口内置多个缓冲区,称为虚通道 (VC, Virtual Channel),包根据其 TC 被放入相应的缓冲区。第三,由于端口在某一时刻有多个缓冲区都拥有可发送的包,因此需要仲裁逻辑来在各个 VC 之间进行选择。最后,交换机 (Switch) 必须在竞争访问同一输出端口 VC 的多个输入端口之间作出选择。这称为端口仲裁 (Port Arbitration),可以是硬件固定分配,也可以由软件编程设置。所有这些硬件机制必须就位,系统才能对包进行优先级排序。若编程和配置得当,这样的系统甚至可以为特定路径提供有保证的服务。

为了说明这一概念,请参考第 71 页的图 2‐22,其中摄像机和 SCSI 设备都需要向系统 DRAM 发送数据。区别在于摄像机数据具有时间敏感性;若到目标设备的传输路径无法跟上其带宽,帧就会被丢弃。系统必须能够保证至少与摄像机带宽相当的速率,否则采集到的视频可能出现卡顿。与此同时,SCSI 数据需要无误地送达,但耗时多久并不重要。因此,当视频数据包和 SCSI 包同时需要发送时,显然视频流量应具有更高的优先级。QoS 是指系统为包分配不同优先级、并以确定性时延和带宽在拓扑中路由的能力。有关 QoS 的更多细节,请参阅第 245 页第 7 章"Quality of Service"。

图 2‐22:QoS 示例
![](images/part01_68913402a366d0cb0ac47ade82ed80c3126c8b2f21e71d0c60b67b3891f455ea.jpg)

## 事务排序

在同一个 VC (虚通道) 内,报文通常按照其到达的相同顺序流动,但该一般规则也存在例外。PCI Express 协议继承了 PCI 的事务排序模型,包括 PCI-X 架构所增加的针对宽松排序 (relaxed-ordering) 情况的支持。这些排序规则保证使用相同流量类别的报文能够以正确的顺序通过拓扑路由,从而避免潜在的死锁或活锁条件。值得注意的一点是,由于排序规则仅在同一 VC (虚通道) 内适用,而使用不同 TC 的报文不一定被映射到同一 VC (虚通道) 中,因此软件层面理解使用不同 TC 的报文之间不存在排序关系。该排序在事务层内的各个 VC (虚通道) 中得以维护。


---

## 流控 (Flow Control)

串行传输中常用的一种典型协议是:仅当接收方有足够的缓冲区空间来接收报文时,发送方才允许向其邻居发送报文。这样可以减少总线上因性能浪费而引发的事件,例如 PCI 所允许的断开与重试,从而将该类问题从传输层中彻底消除。其代价是,接收方必须足够频繁地上报其缓冲区空间以避免不必要的阻塞,而上报本身也会占用少量带宽。在 PCIe 中,这种上报是通过 DLLP (Data Link Layer Packets,数据链路层报文)来完成的,这一点我们将在下一节中介绍。其原因在于避免一种可能的死锁情形:如果使用 TLP,则当发送方自身的接收缓冲区已满时,将无法获取缓冲区大小的更新。而 DLLP 无论缓冲区状况如何,均可以正常发送与接收,从而避免了该问题。流控协议由硬件层自动管理,对软件透明。

图 2‐23:流控基础  
![](images/part01_34defad3d017482a1996623b249b74a472faaf7b5f7614f0334bcd86ea4ac153.jpg)

如图 2‐23(第 72 页)所示,接收器 (Receiver) 内部包含用于存放已接收 TLP 的 VC 缓冲区。接收器使用流控 DLLP 向发送器 (Transmitter) 通告这些缓冲区的大小。发送器会跟踪接收器 VC 缓冲区中的可用空间,所发送的报文数量不得超过接收器所能容纳的数量。随着接收器处理 TLP 并将其从缓冲区中移除,它会周期性地发送流控更新 DLLP (Flow Control Update DLLP),使发送器随时掌握最新的可用空间信息。如需了解更详细的内容,请参阅第 215 页第 6 章"Flow Control"。

## Data Link Layer

该逻辑负责链路 (Link) 管理,并执行三项主要功能:TLP 错误纠正、流控 (Flow Control) 以及部分链路 (Link) 电源管理。它通过生成 DLLP 来实现这些功能,如图 2-24(第 73 页)所示。


---

## DLLP (数据链路层报文)

DLLP 在一条链路 (Link) 上两个相邻设备的数据链路层之间传递。事务层 (Transaction Layer) 完全感知不到这些报文,它们仅在相邻设备之间传输,不会被路由到其他地方。与 TLP 相比,DLLP 体积很小(始终只有 8 字节),这是一件好事,因为它们是为维护链路协议而产生的开销。

图 2‐24:DLLP 的起点与终点  
![](images/part01_b30f53bdfa5d6e8ed045e64ede23898966683e806de825718d4cf1e83872d04e.jpg)

DLLP 组装。如图 2‐24(第 73 页)所示,DLLP 在发送器 (Transmitter) 的数据链路层产生,并由接收器 (Receiver) 的数据链路层消费。DLLP Core 后面会附加一个 16 位 CRC,以便在接收端检查错误。DLLP 的内容随后被转发到物理层,物理层会在报文两端各附加一个 Start 和 End 帧字符(针对前两代 PCIe),然后对其编码,并通过所有可用的通道 (Lane) 以差分方式在链路上发送。

DLLP 分解。当 DLLP 被物理层接收时,比特流会被解码,并去除 Start 和 End 帧字符。报文的其余部分被转发到数据链路层,数据链路层检查 CRC 错误,然后根据报文内容采取相应的动作。数据链路层就是 DLLP 的最终目的地,因此 DLLP 不会被进一步转发到事务层。

## Ack/Nak 协议

如图 2‐25(第 74 页)所示,错误纠正功能由基于硬件的自动重试机制提供。如图 2‐26(第 75 页)所示,每个外发的 TLP 都会添加 LCRC 和序列号 (Sequence Number),并在接收器 (Receiver) 处进行检查。发送器 (Transmitter) 的重放 (Replay) 缓冲区会保留每一个已发送 TLP 的副本,直到对端设备确认收到该 TLP。该确认由接收器发送一个 Ack DLLP(肯定确认)实现,其中携带其所收到的最后一个正确 TLP 的序列号 (Sequence Number)。当发送器 (Transmitter) 收到该 Ack 后,会将重放 (Replay) 缓冲区中具有该序列号 (Sequence Number) 的 TLP 及其之前所有已发送的 TLP 一并清除。

如果接收器 (Receiver) 检测到 TLP 错误,会丢弃该 TLP 并向发送器返回一个 Nak。发送器随后重放 (Replay) 所有未被确认的 TLP,以期在下一次重传时获得更好的结果。由于检测到的错误几乎都是瞬态事件,重放 (Replay) 通常能够纠正问题。该过程通常被称为 Ack/Nak 协议。

图 2‐25:数据链路层重放 (Replay) 机制
![](images/part01_1d0465b846db99c393d9b871470744aced9a9e0f97d9a2254be79fb289631762.jpg)

图 2‐26:数据链路层处的 TLP 与 DLLP 结构
![](images/part01_4b13cbcbba117e0b2830a1899a8f7f3d36a7c3b0c6edb4df39a94d21ad867746.jpg)

DLLP 的基本形式同样如图 2‐26(第 75 页)所示,由一个 4 字节的 DLLP 类型字段(可附带其他信息)和一个 2 字节的 CRC 组成。

图 2‐27(第 76 页)展示了一个跨交换机 (Switch) 的内存读操作示例。通常情况下,该场景的执行步骤如下:

1. 步骤 1a:请求者 (Requester) 发送一个内存读请求,并在自身的重放 (Replay) 缓冲区中保存一份副本。交换机 (Switch) 接收该 MRd TLP,并检查 LCRC 和序列号 (Sequence Number)。步骤 1b:未发现错误,因此交换机向请求者返回 Ack DLLP。请求者收到后,从重放 (Replay) 缓冲区中丢弃该 TLP 的副本。

2. 步骤 2a:交换机根据存储器地址进行路由,将该 MRd TLP 转发至正确的出端口 (Egress Port),并在出端口的重放 (Replay) 缓冲区中保存一份副本。完成者 (Completer) 接收该 MRd TLP 并检查错误。步骤 2b:未发现错误,因此完成者向交换机返回 Ack DLLP。交换机端口从重放 (Replay) 缓冲区中清除其保存的 MRd TLP 副本。

3. 步骤 3a:作为该请求的最终目的地,完成者检查 MRd TLP 中可选的 ECRC 字段。未发现错误,因此该请求被传递至核心逻辑。设备根据命令读取所请求的数据,并返回一个带数据的完成报文 (Completion with Data) TLP(CplD),同时在重放 (Replay) 缓冲区中保存一份副本。交换机接收 CplD TLP 并检查错误。步骤 3b:未发现错误,因此交换机向完成者返回 Ack DLLP。完成者从重放 (Replay) 缓冲区中丢弃 CplD TLP 的副本。

4. 步骤 4a:交换机解码 CplD TLP 中的请求者 ID (Requester ID) 字段,将报文路由至正确的出端口 (Egress Port),并在出端口的重放 (Replay) 缓冲区中保存一份副本。请求者接收 CplD TLP 并检查错误。

步骤 4b:未发现错误,因此请求者向交换机返回 Ack DLLP。交换机从重放 (Replay) 缓冲区中丢弃其 CplD TLP 的副本。请求者检查可选的 ECRC 字段,未发现错误,数据被上送至核心逻辑。

图 2‐27:使用 Ack/Nak 协议的非 Posted (Non‐Posted) 事务
![](images/part01_4ae1274d3c62e6cae58663f0ca6c06a4df881526c14c91a9ae452886aba66420.jpg)

## Flow Control

链路层 (Link Layer) 的第二个主要功能是流控 (Flow Control)。在上电或复位 (Reset) 之后,该机制由数据链路层 (Data Link Layer) 在硬件中自动初始化,并在运行期间持续更新。在 TLP 相关章节中已对该机制做过概述,此处不再重复。若要深入了解该主题,请参阅第 6 章"Flow Control",位于第 215 页。

## 电源管理 (Power Management)

最后,链路层同样参与电源管理 (Power Management),因为 DLLP 被用于传递与链路和系统电源状态相关的请求与握手。欲深入了解该主题,请参阅第 16 章“电源管理 (Power Management)”,位于第 703 页。

## 物理层 (Physical Layer)

---

## 概述

物理层是 PCIe 协议层级结构中的最底层,如图 2‐14 (第 58 页) 所示。TLP 和 DLLP 类型的报文包均从数据链路层向下转发到物理层,以便在链路上发送;同时在接收端又被向上转发到数据链路层。规范将物理层的讨论划分为两个部分:逻辑部分和电气部分,本书也沿用这一划分。逻辑物理层包含与报文包在链路上进行串行传输准备相关、以及将入站报文包恢复为原始形态的数字逻辑。电气物理层则是物理层中面向链路的模拟接口,由每个通道的差分驱动器和接收器组成。

## 物理层 - 逻辑子层

来自数据链路层的 TLP 和 DLLP 被送入物理层的一个缓冲区,在此为它们添加起始字符和结束字符,以便在接收端检测报文的边界。由于起始字符和结束字符出现在报文的两端,因此也称为"成帧"字符。图 2-28(第 77 页)中显示了附加在 TLP 和 DLLP 上的成帧字符,同时也展示了每个字段的大小。

图 2-28:物理层处的 TLP 和 DLLP 结构  
![](images/part01_c58f072a15f652ded0aceac01109da848c2e7a679bd4a382e0f70bae2257870a.jpg)

在该子层内,报文的每个字节会通过一个称为字节交叉(字节分条)的过程被拆分到链路正在使用的所有通道上。实际上,每条通道都作为穿越链路的一条独立串行通路来运行,所有通道的数据在接收端再重新聚合。每个字节都会被加扰,以减少传输线上的重复模式并降低链路上观察到的 EMI(电磁干扰)。对于 PCIe 的前两代(Gen1 和 Gen2 PCIe),8 位字符使用所谓的 8b/10b 编码逻辑被编码为 10 位"符号"。这种编码会为输出数据流带来额外开销,但同时也带来了一些有用的特性(详见第 380 页的"8b/10b 编码")。Gen3 物理层逻辑在以 Gen3 速率发送时,并不会使用 8b/10b 编码对报文字节进行编码,而是采用另一种称为 128b/130b 编码的方案,报文字节经加扰后被发送出去。然后,各通道上的 10b 符号(Gen1 和 Gen2)或报文字节(Gen3)被串行化,并以 2.5 GT/s(Gen1)、5 GT/s(Gen2)或 8 GT/s(Gen3)的速率,以差分方式在链路的每条通道上输出。

接收器以训练好的时钟速率,在所有通道上对到达的报文比特进行采样。如果使用 8b/10b 编码(在 Gen1 和 Gen2 模式下),报文的串行比特流会通过解串器转换为 10 位符号,以便进行 8b/10b 解码。然而,在解码之前,这些符号会经过一个弹性缓冲区——一种巧妙地用于补偿两个相连设备内部时钟之间细微频率差异的器件。接下来,10 位符号流通过 8b/10b 解码器被解码回正确的 8 位字符。Gen3 物理层逻辑在以 Gen3 速率接收报文串行比特流时,会使用一个已建立块锁定的解串器将其转换为字节流。该字节流会经过一个弹性缓冲区,以进行时钟容差补偿。由于以 Gen3 速率传送的报文不采用 8b/10b 编码,因此省略 8b/10b 解码阶段。所有通道上的 8 位字符被解扰,来自所有通道的字节被反交叉合并回单一字符流,最终,来自发送器的原始数据流被恢复出来。

## 链路训练与初始化

物理层的另一职责是链路上的初始化与训练过程。在这一全自动过程中,会执行若干步骤以使链路准备好正常工作,包括确定若干可选条件的状态。例如,链路宽度可以从 1 条通道到 32 条通道不等,并可能支持多种速率。训练过程将发现这些选项,并按状态机顺序遍历,以确定最佳的组合。在该过程中,会检查或建立若干条件以确保正确且最优的运行,包括:

• 链路宽度

• 链路数据速率

• 通道反转(Link Reversal)—— 通道以相反顺序连接

• 极性反转(Polarity Inversion)—— 通道极性反向连接

• 每通道的位锁定 —— 恢复发送器时钟

• 每通道的符号锁定 —— 在比特流中找到一个可识别的位置

• 多通道链路内通道对通道的去偏斜(De-skew)。

## 物理层 - 电气

链路 (Link) 上的物理发送端与接收端通过交流耦合 (AC-coupled) 链路相连，如图 2-29 (第 79 页) 所示。"AC-coupled"(交流耦合) 一词的含义是：在两个器件之间的物理路径上放置一个电容器，用于通过信号的高频 (AC) 分量，同时阻断低频 (DC) 分量。许多串行传输都采用这种方式，因为它允许发送端与接收端的共模电压 (即差分信号正负两路交叉点的电平) 互不相同，也就是说它们不需要具有相同的参考电压。当两个器件距离较近且位于同一机箱内时，这并不是什么大问题；但如果它们位于不同的建筑物中，要使两者拥有精确相同的公共参考电压将非常困难。

图 2-29: 物理层电气  
![](images/part01_f7a6ed1fb949a7e2d336cf74fcfd6bb7623029c1c62460d6f20f9fa133057f62.jpg)

---

## 有序集(Ordered Sets)

设备之间发送的最后一种流量类型仅涉及物理层。尽管接收器能够轻易识别这些信息,但从技术上讲它并不是数据包的形式,因为它没有起始字符和结束字符等结构。它被组织成所谓的有序集(Ordered Set),由发送器的物理层发起,在接收器的物理层终止,如图 2-30(第 80 页)所示。对于 Gen1 和 Gen2 数据速率,有序集以单个 COM 字符开头,后跟三个或更多其他字符,这些字符定义了要发送的信息。PCIe 中所用字符类型的命名规则在第 382 页的"字符表示法"中详细讨论;目前只需了解 COM 字符具有适合此用途的特性即可。有序集的大小始终是 4 字节的整数倍,示例如图 2-31(第 80 页)所示。在 Gen3 工作模式下,有序集的格式与上述 Gen1/Gen2 有所不同。相关内容将在第 505 页的第 14 章"链路初始化与训练(Link Initialization & Training)"中介绍。有序集始终在相邻设备处终止,不会通过 PCIe 结构进行路由转发。

Figure 2‐30: Ordered Sets Origin and Destination  
![](images/part01_66d3d75c287bad02c9558f911ba317ab6316bf563ad0d68c22eae1b4425882bb.jpg)

有序集用于链路训练(Link Training)过程,如第 505 页的第 14 章"链路初始化与训练(Link Initialization & Training)"中所述。它们还用于补偿发送器与接收器内部时钟之间的细微差异,这一过程称为时钟容差补偿(clock tolerance compensation)。最后,有序集还用于指示链路上低功耗状态的进入或退出。

Figure 2‐31: Ordered‐Set Structure  
![](images/part01_94a184797d8a62418f98923cc328ca7fef4f4555e29988d0531350e5288d1461.jpg)

## 协议回顾示例

至此,让我们通过一个示例来回顾整个链路 (Link) 协议,说明从请求者 (Requester) 发起一次内存读请求,直到它从完成者 (Completer) 处获得所请求的数据为止,期间所经历的各个步骤。

## Memory Read Request

在讨论的第一部分中,请参阅第 81 页的图 2-32。Requester 的 Device Core 或 Software Layer 向 Transaction Layer 发送一个 Request,并包含以下信息:32 位或 64 位内存地址、transaction type、以 dword 为单位计算的待读取数据量、traffic class、byte enables、attributes 等。

图 2-32:Memory Read Request 阶段  
![](images/part01_34f769f7dfc2736dc87c224e3be486badf3cb160102a504621d040e46945b775.jpg)

---

## PCI Express Technology

事务层使用这些信息来构建一个 MRd TLP。TLP 包格式的细节将在后文描述,但目前只需知道:会根据地址长度(32 位或 64 位)创建一个 3 DW 或 4 DW 的包头。此外,事务层还会将请求者 ID(总线号、设备号、功能号)添加到包头中,以便完成者可以据此返回完成报文。TLP 被放入相应的虚通道(VC)缓冲区中,等待其轮到的发送时机。一旦 TLP 被选中,流控 (Flow Control) 逻辑会确认邻居设备的接收缓冲区(VC)中有足够的可用空间,然后该存储器读请求 TLP 被发送到数据链路层。

数据链路层向该包添加一个 12 位的序列号 (Sequence Number) 和一个 32 位的 LCRC (链路 CRC) 值。该 TLP 的副本连同序列号和 LCRC 被存储在重放 (Replay) 缓冲区中,然后该包被转发到物理层。

在物理层中,起始字符和结束字符被添加到包中,之后该包按可用通道 (Lane) 进行字节分发、加扰以及 8b/10b 编码。最后,各 Lane 上的比特被串行化,并通过链路 (Link) 以差分形式发送到对端。

完成者将传入的比特流反串行化回 10 位符号,并使其通过弹性缓冲区。10 位符号被解码回字节,来自所有通道的字节被去扰和取消字节分发。起始字符和结束字符被检测并移除。TLP 的其余部分被向上转发到数据链路层。

完成者的数据链路层检查所接收 TLP 中的 LCRC 错误,并检查序列号以判断是否存在 TLP 缺失或乱序。若无错误,它会创建一个 ACK (确认),其中包含与读请求中所使用的相同序列号。计算一个 16 位 CRC 并附加到 ACK 内容上,从而构成一个 DLLP,该 DLLP 被送回物理层,由物理层添加正确的成帧符号,并将 ACK DLLP 发送给请求者。

请求者的物理层接收该 ACK DLLP,检查并移除其中的成帧符号,然后将其向上转发到数据链路层。如果 CRC 有效,它会将已确认的序列号与存储在重放缓冲区中的各 TLP 的序列号进行比较。与收到的 ACK 相对应的、所存储的存储器读请求 TLP 被识别出来,并从重放缓冲区中丢弃。如果请求者收到的是 Nak DLLP,则会重发一份所存储的存储器读请求 TLP。由于 DLLP 仅对数据链路层有意义,因此不会被转发到事务层。

除生成 ACK 外,完成者的链路层还会将该 TLP 向上转发到其事务层。在完成者的事务层中,该 TLP 被放入相应的 VC 接收缓冲区中等待处理。可选择性地执行 ECRC (端到端 CRC) 检查;若未发现错误,则包头中的内容(地址、请求者 ID、存储器读事务类型、所请求的数据量、业务类别等)被转发到完成者的软件层。

## 带数据的完成报文 (Completion with Data)

本节的后半部分讨论请参阅第 83 页的图 2-33。为了响应该内存读请求,完成方设备内核/软件层会向其事务层下发一个带数据的完成报文 (CplD) 请求,其中包含从原始内存读请求中复制的请求者 ID 和 Tag 字段、事务类型、完成报文头的其他部分内容,以及所请求的数据。

图 2-33:带数据的完成报文阶段  
![](images/part01_44abc929e33d3e9a3a65bda68f55cf9bcdd4234c7656778ecebe304461e5d4b0.jpg)

事务层使用这些信息构建 CplD TLP,该 TLP 始终具有 3 DW 的包头(它使用 ID 路由,因此永远不需要 64 位地址)。事务层还会将自身的完成方 ID 添加到包头中。该报文也会被放入相应的 VC 发送缓冲区,一旦被选中,流控 (Flow Control) 逻辑会验证邻近设备是否有足够的空间来接收该报文,确认后将报文向下传递到数据链路层。

与之前一样,数据链路层向报文添加一个 12 位的序列号 (Sequence Number) 和一个 32 位的 LCRC (链路 CRC)。带有序列号和 LCRC 的 TLP 副本会被存入重放 (Replay) 缓冲区,然后报文被转发到物理层。

与之前一样,物理层会向报文添加起始字符和结束字符,将其按字节拆分到可用通道 (Lane) 上,执行加扰,并进行 8b/10b 编码。最后,CplD 报文在所有通道上串行化,并通过链路 (Link) 以差分方式发送至相邻设备。

请求方将传入的串行比特流转换回 10 位符号,并将其送入弹性缓冲区。这些 10 位符号被解码回字节,去加扰并重组通道数据。起始字符和结束字符被检测并移除,得到的 TLP 被向上传递到数据链路层。

与之前一样,数据链路层检查接收到的 CplD TLP 中的 LCRC 错误,并检查序列号以发现缺失或乱序的 TLP。如果未发现错误,它会创建一个 Ack DLLP,其中包含与 CplD TLP 所使用的相同序列号。该 Ack DLLP 会附加一个 16 位 CRC,然后送回物理层,由物理层添加适当的成帧符号并将 Ack DLLP 发送给完成方。

完成方物理层检查并移除 Ack DLLP 中的成帧符号,将其余部分向上传递到数据链路层,由后者检查 CRC。如果未发现错误,它会将该序列号与重放缓冲区中存储的 TLP 的序列号进行比较。与接收到的 Ack 关联的、所存储的 CplD TLP 被识别后,该 TLP 会从重放缓冲区中丢弃。如果完成方接收到的是 Nak DLLP,则它会重新发送一份所存储的 CplD TLP 副本。

与此同时,请求方事务层在相应的虚通道 (VC) 缓冲区中接收 CplD TLP。事务层可以选择性地检查 ECRC (端到端 CRC) 错误。如果未发现错误,它会将包头内容和数据有效载荷(包括完成状态)转发给请求方软件层,至此流程结束。

---

# 3 Configuration (配置) 概述

## 上一章

上一章对 PCI Express 架构进行了全面的介绍,旨在作为一份"高层管理者视角"的概述。该章引入了规范中所描述的 PCIe 端口设计分层方法,介绍了各类报文类型以及事务协议。

## 本章

本章介绍 PCIe 环境中的 Configuration (配置)相关内容,包括:Function 的配置寄存器所实现的空间、如何发现 Function、如何生成与路由 Configuration 事务、PCI 兼容配置空间与 PCIe 扩展配置空间之间的差异,以及软件如何区分 Endpoint (端点)与 Bridge (桥)。

## 下一章

下一章将介绍 Function(功能设备)通过 Base Address Registers(BAR,基地址寄存器)请求内存或 IO 地址空间的目的与方法,以及软件如何对其进行初始化。本章还将介绍 Bridge(桥)的 Base/Limit(基址/上限)寄存器如何初始化,从而使 Switch(交换机)能够在 PCIe 互连中路由 TLP。

---

## Bus、Device 与 Function 的定义

与 PCI 一样,每个 PCIe Function 由其所驻留的 Device 以及 Device 所连接的 Bus 唯一标识。该唯一标识通常被称为 "BDF"(Bus/Device/Function)。Configuration (配置) 软件负责检测给定拓扑中的每一个 Bus、Device 与 Function (BDF)。下面的章节将围绕一个 PCIe 示例拓扑讨论 BDF 的主要特性。第 87 页的图 3-1 展示了一个 PCIe 拓扑,突出显示了示例系统中实现的 Bus、Device 与 Function。本章稍后将说明 Bus 号与 Device 号的分配过程。


---

## PCIe 总线

配置软件最多可以分配 256 个总线号。初始总线号 Bus 0 通常由硬件分配给根复合体 (Root Complex)。Bus 0 由一个虚拟 PCI 总线组成,其中包含集成端点 (integrated endpoint) 和虚拟 PCI-PCI 桥 (P2P),这些端点与桥的设备号和功能号是硬编码的。每个 P2P 桥都会创建一条新总线,其他 PCIe 设备可以连接到该总线上。每条总线必须被分配一个唯一的总线号。配置软件从 Bus 0、Device 0、Function 0 开始搜索桥,从而启动总线号分配过程。当找到一个桥时,软件为该桥所连接的新总线分配一个唯一的、且大于该桥所在总线号的总线号。一旦新总线被分配了总线号,软件在继续扫描当前总线上的其他桥之前,会先在新的总线上搜索桥。这种方法称为"深度优先搜索",在第 104 页的"枚举 (Enumeration) - 拓扑发现 (Discovering the Topology)"中对此进行了详细描述。

## PCIe 设备

PCIe 允许在单条 PCI 总线上最多挂接 32 个设备,但 PCIe 点对点的特性意味着每条 PCIe 链路只能直接连接一个设备,而且该设备始终会被编号为设备 0。根复合体 (Root Complex) 和交换机 (Switch) 拥有虚拟 PCI 总线,这类总线上确实允许多个设备"挂接"在总线上。每个设备必须实现 Function 0,并且可以包含最多 8 个 Function 的集合。当实现两个或更多 Function 时,该设备称为多功能设备 (multi-function device)。

## PCIe Functions

如前所述,每个 Device (设备) 都设计了 Function (功能)。这些 Function 可能包括硬盘接口、显示控制器、以太网控制器、USB 控制器等。具有多个 Function 的 Device 不必按顺序实现。例如,一个 Device 可能实现 Function 0、2 和 7。因此,当配置软件检测到多功能设备时,必须检查每个可能的 Function,以确定其中哪些存在。每个 Function 还拥有自己的配置地址空间,用于设置与该 Function 关联的资源。

图 3-1:系统示例
![](images/part01_796b26ae80ef8b4eae2285a9fc6e3e01a4e27dedd4ba1cd25a014299d25c40dc.jpg)

## Configuration Address Space

最早的 PC 要求用户通过设置开关和跳线来为每块已安装的扩展卡分配资源,这经常会导致内存、IO 和中断设置发生冲突。后续的 IO 架构,包括 Extended ISA (EISA) 和 IBM PS2 系统,是最早实现即插即用架构的架构。在这些架构中,每块插卡都附带配置文件,系统软件据此为其分配基本资源。PCI 通过实现标准化的 Configuration (配置)寄存器扩展了这一能力,使得通用的预包装操作系统可以管理几乎所有的系统资源。以一种标准化的方式启用 Error (错误)上报、中断交付、地址映射等功能,使得"配置软件"这一单一实体能够分配和配置系统资源,从而几乎消除了资源冲突。

PCI 为每个 Function (功能)定义了一段专用的 Configuration (配置)地址空间。映射到该 Configuration (配置)空间的寄存器允许软件发现 Function (功能)的存在,将其配置为正常工作状态,并检查其状态。需要标准化的大多数基本功能都位于 Configuration (配置)寄存器块的头部区域,但 PCI 的架构师们意识到,将可选功能标准化也是有益的,这些可选功能被称为能力结构 (capability structures,例如 Power Management (电源管理)、Hot-Plug (热插拔)等)。每个 Function (功能)的 PCI 兼容 Configuration (配置)空间大小为 256 字节。

## PCI 兼容空间 (PCI-Compatible Space)

在下面的讨论中请参考第 89 页的图 3‐2。PCI 兼容配置空间的 256 字节之所以这样命名,是因为它最初是为 PCI 设计的。该空间的前 16 个双字(64 字节)是配置包头(Header Type 0 或 Header Type 1)。每个 Function 都必须使用 Type 0 包头,但使用 Type 1 包头的桥 Function 除外。其余的 48 个双字用于可选寄存器,包括 PCI Capability 结构。对于 PCIe Function,某些 Capability 结构是必需的。例如,PCIe Function 必须实现以下 Capability 结构:

- PCI Express Capability

- Power Management

- MSI 和/或 MSI‐X

图 3‐2:PCI 兼容配置寄存器空间
![](images/part01_87179b365d2be6585bf707eba292ed9ce1ac72779bb7362e1133b3d921008c53.jpg)

---

## 扩展配置空间 (Extended Configuration Space)

本节讨论期间请参考第 90 页的图 3‐3。在 PCIe 问世之初,原有的 256 字节配置区域内没有足够的空间容纳所有新增的 Capability 结构。因此,配置空间的大小从每个 Function 256 字节扩展到 4 KB,这一区域称为扩展配置空间 (Extended Configuration Space)。960 dword 的扩展配置区域只能通过 Enhanced 配置访问机制访问,因此对传统 PCI 软件不可见。该区域包含了额外的可选 PCIe 扩展 Capability 寄存器,例如图 3‐3 中所列的那些(并非完整列表)。

图 3‐3:每个 PCI Express Function 的 4 KB 配置空间  
![](images/part01_1942869259537b7f4b2e0c2773f830739adecc65a9d75ed0e60a239556142560.jpg)

## Host-to-PCI Bridge 配置寄存器

## 概述

Host‐to‐PCI 桥的配置寄存器不要求必须通过上一节所述的两种配置机制中的任何一种来访问。取而代之的是,它通常以设备特定寄存器(device‐specific registers)的形式实现于内存地址空间中,该地址空间由平台固件所知晓。然而,其配置寄存器的布局与使用方式必须遵循 PCI 2.3 规范所定义的标准 Type 0 模板。

## 只有 Root 可以发起 Configuration 请求

规范规定,只有根复合体 (Root Complex) 才允许作为 Configuration 请求 (Configuration Request) 的发起方。根复合体充当系统处理器的联络者,负责将请求注入到 Fabric 中,并将完成报文 (Completion) 返回。由于具备发起配置事务的能力被限定为只能由处理器通过根复合体进行,从而避免了任何设备都能修改其他设备配置可能引发的混乱局面。

由于只有 Root 可以发起这些请求,因此它们只能向下游方向传输,这意味着不允许点对点的 Configuration 请求。请求根据目标设备的 ID 进行路由,即该设备的 BDF(拓扑中的 Bus 编号、该 Bus 上的 Device 编号以及该 Device 内的 Function 编号)。

## 生成 Configuration (配置) 事务

处理器通常无法直接发起 Configuration 读和写请求,因为它们只能生成内存和 IO 请求。这意味着根复合体 (Root Complex) 需要将其中的某些访问转换为配置请求,以支持该过程。Configuration 空间可通过以下两种机制中的任意一种进行访问:

- 传统 PCI 配置机制,使用 IO 间接访问。

- 增强型配置机制,使用内存映射访问。

---

## 传统 PCI 机制

PCI 规范定义了一种 IO 间接方法,用于指示系统(根复合体或等效实体)执行 PCI 配置访问。实际情况是,当时主流的 PC 处理器(Intel x86)只能寻址 64KB 的 IO 地址空间。在 PCI 规范定义之时,这有限的 IO 空间已经变得相当拥挤,仅剩少量地址范围可用:0800h - 08FFh 和 0C00h - 0CFFh。因此,把所有可能存在的功能(函数)的配置寄存器直接映射到 IO 空间并不现实。同时,内存地址空间的大小也有限,将整个配置空间映射到内存地址空间同样不被认为是理想的方案。于是规范编写者选择了一种常见的解决方案——使用间接地址映射。实现方式是:一个寄存器保存目标地址,另一个寄存器保存送往目标或来自目标的数据。先向地址寄存器执行一次写入,再向数据寄存器执行一次读或写,即可对目标功能的正确内部地址发起一次读或写事务。这种方式很好地解决了地址空间受限的问题,但也意味着需要两次 IO 访问才能完成一次配置访问。

PCI 兼容机制使用位于根复合体主机桥中的两个 32 位 IO 端口。它们分别是位于 IO 地址 0CF8h - 0CFBh 的 Configuration Address Port(配置地址端口),以及位于 IO 地址 0CFCh - 0CFFh 的 Configuration Data Port(配置数据端口)。

访问某个功能的 PCI 兼容配置寄存器的步骤是:首先将目标 Bus、Device、Function 以及 dword 编号写入 Configuration Address Port,并在此过程中设置其 Enable 位;然后向 Configuration Data Port 发起 1、2 或 4 字节的 IO 读或写操作。根复合体中的主机桥会将指定的目标总线与该桥下游存在的总线范围进行比较。若目标总线落在该范围内,桥便会发起一次配置读或写请求(具体取决于对 Configuration Data Port 的 IO 访问是读还是写)。

## Configuration Address Port(配置地址端口)

The Configuration Address Port only latches information when the processor performs a full 32‐bit write to the port, as shown in Figure 3‐4, and a 32‐bit read from the port returns its contents. The information written to the Configuration Address Port must conform to the following template (illustrated in Figure 3‐4) and described on the facing page.

Configuration Address Port 仅在处理器对该端口执行完整的 32 位写操作时才会锁存其信息(如图 3-4 所示);对该端口执行 32 位读操作则返回其内容。写入 Configuration Address Port 的信息必须符合以下模板(如图 3-4 所示,具体说明见对面页)。

Figure 3‐4: Configuration Address Port at 0CF8h

<table><tr><td>31</td><td>30</td><td>24</td><td>23</td><td>16</td><td>15</td><td>11</td><td>10</td><td>8</td><td>7</td><td>2</td><td>1</td><td>0</td></tr><tr><td></td><td colspan="2">Reserved(保留)</td><td>Bus Number(总线号)</td><td>Device Number(设备号)</td><td>Function Number(功能号)</td><td colspan="4">Doubleword(双字)</td><td>0</td><td>0</td><td></td></tr><tr><td colspan="13">Register pointer (64 DW) 寄存器指针(64 个双字)Should always be zeros 应始终为零Enable Configuration Space Mapping 使能配置空间映射1 = enabled 1 = 已使能</td></tr></table>

Bits [1:0] are hard‐wired, read‐only and must return zeros when read. The location is dword aligned and no byte‐specific offset is allowed.

位 [1:0] 为硬件连线、只读位,读时必须返回 0。该位置是双字对齐的,不允许使用字节级偏移。

Bits [7:2] identify the target dword (also called the Register Number) in the target Functionʹs PCI‐compatible configuration space. This mechanism is limited to the compatible configuration space (i.e., the first 64 doublewords of a Function’s configuration space).

位 [7:2] 用于标识目标 Function 的 PCI 兼容配置空间中的目标双字(也称为 Register Number)。此机制仅限于兼容配置空间(即 Function 配置空间的前 64 个双字)。

Bits [10:8] identify the target Function number (0  ‐  7) within the target device.

位 [10:8] 用于标识目标设备内的目标 Function 号(0 - 7)。

• Bits [15:11] identify the target Device number (0 ‐ 31).

• 位 [15:11] 用于标识目标 Device 号(0 - 31)。

• Bits [23:16] identify the target Bus number (0 ‐ 255).

• 位 [23:16] 用于标识目标 Bus 号(0 - 255)。

• Bits [30:24] are reserved and must be zero.

• 位 [30:24] 为保留位,必须为零。

Bit [31] must be set to 1b to enable translation of the subsequent IO access to the Configuration Data Port into a configuration access. If bit 31 is zero and an IO read or write is sent to the Configuration Data Port, the transaction is treated as an ordinary IO Request.

位 [31] 必须置为 1b,以使能将随后对 Configuration Data Port 的 IO 访问转换为配置访问。如果位 31 为 0,且向 Configuration Data Port 发起 IO 读或写,则该事务将被视为普通的 IO Request(请求)。

## 总线比较与数据端口使用

根复合体内的主桥(如图 3‐5,见第 95 页)实现了一个 Secondary Bus Number 寄存器和一个 Subordinate Bus Number 寄存器。Secondary Bus Number 是桥正下方那一级总线的总线号。Subordinate Bus Number 是位于该桥下游的目标总线号。

在单根复合体系统中,该桥的 Secondary Bus Number 寄存器可以是硬连线为 0 的寄存器、由复位强制为 0 的读写寄存器,也可以仅隐式地假定第一条可访问的总线将是 Bus 0。如果 Configuration Address Port(见图 3‐4,见第 92 页)中的第 31 位被设置为 1b,则桥会将目标总线号与下游总线的范围进行比较。

当看到一条 Request (请求)时,桥会判断目标总线号是否落在从 Secondary Bus number 到 Subordinate Bus number(含端点)范围内的下游总线号集合中。如果目标总线与 Secondary Bus 匹配,则该总线即为目标,Request 将以 Type 0 配置 (端点)的方式原样转发。当设备看到 Type 0 Request 时,它们就知道该总线上某个本地设备是目标设备(而不是下游从属总线上的某个设备)。

如果目标总线号大于桥的 Secondary Bus number,但小于或等于桥的 Subordinate Bus number,则该 Request 将以 Type 1 配置请求的形式在桥的 secondary bus 上转发。Type 1 配置访问的含义是:虽然该 Request 必须穿过本总线,但它并非以本总线上的某个设备为目标。相反,该 Request 将由本总线上某座桥转发到下游,而该桥的 Secondary 与 Subordinate 总线号范围中包含目标总线号。因此,只有桥设备会关注 Type 1 配置请求。有关 Type 0 与 Type 1 配置请求的更多信息,请参见第 99 页的"Configuration Requests"。


---

## Single Host System

写入 Configuration Address Port 的信息由 Root Complex 内的 Host/PCI bridge 锁存,如图 3-1(第 87 页)所示。如果 bit 31 为 1b,且目标总线在总线号的下游范围内,则 bridge 会将处理器后续对其 Configuration Data Port 的访问转换为总线 0 上的配置请求 (Configuration Request)。处理器随后向位于 0CFCh 的 Configuration Data Port 发起 IO 读或写事务。这会使 bridge 生成一个 Configuration Request:当对 Configuration Data Port 的 IO 访问是读时,该请求为配置读;当 IO 访问是写时,该请求为配置写。如果目标总线是总线 0,则为 Type 0 配置事务;如果目标总线是该范围内的其他总线,则为 Type 1 配置事务;如果目标总线不在该范围内,则该请求根本不会被转发。


---