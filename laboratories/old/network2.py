import json
import math
import random

import matplotlib.pyplot as plt
import pandas as pd

from scipy import special

from .line2 import *
from .node2 import *
from .connection2 import *

conn_power_def = 1e-3


# pd.set_option('display.max_rows', None)


def snr_dB(pw, ns):
    return math.log10(float(pw) / float(ns)) * 10.0


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

        self.connections_list = []  # list of all possible connections aka all paths
        self.weighted_paths = self.create_df()
        self.route_space = self.create_route_space_df()

    # ---------------------------------------- connect ---------------------------------------
    # set the successive attributes of all the network elements as dictionaries (i.e., each node must have a dict
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

    # ---------------------------------------- generates all paths ---------------------------------------
    # given two node labels, returns all the paths that connect the two nodes as list of node labels.
    # The admissible paths have to cross any node at most once; returns a LIST of all posiible paths
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

    # ---------------------------------------- probe, create weighted df ---------------------------------------
    def probe(self, siginfo, path):
        siginfo.set_path(path)
        power = siginfo.get_sig_power()
        for i in range(len(path) - 1):
            line = path[i] + path[i + 1]
            siginfo.add_noise(self.lines[line].noise_generation(power))
            siginfo.add_latency(self.lines[line].latency_generation())
        return siginfo

    # obtained with the propagation through the paths of a spectral information with a signal power of 1 mW
    # cols = ["path", "start", "end", "total_latency", "total_noise", "SNR"]
    def create_df(self):
        cols = ["path", "start", "end", "total_latency", "total_noise", "SNR"]
        data = []  # list of lists
        for start in self.nodes.keys():
            for end in self.nodes.keys():
                # per ogni combinazine di start e end
                for path in self.find_path(start, end):
                    if len(path) > 1:
                        # print(path)
                        sig = SignalInformation(1e-3)
                        self.probe(sig, path)
                        data.append([path, start, end, sig.get_latency(), sig.get_noise_power(),
                                     snr_dB(sig.get_sig_power(), sig.get_noise_power())])
                        self.connections_list.append(Connection(start, end,
                                                                conn_power_def))  # salva tutte le connessioni possibili cioe tutti i path
        df = pd.DataFrame(data, columns=cols)
        return df

    # ---------------------------------------- stream ---------------------------------------
    def check_free_lines(self, path, channel):
        for i in range(len(path) - 1):
            tmp_line = path[i] + path[i + 1]
            if self.lines[tmp_line].is_channel_free(channel) == False:
                return False
        return True

    # new with line state
    def find_best_snr(self, start, end, channel):
        t_snr = 0
        t_path = []
        # itera tra le righe del dataframe che hanno come valori di start e end quelli voluti
        for idx, row in self.weighted_paths[
            (self.weighted_paths["start"] == start) & (self.weighted_paths["end"] == end)].iterrows():
            if row["SNR"] > t_snr and self.check_free_lines(row["path"], channel):
                t_path = row["path"]
        return t_path

    # new with line state
    def find_best_latency(self, start, end, channel):
        t_lat = 10000.0
        t_path = []
        for idx, row in self.weighted_paths[
            (self.weighted_paths["start"] == start) & (self.weighted_paths["end"] == end)].iterrows():
            if row["total_latency"] < t_lat and self.check_free_lines(row["path"], channel):
                t_path = row["path"]
        return t_path

    def propagate(self, lightpath, path):
        lightpath.set_path(path)
        power = lightpath.get_sig_power()
        ch = lightpath.get_channel()
        for i in range(len(path) - 1):
            line = path[i] + path[i + 1]
            self.lines[line].occupy_line_channel(lightpath.get_channel())
            lightpath.add_noise(self.lines[line].noise_generation(power))
            lightpath.add_latency(self.lines[line].latency_generation())

            # FARE
            # 6. Modify the methods propagate and stream in the class Network that
            # should use and update the attribute route space in order to consider the
            # channel occupancy for any path.
            col = "ch" + str(ch + 1)
            ind = self.route_space.index[self.route_space["path"] == str(path)]
            # print(ind)
            self.route_space.loc[ind, str(col)] = "busy"  # str(path) perche indici sono stringhe non liste madonna
        return lightpath

    # path that connects the input
    # and the output nodes of the connection and that is the best snr or latency
    # path between the considered nodes. The choice of latency or snr has to
    # be made with a label passed as input to the stream function. The label
    # default value has to be set as latency.
    #
    # if there are not any available path between the input and the output nodes of a connection, the
    # resulting snr and latency have to be set to zero and ’None’,
    def stream(self, conn_list, label):
        for conn in conn_list:
            lightp = Lightpath(conn.get_signal_power())
            lightp.set_channel(random.choice(range(10)))  # sets a random channel for the lightpath instead of default 0
            if label == "snr":
                best_path = self.find_best_snr(conn.get_input_node(), conn.get_output_node(), lightp.get_channel())
            else:  # latency
                best_path = self.find_best_latency(conn.get_input_node(), conn.get_output_node(), lightp.get_channel())
            # print(best_path)
            if best_path:  # se lista non e vuota
                self.propagate(lightp, best_path)
                conn.set_latency(lightp.get_latency())
                conn.set_snr(snr_dB(lightp.get_sig_power(), lightp.get_noise_power()))
            else:
                conn.set_availability(False)
        return conn_list

    # ---------------------------------------- route space df ---------------------------------------
    def create_route_space_df(self):
        cols = ["path", "start", "end", "ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8", "ch9", "ch10", ]
        data = []
        for start in self.nodes.keys():
            for end in self.nodes.keys():
                # per ogni combinazine di start e end
                for path in self.find_path(start, end):
                    if len(path) > 1:
                        d = []
                        d.append(str(path))
                        d.append(path[0])
                        d.append(path[-1])
                        for chn in range(10):  # per ogni canale
                            ch_free = True
                            for i in range(len(path) - 1):  # affinche sia libero defve essere libero su ogni linea
                                line = path[i] + path[i + 1]
                                if self.lines[line].is_channel_free(chn) == False:
                                    ch_free = False
                                    break
                            if ch_free:
                                d.append("free")
                            else:
                                d.append("busy")
                        data.append(d)

        df = pd.DataFrame(data, columns=cols)
        return df

    # ---------------------------------------- calculate bit rate ---------------------------------------
    # evaluates the bit rate Rb supported by a specific path
    # given the corresponding GSNR (in linear units) and the transceiver tech-
    # nology
    def calculate_bit_rate(self, path, strategy):
        rs = 32  # Rs is the symbol-rate of the light-path  !!*e9
        bn = 12.5  # Bn is the noise bandwidth
        rb = 0.0

        bert = 10 ** -3
        gsnr = self.weighted_paths.loc[self.weighted_paths["path"] == path, "SNR"]

        #  is for the fixed-rate transceiver strategy assuming PM-QPSK
        # modulation
        if strategy == "fixed-rate":  # fixed-rate transceiver strategy assuming PM-QPSK modulation
            if gsnr >= 2 * (special.erfcinv(2 * bert)) ** 2 * rs / bn:
                rb = 100
            else:
                rb = 0
        # flex-rate transceiver strategy assuming the availability of PM-QPSK (100Gbps),
        # PM-8-QAM (200Gbps) and PM-16QAM (400Gbps) modulations, given a BERt of 10−3
        elif strategy == "flex-rate":
            if gsnr < 2 * (special.erfcinv(2 * bert)) ** 2 * rs / bn:
                rb = 0
            elif 2 * special.erfcinv(2 * bert) ** 2 * rs / bn <= gnrs <= 14 / 3 * special.erfcinv(3 / 2 * bert) ** 2 * rs / bn:
                rb = 100
            elif 14 / 3 * special.erfcinv(3 / 2 * bert) ** 2 * rs / bn <= gsnr <= 10 * special.erfcinv(8 / 3 * bert) ** 2 * rs / bn:
                rb = 200
            else:  # gsnr <= 10 * special.erfcinv(8 / 3 * bert) ** 2 * rs / bn
                rb = 400
        # maximum theoretical Shannon rate with an ideal Gaussian modulation.
        elif strategy == "shannon":
            rb = 2 * rs * math.log2(1 + gsnr * rs / bn)

        return rb * 10 ** 9

    # ---------------------------------------- display network topology ---------------------------------------
    def draw(self):
        for i in self.lines.values():
            plt.plot([i.get_start()[0], i.get_end()[0]], [i.get_start()[1], i.get_end()[1]], color="blue", zorder=0)
        for i in self.nodes.values():
            plt.scatter(i.get_position()[0], i.get_position()[1], color="green", s=500)
            plt.annotate(i.get_label(), (i.get_position()[0], i.get_position()[1]), color="white")
        plt.show()

    # ---------------------------------------- getters and info ---------------------------------------

    def get_conn_list(self):
        return self.connections_list

    def get_lines_list(self):
        return self.lines.keys()

    def get_nodes_list(self):
        return self.nodes.keys()

    def get_route_space(self):
        return self.route_space

    def get_weighted_paths(self):
        return self.weighted_paths

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
