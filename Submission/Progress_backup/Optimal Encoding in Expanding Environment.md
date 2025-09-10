# Optimal Encoding in Expanding Environment

Statement: this encoding has some minimal value in an energy term. If the global reward or constraint can be converted to the potential term, then it is very likely that the language will evolve towards this optimal encoding.

In an expanding environment, where all of the agents have learned the previous environment. What is an environment? A metric space. What is an expanding? A mapping, where f(p) = p, if p s in the original environment, while d(f(p), f(p')) > d(p, p'), for all p != p'. f(p) is also a metric space.

An example: 0, 1, 2, 3 -> a^- and a^+, expanding rate = 2. the optimal solution is adding two new words. Why is it optimal? Because for every a, if ax is changed to ay, then the error can be bounded within the local area of a and not affecting other domains. 

My hypothesis is, optimal encoding in an expanding environment, is proportional to the log of environmental complexity. 

A data point is a trigger for all the other subsequent learning.

It is very interesting that if the emergent protocol are optimal, and how can it be optimal in the environment.



In this part, I want to investigate the relationship between global environmental constraints and individual influence it has on every pair of mappings.

Let's think about an environment with 10 distinctive features. A tolerance rate is 10%, which means either:

- the accuracy of the entire language is 90%
- for a given message, it has a 90% chance to refer to the correct object
- in all the constructed mappings, 10% of them can be ambiguous

I think the third one makes the most sense as it aligns with my intuition. In a total of 10 mappings, 9 of them should be correct. 

**Assumptions on the nature of the speaker (supported by papers?)**: 

- 尽量选择已经存在的单词，避免创造新词汇，除非这个概念确实非常新，不能用已有的词汇或者词汇的组合来表达
- 尽量造成少的误解
- 尽量使用短句子

**Assumptions on the nature of the listener**: 

- 接受信息之后要努力进行模式的匹配
- 如果出现了语义的模糊，那就随机猜测一个结果

但是以上是一些启发式的概念，与真正agent的行为似乎暂时无法建立联系。现在我们来处理这个问题：如何调整MDP的设置，使得我们的agents可以展现出上述的行为？

**policy gradient方法**包含一系列对于更新策略的要求。这些更新策略的详细过程，其实需要对我们agents的设计具有很多的指导作用。

回顾一下Q学习的更新规则，它通过列表的方式，列出并且跟随着每一次交互，更新对于每一个状态和动作下最终奖励的期望。那么在我们的项目中，需要？来使得语言结构涌现出来？

采样……如何有效地利用曾经的经验？

我能不能借鉴iterated learning的方法，用双向的NN来指导智能体，从而实现稳态控制？

**今天的目标**：把那个扩展实验做成功。

（我好像很害怕出现实际的进展，可能是因为出现进展之后又会带来很多新的问题，而我害怕这些问题？从而一直避重就轻？）



嗯，把一堆相关的文献放到Gemini里面，然后问是否有关于Speaker特性的相关讨论。如果能找到原文对应的位置并且精准总结出来的话，那还是不错的。