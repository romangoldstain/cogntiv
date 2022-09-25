import threading
import numpy as np
from common.stats_utils import StatsHelper
from consumer.matrix_datum import MatrixDatum

NONE_TUPLE = None, None


class MatrixWorker:

    def __init__(self, bus, vectors_per_matrix, matrix_processor):
        self.bus = bus
        self.matrix_builder = MatrixBuilder(vectors_per_matrix)
        self.matrix_processor = matrix_processor
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

            # calculate effective rate and accumulating mean and std
            actual_rate = len(matrix) / acq_duration
            self.stats.add_value(actual_rate)

            print(f'Got new matrix! rate={actual_rate} mean={self.stats.mean()} std={self.stats.std()}')
            self.matrix_processor.accept(MatrixDatum(matrix, self.stats.mean(), self.stats.std()))


class MatrixBuilder:

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
