# Block comment/uncomment for each sub exercises

# 1. Accept two int values from the user and return their product.
# If the product is greater than 1000, then return their sum.
a = input("Enter first num: ")
a = int(a)
b = input("Enter second num: ")
b = int(b)
if a * b < 1000:
    print(a * b)
else:
    print(a - b)

# # 2. Given a range of numbers. Iterate from i-th number to the
# # end number and print the sum of the current number and previous number.
# b = 100
# c = input("enter n: 0<= n <=100 : ")
# c = int(c)
# sum = 0
# for i in range(c,b):
#     sum += i
#     print(sum)

# # 3. Given a list of ints, return True if first and last number of a list is same
# n = 10
# list1 = list(range(n))
# print(list1[0] == list1[n-1])

# # 4. Given a list of numbers, Iterate it and print
# # only those numbers which are divisible of 5
# n = 10
# list1 = list(range(n))
# for i in list1:
#     if i % 5 == 0:
#         print(i)

# # 5. Return the number of times that the string “Emma” appears anywhere in
# # the given string: “Emma is a good developer. Emma is also a writer”
# str = "Emma is a good developer. Emma is also a writer"
# print(str.count("Emma"))

# # 6. Given a two list of ints create a third list such that should contain
# # only odd numbers from the first list and even numbers from the second list#
# l1=list(range(10))
# l2 = list(range(10, 20))
# for i in l1:
#     if i % 2 == 1:
#         l1.remove(i)
# for i in l2:
#     if i % 2 == 0:
#         l2.remove(i)
# l1.extend(l2)
# print(l1)

# # 7. Given 2 strings, s1 and s2, create a new string by appending s2 in the middle of s1
# # https://www.adamsmith.haus/python/answers/how-to-insert-a-character-into-a-string-at-an-index-in-python
# s1 = "pippo"
# s2 = "pluto"
# mid = len(s1) // 2 # // : floor division, rounds the result down to the nearest whole number
# s3 = s1[:mid] + s2 + s1[mid:]
# print(s3)

# # 8. Given 2 strings, s1, and s2 return a new string made of the first, middle and last char each input string
# s1 = "pippo"
# s2 = "pluto"
# s3 = []
# for i in (s1, s2):
#     for j in range(len(i)):
#         if j == 0 or j == len(i) - 1 or j == (len(i) // 2):
#             s3.append(i[j])
# print(s3)

# # 9. Given a string input Count all lower case, upper case, digits, and special symbols
# str = input("stringa: ")
# count = [0, 0, 0, 0]  # lc up dg ss
# for i in str:
#     if i.islower(): count[0] += 1
#     if i.isupper(): count[1] += 1
#     if i.isdigit(): count[2] += 1
#     if i.isalnum() == False: count[3] += 1
# print(count)
# # Here's another option:  from StackOverflow
# #
# # s = 'some string'
# #
# # numbers = sum(c.isdigit() for c in s)
# # letters = sum(c.isalpha() for c in s)
# # spaces  = sum(c.isspace() for c in s)
# # others  = len(s) - numbers - letters - spaces

# # 10. Find all occurrences of “USA” in given string ignoring the case
# str = "USA is a big country. usa"
# print(str.lower().count("usa"))

# # 11. Given a string, return the sum and average of the digits that appear
# # in the string, ignoring all other characters
# st = "ciao come va sono 99 pippo 5 pluto foo3"
# count = 0
# sum = 0
# for i in st:
#     if i.isdigit():
#         count += 1
#         sum += int(i)
# print("sum " + str(sum) + "  avg " + str(sum / count))

# # 12. Given an input string, count occurrences of all characters within a string
# from collections import Counter
# stringa = "Given an input string, count occurrences of all characters within a string"
# print(Counter(stringa))

