import itertools
import random
from random import shuffle

from network import *

# ------------------------------------------------------------ WHICH JSON
json="nodes.json"
json="262459.json"

# ------------------------------------------------------------ DRAW
network = Network(json)
network.draw()
print("\nWEIGHTED GRAPH")
print(network.weighted_paths)



# In your main script, modify the way your code generates the connection
# requests. Instead of generating a sequence of N random requests, generate
# them accordingly to a uniform traffic matrix:
#
# A traffic matrix T is defined as a matrix with a row and a column for each node of the network.
# Each element Ti,j represents the bit rate request in Gbps between the
# nodes i,j.
#
#   If Ti,j = 0, there is no connection request between i,j.
#   If Ti,j = Inf, all the possible achievable traffic is allocated.
#
# Add in the class Network a method that creates and manages the connections given a traffic matrix.
# This method chooses a random pair of source-destination nodes with a non zero request Ti,j .
#
# After connection streaming, the allocated traffic has to be subtracted to the given traffic matrix.
# Assume a uniform distribution: all node pair requests always the same bit rate
# of 100 * M Gbps, where M is an increasing integer number (1, 2, 3, ...).

# Run again the main script of point 5 increasing M until the network sat-
# uration and graphically report the results.



sat_percent = 95
request_n=21


# --------------------------------------------------------------- FIXED RATE
print("\nFIXED")

network = Network(json)
n_node = len(network._nodes_list)

nodes_list=network._nodes_list

saturationFix = []
MsFix = []

M = 1
while 1:
    print(M)
    # Assume a uniform distribution: all node pair requests always the same bit rate
    # of 100 * M Gbps, where M is an increasing integer number (1, 2, 3, ...)
    traffic_matrix = np.ones((n_node, n_node)) * 100 * M
    for i in range(n_node): traffic_matrix[i][i] = 0
    # print(traffic_matrix)
    # print(network.lines.keys())

    elements = list(itertools.permutations(network.nodes.keys(), 2))
    for e in elements:  # remove the diagonal : A-A , B-B , C-C , ...
        if e[0] == e[1] or str(e[0])+str(e[1]) not in network._lines.keys(): # se non e nella topologia non serve
            elements.remove(e)
            i=nodes_list.index(e[0])
            j=nodes_list.index(e[1])
            traffic_matrix[i][j] = 0
            # print(e)
    # print(elements)
    n_elem = len(elements)

    # avendo lista di tutte possibili connessioni nodo-nodo ne sceglie 100
    for i in range(request_n):
        if len(elements) == 0:
            break
        shuffle(elements)
        el = random.choice(elements)
        val = network.upgrade_traffic_matrix(traffic_matrix, el[0], el[1]) # update della tfm rimuovendo br
        if (val==0)|(val == np.inf):
            elements.remove(el)

        # print(traffic_matrix)
        # print()

    sat = 0
    for row in traffic_matrix:
        for el in row:
            if el == float('inf'):
                sat += 1
    sat = sat / n_elem * 100

    # print(sat)

    saturationFix.append(sat)
    MsFix.append(M)

    if sat > sat_percent:
        break
    print("\n")
    M += 1

    # print(network.route_space)


plt.plot(MsFix, saturationFix)
plt.title('Saturation Fixed-Rate')
plt.savefig('Plots/M_fixed_rate.png')
plt.xlabel('M')
plt.ylabel('saturation')
plt.grid(linestyle='-', linewidth=0.5)
plt.show()



# --------------------------------------------------------------- FLEX RATE
print("\nFLEX")

netfixed = Network(json,"flex_rate")
n_node = len(netfixed._nodes_list)

nodes_list=netfixed._nodes_list

saturationflex = []
Msflex = []

M = 1
while 1:
    print(M)
    # Assume a uniform distribution: all node pair requests always the same bit rate
    # of 100 * M Gbps, where M is an increasing integer number (1, 2, 3, ...)
    traffic_matrix = np.ones((n_node, n_node)) * 100 * M
    for i in range(n_node): traffic_matrix[i][i] = 0
    # print(traffic_matrix)
    # print(netfixed.lines.keys())

    elements = list(itertools.permutations(netfixed.nodes.keys(), 2))
    for e in elements:  # remove the diagonal : A-A , B-B , C-C , ...
        if e[0] == e[1] or str(e[0])+str(e[1]) not in netfixed._lines.keys(): # se non e nella topologia non serve
            elements.remove(e)
            i=nodes_list.index(e[0])
            j=nodes_list.index(e[1])
            traffic_matrix[i][j] = 0
            # print(e)
    # print(elements)
    n_elem = len(elements)

    # avendo lista di tutte possibili connessioni nodo-nodo ne sceglie 100
    for i in range(request_n):
        if len(elements) == 0:
            break
        shuffle(elements)
        el = random.choice(elements)
        val = netfixed.upgrade_traffic_matrix(traffic_matrix, el[0], el[1]) # update della tfm rimuovendo br
        if (val==0)|(val == np.inf):
            elements.remove(el)
        # print(traffic_matrix)
        # print()

    sat = 0
    for row in traffic_matrix:
        for el in row:
            if el == float('inf'):
                sat += 1
    sat = sat / n_elem * 100

    # print(sat)

    saturationflex.append(sat)
    Msflex.append(M)

    if sat > sat_percent:
        break
    print("\n")
    M += 1

    # print(netfixed.route_space)


plt.plot(Msflex, saturationflex)
plt.title('Saturation Flex-Rate')
plt.savefig('Plots/M_flex_rate.png')
plt.xlabel('M')
plt.ylabel('saturation')
plt.grid(linestyle='-', linewidth=0.5)
plt.show()



# --------------------------------------------------------------- SHANNON
print("\nSHANNON")

netshannon = Network(json,"shannon")
n_node = len(netshannon._nodes_list)

nodes_list=netshannon._nodes_list

saturationshan = []
Msshan = []

M = 1
while 1:
    print(M)
    # Assume a uniform distribution: all node pair requests always the same bit rate
    # of 100 * M Gbps, where M is an increasing integer number (1, 2, 3, ...)
    traffic_matrix = np.ones((n_node, n_node)) * 100 * M
    for i in range(n_node): traffic_matrix[i][i] = 0
    # print(traffic_matrix)
    # print(netshannon.lines.keys())

    elements = list(itertools.permutations(netshannon.nodes.keys(), 2))
    for e in elements:  # remove the diagonal : A-A , B-B , C-C , ...
        if e[0] == e[1] or str(e[0])+str(e[1]) not in netshannon._lines.keys(): # se non e nella topologia non serve
            elements.remove(e)
            i=nodes_list.index(e[0])
            j=nodes_list.index(e[1])
            traffic_matrix[i][j] = 0
            # print(e)
    # print(elements)
    n_elem = len(elements)
    # print(traffic_matrix)

    # avendo lista di tutte possibili connessioni nodo-nodo ne sceglie 100
    for i in range(request_n):
        if len(elements) == 0:
            break
        shuffle(elements)
        el = random.choice(elements)
        val = netshannon.upgrade_traffic_matrix(traffic_matrix, el[0], el[1]) # update della tfm rimuovendo br
        if (val==0)|(val == np.inf):
            elements.remove(el)

        # print(traffic_matrix)
        # print()

    sat = 0
    for row in traffic_matrix:
        for el in row:
            if el == float('inf'):
                sat += 1
    sat = sat / n_elem * 100

    # print(sat)

    saturationshan.append(sat)
    Msshan.append(M)

    if sat > sat_percent:
        break
    print("\n")
    M += 1

    # print(netshannon.route_space)


plt.plot(Msshan, saturationshan)
plt.title('Saturation Shannon-Rate')
plt.savefig('Plots/M_shannon_rate.png')
plt.xlabel('M')
plt.ylabel('saturation')
plt.grid(linestyle='-', linewidth=0.5)
plt.show()





plt.plot(MsFix, saturationFix, label='fixed-rate')
plt.plot(Msflex, saturationflex, label='flex-rate')
plt.plot(Msshan, saturationshan, label='shannon')
plt.xlabel('M')
plt.ylabel('% of unsatisfied requests')
plt.grid(linestyle='-', linewidth=0.5)
plt.legend(loc='lower right')
plt.title('Saturation Parameter')
plt.savefig('Plots/M_all.png')
plt.show()



