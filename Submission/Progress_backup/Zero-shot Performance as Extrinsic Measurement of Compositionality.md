# Zero-shot Performance as Extrinsic Measurement of Compositionality

**Zero-shot performance** refers to the model's performance on the task which it has not been explicitly trained on. When presented with a new **?**, the agents use the learned, generalised knowledge to infer the correct output. 

What percent of data is not included in the training set?

Zero-shot performance = validation performance. Why? And that is, what is performance? Accuracy? 

## Design

The key is to define what is **training**. In this project we aims to investigate our methods of establishing communication protocols across different levels of environmental complexity. The simplest environment, the Referential-Numbers, is not suitable for testing in numbers that have not been seen. This is because if we add a new number to the list, if this number is the target, then the Speaker will not generate a valid message to represent it (Q_S does not have the ability to generalise to new number with all the existing ones). At the same time, the new target is not contained in the Q_L, thus it is impossible for the Listener to give a valid answer.

An ideal framework of **testing**: for testing the baseline (which is capable of communicating *any* target), the baseline should be trained on a **part of the whole T**, and test the agents using at least some unseen targets, and measure the success rate.

一个新的视角：我不把语言看作一个映射的集合，而看成某个条件概率分布。对于Speaker来说，这个条件概率就是$P(m|t)$，初识情况下这可能是某种均匀分布，代表着对于一个给定的目标t，它可能对应着任意的消息m。然而经过训练，这种条件概率分布逐渐出现了对称性破缺，使得某一个或者某一些消息的概率增大，而另一些的概率降低。那么，为什么系统会倾向于向这个方向演化呢？可以基于博弈论进行分析，也可以分析整个系统的势能函数。演化过程中是否存在着某些剪枝与合并的过程？语义空间可以扩张，同时表示空间也可以扩张，会带来什么样的影响呢？

----

平均场：一个Speaker处在一个Listeners场中，而一个Listener处在一个Speakers场中。

博弈论建模：

S的决策集：$\{s_i | s_i(t) \in L, \forall t \in T\}$, $\text{payoff}_s (s_i, \cdot) = ?$, $s_i: T \rightarrow L$

L的决策集：$\{w_i | w_i (m) \in T, \forall m \in L\}$, $\text{payoff}_l (w_i, \cdot) = ?$, $w_i: L \rightarrow T$

贡献：我这篇论文的主要研究贡献：建立并且完善一个baseline，它可以完成任务，同时可以进行任意精确度的分析。更大规模的环境、更快的收敛速度、更准确的表现、更明显的语法结构、更快的结构涌现。另一个贡献的方向是，好像真的没有人提到过，环境的适当扩张，可以刺激语法结构的形成。

我认为，语言是基于早期共识进行的演化。更加精确的语言结构的出现，可能是由于这两点原因：要么大脑迅速发育，可以识别出更加复杂的语义，这是语义空间的迅速扩张。要么是族群之间的交流更加频繁，导致现有的语言无法表示更加一般的、跨族群的语义，因此需要建立新的共识，这是约束性上的加强，要求语言向着可被对方正确识别的方向演化，而共同的语义空间保持不变。同时，在对称性破缺的意义上来讲，越是早期的成功交流，它对于这个语言的结构越具有显著的意义。

纯基于rewards，学习到的语言并不会被包括在state中，那么是否可以促成语法结构的形成？这一点需要在稍微复杂的环境中进行验证。

Bootstrap是结构涌现的基础，也是扩张环境的基础。我应该基于这个设计baseline。

某些时候，一个语句可以感知到，或者影响到整个语言；而另一些时候，一个语句的改变，可能仅仅只会影响到局部的一些语句。这种局部的影响，是否会成为结合性的诱因？？

也许我把各种势能函数想得复杂了？或许可以直接提出一些势能函数来解释对称性破缺，然后再结合我自己的实验结果进行分析？毕竟直接处理势能函数不用考虑复杂的相互作用……我也可以更快地得到相应的结果。

拓扑相似度：每一对映射，计算前端距离和后端距离，画图，进行相关性分析。

文章里面，画一些图作为概念的表示、写一些理论上的公式、写一些核心的算法、写方法的描述、画训练的结果图、分析得到的结果。

论文中，将embedding输入encoding LSTM，再输入softmax从而得到m的依据是什么？原理是什么？好处是什么？这个m再输入到decoding LSTM，为什么可以恢复原来的embedding？将两个embedding进行点积然后softmax度量概率，好处是什么？

整体结构安排：每天至少400字，而且是可以放到终稿里面的那种。为了给润色和修正留出足够的余量，每天的工作量大概要达到1000字。在全文的10000字限制条件下，我预计各个部分的字数安排为：1. 对于环境的介绍（500字）2. 强化学习以及深度强化学习（1000字）3. 对于数字的识别（1500字）4. 对于二维向量的识别（1000字）5. 对于复杂特性物体的识别（1000字）6. 成功率对比分析（500字）7. 语法结构的检测以及对比分析（1500字）8. 环境扩张对于语法结构涌现的促进作用（2000字）9. 结论以及摘要（500字）10. 必要的附录内容。以上结构一共：9500字。嗯看来这个安排还算合理。不过这么一看每天居然要写三个部分啊。诶，应该还有一个对于学习到的语言的分析部分。

一个关于……组合性的语言确实对应着系统基态的证明？在精确的编码中，如果只考虑到编码解码的成功率，那么语言编码本身其实并没有影响。然而在考虑到编码的误差的时候，组合性的语言会具有更加好的误差容忍效果。在环境系统进行扩张时，这种由环境带来的语义空间的误差是不可避免的，因此如果对编码的效率和误差容忍度同时进行约束，那么语言的组合性质将是一个必然的结果。下面我将尝试度量这个结果。首先是一个具体的例子。

你想要得到什么？

在今天几乎所有的主流语言中，整体的语义以及语法结构都是比较固定了的。但是由于互联网的普及，各个圈子中确实会出现一些新的词汇或者用法。其实我们可以看到，之所以一些词汇会被广泛的普及，就在于它们很容易被学会。这里，学会的定义大概是，可以理解它的意思并在恰当的环境中使用。这里就不可避免的带来了一个问题：由于神经的多样性，每个人对于一个词汇的理解，其实都是存在差异的。然而，语言的结合性让这种差异带来的后果被最小化了。更容易被学到的、使用中不容易出错的语言，正是语言演化的方向。

大声说、随意听；谨慎说，小心听。不同的温度会影响语言的学习效果，从而间接影响着语言结构演化。

0123这个例子中，如果进行了足够多的尝试，那么会出现特定的编码方式，比其他的要多的结果吗？还是说都是平均的？

今天先试试写1000字吧。中文英文都可以，先写出来。

---

Questions:

​    what should be the timings of the dissertation.

​        draft by the end of 3pm. - *The work should be done by every small steps, instead of a scary fixed deadline*

​        draft by Friday. - *A draft should be formulated by the end of this week.*

​        introduction: short and sweet. (formally set out of project aims) contribution (product, new environment, new application to the environment, implementation of the agents, listing of points), outline of the paper (one sentence for each chapter)

​        split the lit review: background (theory and terminology), related work (what I build on), 

​        methodology: define the environment clearly, define the methods and training details, how to do hyperparameters training. 

​        next stpes and future work. (quite important) identify limitations or some vague ideas as initial explorations. 

​    that experiments goes well, but should I describe others methods of language induction

​    main findings

​    let's have meetings next weeks

​    overall structures of the paper

---

任务：

1. 确定范围：我要做的是一系列成功的实验，获取足够支撑我结论的结果
    1. 建立成功的交流
    2. 获得一些足够复杂的语言
    3. 成功识别出语法结构，并可视化
    4. 建立一个实验性的相图，分析环境复杂度以及词汇表大小对于语言的影响
2. 确定约束：必须要成功，也就是展现出来一些特性；必须要保证完成RG的任务；今天之内拿到结果
3. 方案规划：我需要详细、清晰地描述出来自己要做的东西，然后交给AI去修改，并且获得初步的结果。然后再拿去学校电脑上跑
4. 补充：对于语言的理论分析（比如结构的存在性以及稳态的更定量的分析）、更加优化的智能体设计，这些问题暂时只做探索性的考量
5. 最终目标：论文达到70分以上



方法论：讲一讲前人的方法的认识，对它进行适当的评价和调整，并且辩证地运用到自己的问题上。



总体任务：

- 写好初稿（包括最基本的内容）
- 发给Joshua进行详细的审阅（需要4天左右）
    - 环境扩张、相似度是最基本的内容，剩下的后续再补充
    - 针对评分表中不太确定的内容进行询问
- 修改好初稿，完善绘图以及所需要的各种公式、针对反馈意见进行修改
- 对照最终的评分表以及handbook进行内容的修饰
- 使用AI对用词进行润色
- 完善参考文献
- 写video script并且录制
- 提交前的最终检查
    - Front matter
    - Appendix
    - Bibliography
    - 在Conclusion后面加上字数
    - Zip文件中加上代码运行说明
- 按时保质保量完成

---

还需要做的实验：环境扩张、相似度检验、induction。为什么可以学习到（理论分析、Q学习）、哪些环境是适用的，边界是什么。implementation of agents？