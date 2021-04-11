# Michael Madigan UDC PA  DA project 5April 2021
# Michael Madigan UDC PA  DA project 5April 2021

# import useful libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# read in csv file with world wide covid data
# data downloaded from https://ourworldindata.org/coronavirus-source-data
# import csv file into a Pandas DataFrame
df1 = pd.read_csv("owid-covid-data.csv")

print(df1.head())   # view top lines of data
print(df1.shape)    # check shape number of row and columns
print(df1.dtypes)   # date is an object

# inspect data to determine which columns contain valuable information for this project
# as the header file is very wide I list the column headings
# Display all column names with a "for loop"
for idx, column in enumerate(df1.columns):
    print(idx, column)
# From the column inspection I determine which columns are relevant to this project
# Relevant columns are : 0 iso_code,  # 3 date,  # 5 new_cases

# from the list gathered the required columns - separate columns ino a new dataframe
# this drops the unneeded columns
selected_cols = ['iso_code', 'date', 'new_cases']
df_iso_date_new_cases = df1.loc[:, selected_cols] # using the .loc function

print("Line 30 header of new dataframe with only three necessary columns")
print(df_iso_date_new_cases.head())

print("Line 33 data types of new df1")
print(df_iso_date_new_cases.dtypes)
# from this we see that the "date" column is an object, this should be changed to a date field

# set the date column to a date format using .to_date() function
# set date format to YMD.
df_iso_date_new_cases['date'] = pd.to_datetime(df_iso_date_new_cases['date'])
print("Line 40 header of new df1 with date column format set to date YMD ")
print(df_iso_date_new_cases.head())

#Check data for NaN
count_NaN = df_iso_date_new_cases[selected_cols].isna().sum()
print("line 43 Count of NaNs in df_iso_date_new_cases dataframe ")
print(count_NaN)

# from the Nan count we see 1576 NaN's in the new_cases column. we need to
# clean the NaN's and replace with zeros.
df_iso_date_new_cases_no_NaN = df_iso_date_new_cases.fillna(0)


#Repeated Check data for NaN to ensure fillna worked as planned
count_NaN = df_iso_date_new_cases_no_NaN[selected_cols].isna().sum()
print("Line 52 Count of NaNs removed in df_iso_date_new_cases dataframe ")
print(count_NaN)

# Select only the rows that pertain to ireland, ISO code = IRL
df_IRL = df_iso_date_new_cases_no_NaN.loc[df_iso_date_new_cases_no_NaN["iso_code"] == 'IRL', :]
print("line 57 data frame header cleaned for Ireland, IRL")
print(df_IRL.head())
print("check shape of data frame for Ireland to ensure reasonable data")
print(df_IRL.shape)
df_IRL.to_csv(r'export_dataframe_df_IRL.csv', index=False, header=True)

#=========================================================================
print("=====================================================")
print("=======Start process again for another dataset ======")
print("=====================================================")
#=========================================================================

# read and clean a second file
# the file is collected by the Irish government and a phone company
# use phone GPS data to determine people movement
# file name is Staying Local Indicator SLI01.20210330T200311.csv

# read in csv file with world wide covid data
df_SLI = pd.read_csv("Staying Local Indicator SLI01.20210403T220407-2.csv")

print(df_SLI.head())   # view top lines of data
print(df_SLI.shape)   # check shape number of row and columns
print(df_SLI.dtypes)   # check data types


# get all column names
for idx, column in enumerate(df_SLI.columns):
    print(idx,column)
# from the column information we see that columns which columns to extract
#0 Statistic
#1 Date
#2 County
#3 UNIT
#4 VALUE

required_cols = ['Date', 'County', 'VALUE']
df_SLI_Date_County_Value = df_SLI.loc[:, required_cols]

print("Line 92 header of new dataframe with only three necessary columns")
print(df_SLI_Date_County_Value.head())

#Check data for NaN
count_NaN = df_SLI_Date_County_Value[required_cols].isna().sum()
print("Line 97 Count of NaNs in df_iso_date_new_cases dataframe ")
print(count_NaN)

# from the Nan count we fill nan's
df_SLI_Date_County_Value_No_NaN = df_SLI_Date_County_Value.fillna(0)

#Repeated Check data for NaN to ensure fillna worked as planned
count_NaN = df_SLI_Date_County_Value_No_NaN[required_cols].isna().sum()
print("Line 105 Count of NaNs removed in df_iso_date_new_cases dataframe ")
print(count_NaN)



print("Line 112 data frame cleaned for State" )
print(df_SLI_Date_County_Value_No_NaN.head())
print("Line 114 check shape of data frame for Ireland to ensure reasonable data" )
print(df_SLI_Date_County_Value_No_NaN.shape)

# set the date column to a date format
#df_SLI_State.loc[:, ['Date']] = pd.to_datetime(df_SLI_State.loc[:, ['Date']], format='%Y/%m/%d')
df_SLI_Date_County_Value_No_NaN['Date'] = pd.to_datetime(df_SLI_Date_County_Value_No_NaN.loc[:, 'Date'])

# Select only the rows that pertain to all ireland i.e. State, County = State
df_SLI_state = df_SLI_Date_County_Value_No_NaN.loc[df_SLI_Date_County_Value_No_NaN["County"] == 'State', :]
df_SLI_state.to_csv(r'export_dataframe_df_SLI_state.csv', index=False, header=True)

#===================================================================================
#
#                        MERGE SECTION
#
#===================================================================================


# merge the cases and SLI dataframes
#df_cases_County = pd.merge(df_IRL, df_SLI_Date_County_Value_No_NaN, left_on='date', right_on='Date', how='outer')
#df_cases_County = pd.merge(df_IRL, df_SLI_state, left_on='date', right_on='Date', how='outer')
df_cases_County = pd.merge(df_IRL, df_SLI_state, left_on='date', right_on='Date', how='left')


print("Line 136 merged df header / shape")
print(df_cases_County.head())
print(df_cases_County.shape)


required_cols = ['date', 'Date', 'County', 'VALUE', 'new_cases']
df_cases_County_2 = df_cases_County.loc[:, required_cols]

df_cases_County_cleaned = df_cases_County_2 = df_cases_County_2.fillna(0)

#date_cols = ['date','Date']
date_cols = ['date']

#df_cases_County_cleaned = (df_cases_County_2[(df_cases_County_2[date_cols] != 0).all(axis=1)]).sort_values('date')

df_cases_County_cleaned = (df_cases_County_2[(df_cases_County_2[date_cols] != 0).all(axis=1)])

#df_cases_County_cleaned = df_cases_County_2.sort_values(by=['VALUE'])

print(df_cases_County_cleaned.head())
df_cases_County_cleaned.to_csv(r'df_cases_County_cleaned.csv', index=False, header=True)

df_cases_County_2.to_csv(r'export_dataframe_merge.csv', index=False, header=True)

#===================================================================================
#
#                       Start plotting
#
#===================================================================================

# collect columns to be plotted to list for the matplotlib functions
new_cases_list=df_cases_County_cleaned['new_cases'].tolist()
Value_list=df_cases_County_cleaned['VALUE'].tolist()
date_list=df_cases_County_cleaned['date'].tolist()

#plt.style.use('fivethirtyeight')


df_cases_County_cleaned.plot(kind='bar', x='date', y=['new_cases'])

df_cases_County_cleaned.plot(kind='bar', x='date', y=['VALUE'],
                       secondary_y=False)

plt.savefig("Figure 1")

plt.ylabel('Some numbers')
plt.xlabel('Some dates')
plt.title('Good Stuff Data')

plt.annotate('Big spike in numbers', xy=(9000, 7500), xytext=(2500, 5000),
             arrowprops=dict(facecolor='blue', shrink=0.05),
             )



# setup data for plots
t = date_list
data1 = new_cases_list
data2 = Value_list

fig, ax1 = plt.subplots()

#plt.legend()

color = 'tab:red'
ax1.set_xlabel('time (s)')
ax1.set_ylabel('new cases reported', color=color)
ax1.plot(t, data1, color=color)
ax1.tick_params(axis='y', labelcolor=color)


ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('SLI', color=color)  # we already handled the x-label with ax1
#ax2.plot(t, data2, color=color)


ax2.tick_params(axis='y', labelcolor=color)

#plt.xlim([18400,  19000])
ax1.set_title('New cases reported in Ireland')
fig.tight_layout()  # otherwise the right y-label is slightly clipped


plt.show()
