import signal_Information

class Node(object):

    def __init__(self, node):
        self._label = node['label']  # string
        self._position = node['position']  # tuple
        self._connected_nodes = node['connected_nodes']  # list of strings
        self._successive = {}  # dict of Line
        self._state=0 # 0 free, 1 busy

    # label
    def label(self):
        return self._label

    # pos
    def position(self):
        return self._position

    # conn nodes
    def connected_nodes(self):
        return self._connected_nodes

    # succ
    def successive(self):
        return self._successive

