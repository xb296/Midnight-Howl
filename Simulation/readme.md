# Simulation
Before implementing RL agents, analytical and simulation results are crucial for a proof-of-concept. In this sub-project, a phase diagram is disirable for showing the conditions of language emergence. 

Two parameters of the whole system are:
- size of vocabulary: v
- environment complexity: c

For a given setting (v, c), the system should be one of two possible configurations:
- grammatical structures emerged
- no grammatical structures emerged

Thus, whether a language can emerge can be determined by values of (v, c).

## Prerequisites
```shell
# install networkx
conda activate study
pip install networkx
```

## Global metrics for language
To determine if a communication protocol is indeed a language, there should be some global metrics for making quantitative determination.

However, after some investigation on existing literature, there seems no well-established metrics for tesing grammars in a language. So I have to come up with something new by myself. Let's think about some examples first, and then maybe it will become more clear how to draw a dividing line of telling if something is a language.

### Examples
non-language: random combination of words
language: CFG generated language; CNF generated language

Then the most significant difference is that languages have **a set of pre-defined grammatical rules** for generating sentences.

## Detecing grammars
I plan to use some bayesian tools as metrics for 'possible' emergent grammars. 

Having a set of data, in which the specific data type of the data is not important, I hope to build a discriminant model to make a probabilistic judgment based on the data. Now I extract data one by one from the original dataset and input it into this discriminant model. This discriminant model has no prior assumptions. It learns purely from the data. For each piece of input data, it can not only make a probabilistic judgment on all the data that has been input, but also obtain information and improve it from the new data. The more data is input, the stronger the modeling ability of this model is. For this model, I expect to get this result: if the data does have some kind of regularity or distribution, then as the data is continuously input, the probability judgment will get closer and closer to 1; on the contrary, if this set of data does not have any internal regularity, then as the data is input, the probability judgment will not increase significantly, and will eventually gradually approach 0. I do not want to use neural networks for modeling. It is best to use an interpretable method based on probability theory to build this model. In short, I want this model to autonomously identify hidden structures in the data, and if there is indeed structure in the data, it will become more and more "convinced" as more data is input; and if there is no structure in the data, then after enough data is input, its judgment will approach 0.

The following explanation is given by Gemini.
Scope: sequential learning, pattern detection, model selection

Bayesian model comparison, Bayesian hypothesis testing



The following is a demonstration.