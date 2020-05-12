import collections
from statistics import mean


class Macs:
    """ Moving Average Crossover Strategy """

    def __init__(self, short_window, long_window):
        """ short_window - short window length
            long_window - long window length """
        self.price_ask = collections.deque(maxlen=long_window)
        self.long_window = long_window
        self.short_window = short_window
        self.last_signal = 0
        self.position = 0

    def update(self, ask, bid):
        self.price_ask.append(ask)
        self.strategy()

    def strategy(self):
        if len(self.price_ask) == self.long_window:
            windows = self.calculate_windows()
            signal = 1 if windows[0] > windows[1] else 0
            self.position = signal - self.last_signal
            self.last_signal = signal

    def calculate_windows(self):
        return mean(list(self.price_ask)[-self.short_window:]), mean(self.price_ask)
