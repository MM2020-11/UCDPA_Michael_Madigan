# Michael Madigan UDC PA  DA project 11April 2021


# import useful libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as md

# read in csv file with world wide covid data
# data downloaded from https://ourworldindata.org/coronavirus-source-data
# import csv file into a Pandas DataFrame
# Download data from site
URL_Covid_dataset = r'https://covid.ourworldindata.org/data/owid-covid-data.csv'
df1_from_web = pd.read_csv(URL_Covid_dataset)
print('Inspection of web data head', df1_from_web.head())
print('Inspection of web data tail', df1_from_web.head())

#Select data source - if offline then use local version
df1 = df1_from_web   # use this data source when on-line
#df1 = pd.read_csv("owid-covid-data.csv") # directly read a downloaded versin if web version is not available

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

selected_cols = ['iso_code', 'date', 'new_cases']
df_web = pd.read_csv(URL_Covid_dataset, usecols=selected_cols)

# from the list gathered the required columns - separate columns ino a new dataframe
# this drops the unneeded columns
selected_cols = ['iso_code', 'date', 'new_cases']
df_iso_date_new_cases = df1.loc[:, selected_cols] # using the .loc function

print("Line 33 header of new dataframe with only three necessary columns")
print(df_iso_date_new_cases.head())

print("Line 36 data types of new df1")
print(df_iso_date_new_cases.dtypes)
# from this we see that the "date" column is an object, this should be changed to a date field

# set the date column to a date format using .to_date() function
# set date format to YMD.
#df_iso_date_new_cases['date'] = pd.to_datetime(df_iso_date_new_cases['date'], yearfirst=True, format="%d/%m/%Y")
df_iso_date_new_cases['date'] = pd.to_datetime(df_iso_date_new_cases['date'], yearfirst=True, format="%Y/%m/%d")

print("Line 43 tail of new df1 with date column format set to date YMD ")
print(df_iso_date_new_cases.tail())

#Check data for NaN
count_NaN = df_iso_date_new_cases[selected_cols].isna().sum()
print("line 48 Count of NaNs in df_iso_date_new_cases dataframe ")
print(count_NaN)

# from the Nan count we see 1576 NaN's in the new_cases column. we need to
# clean the NaN's and replace with zeros.
df_iso_date_new_cases_no_NaN = df_iso_date_new_cases.fillna(0)


#Repeated Check data for NaN to ensure fillna worked as planned
count_NaN = df_iso_date_new_cases_no_NaN[selected_cols].isna().sum()
print("Line 58 Count of NaNs removed in df_iso_date_new_cases dataframe ")
print(count_NaN)

# Select only the rows that pertain to ireland, ISO code = IRL
df_IRL = df_iso_date_new_cases_no_NaN.loc[df_iso_date_new_cases_no_NaN["iso_code"] == 'IRL', :]
print("line 63 data frame header cleaned for Ireland, IRL")
print(df_IRL.head())
print("check shape of data frame for Ireland to ensure reasonable data")
print(df_IRL.shape)
# save to a comma separated value file
df_IRL.to_csv(r'export_dataframe_df_IRL.csv', index=False, header=True)

#=========================================================================
print("=====================================================")
print("=======Start process again for another dataset ======")
print("=====================================================")
#=========================================================================

# read and clean a second file
# the file is collected by the Irish government and a mobile phone company
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

print("Line 102 header of new dataframe with only three necessary columns")
print(df_SLI_Date_County_Value.head())

#Check data for NaN
count_NaN = df_SLI_Date_County_Value[required_cols].isna().sum()
print("Line 97 Count of NaNs in df_iso_date_new_cases dataframe ")
print(count_NaN)

# from the Nan count we fill nan's
df_SLI_Date_County_Value_No_NaN = df_SLI_Date_County_Value.fillna(0)

#Repeated Check data for NaN to ensure fillna worked as planned
count_NaN = df_SLI_Date_County_Value_No_NaN[required_cols].isna().sum()
print("Line 115 Count of NaNs removed in df_iso_date_new_cases dataframe ")
print(count_NaN)



print("Line 120 data frame cleaned for State" )
print(df_SLI_Date_County_Value_No_NaN.head())
print("Line 122 check shape of data frame for Ireland to ensure reasonable data" )
print(df_SLI_Date_County_Value_No_NaN.shape)

# set the date column to a date format
#df_SLI_State.loc[:, ['Date']] = pd.to_datetime(df_SLI_State.loc[:, ['Date']], format='%Y/%m/%d')
df_SLI_Date_County_Value_No_NaN['Date'] = pd.to_datetime(df_SLI_Date_County_Value_No_NaN.loc[:, 'Date'])

# Select only the rows that pertain to all ireland i.e. State, County = State
df_SLI_state = df_SLI_Date_County_Value_No_NaN.loc[df_SLI_Date_County_Value_No_NaN["County"] == 'State', :]

df_SLI_state.sort_index()

df_SLI_state.to_csv(r'export_dataframe_df_SLI_state.csv', index=False, header=True)

#===================================================================================
#
#                        MERGE SECTION
#
#===================================================================================


# merge the new_cases and SLI dataframes
df_cases_County = pd.merge(df_IRL, df_SLI_state, left_on='date', right_on='Date', how='left')

print("Line 146 merged df header / shape")
print(df_cases_County.head())
print(df_cases_County.shape)


required_cols = ['date', 'Date', 'County', 'VALUE', 'new_cases']
df_cases_County_2 = df_cases_County.loc[:, required_cols]

df_cases_County_cleaned = df_cases_County_2 = df_cases_County_2.fillna(0)

#date_cols = ['date','Date']
date_cols = ['date']

#df_cases_County_cleaned = (df_cases_County_2[(df_cases_County_2[date_cols] != 0).all(axis=1)]).sort_values('date')
# remove any 'date' filed that are zero
df_cases_County_cleaned = (df_cases_County_2[(df_cases_County_2[date_cols] != 0).all(axis=1)])
# add a new column just date for later plotting without the time values
df_cases_County_cleaned['just_date'] = df_cases_County_cleaned['date'].dt.date

print(df_cases_County_cleaned.head())
print(df_cases_County_cleaned.tail())





df_cases_County_cleaned.to_csv(r'df_cases_County_cleaned.csv', index=False, header=True)

df_cases_County_2.to_csv(r'export_dataframe_merge.csv', index=False, header=True)


#===================================================================================
#
#                       Start plotting
#
#===================================================================================

# collect columns to be plotted to list for the matplotlib functions
new_cases_list = df_cases_County_cleaned['new_cases'].tolist()
Value_list = df_cases_County_cleaned['VALUE'].tolist()
date_list = df_cases_County_cleaned['just_date'].tolist()


date_list2 = []

#for ts in date_list:
#    days1 = (ts - pd.Timestamp(0)).days
#    date_list2.append(days1)
#    #print(date_list2)


#print(date_list)
#plt.style.use('fivethirtyeight')

#df_cases_County_cleaned.plot(kind='bar', x='date', y=['new_cases'])
#df_cases_County_cleaned.plot(kind='bar', x='date', y=['VALUE'])

# export plot to an image file
# plt.savefig("Figure-SLI data")

#xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
#plt.xaxis.set_major_formatter(xfmt)

xtick_list = []
for tick in range(0, 403):
    if tick%30 == 0:
        xtick_list.append(tick)
#print(f'tick_list= {xtick_list}')

date_range = pd.date_range('2020-01-01', '2021-06-01', freq='MS')

#xtick_list = pd.to_datetime(date_range, format='%Y-%m-%d')

########xtick_list = date_range
test = date_range.map(lambda t: t.strftime('%Y-%m-%d'))
print('data_range = ', test)


fig, ax1 = plt.subplots(1, 1, figsize=(10, 5))

#ax1.plot(date_list, new_cases_list, label="ax1 new cases list label", color = 'blue', lw=1)
#ax1.set_xticklabels(df_cases_County_clea
# ned.index.format(), rotation='vertical', size=6)
#ax1.locator_params(axis='x', nbins=20)
#ax1.set_bins
ax1.set_title("ax1 Plot")
ax1.set_xlabel("ax1 x label xxxxx")
ax1.set_ylabel("ax1 y label yyyyy")
#ax1.marker ='x'

ax1.plot(date_list, new_cases_list, color='tab:blue', label="new cases")
ax1.plot(date_list, Value_list, color='tab:orange', label="Staying local")

secax1 = ax1.secondary_yaxis('right')
secax1.set_ylabel('secondary y label')
secax1.set_ylim(0, 100)

#ax1.secondary_yaxis.set_ylim(1,100)

ax1.annotate('S',  xytext=(10, 10),xy=(300, 500),
             arrowprops=dict(facecolor='blue', shrink=0.05),
             )
ax1.legend(loc='upper left')  #improve performance by instructing legend location

#ax2 = plt.subplots(2,1)
ax2 = df_cases_County_cleaned.plot(kind='bar', x='date', y='VALUE')
ax2.set_xticklabels(df_cases_County_cleaned.index.format(), rotation='vertical', size=6)
ax2.locator_params(axis='x', nbins=20)
ax2.set_title("ax2 Plot")
ax2.set_xlabel("ax2 x label xxxxx")
ax2.set_ylabel("ax2 y label yyyyy")


plt.show()