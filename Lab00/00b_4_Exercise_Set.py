import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# # https://pandas.pydata.org/docs/getting_started/intro_tutorials/02_read_write.html#min-tut-02-read-write
# # data stored as a csv file into a pandas DataFrame. pandas supports many different file formats or data sources out
# # of the box (csv, excel, sql, json, parquet, …)
sales = pd.read_csv("00b_resources/sales_data.csv")

# # 1. Read Total profit of all months and show it using a line plot pandas provides the read_csv() function to read.
# sales['total_profit'].plot()  # plotta direttamente i dataframe di pandas
# plt.show()

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

