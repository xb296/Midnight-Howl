# Agent Analysis on Possible Emergent Properties

In RL, almost everything comes down to E[future rewards], am I right? Thus, the future rewards must be influenced by each agent's actions and rewards. However, in this project, both of the agents are changing their policies. Here, we first fix the policy of the Listener, analysis what is the optimal policy of the Speaker. If the Listener is fixed, then for a given message and a set of targets, it will always give a fixed answer t_m. Afterall, this is the goal of a perfect Listener: always choose a target in the presence of a certain message. So the Speaker's policy will converge to (t, m) if the Listener gives m under t. All other (t, m') will be zero, if (m' _) will not be t for the Listener. 我怎么想到了语义分离现象？如果说对于Listener来说，两个消息是无法区分的，那么Speaker也无法学习到它们之间的区别。

For the listener, if the Speaker is fixed (that is, for a given target, it will always generate a message m), (m, (t, ...)) will be 1 if it chooses t. 

确实，先研究固定长度的消息，毕竟不定长的语言，是所有定长语言的集合。



参数是如何影响收敛速度的？再说。



既然只有一个episode，那么我为什么要用RL？这可能需要结合别人的方法来进行讨论。不过这个问题似乎比较棘手。我初步的回答是，语言是存在相互作用的，一个语义-表示对的改变，势必会影响到另一个语义-表示对。**这个问题**，好好想想能不能用MC来做。我生成一大堆的语义表示对，投放到环境中。那么这就是一个语言。但是它是不是最好的呢？我们可以用能量函数进行评判。下面的问题就是，如何打分呢？然后就是，最高分的语言，是否会具有一个人类语言的某些特性。我认为，对于一个好的语言，一定是具有简洁性与表达性的。

