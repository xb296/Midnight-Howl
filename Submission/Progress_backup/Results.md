# Results And Discussion

[TOC]

## Task Performance

## Problems with Policy Gradient Methods

As discussed in [Background], the referential game is a non-stationary multi-agent cooperative task. According to [Emergence of Language, Serhii and Ivan], non-stationary problems are hard due to multiple reasons. The first is the non-stationary environment means one agent's policy will determine the other agent's behaviour, then affect the reward. At the beginning of the training, both of the agents have to go through a long period of random trial before finally reach a common protocol. This makes the trajectories have a lot of non-usable history, leads to a high variance of the future rewards. The second is large number of possible messages also leads to high variance estimates of the gradients. Because policy gradient methods use a the expectation of the future rewards to derive the gradient, high variances compromises the accurate estimation and leads to slow convergence of the algorithm. 

We propose a novel way to mitigate this is by firstly train the agents in smaller environments, than expand this environment to more complex ones by multiple steps. By having a clear parameterised environmental setting, this can be achived easily. In smaller environments, the required messages are fewer then in the large environments. Besides, in these small environments, the exploration costs less interactions because the targets and possible messages spaces are smaller. This can make the expectation calculation more accurate because of less variance and deviation from the mean value.

Another problem with policy gradient methods is premature convergence. This is a feature of many policy gradient methods, but I've not learned. (Performance)During tranining, the learning curve stuck on a plateau, suggesting the agents are stuck in a local minima and cease to explore any more. What reflected on the learned language is the speaker continuously produces the same messages for several (or even all of) the targets, and the listener produces the same choice for almost all of the messages.



## Grammatical Structures

The new 