import collections
from statistics import mean


class Symbol:
    def __init__(self, short_window, long_window):
        self.fifo = collections.deque(maxlen=long_window)  # long_window + 1 ????????
        self.long_window = long_window
        self.short_window = short_window
        self.last_signal = 0
        self.position = 0

    def update(self, value):
        self.fifo.append(value)
        self.strategy()

    def strategy(self):
        if len(self.fifo) == self.long_window:
            windows = self.calculate_windows()
            signal = 1 if windows[0] > windows[1] else 0
            self.position = signal - self.last_signal
            self.last_signal = signal
            print(self.position)

    def calculate_windows(self):  # decimal type ?????? for precision
        return mean(list(self.fifo)[-self.short_window:]), mean(self.fifo)

    def return_price(self):
        return self.fifo[-1]