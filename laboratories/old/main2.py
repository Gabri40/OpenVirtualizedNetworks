from classes.network2 import *
import random
import numpy as np
import matplotlib.pyplot as plt

conn_power_default = 1e-3


def div(): print("\n" + "------------------------------------------------------------" + "")


# ------------------------------------------------------------create network from file json
filepath = "resources/nodes.json"
net = Network(filepath)
net.connect()
# net.draw()
print(net.get_weighted_paths())
div()
net.get_weighted_paths().to_csv('weighted paths.csv', sep='\t', index=False)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# print(net.get_route_space().loc[0, "path"] == "['A', 'B']")
print(net.get_route_space())
div()

# -----------------------------------------generate list of connections: scieglie 100 tra tutte le connessioni possibili
conn_l = []
nodes = "ABCDEF"
c = 0
while 1:
    con = random.choice(net.get_conn_list())
    if con not in conn_l:
        conn_l.append(con)
        c += 1
    if c == 99:
        break

# ------------------------------------------------------------stream connection list according to label
label = "snr"
# label = "latency"
streamed_conn = net.stream(conn_l, label)
print(net.get_route_space())
div()
net.get_route_space().to_csv('occupied roout space.csv', sep='\t', index=False)

# ------------------------------------------------------------plot the distribution of all the latencies or the snrs
hist_x = []
if label == "snr":
    for c in streamed_conn:
        if c.is_path_available():
            hist_x.append(c.get_snr())
else:
    for c in streamed_conn:
        if c.is_path_available():
            hist_x.append(c.get_latency())
plt.hist(hist_x)  # If cumulative < 0  the direction of accumulation is reversed.
plt.title(label.upper())
plt.show()
