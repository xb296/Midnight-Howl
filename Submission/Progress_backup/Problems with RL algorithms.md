# Problems with RL algorithms

According to [Emergence of Language, Serhii and Ivan], 

1. large number of possible messages leads to high variance estimates of the gradients
2. Non-stationary environment

How to overcome this:

- expanding environment
- Iterative interactions

## Stationary

My understanding: what the agent does can affect the environment itself. The mountain car problem is stationary, because the valley stays in a fixed shape. The game of Go is non-stationary, what the player does can affect the opponent's behaviour, thus affecting the environment (the game board). 

In a stationary environment, the **MDP** model (reward functions and transition probabilities) remain constant or change very slowly compared to the learning agnent.

This requires a clear definition of my problem. 

## MDP

状态是什么？对于S来说，状态是它接收到的目标向量。对于L来说，它的状态是S输出的字符串。嗯……更加详细地说，这是它们的observation。那么observation和状态在这个问题中存在显著区别吗？我认为并不。我认为，状态是从客观角度来看的，是我们对于**agent与环境之间的关系**的一种刻画。而observation是智能体自身比较主观的，对于环境的观测。在目前这个问题中，我认为它们是等同的。

再看状态转移函数：下一个状态的值，与当前状态……无关？确实可以说是无关的。



## Traditional approaches

Neural iterative learning

## Tabular method and grid world environment

This environment is conventional and the most important feature about it is it has geometrical structures.

## One Advantage of RL: Interactions

Statistical models of the language evolution depends on individual interactions, which is the idiom of RL. In this setting, although there are only two agents, but their numerous interactions can lead to emergence of patterns. The idea is such: pattern will emerge when mumtiple 'spins' interact with each other (but not necessarily at the same time). A spin is such a pair: s <-> m. Speaker provides encoding in the direction of m s <- m, while listener provides decoding in the direction of s -> m.

But how can we model the interactions between spins to be interactions between agents? A spin will come up or disappear. When it comes up, it will interact with all its neighbouring spins, which is encoded in the neural network. The result is a change of the global energy of the language, and this change should be differentiable.

Global parameters: environmental complexity and vocabulary acts as the temperature: high temperature means spins are more random, just like the case of complex environment, high tolerance and low vocabulary. In a simple environment, low tolerance and low vocabulary size, sentences are more uniform, just like in a low temperature.(Tolerance is the negative of constraints) The expanding rate may also be a parameter of the language. A fast expanding meaning space leads to more strict constraints of individual spin pair and low exploration, shorter range influence. 

## Premature Convergence

This is a feature of many policy gradient methods, but I've not learned. (Performance)During tranining, the learning curve stuck on a plateau, suggesting the agents are stuck in a local minima and cease to explore any more. What reflected on the learned language is the speaker continuously produces the same messages for several (or even all of) the targets, and the listener produces the same choice for almost all of the messages.

The principle reason for this is: ? (this may be beacuse of some not successful accumulated interactions?) Should be more familiar with PPO, especially the inner workings.

Solution: careful debugging of the neural network, or hyperparameter tuning, or reproducing results with the paper (1st priority).

https://www.reddit.com/r/reinforcementlearning/comments/xatv06/how_to_avoid_early_convergencehow_to_encourage/

