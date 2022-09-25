class MatrixAnalyzer:

    def __init__(self):
        pass

    def accept(self, matrix):
        std = matrix.matrix.std()
        mean = matrix.matrix.mean()

        print(f'mean={mean} std={std}')
