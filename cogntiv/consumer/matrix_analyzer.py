class MatrixAnalyzer:
    """
    Accepts collected matrices and returns calculated analytics artifacts.
    """

    def __init__(self):
        pass

    def analyze(self, matrix):
        return {
            'mean': matrix.mean(0)[0].tolist()[0],
            'std': matrix.std(0)[0].tolist()[0]
        }
    # TODO: consider using ordered dictionary, as order of iteration is not guaranteed.
    # TODO: I bet there is a better way to do the above
