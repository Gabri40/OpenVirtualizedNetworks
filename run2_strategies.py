from random import shuffle
from network import *

# ------------------------------------------------------------ CREATE NETWORK FROM JSON
network = Network('nodes.json')
# network = Network('262459.json')
network.connect()
print(len(network.lines))
# ------------------------------------------------------------ DRAW
network.draw()