# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 17:42:31 2023

@author: Vishal Orsu
"""
import numpy as np # linear algebra
import pandas as pd # db processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

df = pd.read_csv("D:/RWorkshop/Uncleaned_Real_Estate_Sales_2001-2020_GL.csv")


df.head()
df.count()
df.describe()
df.shape
df.info()
df.nunique()
df.isnull().sum()

#data Cleaning

# Drop the specified columns
df.drop(['Address','Date Recorded', 'Non Use Code', 'Assessor Remarks', 'OPM remarks'], axis=1, inplace=True)
# Fill missing values in Residential Type column with 'Unknown'
df["Residential Type"] = df["Residential Type"].fillna("Unknown")
# Replace incorrect spelling of Residential Type
df["Property Type"] = df["Property Type"].replace("Reidential", "Residential")
df.dropna()

# Write the cleaned dataset to a new CSV file
df.to_csv('D:/RWorkshop/Real_Estate_Sales_2001_2020_GL.csv', index=False)

db = pd.read_csv("D:/RWorkshop/Real_Estate_Sales_2001-2020_GL.csv")
#=======1=====================ResearchQue1======================================
# How have real estate sales volumes and prices changed over time, and are there any discernible patterns or trends?
# Plot 1 & 2 single plots [sale]
# Create a subset of the db for the desired columns
db_subset = db[["List Year", "Assessed Value", "Sale Amount"]]

# Group the db by year and calculate the sum of sales amounts for each year
sales_volume = db_subset.groupby("List Year")["Sale Amount"].sum()

# Group the db by year and calculate the mean of assessed values for each year
sales_prices = db_subset.groupby("List Year")["Assessed Value"].mean()

# Create a time series plot of sales volumes over time
fig, ax1 = plt.subplots()
ax1.plot(sales_volume.index, sales_volume, label="Sales Volume", color='blue')
ax1.set_ylabel("Sales Volume (Millions of Dollars)")
ax1.set_title("Real Estate Sales Volume Over Time")
ax1.set_xlabel("Year")
ax1.set_xticks(np.arange(min(sales_volume.index), max(sales_volume.index)+1, 2))
plt.legend()
plt.show()

# Create a time series plot of sales prices over time
fig, ax2 = plt.subplots()
ax2.plot(sales_prices.index, sales_prices/1000000, label="Sales Price", color='red')
ax2.set_ylabel("Sales Price (Millions of Dollars)")
ax2.set_title("Real Estate Sales Price Over Time")
ax2.set_xlabel("Year")
ax2.set_xticks(np.arange(min(sales_prices.index), max(sales_prices.index)+1, 2))
plt.legend()
plt.show()

#    --------------Plot3 Combined Sales Vomues and Prices------------------
# Create a subset of the db for the desired columns
db_subset = db[["List Year", "Assessed Value", "Sale Amount"]]

# Group the db by year and calculate the sum of sales amounts for each year
sales_volume = db_subset.groupby("List Year")["Sale Amount"].sum()

# Group the db by year and calculate the mean of assessed values for each year
sales_prices = db_subset.groupby("List Year")["Assessed Value"].mean()

# Merge the sales volume and prices db frames by year
sales_db = pd.concat([sales_volume, sales_prices], axis=1)
sales_db.columns = ["Sales Volume", "Sales Price"]


# Calculate the overall average of assessed values for all years
overall_avg = db_subset["Assessed Value"].mean()


# Create a time series plot of sales volumes and prices over time
fig, ax = plt.subplots()
ax.plot(sales_db.index, sales_db["Sales Volume"], label="Sales Volume", color="blue")
ax.set_xlabel("Year")
ax.set_ylabel("Sales Volume (Millions of Dollars)", color="blue")
ax.set_xticks(range(2002,2022,2))
# Set the right y-axis limits
ax.set_ylim([0, 1.6])

ax2 = ax.twinx()
ax2.plot(sales_db.index, sales_db["Sales Price"]/1000000, label="Sales Price", color="red")
ax2.set_ylabel("Sales Price (Millions of Dollars)", color="red")
# Set the right y-axis limits
ax2.set_ylim([0, 1.6])
# Plot the average line
ax2.axhline(y=overall_avg/1000000, color='black', linestyle='--', label="Average Sales Price")
ax.set_title("Real Estate Sales Volumes and Prices Over Time")
# Add legend
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc="upper left")
plt.show()

#===2===============================ResearchQue2===============================
# What are the most common types of properties sold, and how do their prices compare across different locations and time periods?


# Extract relevant columns
db = db[["List Year", "Town", "Sale Amount", "Assessed Value", "Property Type", "Residential Type"]]


# Replace incorrect spelling of Residential Type
db["Property Type"] = db["Property Type"].replace("Reidential", "Residential")

#-------------STATS----------
# Calculate statistics for most common property types
types = db["Property Type"].value_counts().head(5).index.tolist()
stats = db.groupby("Property Type")[["Assessed Value", "Sale Amount"]].agg(["mean", "median", "std"])
stats = stats.loc[types]
stats["Count"] = db["Property Type"].value_counts().loc[types]

# Display statistics as a table
print(stats)
#------------Plots----------R2-1----
db["Property Type"].fillna("Unknown", inplace=True)

# Create a bar chart to show the most common property types sold in Connecticut
plt.figure(figsize=(12,6))
ax = sns.countplot(x="Property Type", data=db, order=db["Property Type"].value_counts().index, edgecolor= 'black')
plt.title("Most Common Property Types Sold in Connecticut from 2001 to 2020")
plt.xlabel("Property Type")
plt.ylabel("Number of Properties Sold")
plt.ylim(0, 700000 )
# Format y-axis ticks in k's
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:.0f}k'.format(y/1000)))

# Format numbers on top of bars in k's and percentages
for p in ax.patches:
    value = p.get_height()
    text = f'{value/1000:.1f}k\n({value/db.shape[0]*100:.1f}%)' if value >= 1000 else f'{value}\n({value/db.shape[0]*100:.1f}%)'
    ax.annotate(text, (p.get_x() + p.get_width()/2, p.get_height()), ha='center', va='center', xytext=(0, 15), textcoords='offset points', fontsize=12)


plt.show()




#-------------------R2-2-------------------------------------------------------
 # Filter the data to only include residential properties
residential_db = db[db['Property Type'] == 'Residential']

# Group the data by residential type and year, and calculate the average sale price for each group
avg_prices = residential_db.groupby(['Residential Type', 'List Year'])['Sale Amount'].mean().reset_index()

# Pivot the table to show the average sale price for each year by residential type
avg_prices_table = avg_prices.pivot(index='List Year', columns='Residential Type', values='Sale Amount')

# Round the table to 2 decimal places
avg_prices_table = avg_prices_table.round(2)

# Display the table
print(avg_prices_table)


# Filter the data to only include residential properties
residential_db = db[db['Property Type'] == 'Residential']

# Group the data by residential type and year, and calculate the average sale price for each group
avg_prices = residential_db.groupby(['Residential Type', 'List Year'])['Sale Amount'].mean().reset_index()

# Create a line plot for each residential type
fig, ax = plt.subplots(figsize=(10, 6))
for r_type in avg_prices['Residential Type'].unique():
    plot_data = avg_prices[avg_prices['Residential Type'] == r_type]
    ax.plot(plot_data['List Year'], plot_data['Sale Amount'], label=r_type)

# Set the plot title and axis labels
ax.set_title('Average Sale Price of Residential Properties Over Time')
ax.set_xlabel('Year')
ax.set_ylabel('Average Sale Price ($ in Million)')

# Add a legend
ax.legend()

# Display the plot
plt.show()
#--------------------R2-3-------------------------------------
#----------------Stats-------------------
# Select only residential properties
residential_db = db[db['Property Type'] == 'Residential']

# Group by town and calculate mean sale amount
residential_sales = residential_db.groupby('Town')['Sale Amount'].mean()

# Sort by average sale amount and take top 10
top_10_towns = residential_sales.sort_values(ascending=False)[:10]

# Print top 10 towns
print("Top 10 Towns with Highest Average Sale Amount:")
for i, town in enumerate(top_10_towns.index):
    print("{:2}. {:20} ${:,.0f}".format(i+1, town, top_10_towns[town]))

residential_db = db[db['Property Type'] == 'Residential']
#----------plot
# Group by town and aggregate sale amount
residential_sales = residential_db.groupby('Town')['Sale Amount'].mean()/1000000

# Sort by descending order and take top 10
residential_top10 = residential_sales.sort_values(ascending=False)[:10]

# Create bar plot
plt.figure(figsize=(12,6))
bars = plt.bar(residential_top10.index, residential_top10.values)

# Add gradient to bars
for i, bar in enumerate(bars):
    bar.set_color(plt.cm.get_cmap('coolwarm')(i/len(bars)))

plt.title('Average Sale Amount of Top 10 Residential Towns in Connecticut')
plt.xlabel('Town')
plt.ylabel('Sale Amount (in millions)')
plt.ticklabel_format(style='plain', axis='y')
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:.1f}M'.format(x)))

# Add labels to the bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, '{:.2f}M'.format(height), ha='center', va='bottom', fontsize=10)

plt.show()


#---------------Sale amount vs Year



# group the data by year and calculate the total sale amount for each year
yearly_sale_amount = db.groupby('List Year')['Sale Amount'].sum()

# calculate the average sale amount across all years
average_sale_amount = yearly_sale_amount.mean()

# generate a color gradient for the barplot
colors = sns.color_palette("Blues_r", len(yearly_sale_amount.index))

# create a bar plot of the yearly sale amounts
plt.figure(figsize=(12, 6))
ax = sns.barplot(x=yearly_sale_amount.index, y=yearly_sale_amount.values/1000000, 
                 palette=colors, edgecolor='#000000')

# add a horizontal line to show the average sale amount
ax.axhline(average_sale_amount/1000000, color='#FFA500', ls='--', lw=2)

# set the x-axis labels and rotate them 90 degrees for better readability
plt.xticks(rotation=90)

# set the y-axis labels to show the values in millions with a dollar sign
formatter = ticker.FormatStrFormatter('$%.1fM')
ax.yaxis.set_major_formatter(formatter)

# set the title and labels for the plot
plt.title('Yearly Sale Amount')
plt.xlabel('Year')
plt.ylabel('Sale Amount (in millions)')

# add a grid to make it easier to read the values
plt.grid(axis='y', linestyle='--', alpha=0.7)

# display the plot
plt.show()



#------------------Assessed Value vs Years

# group the data by year and calculate the total assessed amount for each year
yearly_assessed_amount = db.groupby('List Year')['Assessed Value'].sum()

# calculate the average assessed amount across all years
average_assessed_amount = yearly_assessed_amount.mean()

# define a color map for the gradient effect
cmap = sns.color_palette("rocket_r", len(yearly_assessed_amount))

# create a bar plot of the yearly assessed amounts with a gradient effect
plt.figure(figsize=(12, 6))
ax = sns.barplot(x=yearly_assessed_amount.index, y=yearly_assessed_amount.values/1000000,
                 palette=cmap, edgecolor='#000000')

# add a horizontal line to show the average assessed amount
ax.axhline(average_assessed_amount/1000000, color='#FFA500', ls='--', lw=2)

# set the x-axis labels and rotate them 90 degrees for better readability
plt.xticks(rotation=90)

# set the y-axis labels to show the values in millions with a dollar sign
formatter = ticker.FormatStrFormatter('$%.1fM')
ax.yaxis.set_major_formatter(formatter)

# set the title and labels for the plot
plt.title('Yearly Assessed Amount')
plt.xlabel('Year')
plt.ylabel('Assessed Amount (in millions)')

# add a grid to make it easier to read the values
plt.grid(axis='y', linestyle='--', alpha=0.7)

# display the plot
plt.show()


#----------------SCATTER PLOT of ASSESSED VALUE AND SALE AMOUNT----------------
# select the columns for the scatter plot
x = db["Assessed Value"]
y = db["Sale Amount"]

# create the scatter plot
plt.scatter(x, y)
plt.xlabel("Assessed Value")
plt.ylabel("Sale Amount(in Millions of $")
plt.title("Scatter plot of Assessed Value vs Sale Amount")
plt.show()
#=================================Correlation==================================
# select the columns for which you want to calculate the correlation matrix
columns = ["Assessed Value", "Sale Amount", "Gain/loss", "Sale Rankings", "Sales Ratio"]

# calculate the correlation matrix
correlation_matrix = db[columns].corr()

# create correlation matrix
corr = db.corr()

# create heatmap
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.show()

#==============================================================================




