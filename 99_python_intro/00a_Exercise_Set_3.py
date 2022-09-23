# block comment/uncomment for specifics exercise set points

import numpy as np

# 1. Create a 4X2 integer array and print its attributes
a = np.arange(8).reshape(2, 4)
print(a.shape)
print(a.ndim)
print(a.dtype.name)
print(a.size)

# # 2. Create a 5X2 integer array from a range between 100 to 200 such that the
# # difference between each element is 10
# a = np.arange(100, 200, 10).reshape(2, 5)
# print(a)

# # 3. Given the following numPy array, return the array of items in the third
# # column of each row
# a = np.array([(11, 22, 33), (44, 55, 66), (77, 88, 99)])
# for x in a:
#     print(x[2])

# # 4. Given the following numPy array, return the array of the odd rows and
# # the even columns
# a = np.array([(3, 6, 9, 12), (15, 18, 21, 24), (27, 30, 33, 36), (39, 42, 45, 48), (51, 54, 57, 60)])
# nr, nc = a.shape
# print(a)
# print("odd rows")
# [print(a[i]) for i in range(1, nr, 2)]
# print("even cols")
# [print(a.T[i]) for i in range(0, nc, 2)]  # iterate over the transposed array

# # 5. Add the following two numPy arrays and modify the result array by cal-
# # culating the square root of each element
# a = np.array([(5, 6, 9), (21, 18, 27)])
# b = np.array([(15, 33, 24), (4, 7, 1)])
# print(a + b)

# # 6. Sort following NumPy array:
# a = np.array([(34, 43, 73), (82, 22, 12), (53, 94, 66)])
# print(np.sort(a))

# # 7. Given the following numPy array, print the max of axis 0 and the min of
# # axis 1
# a = np.array([(34, 43, 73), (82, 22, 12), (53, 94, 66)])
# print(a)
# print("max row 0: " + str(np.max(a[0])))
# print("max col 0: " + str(np.max(a.T[0])))

# # 8. Given the following numPy array, delete the second column and insert the
# # following new column in its place.
# a = np.array([[34, 43, 73], [82, 22, 12], [53, 94, 66]])
# new_column = np.array([10, 10, 10])
# print(a)
# a = np.delete(a, 0, axis=1)  # axis=0 rows , axis=1 cols
# print()
# a = np.insert(a, 1, new_column, 1)
# print(a)
