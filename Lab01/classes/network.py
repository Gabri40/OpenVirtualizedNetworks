from classes.signal_information import *
from classes.nodes import *
from classes.line import *
import json


class Network:
    def __init__(self, json_path):
        self.json_path = json_path
        self.nodes = {}  # {"label": node_object}
        self.lines = {}

        # salva gli attributi necessari dal file json in un dict
        # brutto perche il dizoinario convertito da json non ha un valore label -> crea un second dic
        nodes_info_dict = json.load(open(json_path))
        for i in nodes_info_dict:
            nodes[i] = Node(i, nodes_info_dict[i])

        # per ogni node ! qui itera in dic obj
        # per ogni node collegato ! qui itera in lista str
        # crea nome linea
        # crea obj linea e add a dic
        for node in nodes.values():
            for con in node.get_connected():
                linename = node.get_label() + con
                lines[linename] = Line(linename, node.get_position(), nodes[con].get_position())



