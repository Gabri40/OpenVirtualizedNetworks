
import signal_information
import lightpath

class Node(object):
    def __init__(self, node_dict):
        self._label = node_dict['label']
        self._position = node_dict['position']
        self._connected_nodes = node_dict['connected_nodes']
        self._successive = {}
        self._transceiver=""

    @property
    def label(self):
        return self._label
    
    @property
    def position(self):
        return self._position
    
    @property
    def connected_nodes(self):
        return self._connected_nodes
    
    @property
    def transceiver(self):
        return self._transceiver
    @transceiver.setter
    def transceiver(self, transceiver):
        self._transceiver = transceiver

    @property
    def successive(self):
        return self._successive
    @successive.setter
    def successive(self, successive):
        self._successive = successive
    
    def probe(self, signal_information,busy=False):
        path = signal_information.path
        if len(path) > 1:
            line_label = path[:2]
            linestr=""
            line = self.successive[linestr.join(line_label)] #  line_label = path[:2] da una list
            signal_information.next()
            signal_information = line.propagate(signal_information,busy)
        return signal_information

    def propagate(self, lightpath,busy=False):
        path = lightpath.path
        if len(path) > 1:
            line_label = path[:2]
            linestr=""
            line = self.successive[linestr.join(line_label)] #  line_label = path[:2] da una list
            lightpath.next()
            lightpath = line.propagate(lightpath,busy)
        return lightpath