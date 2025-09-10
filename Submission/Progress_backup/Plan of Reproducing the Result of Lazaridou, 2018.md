# Plan of Reproducing the Result of Lazaridou, 2018

Basic environmental setup:

- Python 3.11
- PyTorch

Ensure reproducibility:

- fixed random seed

Tracing and debugging of neural networks:

- using tensorboard to visualise rewards

## Algorithmatic settings

Hyperparameters:

Network parameters:

Policy gradient methods. The goal of the algorithm is not to achieve high topological similarity, or compositionality, or explicit grammar. The goal is to establish successful communication, without explicitly specify rules for the messages. What is hypothesised is language structures will emerge from **successful** communications. 

Through some global settings, I also want to link **energy of languages** to the **objective function** of the policy gradient methods.

Objective function: expected value of the total undiscounted reward of the current policy. It represnets a direction towards successful communication.  

Dataset:

Each object is a 594-dim symbolic vector.