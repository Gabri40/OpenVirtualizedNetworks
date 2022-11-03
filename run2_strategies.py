from random import shuffle
from network import *

# ------------------------------------------------------------ WHICH JSON
# json="nodes.json"
json="262459.json"

pd.set_option('display.max_columns', None)  # any val for short, None for full display
pd.set_option('display.max_rows', None)     # any val for short, None for full display
pd.set_option('display.max_colwidth', 20)

# ------------------------------------------------------------ DRAW
network = Network(json)
network.draw()
# print("\nWEIGHTED GRAPH")
# print(network.weighted_paths)



# ------------------------------------------------------------ RUN
# Plot on the same figure the bit rate curve versus GSNR (in dB) of each
# transceiver technology.
#
# Run the main that evaluates the distribution of the SNR on a list of
# 100 randomly chosen connections for the three newly provided network
# description json files and plot the histogram of the accepted connections
# bit rates calculating the overall average. Also calculate the total capacity
# allocated into the network. Compare the three results obtained for the
# three different transceiver strategies.



# ------------------------------------------------------------ GENERATE CONNECTIONS
nodes = list(network.nodes.keys())
connections = []
def_power = 1e-3
conn_n=100
for i in range(conn_n):
    shuffle(nodes)
    conn = Connection(nodes[0], nodes[-1], def_power)
    connections.append(conn)
conn_fixed = connections
conn_flex = connections
conn_shannon = connections

best="snr"


# --------------------------------------------------------------- FIXED RATE
network = Network(json)
network.connect()
print("\nFIXED")

streamed_connections_fixed_rate = network.stream(conn_fixed, best)

snrs = [connection.snr for connection in streamed_connections_fixed_rate]
snrs_ = np.ma.masked_equal(snrs, 0)
plt.hist(snrs_, bins=20)

plt.title('SNR Distribution Full fixed-rate')
plt.xlabel('dB')
plt.savefig('Plots/SNRDistributionFullfixed_rate.png')
plt.show()

bit_rate_fixed_rate = [connection.rb for connection in streamed_connections_fixed_rate]
brfr = np.ma.masked_equal(bit_rate_fixed_rate, 0)
plt.hist(brfr, bins=20,label='fixed-rate')

plt.title('BitRate Full fixed-rate')
plt.xlabel('Gbps')
plt.savefig('Plots/BitRateFullfixed_rate.png')
plt.show()

# print(network.logger)


# --------------------------------------------------------------- FLEX RATE
network_flex_rate = Network(json,"flex_rate")
network_flex_rate.connect()
print("\nFLEX")

streamed_connections_flex_rate = network_flex_rate.stream(conn_flex, best)

snrs = [connection.snr for connection in streamed_connections_flex_rate]
snrs_ = np.ma.masked_equal(snrs, 0)
plt.hist(snrs_, bins=20)

plt.title('SNR Distribution Full flex-rate')
plt.xlabel('dB')
plt.savefig('Plots/SNRDistributionFullflex_rate.png')
plt.show()

bit_rate_flex_rate = [connection.rb for connection in streamed_connections_flex_rate]
brfr = np.ma.masked_equal(bit_rate_flex_rate, 0)
plt.hist(brfr, bins=20, label='flex_rate')

plt.xlabel('Gbps')
plt.title('BitRate Full Flex-Rate')
plt.savefig('Plots/BitRateFullFlex_Rate.png')
plt.show()

# print(network_flex_rate.logger)


# --------------------------------------------------------------- SHANNON RATE
network_shannon = Network(json,"shannon")
network_shannon.connect()
print("\nSHANNON")

streamed_connections_shannon = network_shannon.stream(conn_shannon, best)

snrs = [connection.snr for connection in streamed_connections_shannon]
snrs_ = np.ma.masked_equal(snrs, 0)
plt.hist(snrs_, bins=20)

plt.title('SNR Distribution Full Shannon')
plt.xlabel('dB')
plt.savefig('Plots/SNRDistributionFullshannon.png')
plt.show()

bit_rate_shannon = [connection.rb for connection in streamed_connections_shannon]
brs = np.ma.masked_equal(bit_rate_shannon, 0)

plt.hist(brs,bins=20,label='shannon')

plt.xlabel('Gbps')
plt.title('BitRate Full Shannon')
plt.savefig('Plots/BitRateFullShannon.png')
plt.show()

# print(network_shannon.logger)


# --------------------------------------------------------------- LAT & SNR DISTRIBUTION GRAPHS
streamed_connections = network.stream(connections,best)
latencies = [connection.latency for connection in streamed_connections if connection.latency is not None]
plt.hist(np.ma.masked_equal(latencies, 0), bins=25)
plt.title('Latency Distribution')
plt.savefig('Plots/LatencyDistribution.png')
plt.show()
snrs=[connection.snr for connection in streamed_connections]
plt.hist(np.ma.masked_equal(snrs, 0), bins=20)
plt.title('SNR Dstribution')
plt.savefig('Plots/SNRDistribution.png')
plt.show()


# --------------------------------------------------------------- TOTAL CAPACITY
print("\n")
print("Average Latency: ", np.average(np.ma.masked_equal(latencies,0)))
print("Average SNR: ", np.average(np.ma.masked_equal(snrs,0)))

print("\nTotal Capacity Fixed-Rate:", np.sum(bit_rate_fixed_rate))
print("Average Capacity Fixed-Rate:", np.mean(np.ma.masked_equal(bit_rate_fixed_rate,0)))

print("\nTotal Capacity Flex-Rate:", np.sum(bit_rate_flex_rate))
print("Average Capacity Flex-Rate:", np.mean(np.ma.masked_equal(bit_rate_flex_rate,0)))

print("\nTotal Capacity Shannon:", np.sum(bit_rate_shannon).round(2))
print("Average Capacity Shannon:", np.mean(np.ma.masked_equal(bit_rate_shannon,0).round(2)))
print("\n")