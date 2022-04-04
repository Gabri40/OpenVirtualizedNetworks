import json

# 1. Write a Python program to convert JSON data to Python objects.
# json_obj = '{"Name": "David", "Class": "I", "Age": 6}'
# python_obj = json.loads(json_obj)
# print(python_obj["Name"])
# print(python_obj["Class"])
# print(python_obj["Age"])


# # 2. Write a Python program to convert Python objects (dictionary) to JSON
# # data.
# python_obj = {
#     "name": "dave",
#     "class": "i",
#     "age": 6
# }
# json_obj = json.dumps(python_obj)
# print(type(json_obj))  # json string

# # 3. Write a Python program to convert Python objects into JSON strings.
# # Print all the values.
# python_obj = {
#     "name": "dave",
#     "class": "i",
#     "age": 6
# }
# python_list = ["ciao", 3, "pippo"]
# python_int = 5
#
# json_obj = json.dumps(python_obj)
# json_list = json.dumps(python_list)
# json_int = json.dumps(python_int)
#
# print(json_obj+" | "+json_list+" | "+json_int)

# # 4. Write a Python program to convert Python dictionary objects (sort by
# # key) to JSON data. Print the object members with indent level 4.
# dic = {"a": 2, "c": 1, "b": 3}
# print(dic)
# json_str = json.dumps(dic, sort_keys=True, indent=4)
# print(json_str)

# # 5. Write a Python program to create a new JSON file from an existing JSON
# # file. Use the included json file ’states.json’ and create a new json file that
# # does not contain the ’area code’ field.
# with open("00b_resources/states.json") as json_f:
#     states_data = json.load(json_f)
# for i in states_data["states"]:
#     del i["area_codes"]
# with open("00b_resources/states_updated.json", "w") as new_f:
#     json.dump(states_data, new_f)
#     for i in states_data["states"]:
#         print(i.keys())
