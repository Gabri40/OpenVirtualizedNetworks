import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.constants import c

from signal_information import *
from node import *
from line import *
from connection import *

class Network(object):
    def __init__(self, json_path):
        node_json = json.load(open(json_path,'r'))
        self._nodes = {}
        self._lines = {}
        for node_label in node_json:
            # Create the node instance
            node_dict = node_json[node_label]
            node_dict['label'] = node_label
            node = Node(node_dict)
            self._nodes[node_label] = node
            # Create the line instances
            for connected_node_label in node_dict['connected_nodes']:
                line_dict ={}
                line_label = node_label + connected_node_label
                line_dict['label'] = line_label
                node_position = np.array(node_json[node_label]['position'])
                connected_node_position=np.array(node_json[connected_node_label]['position'])
                line_dict['length'] =np.sqrt(np.sum((node_position-connected_node_position)**2))
                line = Line(line_dict)
                # print(line.label)
                self._lines[line_label] = line

        self._weighted_paths= None
    
    @property
    def nodes(self):
        return self._nodes    
    
    @property
    def lines(self):
        return self._lines

    @property
    def weighted_paths(self):
        return self._weighted_paths
    
    def draw(self):
        nodes = self.nodes
        for node_label in nodes.keys():
            n0 = nodes[node_label]
            x0 = n0.position[0]
            y0 = n0.position[1]
            plt.plot(x0, y0, marker='o', color="blue", zorder=10) # graph nodes + name
            plt.text(x0 + 20, y0 + 20, node_label)
            for connected_node_label in n0.connected_nodes:
                n1 = nodes[connected_node_label]
                x1 = n1.position[0]
                y1 = n1.position[1]
                plt.plot([x0, x1],[y0, y1], color="cyan") # graph lines as straight edges
        plt.title('TOPOLOGY')
        plt.show()
    
    def find_paths(self, start, end,path=[]):
        path = path +[start]  # aggiunge elemento corrente al path
        paths_list =[]
        if start == end:
            return[path]  # quando start==fine path completo

        for node in self._nodes[start].connected_nodes:  # per ogni nodo adiacente al nodo corrente
            if node not in path:  # se non e gia stato considerato in questo path
                subpaths = self.find_paths(node, end, path) # chiama ricorsivamente find_path con start il nodo corrente

                for subpath in subpaths:
                    paths_list.append(subpath) # aggiorna paths_list

        return paths_list
    
    def connect(self):
        nodes_dict = self.nodes
        lines_dict = self.lines
        for node_label in nodes_dict:
            node = nodes_dict[node_label]
            for connected_node in node.connected_nodes:
                line_label = node_label + connected_node
                line = lines_dict[line_label]
                line.successive[connected_node] = nodes_dict[connected_node]
                node.successive[line_label] = lines_dict[line_label]
        print("\n--CONNECTED--\n")
    
    def propagate(self, signal_information,occupation=False):
        path = signal_information.path
        start_node = self.nodes[path[0]]
        propagated_signal_information=start_node.propagate(signal_information,occupation)
        return propagated_signal_information

    def set_weighted_paths(self,power):
        node_labels = self._nodes.keys()
        pairs =[]
        for label1 in node_labels:
            for label2 in node_labels:
                if label1 != label2:
                    pairs.append(label1 + label2)
                    columns =["path","latency","noise","snr"]

        df = pd.DataFrame()
        paths =[]
        latencies =[]
        noises =[]
        snrs =[]
        for pair in pairs:
            for path in self.find_paths(pair[0], pair[1]):
                path_string =""

                for node in path:
                    path_string += node +"->"
                paths.append(path_string[: -2])

                # Propagation
                signal_information = SignalInformation(power, path)
                signal_information = self.propagate(signal_information)
                latencies.append(signal_information.latency)
                noises.append(signal_information.noise_power)
                snrs.append(10*np.log10(signal_information.signal_power/signal_information.noise_power))
       
        df["path"] = paths
        df["latency"] = latencies
        df["noise"] = noises
        df["snr"] = snrs

        self._weighted_paths = df
        # self._weighted_paths = df.set_index("path")

    def available_paths(self,input_node,output_node):
        all_paths =[path for path in self.weighted_paths.path.values
            if((path[0]== input_node)and(path[-1]== output_node)) ]
        unavailable_lines =[line for line in self.lines
            if self.lines[line].state =='occupied' ]

        available_paths =[]
        for path in all_paths :
            available = True
            for line in unavailable_lines :
                if line[0] +'->'+ line[1] in path :
                    available = False
                    break
            if available :
                available_paths.append(path)
        return available_paths

    def find_best_snr(self,input_node,output_node):
        available_paths = self.available_paths(input_node, output_node)
        if available_paths:
            inout_paths =[path for path in available_paths
                if((path[0]== input_node)and(path[-1]== output_node))]
            inout_df = self.weighted_paths.loc[
                self.weighted_paths.path.isin(inout_paths)]
            best_snr = np.max(inout_df.snr.values)
            best_path = inout_df.loc[
                inout_df.snr == best_snr].path.values[0].replace('->','')
        return best_path
    
    def find_best_latency(self,input_node,output_node):
        available_paths = self.available_paths(input_node, output_node)
        if available_paths:
            inout_paths =[path for path in all_paths
                if((path[0]== input_node)and(path[-1]== output_node))]
            inout_df = self.weighted_paths.loc[
                self.weighted_paths.path.isin(inout_paths)]
            best_latency = np.min(inout_df.snr.values)
            best_path = inout_df.loc[
                inout_df.snr == best_latency].path.values[0].replace('->','')
        return best_path


    # ------------------------ STREAM
    def stream(self, connections, best ='latency'):
        streamed_connections =[]
        for connection in connections :
            input_node = connection.input_node
            output_node = connection.output_node
            signal_power = connection.signal_power
            self.set_weighted_paths(signal_power)
            
            if best =='latency':
                path = self.find_best_latency(input_node, output_node)
            elif best =='snr':
                path = self.find_best_snr(input_node, output_node)

            if path: # check di availability fatto gia in find_best_srn/lat
                in_signal_information = SignalInformation(signal_power, path)
                out_signal_information = self.propagate(in_signal_information)
                connection.latency = out_signal_information.latency
                noise = out_signal_information.noise_power
                connection.snr = 10 * np.log10(signal_power / noise)
            else:
                connection.latency = None
                connection.snr=0
            streamed_connections.append(connection)
        return streamed_connections