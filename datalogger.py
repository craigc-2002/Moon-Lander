class DataLogger:
    def __init__(self):
        self._datalog = []

    def log(self, time, data):
        self._datalog.append([time, data])

    def get_log(self):
        data_out = [[], []]
        for i in range(len(self._datalog)):
            data_out[0].append(self._datalog[i][0])
            data_out[1].append(self._datalog[i][1])

        return data_out

    def clear(self):
        self._datalog = []
