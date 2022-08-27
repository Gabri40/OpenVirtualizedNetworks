import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from node import *
from signal_information import *
from line import *
from connection import *


class Network:
    def __init__(self, json_path):
        self._nodes = {}
        self._lines = {}
        self.build_nodes_lines_dict(json_path)
        self._connected = False
        self._weighted_paths = None

    # udes in init
    # builds nodes and line as dict entries from json file : json example:
    # "A": {
    #     "connected_nodes": ["B","C","D"],
    #     "position": [-350e3,150e3]
    # }
    def build_nodes_lines_dict(self, json_path):
        node_json = json.load(open(json_path, 'r'))
        for node_label in node_json:
            # build single nodes objects and add them to own dict
            node_dict = node_json[node_label]
            node_dict['label'] = node_label
            node = Node(node_dict)
            self._nodes[node_label] = node
            # build lines objects
            for connected_label in node_dict['connected_nodes']:
                line_dict = {}  # empty dic
                line_label = node_label + connected_label  # build line label
                line_dict['label'] = line_label  # set line label
                node_position = np.array(node_json[node_label]['position'])  # first node pos
                connected_node_position = np.array(node_json[connected_label]['position'])  # second node pos
                line_dict['length'] = np.sqrt(np.sum((node_position - connected_node_position) ** 2))
                # print(line_dict['length'])
                line = Line(line_dict)
                self._lines[line_label] = line

    # nodes
    def nodes(self):
        return self._nodes

    # lines
    def lines(self):
        return self._lines

    # DRAW
    def draw(self):
        nodes = self.nodes()
        for node_label in nodes:
            n0 = nodes[node_label]
            x0 = n0.position()[0]
            y0 = n0.position()[1]
            plt.plot(x0, y0, marker='o', color="blue", zorder=10)  # graph nodes + name
            plt.text(x0 + 20, y0 + 20, node_label)
            for connected_node_label in n0.connected_nodes():
                n1 = nodes[connected_node_label]
                x1 = n1.position()[0]
                y1 = n1.position()[1]
                plt.plot([x0, x1], [y0, y1], color="cyan")  # graph lines as straight edges
        plt.title('TOPOLOGY')
        plt.show()

    # FIND PATHS
    # all the paths that connect the two nodes as list of node labels. have to cross any node at most once
    def find_path(self, start, end, path=[]):
        path = path + [start]  # aggiunge elemento corrente al path
        paths_list = []
        if start == end:
            return [path]  # quando start==fine path completo

        for node in self._nodes[start].connected_nodes():  # per ogni nodo adiacente al nodo corrente
            if node not in path:  # se non e gia stato considerato in questo path
                subpaths = self.find_path(node, end, path)  # chiama ricorsivamente find_path con start il nodo corrente

                for subpath in subpaths:
                    paths_list.append(subpath)  # aggiorna paths_list

        return paths_list

    # CONNECT
    # set the successive attributes of all the network elements as dictionaries
    def connect(self):
        nodes = self.nodes()
        lines = self.lines()
        for nodename in nodes:
            node = nodes[nodename]
            for connectedname in node.connected_nodes():
                linename = nodename + connectedname
                line = lines[linename]

                line.successive()[connectedname] = nodes[connectedname]
                node.successive()[linename] = lines[linename]

        self._connected = True
        print("\nConnected!\n")

    # PROPAGATE
    def propagate(self, signal_information, busy):
        path = signal_information.path()
        nodename = path[0]
        start_node = self.nodes()[nodename]
        propagated_signal_information = start_node.propagate(signal_information, busy)
        return propagated_signal_information

    # GENERATE DATAFRAME
    def create_weighted_paths(self, power):
        if not self._connected:
            self.connect()
        node_labels = self.nodes()
        pairs = []
        for label1 in node_labels:
            for label2 in node_labels:
                if label1 != label2:
                    pairs.append(label1 + label2)

        columns = ['path', 'latency', 'noise', 'snr']
        df = pd.DataFrame()
        paths = []
        latencies = []
        noises = []
        snrs = []

        for pair in pairs:
            for path in self.find_path(pair[0], pair[1]):
                # print(path)
                path_string = ''
                if len(path) > 1:
                    for node in path:
                        path_string += node + '->'
                    paths.append(path_string[: -2])  # salva tutto cancelladno ultimo "->"

                    signal_information = SignalInformation(power, path)
                    signal_information = self.propagate(signal_information, False)
                    latencies.append(signal_information.latency())
                    noises.append(signal_information.noise_power())
                    snrs.append(10.0 * np.log10(signal_information.signal_power() / signal_information.noise_power()))

        df['path'] = paths
        df['latency'] = latencies
        df['noise'] = noises
        df['snr'] = snrs
        pd.set_option('display.max_columns', None)  # or 1000
        pd.set_option('display.max_rows', 100)  # or 1000
        pd.set_option('display.max_colwidth', 20)  # or 199
        self._weighted_paths = df

    def weighted_paths(self):
        return self._weighted_paths

    # FIND BEST SNR AND LATENCY
    def find_best_snr(self, input_node, output_node):
        available_paths = self.available_paths(input_node, output_node)  # gen available checking occupancy
        if available_paths:
            # save all paths with inp and outp voluti
            inout_paths = [path for path in available_paths if ((path[0] == input_node) and (path[-1] == output_node))]
            # search in df for data from path voluti
            inout_df = self.weighted_paths().loc[self.weighted_paths().path.isin(inout_paths)]

            best_snr = np.max(inout_df.snr.values)
            best_path = inout_df.loc[inout_df.snr == best_snr].path.values[0].replace('->', '')
            return best_path
        else:
            return None

    def find_best_latency(self, input_node, output_node):
        available_paths = self.available_paths(input_node, output_node)
        if available_paths:
            inout_paths = [path for path in available_paths if ((path[0] == input_node) and (path[-1] == output_node))]
            inout_df = self.weighted_paths().loc[self.weighted_paths().path.isin(inout_paths)]

            best_latency = np.min(inout_df.latency.values)
            best_path = inout_df.loc[inout_df.latency == best_latency].path.values[0].replace('->', '')
            return best_path

        else:
            return None

    # STREAM
    #  for each element of a given list of instances of the class Connection, sets its latency
    # and snr attribute.
    # These values have to be calculated propagating a SignalInformation instance that has the path that
    # connects the input and the output nodes of the connection and that is the best snr or latency
    # path between the considered nodes. The choice of latency or snr has to
    # be made with a label passed as input to the stream function. The label
    # default value has to be set as latency.

    def stream(self, connections, best="latency"):
        streamed_connections = []
        for connection in connections:
            input_node = connection.input_node()
            output_node = connection.output_node()
            signal_power = connection.signal_power()
            self.create_weighted_paths(signal_power)
            if best == "latency":
                path = self.find_best_latency(input_node, output_node)
            else:
                path = self.find_best_snr(input_node, output_node)

            if path:  # check availability path
                # crea e propaga un siginfo con power= conn.power per calcolare snr e latency della connessione
                in_signal_information = SignalInformation(signal_power, path)
                out_signal_information = self.propagate(in_signal_information, True)
                connection.set_latency(out_signal_information.latency())
                noise = out_signal_information.noise_power()
                connection.set_snr(10 * np.log10(signal_power / noise))
            else:
                connection.set_latency(None)
                connection.set_snr(0)
            streamed_connections.append(connection)

        return streamed_connections

    # CHECK FOR OCCUPANCY
    def available_paths(self, input_node, output_node):
        # genera tutti i path
        all_paths = []
        for path in self.weighted_paths().path.values:
            if (path[0] == input_node) and (path[-1] == output_node):
                all_paths.append(path)

        # gen tutte linee non dispo
        unavailable_lines = [line for line in self.lines() if self.lines()[line].state == 'occupied']

        # se un alinea non dispo si trova nel path corrente questo non e disponibile
        available_paths = []
        for path in all_paths:
            available = True
            for line in unavailable_lines:
                if line[0] + '->' + line[1] in path:
                    available = False
                    break
            if available:
                available_paths.append(path)

        return available_paths
