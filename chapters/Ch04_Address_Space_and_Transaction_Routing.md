## 第 4 章:地址空间与事务路由

将地址空间同时映射到内存地址空间和 IO 地址空间。这样,新软件可以使用内存地址空间(MMIO)访问设备的内部位置,同时允许传统(旧版)软件继续工作,因为它仍可以使用 IO 地址空间访问设备的内部寄存器。

不依赖传统软件或没有传统兼容性问题的较新设备通常仅通过内存地址空间(MMIO)映射内部寄存器/存储,不申请 IO 地址空间。事实上,PCI Express 规范实际上并不鼓励使用 IO 地址空间,指出它只是为了兼容传统原因而保留,并可能在规范的未来修订版中被弃用。

通用的内存与 IO 地址映射如图 4-1(第 125 页)所示。内存映射的大小取决于系统可使用的地址范围(通常由 CPU 可寻址范围决定)。PCIe 中 IO 映射的大小限制为 32 位(4 GB),尽管在使用 Intel 兼容(x86)处理器的许多计算机中,实际仅使用低 16 位(64 KB)。PCIe 可支持最高 64 位的内存地址。

图 4-1 中的映射示例仅显示了 Endpoint 申请 MMIO 和 IO 空间的能力,但该能力并非 Endpoint 独有。Switch 和 Root Complex 通常也具有通过 MMIO 和 IO 地址访问的设备特定寄存器。

## 可预取与不可预取内存空间

图 4-1 展示了 PCIe 设备所声明的两种不同类型的 MMIO:可预取 MMIO(P-MMIO)与不可预取 MMIO(NP-MMIO)。有必要说明可预取与不可预取内存空间之间的区别。可预取空间具有两个非常明确的属性:

- 读操作没有副作用

- 允许写合并

将一段 MMIO 区域定义为可预取,允许以投机方式预先取出该区域中的数据,以预期 Requester 在不久的将来可能需要比实际请求更多的数据。这样做这种轻度数据缓存之所以是安全的,是因为读取数据不会改变目标设备的任何状态信息。也就是说,读取该位置的行为不会产生副作用。例如,如果 Requester 请求从某地址读取 128 字节,Completer 也可以预先取出紧随其后的 128 字节,以便在请求到达时立即可用,从而改善性能。然而,如果 Requester 始终不再请求这些额外数据,Completer 最终将不得不丢弃它们以释放缓冲区空间。如果读取数据的动作会改变该地址处的值(或者产生其他某种副作用),那么被丢弃的数据将无法再恢复。但是,对于可预取空间而言,读取操作没有副作用,因此始终可以稍后再回去读取,因为原始数据仍然存在。

你也许会好奇,什么样的内存空间可能存在读取副作用呢?一个例子是内存映射的状态寄存器,它被设计为在读取时自动清除自身,以省去程序员在读取状态后显式清除相应位的额外步骤。

对于 PCI 而言,做出这一区分比对于 PCIe 更为重要,因为该总线协议的事务并不包含传输大小。当交换数据的设备位于同一总线上时,这并不是一个问题,因为存在实时握手来指示请求方何时已完成且不再需要更多数据,因此字节数是否已知并不是那么重要。但是当传输必须跨越桥接器时,就没那么容易了,因为对于读操作,桥接器需要在另一侧总线上收集数据时猜测字节数。传输大小猜测错误会增加延迟并降低性能,因此获得预取权限会非常有帮助。这就是为什么在 PCI 中将内存空间指定为可预取是有意义的。由于 PCIe 请求确实包含传输大小,所以这种区分的意义已不如从前,但为了向后兼容,该特性被保留了下来。

## 第 4 章:地址空间与事务路由

图 4‐1:通用存储器与 IO 地址映射  
![](images/part02_ff238d8cb4d6de759075adb4d19f3f6e7aaf994543232b6497dd0bd93541edef.jpg)


---

## 基址寄存器 (BARs)


---

## 概述

系统中的每个设备在所需地址空间的大小和类型方面可能有不同的要求。例如,某个设备可能有 256 字节的内部寄存器/存储空间,应通过 IO 地址空间访问;另一个设备可能有 16KB 的内部寄存器/存储空间,应通过 MMIO 访问。

基于 PCI 的设备不被允许自行决定使用哪些地址来访问其内部位置,这是系统软件(即 BIOS 和 OS 内核)的工作。因此,设备必须为系统软件提供一种方式,以确定设备的地址空间需求。一旦软件知道了设备在地址空间方面的需求,那么在请求可以被满足的前提下,软件只需为该设备分配一个可用的、类型适当(IO、NP-MMIO 或 P-MMIO)的地址范围。

上述功能全部通过配置空间包头中的基址寄存器(BAR)实现。如第 127 页的图 4-2 所示,Type 0 包头提供六个 BAR(每个 32 位),而 Type 1 包头仅有两个 BAR。Type 1 包头出现在所有桥设备中,这意味着每个交换机端口和根复合体端口都具有 Type 1 包头。Type 0 包头位于非桥设备中,例如端点。第 128 页的图 4-3 给出了示例。

系统软件必须首先确定设备请求的地址空间的大小和类型。设备设计者清楚应通过 IO 或 MMIO 访问的内部寄存器/存储的总大小。设备设计者同样清楚当这些寄存器被访问时设备的行为(即读操作是否具有副作用)。这将决定应请求可预取 MMIO(读操作无副作用)还是不可预取 MMIO(读操作有副作用)。基于这些信息,设备设计者将 BAR 的低位硬编码为特定的值,以指示所请求地址空间的类型和大小。

BAR 的高位可由软件写入。系统软件检查 BAR 的低位以确定所请求地址空间的大小和类型后,系统软件随后会将分配给该设备的地址范围的基地址写入 BAR 的高位。由于单个

端点(Type 0 包头)具有六个 BAR,最多可以发起六个不同的地址空间请求。然而,这种情况在实际应用中并不常见。大多数设备会请求 1-3 个不同的地址范围。

并非所有 BAR 都必须实现。如果某个设备不需要使用全部 BAR 来映射其内部寄存器,多余的 BAR 会被硬编码为全 0,以此通知软件这些 BAR 未实现。

图 4-2:配置空间中的 BAR  
![](images/part02_0754b36296a00a43f0467a2571863dc6744e5c61e356c6ed1820fa1e873af09d.jpg)

一旦 BAR 被编程,设备内部的寄存器或本地存储器就可以通过编程到 BAR 中的地址范围来访问。任何时候,当设备看到某个请求的地址映射到其某个 BAR 时,它都会接受该请求,因为它就是目标设备。

图 4-3:PCI Express 设备及 Type 0 和 Type 1 包头的使用  
![](images/part02_880d7b01ffbe102c74937fdb9de0855f5ef6606ba36a5ca59c0258f40509fd4c.jpg)

## BAR 示例 1:32 位存储器地址空间请求

第 130 页的图 4-4 展示了设置 BAR 的基本步骤,在本例中,该 BAR 请求一段 4KB 的不可预取存储器 (NP-MMIO)。在图中,该 BAR 在配置过程中被展示了三个状态:

1. 在图 4-4 的 (1) 中,我们看到 BAR 的未初始化状态。设备设计者已将低位固定,以指示大小和类型,但高位(可读写的)显示为 X,表示其值未知。系统软件首先会对每个 BAR 写入全 1(通过配置写操作)以置位所有可写位。(当然,硬编码的低位不受任何配置写操作影响。)图 4-4 的 (2) 显示的 BAR 第二次视图展示了配置软件对其写入全 1 之后的状态。

写入全 1 的目的是确定最低有效可写位的位置。该位的位置指示了所请求地址空间的大小。在本例中,最低有效可写位是第 12 位,因此该 BAR 请求的地址空间大小为 $2^{12}$(即 4KB)。如果最低有效可写位是第 20 位,那么该 BAR 请求的地址空间大小就是 $2^{20}$(即 1MB)。

2. 在对所有 BAR 写入全 1 之后,软件转而从 BAR0 开始读取每个 BAR 的值,以确定所请求地址空间的类型和大小。第 129 页的表 4-1 总结了本例中对 BAR0 进行配置读的结果。

3. 此过程的最后一步是,既然软件已经知道了所请求地址空间的大小和类型,就由系统软件为 BAR0 分配一段地址范围。图 4-4 的 (3) 中显示的 BAR 第三次视图展示了软件写入了所分配地址块的起始地址之后的状态。在本例中,起始地址为 F900_0000h。

至此 BAR0 的配置完成。一旦软件在 Command 寄存器(偏移 04h)中使能存储器地址译码,只要该设备收到的存储器请求落在从 F900_0000h - F900_0FFFh(大小为 4KB)的范围内,它都将予以接受。

表 4-1:对 BAR 写入全 1 之后读取的结果

<table><tr><td>BAR 位</td><td>含义</td></tr><tr><td>0</td><td>读出为 0b,表示这是一个存储器请求。由于这是存储器请求,位 3:1 也具有编码含义。</td></tr><tr><td>2:1</td><td>读出为 00b,表示目标仅支持 32 位地址译码</td></tr><tr><td>3</td><td>读出为 0b,表示请求的是不可预取存储器(意味着读操作具有副作用);NP-MMIO</td></tr><tr><td>11:4</td><td>读出为全 0,表示请求的大小(这些位被硬编码为 0)</td></tr><tr><td>31:12</td><td>读出为全 1,因为软件尚未用该地址块的起始地址编程这些高位。由于第 12 位是最低有效可写位,所以请求的存储器大小为 $2^{12} = 4KB$。</td></tr></table>

图 4-4:32 位不可预取存储器 BAR 的建立
![](images/part02_c2d206df7d7c6b9fd1b3f40d41fdb0917bc4fef31eb4396435b8ddcf02c672e5.jpg)

## BAR 示例 2:64 位存储器地址空间请求

在上一示例中,我们看到 BAR0 被用于请求非预取存储器地址空间(NP-MMIO)。在本示例中,如图 4-5(第 132 页)所示,BAR1 和 BAR2 被用于请求一块 64MB 的可预取存储器地址空间。这里使用了两个连续的 BAR,是因为该设备为此请求支持 64 位地址,这意味着软件可以根据需要将所请求的地址空间分配在 4GB 地址边界之上(但这不是必需的)。由于地址可以是 64 位地址,必须将两个连续的 BAR 配合使用。

与之前一样,BAR 在配置过程的三个时间点被展示出来:

1. 在图 4-5 的 (1) 中,我们看到 BAR 对的未初始化状态。设备设计者已将下方 BAR(本例中为 BAR1)的低位硬编码,以指示请求的类型和大小,而上方 BAR(BAR2)的各位都是可读写的。系统软件的第一步是向每个 BAR 写入全 1。在图 4-5 的 (2) 中,我们看到在向所有 BAR 写入全 1 之后它们的状态。

2. 如上一示例所述,系统软件已经评估过 BAR0。因此软件的下一步是读取下一个 BAR(BAR1)并对其进行评估,以查看设备是否正在请求额外的地址空间。一旦读取 BAR1,软件便意识到正在请求更多的地址空间,并且该请求是针对可预取存储器地址空间的,该空间可以分配在 64 位地址范围内的任何位置。由于它支持 64 位地址,下一个连续的 BAR(本例中为 BAR2)被视为 BAR1 的高 32 位。因此软件现在也读取 BAR2 的内容。然而,软件不会像评估 BAR1 那样评估 BAR2 的低位,这是因为它知道 BAR2 仅是 BAR1 中开始的 64 位地址请求的高 32 位。表 4-2(第 132 页)汇总了这些配置读取的结果。

3. 此过程的最后一步是,当软件知道了所请求地址空间的大小和类型之后,由系统软件为这些 BAR 分配一个地址范围。BAR 的第三种视图,在图 4-5 的 (3) 中显示了软件使用两次配置写入来为已分配范围编程 64 位起始地址之后的结果。在本示例中,上方 BAR 的第 1 位(BAR 对中的地址位 33)被置 1,下方 BAR 的第 30 位(BAR 对中的地址位 30)被置 1,以表示起始地址为 2\_4000\_0000h。这两个 BAR 中所有其他可写的位均被清零。

至此,BAR 对(BAR1 和 BAR2)的配置完成。一旦软件在 Command 寄存器(偏移量 04h)中使能存储器地址解码,当该设备收到的任何存储器请求落在 2\_4000\_0000h - 2\_43FF\_FFFFh(大小为 64MB)的范围内时,它将予以接受。

图 4-5:64 位可预取存储器 BAR 设置  
![](images/part02_fb829876472623d44b981cc4e53ef1c96d7e11dd42612871eca008f1974bc0e4.jpg)

表 4-2:对两个 BAR 都写入全 1 后读取 BAR 对的结果

<table><tr><td>BAR</td><td>BAR 位</td><td>含义</td></tr><tr><td>下方</td><td>0</td><td>读为 0b,表示这是一次存储器请求。由于这是存储器请求,位 3:1 也具有编码含义。</td></tr><tr><td>下方</td><td>2:1</td><td>读为 10b,表明目标支持 64 位地址解码器,并且下一个连续的 BAR 包含该地址信息的高 32 位。</td></tr><tr><td>下方</td><td>3</td><td>读为 1b,表示该请求是针对可预取存储器的(意味着读取操作没有副作用);P-MMIO</td></tr><tr><td>下方</td><td>25:4</td><td>读为全 0,表示该请求的大小(这些位被硬编码为 0)</td></tr><tr><td>下方</td><td>31:26</td><td>读为全 1,因为软件尚未对这些高位编程该块的起始地址。注意,由于位 26 是最低的可写位,因此存储器地址空间的请求大小为  $2^{26}$ ,即 64MB。</td></tr><tr><td>上方</td><td>31:0</td><td>读为全 1。这些位将作为由系统软件编程的 64 位起始地址的高 32 位使用。</td></tr></table>

---

## BAR 示例 3:IO 地址空间请求

承接前面两个示例,该功能同样在请求 IO 空间,如图 4‐6(第 134 页)所示。在图中,正在请求的 BAR(本例中为 BAR3)在配置过程的三个位置被标出:

1. 在图 4‐6 的 (1) 中,可以看到 BAR 的未初始化状态。系统软件此前已向每个 BAR 写入全 1,并依次评估了 BAR0、BAR1 和 BAR2。现在软件将检查此设备是否通过 BAR3 请求额外的地址空间。图 4‐6 的状态 (2) 展示了写入全 1 后 BAR3 的状态。

2. 软件现在读入 BAR3 以评估请求的大小和类型。第 134 页的表 4‐3 总结了该次配置读取的结果。

3. 既然软件已知这是一次针对 256 字节 IO 地址空间的请求,最后一步就是使用分配给该设备(具体来说就是此 BAR)的 IO 地址范围的基地址对该 BAR 进行编程。图 4‐6 的状态 (3) 展示了此步骤之后 BAR 的状态。在本例中,设备起始地址为 16KB,因此位 14 被写入,得到的基地址为 4000h;所有其他的高位均被清零。

至此,BAR3 的配置完成。一旦软件在 Command 寄存器(偏移 04h)中使能 IO 地址译码,设备将接受并响应地址范围 4000h ‐ 40FFh(共 256 字节)内的 IO 事务。

图 4‐6:IO BAR 的设置  
![](images/part02_003b2db033194e03040a960e27cf1abbdb191136b23a53a655620e2ca61d33eb.jpg)

表 4‐3:向 IO BAR 写入全 1 后的读取结果

<table><tr><td>BAR 位</td><td>含义</td></tr><tr><td>0</td><td>读出为 1b,表示一次 IO 请求。由于这是一次 IO 请求,因此位 1 被保留。</td></tr><tr><td>1</td><td>保留。硬连线为 0b。</td></tr><tr><td>7:2</td><td>读出为 0,表示请求的大小(这些位硬连线为 0)</td></tr><tr><td>31:8</td><td>读出为 1,因为软件尚未使用该块的起始地址对高位进行编程。注意,由于位 8 是最低可写位,因此 IO 请求的大小为  $2^{8}$ ,即 256 字节。</td></tr></table>


---

## 所有 BAR 必须按顺序评估

在经历了前面三个示例之后,情况就变得很清楚:软件必须按顺序评估 BAR。

大多数情况下,功能并不需要全部六个 BAR。即使在我们经历过的示例中,六个可用的 BAR 也只使用了四个。如果本示例中的功能不需要再请求额外的地址空间,设备设计人员会将 BAR4 和 BAR5 的所有位硬连线 (hard-code) 为 0。因此,即使软件向这些 BAR 写入全 1,这些写入也不会产生任何效果。在评估完 BAR3 之后,软件会继续评估 BAR4。一旦检测到没有任何位被置 1,软件就会知道此 BAR 未被使用,继而继续评估下一个 BAR。

所有 BAR 都必须被评估,即使软件发现某个 BAR 未被使用。PCI 或 PCIe 中没有任何规则规定 BAR0 必须是用于地址空间请求的第一个 BAR。如果设备设计人员愿意,他们可以使用 BAR4 来发出地址空间请求,并将 BAR0、BAR1、BAR2、BAR3 和 BAR5 都硬连线为全 0。这意味着软件必须评估包头中的每一个 BAR。

## 可调整大小的 BAR(Resizable BARs)

PCI Express 规范 2.1 版本通过在扩展配置空间中定义一种新的能力结构,新增了对 BAR 中请求地址空间大小进行调整的支持。该新结构允许功能部件声明其能够使用的地址空间大小,然后由系统软件根据可用资源启用其中一种大小。例如,如果某功能部件理想情况下希望使用 2GB 的可预取内存地址空间,但也可以仅以 1GB、512MB 或 256MB 的 P-MMIO 运行,那么当系统软件无法容纳更大空间的请求时,系统软件可能只会允许该功能部件请求 256MB 的地址空间。

## Base and Limit 寄存器

## 概述

一旦某个 Function 的 BAR 被编程完成,该 Function 就知道自己所拥有的地址范围,这意味着对于任何发往其所拥有地址范围(即编程在其某个 BAR 中的地址范围)的事务,该 Function 都会进行认领。这固然很好,但有一点很重要,必须认识到:该 Function 若要"看到"它应当认领的事务,其上游的 Bridge 必须将这些事务向下游转发到目标 Function 所连接的链路上。因此,每一个 Bridge(例如 Switch 端口和根复合体端口)都需要知道其下方有哪些地址范围,以便判断哪些请求应从其主接口(上游侧)转发到其次接口(下游侧)。如果请求所寻址的地址属于该 Bridge 下方某个 Function 的 BAR,则该请求应被转发到该 Bridge 的次接口。

正是 Type 1 包头中的 Base 和 Limit 寄存器,用于记录位于该 Bridge 下方的地址范围。每个 Type 1 包头中存在三组 Base 和 Limit 寄存器。需要三组寄存器的原因是,一个 Bridge 下方可能存在三段相互独立的地址范围:

• 可预取内存空间 (P‐MMIO)

• 不可预取内存空间 (NP‐MMIO)

• IO 空间 (IO)

为了说明这些 Base 和 Limit 寄存器如何工作,我们继续沿用上一节的示例,并将那个已被编程的 Function(一个 Endpoint)置于 Switch 之下,如图 4‐7(第 137 页)所示。该图中还列出了该 Function 的 BAR 所拥有的地址范围。

Endpoint 上游每一个 Bridge 的 Base 和 Limit 寄存器都需要被编程,但作为开始,我们将重点关注与 Endpoint 直接相连的那个 Bridge(端口 B)。

图 4‐7:用于设置 Base 和 Limit 值的拓扑示例  
![](images/part02_a35e23b613320d5bdb8fbce1ad4b754276b9d32ad4bee523d66c3e94362fdbd8.jpg)


---

## 预取地址范围 (P-MMIO)

Type 1 报头 (Header) 拥有两对预取内存 Base/Limit 寄存器。Prefetchable Memory Base/Limit 寄存器用于存储预取地址范围低 32 位的地址信息。如果该桥 (Bridge) 支持 64 位地址解码,则还需要使用 Prefetchable Memory Base/Limit Upper 32 Bits 寄存器,用于保存地址范围的高 32 位(位 [63:32])。第 138 页的图 4-8 给出了软件为指示预取地址范围 2\_4000\_0000h – 2\_43FF\_FFFFh 位于该桥 (Port B) 之下时,应写入这些寄存器的值。这些寄存器中各字段的含义汇总于表 4-4。

图 4-8:示例 Prefetchable Memory Base/Limit 寄存器值

<table><tr><td colspan="2">Device ID</td><td colspan="2">Vendor ID</td></tr><tr><td colspan="2">Status</td><td colspan="2">Command</td></tr><tr><td colspan="3">Class Code</td><td>Rev ID</td></tr><tr><td>BIST</td><td>Header Type</td><td>Latency Timer</td><td>Cache Line Size</td></tr><tr><td colspan="4">Base Address 0 (BAR0)</td></tr><tr><td colspan="4">Base Address 1 (BAR1)</td></tr><tr><td>Secondary Lat Timer</td><td>Subordinate Bus #</td><td>Secondary Bus #</td><td>Primary Bus #</td></tr><tr><td colspan="2">Secondary Status</td><td>IO Limit</td><td>IO Base</td></tr><tr><td colspan="2">(Non-Prefetchable) Memory Limit</td><td colspan="2">(Non-Prefetchable) Memory Base</td></tr><tr><td colspan="2">Prefetchable Memory Limit</td><td colspan="2">Prefetchable Memory Base</td></tr><tr><td colspan="4">Prefetchable Memory Base Upper 32 Bits</td></tr><tr><td colspan="4">Prefetchable Memory Limit Upper 32 Bits</td></tr><tr><td colspan="2">IO Limit Upper 16 Bits</td><td colspan="2">IO Base Upper 16 Bits</td></tr><tr><td colspan="3">Reserved</td><td>Capability Pointer</td></tr><tr><td colspan="4">Expansion ROM Base Address</td></tr><tr><td colspan="2">Bridge Control</td><td>Interrupt Pin</td><td>Interrupt Line</td></tr></table>

![](images/part02_85465c6b3a80c51edb75d9f4ed61ee62e089c610bea78ae06cd89b5276746731.jpg)

## 第 4 章:地址空间与事务路由

表 4‐4:可预取存储器 Base/Limit 寄存器含义示例

<table><tr><td>寄存器</td><td>值</td><td>用途</td></tr><tr><td>Prefetchable Memory Base</td><td>4001h</td><td>该寄存器的高 12 位保存 32 位 BASE 地址的高 12 位(位 [31:20])。基地址的低 20 位隐含为全 0,意味着基地址始终按 1MB 边界对齐。该寄存器的低 4 位指示桥是否支持 64 位地址解码,即是否使用 Upper Base/Limit 寄存器。</td></tr><tr><td>Prefetchable Memory Limit</td><td>43F1h</td><td>类似地,该寄存器的高 12 位保存 32 位 LIMIT 地址的高 12 位(位 [31:20])。Limit 地址的低 20 位隐含为全 F。该寄存器的低 4 位含义与 Base 寄存器的低 4 位相同。</td></tr><tr><td>Prefetchable Memory Base Upper 32 Bits</td><td>00000002h</td><td>保存该端口下游可预取存储器 64 位 BASE 地址的高 32 位。</td></tr><tr><td>Prefetchable Memory Limit Upper 32 Bits</td><td>00000002h</td><td>保存该端口下游可预取存储器 64 位 LIMIT 地址的高 32 位。</td></tr></table>


---

## 非预取范围 (NP-MMIO)

与可预取内存范围不同,非预取内存范围仅支持 32 位地址。因此,基址和上限各只有一个寄存器。按照图 4‐7 中的示例,Port B 的非预取内存基址/上限寄存器应按第 140 页图 4‐9 中所示的数值进行编程。这些数值的含义汇总在表 4‐5 中。

图 4‐9:非预取内存基址/上限寄存器值示例
Type 1 Header

<table><tr><td colspan="2">Device ID</td><td colspan="2">Vendor ID</td></tr><tr><td colspan="2">Status</td><td colspan="2">Command</</></tr><tr><td colspan="3">Class Code</td><td>Rev ID</td></tr><tr><td>BIST</td><td>Header Type</td><td>Latency Timer</td><td>Cache Line Size</td></tr><tr><td colspan="4">Base Address 0 (BAR0)</td></tr><tr><td colspan="4">Base Address 1 (BAR1)</td></tr><tr><td>Secondary Lat Timer</td><td>Subordinate Bus #</td><td>Secondary Bus #</td><td>Primary Bus #</td></tr><tr><td colspan="2">Secondary Status</td><td>IO Limit</td><td>IO Base</td></tr><tr><td colspan="2">(Non-Prefetchable) Memory Limit</td><td colspan="2">(Non-Prefetchable) Memory Base</td></tr><tr><td colspan="2">Prefetchable Memory Limit</td><td colspan="2">Prefetchable Memory Base</td></tr><tr><td colspan="4">Prefetchable Memory Base Upper 32 Bits</td></tr><tr><td colspan="4">Prefetchable Memory Limit Upper 32 Bits</td></tr><tr><td colspan="2">IO Limit Upper 16 Bits</td><td colspan="2">IO Base Upper 16 Bits</td></tr><tr><td colspan="3">Reserved</td><td>Capability Pointer</td></tr><tr><td colspan="4">Expansion ROM Base Address</td></tr><tr><td colspan="2">Bridge Control</td><td>Interrupt Pin</td><td>Interrupt Line</td></tr></table>

![](images/part02_b5ee420b6ebab86a49bcce4a1dabefa73c1033141db7c92cc24041fcaeb9a66c.jpg)

非预取内存范围:F900\_0000h - F90F\_FFFFh

表 4‐5:非预取内存基址/上限寄存器含义示例

<table><tr><td>寄存器</td><td>值</td><td>用途</td></tr><tr><td>(非预取)Memory Base</td><td>F900h</td><td>该寄存器的高 12 位保存 32 位 BASE 地址的高 12 位([31:20] 位)。基址的低 20 位隐含为全 0,意味着基址始终按 1MB 边界对齐。该寄存器的低 4 位必须为 0。</td></tr><tr><td>(非预取)Memory Limit</td><td>F900h</td><td>类似地,该寄存器的高 12 位保存 32 位 LIMIT 地址的高 12 位([31:20] 位)。上限地址的低 20 位隐含为全 F。该寄存器的低 4 位必须为 0。</td></tr></table>

本示例展示了一种值得关注的情况:在 Port B 的配置空间中编程的非预取地址范围(1MB)远大于其下游端点所拥有的 NP-MMIO 范围(4KB)。其原因在于,Type 1 Header 中的内存基址/上限寄存器只能用于指定 20 位及以上的地址位([31:20]),低 20 位地址位 [19:0] 是隐含的。因此,使用内存基址/上限寄存器所能指定的最小地址范围为 1MB。

在我们的示例中,端点请求并被授予了 4KB 的 NP-MMIO(F900\_0000h - F900\_0FFFh)。Port B 被编程为表明该端口下游存在 1MB(即 1024KB)的 NP-MMIO(F900\_0000h - F90F\_FFFFh)。这意味着有 1020KB(F900\_1000h - F90F\_FFFFh)的内存地址空间被浪费。该地址空间不能分配给其他端点,因为报文的路由将无法正常工作。

---

## IO Range

与可预取存储器范围一样,Type 1 Header (类型 1 包头) 也包含两对 IO Base/Limit 寄存器。IO Base/Limit 寄存器保存 IO 地址范围低 16 位的地址信息。如果该 Bridge (桥) 支持 32 位 IO 地址解码(在实际设备中较为少见),则还会使用 IO Base/Limit Upper 16 Bits 寄存器,用于保存 IO 地址范围的高 16 位(位 [31:16])。沿用上例,第 142 页的图 4-10 给出了软件为指示 4000h - 4FFFh 这一 IO 地址范围属于该 Bridge (Port B) 下游而向这些寄存器写入的值。这些寄存器中每个字段的含义汇总在表 4-6 中。

图 4-10:IO Base/Limit 寄存器示例值

<table><tr><td colspan="2">Device ID</td><td colspan="2">Vendor ID</td></tr><tr><td colspan="2">Status</td><td colspan="2">Command</td></tr><tr><td colspan="3">Class Code</td><td>RevID</td></tr><tr><td>BIST</td><td>Header Type</td><td>Latency Timer</td><td>Cache Line Size</td></tr><tr><td colspan="4">Base Address 0 (BAR0)</td></tr><tr><td colspan="4">Base Address 1 (BAR1)</td></tr><tr><td>Secondary Lat Timer</td><td>Subordinate Bus #</td><td>Secondary Bus #</td><td>Primary Bus #</td></tr><tr><td colspan="2">Secondary Status</td><td>IO Limit</td><td>IO Base</td></tr><tr><td colspan="2">(Non-Prefetchable) Memory Limit</td><td colspan="2">(Non-Prefetchable) Memory Base</td></tr><tr><td colspan="2">Prefetchable Memory Limit</td><td colspan="2">Prefetchable Memory Base</td></tr><tr><td colspan="4">Prefetchable Memory Base Upper 32 Bits</td></tr><tr><td colspan="4">Prefetchable Memory Limit Upper 32 Bits</td></tr><tr><td colspan="2">IO Limit Upper 16 Bits</td><td colspan="2">IO Base Upper 16 Bits</td></tr><tr><td colspan="3">Reserved</td><td>Capability Pointer</td></tr><tr><td colspan="4">Expansion ROM Base Address</td></tr><tr><td colspan="2">Bridge Control</td><td>Interrupt Pin</td><td>Interrupt Line</td></tr></table>

![](images/part02_38a387246db1e2abb691885e5a75d06270c47bffec7d92eb9c23ededa1be4c6a.jpg)

表 4-6:IO Base/Limit 寄存器示例含义

<table><tr><td>Register</td><td>Value</td><td>Use</td></tr><tr><td>IO Base</td><td>40h</td><td>该寄存器的高 4 位保存 16 位 BASE 地址的高 4 位(位 [15:12])。基地址的低 12 位隐含为全 0,意味着基地址始终在 4KB 边界上对齐。该寄存器的低 4 位指示该 Bridge (桥) 是否支持 32 位 IO 地址解码器,即是否使用 Upper Base/Limit 寄存器。</td></tr><tr><td>IO Limit</td><td>40h</td><td>类似地,该寄存器的高 4 位保存 16 位 LIMIT 地址的高 4 位(位 [15:12])。Limit 地址的低 12 位隐含为全 F。该寄存器的低 4 位的含义与 Base 寄存器的低 4 位相同。</td></tr><tr><td>IO Base Upper 16 Bits</td><td>0000h</td><td>保存该端口下游 IO 的 32 位 BASE 地址的高 16 位。</td></tr><tr><td>IO Limit Upper 16 Bits</td><td>0000h</td><td>保存该端口下游 IO 的 32 位 LIMIT 地址的高 16 位。</td></tr></table>

在该示例中,我们再次看到一种情况:编程到上游 Bridge (桥) 中的地址范围远大于下游 Function (功能) 实际拥有的地址范围。本例中的 Endpoint (端点) 拥有 256 字节的 IO 地址空间(具体为 4000h - 40FFh)。Port B 已被编程为指示下游存在 4KB IO 地址空间(地址 4000h - 4FFFh)。同样,这仅仅是 Type 1 Header (类型 1 包头) 的一种限制。对于 IO 地址空间,低 12 位(位 [11:0])为隐含值,因此可指定的最小 IO 地址范围是 4KB。该限制实际上比存储器范围的 1MB 最小窗口更为严重。在基于 x86(Intel 兼容)的系统中,处理器仅支持 16 位 IO 地址空间,而由于 Bridge (桥) 中只能指定 IO 地址范围的位 [15:12],这意味着系统中最多只能有 16 (2<sup>4</sup>) 个不同的 IO 地址范围。

---

## 未使用的 Base 和 Limit 寄存器

并非每个 PCIe 设备都会使用全部三种地址空间。事实上,PCI Express 规范实际上并不鼓励使用 IO 地址空间,并指出它只是为了向后兼容而保留,可能在未来版本的规范中被废弃。

在端点并未请求全部三种地址空间的情况下,其上游桥的 base 和 limit 寄存器应编程为何值?它们不能全部编程为 0,因为低地址位仍然会被隐含地认为不同(base = 0;limit = F),这会表示一个有效范围。因此,为了处理这些情况,limit 寄存器的值必须编程为高于 base 的地址。例如,如果某个端点没有请求 IO 地址空间,那么紧邻该功能上游的桥应将其 IO Base 寄存器编程为 00h,并将其 IO Limit 寄存器编程为 F0h。由于 limit 地址高于 base 地址,桥明白这是一个无效设置,并将其理解为:其下游不存在拥有 IO 地址空间的功能。

这种使 base 和 limit 寄存器无效的方法对全部三对 base/limit 寄存器都有效,而不只针对 IO base/limit 寄存器。

## Sanity Check: Registers Used For Address Routing

为了确保你理解 BAR 和 Base/Limit 寄存器的设置规则与方法,请翻阅第 145 页的图 4‐11 以确认其含义。我们只是将示例系统加以扩展,把另一个 endpoint 以及交换机的一个端口(Port A)所请求的额外地址空间纳入其中。请注意,Type 1 报文头也包含 BAR(准确来说是两个),同样可以请求地址空间。桥中的 Base/Limit 寄存器**并不**包含该桥自身 BAR 所拥有的地址。Base/Limit 寄存器仅表示位于该桥下游的地址。

Figure 4‐11: Final Example Address Routing Setup  
![](images/part02_1fb4688cc0829b4d5235f0affa8ed10db0ed46cd85a1abccb1a22d7b7d7b1db3.jpg)

## TLP 路由基础

如前文各节所述,设置 BAR 以及 Base/Limit 寄存器的目的是,确保发往某个功能的报文能够被正确路由,使该目标功能能够看到这些事务并将其认领(Claim)。在 PCI 这类共享总线架构中,所有报文对每个设备都是可见的。请求被路由仅发生在目标位于另一条总线上、且必须跨越某条桥的时候。由于 PCIe 链路(Link)是点对点的,因此要在设备之间递送事务就需要更多的路由动作。

图 4-12:多端口 PCIe 设备承担路由职责  
![](images/part02_b4840c3bc05898076b5ecfd8382467f308afe9b0354e12a5aa7cce3cc0ed8f92.jpg)

如图 4-12(第 146 页)所示,PCI Express 拓扑由若干独立的、点对点的链路构成,每条链路将一个设备与一个或多个相邻设备相连。当报文到达某个链路接口的入站侧(称为入端口,Ingress Port)时,该端口先检查错误,然后做出以下三种决定之一:

1. 接受该报文并在内部使用

2. 将该报文转发到相应的出站(出口)端口

3. 拒绝该报文,因为它既不是预期的目标,也不是通往该目标的接口(注意,还存在其他拒绝报文的原因)


---

## 接收器检测三种类型的流量

假设链路已完全正常运行,每个设备(入口端口)的接收器接口必须检测并判断到达的三种链路流量:有序集 (Ordered Sets)、数据链路层报文 (DLLP) 和事务层报文 (TLP)。有序集和 DLLP 仅存在于本地链路上,因此永远不会路由到其他链路。TLP 则可以根据包头中包含的路由信息在各链路之间转发。

## 路由元素

具有多个端口的设备,例如根复合体 (Root Complex) 和交换机 (Switch),可以在各端口之间转发 TLP,有时也被称为路由代理 (Routing Agents) 或路由元素 (Routing Elements)。它们既会接收发往自身内部资源的 TLP,也会在入口端口与出口端口之间转发 TLP。

值得一提的是,交换机 (Switch) 必须支持对等 (peer-to-peer) 路由,而对于根复合体 (Root Complex) 来说,这一支持是可选的。对等 (peer-to-peer) 流量通常是指一个端点 (Endpoint) 发送目的地址为另一个端点 (Endpoint) 的报文。

端点 (Endpoint) 只有一条链路 (Link),除了目的地为其自身的流量之外,不会收到任何入口流量。它们仅简单地接受或拒绝传入的 TLP。

## TLP 路由的三种方法

---

## 概述

TLP 可以基于地址(存储器或 IO)进行路由,基于 ID(即 Bus、Device、Function 编号)进行路由,或者采用隐式路由。所使用的路由方法取决于 TLP 类型。第 147 页的表 4‐7 汇总了 TLP 类型及其各自使用的路由方法。

表 4‐7:PCI Express TLP 类型与路由方法

<table><tr><td>TLP 类型</td><td>所用路由方法</td></tr><tr><td>Memory Read [Lock]、Memory Write、AtomicOp</td><td>地址路由</td></tr><tr><td>IO Read 和 Write</td><td>地址路由</td></tr><tr><td>Configuration Read 和 Write</td><td>ID 路由</td></tr><tr><td>Message、Message With Data</td><td>地址路由、ID 路由或隐式路由</td></tr><tr><td>Completion、Completion With Data</td><td>ID 路由</td></tr></table>

Message 是唯一支持多于一种路由方法的 TLP 类型。PCI Express 规范中定义的大多数 Message TLP 都使用隐式路由,然而,厂商自定义的 Message 如果需要的话可以使用地址路由或 ID 路由。

## 隐式路由与消息报文的目的

在隐式路由中,既不使用地址路由信息,也不使用 ID 路由信息;报文根据其包头中的一个代码进行路由,该代码指明了拓扑中位置已知的目标(例如根复合体)。这种方式在适用某种隐式路由的情形下简化了消息报文的路由。

为什么需要消息报文?消息事务在 PCI 或 PCI-X 中并未定义,而是由 PCIe 引入。将消息报文作为一种报文类型引入,主要目的是为了实现 PCIe 的设计目标:大幅减少在 PCI 中实现的各种边带信号(例如中断引脚、错误引脚、电源管理信号等)。因此,大多数边带信号都被以消息报文形式出现的带内报文所取代。

隐式路由的作用 使用带内消息报文替代边带信号,需要在由大量点对点链路构成的拓扑中,提供一种将其路由到正确接收方的机制。隐式路由利用了这样一个事实:交换机 (Switch) 和其他路由元素都理解上游与下游的概念,并且根复合体 (Root Complex) 位于拓扑的顶端,而终端设备 (Endpoint) 位于底端。因此,消息报文可以使用一个简单的代码来表明它应当发往根复合体,或者向下游所有设备广播。这种能力消除了针对不同消息事务单独定义目标地址范围或 ID 列表的需要。

各种隐式路由类型可参见第 163 页"隐式路由"一节。

## 分离事务协议 (Split Transaction Protocol)

与大多数其他串行技术一样,PCI Express 使用分离事务协议 (Split Transaction Protocol),允许目标设备接收一个或多个请求,然后针对每个请求以单独的完成报文 (Completion) 进行响应。这是相对于 PCI 总线协议的一项重大改进——后者使用等待状态 (wait‐state) 或延迟事务 (delayed transaction, 即重试) 来处理访问目标设备的延迟。PCI Express 目标设备无需反复轮询以确认何时准备好进行长延迟传输,而是可以在任何就绪时刻主动发起响应。每个事务至少需要两个独立的 TLP——一个是请求 (Request),一个是完成报文 (Completion)(如后文所述,单个读请求可能会导致回送多个完成报文 TLP)。图 4‐13(第 149 页)展示了分离事务的 Request‐Completion 组成部分。本示例展示的是软件从端点 (Endpoint) 读取数据的过程。

Figure 4‐13: PCI Express Transaction Request And Completion TLPs  
![](images/part02_48a5a16bee00019f3f488013bb72a9c97e7ed8508405f635e2c1b6704b7bfa42.jpg)


---

## Posted 与 Non-Posted

为了缓解请求 (Request) - 完成报文 (Completion) 延迟带来的性能损失,内存写事务采用 Posted 方式,即从 Requester 的角度来看,该事务在请求离开 Requester 时即被视为已经完成。如果有助于理解,可以将 "posting"(投递)一词与邮政系统类比:投递一封内存写请求类似于将信件投入邮筒。一旦将信件投入邮筒,你就只能信任系统会去投递它,而不会等待投递确认。这种方式可能比等待整个 Request-Completion 来回要快得多,但——正如所有投递方案一样——关于事务何时(以及是否)在最终接收端成功完成,仍然存在不确定性。

在 PCIe 中,虽然将所有内存写设为 Posted 会带来少量不确定性,但考虑到由此换得的性能收益,这种做法被认为是可接受的。相比之下,对 IO 和配置空间的写入几乎总是会影响设备行为,并且具有较强的时间敏感性。因此,了解这些写请求何时(以及是否)完成是很重要的。正因为如此,IO 写和配置写始终是 Non-Posted 的,并且总会返回一个完成报文以报告操作状态。

综上,Non-Posted 事务需要返回完成报文,而 Posted 事务不需要、并且不应接收到完成报文。第 150 页的表 4-8 列出了 PCIe 中哪些事务是 Posted 的,哪些是 Non-Posted 的。

表 4-8:Posted 与 Non-Posted 事务

<table><tr><td>Request</td><td>How Request Is Handled</td></tr><tr><td>Memory Write</td><td>All memory write requests are posted. No completions are expected or sent.</td></tr><tr><td>Memory Read Memory Read Lock</td><td>All memory read requests are non-posted. A completion with data (made of one or more TLPs) will be returned by the Completer to deliver both the requested data and the status of the memory read. In the event of an error, a completion without data will be returned reporting the status.</td></tr><tr><td>AtomicOp</td><td>All AtomicOp requests are non-posted. A completion with data will be returned by the Completer containing the original value of the target location.</td></tr></table>

## 第 4 章:地址空间与事务路由

表 4‐8:Posted 与 Non‐Posted 事务(续)

<table><tr><td>请求 (Request)</td><td>请求的处理方式</td></tr><tr><td>IO 读 IO 写</td><td>所有 IO 请求都是 Non‐Posted 的。写操作或失败的读操作将返回一个不带数据的完成报文,成功的读操作将返回一个带数据的完成报文。</td></tr><tr><td>Configuration 读 Configuration 写</td><td>所有 Configuration 请求都是 Non‐Posted 的。写操作和失败的读操作将返回一个不带数据的完成报文,而成功的读操作将返回一个带数据的完成报文。</td></tr><tr><td>消息 (Message)</td><td>所有消息都是 Posted 的。路由方式取决于消息类型,但它们都被视为 Posted 请求。</td></tr></table>

## Header 字段定义报文格式与类型

## 概述

如图 4-14 所示(第 152 页),每个 TLP 包含一个三或四个双字(12 或 16 字节)的包头。其中包括 Format 和 Type 字段,它们定义了包头其余部分的内容,并指示 TLP 在穿越拓扑时所使用的路由方法。

图 4-14:事务层包通用 3DW 和 4DW 包头  
![](images/part02_fec46d2d1fd69f8fd6b71b51ac36f4f1abfbb4b8e904d4b9e043ef0ce0204668.jpg)

---

## 第 4 章:地址空间与事务路由


---

## Header Format/Type Field Encodings

Table 4‐9 on page 153 below summarizes the encodings used in TLP header Format and Type fields.

Table 4‐9: TLP Header Format and Type Field Encodings

<table><tr><td>TLP</td><td>FMT[2:0]</td><td>TYPE [4:0]</td></tr><tr><td>Memory Read Request (MRd)</td><td>000 = 3DW, no data001 = 4DW, no data</td><td>0 0000</td></tr><tr><td>Memory Read Lock Request (MRdLk)</td><td>000 = 3DW, no data001 = 4DW, no data</td><td>0 0001</td></tr><tr><td>Memory Write Request (MWr)</td><td>010 = 3DW, w/data011 = 4DW, w/data</td><td>0 0000</td></tr><tr><td>IO Read Request (IORd)</td><td>000 = 3DW, no data</td><td>00010</td></tr><tr><td>IO Write Request (IOWr)</td><td>010 = 3DW, w/data</td><td>0 0010</td></tr><tr><td>Config Type 0 Read Request (CfgRd0)</td><td>000 = 3DW, no data</td><td>0 0100</td></tr><tr><td>Config Type 0 Write Request (CfgWr0)</td><td>010 = 3DW, w/data</td><td>0 0100</td></tr><tr><td>Config Type 1 Read Request (CfgRd1)</td><td>000 = 3DW, no data</td><td>0 0101</td></tr><tr><td>Config Type 1 Write Request (CfgWr1)</td><td>010 = 3DW, w/data</td><td>0 0101</td></tr><tr><td>Message Request (Msg)</td><td>001 = 4DW, no data</td><td>1 0RRR* (for RRR, see routing subfield in “Message Type Field Summary” on page 164)</td></tr><tr><td>Message Request w/Data (MsgD)</td><td>011 = 4DW, w/data</td><td>1 0RRR* (for RRR, see routing subfield in “Message Type Field Summary” on page 164)</td></tr><tr><td>Completion (Cpl)</td><td>000 = 3DW, no data</td><td>0 1010</td></tr><tr><td>Completion W/Data (CplD)</td><td>010 = 3DW, w/ data</td><td>0 1010</td></tr><tr><td>Completion-Locked (CplLk)</td><td>000 = 3DW, no data</td><td>0 1011</td></tr><tr><td>Completion w/Data (CplDLk)</td><td>010 = 3DW, w/ data</td><td>0 1011</td></tr><tr><td>Fetch and Add AtomicOp Request (FetchAdd)</td><td>010 = 3DW, w/data011 = 4DW, w/data</td><td>0 1100</td></tr><tr><td>Unconditional Swap AtomicOp Request (Swap)</td><td>010 = 3DW, w/data011 = 4DW, w/data</td><td>0 1101</td></tr><tr><td>Compare and Swap AtomicOp Request (CAS)</td><td>010 = 3DW, w/data011 = 4DW, w/data</td><td>0 1110</td></tr><tr><td>Local TLP Prefix (LPrfx)</td><td>100 = 1DW</td><td>0 LLLL</td></tr><tr><td>End-to-End TLP Prefix (EPrfx)</td><td>100 = 1DW</td><td>1 EEEE</td></tr></table>

## TLP 包头概述

当 TLP 在入口端口被接收时,会首先在物理层和数据链路层进行错误检查。若没有错误,则在事务层检查该 TLP,以确定应使用哪种路由方式。基本步骤如下:

1. Format 字段和 Type 字段确定包头的大小、格式以及 TLP 的类型。

2. 设备根据与该 TLP 类型相关联的路由方式,判断自身是否为预期接收方。如果是,则接受(消费)该 TLP;如果不是,则将其转发到相应的出口端口——但需遵守该出口端口的排序规则和流控规则。

3. 如果该设备既不是预期接收方,也不在通往预期接收方的路径上,则通常会将其作为不支持的请求(Unsupported Request, UR)拒绝。


---

## 应用路由机制

一旦系统地址被配置好且事务被使能,设备会检查收到的 TLP,并使用相应的配置字段对报文进行路由。后续章节将描述在 PCI Express 交换结构中路由 TLP 时所使用的各种路由机制的基本特性与功能。

---

## ID 路由 (ID Routing)

ID 路由用于在拓扑中定位 Function 的逻辑位置 —— 即 Bus Number、Device Number、Function Number(通常称为 BDF)。它与 PCI 和 PCI‐X 协议中用于配置事务的路由方式兼容。在 PCIe 中,它仍然用于路由配置报文,同时也被用于路由完成报文和部分消息报文。


---

## 总线号、设备号、功能号限制

PCI Express 支持与 PCI 和 PCI‐X 相同的拓扑限制:

1. 总线号使用 8 位,因此一个系统中最多可以有 256 条总线。这包括由交换机 (Switch) 创建的内部总线。

2. 设备号使用 5 位,因此每条总线上最多可以有 32 个设备。较旧的 PCI 总线或交换机 (Switch) 或根复合体 (Root Complex) 中的内部总线可以承载多个下游设备。然而,外部 PCIe 链路 (Link) 始终是点对点的,链路上只有一个下游设备。外部链路的设备号由下游端口 (Downstream Port) 强制规定为始终为设备 0,因此每个外部端点 (Endpoint) 将始终是设备 0(除非使用 ARI (替代路由 ID 解释),在这种情况下,没有设备号;关于 ARI 的更多内容,请参见第 909 页 "IDO (基于 ID 的排序)" 一节)。

3. 功能号使用 3 位,因此每个设备最多可以有 8 个内部功能。

---

## ID 路由中的关键 TLP 包头字段

如果接收到的 TLP 中 Type 字段指示使用 ID 路由,则包头中的 ID 字段(Bus、Device、Function)将用于执行路由检查。这里有两种情况:使用 3DW 包头的 ID 路由和使用 4DW 包头的 ID 路由(仅在消息中可能出现)。第 156 页的图 4‐15 给出了采用 ID 路由与 3DW 包头的 TLP 示例,第 156 页的图 4‐16 则给出了 ID 路由对应的 4DW 包头示例。

图 4‐15:3DW TLP 包头 — ID 路由字段
![](images/part02_a3eae75f4c57834d4b43ecc60db67b8feedf07b5daeead859131dec27b5446e6.jpg)

图 4‐16:4DW TLP 包头 — ID 路由字段
![](images/part02_c5e73cb93b4421601309081f14e7dd41039673423275cf68bf670983767ecc47.jpg)


---

## 端点:一次检查

对于 ID 路由,端点只需将包头中的 ID 字段与自身的 BDF 进行比对即可。每个功能在其链路上每次看到 Type 0 配置写时,都会"捕获"来自 TLP 包头第 8-9 字节的总线号和设备号。规范并未规定应将所捕获的总线号和设备号信息存储在哪里,只要求功能必须将其保存。所保存的总线号和

## 第 4 章:地址空间与事务路由

设备号 (Device Number) 作为该端点 (Endpoint) 发起的 TLP 请求中的请求者 ID (Requester ID),以便该请求的完成者 (Completer) 能够在完成报文 (Completion) 中包含请求者 ID 字段的值。完成报文中的请求者 ID 用于路由该完成报文。

## 交换机(桥):每个端口进行两次检查

对于采用 ID 路由的 TLP,交换机端口首先通过将 TLP 包头 (Header) 中的目标 ID 与自身的 BDF 进行比较,以判断自身是否就是预期的目标接收方,如第 158 页图 4-17 中的 (1) 所示。与端点 (Endpoint) 一样,每当在上游端口 (Upstream Port) 上检测到一次配置写 (Type 0) 时,每个交换机端口都会捕获自身的总线号和设备号。如果 TLP 中的目标 ID 字段与该交换机端口的 ID 相符,则该端口消费该报文。如果 ID 字段不匹配,则接着检查该 TLP 是否是定向到本交换机端口下方的设备。它通过检查 Secondary 与 Subordinate Bus Number 寄存器,判断 TLP 中的目标总线号是否落在该范围(含端点)内。如果是,则该 TLP 应被向下游转发。该检查在第 158 页图 4-17 中以 (2) 表示。如果该报文是向下游流动的(即到达上游端口),并且既不匹配上游端口的 BDF,也不落在 Secondary-Subordinate 总线号范围内,则将在上游端口上作为不支持的请求 (Unsupported Request) 处理。

如果上游端口判定其接收到的 TLP 是定向到它下方某个设备的(因为目标总线号落在其 Secondary-Subordinate 总线号范围内),则它将该 TLP 向下游转发,交换机的所有下游端口都会执行同样的检查。每个下游端口都检查 TLP 是否以自身为目标。如果是,则被寻址的端口消费该 TLP,其余端口忽略该报文。如果不是,则所有下游端口均检查 TLP 是否定向到它们各自端口下方的设备。在该检查中返回 true 的那个端口会将 TLP 转发到它的 Secondary Bus,而其余下游端口则忽略该 TLP。

在本节中,重要的是要记住交换机上的每个端口都是一个桥 (Bridge),因此具有自己的配置空间,配置空间带有 Type 1 包头。尽管第 158 页的图 4-17 只显示了一个 Type 1 包头,但实际上,每个端口(即每个 P2P 桥)都有自己的 Type 1 包头,并在该端口看到 TLP 时执行同样的两次检查。

Figure 4-17: Switch Checks Routing Of An Inbound TLP Using ID Routing  
![](images/part02_fc6f79f8ca30a0eaee36c18c935ef53ffbdba2126190699e50eddded332a2037.jpg)


---

## 地址路由

采用地址路由的 TLP 所引用的存储空间(系统内存和内存映射 IO)以及 IO 地址映射,与 PCI 和 PCI‐X 事务使用的地址映射相同。目标地址低于 4GB(即 32 位地址)的内存请求必须使用 3DW 包头;目标地址高于 4GB(即 64 位地址)的内存请求必须使用 4DW 包头。IO 请求被限制为 32 位地址,仅用于支持旧有功能。

---

## 地址路由中关键的 TLP 包头字段

当 Type 字段指示某条 TLP 使用地址路由时,包头中的地址字段用于执行路由检查。这些地址可以是 32 位地址,也可以是 64 位地址。

**32 位地址的 TLP** 对于 IO 或 32 位内存请求,使用 3DW 包头,如图 4‐18 所示。因此,由这些 TLP 寻址的内存映射寄存器将位于 4GB 内存或 IO 地址边界以下。

**64 位地址的 TLP** 对于 64 位内存请求,使用 4DW 包头,如图 4‐19(第 160 页)所示。由这些 TLP 寻址的内存映射寄存器能够位于 4GB 内存边界以上。

图 4‐18:3DW TLP 包头 ‐ 地址路由字段
![](images/part02_35aa75f79ed03d1081d34cf95b053c7f1e1f7022db9fd9fe908c90f87e7ad67a.jpg)

图 4‐19:4DW TLP 包头 ‐ 地址路由字段
![](images/part02_5c852f5678febf67f3fc428e4d27a5319701cb83d0df73f869d7b9b4793005e2.jpg)

## Endpoint Address Checking

如果 Endpoint 接收到一个采用地址路由的 TLP,则会将包头中的地址与其 Configuration (配置) 头中每个已实现的 Base Address Register (BAR) 进行比较检查,如图 4-20 所示。由于 Endpoint 仅有一个链路接口,因此它要么接受该报文,要么拒绝该报文。当 TLP 中的目标地址与其某个 BAR 所编程的地址范围匹配时,Endpoint 将接受该报文。关于 BAR 使用方式的更多信息,可参见第 126 页的 "Base Address Registers (BARs)" 一节。

## Chapter 4: Address Space & Transaction Routing

Figure 4‐20: 端点检查传入的 TLP 地址
![端点检查传入的 TLP 地址](images/part02_1f97be03524b192e0c9fa2c30aba8a145e6843a83eb62f3695ca2b2ab50f5644.jpg)


---

## Switch 路由

如果传入的 TLP 使用地址路由,Switch 端口首先通过将包头中的地址与其 Type 1 配置头中的两个 BAR 进行比较,以查看该地址是否在该端口本地范围内,如图 4-21 第 162 页的步骤 1 所示。如果与其中一个 BAR 匹配,则该 Switch 端口就是 TLP 的目标,并消费该报文。如果不匹配,则该端口随后检查其 Base/Limit 寄存器对,以查看 TLP 是否以该桥下游的某个功能为目标。如果请求(Request)以 IO 空间为目标,它将检查 IO Base 和 Limit 寄存器,如步骤 2a 所示。但是,如果请求以存储器空间为目标,则它将检查 Nonprefetchable Memory Base/Limit 寄存器和 Prefetchable Memory Base/Limit 寄存器,如第 162 页图 4-21 中的步骤 2b 所示。有关如何评估 Base/Limit 寄存器对的更多信息,请参阅第 136 页的 "Base and Limit Registers" 一节。

Figure 4‐21: Switch Checks Routing Of An Inbound TLP Using Address  
![](images/part02_47521d33eb88e6a8aa297bb7e9520c2500d1748e9639be55d27495f09b5b3353.jpg)

要理解 Switch 中基于地址的 TLP 的路由,最好记住每个 Switch 端口都是其自己的桥。下面是该桥(Switch 端口)在收到基于地址的 TLP 时所采取的步骤:


---

## 下行传输的 TLP(在主接口上接收)

1. 如果 TLP 中的目标地址与某个 BAR 匹配,则该桥(交换机端口)将消费此 TLP,因为它就是该 TLP 的目标。

2. 如果 TLP 中的目标地址落在其某一组 Base/Limit 寄存器的地址范围内,则该报文将被转发到 secondary 接口(下行)。

3. 否则(ELSE),该 TLP 将在主接口上作为不支持的请求 (Unsupported Request) 处理。(如果主接口上没有其他桥声明接收该 TLP,则同样适用此规则。)


---

## 上行传输的 TLP(在次级接口上接收)

1. 如果 TLP 中的目标地址与某个 BAR 匹配,则该桥(交换机端口)将消费此 TLP,因为它是该 TLP 的目标。

2. 如果 TLP 中的目标地址落在其某个 Base/Limit 寄存器组的地址范围内,则此 TLP 将在次级接口上作为不支持的请求 (Unsupported Request) 处理。(除非此端口是交换机的上游端口;在这种情况下,该报文可能是一笔对等 (peer‐to‐peer) 事务,并将被转发到与接收端口不同的某个下游端口上的下游方向。)

3. 否则,只要 TLP 的目标地址不属于本桥,也不属于本桥下挂的任何一个功能,该 TLP 将被转发到主接口(上游方向)。


---

## 组播功能

PCI Express 规范的 2.1 版本新增了对指定一段地址范围以提供组播功能的支持。任何接收到的、落在指定为组播地址范围内的报文,都会按照组播规则进行路由/接收。该地址范围可能未在某个功能的 BAR 中预留,也可能不在桥的 Base/Limit 寄存器对范围内,但仍需要被正确地接收/转发。有关组播功能的更多信息,可参阅第 889 页“组播功能寄存器(Multicast Capability Registers)”一节。

---

## Implicit Routing (隐式路由)

Implicit routing, used in some message packets, is based on the awareness of routing elements that the topology has upstream and downstream directions and a single Root Complex at the top. This allows some simple routing methods without the need to assign a target address or ID. Since the Root Complex generally integrates power management, interrupt, and error handling logic, it is either the source or recipient of most PCI Express messages.


---

## Only for Messages

部分报文使用地址或 ID 路由而非隐式路由,对于这些报文,路由机制的应用方式与前述章节中描述的相同。然而,大多数报文采用隐式路由。隐式路由的目的在于模拟边带信号(side-band signal)的行为,因为 PCIe 的一个设计目标是尽可能消除 PCI 中原有的众多边带信号。PCI 中的这些边带信号通常用于:主机通知所有设备某事件的发生,或设备通知主机某事件的发生。在 PCIe 中,我们使用 Message TLP 来传递这些事件。PCIe 已为以下类型的事件定义了报文:

- 电源管理 (Power Management)

- INTx 传统中断信号

- 错误信号 (Error)

- 锁定事务 (Locked Transaction) 支持

- 热插拔 (Hot-Plug) 信号

- 厂商自定义信号

- 插槽电源限制 (Slot Power Limit) 设置

---

## 隐式路由中的关键 TLP 包头字段

对于隐式路由,包头中的路由子字段用于确定报文的目的地。164 页的图 4-22 展示了使用隐式路由的报文 TLP。

图 4-22:4DW 报文 TLP 包头 - 隐式路由字段
![](images/part02_180e1d6d4c7b49cebf8eda3097555e2eb146e70d55ac049bbc4ae3669523c4b5.jpg)


---

## Message Type 字段汇总

第 165 页的表 4‐10 展示了 Message 的 TLP Header Type 字段如何被解读。如表所示,高两位表明该报文为 Message,而低三位指定所采用的路由方法。需要注意的是,无论选择何种路由选项,Message TLP 始终使用 4DW Header。

对于地址路由,字节 8~15 包含最多 64 位的地址;对于 ID 路由,字节 8 和字节 9 包含目标的 BDF。

表 4‐10:Message Request Header Type 字段使用说明

<table><tr><td>Type 字段位</td><td>说明</td></tr><tr><td>Bit 4:3</td><td>定义事务类型:$10b = \text{Message TLP}$ </td></tr><tr><td>Bit 2:0</td><td>Message Routing 子字段 R[2:0] $\bullet$  000b = Implicit — 路由至 Root Complex $\bullet$  001b = Route by Address(Header 字节 8‐15 包含地址) $\bullet$  010b = Route by ID(Header 字节 8‐9 包含 ID) $\bullet$  011b = Implicit — 向下游广播 $\bullet$  100b = Implicit — 本地:在接收端终结 $\bullet$  101b = Implicit — Gather 并路由至 Root Complex $\bullet$  110b - 111b = 保留:在接收端终结</td></tr></table>


---

## 端点处理

对于隐式路由,端点 (Endpoint) 只需检查其路由子字段是否与自身相匹配。例如,端点会接受广播报文 (Broadcast Message) 或在接收方终止的报文;但不会接受隐式指向根复合体 (Root Complex) 的报文。

---

## Switch 的处理

像交换机（Switch）这样的路由元素会考虑 TLP 所到达的端口以及路由子字段编码是否与之匹配。例如：

1. 交换机的上游端口（Upstream Port）可以合法地接收一条广播消息（Broadcast Message）。它会复制该消息并将其转发到其所有下游端口（Downstream Port）。如果一条隐式路由的广播消息在交换机的下游端口上被接收（意味着该消息原本是向上游传输的），则属于错误，应作为畸形 TLP（Malformed TLP）处理。

2. 交换机可以在其下游端口上接收隐式路由到根复合体（Root Complex）的消息，并将其转发到上游端口，因为根复合体的位置被理解为在上游方向。它不会接受在其上游端口接收的（意味着该消息原本是向下游传输的）隐式路由到根复合体的消息。

---

## PCI Express Technology

3. 如果某个隐式路由的 Message 报文指示应在接收端终止,则接收端的交换机端口会消费该报文,而不是将其转发。

4. 对于使用地址或 ID 路由的报文,Switch 只需执行常规的地址或 ID 检查,据此决定是接受还是转发该报文。

---

## DLLP 和有序集不被路由

DLLP 和有序集流量不会从交换机或根复合体的入口端口路由到出口端口。这些数据包通过链路在端口之间逐段传输,从物理层传送到物理层。

DLLP 在 PCI Express 端口的数据链路层产生,经过物理层,离开端口,穿越链路,到达相邻端口。在该端口,数据包经过物理层后到达数据链路层,在该层被处理和消耗。DLLP 不会继续向上传递到端口的事务层,因此不会被路由。

类似地,有序集数据包在物理层产生,离开端口,穿越链路,到达相邻端口。在该端口,数据包到达物理层,在该层被处理和消耗。有序集不会继续向上传递到端口的数据链路层和事务层,因此也不会被路由。

正如本章所述,只有 TLP 才会通过交换机和根复合体进行路由。它们在源端口的事务层产生,并最终到达目的端口的事务层。

第二部分:

事务层

---

## 5 TLP 组成元素


---

## 上一章

上一章介绍了功能( Function )通过基地址寄存器( Base Address Registers, BAR )请求地址空间( 内存地址空间或 IO 地址空间 )的目的与方法,以及软件应如何设置所有桥的 Base/Limit 寄存器,以便将 TLP 从源端口路由到正确的目标端口。本章还讨论了 PCI Express 中 TLP 路由的一般概念,包括基于地址的路由、基于 ID 的路由和隐式路由。

## 本章概述

PCI Express 设备之间以数据包的形式传输信息。数据包主要分为三大类:事务层数据包 (Transaction Layer Packets, TLPs)、数据链路层数据包 (Data Link Layer Packets, DLLPs) 以及有序集合 (Ordered Sets)。本章将介绍各类 TLP 的用途、格式与定义,并详细说明其相关字段。DLLP 将在第 9 章"ʺDLLP Elementsʺ"(第 307 页)中单独介绍。

---

## 下一章

下一章将讨论流控 (Flow Control) 协议的目的与详细操作机制。流控 (Flow Control) 旨在确保发送器永远不会发出接收器 (Receiver) 无法接受的 TLP。这可以避免接收缓冲区溢出,并消除 PCI 风格中诸如断开连接、重传 (Retry) 以及等待周期等低效机制。

## 基于包协议简介


---

## 概述

与并行总线不同,像 PCIe 这样的串行传输总线不使用控制信号来标识在某一时刻链路上发生了什么。取而代之的是,它们所发送的比特流必须具有预期的长度和可识别的格式,以便接收器能够理解其内容。此外,PCIe 在数据包传输过程中不使用任何即时的握手交互。

除了逻辑空闲 (Logical Idle) 符号和被称为有序集合 (Ordered Sets) 的物理层数据包外,信息在一条活跃的 PCIe 链路上以称为数据包 (Packets) 的基本块来传递,这些数据包由符号 (Symbols) 构成。所交换的两大类数据包分别是高层的事务层数据包 (TLP, Transaction Layer Packets) 和低层的链路维护数据包,即数据链路层数据包 (DLLP, Data Link Layer Packets)。这些数据包及其流向在第 170 页的图 5-1 中给出。有序集合也是数据包,但与 TLP 和 DLLP 不同,它们并不使用起始和结束符号进行定界。它们也不像 TLP 和 DLLP 那样按字节拆分到多通道 (Lanes) 上。有序集合数据包会在链路 (Link) 的所有通道上复制发送。

图 5-1:TLP 与 DLLP 数据包  
![](images/part02_c95d2324c799f59c2437e1a433388a586089185e3661fa7dacda8c2af34d8ef6.jpg)


---

## Motivation for a Packet-Based Protocol

There are three distinct advantages to using a packet‐based protocol especially when it comes to data integrity:


---

## 1. 数据包格式定义清晰

早期的总线(如 PCI)允许大小不定的传输,导致在传输结束之前无法识别有效负载的边界。此外,任意一方设备都可以在传输完成之前终止传输,这使得发送方难以计算并发送覆盖整个有效负载的校验和或 CRC。PCI 转而采用了一种简单的奇偶校验方案,并在每个数据阶段都进行校验。

相比之下,PCIe 数据包具有明确的尺寸和格式。位于起始位置的包头指明了数据包类型,并包含必需和可选字段。除地址字段可为 32 位或 64 位外,其余包头字段的大小都是固定的。一旦传输启动,接收方不能暂停或提前终止。这种结构化的格式便于在 TLP 中加入有助于可靠传输的信息,包括成帧符号、CRC 以及数据包序列号 (Sequence Number)。


---

## 2. 帧定界符号界定报文边界

在 Gen1 和 Gen2 工作模式使用 8b/10b 编码时,每个 TLP 和 DLLP 报文的发送都由 Start (起始) 和 End (结束) 控制符号进行定界,清晰地为接收器界定报文边界。这相对于 PCI 和 PCI-X 是一个巨大的改进——在后两者中,单一的 FRAME# 信号的置位与撤销用于指示一次事务的开始与结束。该信号(或任何其他控制信号)上的毛刺都可能导致目标设备误解总线事件。PCIe 接收器必须在判定链路 (Link) 活动开始或结束之前正确解码一个完整的 10 位符号,因此对于未预期或未识别的符号,可以更便捷地将其识别并作为错误处理。

对于 Gen3 中使用的 128b/130b 编码,不再使用控制字符,也就没有所谓的帧定界符号。有关 Gen3 编码与早期版本之间差异的更多内容,请参阅第 407 页的第 12 章"物理层 — 逻辑 (Gen3)"。

## 3. CRC 校验整个报文

与 PCI 在事务的地址阶段和数据阶段使用边带奇偶校验信号不同,PCIe 的带内 CRC 值用于校验整个报文的无错传输。TLP 报文还会由发送器的数据链路层追加一个序列号,以便当接收器检测到错误时,问题报文可以被自动重发。发送器在重传缓冲区(Retry Buffer)中保存每一份已发送 TLP 的副本,直到收到接收器的确认。这种 TLP 确认机制称为 Ack/Nak 协议(详见第 10 章" Ack/Nak 协议",第 317 页),它构成了链路级 TLP 错误检测与纠正的基础。Ack/Nak 协议错误恢复机制允许在发生问题的链路位置及时解决问题,但需要本地硬件方案予以支持。

## 事务层包 (TLP) 详细信息

在 PCI Express 中，高层事务由发送设备的设备核发起，并在接收设备的核中终止。事务层 (Transaction Layer) 对这些请求进行操作，在发送器 (Transmitter) 一侧组装外发的 TLP，并在接收器 (Receiver) 一侧对它们进行解析。在此过程中，每个设备的数据链路层 (Data Link Layer) 和物理层 (Physical Layer) 也参与最终的包组装过程。

---

## TLP 装配与拆解

TLP 在链路 (Link) 发送侧的装配以及在接收侧的拆解,其总体流程如图 5‐2 (第 173 页) 所示。下面我们将从报文创建开始,逐步走过各个阶段,直到报文被送达接收方的核心逻辑。事务层包 (TLP) 装配与拆解的关键阶段如下所列。列表中的编号与图 5‐2 (第 173 页) 中的编号相对应。

## 发送器(Transmitter):

1. 设备 A 的核心逻辑向其 PCIe 接口发送一个请求。具体的实现方式不在规范或本书的讨论范围内。该请求包括:

— 目标地址或 ID(路由信息)

— 源信息,例如请求者 ID (Requester ID) 和 Tag 字段(标签)

— 事务类型/报文类型(要执行的命令,例如内存读)

— 数据有效负载大小(如果有)以及数据有效负载(如果有)

— 流量类 (TC, Traffic Class,用于分配报文优先级)

— 请求的属性(No Snoop、Relaxed Ordering 等)

2. 基于该请求,事务层构建 TLP 包头,追加任何数据有效负载,并在支持且已启用的情况下,可选择性地计算并追加摘要(端到端 CRC, ECRC)。此时,TLP 被放入一个虚通道 (VC, Virtual Channel) 缓冲区中。虚通道根据事务排序 (Transaction Ordering) 规则管理 TLP 的顺序,并在 TLP 传递到数据链路层之前,验证接收方是否具有足够的流控 (Flow Control) 信用来接受该 TLP。

3. 当 TLP 到达数据链路层时,它被分配一个序列号 (Sequence Number),然后根据 TLP 的内容和该序列号计算链路 CRC。生成报文的副本被保存在重传缓冲区 (Retry Buffer) 中,以防传输过程中出现错误,同时该报文也会被传递到物理层。

Figure 5‐2: PCIe TLP 装配/拆解  
![](images/part02_9975e4bc5a3afd16b56b819f3cae3190ba51c80a39c9d42a9bc457fc722ea5f4.jpg)

4. 物理层执行多项操作以准备报文进行串行传输,包括字节拆分 (byte striping)、加扰 (scrambling)、编码 (encoding) 以及比特的串行化。对于 Gen1 和 Gen2 设备,在使用 8b/10b 编码时,控制字符 STP 和 END 被添加到报文的两端。最后,报文通过链路 (Link) 进行传输。在 Gen3 模式下,STP 令牌被添加到 TLP 的前端,但报文末端不添加 END。而 STP 令牌包含有关 TLP 报文大小的信息。

## 接收器(Receiver):

5. 在接收器(本例中的设备 B)端,所有为传输该报文所做的准备工作现在都必须被撤销。物理层将比特流解串行化,解码得到的符号,并对字节进行解除分条(stripe)处理。

   控制字符在此处被移除,因为它们仅在物理层有意义,随后该报文被转发到数据链路层。

6. 数据链路层计算 CRC 并将其与收到的 CRC 进行比较。如果匹配,则检查序列号。如果没有错误,则移除 CRC 和序列号,TLP 被传递给接收器的事务层,并通过返回一个 Ack DLLP 通知发送方已正确接收。如果出现错误,则返回 Nak,发送方将重传(Replay)其重传缓冲区(Retry Buffer)中的 TLP。

7. 在事务层,TLP 被解码,信息被传递给核逻辑以执行相应操作。如果接收设备是该报文的最终目标,则它会检查 ECRC 错误,并在存在相关 ECRC 错误条件时向核逻辑上报。

---

## TLP 结构 (TLP Structure)

事务层包 (Transaction Layer Packet) 中每个字段的基本用法在第 174 页的表 5-1 中定义。

表 5-1:TLP 包头 Type 字段定义事务变体 (TLP Header Type Field Defines Transaction Variant)

<table><tr><td>TLP 组成部分 (TLP Component)</td><td>协议层 (Protocol Layer)</td><td>组成部分用途 (Component Use)</td></tr><tr><td>Header (包头)</td><td>事务层 (Transaction Layer)</td><td>大小为 3 或 4 DW(12 或 16 字节)。格式随类型而异,但 Header 定义了以下参数,包括:事务类型目标地址、ID 等传输大小(若有)、字节使能属性 (Attributes)流量类 (Traffic Class)</td></tr><tr><td>Data (数据)</td><td>事务层 (Transaction Layer)</td><td>可选的 1-1024 DW 有效载荷,由字节使能或按字节对齐的起始与结束地址加以限定。注意不能指定长度为 0,但零长度读操作(在某些场合下有用)可通过指定长度为 1 DW、字节使能全为 0 来近似实现。完成方 (Completer) 返回的数据是未定义的,但请求方 (Requester) 并不使用该数据,因此效果相同。</td></tr><tr><td>Digest/ECRC (摘要/端到端 CRC)</td><td>事务层 (Transaction Layer)</td><td>可选。出现时,ECRC 大小始终为 1 DW。</td></tr></table>

---

## 通用 TLP 包头格式


---

## 概述

第 175 页的图 5‐3 展示了通用 TLP 4DW 包头 (Header) 的格式与内容。本节将概述几乎所有事务类型共有的字段。与特定事务类型相关的包头格式差异将在后续章节中介绍。

图 5‐3:通用 TLP 包头字段  
![](images/part02_86de3a251a1f2d00f0f15727ca8579b021fdfe1bcfc1111e0c0d75e2bd01a7df.jpg)

---

## Generic Header Field Summary

Table 5‐2 on page 176 summarizes the size and use of each of the generic TLP header fields. Note that fields marked “R” in Figure 5‐3 on page 175 are reserved and should be set to zero.

Table 5‐2: Generic Header Field Summary

<table><tr><td>Header Field</td><td>Header Location</td><td>Field Use</td></tr><tr><td>Fmt[2:0] (Format)</td><td>Byte 0 Bit 7:5</td><td>These bits encode information about header size and whether a data payload will be part of the TLP:00b 3DW header, no data01b 4DW header, no data10b 3DW header, with data11b 4DW header, with dataAn address below 4GB must use a 3DW header. The spec states that receiver behavior is undefined if 4DW header is used for an address below 4GB with the upper 32 bits of the 64-bit address set to zero.</td></tr><tr><td>Type[4:0]</td><td>Byte 0 Bit 4:0</td><td>These bits encode the transaction variant used with this TLP. The Type field is used with Fmt [1:0] field to specify transaction type, header size, and whether data payload is present. See “Generic Header Field Details” on page 178 for details.</td></tr><tr><td>TC [2:0] (Traffic Class)</td><td>Byte 1 Bit 6:4</td><td>These bits encode the traffic class to be applied to this TLP and to the completion associated with it (if any):000b = Traffic Class 0 (Default).111b = Traffic Class 7TC 0 is the default class, while TC 1-7 are used to provide differentiated services. See “Traffic Class (TC)” on page 247 for additional information.</td></tr><tr><td>Attr [2] (Attributes)</td><td>Byte 1 Bit 2</td><td>This third Attribute bit indicates whether ID-based Ordering is to be used for this TLP. To learn more, see “ID Based Ordering (IDO)” on page 301.</td></tr><tr><td>TH (TLP Processing Hints)</td><td>Byte 1 Bit 0</td><td>Indicates when TLP Hints have been included to give the system some idea about how best to handle this TLP. See “TPH (TLP Processing Hints)” on page 899 for a discussion on their usage.</td></tr><tr><td>TD (TLP Digest)</td><td>Byte 2 Bit 7</td><td>If TD = 1, the optional 4-byte TLP Digest has been included with this TLP as the ECRC value. Some rules:Presence of the Digest field must be checked by all receivers based on this bit.A TLP with TD = 1 but no Digest is handled as a Malformed TLP.If a device supports checking ECRC and TD=1, it must perform the ECRC check.If a device does not support checking ECRC (optional) at the ultimate destination, it must ignore the digest.For more on this topic see “CRC” on page 653 and “ECRC Generation and Checking” on page 657.</td></tr><tr><td>EP (Poisoned Data)</td><td>Byte 2 Bit 6</td><td>If EP = 1, the data accompanying this data should be considered invalid although the transaction is being allowed to complete normally. For more on poisoned packets, refer to “Data Poisoning” on page 660.</td></tr><tr><td>Attr [1:0] (Attributes)</td><td>Byte 2 Bit 5:4</td><td>Bit 5 = Relaxed ordering: When set to 1, PCI-X relaxed ordering is enabled for this TLP. If 0, then strict PCI ordering is used.Bit 4 = No Snoop: When set to 1, Requester is indicating that no host cache coherency issues exist for this TLP. System hardware can thus save time by skipping the normal processor cache snoop for this request. When 0, PCI -type cache snoop protection is required.</td></tr><tr><td>Address Type [1:0]</td><td>Byte 2 Bit 3:2</td><td>For Memory and Atomic Requests, this field supports address translation for virtualized systems. The translation protocol is described in a separate spec called Address Translation Services, where it can be seen that the field encodes as:00 = Default/Untranslated01 = Translation Request10 = Translated11 = Reserved</td></tr><tr><td>Length [9:0]</td><td>Byte 2 Bit 1:0Byte 3 Bit 7:0</td><td>TLP data payload transfer size, in DW. Encoding:00 0000 0001b = 1DW00 0000 0010b = 2DW..11 1111 1111b = 1023 DW00 0000 0000b = 1024 DW</td></tr><tr><td>Last DW Byte Enables [3:0]</td><td>Byte 7 Bit 7:4</td><td>These four high-true bits map one-to-one to the bytes within the last double word of payload.Bit 7 = 1: Byte 3 in last DW is valid; otherwise notBit 6 = 1: Byte 2 in last DW is valid; otherwise notBit 5 = 1: Byte 1 in last DW is valid; otherwise notBit 4 = 1: Byte 0 in last DW is valid; otherwise not</td></tr><tr><td>First DW Byte Enables [3:0]</td><td>Byte 7 Bit 3:0</td><td>These four high-true bits map one-to-one to the bytes within the first double word of payload.Bit 3 = 1: Byte 3 in first DW is valid; otherwise notBit 2 = 1: Byte 2 in first DW is valid; otherwise notBit 1 = 1: Byte 1 in first DW is valid; otherwise notBit 0 = 1: Byte 0 in first DW is valid; otherwise not</td></tr></table>

## 通用包头字段详解

在以下各节中,我们将详细描述 TLP 包头中各字段的细节,这些字段在第 175 页的图 5-3 中已给出。


---

## Header Type/Format Field Encodings

Table 5‐3 on page 179 summarizes the encodings used in TLP header Type and Format (Fmt) fields.

Table 5‐3: TLP Header Type and Format Field Encodings

<table><tr><td>TLP</td><td>FMT[2:0]</td><td>TYPE [4:0]</td></tr><tr><td>Memory Read Request (MRd)</td><td>000 = 3DW, no data001 = 4DW, no data</td><td>0 0000</td></tr><tr><td>Memory Read Lock Request (MRdLk)</td><td>000 = 3DW, no data001 = 4DW, no data</td><td>0 0001</td></tr><tr><td>Memory Write Request (MWr)</td><td>010 = 3DW, w/ data011 = 4DW, w/ data</td><td>0 0000</td></tr><tr><td>IO Read Request (IORd)</td><td>000 = 3DW, no data</td><td>0 0010</td></tr><tr><td>IO Write Request (IOWr)</td><td>010 = 3DW, w/ data</td><td>0 0010</td></tr><tr><td>Config Type 0 Read Request (CfgRd0)</td><td>000 = 3DW, no data</td><td>0 0100</td></tr><tr><td>Config Type 0 Write Request (CfgWr0)</td><td>010 = 3DW, w/ data</td><td>0 0100</td></tr><tr><td>Config Type 1 Read Request (CfgRd1)</td><td>000 = 3DW, no data</td><td>0 0101</td></tr><tr><td>Config Type 1 Write Request (CfgWr1)</td><td>010 = 3DW, w/ data</td><td>0 0101</td></tr><tr><td>Message Request (Msg)</td><td>001 = 4DW, no data</td><td>1 0 rrr*(see routing field)</td></tr><tr><td>Message Request W/Data (MsgD)</td><td>011 = 4DW, w/ data</td><td>1 0rrr*(see routing field)</td></tr><tr><td>Completion (Cpl)</td><td>000 = 3DW, no data</td><td>0 1010</td></tr><tr><td>Completion W/Data (CplD)</td><td>010 = 3DW, w/ data</td><td>0 1010</td></tr><tr><td>Completion-Locked (CplLk)</td><td>000 = 3DW, no data</td><td>0 1011</td></tr><tr><td>Completion W/Data (CplDLk)</td><td>010 = 3DW, w/ data</td><td>0 1011</td></tr><tr><td>Fetch and Add AtomicOp Request</td><td>010 = 3DW, w/ data011 = 4DW, w/ data</td><td>0 1100</td></tr><tr><td>Unconditional Swap AtomicOp Request</td><td>010 = 3DW, w/ data011 = 4DW, w/ data</td><td>0 1101</td></tr><tr><td>Compare and Swap AtomicOp Request</td><td>010 = 3DW, w/ data011 = 4DW, w/ data</td><td>0 1110</td></tr><tr><td>Local TLP Prefix</td><td>100 = TLP Prefix</td><td> $0L_3L_2L_1L_0$ </td></tr><tr><td>End-to-End TLP Prefix</td><td>100 = TLP Prefix</td><td> $1E_3E_2E_1E_0$ </td></tr></table>

---

## Header Type/Format 字段编码

第 179 页的表 5‐3 汇总了 TLP Header 中 Type 字段 (类型) 与 Fmt 字段 (格式) 字段所使用的编码。

表 5‐3:TLP Header Type 字段 (类型) 与 Fmt 字段 (格式) 字段编码

<table><tr><td>TLP</td><td>FMT[2:0]</td><td>TYPE [4:0]</td></tr><tr><td>Memory Read Request (MRd)</td><td>000 = 3DW, no data001 = 4DW, no data</td><td>0 0000</td></tr><tr><td>Memory Read Lock Request (MRdLk)</td><td>000 = 3DW, no data001 = 4DW, no data</td><td>0 0001</td></tr><tr><td>Memory Write Request (MWr)</td><td>010 = 3DW, w/ data011 = 4DW, w/ data</td><td>0 0000</td></tr><tr><td>IO Read Request (IORd)</td><td>000 = 3DW, no data</td><td>0 0010</td></tr><tr><td>IO Write Request (IOWr)</td><td>010 = 3DW, w/ data</td><td>0 0010</td></tr><tr><td>Config Type 0 Read Request (CfgRd0)</td><td>000 = 3DW, no data</td><td>0 0100</td></tr><tr><td>Config Type 0 Write Request (CfgWr0)</td><td>010 = 3DW, w/ data</td><td>0 0100</td></tr><tr><td>Config Type 1 Read Request (CfgRd1)</td><td>000 = 3DW, no data</td><td>0 0101</td></tr><tr><td>Config Type 1 Write Request (CfgWr1)</td><td>010 = 3DW, w/ data</td><td>0 0101</td></tr><tr><td>Message Request (Msg)</td><td>001 = 4DW, no data</td><td>1 0 rrr*(see routing field)</td></tr><tr><td>Message Request W/Data (MsgD)</td><td>011 = 4DW, w/ data</td><td>1 0rrr*(see routing field)</td></tr><tr><td>Completion (Cpl)</td><td>000 = 3DW, no data</td><td>0 1010</td></tr><tr><td>Completion W/Data (CplD)</td><td>010 = 3DW, w/ data</td><td>0 1010</td></tr><tr><td>Completion-Locked (CplLk)</td><td>000 = 3DW, no data</td><td>0 1011</td></tr><tr><td>Completion W/Data (CplDLk)</td><td>010 = 3DW, w/ data</td><td>0 1011</td></tr><tr><td>Fetch and Add AtomicOp Request</td><td>010 = 3DW, w/ data011 = 4DW, w/ data</td><td>0 1100</td></tr><tr><td>Unconditional Swap AtomicOp Request</td><td>010 = 3DW, w/ data011 = 4DW, w/ data</td><td>0 1101</td></tr><tr><td>Compare and Swap AtomicOp Request</td><td>010 = 3DW, w/ data011 = 4DW, w/ data</td><td>0 1110</td></tr><tr><td>Local TLP Prefix</td><td>100 = TLP Prefix</td><td> $0L_3L_2L_1L_0$ </td></tr><tr><td>End-to-End TLP Prefix</td><td>100 = TLP Prefix</td><td> $1E_3E_2E_1E_0$ </td></tr></table>

---

## Digest / ECRC 字段

TLP Digest 位用于报告 End-to-End CRC (ECRC) 是否存在。如果支持并由软件启用了该可选功能,则设备会为它们发出的所有 TLP 计算并附加 ECRC。请注意,使用 ECRC 要求设备包含可选的 Advanced Error Reporting 寄存器,因为相关的 capability 和 control 寄存器就位于该处。

ECRC 的生成与校验。ECRC 覆盖 TLP 在整个 Fabric 中转发时不会发生变化的所有字段。然而,报文在拓扑中传输时,存在两个合法可能发生变化的位:

Type 字段的 bit 0 —— 当配置事务跨越桥转发并因到达目标总线而从 type 1 变为 type 0 配置事务时,该位会发生变化。这一过程通过修改 Type 字段的 bit 0 来完成。

Error/Poisoned (EP) 位 —— 如果报文所携带的数据被识别为已损坏,该位可能在 TLP 穿越 Fabric 时发生变化。这是一项被称为 error forwarding 的可选功能。

由谁校验 ECRC?ECRC 的预期目标是 TLP 的最终接收方。LCRC 的校验只能确认报文在某一给定链路上没有发生传输错误,但报文在路由元素(Switch 或 Root Complex)的出口端口处会被重新计算,然后才转发到下一条链路,这可能会掩盖路由元素内部的错误。为了防止这种情况,ECRC 在 Requester 和 Completer 之间一路保持不变地传递。当目标设备校验 ECRC 时,沿途任何可能的错误都有很高的概率被检出。

规范就 Switch 在 ECRC 校验中所扮演的角色给出了两点说明:

支持 ECRC 校验的 Switch 会对发往 Switch 内部位置的 TLP 执行该校验。"对于所有其他 TLP,Switch 必须保留 ECRC(原样转发),将其作为 TLP 的不可分割的一部分。"

"请注意,Switch 可以对穿越 Switch 的 TLP 执行 ECRC 校验。由 Switch 检测到的 ECRC 错误会以与其他设备相同的方式上报,但不会影响该 TLP 穿越 Switch 的过程。"

---

## 使用字节使能 (Byte Enable)

概述。与 PCI 类似,PCIe 需要一种机制来协调其 DW 对齐的地址与偶尔出现的非 DW 对齐的传输大小或起始/结束地址。为此,PCI Express 使用了前面在第 175 页的图 5‐3 和第 176 页的表 5‐2 中介绍的两个 Byte Enable 字段。First DW Byte Enable 字段和 Last DW Byte Enable 字段允许 Requester (请求端) 指定所传输的第一个和最后一个双字中感兴趣的那些字节。

## 字节使能规则

1. 字节使能位高电平有效。值为 0 表示完成报文不应使用数据负载中的对应字节;值为 1 表示应使用该字节。

2. 若有效数据全部位于单个 DW(Double Word)内,则 Last DW Byte Enable 字段必须 = 0000b。

3. 若包头 Length 字段表明传输长度超过 1DW,则 First DW Byte Enable 必须至少使能一位。

4. 若 Length 字段表明传输长度为 3DW 或以上,则 First DW Byte Enable 字段和 Last DW Byte Enable 字段必须设置为连续位。这种情况下,字节使能仅用于给出相对于 DW 对齐地址的有效起始地址和结束地址的字节偏移。

5. 若传输长度为 1DW,则允许 First DW Byte Enable 字段使用不连续的字节使能位图样。

6. 若传输长度介于一个 DW 与两个 DW 之间,则允许 First DW 和 Second DW Byte Enable 字段同时使用不连续的字节使能位图样。

7. 传输长度为 1DW 且所有字节使能均未置位的写请求是合法的,但对完成方没有任何效果。

8. 若 1DW 读请求的所有字节使能均未置位,则完成方返回 1DW 内容未定义的数据负载。该机制可作为一种 Flush(刷新)手段,利用事务排序规则,在完成报文返回之前强制将所有先前已 Post 的写操作刷出到内存。

字节使能示例。 该用例下的字节使能使用示例如 Figure 5‐4(第 182 页)所示。注意,传输长度必须从首个使能了任何有效字节的 DW 延伸至最后一个使能了任何有效字节的 DW。由于该传输超过 2DW,字节使能只能用于指定传输的起始地址位置(2d)与结束地址位置(34d)。

Figure 5‐4: 使用 First DW 与 Last DW 字节使能字段  
![](images/part02_6866d40c7ae466d43b498249907df37be5b233a907f7c511faebe3237f726984.jpg)

---

## Transaction Descriptor 字段 (事务描述符)

由于事务在请求者和完成者之间传输时,任何时刻同一 Requester (请求者) 都可能有多个分离事务被排队,因此有必要对每个事务进行唯一标识。为此,规范定义了若干重要的包头字段,共同构成唯一的 Transaction Descriptor (事务描述符),如图 5-5 所示。

图 5-5:Transaction Descriptor (事务描述符) 字段

<table><tr><td rowspan="2"></td><td colspan="2">+0</td><td colspan="5">+1</td><td colspan="5">+2</td><td colspan="2">+3</td></tr><tr><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>0</td><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td></tr><tr><td>Byte 0</td><td>Fmt</td><td>Type</td><td>R</td><td>TC</td><td>R</td><td>Attr</td><td>R</td><td>TH</td><td>TD</td><td>EP</td><td>Attr</td><td>AT</td><td colspan="2">Length</td></tr><tr><td>Byte 4</td><td colspan="8">Completer ID</td><td colspan="2">Cmpl Status</td><td>BCM</td><td colspan="3">Byte Count</td></tr><tr><td>Byte 8</td><td colspan="8">Requester ID</td><td colspan="4">Tag</td><td>R</td><td>Lower Addr</td></tr></table>

虽然 Transaction Descriptor (事务描述符) 字段在包头中并不位于相邻位置,但它们共同描述了事务的关键属性,包括:

Transaction ID (事务 ID)。由 Requester ID (请求者 ID,即 Requester 的 Bus、Device 和 Function 编号) 与 TLP 的 Tag 字段组合而成。

Traffic Class (流量类,TC)。Traffic Class (流量类,TC) 由 Requester 根据内核逻辑请求添加,在通过拓扑到达 Completer 的过程中保持不变。在每条 Link (链路) 上,TC 会被映射到某一个 Virtual Channel (虚通道) 上。

Transaction Attributes (事务属性)。基于 ID 的 Ordering (定序)、Relaxed Ordering (宽松定序) 和 No Snoop (无监听) 等位也随 Request (请求) 包一起传送到 Completer。

---

## 带数据负载 TLP 的附加规则

下列规则适用于包含数据负载的 TLP。

1. Length 字段仅指数据负载。

2. 负载中的第一个数据字节(紧跟包头之后)始终与最低(起始)地址相关联。

3. Length 字段始终表示所传输的整数字(DW)数。部分 DW 的限定通过 First DW Byte Enable 和 Last DW Byte Enable 字段完成。

4. 规范规定,当 Completer 响应单个内存请求返回多个事务时,对于 Root Complex,每个中间事务必须以自然对齐的 64 字节或 128 字节地址边界结束。此行为由一个称为 Read Completion Boundary (RCB) 的配置位控制。其他所有设备遵循 PCI-X 协议,在自然对齐的 128 字节边界处拆分此类事务。这使得桥接器中的缓冲区管理更为简单。

5. 发送 Message 请求时,Length 字段保留(除非该消息是带数据的版本,即 MsgD)。

6. TLP 数据负载不得超过 Device Control 寄存器中 Max_Payload_Size 字段的当前值。只有写事务带有数据负载,因此此限制不适用于读请求。接收器需在写操作期间检查是否违反 Max_Payload_Size 限制,违规将被视为 Malformed TLP。

7. 接收器还必须检查 Length 字段值与 TLP 中实际传输的数据量之间的不一致。此类违规同样被视为 Malformed TLP。

8. 请求不得混合使用起始地址与传输长度的组合,以避免导致内存访问跨越 4KB 边界。对此类情况的检查虽为可选项,但一旦发现,将视为 Malformed TLP。

---

## 特定 TLP 格式:请求与完成报文 TLP

本节描述用于实现特定事务类型的 3DW 和 4DW 包头格式。先前介绍的许多通用字段依然适用,但本节重点关注在特定事务类型中处理方式不同的字段。TLP 包头格式的详细说明将在后续章节中按以下 TLP 类型分别描述:1) IO 请求 (IO Request)、2) 内存请求 (Memory Request)、3) 配置请求 (Configuration Request)、4) 完成报文 (Completion) 以及 5) 消息请求 (Message Request)。


---

## IO Requests

虽然规范不鼓励使用 IO 事务,但仍为 Legacy 设备和需要依赖驻留在系统 IO 映射而非内存映射中的兼容设备的软件保留了使用空间。虽然 IO 事务在技术上可以访问 32 位 IO 范围,但实际上许多系统(以及 CPU)将 IO 访问限制在该范围的低 16 位(64KB)。第 185 页的图 5-6 展示了系统 IO 映射以及 16 位和 32 位地址边界。未将自身标识为 Legacy 设备的设备不允许在其配置基地址寄存器中请求 IO 地址空间。

图 5-6:系统 IO 映射  
![](images/part02_6e6817b2254ebb975f278610668a2f09f3d6eb0c14374f26db535bad26c54eb4.jpg)  
IO 请求包头格式。第 185 页的图 5-7 展示了 3 DW 的 IO 请求包头,后续章节将介绍每个字段。

图 5-7:3DW IO 请求包头格式  
![](images/part02_ec3566d8277fa448d856eb8d8b0127bafc6605dac2584e6c1f5197148ad9f4f7.jpg)

IO 请求包头字段。第 186 页的表 5-4 描述了 IO 请求包头中每个字段的位置和用途。

表 5-4:IO 请求包头字段

<table><tr><td>字段名称</td><td>包头字节/位</td><td>功能</td></tr><tr><td>Fmt [2:0](Format)(格式)</td><td>Byte 0 Bit 7:5</td><td>IO 请求的报文格式:000b = IO 读 (3DW without data)010b = IO 写 (3DW with data)</td></tr><tr><td>Type [4:0]</td><td>Byte 0 Bit 4:0</td><td>IO 请求的报文类型为 00010b</td></tr><tr><td>TC [2:0](Traffic Class)(流量类)</td><td>Byte 1 Bit 6:4</td><td>IO 请求的流量类始终为零,以确保这些报文永远不会干扰任何高优先级报文。</td></tr><tr><td>Attr [2](Attributes)(属性)</td><td>Byte 1 Bit 2</td><td>ID-based Ordering 不适用于 IO 请求,该位为保留位。</td></tr><tr><td>TH(TLP Processing Hints)(TLP 处理提示)</td><td>Byte 1 Bit 0</td><td>TLP 处理提示不适用于 IO 请求,该位为保留位。</td></tr><tr><td>TD(TLP Digest)(TLP 摘要)</td><td>Byte 2 Bit 7</td><td>指示 TLP 末端是否存在摘要字段(ECRC)。</td></tr><tr><td>EP(Poisoned Data)(中毒数据)</td><td>Byte 2 Bit 6</td><td>指示数据有效负载(如果存在)是否被中毒。</td></tr><tr><td>Attr [1:0](Attributes)(属性)</td><td>Byte 2 Bit 5:4</td><td>Relaxed Ordering 和 No Snoop 位不适用于 IO 请求,始终为零。</td></tr><tr><td>AT [1:0](Address Type)(地址类型)</td><td>Byte 2 Bit 3:2</td><td>地址类型不适用于 IO 请求,这些位必须为零。</td></tr><tr><td>Length [9:0]</td><td>Byte 2 Bit 1:0Byte 3 Bit 7:0</td><td>指示以 DW 为单位的数据有效负载大小。对于 IO 请求,该字段始终为 1,因为传输不能超过 4 字节。First DW Byte Enables 用于限定使用哪些字节。</td></tr><tr><td>Requester ID [15:0](请求者 ID)</td><td>Byte 4 Bit 7:0Byte 5 Bit 7:0</td><td>标识请求者的“返回地址”以用于相应的完成报文。Byte 4, 7:0 = Bus NumberByte 5, 7:3 = Device NumberByte 5, 2:0 = Function Number</td></tr><tr><td>Tag [7:0](标签字段)</td><td>Byte 6 Bit 7:0</td><td>这些位标识来自请求者的特定请求。每个发出的请求分配一个唯一的 Tag 值。默认情况下仅使用位 4:0,但 Extended Tag 和 Phantom Functions 选项可将其扩展至 11 位,从而允许同时有最多 2048 个未完成请求在执行中。</td></tr><tr><td>Last DW BE [3:0](Last DW Byte Enables)(最后一个 DW 字节使能)</td><td>Byte 7 Bit 7:4</td><td>这些位必须为 0000b,因为 IO 请求只能是一个 DW 大小。</td></tr><tr><td>1st DW BE [3:0](First DW Byte Enables)(第一个 DW 字节使能)</td><td>Byte 7 Bit 3:0</td><td>这些位限定单 DW 有效负载中的字节。对于 IO 请求,任何位组合均有效(包括全零)。</td></tr><tr><td>Address [31:2]</td><td>Byte 8 Bit 7:0Byte 9 Bit 7:0Byte 10 Bit 7:0Byte 11 Bit 7:2</td><td>IO 传输的 32 位起始地址的高 30 位。32 位地址的低 2 位为保留位(00b),强制采用 DW 对齐的起始地址。</td></tr></table>

## 内存请求

PCI Express 内存事务包括两类:读请求及其对应的完成报文,以及写请求。第 188 页的图 5-8 所示的系统内存映射同时描绘了 3DW 和 4DW 内存请求报文。请记住一个规范中多次重复强调的关键点:内存传输绝不允许跨越 4KB 地址边界。

Figure 5‐8: 3DW 和 4DW 内存请求 Header 格式  
![](images/part02_93481f62478e88c776bdd0b5bb56579eec265c6153ca3401d6c0b38f7ea618ab.jpg)  
内存请求 Header 字段。4DW 内存请求 Header 中每个字段的位置与用途见第 189 页的表 5-5。需要注意的是,3DW Header 与 4DW Header 之间的区别仅在于起始地址字段的位置和大小。

Table 5‐5: 4DW 内存请求 Header 字段

<table><tr><td>字段名</td><td>Header 字节/位</td><td>功能</td></tr><tr><td>Fmt [2:0](格式)</td><td>Byte 0 Bit 7:5</td><td>报文格式:000b = 内存读 (3DW 无数据)010b = 内存写 (3DW 带数据)001b = 内存读 (4DW 无数据)011b = 内存写 (4DW 带数据)1xxb = 报文起始处已添加 TLP Prefix。有关详情,请参阅第 899 页的 "TPH (TLP Processing Hints)"。</td></tr><tr><td>Type[4:0]</td><td>Byte 0 Bit 4:0</td><td>TLP 报文 Type 字段:00000b = 内存读或内存写00001b = 内存读锁定Type 字段与 Fmt [1:0] 字段配合使用,用于指定事务类型、Header 大小以及是否包含数据 Payload。</td></tr><tr><td>TC [2:0](流量类)</td><td>Byte 1 Bit 6:4</td><td>这些位对应用于该请求及其关联完成报文的流量类。000b = 流量类 0(默认)。111b = 流量类 7有关详情,请参阅第 247 页的 "Traffic Class (TC)"。</td></tr><tr><td>Attr [2](属性)</td><td>Byte 1 Bit 2</td><td>指示本 TLP 是否使用基于 ID 的排序。有关详情,请参阅第 301 页的 "ID Based Ordering (IDO)"。</td></tr><tr><td>TH(TLP 处理提示)</td><td>Byte 1 Bit 0</td><td>指示报文是否包含 TLP Hints。有关这些提示的讨论,请参阅第 899 页的 "TPH (TLP Processing Hints)"。</td></tr></table>

## PCI Express Technology

表 5‐5:4DW Memory Request Header 字段(续)

<table><tr><td>字段名称</td><td>包头字节/位</td><td>功能</td></tr><tr><td>TD(TLP Digest)</td><td>Byte 2 Bit 7</td><td>若为 1,则本 TLP 包含可选的 TLP Digest 字段。一些规则:所有接收器都必须检查 Digest 字段是否存在(通过该位)。TD = 1 但无 Digest 字段的 TLP 视为 Malformed。若 TD 位置 1,则接收端在启用 ECRC 检查时必须执行 ECRC 检查。如果接收器不支持可选的 ECRC 检查,则必须忽略 Digest 字段。</td></tr><tr><td>EP(Poisoned Data)</td><td>Byte 2 Bit 6</td><td>若为 1,则表示该报文所携带的数据应被视为存在错误,但事务仍允许正常完成。</td></tr><tr><td>Attr [1:0](Attributes)</td><td>Byte 2 Bit 5:4</td><td>Bit 5 = Relaxed ordering。当置 1 时,该 TLP 启用 PCI-X Relaxed Ordering;否则使用严格的 PCI 顺序。Bit 4 = No Snoop。若为 1,则系统硬件无须为该 TLP 触发处理器缓存监听以保证一致性;否则需要进行缓存监听。</td></tr><tr><td>Address Type [1:0]</td><td>Byte 2 Bit 3:2</td><td>该字段用于支持虚拟化系统中的地址转换。转换协议在单独的规范 Address Translation Services 中描述,可看出该字段编码方式为:00 = Default/Untranslated01 = Translation Request10 = Translated11 = Reserved</td></tr><tr><td>Length [9:0]</td><td>Byte 2 Bit 1:0Byte 3 Bit 7:0</td><td>TLP 数据有效负载的传输大小,以 DW 为单位。最大为 1024 DW (4KB),编码方式为:00 0000 0001b = 1DW00 0000 0010b = 2DW..11 1111 1111b = 1023 DW00 0000 0000b = 1024 DW</td></tr><tr><td>Requester ID [15:0]</td><td>Byte 4 Bit 7:0Byte 5 Bit 7:0</td><td>标识请求者的 Completion 返回地址:Byte 4,7:0 = Bus NumberByte 5,7:3 = Device NumberByte 5,2:0 = Function Number</td></tr><tr><td>Tag [7:0]</td><td>Byte 6 Bit 7:0</td><td>标识请求者发出的每一个 outstanding 请求。默认仅使用 bit 4:0,允许同时有最多 32 个请求处于进行中。若 Control Register 中的 Extended Tag 位置 1,则可使用全部 8 位(256 个 Tag)。</td></tr><tr><td>Last BE [3:0](Last DW Byte Enables)</td><td>Byte 7 Bit 7:4</td><td>用于限定传输数据中最后一个 DW 内的字节。</td></tr><tr><td>1st DW BE [3:0](First DW Byte Enables)</td><td>Byte 7 Bit 3:0</td><td>用于限定数据有效负载中第一个 DW 内的字节。</td></tr><tr><td>Address [63:32]</td><td>Byte 8 Bit 7:0Byte 9 Bit 7:0Byte 10 Bit 7:0Byte 11 Bit 7:0</td><td>64 位内存事务起始地址的高 32 位。</td></tr><tr><td>Address [31:2]</td><td>Byte 12 Bit 7:0Byte 13 Bit 7:0Byte 14 Bit 7:0Byte 15 Bit 7:2</td><td>64 位内存事务起始地址的低 32 位。地址的最低两位被保留,强制要求起始地址按 DW 对齐。</td></tr></table>

Memory Request 注意事项。Memory Request 的特性包括:

1. Memory 数据传输不得跨越 4KB 边界。

2. 所有 Memory Write 均采用 Posted 方式以提升性能。

3. 可以使用 32 位或 64 位地址。

4. 数据有效负载大小介于 0 到 1024 DW(0~4KB)之间。

5. 可以使用 QoS 特性,包括最多 8 个 Traffic Class。

6. No Snoop 属性可用于在事务访问主存时减轻系统对处理器缓存进行监听的需求。

7. 可以使用 Relaxed Ordering 属性,以允许报文路径上的设备采用 Relaxed Ordering 规则,从而有望提升性能。

---

## Configuration Requests(配置请求)

PCI Express 使用与 PCI 相同的方式来使用 Type 0 和 Type 1 配置请求,以保持向后兼容性。Type 1 周期向下游传播,直到到达其 secondary bus 与目标总线相匹配的桥为止。此时,该桥把配置事务从 Type 1 转换为 Type 0。桥根据先前编程的总线号寄存器——Primary、Secondary 和 Subordinate Bus Number——来判断何时转发并转换配置周期。有关此主题的更多信息,请参阅第 91 页的"Legacy PCI Mechanism(传统 PCI 机制)"一节。

图 5-9:3DW Configuration Request And Header Format(3DW 配置请求与包头格式)
![](images/part02_5807124a29434194ad38ae629fb7a39f2a557405c60e04e616a162a37d27fdd8.jpg)

在第 193 页的图 5-9 中,展示了一个 Type 1 配置周期向下游传播,并由该总线的桥将其转换为 Type 0(通过改变 Type 字段的 bit 0 来实现)。请注意,与 PCI 不同的是,一条 Link(链路)下游只能驻留一个设备。因此,不需要 IDSEL 或其他硬件指示来告知设备它应当认领该 Type 0 周期;设备在其上游 Link 上看到的任何 Type 0 配置周期都将被视为针对该设备本身。

Definitions Of Configuration Request Header Fields(配置请求包头字段定义)。第 194 页的表 5-6 描述了图 5-9 所示配置请求包头中每个字段的位置和用途。

表 5-6:Configuration Request Header Fields(配置请求包头字段)

<table><tr><td>字段名称</td><td>包头字节/位</td><td>功能</td></tr><tr><td>Fmt [2:0](格式)</td><td>Byte 0 Bit 7:5</td><td>始终为 3DW 包头000b = configuration read(配置读,无数据)010b = configuration write(配置写,带数据)</td></tr><tr><td>Type [4:0]</td><td>Byte 0 Bit 4:0</td><td>00100b = Type 0 配置请求00101b = Type 1 配置请求</td></tr><tr><td>TC [2:0](流量类)</td><td>Byte 1 Bit 6:4</td><td>配置请求的 Traffic Class 必须为零,以确保这些报文永远不会干扰任何高优先级报文。</td></tr><tr><td>Attr [2](属性)</td><td>Byte 1 Bit 2</td><td rowspan="2">这些位为保留位,配置请求中必须为零。</td></tr><tr><td>TH(TLP 处理提示)</td><td>Byte 1 Bit 0</td></tr><tr><td>TD(TLP 摘要)</td><td>Byte 2 Bit 7</td><td>指示在该 TLP 末尾是否存在摘要字段(1 DW)。</td></tr><tr><td>EP(Poisoned Data,中毒数据)</td><td>Byte 2 Bit 6</td><td>指示数据负载已被中毒。</td></tr><tr><td>Attr [1:0](属性)</td><td>Byte 2 Bit 5:4</td><td>配置请求中 Relaxed Ordering 与 No Snoop 位始终 = 0。</td></tr><tr><td>AT [1:0](地址类型)</td><td>Byte 2 Bit 3:2</td><td>Address Type 在配置请求中为保留,必须为零。</td></tr><tr><td>Length [9:0]</td><td>Byte 2 Bit 1:0Byte 3 Bit 7:0</td><td>数据负载大小以 DW 为单位,配置请求始终 = 1。Byte Enables 对该 DW 内的字节进行限定,任意组合均合法。</td></tr><tr><td>Requester ID [15:0]</td><td>Byte 4 Bit 7:0Byte 5 Bit 7:0</td><td>标识请求者的完成报文返回地址:Byte 4, 7:0 = Bus NumberByte 5, 7:3 = Device NumberByte 5, 2:0 = Function Number</td></tr><tr><td>Tag [7:0]</td><td>Byte 6 Bit 7:0</td><td>这些位标识请求者发出的未完成请求。默认情况下仅使用 bit 4:0(同时 32 个未完成事务),但如果 Control Register 中的 Extended Tag 位被置 1,则可使用全部 8 位(256 个标签)。</td></tr><tr><td>Last BE [3:0](最后一个 DW 字节使能)</td><td>Byte 7 Bit 7:4</td><td>这些位对所传输最后一个数据 DW 中的字节进行限定。由于配置请求大小只能为一个 DW,这些位必须为零。</td></tr><tr><td>1st DW BE [3:0](第一个 DW 字节使能)</td><td>Byte 7 Bit 3:0</td><td>这些高有效位对所传输第一个数据 DW 中的字节进行限定。对于配置请求,任何位组合均有效(包括全部无效)。</td></tr><tr><td>Completer ID [15:0]</td><td>Byte 8 Bit 7:0Byte 9 Bit 7:0</td><td>标识本次配置周期所访问的完成者。Byte 8, 7:0 = Bus NumberByte 9, 7:3 = Device NumberByte 9, 2:0 = Function Number</td></tr><tr><td>Ext Register Number[3:0](扩展寄存器号)</td><td>Byte 10 Bit 3:0</td><td>这些位提供用于访问扩展配置空间 DW 空间的高 4 位。它们与 Register Number 组合,形成访问 1024 DW(4096 字节)空间所需的 10 位地址。对于 PCI 兼容的配置空间,此字段必须为零。</td></tr><tr><td>Register Number [5:0]</td><td>Byte 11 Bit 7:0</td><td>作为配置 DW 空间的低 8 位,这些位指定寄存器号。最低两位始终为零,强制按 DW 对齐访问。</td></tr></table>

Configuration Request Notes(配置请求注意事项)。配置请求始终使用 3DW 包头格式,并根据目标 Bus、Device 和 Function 号进行路由。所有设备在每次接收到 Type 0 配置写周期时,都会从请求中的目标编号"捕获"自己的 Bus 和 Device Number。这样做是因为它们日后在发送自己的请求时,需要使用这些编号作为自己的 Requester ID。

---

## 完成报文 (Completions)

除非发生错误导致无法返回,否则非发布的请求 (Request) 都应当收到对应的完成报文 (Completion)。例如,Memory 读、IO 读或 Configuration 读请求通常会返回带数据的完成报文;而 IO 写或 Configuration 写请求通常返回不带数据的完成报文,仅用于报告该事务 (transaction) 的状态。

完成报文中的许多字段与对应的请求使用相同的取值,包括流量类 (Traffic Class, TC)、属性位以及原始的请求者 ID (Requester ID, 用于将完成报文路由回请求者)。第 197 页的图 5-10 展示了一个针对非发布请求返回的完成报文,以及它所使用的 3DW 包头 (Header) 格式。完成报文还在包头中提供了 Completer ID (完成者 ID)。在正常运行期间,Completer ID 并不重要,但在系统调试过程中,了解完成报文来自何处对错误诊断可能有所帮助。

图 5-10:3DW 完成报文包头格式
![](images/part02_a6cddfbfaf4ca7c4ab4647260c51d133a2bd27b3074d97b8c5923f662039ce02.jpg)
完成报文包头字段定义。第 197 页的表 5-7 描述了完成报文包头中每个字段的位置和用途。

表 5-7:完成报文包头字段

<table><tr><td>字段名</td><td>包头字节/位</td><td>功能</td></tr><tr><td>Fmt [2:0] (Format 格式)</td><td>Byte 0 Bit 7:5</td><td>报文格式 (始终为 3DW 包头)000b = 不带数据的完成报文 (Cpl)010b = 带数据的完成报文 (CplD)</td></tr><tr><td>Type [4:0]</td><td>Byte 0 Bit 4:0</td><td>报文类型,完成报文为 01010b。</td></tr></table>

---

## PCI Express Technology

Table 5‐7: 完成报文头字段(续)

<table><tr><td>字段名称</td><td>包头字节/位</td><td>功能</td></tr><tr><td>TC [2:0](流量类)</td><td>Byte 1 Bit 6:4</td><td>完成报文此处必须使用与对应请求(Request)相同的值。</td></tr><tr><td>Attr [2](属性)</td><td>Byte 1 Bit 2</td><td>指示此 TLP 是否使用基于 ID 的排序(IDO)。有关详细信息,请参阅第 301 页 "ID Based Ordering (IDO)"。</td></tr><tr><td>TH(TLP 处理提示)</td><td>Byte 1 Bit 0</td><td>完成报文保留。</td></tr><tr><td>TD(TLP Digest)</td><td>Byte 2 Bit 7</td><td>若 = 1,表示 TLP 末尾存在摘要字段。</td></tr><tr><td>EP(中毒数据)</td><td>Byte 2 Bit 6</td><td>若 = 1,表示数据载荷已被中毒。</td></tr><tr><td>Attr [1:0](属性)</td><td>Byte 2 Bit 5:4</td><td>完成报文此处必须使用与对应请求(Request)相同的值。</td></tr><tr><td>AT [1:0](地址类型)</td><td>Byte 2 Bit 3:2</td><td>地址类型(Address Type)对完成报文保留,必须为零,但并不要求也不建议接收器对此进行检查。</td></tr><tr><td>Length [9:0]</td><td>Byte 2 Bit 1:0Byte 3 Bit 7:0</td><td>指示数据载荷的大小(以 DW 为单位)。对完成报文而言,此字段反映与此完成报文相关联的数据载荷的大小。</td></tr><tr><td>Completer ID [15:0]</td><td>Byte 4 Bit 7:0Byte 5 Bit 7:0</td><td>标识完成方以支持问题调试。Byte 4 7:0 = Completer Bus #Byte 5 7:3 = Completer Dev #Byte 5 2:0 = Completer Function #</td></tr></table>