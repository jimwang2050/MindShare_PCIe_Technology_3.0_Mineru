# Ch08_Transaction_Ordering

| EN | ZH |
|---|---|
| # Transaction Ordering | # 事务排序 |

| EN | ZH |
|---|---|
| ## The Previous Chapter | ## 前一章 |
| The previous chapter discusses the mechanisms that support Quality of Service and describes the means of controlling the timing and bandwidth of different packets traversing the fabric. These mechanisms include application-specific software that assigns a priority value to every packet, and optional hardware that must be built into each device to enable managing transaction priority. | 前一章讨论了支持服务质量（Quality of Service）的机制，并描述了控制穿越互连结构中不同数据包时序和带宽的方法。这些机制包括为每个数据包分配优先级值的应用特定软件，以及必须内置于每个设备中以实现事务优先级管理的可选硬件。 |

| EN | ZH |
|---|---|
| ## This Chapter | ## 本章 |
| This chapter discusses the ordering requirements for transactions in a PCI Express topology. These rules are inherited from PCI. The Producer/Consumer programming model motivated many of them, so its mechanism is described here. The original rules also took into consideration possible deadlock conditions that must be avoided. | 本章讨论PCI Express拓扑结构中事务的排序要求。这些规则继承自PCI。生产者/消费者编程模型是其中许多规则的动因，因此此处描述了其机制。原始规则还考虑了必须避免的可能死锁条件。 |

## The Next Chapter

| EN | ZH |
|---|---|
| The next chapter describes, Data Link Layer Packets (DLLPs). We describe the use, format, and definition of the DLLP packet types and the details of their related fields. DLLPs are used to support Ack/Nak protocol, power management, flow control mechanism and can be used for vender defined purposes. | 下一章描述数据链路层包(DLLP)。我们将介绍DLLP包类型的使用、格式和定义及其相关字段的详细信息。DLLP用于支持Ack/Nak协议、电源管理、流控机制，并可用于厂商自定义目的。 |

## Introduction

## 引言

| EN | ZH |
| --- | --- |
| As with other protocols, PCI Express imposes ordering rules on transactions of the same traffic class (TC) moving through the fabric at the same time. Transactions with different TCs do not have ordering relationships. The reasons for these ordering rules related to transactions of the same TC include: | 与其他协议一样，PCI Express 对同时在同一结构中移动的相同流量类（TC）的事务施加了排序规则。不同 TC 的事务之间没有排序关系。与相同 TC 事务相关的这些排序规则的原因包括： |
| • Maintaining compatibility with legacy buses (PCI, PCI‐X, and AGP). | • 保持与传统总线（PCI、PCI-X 和 AGP）的兼容性。 |
| • Ensuring that the completion of transactions is deterministic and in the sequence intended by the programmer. | • 确保事务的完成是确定性的，并符合程序员预期的顺序。 |

## PCI Express 3.0 Technology

| EN | ZH |
|---|---|
| ## PCI Express 3.0 Technology | ## PCI Express 3.0 技术 |
| • Avoiding deadlock conditions. | • 避免死锁条件。 |
| • Maximize performance and throughput by minimizing read latencies and managing read and write ordering. | • 通过最小化读取延迟和管理读写排序来最大化性能和吞吐量。 |
| Implementation of the specific PCI/PCIe transaction ordering is based on the following features: | 特定 PCI/PCIe 事务排序的实现基于以下特性： |
| 1. Producer/Consumer programming model on which the fundamental ordering rules are based. | 1. 生产者/消费者编程模型，基本排序规则基于该模型。 |
| 2. Relaxed Ordering option that allows an exception to this when the Requester knows that a transaction does not have any dependencies on previous transactions. | 2. 宽松排序选项，当请求者知道某个事务不依赖于先前事务时，允许对此进行例外处理。 |
| 3. ID Ordering option that allows a switches to permit requests from one device to move ahead of requests from another device because unrelated threads of execution are being performed by these two devices. | 3. ID 排序选项，允许交换机让一个设备的请求优先于另一个设备的请求，因为这两个设备正在执行不相关的执行线程。 |
| 4. Means for avoiding deadlock conditions and supporting PCI legacy implementations. | 4. 用于避免死锁条件和支持 PCI 遗留实现的手段。 |

## Definitions / 定义

| EN | ZH |
|----|----|
| There are three general models for ordering transactions in a traffic flow: | 在流量流中，事务排序有三种通用模型： |
| 1. **Strong Ordering**: PCI Express requires strong ordering of transactions flowing through the fabric that have the same Traffic Class (TC) assignment. Transactions that have the same TC value assigned to them are mapped to a given VC, therefore the same rules apply to transactions within each VC. Consequently, when multiple TCs are assigned to the same VC all transactions are typically handled as a single TC, even though no ordering relationship exists between different TCs. | 1. **强排序(Strong Ordering)**：PCI Express要求对通过结构(Fabric)传输且具有相同流量类(Traffic Class, TC)分配的事务进行强排序。被分配相同TC值的事务被映射到给定VC(Virtual Channel)，因此相同的规则适用于每个VC内的事务。因此，当多个TC被分配到同一个VC时，所有事务通常被视为单个TC处理，即使不同TC之间不存在排序关系。 |
| 2. **Weak Ordering**: Transactions stay in sequence unless reordering would be helpful. Maintaining the strong ordering relationship between transactions can result in all transactions being blocked due to dependencies associated with a given transaction model (e.g., The Producer/Consumer Model). Some of the blocked transactions very likely are not related to the dependencies and can safely be reordered ahead of blocking transactions. | 2. **弱排序(Weak Ordering)**：事务保持顺序，除非重新排序会有帮助。维持事务之间的强排序关系可能导致所有事务因给定事务模型（例如生产者/消费者模型，Producer/Consumer Model）的相关依赖而被阻塞。某些被阻塞的事务很可能与这些依赖无关，可以安全地重新排序到阻塞事务之前。 |
| 3. **Relaxed Ordering**: Transactions can be reordered, but only under certain controlled conditions. The benefit is improved performance like the weak-ordered model, but only when specified by software so as to avoid problems with dependencies. The drawback is that only some transactions will be optimized for performance. There is some overhead for software to enable transactions for Relaxed Ordering (RO). | 3. **宽松排序(Relaxed Ordering)**：事务可以被重新排序，但仅在特定的受控条件下。其优点是像弱排序模型一样提升性能，但仅在软件指定时生效，以避免依赖问题。缺点是只有部分事务会得到性能优化，并且软件启用宽松排序(RO)会有一定的开销。 |

| EN | ZH |
|---|---|
| ## Simplified Ordering Rules | ## 简化排序规则 |
| The 2.1 revision of the spec introduced a simplified version of the Ordering Table as shown in Table 8‑1 on page 289. The table can be segmented on a per topic basis as follows: | 2.1修订版规范引入了排序表的简化版本，如表8-1（第289页）所示。该表可按主题分类如下： |
| • Producer/Consumer rules (page 290) | • 生产者/消费者规则（第290页） |
| • Relaxed Ordering rules (page 296) | • 宽松排序规则（第296页） |
| • Weak Ordering rules (page 299) | • 弱排序规则（第299页） |
| • ID Ordering rules (page 301) | • ID排序规则（第301页） |
| • Deadlock avoidance (page 303) | • 死锁避免（第303页） |
| These sections provide details associated with the ordering models, operation, rationales, conditions and requirement. | 这些章节提供了与排序模型、操作、原理、条件和要求相关的详细信息。 |

## Ordering Rules and Traffic Classes (TCs)

| EN | ZH |
|---|---|
| PCI Express ordering rules apply to transactions of the same Traffic Class (TC). Transactions moving through the fabric that have different TCs have no ordering requirement and are considered to be associated with unrelated applications. As a result, there is no transaction ordering related performance degradation associated with packets of different TCs. | PCI Express 排序规则适用于同一流量类（TC）的事务。在结构中传输且具有不同 TC 的事务之间没有排序要求，它们被视为与不相关的应用相关联。因此，不同 TC 的数据包之间不存在与事务排序相关的性能下降。 |
| Packets that do share the same TC may experience performance degradation as they flow through the PCIe fabric. This is because switches and devices must support ordering rules that may require packets to be delayed or forwarded in front of packets previously sent. | 共享同一 TC 的数据包在流经 PCIe 结构时可能会经历性能下降。这是因为交换机和设备必须支持排序规则，这些规则可能要求数据包被延迟，或者被优先转发到先前已发送的数据包之前。 |
| As discussed in Chapter 7, entitled "Quality of Service," on page 245, transactions of different TC may map to the same VC. The TC-to-VC mapping configuration determines which packets of a given TC map to a specific VC. Even though the transaction ordering rules apply only to packets of the same TC, it may be simpler to design endpoint devices/switches/root complexes that apply the transaction ordering rules to all packets within a VC even though multiple TCs are mapped to the same VC. | 如第 245 页第 7 章"服务质量"所述，不同 TC 的事务可以映射到同一 VC。TC 到 VC 的映射配置决定了给定 TC 的哪些数据包映射到特定的 VC。尽管事务排序规则仅适用于同一 TC 的数据包，但将端点设备/交换机/根复合体设计为对同一 VC 内的所有数据包应用事务排序规则可能更为简单，即使多个 TC 映射到同一 VC 也是如此。 |
| As one would expect, there are no ordering relationships between packets that map to different VCs no matter their TC. | 正如所料，映射到不同 VC 的数据包之间无论其 TC 如何，都不存在排序关系。 |

## Ordering Rules Based On Packet Type

| EN | ZH |
| --- | --- |
| Ordering relationships defined by the PCIe spec are based on TLP type. TLPs are divided into three categories: 1) Posted, 2) Completion and 3) Non-Posted TLPs. | PCIe 规范定义的排序关系基于 TLP 类型。TLP 分为三类：1) Posted（发布），2) Completion（完成报文）和 3) Non-Posted（非发布）TLP。 |
| The Posted category of TLPs include memory write requests (MWr) and Messages (Msg/MsgD). Completion category of TLPs include Cpl and CplD. Non-Posted category of TLPs include MRd, IORd, IOWr, CfgRd0, CfgRd1, CfgWr0 and CfgWr1. | Posted 类 TLP 包括存储器写请求 (MWr) 和消息 (Msg/MsgD)。Completion 类 TLP 包括 Cpl 和 CplD。Non-Posted 类 TLP 包括 MRd、IORd、IOWr、CfgRd0、CfgRd1、CfgWr0 和 CfgWr1。 |
| The transaction ordering rules are described by a table in the following section "The Simplified Ordering Rules Table" on page 288. As you will notice, the table shows TLPs listed according to the three categories mentioned above with their ordering relationships defined. | 事务排序规则由下一节（第 288 页的 "简化排序规则表"）中的表格描述。您会注意到，该表根据上述三类列出 TLP，并定义了它们的排序关系。 |

## The Simplified Ordering Rules Table / 简化排序规则表

| EN | ZH |
|---|---|
| The table is organized in a Row Pass Column fashion. All of the rules are summarized following the Simplified Ordering Table. Each rule or group of rules define the actions that are required. | 该表采用行可超越列的编排方式。所有规则均在简化排序表之后进行了总结。每一条或每一组规则定义了所需采取的操作。 |
| In Table 8-1 on page 289, columns 2-5 represent transactions that have previously been delivered by a PCI Express device, while row A-D represents a new transaction that has just arrived. For outbound transactions, the table specifies whether a transaction represented in the row (A-D) is allowed to pass a previous transaction represented by the column (2-5). A 'No' entry means the transaction in the row is not allowed to pass the transaction in the column. A 'Yes' entry means the transaction in the row must be allowed to pass the transaction in the column to avoid a deadlock. A 'Yes/No' entry means a transaction in a row is allowed to pass the transaction in the column but is not required to do so. The entries in the following have the meaning. | 在第289页的表8-1中，第2至5列表示PCI Express设备先前已传送的事务，而行A至D表示刚刚到达的新事务。对于对外事务，该表规定了行(A-D)所代表的事务是否被允许超越列(2-5)所代表的先前事务。"No"表项表示行中的事务不允许超越列中的事务。"Yes"表项表示行中的事务必须被允许超越列中的事务，以避免死锁。"Yes/No"表项表示行中的事务被允许超越列中的事务，但并非必须这样做。以下各项具有相应的含义。 |

**Table 8-1: Simplified Ordering Rules Table**
**表8-1：简化排序规则表**

<table><tr><td rowspan="2" colspan="2">Row pass Column? (Col 1)</td><td rowspan="2">Posted Request (Col 2)</td><td colspan="2">Non-Posted Request</td><td rowspan="2">Completion (Col 5)</td></tr><tr><td>Read Request (Col 3)</td><td>NPR with Data (Col 4)</td></tr><tr><td colspan="2">Posted Request (Row A)</td><td>a) No b) Y/N</td><td>Yes</td><td>Yes</td><td>a) Y/Nb) Yes</td></tr><tr><td rowspan="2">Non-Posted Request</td><td>Read Request (Row B)</td><td>a) No b) Y/N</td><td>Y/N</td><td>Y/N</td><td>Y/N</td></tr><tr><td>NPR with Data (Row C)</td><td>a) No b) Y/N</td><td>Y/N</td><td>Y/N</td><td>Y/N</td></tr><tr><td colspan="2">Completion (Row D)</td><td>a) No b) Y/N</td><td>Yes</td><td>Yes</td><td>a) Y/Nb) No</td></tr></table>

| EN | ZH |
|---|---|
| • A2a, B2a, C2a, D2a — to enforce the Producer/Consumer model, a subsequent transaction is not allowed to pass a Posted Request. | • A2a、B2a、C2a、D2a——为了强制执行生产者/消费者模型，后续事务不允许超越Posted请求。 |
| • A2, D2b — If RO is set, then a Read Completion is permitted to pass a previously queued Memory Write or Message Request. | • A2、D2b——如果设置了RO（宽松排序），则允许读完成超越先前排队的存储器写或消息请求。 |
| A2b, B2b, C2b, D2b — if the optional IDO is being used, a subsequent transaction is allowed to pass a Posted Request, as long as their Requester IDs are different. | A2b、B2b、C2b、D2b——如果使用了可选的IDO（基于ID的排序），则只要其请求者ID不同，后续事务就被允许超越Posted请求。 |
| • A3, A4 — A Memory Write or Message Request must be allowed to pass Non-Posted Requests to avoid deadlocks. | • A3、A4——存储器写或消息请求必须被允许超越Non-Posted请求，以避免死锁。 |
| • A5a — Posted Request is permitted but not required to pass Completions. | • A5a——Posted请求被允许但非必须超越完成报文。 |
| A5b — Deadlock avoidance case. In a PCIe-to-PCI/PCI-X bridge, for transactions going from PCIe to PCI or PCI-X, a Posted Request must be able to pass a Completion, or a deadlock may occur. | A5b——死锁避免情况。在PCIe到PCI/PCI-X桥中，对于从PCIe到PCI或PCI-X的事务，Posted请求必须能够超越完成报文，否则可能发生死锁。 |
| • B3, B4, B5, C3, C4, C5, — These cases implement weak ordering without risking any ordering related problems. | • B3、B4、B5、C3、C4、C5——这些情况实现了弱排序，而不会带来任何排序相关问题的风险。 |
| D3, D4 — Completions must be allowed to pass Read and I/O or Configuration Write Requests (Non-Posted Requests) to avoid deadlocks. | D3、D4——完成报文必须被允许超越读请求和I/O或配置写请求（Non-Posted请求），以避免死锁。 |
| • D5a — Completions with different Transaction IDs may pass each other. | • D5a——具有不同事务ID的完成报文可以相互超越。 |
| D5b — Completions with the same Transaction ID are not allowed to pass each other. This ensures that multiple completions for a single request will remain in ascending address order. | D5b——具有相同事务ID的完成报文不允许相互超越。这确保了对单个请求的多个完成报文将保持地址升序。 |

## 生产者/消费者模型 (Producer/Consumer Model)

| EN | ZH |
|---|---|
| This section describes the operation of the Producer/Consumer model and the associated ordering rules required for proper operation. Figure 8-1 on page 291 simply illustrates a sample topology. Subsequent examples of this topology describe the operation of the Producer/Consumer model with proper ordering, followed by an example of the model failing due to improper ordering. | 本节描述生产者/消费者模型的操作以及正确运行所需的关联排序规则。图8-1（第291页）简单展示了一个示例拓扑。基于该拓扑的后续示例描述了在正确排序下生产者/消费者模型的操作，随后给出了一个因排序不当而导致模型失败的示例。 |
| The Producer/Consumer model is the common method for data delivery in PCI and PCIe. The model comprises five elements as depicted in Figure 8-1: | 生产者/消费者模型是PCI和PCIe中数据传输的常用方法。该模型包含如图8-1所示的五个要素： |
| • Producer of data | • 数据生产者 |
| • Memory data buffer | • 内存数据缓冲区 |
| • Flag semaphore indicating data has been send by the Producer | • 标志信号量，指示生产者已发送数据 |
| • Consumer of data | • 数据消费者 |
| • Status semaphore indicating Consumer has read data | • 状态信号量，指示消费者已读取数据 |
| The specification states that the Producer/Consumer model will work regardless of the arrangement of all the elements involved. In this example, the Flag and Status elements reside in the same physical device, but could be located in different devices. | 规范指出，无论所有相关元素的排列如何，生产者/消费者模型都能正常工作。在本示例中，Flag和Status元素位于同一物理设备中，但它们也可以位于不同的设备中。 |

**Figure 8-1: Example Producer/Consumer Topology**

![](images/part02_5eda80caf08f99026b670ecf9b0512d6f0256d429817f55a48074adb20abd139.jpg)

## Producer/Consumer Sequence — No Errors

Refer to Figure 8-2 on page 293 during the following discussion. The example presumes that the Flag and Status element are cleared to start with. These semaphores are included within the same device in this example. The sequence of numbered events in the description below and depicted in Figure 8-2 on page 293 reflect the correct ordering in this Part 1 sequence.

1. In the example, a device called the Producer performs one or more Memory Write transactions (Posted Requests) targeting a Data Buffer in memory. Some delay can occur as the data flows through Posted buffers.

2. The Consumer periodically checks the Flag by initiating a Memory Read transaction (Non-Posted Request) to determine if data has been delivered by the Producer.

3. The Flag semaphore is read by the device and a Memory Read Completion is returned to the Consumer, indicating that notification of data delivery has not been performed by the Producer (Flag = 0) yet.

4. The Producer sends a Memory Write Transaction (Posted Request) to update the Flag to 1.

5. Once again, the Consumer checks the Flag by performing the same transaction performed in step 2.

6. When Flag semaphore is read this time, the Flag is set to 1, indicating to the Consumer, via the Completion, that all of the data has been delivered by the Producer to memory.

7. Next, the Consumer performs a Memory Write transaction (Posted Request) to clear the Flag semaphore back to zero.

Figure 8-3 on page 294 continues the example in this Part 2 sequence.

8. The Producer, having more data to send, periodically checks the Status semaphore by initiating a Memory Read transaction (Non-Posted Request).

9. The Status semaphore is read by the Producer and a Memory Read Completion is returned to the Producer, indicating that the Consumer has not read the memory buffer contents and updated Status (Status = 0).

10. The Consumer, knowing that the memory buffer has data available, performs one or more Memory Read Requests (Non-Posted Requests) to get the contents from the buffer.

11. Memory contents are read and returned to the Consumer.

12. Upon completing the data transfer, the Consumer initiates a Memory Write Request (Posted Request) to set the Status semaphore to a 1.

13. Once again, the Producer checks the Status semaphore by delivering a Memory Read Request (Non-Posted Request).

14. The device reads the Status and this time it is set to 1. The Completion is returned to the Producer, thereby indicating data can be sent to Memory.

15. The Producer sends a Memory Write to Clear the Status semaphore to 0.

16. The sequence of events starting with step 1. is repeated by the Producer.

## 生产者/消费者序列 — 无错误

| EN | ZH |
|---|---|
| Refer to Figure 8-2 on page 293 during the following discussion. The example presumes that the Flag and Status element are cleared to start with. These semaphores are included within the same device in this example. The sequence of numbered events in the description below and depicted in Figure 8-2 on page 293 reflect the correct ordering in this Part 1 sequence. | 以下讨论请参考第293页的图8-2。本示例假定标志(Flag)和状态(Status)元素初始时已被清除。这些信号量位于同一设备内。下文描述中及图8-2所描绘的编号事件序列反映了本部分1序列的正确顺序。 |
| 1. In the example, a device called the Producer performs one or more Memory Write transactions (Posted Requests) targeting a Data Buffer in memory. Some delay can occur as the data flows through Posted buffers. | 1. 在本示例中，一个称为生产者(Producer)的设备执行一次或多次指向存储器中数据缓冲器的存储器写事务（发布请求）。数据流经发布缓冲器时可能会产生一些延迟。 |
| 2. The Consumer periodically checks the Flag by initiating a Memory Read transaction (Non-Posted Request) to determine if data has been delivered by the Producer. | 2. 消费者(Consumer)通过发起存储器读事务（非发布请求）周期性地检查标志，以确定生产者是否已交付数据。 |
| 3. The Flag semaphore is read by the device and a Memory Read Completion is returned to the Consumer, indicating that notification of data delivery has not been performed by the Producer (Flag = 0) yet. | 3. 设备读取标志信号量，并向消费者返回存储器读完成报文，指示生产者尚未执行数据交付的通知（标志 = 0）。 |
| 4. The Producer sends a Memory Write Transaction (Posted Request) to update the Flag to 1. | 4. 生产者发送存储器写事务（发布请求）将标志更新为1。 |
| 5. Once again, the Consumer checks the Flag by performing the same transaction performed in step 2. | 5. 消费者再次执行与步骤2相同的事务来检查标志。 |
| 6. When Flag semaphore is read this time, the Flag is set to 1, indicating to the Consumer, via the Completion, that all of the data has been delivered by the Producer to memory. | 6. 本次读取标志信号量时，标志被设置为1，通过完成报文向消费者指示生产者已将所有数据交付至存储器。 |
| 7. Next, the Consumer performs a Memory Write transaction (Posted Request) to clear the Flag semaphore back to zero. | 7. 接下来，消费者执行存储器写事务（发布请求）将标志信号量清除回零。 |
| Figure 8-3 on page 294 continues the example in this Part 2 sequence. | 第294页的图8-3在本部分2序列中继续该示例。 |
| 8. The Producer, having more data to send, periodically checks the Status semaphore by initiating a Memory Read transaction (Non-Posted Request). | 8. 生产者有更多数据要发送，通过发起存储器读事务（非发布请求）周期性地检查状态信号量。 |
| 9. The Status semaphore is read by the Producer and a Memory Read Completion is returned to the Producer, indicating that the Consumer has not read the memory buffer contents and updated Status (Status = 0). | 9. 生产者读取状态信号量，并向生产者返回存储器读完成报文，指示消费者尚未读取存储器缓冲器内容并更新状态（状态 = 0）。 |
| 10. The Consumer, knowing that the memory buffer has data available, performs one or more Memory Read Requests (Non-Posted Requests) to get the contents from the buffer. | 10. 消费者得知存储器缓冲器中有数据可用，执行一次或多次存储器读请求（非发布请求）以从缓冲器获取内容。 |
| 11. Memory contents are read and returned to the Consumer. | 11. 存储器内容被读取并返回给消费者。 |
| 12. Upon completing the data transfer, the Consumer initiates a Memory Write Request (Posted Request) to set the Status semaphore to a 1. | 12. 完成数据传输后，消费者发起存储器写请求（发布请求）将状态信号量设置为1。 |
| 13. Once again, the Producer checks the Status semaphore by delivering a Memory Read Request (Non-Posted Request). | 13. 生产者再次通过发送存储器读请求（非发布请求）检查状态信号量。 |
| 14. The device reads the Status and this time it is set to 1. The Completion is returned to the Producer, thereby indicating data can be sent to Memory. | 14. 设备读取状态，本次状态被设置为1。完成报文返回给生产者，从而指示可以向存储器发送数据。 |
| 15. The Producer sends a Memory Write to Clear the Status semaphore to 0. | 15. 生产者发送存储器写操作将状态信号量清除为0。 |
| 16. The sequence of events starting with step 1. is repeated by the Producer. | 16. 生产者重复从步骤1开始的事件序列。 |

Figure 8-2: Producer/Consumer Sequence Example — Part 1
![](images/part02_18c3d10494719e3f89351b1fca0e67124b2f0e9505a830ce4e2539dfcc615644.jpg)

Figure 8-3: Producer/Consumer Sequence Example — Part 2
![](images/part02_dcada6a33b479b3fd6bb6c856cb1f96518aad2ce1a3930a6089a7acf08c27b7a.jpg)