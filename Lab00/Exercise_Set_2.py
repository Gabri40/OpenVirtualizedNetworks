# 1. Given two list. Create a third list by picking an odd-index element from
# the first list and even index elements from second.
listOne = [3, 6, 9, 12, 15, 18, 21]
listTwo = [4, 8, 12, 16, 20, 24, 28]
list3 = []
list3.extend(listOne[::2])  # odd indexes
list3.extend(listTwo[1::2])  # even indexes
print(list3)

# 2. Given an input list removes the element at index 4 and add it to the 2nd
# position and also, at the end of the list
sampleList = [34, 54, 67, 89, 11, 43, 94]
tmp = sampleList.pop(4)
sampleList.insert(0, tmp)
sampleList.append(tmp)
print(sampleList)
