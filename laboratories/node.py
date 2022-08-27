import json
import numpy as np
import matplotlib.pyplot as plt

from signal_information import *


class Node(object):

    def __init__(self, node):
        self._label = node['label']  # string
        self._position = node['position']  # tuple
        self._connected_nodes = node['connected_nodes']  # list of strings
        self._successive = {}  # dict of Line

    # label
    def label(self):
        return self._label

    # pos
    def position(self):
        return self._position

    # conn nodes
    def connected_nodes(self):
        return self._connected_nodes

    # succ
    def successive(self):
        return self._successive

    # PROPAGATE
    def propagate(self, signal_information, busy=False):
        path = signal_information.path()
        if len(path) > 1:
            line_label = path[0] + path[1]  # the 1st and the 2nd element of path
            line = self.successive()[line_label]
            signal_information.next()
            signal_information = line.propagate(signal_information, busy)
        return signal_information
