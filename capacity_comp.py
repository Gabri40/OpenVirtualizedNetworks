from random import shuffle
from network import *


base=[9000,36000,39664.41]
b2=[8800,32800,34403.87]
noise=[7800,31200,32325.64]

#base
plt.bar("Fixed",9000,color="#737373")
plt.bar("Fixed ",8800,color="black")

plt.bar("Flex",36000,color="#737373")
plt.bar("Flex ",32800 ,color="black")

plt.bar("Shannon",39664.41,color="#737373")
plt.bar("Shannon ",34403,color="black")

plt.ylabel('Total Capacity')
plt.savefig('Plots/Capacity_B2.png',transparent=True)
plt.show()

#base
plt.bar("Fixed",9000,color="#737373")
plt.bar("Fixed ",7800,color="black")

plt.bar("Flex",36000,color="#737373")
plt.bar("Flex ",31200,color="black")

plt.bar("Shannon",39664.41,color="#737373")
plt.bar("Shannon ",32325,color="black")


plt.ylabel('Total Capacity')
plt.savefig('Plots/Capacity_NF.png',transparent=True)
plt.show()

