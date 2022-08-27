import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from random import shuffle

from signal_information import *
from node import *
from line import *
from network import *

# --------------------- CREATE NETWORK FROM JSON
network = Network('nodes.json')
# network = Network('262459.json')
network.connect()
wp_power = 0.001
network.create_weighted_paths(wp_power)
# network.draw()
# print(network.weighted_paths())

# --------------------- CREATE RANDOM CONN LIST AND PLOT SNR, LAT DISTRIBUTIONS
nodes = list(network.nodes().keys())
connections = []
def_power = 1
for i in range(100):
    shuffle(nodes)
    conn = Connection(nodes[0], nodes[-1], def_power)
    connections.append(conn)

latencies = []
snrs = []
streamed_connections = network.stream(connections)
for connection in streamed_connections:
    latencies.append(connection.latency())
    snrs.append(connection.snr())

plt.hist(latencies)
plt.title("Latency Distribution")
plt.show()
plt.hist(snrs)
plt.title("SNR Distribution")
plt.show()

print(network.weighted_paths())
