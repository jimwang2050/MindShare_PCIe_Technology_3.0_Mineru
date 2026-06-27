# Ch19_Hot_Plug_Power_Budgeting

| EN | ZH |
|---|---|
| ## Usage Models | ## 使用模型 |

## 99.2.1 Intelligent Adapters | 99.2.1 智能适配器

| EN | ZH |
| --- | --- |
| Intelligent adapters are typically peripheral devices that use a local processor to offload tasks from the host. Examples of intelligent adapters include RAID controllers, modem cards, and content processing blades that perform tasks such as security and flow processing. Generally, these tasks are either computationally onerous or require significant I/O bandwidth if performed by the host. By adding a local processor to the endpoint, system designers can enjoy significant incremental performance. In the RAID market, a significant number of products utilize local intelligence for their I/O processing. | 智能适配器通常是利用本地处理器来卸载主机任务的外围设备。智能适配器的示例包括 RAID 控制器、调制解调器卡以及执行安全处理和流处理等内容处理刀片。通常，这些任务要么计算量繁重，要么若由主机执行则需要大量 I/O 带宽。通过在端点中添加本地处理器，系统设计人员可以获得显著的增量性能提升。在 RAID 市场中，相当多的产品利用本地智能进行其 I/O 处理。 |
| Another example of intelligent adapters is an ecommerce blade. Because general purpose host processors are not optimized for the exponential mathematics necessary for SSL, utilizing a host processor to perform an SSL handshake typically reduces system performance by over 90%. Furthermore, one of the requirements for the SSL handshake operation is a true random number generator. Many general purpose processors do not have this feature, so it is actually difficult to perform SSL handshakes without dedicated hardware. Similar examples abound throughout the intelligent adapter marketplace; in fact, this usage model is so prevalent that for many applications it has become the de facto standard implementation. | 智能适配器的另一个示例是电子商务刀片。由于通用主机处理器并未针对 SSL 所需的指数运算进行优化，因此利用主机处理器执行 SSL 握手通常会使系统性能降低 90% 以上。此外，SSL 握手操作的要求之一是需要一个真正的随机数生成器。许多通用处理器不具备此功能，因此没有专用硬件实际上很难执行 SSL 握手。类似的示例在智能适配器市场中比比皆是；事实上，这种使用模式非常普遍，以至于在许多应用中它已成为事实上的标准实现。 |

## 99.2.2 Host Failover | 99.2.2 主机故障切换

| EN | ZH |
|----|----|
| Host failover capabilities are designed into systems that require high availability. | 主机故障转移能力被设计到需要高可用性的系统中。 |
| High availability has become an increasingly important requirement, especially in storage and communication platforms. | 高可用性已成为日益重要的需求，尤其是在存储和通信平台中。 |
| The only practical way to ensure that the overall system remains operational is to provide redundancy for | 确保整个系统保持可运行状态的唯一实用方法是提供冗余，以 |

## Chapter : Appendix C: Implementing Intelligent Adapt- | 附录 C：实现智能适配器

| EN | ZH |
| --- | --- |
| all components. Host failover systems typically include a host based system attached to several endpoints. In addition, a backup host is attached to the system and is configured to monitor the system status. When the primary host fails, the backup host processor must not only recognize the failure, but then take steps to assume primary control, remove the failed host to prevent additional disruptions, reconstitute the system state, and continue the operation of the system without losing any data. | 所有组件。主机故障转移系统通常包括一个连接到多个端点（Endpoint）的主机系统。此外，一个备份主机连接到该系统，并被配置为监控系统状态。当主主机发生故障时，备份主机处理器不仅要识别出故障，还必须采取措施接管主控制权，移除故障主机以防止额外的中断，重建系统状态，并在不丢失任何数据的情况下继续系统的运行。 |

## 99.2.3 Multiprocessor Systems | 99.2.3 多处理器系统

| EN | ZH |
| --- | --- |
| Multiprocessor systems provide greater processing bandwidth by allowing multiple computational engines to simultaneously work on sections of a complex problem. | 多处理器系统允许多个计算引擎同时处理复杂问题的不同部分，从而提供更大的处理带宽。 |
| Unlike systems utilizing host failover, where the backup processor is essentially idle, multiprocessor systems utilize all the engines to boost computational throughput. | 与采用主机故障切换的系统（其中备份处理器基本处于空闲状态）不同，多处理器系统利用所有引擎来提高计算吞吐量。 |
| This enables a system to reach performance levels not possible by using only a single host processor. | 这使得系统能够达到仅使用单个主处理器无法实现的性能水平。 |
| Multiprocessor systems typically consist of two or more complete sub‐systems that can pass data between themselves via a special interconnect. | 多处理器系统通常由两个或更多完整的子系统组成，这些子系统之间可以通过特殊的互连传递数据。 |
| A good example of a multihost system is a blade server chassis. | 多主机系统的一个典型例子是刀片式服务器机箱。 |
| Each blade is a complete subsystem, often replete with its own CPU, Direct Attached Storage, and I/O. | 每个刀片都是一个完整的子系统，通常配备有自己的 CPU、直连存储和 I/O。 |

## 99.3 The History Multi-Processor Implementations Using PCI | 99.3 使用 PCI 的多处理器实现历史

| EN | ZH |
|---|---|
| To better understand the implementation proposed for PCI Express, one needs to first understand the PCI implementation. | 为了更好地理解PCI Express提出的实现方式，首先需要了解PCI的实现。 |
| PCI was originally defined in 1992 for personal computers. Because of the nature of PCs at that time, the protocol architects did not anticipate the need for multiprocessors. Therefore, they designed the system assuming that the host processor would enumerate the entire memory space. Obviously, if another processor is added, the system operation would fail as both processors would attempt to service the system requests. | PCI最初于1992年为个人计算机定义。由于当时PC的特性，协议架构师并未预见到多处理器的需求。因此，他们设计系统时假设主处理器将枚举整个内存空间。显然，如果添加另一个处理器，系统操作将会失败，因为两个处理器都会试图处理系统请求。 |
| Several methodologies were subsequently invented to accommodate the requirement for multiprocessor capabilities using PCI. The most popular implementation, and the one discussed in this paper for PCI Express, is the use of non-transparent bridging between the processing subsystems to isolate their memory spaces.<sup>1</sup> | 随后发明了多种方法来满足使用PCI实现多处理器能力的需求。最流行的实现方式——也是本文针对PCI Express所讨论的——是在处理子系统之间使用非透明桥接来隔离各自的内存空间。<sup>1</sup> |
| Because the host does not know the system topology when it is first powered up or reset, it must perform discovery to learn what devices are present and then map them into the memory space. To support standard discovery and configuration software, the PCI specification defines a standard format for Control and Status Registers (CSRs) of compliant devices. The standard PCI-to-PCI bridge CSR header, called a Type 1 header, includes primary, secondary and subordinate bus number registers that, when written by the host, define the CSR addresses of devices on the other side of the bridge. Bridges that employ a Type 1 CSR header are called transparent bridges. | 由于主机在首次上电或复位时不知道系统拓扑，它必须执行发现过程来了解存在哪些设备，然后将它们映射到内存空间中。为了支持标准的发现和配置软件，PCI规范为兼容设备的控制和状态寄存器(CSR)定义了标准格式。标准PCI到PCI桥的CSR头部称为Type 1头部，包含主总线号、次级总线号和从属总线号寄存器，当主机写入这些寄存器时，它们定义了桥另一侧设备的CSR地址。采用Type 1 CSR头部的桥称为透明桥。 |
| A Type 0 header is used for endpoints. A Type 0 CSR header includes base address registers (BARs) used to request memory or I/O apertures from the host. Both Type 1 and Type 0 headers include a class code register that indicates what kind of bridge or endpoint is represented, with further information available in a subclass field and in device ID and vendor ID registers. The CSR header format and addressing rules allow the processor to search all the branches of a PCI hierarchy, from the host bridge down to each of its leaves, reading the class code registers of each device it finds as it proceeds, and assigning bus numbers as appropriate as it discovers PCI-to-PCI bridges along the way. At the completion of discovery, the host knows which devices are present and the memory and I/O space each device requires to function. These concepts are illustrated in Figure C-0-1. | Type 0头部用于端点。Type 0 CSR头部包含基址寄存器(BAR)，用于向主机请求内存或I/O窗口。Type 1和Type 0头部都包含类别代码寄存器，指示所代表的是何种桥或端点，子类别字段以及设备ID和厂商ID寄存器提供进一步信息。CSR头部格式和寻址规则允许处理器搜索PCI层次结构的所有分支，从主桥向下直到每个叶子节点，在遍历过程中读取所发现的每个设备的类别代码寄存器，并在发现PCI到PCI桥时相应地分配总线号。发现过程完成后，主机知道存在哪些设备以及每个设备运行所需的内存和I/O空间。这些概念如图C-0-1所示。 |

Figure 0-1: Enumeration Using Transparent Bridges | 图0-1：使用透明桥的枚举

<img src="images/part06_f19b0d11bcc662e3364a706795525203cbb743404a04fb6c4daa834282b683f2.jpg" width="700" alt="">

## Implementing Multi-host | Intelligent Adapters in PCI Express Base Systems / 在 PCI Express 基础系统中实现多主机/智能适配器

| EN | ZH |
|---|---|
| Up to this point, our discussions have been limited to one processor with one memory space. As technology progressed, system designers began developing end points with their own native processors built in. The problem that this caused was that both the host processor and the intelligent adapter would, upon power up or reset, attempt to enumerate the entire system, causing system conflict and ultimately a non‑functional system. | 至此，我们的讨论仅限于单一处理器和单一存储器空间。随着技术的进步，系统设计人员开始开发内置自有处理器的端点。这带来的问题是，主机处理器和智能适配器在上电或复位时都会尝试枚举整个系统，导致系统冲突，最终使系统无法运行。 |
| To get around this, architects designed non‑transparent bridges. A non‑transparent PCI‑to‑PCI Bridge, or PCI Express‑to‑PCI Express Bridge, is a bridge that exposes a Type 0 CSR header on both sides and forwards transactions from one side to the other with address translation, through apertures created by the BARs of those CSR headers. Because it exposes a Type 0 CSR header, the bridge appears to be an endpoint to discovery and configuration software, eliminating potential discovery software conflicts. Each BAR on each side of the bridge creates a tunnel or window into the memory space on the other side of the bridge. To facilitate communication between the processing domains on each side, the non‑transparent bridge also typically includes doorbell registers to send interrupts from each side of the bridge to the other, and scratchpad registers accessible from both sides. | 为解决这一问题，架构师设计了非透明桥。非透明 PCI‑PCI 桥或 PCI Express‑PCI Express 桥是一种在两侧暴露 Type 0 CSR 头标，并通过这些 CSR 头标的基址寄存器（BAR）所创建的窗口，在两侧之间进行地址转换并转发事务的桥接器。由于暴露了 Type 0 CSR 头标，该桥接器对发现和配置软件而言表现为一个端点，从而消除了潜在的发现软件冲突。桥接器每一侧的每个 BAR 都在对侧存储器空间中创建一个隧道或窗口。为了便于两侧处理域之间的通信，非透明桥通常还包括门铃寄存器（用于从桥的一侧向另一侧发送中断）以及可从两侧访问的便签寄存器。 |
| A non‑transparent bridge is functionally similar to a transparent bridge in that both provide a path between two independent PCI buses (or PCI Express links). The key difference is that when a non‑transparent bridge is used, devices on the downstream side of the bridge (relative to the system host) are not visible from the upstream side. This allows an intelligent controller on the downstream side to manage the devices in its local domain, while at the same time making them appear as a single device to the upstream controller. The path between the two buses allows the devices on the downstream side to transfer data directly to the upstream side of the bus without directly involving the intelligent controller in the data movement. Thus transactions are forwarded across the bus unfettered just as in a PCI‑to‑PCI Bridge, but the resources responsible are hidden from the host, which sees a single device. | 非透明桥在功能上与透明桥类似，两者都在两条独立的 PCI 总线（或 PCI Express 链路）之间提供通路。关键区别在于，使用非透明桥时，桥接器下游侧（相对于系统主机）的设备对上游侧不可见。这使得下游侧的智能控制器可以管理其本地域中的设备，同时使这些设备在上游控制器看来如同单个设备。两条总线之间的通路允许下游侧设备直接将数据传输到总线上游侧，而无需智能控制器直接参与数据移动。因此，事务就像在 PCI‑PCI 桥中一样不受阻碍地在总线间转发，但所涉及的资源对主机而言是隐藏的，主机看到的只是一个单一设备。 |
| Because we now have two memory spaces, the PCI Express system needs to translate addresses of transactions that cross from one memory space to the other. This is accomplished via Translation and Limit Registers associated with the BAR. | 由于现在存在两个存储器空间，PCI Express 系统需要对从一个存储器空间跨越到另一个存储器空间的事务进行地址转换。这是通过与 BAR 相关联的转换与边界寄存器（Translation and Limit Registers）来实现的。 |

See "Address Translation" on page 958 for a detailed description; Figure C-0-2 on page 949 provides a conceptual rendering of Direct Address Translation.

Address translation can be done by Direct Address Translation (essentially replacement of the data under a mask), table lookup, or by adding an offset to an address.

Figure C-0-3 on page 950 shows Table Lookup Translation used to create multiple windows spread across system memory space for packet originated in a local I/O processor's domain, as well as Direct Address Translation used to create a single window in the opposite direction.

| EN | ZH |
|---|---|
| Address translation can be done by Direct Address Translation (essentially replacement of the data under a mask), table lookup, or by adding an offset to an address. Figure C‑0‑3 on page 950 shows Table Lookup Translation used to create multiple windows spread across system memory space for packet originated in a local I/O processor's domain, as well as Direct Address Translation used to create a single window in the opposite direction. | 地址转换可通过直接地址转换（本质上是在掩码下替换数据）、表查找或向地址添加偏移量来完成。第 950 页的图 C‑0‑3 展示了用于为本地 I/O 处理器域发起的数据包创建分布在系统存储器空间中的多个窗口的表查找转换，以及用于在相反方向创建单个窗口的直接地址转换。 |

| EN | ZH |
| --- | --- |
| ## Chapter : Appendix C: Implementing Intelligent Adapt- | ## 附录 C：实现智能适配器 |
| Figure 0-2: Direct Address Translation | 图 0-2：直接地址翻译 |

<img src="images/part06_16233cf40f4625514aa729e0d5e6ef58d10bffece04650cd6f5ca16551038551.jpg" width="700" alt="">

| EN | ZH |
| --- | --- |
| Figure 0-3: Look Up Table Translation Creates Multiple Windows | 图 0-3：查找表翻译创建多个窗口 |

<img src="images/part06_6167f9ca8ef7cd1d5ab3169da775a6c92633563dbc3ff796511be68938551498.jpg" width="700" alt="">

## 99.4.1 Example: Implementing Intelligent Adapters in a PCI Express Base System | 99.4.1 示例：在 PCI Express 基础系统中实现智能适配器
## 示例：在 PCI Express 基础系统中实现智能适配器

| EN | ZH |
|---|---|
| Intelligent adapters will be pervasive in PCI Express systems, and will likely be the most widely used example of systems with "multiple processors". | 智能适配器将在 PCI Express 系统中无处不在，很可能成为"多处理器"系统中最广泛使用的实例。 |
| Figure C-0-4 on page 951 illustrates how PCI Express systems will implement intelligent adapters. The system diagram consists of a system host, a root complex (the PCI Express version of a Northbridge), a three port switch, an example endpoint, and an intelligent add-in card. Similar to the system architecture, the add-in card contains a local host, a root complex, a three port switch, and an | 图 C-0-4（第 951 页）展示了 PCI Express 系统如何实现智能适配器。该系统框图包含一个系统主机、一个根复合体（PCI Express 版本的北桥）、一个三端口交换机、一个示例端点和一块智能插卡。与系统架构类似，该智能插卡包含一个本地主机、一个根复合体、一个三端口交换机和一个 |

## Chapter : Appendix C: Implementing Intelligent Adapters in PCI and PCI Express Systems | 附录 C：在 PCI 和 PCI Express 系统中实现智能适配器

Figure 0-4: Intelligent Adapters in PCI and PCI Express Systems | 图0-4：PCI和PCI Express系统中的智能适配器

<img src="images/part06_0e0303807b2f7dda9278e3b16af14b791f92f12d8fda9ad48de3811f454afdbb.jpg" width="700" alt="">

| EN | ZH |
|---|---|
| example endpoint. However we should note two significant differences: the intelligent add‑in card contains an EEPROM, and one port of the switch contains a back to back non‑transparent bridge. | 示例端点。但我们应注意两个重要区别：智能插件卡包含一个EEPROM，且交换机的一个端口包含一个背对背非透明桥。 |
| Upon power up, the system host will begin enumerating to determine the topology. It will pass through the Root Complex and enter the first switch (Switch A). Upon entering the topmost port, it will see a transparent bridge, so it will know to continue to enumerate. The host will then poll the leftmost port and, upon finding a Type 0 CSR header, will consider it an endpoint and explore no deeper along that branch of the PCI hierarchy. The host will then use the information in the endpoint's CSR header to configure base and limit registers in bridges and BARs in endpoints to complete the memory map for this branch of the system. | 上电后，系统主机将开始枚举以确定拓扑。它将经过根复合体进入第一个交换机（Switch A）。进入最顶层端口时，它将看到一个透明桥，因此会继续枚举。主机随后轮询最左侧端口，当发现Type 0 CSR头时，将其视为端点，不再沿该PCI层次分支继续向下探寻。然后，主机使用端点CSR头中的信息配置桥中的基址和限制寄存器以及端点中的BAR（基址寄存器），以完成该系统分支的存储器映射。 |
| The host will then explore the rightmost port of Switch A and read the CSR header registers associated with the top port of Switch B. Because this port is a non‑transparent bridge, the host finds a Type 0 CSR header. The host processor therefore believes that this is an endpoint and explores no deeper along that branch of the PCI hierarchy. The host reads the BARs of the top port of Switch B to determine the memory requirements for windows into the memory space on the other side of the bridge. The memory space requirements can be preloaded from an EEPROM into the BAR Setup Registers of Switch B's non‑transparent port or can be configured by the processor that is local to Switch B prior to allowing the system host to complete discovery. | 主机随后探测Switch A最右侧端口，并读取与Switch B顶层端口相关联的CSR头寄存器。由于该端口是一个非透明桥，主机发现的是Type 0 CSR头。因此主机处理器认为这是一个端点，不再沿该PCI层次分支继续探寻。主机读取Switch B顶层端口的BAR，以确定桥另一侧存储器空间窗口的存储器需求。存储器空间需求可从EEPROM预加载到Switch B非透明端口的BAR设置寄存器中，也可在允许系统主机完成发现之前由Switch B的本地处理器进行配置。 |
| Similar to the host processor power up sequence, the local host will also begin enumerating its own system. Like the system host processor, it will allocate memory for endpoints and continue to enumerate when it encounters a transparent bridge. When the host reaches the topmost port of Switch B, it sees a non‑transparent bridge with a Type 0 CSR header. Accordingly, it reads the BARs of the CSR header to determine the memory aperture requirements, then terminates discovery along this branch of its PCI tree. Again, the memory aperture information can be supplied by an EEPROM, or by the system host. | 与主机处理器上电序列类似，本地主机也将开始枚举其自身系统。与系统主机处理器一样，它将为端点分配存储器，并在遇到透明桥时继续枚举。当主机到达Switch B最顶层端口时，它看到一个带有Type 0 CSR头的非透明桥。因此，它读取CSR头中的BAR以确定存储器窗口需求，然后终止沿其PCI树该分支的发现。同样，存储器窗口信息可由EEPROM提供，或由系统主机提供。 |
| Communication between the two processor domains is achieved via a mailbox system and doorbell interrupts. The doorbell facility allows each processor to send interrupts to the other. The mailbox facility is a set of dual ported registers that are both readable and writable by both processors. Shared memory mapped mechanisms via the BARs may also be used for inter‑processor communication. | 两个处理器域之间的通信通过邮箱系统和门铃中断实现。门铃机制允许每个处理器向对方发送中断。邮箱机制是一组双端口寄存器，两个处理器均可读写。通过BAR的共享存储器映射机制也可用于处理器间通信。 |

## 99.4.2 Example: Implementing Host Failover in a PCI Express System | 99.4.2 示例：在 PCI Express 系统中实现主机故障切换
## 示例：在PCI Express系统中实现主机故障切换

| EN | ZH |
|---|---|
| Figure C-0-5 on page 953 illustrates how most PCI Express systems will implement host failover. The primary host processor in this illustration is on the left side of the diagram, with the backup host on the right side of the diagram. Like most systems with which we are familiar, the host processor connects to a root complex. In turn, the root complex routes its traffic to the switch. In this example, the switch has two ports to end points in addition to the upstream port for the primary host we have just described. Furthermore, this system also has another processor, which is connected to the switch via another root complex. | 图C-0-5（第953页）展示了大多数PCI Express系统如何实现主机故障切换。此图中的主宿主机位于示意图左侧，备份宿主机位于右侧。与我们熟悉的大多数系统一样，宿主机连接到一个根复合体。根复合体再将其流量路由到交换机。在此示例中，除了我们刚刚描述的主宿主机的上游端口外，交换机还有两个通向端点的端口。此外，该系统还有另一个处理器，该处理器通过另一个根复合体连接到交换机。 |

Figure 0-5: Host Failover in PCI and PCI Express Systems | 图0-5：PCI和PCI Express系统中的主机故障切换

<img src="images/part06_dcdfbe316f4856a23c1d4583b50d833827e3691ebefb4bde0b61800919d42d50.jpg" width="700" alt="">

| EN | ZH |
|---|---|
| The switch ports to both processors need to be configurable to behave either as a transparent bridge or a non-transparent bridge. An EEPROM or strap pins on the switch can be used to initially bootstrap this configuration. | 连接到两个处理器的交换机端口必须可配置为透明桥或非透明桥。可以使用交换机上的EEPROM或配置引脚来初始引导此配置。 |
| Under normal operation, upon power up, the primary host begins to enumerate the system. In our example, as the primary host processor begins its discovery protocol through the fabric, it discovers the two end points, and their memory requirements, by sizing their BARs. When it gets to the upper right port, it finds a Type 0 CSR header. This signifies to the primary host processor that it should not attempt discovery on the far side of the associated switch port. As in the previous example, the BARs associated with the non-transparent switch port may have been configured by EEPROM load prior to discovery or might be configured by software running on the local processor. | 在正常操作下，上电后，主宿主机开始枚举系统。在我们的示例中，当主宿主机处理器开始通过交换结构执行其发现协议时，它通过测量端点的基址寄存器（BAR）来发现这两个端点及其内存需求。当它到达右上端口时，发现了一个类型0 CSR头标。这向主宿主机处理器表明，它不应尝试在相关交换机端口的远端进行发现。与前面的示例一样，与非透明交换机端口相关联的基址寄存器（BAR）可以在发现之前通过EEPROM加载来配置，也可以由本地处理器上运行的软件来配置。 |
| Again, similar to the previous example, the backup processor powers up and begins to enumerate. In this example, the backup processor chipset consists of the root complex and the backup processor only. It discovers the non-transparent switch port and terminates its discovery there. It is keyed by EEPROM loaded Device ID and Vendor ID registers to load an appropriate driver. | 同样，与前面的示例类似，备份处理器上电并开始枚举。在此示例中，备份处理器芯片组仅由根复合体和备份处理器组成。它发现非透明交换机端口并在此终止其发现。它通过EEPROM加载的设备ID和供应商ID寄存器来加载相应的驱动程序。 |
| During the course of normal operation, the host processor performs all of its normal duties as it actively manages the system. In addition, it will send messages to the backup processor called heartbeat messages. Heartbeat messages are indications of the continued good health of the originating processor. A heartbeat message might be as simple as a doorbell interrupt assertion, but typically would include some data to reduce the possibility of a false positive. Checkpoint and journal messages are alternative approaches to providing the backup processor with a starting point, should it need to take over. In the journal methodology, the backup is provided with a list or journal of completed transactions (in the application specific sense, not in the sense of bus transactions). In the checkpoint methodology, the backup is periodically provided with a complete system state from which it can restart if necessary. The heartbeat's job is to provide the means by which the backup processor verifies that the host processor is still operational. Typically this data provides the latest activities and the state of all the peripherals. | 在正常操作过程中，宿主机处理器主动管理系统，执行其所有正常职责。此外，它还会向备份处理器发送称为心跳消息的消息。心跳消息是源处理器持续健康的指示。心跳消息可能就像门铃中断断言一样简单，但通常包含一些数据以减少误报的可能性。检查点（checkpoint）和日志（journal）消息是为备份处理器提供起始点的替代方法，以备其需要接管之需。在日志方法中，备份处理器会获得已完成事务（在应用特定意义上，而非总线事务意义上）的列表或日志。在检查点方法中，备份处理器会定期获得完整的系统状态，必要时可以从中重新启动。心跳的作用是提供备份处理器验证宿主机处理器仍在运行的手段。通常这些数据提供最新的活动以及所有外设的状态。 |
| If the backup processor fails to receive timely heartbeat messages, it will begin assuming control. One of its first tasks is to demote the primary port to prevent the failed processor from interacting with the rest of the system. This is accomplished by reprogramming the CSRs of the switch using a memory mapped view of the switch's CSRs provided via a BAR in the non-transparent port. To take over, the backup processor reverses the transparent/non-transparent modes at both its port and the primary processor's port and takes down the link to the primary processor. After cleaning up any transactions left in the queues or left in an incomplete state as a result of the host failure, the backup processor reconfigures the system so that it can serve as the host. Finally, it uses the data in the checkpoint or journal messages to restart the system. | 如果备份处理器未能及时收到心跳消息，它将开始接管控制。其首要任务之一是降级主端口，以防止故障处理器与系统的其余部分交互。这通过使用非透明端口中基址寄存器（BAR）提供的交换机CSR的内存映射视图来重新编程交换机的CSR来实现。为了接管，备份处理器反转其端口和主处理器端口的透明/非透明模式，并关闭到主处理器的链路。在清理队列中遗留的或因主机故障而处于未完成状态的事务之后，备份处理器重新配置系统以便其能够充当宿主机。最后，它使用检查点或日志消息中的数据来重新启动系统。 |

| EN | ZH |
|---|---|
| ## Example: Implementing Dual Host in a PCI Express Base System | ## 示例：在PCI Express基本系统中实现双主机 |
| Figure C-0-6 on page 955 illustrates how PCI Express systems might implement a dual host system<sup>1</sup>. In this example, the leftmost blocks are a typically complete system, with the rightmost blocks being a separate subsystem. As previously discussed, connecting the leftmost and rightmost diagram is a set of nontransparent bridges. | 第955页的图C‑0‑6说明了PCI Express系统如何实现双主机系统<sup>1</sup>。在此示例中，最左侧的模块是一个典型的完整系统，而最右侧的模块则是一个独立的子系统。如前所述，连接最左侧和最右侧图的部分是一组非透明桥。 |

**Figure 0-6: Dual Host in a PCI and PCI Express System**

<img src="images/part06_3e90664de5b3fa4c38071f2bcf85d67cc73ba20b85766b70b400fce321e4722b.jpg" width="700" alt="">

| EN | ZH |
|---|---|
| Upon power up, both processors will begin enumerating. As before, the hosts will search out the endpoints by reading the CSR and then allocate memory | 上电后，两个处理器将开始枚举。与之前一样，主机将通过读取CSR来搜索端点，然后分配内存。 |

## PCI Express 3.0 Technology | PCI Express 3.0 技术

| EN | ZH |
|---|---|
| appropriately. When the hosts encounter the non-transparent bridge port in each of their private switches, they will assume it is an endpoint and, using the data in the EEPROM, allocate resources. Both systems will use the doorbell and mailbox registers described above to communicate with each other. | 适当地。当主机在其各自私有交换机中遇到非透明桥接端口时，会将其假定为端点，并利用EEPROM中的数据分配资源。两个系统将使用上文所述的门铃寄存器和邮箱寄存器相互通信。 |
| <sup>2</sup>The dual-host system model may be extended to a fully redundant dual star system by using additional switches to dual-port the hosts and line cards into a redundant fabric as shown in Figure C-0-7 on page 957. This is particularly attractive to vendors who employ chassis based systems for their flexibility, scalability and reliability. | <sup>2</sup>双主机系统模型可通过使用额外的交换机将主机和线路卡双端口接入冗余结构来扩展为完全冗余的双星型系统，如图C-0-7（第957页）所示。这对于采用基于机箱的系统（因其灵活性、可扩展性和可靠性）的供应商尤其具有吸引力。 |
| Two host cards are shown. Host A is the primary host of Fabric A and the secondary host of Fabric B. Similarly, Host B is the primary host of Fabric B and the secondary host of Fabric A. | 图中显示两个主机卡。主机A是结构A的主主机和结构B的从主机。类似地，主机B是结构B的主主机和结构A的从主机。 |
| Each host is connected to the fabric it serves via a transparent bridge/switch port and to the fabric for which it provides only backup via a non-transparent bridge/switch port. These non-transparent ports are used for host-to-host communications and also support cross-domain peer-to-peer transfers where address maps do not allow a more direct connection. | 每个主机通过透明桥接器/交换机端口连接到其所服务的结构，并通过非透明桥接器/交换机端口连接到其仅提供备份的结构。这些非透明端口用于主机间通信，并在地址映射不允许更直接连接的情况下支持跨域对等传输。 |

Figure 0-7: Dual-Star Fabric | 图0-7：双星型结构

<img src="images/part06_69ca642d9ad66b908a02f832e8d4df8a1e3ead77d74ca0a56383a15939f36816.jpg" width="700" alt="">

## 99.5 Summary | 99.5 总结

<table>
<tr>
<td width="50%">
Through non-transparent bridging, PCI Express Base offers vendors the ability to integrate intelligent adapters and multi-host systems into their next generation designs. This appendix demonstrated how these features will be deployed using de-facto standard techniques adopted in the PCI environment and showed how they would be utilized for various applications. Because of this, we can expect this methodology to become the industry standard in the PCI Express paradigm.
</td>
<td width="50%" style="background-color:#e8e8e8">
通过非透明桥接，PCI Express Base为供应商提供了将智能适配器和多主机系统集成到其下一代设计中的能力。本附录演示了如何使用PCI环境中采用的事实标准技术来部署这些特性，并展示了它们将如何被用于各种应用。因此，我们可以预期这种方法将成为PCI Express范式中的行业标准。
</td>
</tr>
</table>

## 99.6 Address Translation | 99.6 地址翻译

<table>
<tr>
<td width="50%">
This section provides an in-depth description of how systems that use nontransparent bridges communicate using address translation. We provide details about the mechanism by which systems determine not only the size of the memory allocated, but also about how memory pointers are employed. Implementations using both Direct Address Translation as well as Lookup Table Based Address Translation are discussed. By using the same standardized architectural implementation of non transparent bridging popularized in the PCI paradigm into the PCI Express environment, interconnect vendors can speed market adoption of PCI Express into markets requiring intelligent adapters, host failover and multihost capabilities.
</td>
<td width="50%" style="background-color:#e8e8e8">
本节深入描述了使用非透明桥的系统如何通过地址翻译进行通信。我们详细阐述了系统不仅确定分配内存大小的机制，还介绍了内存指针的使用方式。讨论了使用直接地址翻译以及基于查找表的地址翻译的实现。通过将在PCI范式中流行的非透明桥接的相同标准化架构实现引入PCI Express环境，互联供应商可以加快PCI Express在需要智能适配器、主机故障切换和多主机能力的市场中的采用。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
The transparent bridge uses base and limit registers in I/O space, non-prefetchable memory space, and prefetchable memory space to map transactions in the downstream direction across the bridge. All downstream devices are required to be mapped in contiguous address regions such that a single aperture in each space is sufficient. Upstream mapping is done via inverse decoding relative to the same registers. A transparent bridge does not translate the addresses of forwarded transactions/packets.
</td>
<td width="50%" style="background-color:#e8e8e8">
透明桥使用I/O空间、不可预取存储器空间和可预取存储器空间中的基址和限制寄存器，以在桥的下行方向映射事务。所有下游设备必须映射在连续的地址区域中，使得每个空间中的单个窗口就足够了。上行映射通过相对于相同寄存器的反向解码完成。透明桥不会翻译转发的事务/数据包的地址。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
The non-transparent bridges use the standard set of BARs in their Type 0 CSR header to define apertures into the memory space on the other side of the bridge. There are two sets of BARs: one on the Primary side and one on the Secondary. BARs define resource apertures that allow the forwarding of transactions to the opposite (other side) interface.
</td>
<td width="50%" style="background-color:#e8e8e8">
非透明桥使用其Type 0 CSR头部中的标准BAR集来定义通往桥另一侧存储器空间的窗口。有两组BAR：一组在主侧，一组在从侧。BAR定义了允许将事务转发到对侧（另一侧）接口的资源窗口。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
For each BAR bridge there exists a set of associated control and setup registers usually writable from the other side of the bridge. Each BAR has a "setup" register, which defines the size and type of its aperture, and an address translation register. Some bars also have a limit register that can be used to restrict its aperture's size. These registers need to be programmed prior to allowing access from outside the local subsystem. This is typically done by software running on a local processor or by loading the registers from EEPROM.
</td>
<td width="50%" style="background-color:#e8e8e8">
对于每个BAR桥，存在一组相关的控制和设置寄存器，通常可从桥的另一侧写入。每个BAR有一个"设置"寄存器，用于定义其窗口的大小和类型，以及一个地址翻译寄存器。某些BAR还有一个限制寄存器，可用于限制其窗口的大小。这些寄存器需要在允许从本地子系统外部访问之前进行编程。这通常由运行在本地处理器上的软件完成，或通过从EEPROM加载寄存器来完成。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
In PCI Express, the Transaction ID fields of packets passing through these apertures are also translated to support Device ID routing. These Device IDs are used to route completions to non-posted requests and ID routed messages.
</td>
<td width="50%" style="background-color:#e8e8e8">
在PCI Express中，通过这些窗口的数据包的Transaction ID字段也会被翻译以支持Device ID路由。这些Device ID用于将完成报文路由到非发布请求和ID路由消息。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
The transparent bridge forwards CSR transactions in the downstream direction according to the secondary and subordinate bus number registers, converting Type 1 CSRs to Type 0 CSRs as required. The non-transparent bridge accepts only those CSR transactions addressed to it and returns an unsupported request response to all others.
</td>
<td width="50%" style="background-color:#e8e8e8">
透明桥根据次级总线号和从属总线号寄存器在下行方向转发CSR事务，根据需要将Type 1 CSR转换为Type 0 CSR。非透明桥仅接受那些寻址到自身的CSR事务，并对所有其他事务返回不支持请求响应。
</td>
</tr>
</table>

## 99.6.1 Direct Address Translation | 99.6.1 直接地址翻译

<table>
<tr>
<td width="50%">
The addresses of all upstream and downstream transactions are translated (except BARs accessing CSRs). With the exception of the cases in the following two sections, addresses that are forwarded from one interface to the other are translated by adding a Base Address to their offset within the BAR that they landed in as seen in Figure C-0-8 on page 959. The BAR Base Translation Registers are used to set up these base translations for the individual BARs.
</td>
<td width="50%" style="background-color:#e8e8e8">
所有上行和下行事务的地址均被翻译（访问CSR的BAR除外）。除以下两节所述情况外，从一个接口转发到另一个接口的地址，通过在其所落入的BAR内的偏移量上加上一个基地址来进行翻译，如图C-0-8（第959页）所示。BAR基地址翻译寄存器用于为各个BAR设置这些基地址翻译。
</td>
</tr>
</table>

Figure 0-8: Direct Address Translation | 图0-8：直接地址转换

<img src="images/part06_b9f658a82478d41670c0713da32fb2eee4cb996c6d3204c17970773156d57fed.jpg" width="700" alt="">

## 99.6.2 Lookup Table Based Address Translation | 99.6.2 基于查找表的地址转换

<table>
<tr>
<td width="50%">
Following the de facto standard adopted by the PCI community, PCI Express should provide several BARs for the purposes of allocating resources. All BARs contain the memory allocation; however, in accordance with PCI industry conventions, BAR 0 contains the CSR information whereas BAR1 contains I/O information, BAR 2 and BAR 3 are utilized for Lookup Table Based Translation. BAR 4 and BAR 5 are utilized for Direct Address Translations.
</td>
<td width="50%" style="background-color:#e8e8e8">
遵循PCI社区采纳的事实标准，PCI Express应提供多个BAR用于资源分配。所有BAR都包含内存分配；然而，根据PCI行业惯例，BAR 0包含CSR信息，而BAR 1包含I/O信息，BAR 2和BAR 3用于基于查找表的转换。BAR 4和BAR 5用于直接地址转换。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
On the secondary side, BAR3 uses a special lookup table based address translation for transactions that fall inside its window as seen in Figure C‐0‐9 on page 960. The lookup table provides more flexibility in secondary bus local addresses to primary bus addresses. The location of the index field with the address bus is programmable to adjust aperture size.
</td>
<td width="50%" style="background-color:#e8e8e8">
在从属侧，BAR 3对其窗口范围内的事务使用一种特殊的基于查找表的地址转换，如图C-0-9（第960页）所示。查找表为从属总线本地地址到主总线地址提供了更大的灵活性。地址总线中索引字段的位置是可编程的，以调整孔径大小。
</td>
</tr>
</table>

Figure 0‐9: Lookup Table Based Translation | 图0‐9：基于查找表的转换  
<img src="images/part06_46e325e25efdfe78f84ef0cb38c00866541e316a5f27b0f5e056285f1bce257c.jpg" width="700" alt="">

## 99.6.3 Downstream BAR Limit Registers | 99.6.3 下游BAR限制寄存器

<table>
<tr>
<td width="50%">
The two downstream BARs on the primary side (BAR2/3 and BAR4/5) also have Limit registers, programmable from the local side, to further restrict the size of the window they expose, as seen in Figure C‐0‐10 on page 961. BARs can only be assigned memory resources in "power of two" granularity. The limit registers provide a means to obtain better granularity by "capping" the size of the BAR within the "power of two" granularity. Only transactions below the Limit registers are forwarded to the secondary bus. Transactions above the limit are discarded or return 0xFFFFFFFF, or a master abort equivalent packet, on reads.
</td>
<td width="50%" style="background-color:#e8e8e8">
主侧的两个下游BAR（BAR2/3和BAR4/5）也有可从本地侧编程的限制寄存器，用于进一步限制它们所暴露窗口的大小，如图C-0-10（第961页）所示。BAR只能以"2的幂"粒度分配存储器资源。限制寄存器提供了一种通过在"2的幂"粒度内"封顶"BAR大小来获得更好粒度的方法。只有低于限制寄存器的事务才会被转发到副总线。高于限制的事务将被丢弃，或在读操作时返回0xFFFFFFFF或主中止等效报文。
</td>
</tr>
</table>

Figure 0‐10: Use of Limit Register | 图0‐10：限制寄存器的使用
<img src="images/part06_16fce13f8a5cd71d166a65ba7b9fcbcd49e7b122d14528f1c3be9b36c0ede20a.jpg" width="700" alt="">

## 99.6.4 Forwarding 64bit Address Memory Transactions | 99.6.4 转发64位地址存储器事务

<table>
<tr>
<td width="50%">
Certain BARs can be configured to work in pairs to provide the base address and translation for transactions containing 64-bit addresses. Transactions that hit within these 64-bit BARs are forwarded using Direct Address Translation. As in the case of 32 bit transactions, when a memory transaction is forwarded from the primary to the secondary bus, the primary address can be mapped to another address in the secondary bus domain. The mapping is performed by substituting a new base address for the base of the original address.
</td>
<td width="50%" style="background-color:#e8e8e8">
某些基址寄存器（BAR）可被配置为成对工作，为包含64位地址的事务提供基地址和地址转换。命中这些64位BAR范围内的事务将使用直接地址转换进行转发。与32位事务的情况类似，当存储器事务从主总线转发到从总线时，主总线地址可被映射到从总线域中的另一个地址。该映射通过用新的基地址替换原始地址的基址部分来执行。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
A 64-bit BAR pair on the system side of the bridge is used to translate a window of 64-bit addresses in packets originated on the system side of the bridge down below 232 in local space.
</td>
<td width="50%" style="background-color:#e8e8e8">
位于桥系统侧的64位BAR对用于将桥系统侧发起的数据包中的64位地址窗口转换到本地空间中2^32以下的地址范围。
</td>
</tr>
</table>

# Appendix D: Locked Transactions | 附录D：锁定事务

## 99.1 Introduction | 99.1 引言

<table>
<tr>
<td width="50%">
Native PCI Express implementations do not support the old lock protocol. Support for Locked transaction sequences only exists to support legacy device software executing on the host processor that performs a locked RMW (read-modify-write) operation on a memory location in a legacy PCI device. This chapter defines the protocol defined by PCI Express for this legacy support of locked access sequences that target legacy devices. Failure to support lock may result in deadlocks.
</td>
<td width="50%" style="background-color:#e8e8e8">
原生PCI Express实现不支持旧的锁定协议。对锁定事务序列的支持仅是为了支持在主机处理器上执行的遗留设备软件，这些软件对遗留PCI设备中的存储器位置执行锁定的RMW（读-修改-写）操作。本章定义了PCI Express为针对遗留设备的锁定访问序列提供的这种遗留支持所定义的协议。不支持锁定可能会导致死锁。
</td>
</tr>
</table>

## 99.2 Background | 99.2 背景

<table>
<tr>
<td width="50%">
PCI Express supports atomic or uninterrupted transaction sequences (usually described as an atomic read-modify-write sequence) for legacy devices only. Native PCIe devices don't support this at all and will return a Completion with UR (Unsupported Request) status if they receive a locked Request.
</td>
<td width="50%" style="background-color:#e8e8e8">
PCI Express仅对遗留设备支持原子或不可中断的事务序列（通常描述为原子读-修改-写序列）。原生PCIe设备完全不支持此功能，如果收到锁定请求，将返回带有UR（不支持请求）状态的完成报文。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Locked operations consist of the basic RMW sequence, that is:
</td>
<td width="50%" style="background-color:#e8e8e8">
锁定操作由基本的RMW序列组成，即：
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
1. One or more memory reads from the target location to obtain the value.
</td>
<td width="50%" style="background-color:#e8e8e8">
1. 从目标位置进行一次或多次存储器读取以获取数值。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
2. The modification of the data in a processor register.
</td>
<td width="50%" style="background-color:#e8e8e8">
2. 在处理器寄存器中修改数据。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
3. One or more writes to write the modified value back to the target memory location.
</td>
<td width="50%" style="background-color:#e8e8e8">
3. 进行一次或多次写入，将修改后的值写回目标存储器位置。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
This transaction sequence must be performed such that no other accesses are permitted to the target locations (or device) during the locked sequence. This requires blocking other transactions during the operation. This can potentially result in deadlocks and poor performance.
</td>
<td width="50%" style="background-color:#e8e8e8">
此事务序列的执行必须确保在锁定序列期间不允许对目标位置（或设备）进行任何其他访问。这需要在操作期间阻止其他事务。这可能导致死锁和性能下降。
</td>
</tr>
</table>

## PCI Express Technology | PCI Express技术

<table>
<tr>
<td width="50%">
The devices required to support locked sequences are:
</td>
<td width="50%" style="background-color:#e8e8e8">
需要支持锁定序列的设备包括：
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• The Root Complex.
</td>
<td width="50%" style="background-color:#e8e8e8">
• 根复合体。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• Any Switches in the path to a Legacy Device that may be the target of a locked transaction series.
</td>
<td width="50%" style="background-color:#e8e8e8">
• 通往可能成为锁定事务系列目标的遗留设备路径上的任何交换机。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• PCIe-to-PCI Bridge or PCIe-to-PCI-X Bridge.
</td>
<td width="50%" style="background-color:#e8e8e8">
• PCIe到PCI桥或PCIe到PCI-X桥。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• Any Legacy Device whose driver issues locked transactions to memory residing within the legacy device.
</td>
<td width="50%" style="background-color:#e8e8e8">
• 任何其驱动程序向驻留在遗留设备内的存储器发出锁定事务的遗留设备。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Locking in the PCI environment is achieved by the use of the LOCK# signal. The equivalent functionality in PCIe is accomplished by using a specific Request that emulates the LOCK# signal functionality.
</td>
<td width="50%" style="background-color:#e8e8e8">
在PCI环境中，锁定是通过使用LOCK#信号实现的。在PCIe中，等效功能是通过使用模拟LOCK#信号功能的特定请求来实现的。
</td>
</tr>
</table>

## 99.3 The PCI Express Lock Protocol | 99.3 PCI Express锁定协议

<table>
<tr>
<td width="50%">
The only source of lock supported by PCI Express is the system processor acting through the Root Complex. A locked operation is performed between a Root Port and the Legacy Endpoint. In most systems, the legacy device is typically a PCI Express-to-PCI or PCI Express-to-PCI-X bridge. Only one locked sequence at a time is supported for a given hierarchical path.
</td>
<td width="50%" style="background-color:#e8e8e8">
PCI Express支持的唯一锁定源是通过根复合体进行操作的系统处理器。锁定操作在根端口和遗留端点之间执行。在大多数系统中，遗留设备通常是PCI Express到PCI或PCI Express到PCI-X桥。对于给定的层次路径，一次仅支持一个锁定序列。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Locked transactions are constrained to use only Traffic Class 0 and Virtual Channel 0. Transactions with other TC values that map to a VC other than zero are permitted to traverse the fabric without regard to the locked operation, but transactions that map to VC0 are affected by the lock rules described here.
</td>
<td width="50%" style="background-color:#e8e8e8">
锁定事务被限制为仅使用流量类0和虚通道0。映射到非零VC的其他TC值的事务允许穿越结构而无需考虑锁定操作，但映射到VC0的事务受此处描述的锁定规则影响。
</td>
</tr>
</table>

## Lock Messages — The Virtual Lock Signal | 锁定消息——虚拟锁定信号

<table>
<tr>
<td width="50%">
PCI Express defines the following transactions that, together, act as a virtual wire and replace the LOCK# signal.
</td>
<td width="50%" style="background-color:#e8e8e8">
PCI Express定义了以下事务，它们共同起到虚拟导线的作用并取代LOCK#信号。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Memory Read Lock Request (MRdLk) — Originates a locked sequence. The first MRdLk transaction blocks other Requests in VC0 from reaching the target device. One or more of these locked read requests may be issued during the sequence.
</td>
<td width="50%" style="background-color:#e8e8e8">
存储器读锁定请求（MRdLk）——发起锁定序列。第一个MRdLk事务阻止VC0中的其他请求到达目标设备。在序列期间可以发出一个或多个此类锁定读请求。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Memory Read Lock Completion with Data (CplDLk) — Returns data and confirms that the path to the target is locked. A successful read Completion that returns data for the first Memory Read Lock request results in the path between the Root Complex and the target device being locked. That is, transactions traversing the same path from other ports are blocked from reaching either the root port or the target port. Transactions being routed in buffers for VC1-VC7 are unaffected by the lock.
</td>
<td width="50%" style="background-color:#e8e8e8">
带数据的存储器读锁定完成报文（CplDLk）——返回数据并确认到目标的路径已锁定。为第一个存储器读锁定请求返回数据的成功读完成报文会导致根复合体与目标设备之间的路径被锁定。也就是说，从其他端口穿越同一条路径的事务被阻止到达根端口或目标端口。在VC1-VC7缓冲区中路由的事务不受锁定的影响。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Memory Read Lock Completion without Data (CplLK) — A Completion without a data payload indicates that the lock sequence cannot complete currently and the path remains unlocked.
</td>
<td width="50%" style="background-color:#e8e8e8">
不带数据的存储器读锁定完成报文（CplLK）——不带数据负载的完成报文表示锁定序列当前无法完成，且路径保持未锁定状态。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Unlock Message — An unlock message is issued by the Root Complex from the locked root port. This message unlocks the path between the root port and the target port.
</td>
<td width="50%" style="background-color:#e8e8e8">
解锁消息——由根复合体从锁定的根端口发出解锁消息。该消息解锁根端口与目标端口之间的路径。
</td>
</tr>
</table>

## The Lock Protocol Sequence — an Example | 锁定协议序列——示例

<table>
<tr>
<td width="50%">
This section explains the PCI Express lock protocol by example. The example includes the following devices:
</td>
<td width="50%" style="background-color:#e8e8e8">
本节通过示例解释PCI Express锁定协议。该示例包括以下设备：
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• The Root Complex that initiates the Locked transaction series on behalf of the host processor.
</td>
<td width="50%" style="background-color:#e8e8e8">
• 代表主机处理器发起锁定事务系列的根复合体。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• A Switch in the path between the root port and targeted legacy endpoint.
</td>
<td width="50%" style="background-color:#e8e8e8">
• 位于根端口与目标遗留端点之间路径上的交换机。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• A PCI Express-to-PCI Bridge in the path to the target.
</td>
<td width="50%" style="background-color:#e8e8e8">
• 通往目标路径上的PCI Express到PCI桥。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• The target PCI device whose Device Driver initiated the locked RMW.
</td>
<td width="50%" style="background-color:#e8e8e8">
• 其设备驱动程序发起锁定RMW的目标PCI设备。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• A PCI Express endpoint is included to describe Switch behavior during lock.
</td>
<td width="50%" style="background-color:#e8e8e8">
• 包含一个PCI Express端点以描述锁定期间的交换机行为。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
In this example, the locked operation completes normally. The steps that occur during the operation are described in the two sections that follow.
</td>
<td width="50%" style="background-color:#e8e8e8">
在此示例中，锁定操作正常完成。操作期间发生的步骤在接下来的两节中描述。
</td>
</tr>
</table>

## The Memory Read Lock Operation | 存储器读锁定操作

<table>
<tr>
<td width="50%">
Figure E-1 on page 967 illustrates the first step in the Locked transaction series (i.e., the initial memory read to obtain the semaphore):
</td>
<td width="50%" style="background-color:#e8e8e8">
第967页的图E-1说明了锁定事务系列的第一步（即获取信号量的初始存储器读取）：
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
1. The CPU initiates the locked sequence (a Locked Memory Read) as a result of a driver executing a locked RMW instruction that targets a PCI target.
</td>
<td width="50%" style="background-color:#e8e8e8">
1. CPU因驱动程序执行针对PCI目标的锁定RMW指令而发起锁定序列（锁定存储器读取）。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
2. The Root Port issues a Memory Read Lock Request from port 2. The Root Complex is always the source of a locked sequence.
</td>
<td width="50%" style="background-color:#e8e8e8">
2. 根端口从端口2发出存储器读锁定请求。根复合体始终是锁定序列的源。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
3. The Switch receives the lock request on its upstream port and forwards the request to the target egress port (3). The switch, upon forwarding the request to the egress port, must block all requests from ports other than the ingress port (1) from being sent from the egress port.
</td>
<td width="50%" style="background-color:#e8e8e8">
3. 交换机在其上行端口上接收到锁定请求，并将该请求转发到目标出口端口（3）。交换机在将请求转发到出口端口时，必须阻止来自除入口端口（1）之外的其他端口的所有请求从该出口端口发出。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
4. A subsequent peer-to-peer transfer from the illustrated PCI Express endpoint to the PCI bus (switch port 2 to switch port 3) would be blocked until the lock is cleared. Note that the lock is not yet established in the other direction. Transactions from the PCI Express endpoint could be sent to the Root Complex.
</td>
<td width="50%" style="background-color:#e8e8e8">
4. 随后从图示的PCI Express端点到PCI总线（交换机端口2到交换机端口3）的对等传输将被阻止，直到锁定解除。请注意，另一个方向尚未建立锁定。来自PCI Express端点的事务可以发送到根复合体。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
5. The Memory Read Lock Request is sent from the Switch's egress port to the PCI Express-to-PCI Bridge. This bridge will implement PCI lock semantics (See the MindShare book entitled PCI System Architecture, Fourth Edition, for details regarding PCI lock).
</td>
<td width="50%" style="background-color:#e8e8e8">
5. 存储器读锁定请求从交换机的出口端口发送到PCI Express到PCI桥。该桥将实现PCI锁定语义（有关PCI锁定的详细信息，请参阅MindShare出版的《PCI系统体系结构，第四版》）。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
6. The bridge performs the Memory Read transaction on the PCI bus with the PCI LOCK# signal asserted. The target memory device returns the requested semaphore data to the bridge.
</td>
<td width="50%" style="background-color:#e8e8e8">
6. 桥在PCI总线上执行存储器读事务，并断言PCI LOCK#信号。目标存储器设备将请求的信号量数据返回给桥。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
7. Read data is returned to the Bridge and is delivered back to the Switch via a Memory Read Lock Completion with Data (CplDLk).
</td>
<td width="50%" style="background-color:#e8e8e8">
7. 读数据返回到桥，并通过带数据的存储器读锁定完成报文（CplDLk）传递回交换机。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
8. The switch uses ID routing to return the packet upstream towards the host processor. When the CplDLk packet is forwarded to the upstream port of the Switch, it establishes a lock in the upstream direction to prevent traffic from other ports from being routed upstream. The PCI Express endpoint is completely blocked from sending any transaction to the Switch ports via the path of the locked operation. Note that transfers between Switch ports not involved in the locked operation would be permitted (not shown in this example).
</td>
<td width="50%" style="background-color:#e8e8e8">
8. 交换机使用ID路由将数据包向上游返回给主机处理器。当CplDLk数据包被转发到交换机的上行端口时，它在上行方向建立了锁定，以防止来自其他端口的流量被路由到上游。PCI Express端点被完全阻止通过锁定操作的路径向交换机端口发送任何事务。请注意，不参与锁定操作的交换机端口之间的传输是允许的（本例中未示出）。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
9. Upon detecting the CplDLk packet, the Root Complex knows that the lock has been established along the path between it and the target device, and the completion data is sent to the CPU.
</td>
<td width="50%" style="background-color:#e8e8e8">
9. 在检测到CplDLk数据包时，根复合体就知道锁定已在其与目标设备之间的路径上建立，并且完成数据被发送到CPU。
</td>
</tr>
</table>

Figure D-1: Lock Sequence Begins with Memory Read Lock Request | 图D-1：锁定序列以存储器读锁定请求开始
<img src="images/part06_f6913aa97476401663ef2a81abb4e6b5da7417c5e2f611200ca27786fdc6951b.jpg" width="700" alt="">

## Read Data Modified and Written to Target and Lock Completes | 读数据被修改并写入目标，锁定完成

<table>
<tr>
<td width="50%">
The device driver receives the semaphore value, alters it, and then initiates a memory write to update the semaphore within the memory of the legacy PCI device. Figure E-2 on page 969 illustrates the write sequence followed by the Root Complex's transmission of the Unlock message that releases the lock:
</td>
<td width="50%" style="background-color:#e8e8e8">
设备驱动程序接收信号量值，修改它，然后发起存储器写入以更新遗留PCI设备存储器中的信号量。第969页的图E-2说明了写入序列，随后根复合体发送解锁消息以释放锁定：
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
10. The Root Complex issues the Memory Write Request across the locked path to the target device.
</td>
<td width="50%" style="background-color:#e8e8e8">
10. 根复合体通过锁定的路径向目标设备发出存储器写请求。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
11. The Switch forwards the transaction to the target egress port (3). The memory address of the Memory Write must be the same as the initial Memory Read request.
</td>
<td width="50%" style="background-color:#e8e8e8">
11. 交换机将事务转发到目标出口端口（3）。存储器写的存储器地址必须与初始存储器读请求的地址相同。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
12. The bridge forwards the transaction to the PCI bus.
</td>
<td width="50%" style="background-color:#e8e8e8">
12. 桥将事务转发到PCI总线。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
13. The target device receives the memory write data.
</td>
<td width="50%" style="background-color:#e8e8e8">
13. 目标设备接收存储器写数据。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
14. Once the Memory Write transaction is sent from the Root Complex, it sends an Unlock message to instruct the Switches and any PCI/PCI-X bridges in the locked path to release the lock. Note that the Root Complex presumes the operation has completed normally (because memory writes are posted and no Completion is returned to verify success).
</td>
<td width="50%" style="background-color:#e8e8e8">
14. 一旦存储器写事务从根复合体发出，它就发送一条解锁消息，指示锁定路径中的交换机和任何PCI/PCI-X桥释放锁定。请注意，根复合体假定操作已正常完成（因为存储器写是发布性的，不返回完成报文来验证成功）。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
15. The Switch receives the Unlock message, unlocks its ports and forwards the message to the egress port that was locked to notify any other Switches and/or bridges in the locked path that the lock must be cleared.
</td>
<td width="50%" style="background-color:#e8e8e8">
15. 交换机接收解锁消息，解锁其端口，并将该消息转发到被锁定的出口端口，以通知锁定路径中的任何其他交换机和/或桥必须解除锁定。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
16. Upon detecting the Unlock message, the bridge must also release the lock on the PCI bus.
</td>
<td width="50%" style="background-color:#e8e8e8">
16. 在检测到解锁消息时，桥还必须释放PCI总线上的锁定。
</td>
</tr>
</table>

Figure D-2: Lock Completes with Memory Write Followed by Unlock Message | 图D-2：锁定以存储器写后跟解锁消息完成
<img src="images/part06_5b9488b3a211370278d851a4da3e757bbb0a8776bfad32d700487c491a9d52cb.jpg" width="700" alt="">

## 99.3.3 Notification of an Unsuccessful Lock | 99.3.3 不成功锁定的通知

<table>
<tr>
<td width="50%">
A locked transaction series is aborted when the initial Memory Read Lock Request receives a Completion packet with no data (CplLk). This means that the locked sequence must terminate because no data was returned. This could result from an error associated with the memory read transaction, or perhaps the target device is busy and cannot respond at this time.
</td>
<td width="50%" style="background-color:#e8e8e8">
当初始存储器读锁定请求收到不带数据的完成报文（CplLk）时，锁定事务系列被中止。这意味着锁定序列必须终止，因为没有返回数据。这可能是由于与存储器读事务相关的错误，或者目标设备正忙而无法响应所致。
</td>
</tr>
</table>

## 99.4 Summary of Locking Rules | 99.4 锁定规则总结

<table>
<tr>
<td width="50%">
Following is a list of ordering rules that apply to the Root Complex, Switches, and Bridges.
</td>
<td width="50%" style="background-color:#e8e8e8">
以下是适用于根复合体、交换机和桥的有序规则列表。
</td>
</tr>
</table>

## 99.4.1 Rules Related To the Initiation and Propagation of Locked Transactions | 99.4.1 与锁定事务发起和传播相关的规则

<table>
<tr>
<td width="50%">
Locked Requests which are completed with a status other than Successful Completion do not establish lock.
</td>
<td width="50%" style="background-color:#e8e8e8">
以成功完成之外的状态完成的锁定请求不会建立锁定。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Regardless of the status of any of the Completions associated with a locked sequence, all locked sequences and attempted locked sequences must be terminated by the transmission of an Unlock Message.
</td>
<td width="50%" style="background-color:#e8e8e8">
无论与锁定序列关联的任何完成报文的状态如何，所有锁定序列和尝试的锁定序列都必须通过发送解锁消息来终止。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
MRdLk, CplDLk and Unlock semantics are allowed only for the default Traffic Class (TC0).
</td>
<td width="50%" style="background-color:#e8e8e8">
MRdLk、CplDLk和解锁语义仅允许用于默认流量类（TC0）。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• Only one locked transaction sequence attempt may be in progress at a given time within a single hierarchy domain.
</td>
<td width="50%" style="background-color:#e8e8e8">
• 在单个层次域中，同一时间只能有一个锁定事务序列尝试在进行中。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Any device which is not involved in the locked sequence must ignore the Unlock Message.
</td>
<td width="50%" style="background-color:#e8e8e8">
任何未参与锁定序列的设备必须忽略解锁消息。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
The initiation and propagation of a locked transaction sequence through the PCI Express fabric is performed as follows:
</td>
<td width="50%" style="background-color:#e8e8e8">
锁定事务序列通过PCI Express结构的发起和传播按如下方式执行：
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• A locked transaction sequence is started with a MRdLk Request:
</td>
<td width="50%" style="background-color:#e8e8e8">
• 锁定事务序列以MRdLk请求开始：
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
— Any successive reads associated with the locked transaction sequence must also use MRdLk Requests.
</td>
<td width="50%" style="background-color:#e8e8e8">
— 与锁定事务序列关联的任何后续读取也必须使用MRdLk请求。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
The Completions for any successful MRdLk Request use the CplDLk Completion type, or the CPlLk Completion type for unsuccessful Requests.
</td>
<td width="50%" style="background-color:#e8e8e8">
任何成功的MRdLk请求使用CplDLk完成报文类型，不成功的请求使用CplLk完成报文类型。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
If any read associated with a locked sequence is completed unsuccessfully, the Requester must assume that the atomicity of the lock is no longer assured, and that the path between the Requester and Completer is no longer locked.
</td>
<td width="50%" style="background-color:#e8e8e8">
如果与锁定序列关联的任何读取未成功完成，请求者必须假定锁定的原子性不再得到保证，并且请求者与完成者之间的路径不再锁定。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• All writes associated with a locked sequence must use MWr Requests.
</td>
<td width="50%" style="background-color:#e8e8e8">
• 与锁定序列关联的所有写入必须使用MWr请求。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
The Unlock Message is used to indicate the end of a locked sequence. A Switch propagates Unlock Messages through the locked Egress Port.
</td>
<td width="50%" style="background-color:#e8e8e8">
解锁消息用于指示锁定序列的结束。交换机通过锁定的出口端口传播解锁消息。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Upon receiving an Unlock Message, a legacy Endpoint or Bridge must unlock itself if it is in a locked state. If it is not locked, or if the Receiver is a PCI Express Endpoint or Bridge which does not support lock, the Unlock Message is ignored and discarded.
</td>
<td width="50%" style="background-color:#e8e8e8">
在收到解锁消息时，如果遗留端点或桥处于锁定状态，它必须解锁自身。如果它未锁定，或者接收者是PCI Express端点或不支持锁定的桥，则解锁消息被忽略并丢弃。
</td>
</tr>
</table>

## 99.4.2 Rules Related to Switches | 99.4.2 与交换机相关的规则

<table>
<tr>
<td width="50%">
Switches must detect transactions associated with locked sequences from other transactions to prevent other transactions from interfering with the lock and potentially causing deadlock. The following rules cover how this is done. Note that locked accesses are limited to TC0, which is always mapped to VC0.
</td>
<td width="50%" style="background-color:#e8e8e8">
交换机必须从其他事务中检测与锁定序列关联的事务，以防止其他事务干扰锁定并可能导致死锁。以下规则涵盖了如何做到这一点。请注意，锁定访问仅限于TC0，它始终映射到VC0。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
When a Switch propagates a MRdLk Request from an Ingress Port to the Egress Port, it must block all Requests which map to the default Virtual Channel (VC0) from being propagated to the Egress Port. If a subsequent MRdLk Request is received at this Ingress Port addressing a different Egress Port, the behavior of the Switch is undefined. Note that this sort of split-lock access is not supported by PCI Express and software must not cause such a locked access. System deadlock may result from such accesses.
</td>
<td width="50%" style="background-color:#e8e8e8">
当交换机将MRdLk请求从入口端口传播到出口端口时，它必须阻止所有映射到默认虚通道（VC0）的请求被传播到出口端口。如果在此入口端口接收到寻址不同出口端口的后续MRdLk请求，则交换机的行为是未定义的。请注意，PCI Express不支持这种分裂锁定访问，软件不得引起这样的锁定访问。此类访问可能导致系统死锁。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
When the CplDLk for the first MRdLk Request is returned, if the Completion indicates a Successful Completion status, the Switch must block all Requests from all other Ports from being propagated to either of the Ports involved in the locked access, except for Requests which map to channels other than VC0 on the Egress Port.
</td>
<td width="50%" style="background-color:#e8e8e8">
当第一个MRdLk请求的CplDLk返回时，如果完成报文指示成功完成状态，交换机必须阻止来自所有其他端口的所有请求传播到参与锁定访问的任一端口，但映射到出口端口上非VC0通道的请求除外。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
The two Ports involved in the locked sequence must remain blocked until the Switch receives the Unlock Message (at the Ingress Port which received the initial MRdLk Request)
</td>
<td width="50%" style="background-color:#e8e8e8">
参与锁定序列的两个端口必须保持阻塞状态，直到交换机（在接收初始MRdLk请求的入口端口处）收到解锁消息。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
— The Unlock Message must be forwarded to the locked Egress Port.
</td>
<td width="50%" style="background-color:#e8e8e8">
— 解锁消息必须转发到锁定的出口端口。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
— The Unlock Message may be broadcast to all other Ports.
</td>
<td width="50%" style="background-color:#e8e8e8">
— 解锁消息可以广播到所有其他端口。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
The Ingress Port is unblocked once the Unlock Message arrives, and the Egress Port(s) which were blocked are unblocked following the transmission of the Unlock Message out of the Egress Port(s). Ports that were not involved in the locked access are unaffected by the Unlock Message.
</td>
<td width="50%" style="background-color:#e8e8e8">
一旦解锁消息到达，入口端口被解除阻塞，而被阻塞的出口端口在将解锁消息从出口端口发出后解除阻塞。未参与锁定访问的端口不受解锁消息的影响。
</td>
</tr>
</table>

## 99.4.3 Rules Related To PCI Express/PCI Bridges | 99.4.3 与PCI Express/PCI桥相关的规则

<table>
<tr>
<td width="50%">
The requirements for PCI Express/PCI Bridges are similar to those for Switches, except that, because these Bridges only use TC0 and VC0, all other traffic is blocked during the locked access. Requirements on the PCI bus side are described in the MindShare book, PCI System Architecture, Fourth Edition.
</td>
<td width="50%" style="background-color:#e8e8e8">
对PCI Express/PCI桥的要求与对交换机的要求类似，只是由于这些桥仅使用TC0和VC0，因此在锁定访问期间所有其他流量都被阻塞。有关PCI总线侧的要求在MindShare出版的《PCI系统体系结构，第四版》中描述。
</td>
</tr>
</table>

## 99.4.4 Rules Related To the Root Complex | 99.4.4 与根复合体相关的规则

<table>
<tr>
<td width="50%">
A Root Complex is permitted to support locked transactions as a Requester. If locked transactions are supported, a Root Complex must follow the rules already described to perform a locked access. The mechanism(s) used by the Root Complex to interface to the host processor's FSB (Front-Side Bus) are outside the scope of the spec.
</td>
<td width="50%" style="background-color:#e8e8e8">
根复合体允许作为请求者支持锁定事务。如果支持锁定事务，根复合体必须遵循已描述的规则来执行锁定访问。根复合体用于与主机处理器FSB（前端总线）接口的机制不在本规范的范围内。
</td>
</tr>
</table>

## 99.4.5 Rules Related To Legacy Endpoints | 99.4.5 与遗留端点相关的规则

<table>
<tr>
<td width="50%">
Legacy Endpoints are permitted to support locked accesses, although their use is discouraged. If locked accesses are supported, legacy Endpoints must handle them as follows:
</td>
<td width="50%" style="background-color:#e8e8e8">
允许遗留端点支持锁定访问，但不鼓励使用。如果支持锁定访问，遗留端点必须按如下方式处理：
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
The legacy Endpoint becomes locked when it transmits the first Completion for the first read request of the locked transaction series access with a Successful Completion status:
</td>
<td width="50%" style="background-color:#e8e8e8">
当遗留端点为锁定事务系列访问的第一个读请求发送第一个状态为成功完成的完成报文时，该遗留端点变为锁定状态：
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
— If the completion status is not Successful Completion, the legacy Endpoint does not become locked.
</td>
<td width="50%" style="background-color:#e8e8e8">
— 如果完成状态不是成功完成，则遗留端点不会变为锁定状态。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
— Once locked, the legacy Endpoint must remain locked until it receives the Unlock Message.
</td>
<td width="50%" style="background-color:#e8e8e8">
— 一旦锁定，遗留端点必须保持锁定状态，直到收到解锁消息。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
While locked, a legacy Endpoint must not issue any Requests using Traffic Classes which map to the default Virtual Channel (VC0). Note that this requirement applies to all possible sources of Requests within the Endpoint, in the case where there is more than one possible source of Requests. Requests may be issued using TCs which map to VCs other than VC0.
</td>
<td width="50%" style="background-color:#e8e8e8">
在锁定状态下，遗留端点不得使用映射到默认虚通道（VC0）的流量类发出任何请求。请注意，此要求适用于端点内所有可能的请求源（如果有多个可能的请求源的情况）。可以使用映射到VC0以外的VC的TC来发出请求。
</td>
</tr>
</table>

## 99.4.6 Rules Related To PCI Express Endpoints | 99.4.6 与PCI Express端点相关的规则

<table>
<tr>
<td width="50%">
Native PCI Express Endpoints do not support lock. A PCI Express Endpoint must treat a MRdLk Request as an Unsupported Request.
</td>
<td width="50%" style="background-color:#e8e8e8">
原生PCI Express端点不支持锁定。PCI Express端点必须将MRdLk请求视为不支持请求。
</td>
</tr>
</table>

## Locked Transactions | 锁定事务

## 99.1 Introduction | 99.1 引言

<table>
<tr>
<td width="50%">
Native PCI Express implementations do not support the old lock protocol. Support for Locked transaction sequences only exists to support legacy device software executing on the host processor that performs a locked RMW (read-modify-write) operation on a memory location in a legacy PCI device. This chapter defines the protocol defined by PCI Express for this legacy support of locked access sequences that target legacy devices. Failure to support lock may result in deadlocks.
</td>
<td width="50%" style="background-color:#e8e8e8">
原生 PCI Express 实现不支持旧的锁定协议。支持锁定事务序列仅为了支持在主机处理器上执行的遗留设备软件，该软件在遗留 PCI 设备的内存位置上执行锁定的 RMW（读-修改-写）操作。本章定义了 PCI Express 为此遗留支持所定义的协议，用于针对遗留设备的锁定访问序列。不支持锁定可能会导致死锁。
</td>
</tr>
</table>

## 99.2 Background | 99.2 背景

<table>
<tr>
<td width="50%">
PCI Express supports atomic or uninterrupted transaction sequences (usually described as an atomic read‐modify‐write sequence) for legacy devices only. Native PCIe devices don't support this at all and will return a Completion with UR (Unsupported Request) status if they receive a locked Request.
</td>
<td width="50%" style="background-color:#e8e8e8">
PCI Express仅在传统设备中支持原子性或不可中断的事务序列（通常描述为原子读-修改-写序列）。原生PCIe设备完全不支持此功能，如果收到锁定请求，将返回带有UR（不支持请求）状态的完成报文。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Locked operations consist of the basic RMW sequence, that is:
</td>
<td width="50%" style="background-color:#e8e8e8">
锁定操作由基本的RMW序列组成，即：
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
1. One or more memory reads from the target location to obtain the value.
</td>
<td width="50%" style="background-color:#e8e8e8">
1. 从目标位置进行一次或多次存储器读取以获取该值。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
2. The modification of the data in a processor register.
</td>
<td width="50%" style="background-color:#e8e8e8">
2. 在处理器寄存器中修改数据。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
3. One or more writes to write the modified value back to the target memory location.
</td>
<td width="50%" style="background-color:#e8e8e8">
3. 进行一次或多次写入以将修改后的值写回目标存储器位置。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
This transaction sequence must be performed such that no other accesses are permitted to the target locations (or device) during the locked sequence. This requires blocking other transactions during the operation. This can potentially result in deadlocks and poor performance.
</td>
<td width="50%" style="background-color:#e8e8e8">
该事务序列的执行必须确保在锁定序列期间，不允许对目标位置（或设备）进行任何其他访问。这需要在操作期间阻止其他事务。这可能导致死锁和性能下降。
</td>
</tr>
</table>

## PCI Express Technology | PCI Express 技术

<table>
<tr>
<td width="50%">
The devices required to support locked sequences are:

• The Root Complex.

• Any Switches in the path to a Legacy Device that may be the target of a locked transaction series.

• PCIe‐to‐PCI Bridge or PCIe‐to‐PCI‐X Bridge.

• Any Legacy Device whose driver issues locked transactions to memory residing within the legacy device.
</td>
<td width="50%" style="background-color:#e8e8e8">
需要支持锁定序列的设备包括：

• 根复合体。

• 路径中可能成为锁定事务系列目标的传统设备所经的任何交换机。

• PCIe到PCI桥或PCIe到PCI-X桥。

• 其驱动程序对驻留在传统设备内的存储器发出锁定事务的任何传统设备。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Locking in the PCI environment is achieved by the use of the LOCK# signal. The equivalent functionality in PCIe is accomplished by using a specific Request that emulates the LOCK# signal functionality.
</td>
<td width="50%" style="background-color:#e8e8e8">
在PCI环境中，锁定是通过使用LOCK#信号实现的。PCIe中的等效功能是通过使用模拟LOCK#信号功能的特定请求来完成的。
</td>
</tr>
</table>

## 99.3 The PCI Express Lock Protocol | 99.3 PCIe 锁定协议

<table>
<tr>
<td width="50%">
The only source of lock supported by PCI Express is the system processor acting through the Root Complex. A locked operation is performed between a Root Port and the Legacy Endpoint. In most systems, the legacy device is typically a PCI Express-to-PCI or PCI Express-to-PCI-X bridge. Only one locked sequence at a time is supported for a given hierarchical path.
</td>
<td width="50%" style="background-color:#e8e8e8">
PCI Express 支持的锁定唯一来源是通过根复合体（Root Complex）作用的系统处理器。锁定操作在根端口（Root Port）与传统端点（Legacy Endpoint）之间执行。在大多数系统中，传统设备通常是 PCI Express-to-PCI 或 PCI Express-to-PCI-X 桥接器。对于给定的层次路径，一次仅支持一个锁定序列。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Locked transactions are constrained to use only Traffic Class 0 and Virtual Channel 0. Transactions with other TC values that map to a VC other than zero are permitted to traverse the fabric without regard to the locked operation, but transactions that map to VC0 are affected by the lock rules described here.
</td>
<td width="50%" style="background-color:#e8e8e8">
锁定事务（Locked transactions）被限制为仅使用流量类 0（Traffic Class 0）和虚通道 0（Virtual Channel 0）。映射到非零 VC 的其他 TC 值的事务允许在结构（fabric）中传输，而不受锁定操作的影响，但映射到 VC0 的事务则受此处描述的锁定规则影响。
</td>
</tr>
</table>

## Lock Messages — The Virtual Lock Signal | 锁消息 — 虚拟锁定信号

<table>
<tr>
<td width="50%">
PCI Express defines the following transactions that, together, act as a virtual wire and replace the LOCK# signal.
</td>
<td width="50%" style="background-color:#e8e8e8">
PCI Express 定义了以下事务，它们共同充当虚拟连线并取代 LOCK# 信号。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Memory Read Lock Request (MRdLk) — Originates a locked sequence. The first MRdLk transaction blocks other Requests in VC0 from reaching the target device. One or more of these locked read requests may be issued during the sequence.
</td>
<td width="50%" style="background-color:#e8e8e8">
存储器读锁定请求（MRdLk）— 发起一个锁定序列。第一个 MRdLk 事务阻止 VC0 中的其他请求到达目标设备。在该序列期间，可以发出一个或多个此类锁定读请求。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Memory Read Lock Completion with Data (CplDLk) — Returns data and confirms that the path to the target is locked. A successful read Completion that returns data for the first Memory Read Lock request results in the path between the Root Complex and the target device being locked. That is, transactions traversing the same path from other ports are blocked from reaching either the root port or the target port. Transactions being routed in buffers for VC1-VC7 are unaffected by the lock.
</td>
<td width="50%" style="background-color:#e8e8e8">
带数据的存储器读锁定完成（CplDLk）— 返回数据并确认通往目标的路径已被锁定。成功返回数据的读完成（针对第一个存储器读锁定请求）将导致根复合体与目标设备之间的路径被锁定。也就是说，来自其他端口且经过同一路径的事务被阻止到达根端口或目标端口。在 VC1-VC7 缓冲区中路由的事务不受锁定的影响。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Memory Read Lock Completion without Data (CplLK) — A Completion without a data payload indicates that the lock sequence cannot complete currently and the path remains unlocked.
</td>
<td width="50%" style="background-color:#e8e8e8">
不带数据的存储器读锁定完成（CplLK）— 不带数据载荷的完成表示锁定序列当前无法完成，路径保持解锁状态。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Unlock Message — An unlock message is issued by the Root Complex from the locked root port. This message unlocks the path between the root port and the target port.
</td>
<td width="50%" style="background-color:#e8e8e8">
解锁消息 — 由根复合体从锁定的根端口发出解锁消息。该消息解锁根端口与目标端口之间的路径。
</td>
</tr>
</table>

## The Lock Protocol Sequence — an Example | 锁协议序列示例

<table>
<tr>
<td width="50%">
This section explains the PCI Express lock protocol by example. The example includes the following devices:
</td>
<td width="50%" style="background-color:#e8e8e8">
本节通过示例解释PCI Express锁协议。该示例包括以下设备：
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• The Root Complex that initiates the Locked transaction series on behalf of the host processor.
</td>
<td width="50%" style="background-color:#e8e8e8">
• 代表主机处理器发起锁定事务序列的根复合体。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• A Switch in the path between the root port and targeted legacy endpoint.
</td>
<td width="50%" style="background-color:#e8e8e8">
• 位于根端口与目标传统端点之间路径上的交换机。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• A PCI Express‐to‐PCI Bridge in the path to the target.
</td>
<td width="50%" style="background-color:#e8e8e8">
• 位于到达目标路径上的PCI Express到PCI桥。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• The target PCI device who's Device Driver initiated the locked RMW.
</td>
<td width="50%" style="background-color:#e8e8e8">
• 其设备驱动程序发起锁定读-修改-写（RMW）操作的目标PCI设备。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• A PCI Express endpoint is included to describe Switch behavior during lock.
</td>
<td width="50%" style="background-color:#e8e8e8">
• 包含一个PCI Express端点，用于描述锁定期间交换机的行为。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
In this example, the locked operation completes normally. The steps that occur during the operation are described in the two sections that follow.
</td>
<td width="50%" style="background-color:#e8e8e8">
在此示例中，锁定操作正常完成。操作期间发生的步骤将在接下来的两节中描述。
</td>
</tr>
</table>

## The Memory Read Lock Operation | 存储器读锁定操作

<table>
<tr>
<td width="50%">
Figure E-1 on page 967 illustrates the first step in the Locked transaction series (i.e., the initial memory read to obtain the semaphore):
</td>
<td width="50%" style="background-color:#e8e8e8">
图E-1（第967页）展示了锁定事务序列的第一步（即获取信号量的初始存储器读操作）：
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
1. The CPU initiates the locked sequence (a Locked Memory Read) as a result of a driver executing a locked RMW instruction that targets a PCI target.
</td>
<td width="50%" style="background-color:#e8e8e8">
1. 由于驱动执行了针对PCI目标的锁定RMW（读-修改-写）指令，CPU发起锁定序列（锁定存储器读）。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
2. The Root Port issues a Memory Read Lock Request from port 2. The Root Complex is always the source of a locked sequence.
</td>
<td width="50%" style="background-color:#e8e8e8">
2. 根端口从端口2发出存储器读锁定请求。根复合体始终是锁定序列的发起源。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
3. The Switch receives the lock request on its upstream port and forwards the request to the target egress port (3). The switch, upon forwarding the request to the egress port, must block all requests from ports other than the ingress port (1) from being sent from the egress port.
</td>
<td width="50%" style="background-color:#e8e8e8">
3. 交换机在其上游端口接收锁定请求，并将该请求转发到目标出口端口（3）。交换机在将请求转发到出口端口后，必须阻止除入口端口（1）之外的所有端口的请求从该出口端口发出。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
4. A subsequent peer-to-peer transfer from the illustrated PCI Express endpoint to the PCI bus (switch port 2 to switch port 3) would be blocked until the lock is cleared. Note that the lock is not yet established in the other direction. Transactions from the PCI Express endpoint could be sent to the Root Complex.
</td>
<td width="50%" style="background-color:#e8e8e8">
4. 后续从图示PCI Express端点到PCI总线（交换机端口2到交换机端口3）的对等传输将被阻塞，直到锁定解除。请注意，锁定在另一个方向上尚未建立。来自PCI Express端点的事务可以发送到根复合体。
</td>
</tr>
</table>

## PCI Express Technology | PCI Express技术

<table>
<tr>
<td width="50%">
5. The Memory Read Lock Request is sent from the Switch's egress port to the PCI Express‐to‐PCI Bridge. This bridge will implement PCI lock semantics (See the MindShare book entitled PCI System Architecture, Fourth Edition, for details regarding PCI lock).
</td>
<td width="50%" style="background-color:#e8e8e8">
5. Memory Read Lock Request从交换机的出口端口发送到PCI Express-to-PCI桥。该桥将实现PCI锁定语义（关于PCI锁定的详细信息，请参阅MindShare所著的《PCI系统架构第四版》）。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
6. The bridge performs the Memory Read transaction on the PCI bus with the PCI LOCK# signal asserted. The target memory device returns the requested semaphore data to the bridge.
</td>
<td width="50%" style="background-color:#e8e8e8">
6. 桥在PCI总线上执行Memory Read事务，并置位PCI LOCK#信号。目标存储器设备将请求的信号量数据返回给桥。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
7. Read data is returned to the Bridge and is delivered back to the Switch via a Memory Read Lock Completion with Data (CplDLk).
</td>
<td width="50%" style="background-color:#e8e8e8">
7. 读取数据返回到桥，并通过带数据的Memory Read Lock Completion（CplDLk）传回给交换机。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
8. The switch uses ID routing to return the packet upstream towards the host processor. When the CplDLk packet is forwarded to the upstream port of the Switch, it establishes a lock in the upstream direction to prevent traffic from other ports from being routed upstream. The PCI Express endpoint is completely blocked from sending any transaction to the Switch ports via the path of the locked operation. Note that transfers between Switch ports not involved in the locked operation would be permitted (not shown in this example).
</td>
<td width="50%" style="background-color:#e8e8e8">
8. 交换机使用ID路由将报文向上游发送到主机处理器。当CplDLk报文被转发到交换机的上游端口时，它会在上游方向建立锁定，以防止来自其他端口的流量被路由到上游。PCI Express端点被完全阻塞，无法通过锁定操作的通路向交换机端口发送任何事务。注意，不涉及锁定操作的交换机端口之间的传输是允许的（本例中未显示）。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
9. Upon detecting the CplDLk packet, the Root Complex knows that the lock has been established along the path between it and the target device, and the completion data is sent to the CPU.
</td>
<td width="50%" style="background-color:#e8e8e8">
9. 当检测到CplDLk报文时，根复合体知道锁定已在其与目标设备之间的路径上建立，完成数据被发送到CPU。
</td>
</tr>
</table>

Figure D‐1: Lock Sequence Begins with Memory Read Lock Request | 图D‐1：锁定序列以存储器读锁定请求开始
<img src="images/part06_f6913aa97476401663ef2a81abb4e6b5da7417c5e2f611200ca27786fdc6951b.jpg" width="700" alt="">

## Read Data Modified and Written to Target and Lock Completes | 读取数据修改后写入目标并完成锁定

<table>
<tr>
<td width="50%">
The device driver receives the semaphore value, alters it, and then initiates a memory write to update the semaphore within the memory of the legacy PCI device. Figure E-2 on page 969 illustrates the write sequence followed by the
</td>
<td width="50%" style="background-color:#e8e8e8">
设备驱动程序接收信号量值，修改该值，然后发起一次存储器写操作，以更新传统PCI器件存储器中的信号量。第969页的图E-2展示了写入序列，随后由
</td>
</tr>
</table>

## PCI Express Technology | PCI Express技术

<table>
<tr>
<td width="50%">
Root Complex's transmission of the Unlock message that releases the lock:
</td>
<td width="50%" style="background-color:#e8e8e8">
根复合体发送Unlock报文以释放锁定：
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
10. The Root Complex issues the Memory Write Request across the locked path to the target device.
</td>
<td width="50%" style="background-color:#e8e8e8">
10. 根复合体通过锁定路径向目标设备发出Memory Write Request。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
11. The Switch forwards the transaction to the target egress port (3). The memory address of the Memory Write must be the same as the initial Memory Read request.
</td>
<td width="50%" style="background-color:#e8e8e8">
11. 交换机将事务转发到目标出口端口(3)。Memory Write的存储器地址必须与初始Memory Read请求相同。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
12. The bridge forwards the transaction to the PCI bus.
</td>
<td width="50%" style="background-color:#e8e8e8">
12. 桥接器将事务转发到PCI总线。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
13. The target device receives the memory write data.
</td>
<td width="50%" style="background-color:#e8e8e8">
13. 目标设备接收到存储器写数据。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
14. Once the Memory Write transaction is sent from the Root Complex, it sends an Unlock message to instruct the Switches and any PCI/PCI‐X bridges in the locked path to release the lock. Note that the Root Complex presumes the operation has completed normally (because memory writes are posted and no Completion is returned to verify success).
</td>
<td width="50%" style="background-color:#e8e8e8">
14. 一旦从根复合体发送了Memory Write事务，它就发送一个Unlock报文来指示锁定路径中的交换机和任何PCI/PCI‐X桥接器释放锁定。注意，根复合体假定操作已正常完成（因为存储器写是Posted事务，不会返回Completion来验证成功）。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
15. The Switch receives the Unlock message, unlocks its ports and forwards the message to the egress port that was locked to notify any other Switches and/ or bridges in the locked path that the lock must be cleared.
</td>
<td width="50%" style="background-color:#e8e8e8">
15. 交换机接收Unlock报文，解锁其端口，并将该报文转发到被锁定的出口端口，以通知锁定路径中的任何其他交换机和/或桥接器必须清除锁定。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
16. Upon detecting the Unlock message, the bridge must also release the lock on the PCI bus.
</td>
<td width="50%" style="background-color:#e8e8e8">
16. 检测到Unlock报文后，桥接器也必须释放PCI总线上的锁定。
</td>
</tr>
</table>

Figure D‐2: Lock Completes with Memory Write Followed by Unlock Message | 图D‐2：锁定以存储器写后跟解锁消息完成
<img src="images/part06_5b9488b3a211370278d851a4da3e757bbb0a8776bfad32d700487c491a9d52cb.jpg" width="700" alt="">

## 99.3.3 Notification of an Unsuccessful Lock | 99.3.3 锁定失败通知

<table>
<tr>
<td width="50%">
A locked transaction series is aborted when the initial Memory Read Lock Request receives a Completion packet with no data (CplLk). This means that the locked sequence must terminate because no data was returned. This could result from an error associated with the memory read transaction, or perhaps the target device is busy and cannot respond at this time.
</td>
<td width="50%" style="background-color:#e8e8e8">
当事初始内存读取锁定请求收到一个不带数据的完成报文(CplLk)时，锁定事务序列被中止。这意味着由于没有返回数据，锁定序列必须终止。这可能是由与内存读取事务相关的错误所致，或者目标设备正忙而暂时无法响应。
</td>
</tr>
</table>

## 99.4 Summary of Locking Rules | 99.4 锁定规则总结

<table>
<tr>
<td width="50%">
Following is a list of ordering rules that apply to the Root Complex, Switches, and Bridges.
</td>
<td width="50%" style="background-color:#e8e8e8">
以下是适用于根复合体、交换机和桥的排序规则列表。
</td>
</tr>
</table>

## 99.4.1 Rules Related To the Initiation and Propagation of Locked Transactions | 99.4.1 锁定事务的发起与传播相关规则

<table>
<tr>
<td width="50%">
Locked Requests which are completed with a status other than Successful Completion do not establish lock.
</td>
<td width="50%" style="background-color:#e8e8e8">
以非成功完成状态完成锁定请求不会建立锁。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Regardless of the status of any of the Completions associated with a locked sequence, all locked sequences and attempted locked sequences must be terminated by the transmission of an Unlock Message.
</td>
<td width="50%" style="background-color:#e8e8e8">
无论与锁定序列相关的任何完成报文的状态如何，所有锁定序列及尝试的锁定序列都必须通过发送解锁报文来终止。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
MRdLk, CplDLk and Unlock semantics are allowed only for the default Traffic Class (TC0).
</td>
<td width="50%" style="background-color:#e8e8e8">
MRdLk、CplDLk 和 Unlock 语义仅允许用于默认流量类 (TC0)。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• Only one locked transaction sequence attempt may be in progress at a given time within a single hierarchy domain.
</td>
<td width="50%" style="background-color:#e8e8e8">
• 在单个层次域内，同一时刻只能有一个锁定事务序列尝试在进行中。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Any device which is not involved in the locked sequence must ignore the Unlock Message.
</td>
<td width="50%" style="background-color:#e8e8e8">
未参与锁定序列的任何设备必须忽略解锁报文。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
The initiation and propagation of a locked transaction sequence through the PCI Express fabric is performed as follows:
</td>
<td width="50%" style="background-color:#e8e8e8">
锁定事务序列在 PCI Express 结构中的发起与传播如下进行：
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• A locked transaction sequence is started with a MRdLk Request:
</td>
<td width="50%" style="background-color:#e8e8e8">
• 锁定事务序列以 MRdLk 请求开始：
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
— Any successive reads associated with the locked transaction sequence must also use MRdLk Requests.
</td>
<td width="50%" style="background-color:#e8e8e8">
— 与锁定事务序列相关的任何后续读取也必须使用 MRdLk 请求。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
The Completions for any successful MRdLk Request use the CplDLk Completion type, or the CplLk Completion type for unsuccessful Requests.
</td>
<td width="50%" style="background-color:#e8e8e8">
任何成功 MRdLk 请求的完成报文使用 CplDLk 完成类型，而不成功的请求则使用 CplLk 完成类型。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
If any read associated with a locked sequence is completed unsuccessfully, the Requester must assume that the atomicity of the lock is no longer assured, and that the path between the Requester and Completer is no longer locked.
</td>
<td width="50%" style="background-color:#e8e8e8">
如果与锁定序列相关的任何读取未成功完成，请求者必须假定锁的原子性不再得到保证，且请求者与完成者之间的路径不再被锁定。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
• All writes associated with a locked sequence must use MWr Requests.
</td>
<td width="50%" style="background-color:#e8e8e8">
• 与锁定序列相关的所有写入必须使用 MWr 请求。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
The Unlock Message is used to indicate the end of a locked sequence. A Switch propagates Unlock Messages through the locked Egress Port.
</td>
<td width="50%" style="background-color:#e8e8e8">
解锁报文用于指示锁定序列的结束。交换机通过加锁的出口端口传播解锁报文。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
Upon receiving an Unlock Message, a legacy Endpoint or Bridge must unlock itself if it is in a locked state. If it is not locked, or if the Receiver is a PCI Express Endpoint or Bridge which does not support lock, the Unlock Message is ignored and discarded.
</td>
<td width="50%" style="background-color:#e8e8e8">
在接收到解锁报文时，传统端点或桥如果处于锁定状态则必须解锁自身。如果其未被锁定，或者接收者是不支持锁的 PCI Express 端点或桥，则解锁报文将被忽略并丢弃。
</td>
</tr>
</table>

## 99.4.2 Rules Related to Switches | 99.4.2 与交换机相关的规则

<table>
<tr>
<td width="50%">
Switches must detect transactions associated with locked sequences from other transactions to prevent other transactions from interfering with the lock and potentially causing deadlock. The following rules cover how this is done. Note that locked accesses are limited to TC0, which is always mapped to VC0.
</td>
<td width="50%" style="background-color:#e8e8e8">
交换机必须能从其他事务中检测与锁定序列相关联的事务，以防止其他事务干扰锁定并可能导致死锁。以下规则涵盖了如何实现这一点。请注意，锁定访问仅限于TC0，而TC0始终映射到VC0。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
When a Switch propagates a MRdLk Request from an Ingress Port to the Egress Port, it must block all Requests which map to the default Virtual Channel (VC0) from being propagated to the Egress Port. If a subsequent MRdLk Request is received at this Ingress Port addressing a different Egress Port, the behavior of the Switch is undefined. Note that this sort of split-lock access is not supported by PCI Express and software must not cause such a locked access. System deadlock may result from such accesses.
</td>
<td width="50%" style="background-color:#e8e8e8">
当交换机将MRdLk请求从入端口传播到出端口时，它必须阻止所有映射到默认虚通道(VC0)的请求传播到该出端口。如果随后在此入端口收到寻址不同出端口的MRdLk请求，则交换机的行为是未定义的。请注意，这种类型的分离锁定访问不受PCI Express支持，软件不得导致此类锁定访问。此类访问可能导致系统死锁。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
When the CplDLk for the first MRdLk Request is returned, if the Completion indicates a Successful Completion status, the Switch must block all Requests from all other Ports from being propagated to either of the Ports involved in the locked access, except for Requests which map to channels other than VC0 on the Egress Port.
</td>
<td width="50%" style="background-color:#e8e8e8">
当针对第一个MRdLk请求的CplDLk返回且完成报文指示成功完成状态时，交换机必须阻止所有来自其他端口的请求传播到涉及锁定访问的两个端口中的任何一个，但映射到出端口上VC0以外通道的请求除外。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
The two Ports involved in the locked sequence must remain blocked until the Switch receives the Unlock Message (at the Ingress Port which received the initial MRdLk Request)

— The Unlock Message must be forwarded to the locked Egress Port.

— The Unlock Message may be broadcast to all other Ports.
</td>
<td width="50%" style="background-color:#e8e8e8">
涉及锁定序列的两个端口必须保持阻塞状态，直到交换机在收到初始MRdLk请求的入端口处接收到解锁消息。

— 解锁消息必须转发到被锁定的出端口。

— 解锁消息可以广播到所有其他端口。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
The Ingress Port is unblocked once the Unlock Message arrives, and the Egress Port(s) which were blocked are unblocked following the transmission of the Unlock Message out of the Egress Port(s). Ports that were not involved in the locked access are unaffected by the Unlock Message.
</td>
<td width="50%" style="background-color:#e8e8e8">
一旦解锁消息到达，入端口即解除阻塞，而被阻塞的出端口在解锁消息从该出端口发送出去后解除阻塞。未涉及锁定访问的端口不受解锁消息的影响。
</td>
</tr>
</table>

## 99.4.3 Rules Related To PCI Express/PCI Bridges | 99.4.3 PCI Express/PCI 桥相关规则

<table>
<tr>
<td width="50%">
The requirements for PCI Express/PCI Bridges are similar to those for Switches, except that, because these Bridges only use TC0 and VC0, all other traffic is blocked during the locked access. Requirements on the PCI bus side are described in the MindShare book, PCI System Architecture, Fourth Edition.
</td>
<td width="50%" style="background-color:#e8e8e8">
PCI Express/PCI 桥的需求与交换机类似，不同之处在于，由于这些桥仅使用 TC0 和 VC0，因此在锁定访问期间所有其他流量都被阻止。PCI 总线侧的需求在 MindShare 书籍《PCI 系统体系结构（第四版）》中描述。
</td>
</tr>
</table>

## 99.4.4 Rules Related To the Root Complex | 99.4.4 与根复合体相关的规则

<table>
<tr>
<td width="50%">
A Root Complex is permitted to support locked transactions as a Requester. If locked transactions are supported, a Root Complex must follow the rules already described to perform a locked access. The mechanism(s) used by the Root Complex to interface to the host processor's FSB (Front‐Side Bus) are outside the scope of the spec.
</td>
<td width="50%" style="background-color:#e8e8e8">
根复合体作为请求者可以支持锁定事务。如果支持锁定事务，根复合体必须遵循已描述的规则来执行锁定访问。根复合体用于与主机处理器FSB（前端总线）接口的机制不在本规范范围内。
</td>
</tr>
</table>

## 99.4.5 Rules Related To Legacy Endpoints | 99.4.5 与传统端点相关的规则

<table>
<tr>
<td width="50%">
Legacy Endpoints are permitted to support locked accesses, although their use is discouraged. If locked accesses are supported, legacy Endpoints must handle them as follows:
</td>
<td width="50%" style="background-color:#e8e8e8">
允许传统端点支持锁定访问，但不鼓励使用。如果支持锁定访问，传统端点必须按如下方式处理：
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
The legacy Endpoint becomes locked when it transmits the first Completion for the first read request of the locked transaction series access with a Successful Completion status:
</td>
<td width="50%" style="background-color:#e8e8e8">
当传统端点传输锁定事务系列访问中第一个读请求的第一个完成报文且状态为成功完成时，该传统端点即被锁定：
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
— If the completion status is not Successful Completion, the legacy Endpoint does not become locked.
</td>
<td width="50%" style="background-color:#e8e8e8">
— 如果完成报文状态不是成功完成，则传统端点不会进入锁定状态。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
— Once locked, the legacy Endpoint must remain locked until it receives the Unlock Message.
</td>
<td width="50%" style="background-color:#e8e8e8">
— 一旦锁定，传统端点必须保持锁定状态，直到收到解锁消息。
</td>
</tr>
</table>

<table>
<tr>
<td width="50%">
While locked, a legacy Endpoint must not issue any Requests using Traffic Classes which map to the default Virtual Channel (VC0). Note that this requirement applies to all possible sources of Requests within the Endpoint, in the case where there is more than one possible source of Requests. Requests may be issued using TCs which map to VCs other than VC0.
</td>
<td width="50%" style="background-color:#e8e8e8">
在锁定状态下，传统端点不得使用映射到默认虚通道（VC0）的流量类发出任何请求。注意，此要求适用于端点内所有可能的请求源（如果有多个可能的请求源）。可以使用映射到非VC0的虚通道的流量类来发出请求。
</td>
</tr>
</table>