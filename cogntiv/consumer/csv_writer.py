import csv
import datetime


class CSVWriter:
    """
    Flushes collected and calculated artifacts (rate stats and analytics) into CSV file.
    """

    def __init__(self):
        filename = datetime.datetime.now().strftime('%Y%m%d_%H%M_%S_results.csv')
        # filename = 'debug_results.csv''
        self.file = open(filename, 'w', newline='')
        self.writer = csv.writer(self.file)
        self.rows = 0
        # might throw
        print(f'Writing to result file: {filename}')

    def accept(self, rate_stats, matrix_analytics):

        # Write header every 100 rows
        if self.rows % 100 == 0:
            header = []
            header.extend(rate_stats.keys())
            for k in matrix_analytics.keys():
                header.extend(list(map(lambda vv: f'{k}_{vv}', [*range(1, len(matrix_analytics[k]) + 1)])))
            self.writer.writerow(header)

        # write data

        row = []
        row.extend(rate_stats.values())
        for v in matrix_analytics.values():
            row.extend(v)

        self.writer.writerow(row)
        self.rows += 1

    def close(self):
        self.file.close()
        # TODO: more care here, please
