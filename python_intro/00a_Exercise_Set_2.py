# block comment/uncomment for specifics exercise set points

# 1. Given two list. Create a third list by picking an odd-index element from
# the first list and even index elements from second.
listOne = [3, 6, 9, 12, 15, 18, 21]
listTwo = [4, 8, 12, 16, 20, 24, 28]
list3 = []
list3.extend(listOne[::2])  # odd indexes
list3.extend(listTwo[1::2])  # even indexes
print(list3)

# # 2. Given an input list removes the element at index 4 and add it to the 2nd
# # position and also, at the end of the list
# sampleList = [34, 54, 67, 89, 11, 43, 94]
# tmp = sampleList.pop(4)
# sampleList.insert(0, tmp)
# sampleList.append(tmp)
# print(sampleList)

# # Understanding slice notation
# # https://stackoverflow.com/questions/509211/understanding-slice-notation
# # 3. Given a list slice it into a 3 equal chunks and revert each list
# sampleList = [11, 45, 8, 23, 14, 12, 78, 45, 89]
# leng = len(sampleList) // 3
# for i in range(0, len(sampleList) - 1, leng):  # itera con step len(list)//3
#     print(sampleList[i:i + leng])

# # 4. Given a list iterate it and count the occurrence of each element and create
# # a dictionary to show the count of each element
# # https://docs.python.org/3/library/collections.html
# from collections import Counter
# sampleList = [11, 45, 8, 11, 23, 45, 23, 45, 89]
# dic = {}
# dic = Counter(sampleList)
# print(dic)
# print(dic[45])

# # 5. Given a two list of equal size create a set such that it shows the element
# # from both lists in the pair       # pair ???
# firstList = [2, 3, 4, 5, 6, 7, 8]
# secondList = [4, 9, 16, 25, 36, 49, 64]
# s = set()
# s.update(firstList)
# s.update(secondList)
# print(s)

# # 6. Given a following two sets find the intersection and remove those elements
# # from the first set
# firstSet = {23, 42, 65, 57, 78, 83, 29}
# secondSet = {57, 83, 29, 67, 73, 43, 48}
# print(firstSet)
# [firstSet.remove(i) for i in firstSet.intersection(secondSet)]  # inline for loops need []
# print(firstSet)

# # 7. Given two sets, Checks if One Set is Subset or superset of Another Set. if
# # the subset is found delete all elements from that set
# # https://www.toppr.com/guides/maths/sets/subsets-and-supersets/
# # a set A is referred to as the subset of another set B, if every element of
# # set A is also an element of set B.
# # Supersets are those sets which are defined by the following conditions: A ⊂ B and A ≠ B
# # When these two conditions are fulfilled, B is called a superset of set A.
# firstSet = {57, 83, 29}
# secondSet = {57, 83, 29, 67, 73, 43, 48}
# if firstSet.issubset(secondSet):
#     [secondSet.remove(i) for i in firstSet]
#     print("first is sub")
#     print(secondSet)
# elif secondSet.issubset(firstSet):
#     [firstSet.remove(i) for i in secondSet]
#     print("second is sub")
#     print(firstSet)

# # 8. Iterate a given list and Check if a given element already exists in a dictio-
# # nary as a key’s value if not delete it from the list
# rollNumber = [47, 64, 69, 37, 76, 83, 95, 97]
# sampleDict = {"Jhon": 47, "Emma": 69, "Kelly": 76, "Jason": 97}
# print(95 in sampleDict.values())  # non rimuove 95 ???????????????????????????????
# for i in rollNumber:
#     if i not in sampleDict.values():
#         rollNumber.remove(i)
# print(rollNumber)

# # 9. Given a dictionary get all values from the dictionary and add it in a list
# # but don’t add duplicates
# speed = {"’Jan’": 47, "Feb": 52, "’March ’": 47, "’April ’": 44,
#          "’May’": 52, "’June ’": 53, "’July ’": 54, "’Aug’": 44, "’Sept ’": 54}
# speedset = set(speed.values())  # A QUANTO PARE FARE set(iterable) rimuove duplicati e mette in ordine cresecente :D
# speedlist = list(speedset)
# print(speedlist)

# # 10. Remove duplicate from a list and create a tuple and find the minimum
# # and maximum number
# sampleList = [87, 52, 44, 53, 54, 87, 52, 53]
# tupl = tuple(set(sampleList))
# print(tupl[0])
# print(tupl[len(tupl) - 1])  # this set stuff is kinda sus
