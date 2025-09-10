# Theoretical Analysis on Language Expressivity

The idea here is, we assume external pressure can leads to emergence of compositionality. Then, where is the critical point of this change? How far is it, that our findings from this critical point? It is not very relevant to the project, but is extremely interesting to me.

For an abstract language, there is no alphabet (i.e. we don't think about how letters composite words).

Alphabet/Vocabulary: $\Sigma$

Sentence/String/Message: $m \in \Sigma^*, s.t. \forall m, 0 \leq |m| \lt \infty, m_i \in \Sigma $

Language: $L \sub \Sigma^*$

Compositionality: $|L| \gt |\Sigma|$?



For constant length messages, $|M| = |V|^{L_s}$ is the critical point. If the meaning space $|M|$ is larger, then it is strictly non-acceptable for the language to express all meanings. Plot a graph of $\log |M|$ and  $|V|$.

![image-20250815173220630](/Users/xiaotongbai/Documents/Research/Dissertation/Progress Articles/image-20250815173220630-5275557.png)

对于另一种非结合的语言，那么它应该具有某种“识别性”：语义与词汇的位置无关，而只与词汇的出现相关。此时，aa=a，ab=ba。

Critical point: 
$$
|M| = \sum_{i = 1}^{L_s} \binom{|V|}{i} \leq \sum_{i = 1}^{|V|} \binom{|V|}{i} = 2^{|V|} - 1
$$
Is there any good approximation of the first summation? 