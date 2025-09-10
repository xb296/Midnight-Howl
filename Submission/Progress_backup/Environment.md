# Environment

An important feature of the project is the environmental complexity. Thus, we present () environments here as examples, and analysis their complexity.

The first category is numerical environment, where each feature is represented by a scalar. Numerical features have the advantage of obvious, graphical and measurable. In our project, we investigate integer values, i.e. $T = \{0, 1, 2, \dots, n\}$, and the environmental complexity is $O(n)$. The complexity is controlled by different values of $n$, and difference of two different targets is measured by $|t_1 - t_2|$. The reason we choose this environment also includes its eeasily graphed semantics. However, this kind of environments lack practical use, so we extend it to be vectorised environment.

In a vectorised environment, each target is a vector of dimension $n$. Vectors have the ablility to represent more complicated features compared to scalars while also preserves geometrical features and measurable. In this project, three kindes of vectors are studied: geometric points, attribute encodings, and embeddings. 

数字 - 欧氏空间中的向量 - 流形上的点 - 非欧式空间中流形上的点。

In the experiments, we used 2D grids as a representation of 2D vector field. The grid is a $a \times a$ square with density $d_s$. Thus, the number of all vectors in the grid can be controlled by the density. It is a natural extension to the scalar environment, which is of 1-dimension. 

One-hot embeddings of vectors are also used in the experiments. These are used to represent attributes of objects. This has the power of representing complicated objects while still preserves explainablilty. 

For example, if we have 10 objects, then each object has 3 different attributes. Then 

Then, we have a novel maze environment, which is represented by concatenated vectors. The goal of the two agents is to escape the maze as soon as possible. (intermediate goals, reward shaping etc.) This can exisibits how the agents can learn to communicate about navigation in a environment, and test the definition of environmental complexity. For the agent, the observation should be an grey-scale image, and the agent is represented as a dot. (Follow the literature?)



Embeddings are vectors produced by neural networks to represent cerntain objects. 

The goal of all these settings is to demonstrate that if the target space has some geometrical properties, then the geometrical property can affect the learned language, thus form a basis of compositionality. 

