
class MatrixAnalyzer:
    def __init__(self):
        pass

    def analyze(self, matrix):
        return {
            'mean': matrix.mean(0)[0].tolist()[0],
            'std': matrix.std(0)[0].tolist()[0]
        }
    # TODO: consider using ordered dictionary, as order of iteration is not guaranteed.
