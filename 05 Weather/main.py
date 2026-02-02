# with open("weather_data.csv") as data_file:
#     data = data_file.readlines()
#     print(data)

# import csv
# with open("weather_data.csv") as data_file:
#     data = csv.reader(data_file)
#     print(data) # displays object location
#     temperatures = []
#     # for row in data:
#     #     print(row)
"""
 csv.reader is a one-time iterator.
Once you've looped through it, the file pointer is moved to the end of the file, and there’s nothing more to read.
"""
#     for row in data:
#         if row[1] != "temp":
#             temperatures.append(int(row[1]))
#     print(temperatures)

import pandas

read = pandas.read_csv("weather_data.csv")
# print(read)
# print(read["temp"])

# print(type(read))
# print(type(read["temp"]))

data_dict = read.to_dict()
print(data_dict)

# temp_list = read["temp"].to_list()
# print(temp_list)
# print(len(temp_list))
#
# avg = sum(temp_list) / len(temp_list)
# print(avg)

# print(read["temp"].max())
# print(read["temp"].mean())

# Get Data in Columns

# print(read["condition"])  # Both gives same output
# print(read.condition)

# Get Data in row
print(read[read.day == "Monday"])

# Get data row where a temp is maximum
print(read.temp == read.temp.max())

# data = pandas.DataFrame(data_)
