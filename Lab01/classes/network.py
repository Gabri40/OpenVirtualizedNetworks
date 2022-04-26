from .signal_information import *
from .node import *
from .line import *
import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


class Network:
    def __init__(self, json_path):
        self.json_path = json_path
        self.nodes = {}  # {"label": node_object}
        self.lines = {}

        # salva gli attributi necessari dal file json in un dict
        # brutto perche il dizoinario convertito da json non ha un valore label -> crea un second dic
        nodes_info_dict = json.load(open(json_path))
        for i in nodes_info_dict:
            self.nodes[i] = Node(i, nodes_info_dict[i])

        # per ogni node ! qui itera in dic obj
        # per ogni node collegato ! qui itera in lista str
        # crea nome linea
        # crea obj linea e add a dic
        for node in self.nodes.values():
            for con in node.get_connected():
                linename = node.get_label() + con
                self.lines[linename] = Line(linename, node.get_position(), self.nodes[con].get_position())

    def print_nodes_info(self):
        for i in self.nodes.values():
            print(i.get_label())
            print(i.get_position())
            print(i.get_connected())
            print(i.get_successive())
            print()

    def print_lines_info(self):
        for i in self.lines.values():
            print(i.get_label())
            print(i.get_lenght())
            print(i.get_successive())
            print()

    def get_lines_list(self):
        return self.lines.keys()

    def get_nodes_list(self):
        return self.nodes.keys()

    # set the successive attributes of all
    # the network elements as dictionaries (i.e., each node must have a dict
    # of lines and each line must have a dictionary of a node);
    def connect(self):
        # connect nodes
        for node in self.nodes.values():
            for line in self.lines.values():
                if line.get_label()[0] == node.get_label():
                    node.add_successive(line)

        # connect lines
        for line in self.lines.values():
            for node in self.nodes.values():
                if line.get_label()[1] == node.get_label():
                    line.add_successive(node)

    # given two node labels, this function re-
    # turns all the paths that connect the two nodes as list of node labels.
    # The admissible paths have to cross any node at most once;
    def find_path(self, start, end, path=[]):
        path = path + [start]  # aggiunge elemento corrente al path
        paths_list = []
        if start == end:
            return [path]  # quando start==fine path completo

        for node in self.nodes[start].get_connected():  # per ogni nodo adiacente al nodo corrente
            if node not in path:  # se non e gia stato considerato in questo path
                subpaths = self.find_path(node, end, path)  # chiama ricorsivamente find_path con start il nodo corrente

                for subpath in subpaths:
                    paths_list.append(subpath)  # aggiorna paths_list

        return paths_list

    # propagate the
    # signal information through the path specified in it and returns the
    # modified spectral information;
    def propagate(self, siginfo, path):
        siginfo.set_path(path)
        power = siginfo.get_sig_power()
        for i in range(len(path) - 1):
            line = path[i] + path[i + 1]
            siginfo.add_noise(self.lines[line].noise_generation(power))
            siginfo.add_latency(self.lines[line].latency_generation())

    # draw the network using matplotlib
    # (nodes as dots and connection as lines).
    def draw(self):
        for i in self.nodes.values():
            plt.plot(i.get_position()[0], i.get_position()[1], marker="o", linestyle="none", color="green",)
            plt.annotate(i.get_label(), (i.get_position()[0], i.get_position()[1]))
        for i in self.lines.values():
            plt.plot([i.get_start()[0], i.get_end()[0]], [i.get_start()[1], i.get_end()[1]], color="green")
        plt.show()
