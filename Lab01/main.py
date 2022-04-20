from classes.signal_information import *
from classes.node import *
from classes.line import *
import json

# point 1 test
# info = SignalInformation(100.0, )
# print(info.get_latency())
# print(info.get_path())
# info.update_path()
# print(info.get_path())

# point 2 test

# salva gli attributi necessari dal file json in un dict
nodes_info_dict = json.load(open("resources/nodes.json"))
# inizializza dizionario vuoto per oggetti nodo nella forma {"label": node_object}
nodes = {}
# brutto perche il dizoinario convertito da json non ha un valore label
for i in nodes_info_dict:
    nodes[i] = Node(i, nodes_info_dict[i])
    # print(nodes_dict[i].get_label())
# print()

# point 3
lines = {}
for node in nodes.values():  # per ogni node ! qui itera in dic obj
    for con in node.get_connected():  # per ogni node collegato ! qui itera in lista str
        linename = node.get_label() + con  # crea nome linea
        lines[linename] = Line(linename, node.get_position(), nodes[con].get_position())  # crea obj linea e add a dic
        # print(lines[linename].get_label())
for i in lines.values():
    print(i.get_label())
