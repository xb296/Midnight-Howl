# import necessary libraries
import numpy as np

# define a class for the environment
# which is a dataset of spacial vectors
class Environment:
    def __init__(self):
        self.dataset = []

        # generate a dataset of spacial vectors
        # for example, 2D vectors
        for j in range(2):
            # for example, there are 2 clusters of vectors
            # each cluster has 100 vectors
            # the vectors are generated from a normal distribution
            # the mean of the normal distribution is different for each cluster
            # the variance of the normal distribution is the same for each cluster
            # the variance is 1
            
            for i in range(100):
                if j == 0:
                    # vector is a random 2D vector centered at (20, 0)
                    # the distribution is normal with mean (20, 0) and variance 1
                    vector = np.random.normal(loc=[20, 0], scale=1, size=2)
                    self.dataset.append(vector)
                else:
                    # vector is a random 2D vector centered at (-20, 0)
                    # the distribution is normal with mean (-20, 0) and variance 1
                    vector = np.random.normal(loc=[-20, 0], scale=1, size=2)
                    self.dataset.append(vector)

    def get_dataset(self):
        return self.dataset
