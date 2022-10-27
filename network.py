import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from node import *
from line import *
from signal_Information import *
from connection import *


class Network:
    def __init__(self, json_path):
        self._nodes = {}
        self._lines = {}
        self.build_NL_dicts(json_path)
        self._weighted_paths = None
        self._route_space = None

    

    # BUILD NL df
    # converts json to dicts of nodes and lines object with the label as key
    def build_NL_dicts(self, json_path):
        nodes_json = json.load(open(json_path, 'r'))
        for node_label in nodes_json:
            node_dict = nodes_json[node_label]
            node_dict['label'] = node_label
            node = Node(node_dict)
            self._nodes[node_label] = node
            for connected_label in node_dict['connected_nodes']:
                line_dict = {}  # empty dic
                line_label = node_label + connected_label  # build line label
                line_dict['label'] = line_label  # set line label
                node_position = np.array(nodes_json[node_label]['position'])  # first node pos
                connected_node_position = np.array(nodes_json[connected_label]['position'])  # second node pos
                line_dict['length'] = np.sqrt(np.sum((node_position - connected_node_position) ** 2))
                # print(line_dict['length'])
                line = Line(line_dict)
                self._lines[line_label] = line

    def nodes(self):
        return self._nodes
    def lines(self):
        return self._lines
   
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

    
    # FIND PATHS (recursive)
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


    # PROPAGATE -> PROBE
    # has to propagate the signal information through the path specified in it and returns it
    # with the udated noise and latency
    def probe(self, signal_info):
        path = signal_info.path()
        for node_ind in range(len(path)-1):
            line_label=str(path[node_ind]+path[node_ind+1])
            signal_info.add_latency(self._lines[line_label].latency_generation())
            signal_info.add_noise(self._lines[line_label].noise_generation(signal_info.signal_power()))
        return signal_info

    
    # PATHS DATAFRAME
    def get_weighted_paths(self): return self._weighted_paths
    def create_weighted_paths(self):
        # columns = ['path', 'latency', 'noise', 'snr']
        df = pd.DataFrame()
        paths = []
        latencies = []
        noises = []
        snrs = []
        node_labels = self.nodes()
        pairs = []
        power=1e-3

        # genera tutte le coppie di (start,end)
        for label1 in node_labels:
            for label2 in node_labels:
                if label1 != label2:
                    pairs.append(label1 + label2)

        for pair in pairs: # per ogni coppia
            for path in self.find_path(pair[0], pair[1]): # calcola tutti i path
                path_string = ''
                if len(path) > 1:
                    for node in path:
                        path_string += node + '->'
                    paths.append(path_string[: -2])  # salva formattato cancelladno ultimo "->"
                    signal_information = SignalInformation(power, path)
                    signal_information = self.probe(signal_information)
                    latencies.append(signal_information.latency())
                    noises.append(signal_information.noise_power())
                    snrs.append(10.0 * np.log10(signal_information.signal_power() / signal_information.noise_power()))

        df['path'] = paths
        df['latency'] = latencies
        df['noise'] = noises
        df['snr'] = snrs
        self._weighted_paths = df.set_index('path')


    # DRAW GRAPH
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


    # FIND BEST SNR/LAT
    def find_best_snr(self,inputn,outputn):
        best=0
        bestpath=""
        for path in self.find_path(inputn,outputn): 
            if self.check_path_lines_occupancy(path)==0:
                path_string = '' # needed for formatting
                for node in path:
                    path_string += node + '->'
                path_string=path_string[: -2]
                snr=self._weighted_paths.loc[path_string,"snr"]
                if snr>best:
                    best=snr
                    bestpath=path
        return bestpath # nella forma list of nodes label
    def find_best_latency(self,inputn,outputn):
        best=999999999
        bestpath=""
        for path in self.find_path(inputn,outputn): 
            if self.check_path_lines_occupancy(path)==0:
                path_string = '' # needed for formatting
                for node in path:
                    path_string += node + '->'
                path_string=path_string[: -2]
                lat=self._weighted_paths.loc[path_string,"latency"]
                if lat<best:
                    best=lat
                    bestpath=path
        return bestpath
    def check_path_lines_occupancy(self,path):
        for node_ind in range(len(path)-1):
            line_label=str(path[node_ind]+path[node_ind+1])
            if self._lines[line_label].state()==1: return 1
        return 0


    # STREAM
    # set latency and snr of conn list propagating siginfo on
    # path that either has best snr or lat (par)
    def stream(self, connlist,best="latency"):
        streamed_connections = []
        for connection in connlist:
            input_node = connection.input_node()
            output_node = connection.output_node()
            signal_power = connection.signal_power()

            if best == "latency":
                path = self.find_best_latency(input_node, output_node)
            elif best == "snr":
                path = self.find_best_snr(input_node, output_node)
                
            if path:
                sig=SignalInformation(signal_power,path)
                self.probe(sig)
                connection.set_latency(sig.latency())
                connection.set_snr(10.0 * np.log10(sig.signal_power() / sig.noise_power()))
            else :
                connection.set_snr(0.0)
                connection.set_latency(None)
            streamed_connections.append(connection)
        return streamed_connections    

    
    # ROUTE SPACE
    def create_route_space(self):
        df = pd.DataFrame()
        paths = []
        latencies = []
        noises = []
        snrs = []
        node_labels = self.nodes()
        pairs = []
        power=1e-3

        # genera tutte le coppie di (start,end)
        for label1 in node_labels:
            for label2 in node_labels:
                if label1 != label2:
                    pairs.append(label1 + label2)

        for pair in pairs: # per ogni coppia
            for path in self.find_path(pair[0], pair[1]): # calcola tutti i path
                path_string = ''
                if len(path) > 1:
                    for node in path:
                        path_string += node + '->'
                    paths.append(path_string[: -2])  # salva formattato cancelladno ultimo "->"
