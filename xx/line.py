import json
import numpy as np
import matplotlib.pyplot as plt

from node import *
from signal_information import *


class Line(object):
    def __init__(self, line_dict):
        self._label = line_dict['label']
        self._length = line_dict['length']
        self._successive = {}  # dict [Node]
        self._state = ['free'] * 10

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

    # PROPAGATE
    def propagate(self, lightpath, busy=False):
        # update noise and latency of siginfo
        latency = self.latency_generation()
        lightpath.add_latency(latency)
        signal_power = lightpath.signal_power()
        noise = self.noise_generation(signal_power)
        lightpath.add_noise(noise)

        if busy:
            ch = lightpath.get_channel()
            self._state[ch] = 'occupied'

        node = self.successive()[lightpath.path()[0]]
        lightpath = node.propagate(lightpath, busy)
        return lightpath
