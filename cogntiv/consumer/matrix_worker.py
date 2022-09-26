import threading
import numpy as np
from common.stats_utils import StatsHelper

NONE_TUPLE = None, None


class MatrixWorker:

    def __init__(self, bus, vectors_per_matrix, matrix_analyzer, consumer):
        self.bus = bus
        self.matrix_builder = MatrixBuilder(vectors_per_matrix)
        self.matrix_analyzer = matrix_analyzer
        self.consumer = consumer
        self.running = False
        self.stats = StatsHelper()

    def start(self):
        if self.running:
            return

        self.running = True
        th = threading.Thread(target=self._poll_and_process, daemon=True, args=())
        th.start()
        return th

    def stop(self):
        self.running = False

    def _poll_and_process(self):
        while self.running:
            in_vector_msg = self.bus.get()
            matrix, acq_duration = self.matrix_builder.accept(in_vector_msg.data, in_vector_msg.received_at)
            if matrix is None:
                continue
            # else - we got ourselves a brand-new matrix!

            # Calculate effective rate, mean and std
            actual_rate = len(matrix) / acq_duration
            self.stats.add_value(actual_rate)

            # Create artifacts for the consumer - stats and analytics dictionaries.

            print(f'New matrix acquired @ {actual_rate}msg/sec')

            rate_stats = {
                'rate': actual_rate,
                'rate_mean': self.stats.mean(),
                'rage_std': self.stats.std()
            }
            # TODO: consider using ordered dictionary, as order of iteration is not guaranteed.

            analytics = self.matrix_analyzer.analyze(matrix)

            self.consumer.accept(rate_stats, analytics)


class MatrixBuilder:
    """
    Constructs matrices based on incoming vectors.
    The class uses backing array in a cycling manner (not thread safe)
    """

    def __init__(self, vectors_per_matrix):
        self.backing_array = [None] * vectors_per_matrix
        self.index = 0
        self.received_at_min = -1

    def accept(self, vector, received_at):
        self.backing_array[self.index] = vector
        if self.index == len(self.backing_array) - 1:
            # Reach target vector count. Create new matrix and reset state.

            out_matrix = np.matrix(self.backing_array)
            acquisition_time = received_at - self.received_at_min

            # reset state
            self.index = 0
            self.received_at_min = -1

            return out_matrix, acquisition_time

        if self.index == 0:
            self.received_at_min = received_at

        self.index += 1
        return NONE_TUPLE
