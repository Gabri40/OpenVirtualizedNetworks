from random import shuffle
from network import *

# -------------------
# USATO FINO AL LAB 5
# -------------------


# ------------------------------------------------------------ CREATE NETWORK FROM JSON
network = Network('nodes.json')
# network = Network('262459.json')
network.connect()
print(len(network.lines))

# ------------------------------------------------------------ DRAW
network.draw()



# ------------------------------------------------------------ WEIGHTED PATH
network.set_weighted_paths(1e-3)
pd.set_option('display.max_columns', None)  # val or None
# pd.set_option('display.max_rows', None)  # val or None
pd.set_option('display.max_colwidth', 10)  # or 199
print("\nWEIGHTED GRAPH")
print(network.weighted_paths)



# ------------------------------------------------------------ STREAM
# LAB4 es6
# Create a main that constructs the network defined by ’nodes.json’ and
# runs its method stream over 100 connections with signal power equal
# to 1 mW and the input and output nodes randomly chosen. This run has
# to be performed in turn for latency and snr path choice. Accordingly, plot
# the distribution of all the latencies or the snrs.
best="latency"
# best="snr"

nodes = list(network.nodes.keys())
connections = []
def_power = 1e-3
conn_n=100
for i in range(conn_n):
    shuffle(nodes)
    conn = Connection(nodes[0], nodes[-1], def_power)
    connections.append(conn)


latencies = []
snrs = []
streamed_connections = network.stream(connections,best)
for connection in streamed_connections:
    if connection.latency is not None: latencies.append(connection.latency)
    if connection.snr > 0: snrs.append(connection.snr)

if best=="latency":
    plt.hist(latencies,bins=10)
    plt.title("Latency Distribution")
    plt.show()
else:
    plt.hist(snrs,bins=10)
    plt.title("SNR Distribution")
    plt.show()



# ------------------------------------------------------------ UPDATED ROUTE SPACE
# Modify the methods propagate and stream in the class Network that
# should use and update the attribute route space in order to consider the
# channel occupancy for any path.
# Run the last exercise of the previous set (Lab 4) with this new network
# abstraction on a list of 100 randomly chosen connections.

pd.set_option('display.max_columns', None)  # val or None
pd.set_option('display.max_rows', None)  # val or None
pd.set_option('display.max_colwidth', 10)  # or 199
print("\nROUTE SPACE UPDATED")
print(network.route_space)





