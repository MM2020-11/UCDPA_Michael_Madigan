# Michael Madigan UDC PA  DA project 16April 2021


# import useful libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt


# read in csv file with world wide covid data
# data downloaded from https://ourworldindata.org/coronavirus-source-data
# import csv file into a Pandas DataFrame
# Download data from site
#URL_Covid_dataset = r'https://covid.ourworldindata.org/data/owid-covid-data.csv'
#df1_from_web = pd.read_csv(URL_Covid_dataset)
#print('Inspection of web data head', df1_from_web.head())
#print('Inspection of web data tail', df1_from_web.head())

#Select data source - if offline then use local version
#df1 = df1_from_web   # use this data source when on-line
df1 = pd.read_csv("owid-covid-data.csv") # directly read a downloaded version if web version is not available

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
#df_web = pd.read_csv(URL_Covid_dataset, usecols=selected_cols)

# from the list gathered the required columns - separate columns ino a new dataframe
# this drops the unneeded columns
selected_cols = ['iso_code', 'date', 'new_cases']
df_iso_date_new_cases = df1.loc[:, selected_cols] # using the .loc function

print("Line 44 header of new dataframe with only three necessary columns")
print(df_iso_date_new_cases.head())

print("Line 47 data types of new df1")
print(df_iso_date_new_cases.dtypes)
# from this we see that the "date" column is an object, this should be changed to a date field

# set the date column to a date format using .to_date() function
# set date format to YMD.
df_iso_date_new_cases['date'] = pd.to_datetime(df_iso_date_new_cases['date'], yearfirst=True, format="%d/%m/%Y")
#df_iso_date_new_cases['date'] = pd.to_datetime(df_iso_date_new_cases['date'], yearfirst=True, format="%Y/%m/%d")

#df_SLI_Date_County_Value['Date'] = df_SLI_Date_County_Value['Date'].str.replace('2020 December20', '2020 December 20')
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
print("Line 71 Count of NaNs removed in df_iso_date_new_cases dataframe ")
print(count_NaN)

# Select only the rows that pertain to ireland, ISO code = IRL
df_IRL = df_iso_date_new_cases_no_NaN.loc[df_iso_date_new_cases_no_NaN["iso_code"] == 'IRL', :]
print("line 63 data frame header cleaned for Ireland, IRL")
print(df_IRL.head())
print("check shape of data frame for Ireland to ensure reasonable data")
print(df_IRL.shape)
# save to a comma separated value file for inspection
df_IRL.to_csv(r'export_dataframe_df_IRL.csv', index=False, header=True)

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

#required_cols = ['Date', 'County', 'VALUE']
#URL_SLI_dataset = 'https://ws.cso.ie/public/api.jsonrpc?data=%7B%22jsonrpc%22:%222.0%22,%22method%22:%22PxStat.Data.Cube_API.ReadDataset%22,%22params%22:%7B%22class%22:%22query%22,%22id%22:%5B%5D,%22dimension%22:%7B%7D,%22extension%22:%7B%22pivot%22:null,%22codes%22:false,%22language%22:%7B%22code%22:%22en%22%7D,%22format%22:%7B%22type%22:%22JSON-stat%22,%22version%22:%222.0%22%7D,%22matrix%22:%22SLI01%22%7D,%22version%22:%222.0%22%7D%7D'
#df_SLI = pd.read_json(URL_SLI_dataset)
#df_SLI = pd.json_normalize(df_SLI)
#df_SLI.to_csv(r'export_df_SLI_json.csv', index=False, header=True)


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

print("Line 102 header of new dataframe with only three necessary columns")
print(df_SLI_Date_County_Value.head())

#Check data for NaN
count_NaN = df_SLI_Date_County_Value[required_cols].isna().sum()
print("Line 121 Count of NaNs in df_iso_date_new_cases dataframe ")
print("\n count_NaN in SLI df =\n", count_NaN, '\n')

#initially just removed NaN with zero however a few missing plot points dropped to zero
# better to interpolate as only a few few small quantity of NaN's
df_SLI_Date_County_Value = df_SLI_Date_County_Value.interpolate(axis=0)

# from the Nan count we fill nan's - not required use interpolation
df_SLI_Date_County_Value_No_NaN = df_SLI_Date_County_Value.fillna(0)

#Repeated Check data for NaN to ensure fillna worked as planned
count_NaN = df_SLI_Date_County_Value_No_NaN[required_cols].isna().sum()
print("Line 129 Count of NaNs removed in df_iso_date_new_cases dataframe ")
print('df_SLI_Date_County_Value_No_NaN = count_NaN = ', count_NaN)



print("Line 134 data frame cleaned for State" )
print(df_SLI_Date_County_Value_No_NaN.head())
print("Line 136 check shape of data frame for Ireland to ensure reasonable data" )
print(df_SLI_Date_County_Value_No_NaN.shape)

# set the date column to a date format
#df_SLI_State.loc[:, ['Date']] = pd.to_datetime(df_SLI_State.loc[:, ['Date']], format='%Y/%m/%d')
# note on debugging noticed a date field format error
# normal format is yyyy space Month space day, however data has
df_SLI_Date_County_Value_No_NaN['New_Date'] = pd.to_datetime(df_SLI_Date_County_Value_No_NaN['Date'], format="%Y %B %d")
#df_SLI_Date_County_Value_No_NaN['New_Date2'] = pd.to_datetime(df_SLI_Date_County_Value_No_NaN['Date'], format="%Y %B %d")


# Select only the rows that pertain to all ireland i.e. State, County = State
df_SLI_state = df_SLI_Date_County_Value_No_NaN.loc[df_SLI_Date_County_Value_No_NaN["County"] == 'State', :]


#df_SLI_state.sort_index()

df_SLI_state.to_csv(r'export_dataframe_df_SLI_state.csv', index=False, header=True)

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

#df_cases_County_cleaned = (df_cases_County_2[(df_cases_County_2[date_cols] != 0).all(axis=1)]).sort_values('date')
# remove any 'date' filed that are zero
df_cases_County_cleaned = (df_cases_County_2[(df_cases_County_2[date_cols] != 0).all(axis=1)])

# add a new column just date for later plotting without the time values - just_date
df_cases_County_cleaned['just_date'] = df_cases_County_cleaned['date'].dt.date

print('\ndf_cases_County_cleaned head = \n', df_cases_County_cleaned.head())
print('\ndf_cases_County_cleaned tail = \n', df_cases_County_cleaned.tail())

# save files for debugging
df_cases_County_cleaned.to_csv(r'export_df_cases_County_cleaned.csv', index=False, header=True)
df_cases_County_2.to_csv(r'export_dataframe_merge.csv', index=False, header=True)

correlation = df_cases_County_2['VALUE'].corr( df_cases_County_2['new_cases'], method='pearson')
print('\n coor1 = ', correlation)

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


correlation = df_pup2['VALUE'].corr( df_pup2['new_cases'],method='pearson')
print('\n coor2 = ', correlation )

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

print('pup_date_list', pup_date_list)
print('pup_VALUE_list', pup_VALUE_list)

# export plot to an image file
plt.savefig("Figure-SLI data")

fig, ax1 = plt.subplots(1,1, figsize=(10, 5))

ax1.set_title("Plot of Irish covid cases compared to staying alone metris (ax1)")
ax1.set_xlabel("ax1 x label xxxxx")
ax1.set_ylabel("ax1 y label yyyyy")

ax1.annotate('A',  xytext=(1, 50),xy=(20, 75), arrowprops=dict(facecolor='blue', shrink=0.05))

ax1.plot(date_list, new_cases_list, color='tab:blue', label="new cases")
#ax1.plot(date_list, Value_list, color='tab:red', label="Staying local")
#ax1.plot(pup_date_list, pup_VALUE_list, color='tab:red', label="pup")

ax1.set_ylabel('Number of new covid cases')

ax1.legend(loc='upper left')  # Improve performance by instructing legend location
# add an arrow annotation to plot
ax1.annotate('Large spike', xy=(.76, .95),  xycoords='axes fraction',
            xytext=(0.55, 0.8), textcoords='axes fraction',
            arrowprops=dict(facecolor='blue', shrink=0.05),
            horizontalalignment='right', verticalalignment='top',
            )


ax1a = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax1a.plot(date_list, Value_list, color='tab:orange', label="Staying local")
#ax1a = ax1.secondary_yaxis('right')
ax1a.set_ylabel('secondary y label')
ax1a.set_ylim(50, 80)

#ax1b = ax1.twinx()  # instantiate a second axes that shares the same x-axis
#ax1b.plot(pup_date_list, pup_VALUE_list, color='tab:red', label="pup")
#ax1b.set_ylabel('ax1b secondary y label')

#============================================================================================
# Second plot
#============================================================================================

ax2 = plt.subplots(1,1)
ax2 = df_cases_County_cleaned.plot(kind='bar', x='date', y='VALUE')
ax2.set_xticklabels(df_cases_County_cleaned.index.format(), rotation='vertical', size=6)
ax2.locator_params(axis='x', nbins=20)
ax2.set_title("ax2 Plot")
ax2.set_xlabel("ax2 x label xxxxx")
ax2.set_ylabel("ax2 y label yyyyy")

ax2.annotate('A',  xytext=(1, 50),xy=(20, 75),
             arrowprops=dict(facecolor='blue', shrink=0.05),
             )



fig, ax3 = plt.subplots(1, 1, figsize=(10, 5))
ax3.plot(pup_date_list, pup_VALUE_list, color='tab:green', label="AX3 new cases")




# print header to inspect
print('df_pup head = \n', df_pup.head())   # view top lines of data
print('df_pup dtypes = \n', df_pup.dtypes)   # view top lines of data

df_bar1 = df_pup[df_pup['Sex'].isin(['Female', 'Male']) ]

#count_females = df_bar1['Sex'].count(isin(['female']))
#print("female", count_females)
#count_males = df_bar1['Sex'].isin(['male']).count()
#print('male', count_males)

df_bar1 = (df_bar1.groupby(["Sex"]).sum().sort_values(["VALUE"], ascending=False).rename(columns={"VALUE" : "Sum of Value"}).reset_index())
fig, ax4 = plt.subplots(1, 1, figsize=(8, 4))
ax4.set_title("Comparison of male / female persons ax4 Plot")
ax4.set_xlabel("Category Male / Female")
ax4.set_ylabel("Number of persons ax4 y label yyyyy")
ax4.bar(df_bar1['Sex'], df_bar1['Sum of Value'], color='tab:blue', label="PUP sum of Sexes")

mean_females = df_pup.loc[df_pup['Sex'] == 'Female', 'VALUE'].mean()
print('\n mean no. of female = ', mean_females)

mean_males = df_pup.loc[df_pup['Sex'] == 'Male', 'VALUE'].mean()
print('\n mean no. of male = ', mean_males)

ax4.text(-0.05, 3.0E7, int(mean_males), style='italic',
        bbox={'facecolor': 'green', 'alpha': 0.1, 'pad': 8})

ax4.text(.95, 3.0E7, int(mean_females), style='italic',
        bbox={'facecolor': 'green', 'alpha': 0.1, 'pad': 8})

Ratio_M_F = mean_males /    mean_females
print("%.2f" % Ratio_M_F)
Ratio_M_F_text = "Ratio Male/Female = " + ("%.2f" % Ratio_M_F)

ax4.text(.73, 6.0E7, Ratio_M_F_text, style='italic',
        bbox={'facecolor': 'green', 'alpha': 0.1, 'pad': 8})




df_bar2 = (df_pup.groupby(["Statistic"]).mean().sort_values(["VALUE"], ascending=False).rename(columns={"VALUE" : "Sum of Value"}).reset_index())

fig, ax5 = plt.subplots() # 1, figsize=(4, 4))
fig.subplots_adjust(bottom=0.5)
ax5.set_title("(Plot ax5) Comparison of supports payments")
ax5.set_xlabel("Government support payments")
ax5.set_ylabel("Number of people")
ax5.set_xticklabels(df_bar2.loc[:, 'Statistic'],  rotation='vertical', size=8)
print('\n List of statistics = \n', df_bar2.loc[:, 'Statistic'])
# Pad margins so that markers don't get clipped by the axes
ax5.margins(.1)
ax5.bar(df_bar2['Statistic'], df_bar2['Sum of Value'], color='tab:blue', label="No.People")
ax5.legend()





plt.show()