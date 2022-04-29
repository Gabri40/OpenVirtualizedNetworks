import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# https://pandas.pydata.org/docs/getting_started/intro_tutorials/02_read_write.html#min-tut-02-read-write
# data stored as a csv file into a pandas DataFrame. pandas supports many different file formats or data sources out
# of the box (csv, excel, sql, json, parquet, …)
sales = pd.read_csv("00b_resources/sales_data.csv")
print(sales)

# block comment uncomment exercise points

# 1. Read Total profit of all months and show it using a line plot pandas provides the read_csv() function to read.
sales['total_profit'].plot()  # plotta direttamente i dataframe di pandas
plt.show()

# # 2. Get Total profit of all months and show line plot with the following Style
# # properties:
# # label = ’Profit data of last year’; color=’r’; marker=’o’;
# # markerfacecolor=’k’; linestyle=’–’; linewidth=3.
# sales['total_profit'].plot.line(title="Profit data of last year", ylabel="Profit", xlabel="Month", color="r",
#                                 marker="o", markerfacecolor="k",
#                                 linestyle="-", linewidth=3)
# plt.show()

# # 3. Read all product sales data and show it using a multiline plot
# sales.plot()
# plt.show()

# # 4. Read toothpaste sales data of each month and show it using a scatter plot
# # A scatter plot is a diagram drawn between two distributions of variables X and Y on a two dimensional plane.
# sales.plot.scatter(x="month_number", y="toothpaste", title="toothpaste sales data")  # x="" and y="" are the actual names of columns in the dataframe
# plt.show()

# # 5. Read sales data of bathing soap of all months and show it using a bar
# # chart. Save this plot to your hard disk
# sales.plot.bar(x="month_number", ylabel="sales", y="bathingsoap", title="bathing soap sales")
# plt.savefig("00b_set4_ex5_barplot.png")
# plt.show()

# # 6. Read the total profit of each month and show it using the histogram to
# # see most common profit ranges
# sales.plot.hist(column="total_profit")
# plt.show()

# # 7. Read Bathing soap facewash of all months and display it using the Subplot
# figure, axes = plt.subplots(1, 2)
# sales["facewash"].plot(ax=axes[0], xlabel="month", ylabel="sales", title="facewash")
# sales["bathingsoap"].plot(ax=axes[1], xlabel="month", ylabel="sales", title="bodywash",c="green")
# plt.show()
