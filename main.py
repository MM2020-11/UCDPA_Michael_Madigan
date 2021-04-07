# Michael Madigan UDC PA  DA project 5April 2021


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# read in csv file with world wide covid data
df1 = pd.read_csv("owid-covid-data.csv")

print(df1.head())   # view top lines of data
print(df1.shape)   # check shape number of row and columns
print(df1.dtypes)   # date is an object

# get all column names
for idx,column in enumerate(df1.columns):
    print(idx,column)
# from the column information we see that columns which columns to extract
# 0 iso_code
# 3 date
# 5 new_cases

# from the list we gather the required columns
required_cols = ['iso_code', 'date', 'new_cases']
df_iso_date_new_cases = df1.loc[:, required_cols]
#df_iso_date_new_cases = df1[required_cols]
print("Line 25 header of new dataframe with only three necessary columns")
print(df_iso_date_new_cases.head())

# set the date column to a date format
# set date format to YMD
df_iso_date_new_cases['date'] = pd.to_datetime(df_iso_date_new_cases['date'])

print("Line 33 header of new df1 with date column format set to date YMD ")
print(df_iso_date_new_cases.head())
print("Line 34 data types of new df1")
print(df_iso_date_new_cases.dtypes)   # date is an object


#Check data for NaN
count_NaN = df_iso_date_new_cases[required_cols].isna().sum()
print("line 40 Count of NaNs in df_iso_date_new_cases dataframe ")
print(count_NaN)

# from the Nan count we see 1576 NaN's in the new_cases column. we need to
# clean the NaN's and replace with zeros.
df_iso_date_new_cases_no_NaN = df_iso_date_new_cases.fillna(0)

#Repeated Check data for NaN to ensure fillna worked as planned
count_NaN = df_iso_date_new_cases_no_NaN[required_cols].isna().sum()
print("Line 49 Count of NaNs removed in df_iso_date_new_cases dataframe ")
print(count_NaN)

# Select only the rows that pertain to ireland, ISO code = IRL
df_IRL = df_iso_date_new_cases_no_NaN.loc[df_iso_date_new_cases_no_NaN["iso_code"] == 'IRL',:]
print("line 54 data frame header cleaned for Ireland, IRL" )
print(df_IRL.head())
print("check shape of data frame for Ireland to ensure reasonable data" )
print(df_IRL.shape)


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
for idx,column in enumerate(df_SLI.columns):
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

#df_SLI_State = df_SLI_Date_County_Value_No_NaN.loc[:, df_SLI_Date_County_Value_No_NaN["County"] == 'State']
#df_SLI_State = df_SLI_Date_County_Value_No_NaN.loc[['County'] == 'State', :]

#df_SLI_State = df_SLI_Date_County_Value_No_NaN.loc[df_SLI_Date_County_Value_No_NaN["County"] == 'State',:]
print("Line 112 data frame cleaned for State" )
print(df_SLI_Date_County_Value_No_NaN.head())
print("Line 114 check shape of data frame for Ireland to ensure reasonable data" )
print(df_SLI_Date_County_Value_No_NaN.shape)

# set the date column to a date format
#df_SLI_State.loc[:, ['Date']] = pd.to_datetime(df_SLI_State.loc[:, ['Date']], format='%Y/%m/%d')
df_SLI_Date_County_Value_No_NaN['Date'] = pd.to_datetime(df_SLI_Date_County_Value_No_NaN.loc[:, 'Date'])
#df_SLI_Date_County_Value_No_NaN['Date'] = pd.to_datetime(df_iso_date_new_cases['Date'])


#print(df_SLI_State.head())
#print("R124 header of new dataframe with date column format set to date")
#print(df_SLI_State.dtypes)   # date is an object


#==========================================
#                 MERGE SECTION
#==========================================

df_cases_County = pd.merge(df_SLI_Date_County_Value_No_NaN, df_IRL, left_on='Date', right_on='date', how='outer')


print("Line 136 merged df header / shape")
print(df_cases_County.head())
print(df_cases_County.shape)


required_cols = ['Date', 'County', 'VALUE', 'new_cases']
df_cases_County_2 = df_cases_County.loc[:, required_cols]

df_cases_County_2 = df_cases_County_2.fillna(0)

print(df_cases_County_2.head())
print(df_cases_County_2.shape)

df_cases_County_2.to_csv(r'export_dataframe_merge.csv', index=False, header=True)

#===================================================================================
#            start plotting
#===================================================================================



df_cases_County_2.plot(kind = 'line', x='Date', y=['new_cases','VALUE'],
                       secondary_y=False, style="g")



#par1 = plt.twinx()

#par1.set_ylabel("Temperature")
#par1.set_ylim(0, 4)
###p2, = par1.plot([0, 1, 2], [0, 3, 2], label="Temperature")
###par1.axis["right"].label.set_color(p2.get_color())


plt.ylabel('Some numbers')
plt.xlabel('Some dates')
plt.title('Good Stuff Data')


plt.annotate('Big spike in numbers', xy=(9000, 7500), xytext=(2500, 5000),
             arrowprops=dict(facecolor='blue', shrink=0.05),
             )

#plt.draw()
plt.show()



