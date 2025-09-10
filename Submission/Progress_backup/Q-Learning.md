# Q-Learning

[TOC]

Two agents have to interact with each other to invent their own language. 

Target space: $T = \{0, 1, 2, 3\}$. 

Vocabulary: $V = \{a, b, c, d\}$. 

One agent is the **Speaker**, it observes a number $t \in T$, then outputs a message $m$. Thus, the Q table of Speaker is $Q_S(t, m)$.

State space $S_S$ = $T$. Action space $A_S = V^{l_m}$, where $l_m$ is the message length (fixed length).

The other agent is the **Listener**, it takes $m$, as well as two choices $\{t, t'\}$, where $t, t' \in T, t' \neq t$, and outputs an answer $w$. One question to think about here, is $(t, t')$ and $(t', t)$ are different states to prevent the agents to learn fixed position correspondence.

State space $S_L = \{(m, t, t', \dots)\}$. Action space $A_L = \{t, t', \dots\}$ which depends on the state.

The Q table of Listener is $Q_L(\{m, t, t'\}, w)$.

The reward $r = 1$ if $t = w$, otherwise $r = 0$.

Episode: one full episode consists of only one attempt at the communication.

Conventional update rule:
$$
Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma \max_{a'} Q(s′,a′) - Q(s,a)]
$$
Becomes: 
$$
Q(s, a) \leftarrow Q(s, a) + \alpha [r - Q(s, a)]
$$
It stablises at $Q(s, a)$ if $r = Q(s, a)$.

After each update, both of the Q tables will converge.

## Complexity Analysis

Let's think about this problem with regard to environmental complexity. 

Assume the length of the message is fixed to be $l_m$, the number of Listener's choices is $n_c$ (including the target).

### Space Complexity

The size of $Q_S$ is $|T| \times |V|^{l_m}$

The size of $Q_L$ is $|V|^{l_m} \cdot |T| \cdot (|T| - 1) \times n_c$

 $Q_L \sim 10^6$, if $|V| = 10$, $l_m = 3$, $|T| = 18$, and $n_c = 3$. 

Thanks! This code works for me, but let's extend it to be more challenging: I want to test if this method supports 1,000,000 states! Specifically, I need 10 symbols ('a' to 'j'), the length of each message should be 3, there will be 18 targets (0 to 17), and the number of Listener's choices is 3 (not 2 in the current case). 

### Time Complexity

How many interactions is required for the convergence? 

## Performance Analysis

This shouldn't be a difficult task, but what I observed is: 

- after 55000 episodes, success rate rised up to 93.5%
- 200000 episodes of training still can't make the final commmunication success rate to be 100%

### Analysis

This is quite counterintuitive. Some questions I have to investigate:

- what determines the convergence rate
- what determines the success rate during training
- how to make training quicker and more accurate
- why does the emergent protocol not function perfectly

The problem is because of the way Listener finds its best choice for each of the target. The program chooses one possible message (which is fine), tests each target (), makes a random state, then counts the number of each guess, find the corresponding target. 如果t是正在被测试的目标，那么Q表可以给出正确的选择。然而，对于那些不是'out of scope'的映射，比如已经建立了3-a的映射，那么对于同样的消息a，如果状态中出现了3，那么可以正确选出这个3。但是我们这里测试的是随机情况，(a, 0, 1)这些状态并不能给出有效的信息，因此选择就是随机的。这种情况下，随机选出的target的数量，可能是会多于这个正确的3的数量的。以下就是一个案例：

```
[Speaker's Learned Policy]
Target -> Chosen Message
  0    ->    'b'
  1    ->    'c'
  2    ->    'd'
  3    ->    'a'

--- (part of) Listener's Full Q-Table ---
State (Msg, C1, C2)       | Q(Action=C1)    | Q(Action=C2)   
------------------------------------------------------------
('a', 0, 1)               | *0.4894*        |  0.4220        
('a', 0, 2)               | *0.4773*        |  0.3906        
('a', 0, 3)               |  0.0001         | *0.9984*       
('a', 1, 0)               |  0.3497         | *0.6407*       
('a', 1, 2)               | *0.5238*        |  0.3753        
('a', 1, 3)               |  0.0000         | *1.0000*       
('a', 2, 0)               |  0.4172         | *0.5078*       
('a', 2, 1)               |  0.3614         | *0.5936*       
('a', 2, 3)               |  0.0474         | *0.9683*       
('a', 3, 0)               | *0.9546*        |  0.0050        
('a', 3, 1)               | *0.9612*        |  0.0081        
('a', 3, 2)               | *0.9992*        |  0.0050 

message: a, target: 0, best choice: 0
message: a, target: 1, best choice: 0
message: a, target: 2, best choice: 3
message: a, target: 3, best choice: 3

[Listener's Learned Policy]
Message -> Interpreted Target
  'a'    ->    0
```

从上述的Q表中可以看出，对于消息a，如果3出现在candidates中，那么Listener是可以正确选出的。然而，由于干扰项的存在，这个“总结”的过程并不正确。0和3都出现了两次。由于它要选择出现次数最多的数字，因此就选择了0。

Therefore, the **testing** process should be: select each target, feed into the Speaker, and use this target with some random targets to test the Listener. That is to say, the Listener is not capable of tell the meaning of a single message, without the true target.

Limitation: 

## Next Step

Since this is working for the simple environment, how about more complicated ones?

