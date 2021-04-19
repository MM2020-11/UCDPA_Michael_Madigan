# Michael Madigan UDC PA  DA project 18April 2021
# Project for assiment of UCS PA data analytics course, March/April 2021
# Program reads three data sources, cleans, merges and plots the data
#

# import useful libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

# read in csv file with world wide covid data
# data downloaded from https://ourworldindata.org/coronavirus-source-data
# import csv file into a Pandas DataFrame
# Download data from site
URL_Covid_dataset = r'https://covid.ourworldindata.org/data/owid-covid-data.csv'
#df1_from_web = pd.read_csv(URL_Covid_dataset)


#Select data source - if offline then use local version
#df1 = df1_from_web   # use this data source when on-line is available
df1 = pd.read_csv("owid-covid-data.csv") # directly read a downloaded version if web version is not available

print(df1.head())   # view top lines of data
print(df1.shape)    # check shape number of row and columns
print(df1.dtypes)   # date is an object

# inspect data to determine which columns contain valuable information for this project
# as the header file is very wide I list the column headings
# Display all column names with a "for loop" instead of print('df1 columns', df1.columns) to get a neater print
for idx, column in enumerate(df1.columns):
    print(idx, column)
# From the column inspection I determine which columns are relevant to this project
# Relevant columns are : 0 iso_code,  # 3 date,  # 5 new_cases

selected_cols = ['iso_code', 'date', 'new_cases']
#df_web = pd.read_csv(URL_Covid_dataset, usecols=selected_cols)

# from the list gathered the required columns - separate columns ino a new dataframe
# this drops the unneeded columns
selected_cols = ['iso_code', 'date', 'new_cases']
df_iso_date_new_cases = df1.loc[:, selected_cols] # using the .loc function

print("Line 44 header of new dataframe with only three necessary columns")
print(df_iso_date_new_cases.head())

print("Line 48 data types of new df1")
print(df_iso_date_new_cases.dtypes)
# from this we see that the "date" column is an object, this should be changed to a date field

# set the date column to a date format using .to_date() function
# set date format to YMD.
df_iso_date_new_cases['date'] = pd.to_datetime(df_iso_date_new_cases['date'], yearfirst=True, format="%Y/%m/%d")


print("Line 56 tail of new df1 with date column format set to date YMD ")
print(df_iso_date_new_cases.tail())

#Check data for NaN
count_NaN = df_iso_date_new_cases[selected_cols].isna().sum()
print("line 61 Count of NaNs in df_iso_date_new_cases dataframe ")
print(count_NaN)

# from the Nan count we see quantity of NaN's in the new_cases column. we need to
# clean the NaN's and replace with zeros.
df_iso_date_new_cases_no_NaN = df_iso_date_new_cases.fillna(0)

#Repeated Check data for NaN to ensure fillna worked as planned
count_NaN = df_iso_date_new_cases_no_NaN[selected_cols].isna().sum()
print("Line 70 Count of NaNs removed in df_iso_date_new_cases dataframe ")
print('count_NaN', count_NaN)

# Select only the rows that pertain to ireland, ISO code = IRL
df_IRL = df_iso_date_new_cases_no_NaN.loc[df_iso_date_new_cases_no_NaN["iso_code"] == 'IRL', :]
print("line 75 data frame header cleaned for Ireland, IRL")
print(df_IRL.head())
print("check shape of data frame for Ireland to ensure reasonable data")
print(df_IRL.shape)
# save to a comma separated value file for inspection
df_IRL.to_csv(r'export_df_IRL.csv', index=False, header=True)



#=========================================================================
print("===============================================================")
print("=======Start process again for another different dataset ======")
print("===============================================================")
#=========================================================================

# read and clean a second file
# the file is collected by the Irish government and a mobile phone company
# use phone GPS data to determine people movement
# file name is Staying Local Indicator SLI01.20210330T200311.csv
#https://ws.cso.ie/public/api.jsonrpc?data=%7B%22jsonrpc%22:%222.0%22,%22method%22:%22PxStat.Data.Cube_API.ReadDataset%22,%22params%22:%7B%22class%22:%22query%22,%22id%22:%5B%5D,%22dimension%22:%7B%7D,%22extension%22:%7B%22pivot%22:null,%22codes%22:false,%22language%22:%7B%22code%22:%22en%22%7D,%22format%22:%7B%22type%22:%22JSON-stat%22,%22version%22:%222.0%22%7D,%22matrix%22:%22SLI01%22%7D,%22version%22:%222.0%22%7D%7D

#read in csv file with staying local data ( in event internet not available )
df_SLI = pd.read_csv("SLI01.20210415T090423.csv")

print('df_SLI head = ', df_SLI.head())   # view top lines of data
print('df_SLI shape = ', df_SLI.shape)   # check shape number of row and columns
print('df_SLI dtypes = ', df_SLI.dtypes)   # check data types

# get all column names
for idx, column in enumerate(df_SLI.columns):
    print(idx,column)
# from the column information we see which columns are relevant
#0 Statistic
#2 Date
#2 County
#3 UNIT
#4 VALUE
#5 Date2

required_cols = ['Date', 'County', 'VALUE']
df_SLI_Date_County_Value = df_SLI.loc[:, required_cols]

# during debuggibg found and clean an error in date format for 20Dec20
# data cleaned here
df_SLI_Date_County_Value['Date'] = df_SLI_Date_County_Value['Date'].str.replace('2020 December20', '2020 December 20')

print("Line 121 header of new dataframe with only three necessary columns")
print(df_SLI_Date_County_Value.head())

#Check data for NaN
count_NaN = df_SLI_Date_County_Value[required_cols].isna().sum()
print("Line 126 Count of NaNs in df_iso_date_new_cases dataframe ")
print("\n count_NaN in SLI df =\n", count_NaN, '\n')

#initially just removed NaN with zero however a few missing plot points dropped to zero
# better to interpolate as only a few few small quantity of NaN's
df_SLI_Date_County_Value = df_SLI_Date_County_Value.interpolate(axis=0)

# from the Nan count we fill nan's - not required use interpolation
df_SLI_Date_County_Value_No_NaN = df_SLI_Date_County_Value.fillna(0)

#Repeated Check data for NaN to ensure fillna worked as planned
count_NaN = df_SLI_Date_County_Value_No_NaN[required_cols].isna().sum()
# Count of NaNs removed in df_iso_date_new_cases dataframe
print('df_SLI_Date_County_Value_No_NaN = count_NaN = ', count_NaN)


print("Line 142 data frame cleaned for State" )
print(df_SLI_Date_County_Value_No_NaN.head())
# Check shape of data frame for Ireland to ensure reasonable data
print(df_SLI_Date_County_Value_No_NaN.shape)

# format as date
df_SLI_Date_County_Value_No_NaN['New_Date'] = pd.to_datetime(df_SLI_Date_County_Value_No_NaN['Date'], format="%Y %B %d")

# Select only the rows that pertain to all ireland i.e. State, County = State
df_SLI_state = df_SLI_Date_County_Value_No_NaN.loc[df_SLI_Date_County_Value_No_NaN["County"] == 'State', :]

df_SLI_state.to_csv(r'export_df_SLI_state.csv', index=False, header=True)

#===================================================================================
#
# Read in a third file
#
# read in csv file with
# file from Irish gov web site https://data.cso.ie/
# Persons on the Live Register, in receipt of the Pandemic Unemployment Payment,
# in receipt of the Temporary Wage Subsidy Scheme and Total excluding overlaps.
#
#===================================================================================

df_pup = pd.read_csv("LRW01.20210413T150452.csv")
print('df_pup head = ', df_pup.head())   # view top lines of data
print('df_pup shape = ', df_pup.shape)   # check shape number of row and columns
print('df_pup dtypes = ', df_pup.dtypes)   # check data types

# convert YYYYWww to the Monday the starting date on the week.
# This will allow comparison woth other data sets
# expand the YYYYWww to YYYYWww-dd by adding a -1
df_pup['first_Monday'] = df_pup['Week'] + '-1'
#convert the first_Monday string to a date
df_pup['first_Monday_date'] = pd.to_datetime(df_pup['first_Monday'], yearfirst=True, format="%YW%W-%w")
# export file for inspection - only required during debugging
df_pup.to_csv(r'export_df_pup.csv', index=False, header=True)
# print header to inspect
print('df_pup head = ', df_pup.head())   # view top lines of data

# clean data in pup dataframe
# select the required columns
required_cols = ['Statistic', 'Age Group', 'Sex', 'VALUE', 'first_Monday_date']
df_pup1 = df_pup.loc[:, required_cols]

print('\n df_pup1 head = \n', df_pup1.head())   # view top lines of data

# Select only the relevant rows
df_pup1 = df_pup1.loc[df_pup1["Statistic"] == 'Persons in receipt of the Pandemic Unemployment Payment', :]
df_pup1 = df_pup1.loc[df_pup1["Age Group"] == 'All ages', :]
df_pup1 = df_pup1.loc[df_pup1["Sex"] == 'Both sexes', :]

print('\n df_pup1 head = \n', df_pup1.head())   # view top lines of data

# reduce data further
required_cols = ['Statistic', 'VALUE', 'first_Monday_date']
df_pup1 = df_pup1.loc[:, required_cols]

# export file for inspection - only required during debugging
df_pup1.to_csv(r'export_df_pup1.csv', index=False, header=True)

#Check data for NaN
print('\n check for Nan in df_pup1 = \n ', df_pup1[required_cols].isna().sum(), '\n')



#===================================================================================
#
#
#                        MERGE SECTION - First
#
#
#===================================================================================
print('df_IRL dtypes = ', df_IRL.dtypes)
print('df_SLI_state dtypes = ', df_SLI_state.dtypes)

# merge the new_cases and SLI dataframes
df_cases_County = pd.merge(df_IRL, df_SLI_state, left_on='date', right_on='New_Date', how='left')

print('\n df_cases_County head = ', df_cases_County.head())
print('\n df_cases_County shape = ', df_cases_County.shape)


required_cols = ['date', 'Date', 'County', 'VALUE', 'new_cases']
df_cases_County_2 = df_cases_County.loc[:, required_cols]

df_cases_County_cleaned = df_cases_County_2 = df_cases_County_2.fillna(0)

#date_cols = ['date','Date']
date_cols = ['date']

# remove any 'date' field that are zero
df_cases_County_cleaned = (df_cases_County_2[(df_cases_County_2[date_cols] != 0).all(axis=1)])

# add a new column just date for later plotting without the time values - just_date
df_cases_County_cleaned['just_date'] = df_cases_County_cleaned['date'].dt.date

print('\ndf_cases_County_cleaned head = \n', df_cases_County_cleaned.head())
print('\ndf_cases_County_cleaned tail = \n', df_cases_County_cleaned.tail())

# save files for debugging
df_cases_County_cleaned.to_csv(r'export_df_cases_County_cleaned.csv', index=False, header=True)
df_cases_County_2.to_csv(r'export_merge.csv', index=False, header=True)

correlation = df_cases_County_2['VALUE'].corr( df_cases_County_2['new_cases'], method='pearson')
print('\n Pearson correlation coefficient for new cases and SLI = ', correlation)

#===================================================================================
#
#
#                        MERGE SECTION - Second
#
#
#===================================================================================
# merge the new_cases and pup dataframes
df_cases_pup1 = pd.merge(df_IRL, df_pup1, left_on='date', right_on='first_Monday_date', how='left')
df_cases_pup1 = df_cases_pup1.drop(labels=[0], axis=0)

# as the pup df is missing many data points between dates interpolate to construct
# a clearer picture of the trend

df_cases_pup1.to_csv(r'export_df_cases_pup1.csv', index=False, header=True)
df_pup2 = df_cases_pup1.interpolate(axis=0)
df_pup2.to_csv(r'export_df_pup2.csv', index=False, header=True)

print('\n df_cases_pup1 head = ', df_cases_pup1.head())
print('\n df_cases_pup1 shape = ', df_cases_pup1.shape)
# save files for debugging
df_cases_pup1.to_csv(r'export_df_cases_pup1.csv', index=False, header=True)


correlation = df_pup2['VALUE'].corr( df_pup2['new_cases'], method='pearson')
print('\n Correlation between pup payments and new cases = ', correlation )

#===================================================================================
#
#                       Start plotting
#
#===================================================================================

# collect columns to be plotted to list for the matplotlib functions
new_cases_list = df_cases_County_cleaned['new_cases'].tolist()
Value_list = df_cases_County_cleaned['VALUE'].tolist()
date_list = df_cases_County_cleaned['just_date'].tolist()

pup_date_list = df_pup2['date'].tolist()
pup_VALUE_list = df_pup2['VALUE'].tolist()


fig, ax1 = plt.subplots(1, 1, figsize=(10, 5))
ax1.set_title("Plot of Irish covid cases compared to Staying Local metric")
ax1.set_xlabel("Reported dates")
ax1.set_ylabel('Number of new covid cases')
#ax1.annotate('A',  xytext=(1, 50),xy=(20, 75), arrowprops=dict(facecolor='blue', shrink=0.05))

ax1.plot(date_list, new_cases_list, color='tab:blue', label="new cases")



# add an arrow annotation to plot
ax1.annotate('Large spike', xy=(.73, .95),  xycoords='axes fraction',
            xytext=(0.54, 0.8), textcoords='axes fraction',
            arrowprops=dict(facecolor='blue', shrink=0.05),
            horizontalalignment='right', verticalalignment='top',
            )


ax1a = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax1a.plot(date_list, Value_list, color='tab:orange', label="Staying Local")
ax1a.set_ylabel('Percentage of people staying local')
ax1a.set_ylim(50, 80) # limits set to best present data

ax1.legend(loc='upper left')  # Improve performance by instructing legend location




#============================================================================================
# Second plot
#============================================================================================


fig, ax2 = plt.subplots(1,1, figsize=(10, 5))

ax2.set_title("Plot of Irish covid cases compared to numbers receiving pup")
ax2.set_xlabel("Reported dates")
ax2.set_ylabel('Number of new covid cases')
ax2.annotate('A',  xytext=(1, 50),xy=(20, 75), arrowprops=dict(facecolor='blue', shrink=0.05))


ax2.plot(date_list, new_cases_list, color='tab:blue', label="new cases")
#ax2.plot(date_list, Value_list, color='tab:red', label="Staying local")
#ax2.plot(pup_date_list, pup_VALUE_list, color='tab:red', label="pup")
ax2.legend(loc='upper left')  # Improve performance by instructing legend location

# add an arrow annotation to plot
ax2.annotate('Large spike', xy=(.73, .95),  xycoords='axes fraction',
            xytext=(0.54, 0.8), textcoords='axes fraction',
            arrowprops=dict(facecolor='blue', shrink=0.05),
            horizontalalignment='right', verticalalignment='top',
            )


ax2b = ax2.twinx()  # instantiate a second axes that shares the same x-axis
ax2b.plot(pup_date_list, pup_VALUE_list, color='tab:red', label="pup")
ax2b.set_ylabel('No people receiving pandemic payments')

ax2.legend(loc='upper left')  # Improve performance by instructing legend location

# set start and end points for vertical line, convert date limits to date/number for graph
# three point of interest when data jumped
px1 = dt.datetime.strptime('2020-04-10', '%Y-%m-%d')
px2 = dt.datetime.strptime('2020-10-20', '%Y-%m-%d')
px3 = dt.datetime.strptime('2021-01-02', '%Y-%m-%d')

# draw a line on chart at the mean value slight above the dashed line
ax2.vlines(px1, 100,8000, label='ax2 h', ls='--', color='g')
line_text1 = " Large increase"
ax2.text(px1, 4000, line_text1)

ax2.vlines(px2, 100,4000, label='ax2 h', ls='--', color='g')
line_text2 = " Step increase"
ax2.text(px2, 4000, line_text2)

ax2.vlines(px3, 100,8000, label='ax2 h', ls='--', color='g')
line_text3 = " Christmas bounce"
ax2.text(px3, 50, line_text3)


#=================================================
# plot 3
#=================================================
# plot pup and average of pup
fig, ax3 = plt.subplots(1, 1, figsize=(10, 5))
ax3.plot(pup_date_list, pup_VALUE_list, color='tab:green', label="No. people on pup")
ax3.set_title("Number of people receiving pandemic payments")
ax3.set_xlabel("Date")
ax3.set_ylabel("Number of people receiving pandemic payments")
ax3.legend()
#calculate  pup mean
pup_mean=df_pup2['VALUE'].mean()
pup_max=df_pup2['VALUE'].max()
# set start and end points for line, convert date limits to date/number for graph
px1 = dt.datetime.strptime('2020-01-01','%Y-%m-%d')
px2 = dt.datetime.strptime('2021-05-01','%Y-%m-%d')
# draw a line on chart at the mean value slight above the dashed line
ax3.hlines(pup_mean, px1, px2, label='ax3 h', ls='--', color='g')
mean_line_text = "Mean no. of people receiving pup = " + str(int(pup_mean))
ax3.text(px1, pup_mean+10000, mean_line_text)
# add a text box at the max location
max_text = "Max = " + str(int(pup_max))
ax3.text(px1+(px2-px1)/10, pup_max, max_text)

# print header to inspect
print('df_pup head = \n', df_pup.head())   # view top lines of data
print('df_pup dtypes = \n', df_pup.dtypes)   # view data types

#count number of people on 'Persons in receipt of the Pandemic Unemployment Payment'
df_bar1 = df_pup.loc[df_pup['Statistic'] == 'Persons in receipt of the Pandemic Unemployment Payment', :]
df_bar1 = df_bar1.loc[df_pup['Age Group'] == 'All ages', :]
df_bar1 = df_bar1.loc[(df_pup['Sex'] == 'Male') | (df_pup['Sex'] == 'Female'), :]
df_bar1.to_csv(r'export_df_bar1.csv', index=False, header=True)


df_bar1 = (df_bar1.groupby(["Sex"]).mean().sort_values(["VALUE"], ascending=False).rename(columns={"VALUE": "mean of Value"}).reset_index())
fig, ax4 = plt.subplots(1, 1, figsize=(8, 4))
ax4.set_title("Comparison of average male vs female on PUP")
ax4.set_xlabel("Category Male / Female")
ax4.set_ylabel("Number of persons")

ax4.bar(df_bar1['Sex'], df_bar1['mean of Value'], color='tab:blue', label="PUP average of Sexes")

mean_females = df_pup.loc[(df_pup["Age Group"] == 'All ages') & (df_pup["Sex"] != 'Both Sexes') & (df_pup["Sex"] == 'Female'),'VALUE'].mean()
print('\n mean no. of female = ', mean_females)

mean_males = df_pup.loc[(df_pup["Age Group"] == 'All ages') & (df_pup["Sex"] != 'Both Sexes') & (df_pup["Sex"] == 'Male'),'VALUE'].mean()
print('\n mean no. of male = ', mean_males)


# add numerical data half way up bar
ax4.text(-0.1, mean_males/2, int(mean_males), style='italic',
        bbox={'facecolor': 'green', 'alpha': 0.1, 'pad': 8})

# add numerical data half way up bar
ax4.text(.9, mean_females/2, int(mean_females), style='italic',
        bbox={'facecolor': 'green', 'alpha': 0.1, 'pad': 8})

Ratio_M_F = mean_males /    mean_females
print("%.2f" % Ratio_M_F)
Ratio_M_F_text = "Ratio Male/Female = " + ("%.2f" % Ratio_M_F)

# add numerical data above the female bar
ax4.text(.73, mean_females + 30000, Ratio_M_F_text, style='italic',
        bbox={'facecolor': 'green', 'alpha': 0.1, 'pad': 8})



#df_bar2 = (df_pup.groupby(["Statistic"]).mean().sort_values(["VALUE"], ascending=False).rename(columns={"VALUE" : "Sum of Value"}).reset_index())
df_bar2 = (df_pup.groupby(["Statistic"]).mean().sort_values(["VALUE"], ascending=False).rename(columns={"VALUE" : "mean of Value"}).reset_index())

fig, ax5 = plt.subplots( figsize=(7, 8))
fig.subplots_adjust(bottom=0.5)
ax5.set_title("Plot 5 Comparison of supports payments")
ax5.set_xlabel("Government support payments")
ax5.set_ylabel("Number of people")
ax5.set_xticklabels(df_bar2.loc[:, 'Statistic'],  rotation='vertical', size=8)
print('\n List of statistics = \n', df_bar2.loc[:, 'Statistic'])
# Pad margins so that markers don't get clipped by the axes
ax5.margins(.1)
ax5.bar(df_bar2['Statistic'], df_bar2['mean of Value'], color='tab:blue', label="No.People")
ax5.legend()


#==============================================================================
#  Plot #5 chart pup by age group
#==============================================================================


#Count number of people on 'Persons in receipt of the Pandemic Unemployment Payment'
df_bar6 = df_pup.loc[df_pup['Statistic'] == 'Persons in receipt of the Pandemic Unemployment Payment', :]
df_bar6 = df_bar6.loc[df_pup['Age Group'] != 'All ages', :]
df_bar6 = df_bar6.loc[(df_pup['Sex'] == 'Both sexes'), :]

#df_bar6 = (df_bar6.groupby(["Age Group"]).mean().sort_values(["VALUE"], ascending=False).rename(columns={"VALUE": "mean of Value"}).reset_index())
df_bar6 = df_bar6.groupby('Age Group', as_index=False)['VALUE'].mean()
df_bar6.to_csv(r'export_df_bar6.csv', index=True, header=True)

fig, ax6 = plt.subplots(figsize=(12, 5))
rects1 = ax6.bar(df_bar6['Age Group'], df_bar6['VALUE'], color='tab:orange', label="PUP average of Age groups")

ax6.set_title("Comparison of age groups on PUP")
ax6.set_xlabel("Category Age group")
ax6.set_ylabel("Number of persons")
ax6.legend()

#==============================================================================
#  Plot #6 chart pup by age group and sex
#==============================================================================


#Count number of people on 'Persons in receipt of the Pandemic Unemployment Payment'
df_bar7 = df_pup.loc[df_pup['Statistic'] == 'Persons in receipt of the Pandemic Unemployment Payment', :]
df_bar7 = df_bar7.loc[df_pup['Age Group'] != 'All ages', :]
df_bar7 = df_bar7.groupby(['Age Group', 'Sex'], as_index=False)['VALUE'].mean().round(0)
df_barM = df_bar7.loc[(df_pup['Sex'] == 'Male'), :]
df_barF = df_bar7.loc[(df_pup['Sex'] == 'Female'), :]


df_bar7.to_csv(r'export_df_bar7.csv', index=True, header=True)

fig, ax7 = plt.subplots(figsize=(12, 5))
b1 = ax7.bar(df_barM['Age Group'], df_barM['VALUE'], color='tab:blue', label="Male")
b2 = ax7.bar(df_barF['Age Group'], df_barF['VALUE'], color='tab:red', label="Female", bottom=df_barM['VALUE'] )
ax7.set_title("Comparison of age groups and sex on PUP")
ax7.set_xlabel("Category Age group")
ax7.set_ylabel("Number of persons")

ax7.bar_label(b1, label_type='center')
ax7.bar_label(b2, label_type='center')

ax7.legend()


plt.show()

