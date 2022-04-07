from classes.signal_information import *
from classes.nodes import *

# # point 1 test
# path = ["A", "B", "C"]
# info = SignalInformation(100.0, path)
# print(info.get_latency())
# print(info.get_path())
# info.update_path()
# print(info.get_path())

# point 2 test
dic = {
    "label": "A",
    "position": (0, 1),
    "connected_nodes": ["B", "C"]
}
node = Node(dic)
print(node.get_label())
print(node.get_position())
