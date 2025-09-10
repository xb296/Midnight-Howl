# Referential Grid
Since Referential-Vector failed due to high environmental compelxity, I decide to switch to this less complicated version.

In this world, the only variable is the environmental complexity. In the gridworld environment, each grid is represented by a vector.

> This approach is a mitigation between discrete grids and continuous 2D vector space. When the grid is divided infinitely, each 2D vector will be contained in exactly one box. Thus, the infinitely condensed grid is equivalent to 2D vector space.

This environment also raises another fundamental question: will the listener effectively learn based on its memory? I mean, if it learns a vector x is represented by a word 'abb', when seeing another vector y which is close to x, will it guess y is represented by a word similar to 'abb'?

Rewards:
Reward function in the real world may be way more complicated than we expect.

Effects of Exploration:

The implicit tradeoff of "exactivity" and "ease of speaking"



We remove the 'two' sets of points. Just one in this experiment.

Is the language's composibility a result of
- expanding environmental complexity throughtout training
- enhancing ability of congnition during evolution

The idea of alpha-beta annealing:
Train Speaker first, then listener, then speaker again, then listener...



Compositionality:
Think about the pumping lemma: looping/recursive structure in a language.
aabb
aaabbb...

## Design


## Questions
1. If we have a string of length 3, how many possible tree structures when traversed using mid-order?
2. Does language emerge with pre-ordered tree structure?
3. Can we effectively communicate with emerged language to agents, to figure out the meaning of the language?
4. How to transfer from string made up with letters to sentences made up with words
5. Is structure a intric feature of language, or human mind?
6. Does neural networks have memory like human mind, to affect generalability?

## Problem
Here is a problem making the training behaves badly. The key is I have no idea how neural networks generialise agreed protocols and tries to make new agreement. 

Is the neural network deterministic? If it is, then for a given input, it always generates the same output.

For the speaker's trajectory, it is like: 
target1, str1, (target'1), reward1;
target2, str2, (target'2), reward2;
...

For the listener's trajectory, it is like:
(target1), str1, target1', reward1;
...

How do NNs update? Speaker's performance depends on listener, while listener's performance depends on speaker. Circular dependancy?

