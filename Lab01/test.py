from classes.signal_information import *
from classes.node import *
from classes.line import *
from classes.network import *
import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# point 1 test
# info = SignalInformation(100.0, )
# print(info.get_latency())
# print(info.get_path())
# info.update_path()
# print(info.get_path())

# point 2 test

# # salva gli attributi necessari dal file json in un dict
# nodes_info_dict = json.load(open("resources/nodes.json"))
# # inizializza dizionario vuoto per oggetti nodo nella forma {"label": node_object}
# nodes = {}
# # brutto perche il dizoinario convertito da json non ha un valore label
# for i in nodes_info_dict:
#     nodes[i] = Node(i, nodes_info_dict[i])
#     # print(nodes_dict[i].get_label())
# # print()
#
# # point 3
# lines = {}
# for node in nodes.values():  # per ogni node ! qui itera in dic obj
#     for con in node.get_connected():  # per ogni node collegato ! qui itera in lista str
#         linename = node.get_label() + con  # crea nome linea
#         lines[linename] = Line(linename, node.get_position(), nodes[con].get_position())  # crea obj linea e add a dic
#         # print(lines[linename].get_label())
# for i in lines.values():
#     print(i.get_label())

# point 4
filepath = "resources/nodes.json"
info = SignalInformation(1e-3)
net = Network(filepath)
net.connect()
print(net.create_df())

# net.propagate(info, ["A", "B", "D", "E", "F"])
# print("path:  " + str(info.get_path()))
# print("lat:  " + str(info.get_latency()))
# print("noise:  " + str(info.get_noise_power()))

# net.print_nodes_info()
# net.print_lines_info()
# print(net.get_nodes_list())
# print(net.get_lines_list())

# for i in net.find_path("A", "F"):
#     print(i)
# print("----------")
# print(type(net.find_path("A", "F")))

# net.draw()
