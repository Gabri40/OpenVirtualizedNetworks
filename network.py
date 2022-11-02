import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.special as math

from signal_information import *
from lightpath import *
from node import *
from line import *
from connection import *


class Network(object):
    def __init__(self, json_path):
        node_json = json.load(open(json_path,'r'))
        self._nodes = {}
        self._lines = {}
        self._connected= False

        # crea dizionari di nodes e lines partendo da json
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
        self._route_space=None
    
    @property
    def nodes(self):
        return self._nodes    
    
    @property
    def lines(self):
        return self._lines

    @property
    def weighted_paths(self):
        return self._weighted_paths

    @property
    def route_space(self):
        return self._route_space


    # ------------------------------------------------------------ CONNECT
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
        self._connected=True

    
    # ------------------------------------------------------------ FIND PATHS
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


    # ------------------------------------------------------------ PROPAGATE
    def probe(self, signal_info):
        path = signal_info.path
        start_node = self.nodes[path[0]]
        propagated_lightpath=start_node.propagate(signal_info)
        return propagated_lightpath

    def propagate(self, lightpath,busy=False):
        path = lightpath.path
        start_node = self.nodes[path[0]]
        propagated_lightpath=start_node.propagate(lightpath)
        return propagated_lightpath



    # ------------------------------------------------------------ DRAW
    def draw(self):
        if not self._connected: self.connect()
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
    

    # ------------------------------------------------------------ WEIGHTED PATH
    def set_weighted_paths(self,power):
        if not self._connected: self.connect()
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
                signal_information = self.probe(signal_information)
                latencies.append(signal_information.latency)
                noises.append(signal_information.noise_power)
                snrs.append(10*np.log10(signal_information.signal_power/signal_information.noise_power))
       
        df["path"] = paths
        df["latency"] = latencies
        df["noise"] = noises
        df["snr"] = snrs

        # self._weighted_paths = df.set_index("path")
        self._weighted_paths = df


        route_space=pd.DataFrame()
        route_space['path']=paths
        for i in range (10):
            route_space[str(i)]=['free']*len(paths)

        # self._route_space=route_space.set_index("path")
        self._route_space=route_space


    # ------------------------------------------------------------ FIND BEST PATH
    # genera tutte le path con almeno un canale libero
    def available_paths(self,start,end):
        if self.weighted_paths is None :
            self.set_weighted_paths(1e-3)

        all_paths=[]
        for path in self.weighted_paths.path.values :
            if ((path[0]==start) and (path[-1]==end)):
                all_paths.append(path)
        
        available_paths = []
        for path in all_paths:
            if "free" in self.route_space.loc[self.route_space.path==path].T.values[1:]:
                available_paths.append(path)
        return available_paths

    def find_best_snr(self,start,end):
        # paths=self.weighted_paths.path.values
        paths=self.available_paths(start,end)
        if paths:
            inout_paths=[path for path in paths if path[0]==start and path[-1]==end]
            
            inout_df = self.weighted_paths.loc[ self.weighted_paths.path.isin(inout_paths) ]
            best_snr= np.max(inout_df.snr.values)
            best_path = inout_df.loc[ inout_df.snr== best_snr ].path.values[0]
        else:
            return None
        return best_path

    def find_best_latency(self,start,end):
        # paths=self.weighted_paths.path.values
        paths=self.available_paths(start,end)
        if paths:    
            inout_paths=[path for path in paths if path[0]==start and path[-1]==end]

            inout_df = self.weighted_paths.loc[ self.weighted_paths.path.isin(inout_paths) ]
            best_lat = np.min(inout_df.latency.values)
            best_path = inout_df.loc[ inout_df.latency == best_lat ].path.values[0]
        else:
            return None
        return best_path

        
    # ------------------------------------------------------------ STREAM
    # for each element
    # of a given list of instances of the class Connection, sets its latency
    # and snr attribute. These values have to be calculated propagating a
    # SignalInformation instance that has the path that connects the input
    # and the output nodes of the connection and that is the best snr or latency
    # path between the considered nodes. The choice of latency or snr has to
    # be made with a label passed as input to the stream function. The label
    # default value has to be set as latency.
    def stream(self, connections, best='latency'):
        if not self._connected: self.connect()
        if self.weighted_paths is None :
            self.set_weighted_paths(1e-3)

        streamed_connections = []
        for connection in connections:
            in_node = connection.input_node
            out_node = connection.output_node
            sig_power = connection.signal_power

            if best == 'latency':
                path = self.find_best_latency(in_node, out_node)
            elif best == 'snr':
                path= self.find_best_snr(in_node, out_node)

            if path: # potrebbero non essercene con canali liberi

                path_occupancy = self.route_space.loc[self.route_space.path==path].T.values[1:]

                channel =[i for i in range(len(path_occupancy)) if path_occupancy[i]=="free"][0]

                path=path.replace("->","")

                in_signal_information = SignalInformation(sig_power,path)
                out_signal_information = self.propagate(in_signal_information)

                connection.latency = out_signal_information.latency
                noise = out_signal_information.noise_power
                connection.snr = 10*np.log10(sig_power/noise)

                self.update_route_space(path,channel)

            else :
                connection.latency=None
                # connection.latency=0
                connection.snr=0

            streamed_connections.append(connection)
        return streamed_connections



    # ------------------------------------------------------------ ROUTE SPACE UPDATING
    # has to update both the route space df value 
    # !!! multiple paths can use the same line so have to be updated
    # -> needs to convert path to the set of lines name to update

    # set di label di lines della path specificata !! set elements are unique!
    def path_to_lines(self,path):
        path=path.replace('->','')
        return set([path[i] + path[i+1] for i in range(len(path)-1)])

    def update_route_space(self,path,channel):
        # salva linee del path corrente da modificare
        lines=self.path_to_lines(path)

        #update route space lines che contengono stesse linee
        all_p=self.route_space.path.values
        for path in all_p:
            path_formatted=path.replace('->','')
            for line in lines:
                if line in path_formatted:
                    self.route_space.loc[self.route_space.path==path, str(channel)]="occupied"



    # ------------------------------------------------------------ CALCULATE BIT RATE
    # Implement a method calculate bit rate(path, strategy) in the Net-
    # work class that evaluates the bit rate Rb supported by a specific path
    # given the corresponding GSNR (in linear units) and the transceiver tech-
    # nology

    def calculate_bit_rate(self, lightpath, strategy):
        global BER_t
        Rs = lightpath.Rs
        global Bn
        path = lightpath.path
        Rb = 0
        GSNR_db = pd.array(self.weighted_paths.loc[self.weighted_paths['path'] == path]['snr'])[0]
        GSNR = 10 ** (GSNR_db / 10)
        if strategy == 'fixed_rate':
            if GSNR > 2 * math.erfcinv(2 * BER_t) ** 2 * (Rs / Bn):
                Rb = 100
            else:
                Rb = 0

        if strategy == 'flex_rate':
            if GSNR < 2 * math.erfcinv(2 * BER_t) ** 2 * (Rs / Bn):
                Rb = 0
            elif (GSNR > 2 * math.erfcinv(2 * BER_t) ** 2 * (Rs / Bn)) & (GSNR < (14 / 3) * math.erfcinv(
                    (3 / 2) * BER_t) ** 2 * (Rs / Bn)):
                Rb = 100
            elif (GSNR > (14 / 3) * math.erfcinv((3 / 2) * BER_t) ** 2 * (Rs / Bn)) & (GSNR < 10 * math.erfcinv(
                    (8 / 3) * BER_t) ** 2 * (Rs / Bn)):
                Rb = 200
            elif GSNR > 10 * math.erfcinv((8 / 3) * BER_t) ** 2 * (Rs / Bn):
                Rb = 400

        if strategy == 'shannon':
            Rb = 2 * Rs * np.log2(1 + Bn / Rs * GSNR) / 1e9

        return Rb

            





