from random import shuffle
from network import *


# --------------------- CREATE NETWORK FROM JSON
network = Network('nodes.json')
# network = Network('262459.json')
network.connect()


# --------------------- BUILD DF
network.create_weighted_paths()
pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', 50)  # or 1000
pd.set_option('display.max_colwidth', 15)  # or 199
print(network.get_weighted_paths())


# --------------------- DRAW
# network.draw()


# --------------------- STREAM CONNECTIONS
nodes = list(network.nodes().keys())
connections = []
def_power = 1e-3
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

# plt.hist(latencies)
# plt.title("Latency Distribution")
# plt.show()
# plt.hist(snrs)
# plt.title("SNR Distribution")
# plt.show()