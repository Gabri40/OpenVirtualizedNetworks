from .signal_information import *


class Node:
    def __init__(self, name, att_dic):
        self.label = name
        self.position = tuple(att_dic["position"])
        self.connected_nodes = att_dic["connected_nodes"]
        self.successive = {}  # line dict

    # label
    def get_label(self):
        return self.label

    def set_label(self, label):
        self.label = label

    # position
    def get_position(self):
        return self.position

    def set_position(self, pos):
        self.position = pos

    # connected nodes
    def get_connected(self):
        return self.connected_nodes

    def set_connecting(self, nodes):
        self.connected_nodes = nodes

    # successive
    def get_successive(self):
        return self.successive

    def add_successive(self, succ):
        self.successive[succ.get_label()] = succ
