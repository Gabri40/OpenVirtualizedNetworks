import node
import signal_Information

class Line(object):
    def __init__(self, line_dict):
        self._label = line_dict['label']
        self._length = line_dict['length']
        self._successive = {}  # dict [Node]
        self._state = ['free','free','free','free','free','free','free','free','free','free']

    # label
    def label(self):
        return self._label

    # len
    def length(self):
        return self._length

    # succ
    def successive(self):
        return self._successive

    # state
    def state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    # LATENCY GEN
    def latency_generation(self):
        latency = self._length / (2 * (10 ** 8) * 2 / 3)
        return latency

    # NOISE GEN
    def noise_generation(self, signal_power):
        return 1e-9 * signal_power * self.length()