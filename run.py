from random import shuffle
from network import *


# --------------------- CREATE NETWORK FROM JSON
network = Network('nodes.json')
# network = Network('262459.json')
network.connect()


# --------------------- BUILD DF
# network.set_weighted_paths(1e-3)
# pd.set_option('display.max_columns', None)  # val or None
# pd.set_option('display.max_rows', None)  # val or None
# pd.set_option('display.max_colwidth', 15)  # or 199
# print("\nWEIGHTED GRAPH")
# print(network.weighted_paths)


# --------------------- DRAW
# network.draw()


# --------------------- STREAM CONNECTIONS
nodes = list(network.nodes.keys())
connections = []
def_power = 1
for i in range(100):
    shuffle(nodes)
    conn = Connection(nodes[0], nodes[-1], def_power)
    connections.append(conn)

latencies = []
snrs = []
best="snr" # change to lat for diff
streamed_connections = network.stream(connections,best)
for connection in streamed_connections:
    latencies.append(connection.latency)
    snrs.append(connection.snr)

if best=="lat":
    plt.hist(latencies,bins=10)
    plt.title("Latency Distribution")
    plt.show()
else:
    plt.hist(snrs,bins=10)
    plt.title("SNR Distribution")
    plt.show()