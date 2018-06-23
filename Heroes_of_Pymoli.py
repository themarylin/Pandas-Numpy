import pandas as pd
import numpy as np
import json
import os
import csv

#load json data
data_path = os.path.join('Resources','purchase_data.json')
data_path

#open json file and print json data to find keys and understand data
with open (data_path) as game_json:
    game_data = json.load(game_json)


#convert data into panda dataframe
game_pd = pd.DataFrame(game_data)
game_pd.head(3)

#finding number of rows, which is equivalent to number of players
numbers = game_pd['SN'].nunique()
num_players = {'Total Players':[numbers]}
num_pd = pd.DataFrame.from_dict(num_players)
num_pd

#run calculations for summary
num_items = len(game_pd['Item ID'].unique())
price_mean = game_pd['Price'].mean()
purchase_count = game_pd['Price'].count()
total_purchase = game_pd['Price'].sum()

total_analysis = {'Number of Unique Items':[num_items], 'Average Purchase Price':[price_mean], 'Total Number of Purchases':[purchase_count], 'Total Revenue':[total_purchase]}
total_analysis_pd = pd.DataFrame.from_dict(total_analysis)
total_analysis_pd = total_analysis_pd[['Number of Unique Items','Average Purchase Price', 'Total Number of Purchases','Total Revenue']]

#data formatting
total_analysis_pd = total_analysis_pd.round(2)
total_analysis_pd['Average Purchase Price'] = total_analysis_pd['Average Purchase Price'].map("${:,.2f}".format)
total_analysis_pd['Total Revenue'] = total_analysis_pd['Total Revenue'].map("${:,.2f}".format)
total_analysis_pd

#create series by gender, sort and then grouped
gender_pd = game_pd['Gender']
gender_sorted = gender_pd.sort_values()
gender_grouped = gender_sorted.value_counts()

percent = []
gender_demo = gender_grouped.to_frame(name = 'Count')

#calculate percentage of gender demographics
for x in gender_demo['Count']:
    percent.append((x/game_pd.shape[0])*100)

#add another column to the current dataframe to include percentages
gender_demo['Percent'] = percent
gender_demo = gender_demo.round(2)
gender_demo['Percent'] = gender_demo['Percent'].map('{:,.2f}%'.format)
gender_demo

#Purchasing Analysis by gender
purchase_gender = game_pd.loc[:,['Gender','Price']]
purchase_count = purchase_gender.groupby(['Gender']).count()['Price'].rename('Purchase Count')

purchase_avgerage= purchase_gender.groupby(['Gender']).mean()['Price'].rename('Average Purchase Price')

purchase_sum = purchase_gender.groupby(['Gender']).sum()['Price'].rename('Total Purchase Value')

purchase_norm = purchase_sum/gender_demo['Count']
purchase_norm = pd.DataFrame({"Normalized Totals":purchase_norm})

#dataframe formatting
purchase_total = pd.concat([purchase_count, purchase_avgerage, purchase_sum, purchase_norm], axis = 1)
purchase_total = purchase_total.round(2)
purchase_total['Average Purchase Price'] = purchase_total['Average Purchase Price'].map("${:,.2f}".format)
purchase_total['Total Purchase Value'] = purchase_total['Total Purchase Value'].map("${:,.2f}".format)
purchase_total['Normalized Totals'] = purchase_total['Normalized Totals'].map("${:,.2f}".format)

#display table
purchase_total

#establish age groups
age_group = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

# Categorize the existing players using the age bins
game_pd["Age Ranges"] = pd.cut(game_pd["Age"], age_group, labels=group_names)

#calculations for age ranges
age_demo_totals = game_pd['Age Ranges'].value_counts()
age_demo_percents = age_demo_totals/numbers * 100
age_demo_percents = age_demo_percents.map('{:,.2f}%'.format)
age_demo = pd.DataFrame({'Total Count':age_demo_totals, 'Percentage of Players':age_demo_percents} )
age_demo = age_demo.round(2)

age_demo = age_demo.sort_index()
age_demo

#calculations for age purchase summary
age_purchase_count = game_pd.groupby(['Age Ranges']).count()['Price'].rename('Purchase Count')
age_purchase_average = game_pd.groupby(['Age Ranges']).mean()['Price'].rename('Average Purchase Price')
age_purchase_total = game_pd.groupby(['Age Ranges']).sum()['Price'].rename('Total Purchase Value')

age_purchase_normal = age_purchase_total/age_demo['Total Count']

# Convert to DataFrame
age_data = pd.DataFrame({"Purchase Count": age_purchase_count, "Average Purchase Price": age_purchase_average, "Total Purchase Value": age_purchase_total, "Normalized Totals": age_purchase_normal})

#data formatting for age demographics
age_data = age_data.round(2)
age_data['Average Purchase Price'] = age_data['Average Purchase Price'].map('${:,.2f}'.format)
age_data['Normalized Totals'] = age_data['Normalized Totals'].map('${:,.2f}'.format)
age_data['Total Purchase Value'] = age_data['Total Purchase Value'].map('${:,.2f}'.format)

age_data = age_data.loc[:, ["Purchase Count", "Average Purchase Price", "Total Purchase Value", "Normalized Totals"]]
age_data = age_data.sort_index()
age_data

#run calculations 
user_total = game_pd.groupby(["SN"]).sum()["Price"].rename("Total Purchase Price")
user_average = game_pd.groupby(["SN"]).mean()["Price"].rename("Average Purchase Price")
user_count = game_pd.groupby(["SN"]).count()["Price"].rename("Purchase Count")

#convert to dataframe
user_data = pd.DataFrame({'Total Purchase Price':user_total, 'Average Purchase Price':user_average,'Purchase Count':user_count})

#sort the data by largest purchase value
user_sorted = user_data.sort_values("Total Purchase Price", ascending = False)

#data format
user_sorted['Total Purchase Price'] = user_sorted['Total Purchase Price'].map('${:,.2f}'.format)
user_sorted['Average Purchase Price'] = user_sorted['Average Purchase Price'].map('${:,.2f}'.format)

user_sorted = user_sorted.loc[:,['Purchase Count','Total Purchase Price','Average Purchase Price']]
top_spenders = user_sorted.head(5)
top_spenders

#extract item data
item_data = game_pd.loc[:,['Item ID','Item Name','Price']]

#calculations for most popular items
average_item_price = item_data.groupby(['Item ID','Item Name']).mean()['Price'].rename('Average Item Price')
item_count = item_data.groupby(['Item ID','Item Name']).count()['Price'].rename('Purchase Count')
total_item_purchase = item_data.groupby(['Item ID','Item Name']).sum()['Price'].rename('Total Purchase Value')

item_data_pd = pd.DataFrame({'Purchase Count':item_count,'Average Item Price':average_item_price,'Total Purchase Value':total_item_purchase})

popular_item = item_data_pd.sort_values(by = 'Purchase Count', ascending = False)
popular_item['Average Item Price'] = popular_item['Average Item Price'].map('${:,.2f}'.format)
popular_item['Total Purchase Value'] = popular_item['Total Purchase Value'].map('${:,.2f}'.format)
popular_item = popular_item.head(5)
popular_item

#calculations for most profitable item
item_profitable = item_data_pd.sort_values(by = 'Total Purchase Value', ascending = False)
item_profitable['Average Item Price'] = item_profitable['Average Item Price'].map('${:,.2f}'.format)
item_profitable['Total Purchase Value'] = item_profitable['Total Purchase Value'].map('${:,.2f}'.format)
item_profitable = item_profitable.head(5)
item_profitable

#export data tables to different csv files
total_analysis_pd.to_csv('Output\\summary.csv')
gender_demo.to_csv('Output\\gender_demographics.csv')
purchase_total.to_csv('Output\\gender_demographics_summary.csv')
age_demo.to_csv('Output\\age_demographics.csv')
age_data.to_csv('Output\\age_purchase_summary.csv')
top_spenders.to_csv('Output\\top_spenders.csv')
popular_item.to_csv('Output\\popular_item.csv')
item_profitable.to_csv('Output\\item_profitable.csv')