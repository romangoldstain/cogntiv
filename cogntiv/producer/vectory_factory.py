import numpy as np


class VectorFactory:
    """
    Facility for creating normal distribution samples vectors.
    """

    def __init__(self, vector_length=50):
        self.rng = np.random.default_rng()
        self.vector_length = vector_length

    def create(self):
        return self.rng.standard_normal(self.vector_length)
