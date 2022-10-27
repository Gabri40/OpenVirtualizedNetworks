import json

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import special

from node import *
from xx.signal_information2 import *
from line import *
from connection import *

BER_t = 1e-3
Rs = 32e9  # symbol-rate of the light-path that can be fixed to 32 GHz
Bn = 12.5e9  # noise bandwidth


def path_to_line_set(path):
    path = path.replace('->', '')
    return set([path[i] + path[i + 1] for i in range(len(path) - 1)])


class Network:
    def __init__(self, json_path):
        self._nodes = {}
        self._lines = {}
        self.build_nodes_lines_dict(json_path)
        self._connected = False
        self._weighted_paths = None
        self._route_space = None

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
    def propagate(self, lightpath, busy=False):
        path = lightpath.path()
        nodename = path[0]
        start_node = self.nodes()[nodename]
        propagated_lightpath = start_node.propagate(lightpath, busy)
        return propagated_lightpath

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

        # columns = ['path', 'latency', 'noise', 'snr']
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

        self._weighted_paths = df

        route_space = pd.DataFrame()
        route_space['path'] = paths
        for i in range(10):
            route_space[str(i)] = ['free'] * len(paths)
        self._route_space = route_space

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
            best_path = inout_df.loc[inout_df.snr == best_snr].path.values[0]
            return best_path
        else:
            return None

    def find_best_latency(self, input_node, output_node):
        available_paths = self.available_paths(input_node, output_node)
        if available_paths:
            inout_paths = [path for path in available_paths if ((path[0] == input_node) and (path[-1] == output_node))]
            inout_df = self.weighted_paths().loc[self.weighted_paths().path.isin(inout_paths)]

            best_latency = np.min(inout_df.latency.values)
            best_path = inout_df.loc[inout_df.latency == best_latency].path.values[0]
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
            elif best == "snr":
                path = self.find_best_snr(input_node, output_node)
            else:
                path = None
                print("ERROR")

            # print(path)
            if path:
                path_occupancy = self.route_space().loc[self.route_space().path == path].T.values[1:]
                # print(path_occupancy)
                # print()
                channel = [i for i in range(len(path_occupancy)) if path_occupancy[i] == 'free'][0]
                # print(channel)
                # print()

                path = path.replace('->', '')

                in_lightpath = Lightpath(signal_power, path, channel)
                out_lightpath = self.propagate(in_lightpath, True)
                connection.set_latency(out_lightpath.latency())

                noise = out_lightpath.noise_power()
                connection.set_snr(10 * np.log10(signal_power / noise))

                self.update_route_space(path, channel)

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

        # se una linea non dispo si trova nel path corrente questo non e disponibile
        available_paths = []
        for path in all_paths:
            path_occupancy = self.route_space().loc[self.route_space().path == path].T.values[1:]
            if 'free' in path_occupancy:
                available_paths.append(path)
        return available_paths

    # ROUTE SPACE
    def route_space(self):
        return self._route_space

    def update_route_space(self, path, channel):
        all_paths = [path_to_line_set(p) for p in self.route_space().path.values]
        states = self.route_space()[str(channel)]
        lines = path_to_line_set(path)
        for i in range(len(all_paths)):
            line_set = all_paths[i]
            if lines.intersection(line_set):
                states[i] = 'occupied'
        self.route_space()[str(channel)] = states

    def calculate_bit_rate(self, lightpath, strategy):
        path = lightpath.path()
        GSNR_db = pd.array(self.weighted_paths().loc[self.weighted_paths()['path'] == path]['snr'])[0]
        GSNR = 10 ** (GSNR_db / 10)

        if strategy == 'fixed_rate':
            if GSNR > 2 * special.erfcinv(2 * BER_t) ** 2 * (Rs / Bn):
                Rb = 100
            else:
                Rb = 0

        if strategy == 'flex_rate':
            if GSNR < 2 * special.erfcinv(2 * BER_t) ** 2 * (Rs / Bn):
                Rb = 0
            elif (GSNR > 2 * special.erfcinv(2 * BER_t) ** 2 * (Rs / Bn)) & (GSNR < (14 / 3) * special.erfcinv(
                    (3 / 2) * BER_t) ** 2 * (Rs / Bn)):
                Rb = 100
            elif (GSNR > (14 / 3) * special.erfcinv((3 / 2) * BER_t) ** 2 * (Rs / Bn)) & (GSNR < 10 * special.erfcinv(
                    (8 / 3) * BER_t) ** 2 * (Rs / Bn)):
                Rb = 200
            elif GSNR > 10 * special.erfcinv((8 / 3) * BER_t) ** 2 * (Rs / Bn):
                Rb = 400

        if strategy == 'shannon':
            Rb = 2 * Rs * np.log2(1 + Bn / Rs * GSNR) / 1e9

        return Rb
