# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 14:34:04 2020

@author: ANSURI
"""

import pandas as pd
import matplotlib as plt
from matplotlib import pyplot
import numpy as np

filename= "https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DA0101EN/auto.csv"

headers = ["symboling","normalized-losses","make","fuel-type","aspiration", "num-of-doors","body-style",
         "drive-wheels","engine-location","wheel-base", "length","width","height","curb-weight","engine-type",
         "num-of-cylinders", "engine-size","fuel-system","bore","stroke","compression-ratio","horsepower",
         "peak-rpm","city-mpg","highway-mpg","price"]

df = pd.read_csv(filename, names = headers)

df.head()

#replace ? into NaN

df.replace("?", np.nan, inplace = True)
df.head()

#Evaluate Missing Values
missing_value = df.isnull();
missing_value.head();

#Count missing value in each Column

for column_miss in missing_value.columns.values.tolist():
    print(column_miss)
    print(missing_value[column_miss].value_counts())
    print(" ")

#Replace by mean:
#
#"normalized-losses": 41 missing data, replace them with mean
#"stroke": 4 missing data, replace them with mean
#"bore": 4 missing data, replace them with mean
#"horsepower": 2 missing data, replace them with mean
#"peak-rpm": 2 missing data, replace them with mean

    
avg_norm_loss = df["normalized-losses"].astype("float").mean(axis=0);
print("Average or Mean value of normalized-losses Column : ", avg_norm_loss)

#Replace "NaN" by mean value in "normalized-losses" column

df["normalized-losses"].replace(np.nan,avg_norm_loss, inplace = True)

def replaceByMean (column_name, column_type, frame_axis):
    avg = df[column_name].astype(column_type).mean(axis=frame_axis);
    print("Average or Mean value of "+ column_name +" is :", avg);
    df[column_name].replace(np.nan,avg, inplace = True)

replaceByMean("stroke","float",0)
replaceByMean("bore","float",0)
replaceByMean("horsepower","float",0)
replaceByMean("peak-rpm","float",0)

#Replace by frequency:
#"num-of-doors": 2 missing data, replace them with "four".
#Reason: 84% sedans is four doors. Since four doors is most frequent, it is most likely to occur
#Drop the whole row:

df['num-of-doors'].value_counts()
df['num-of-doors'].value_counts().idxmax()

df['num-of-doors'].replace(np.nan,"four", inplace = True)

#
#"price": 4 missing data, simply delete the whole row
#Reason: price is what we want to predict. 
#Any data entry without price data cannot be used for prediction; 
#therefore any row now without price data is not useful to us

# simply drop whole row with NaN in "price" column
df.dropna(subset=["price"],axis=0, inplace=True)

# reset index, because we droped two rows
df.reset_index(drop=True, inplace=True)



#Correct data format
#In Pandas, we use
#.dtype() to check the data type
#.astype() to change the data type

df.dtypes

df[["bore", "stroke"]] = df[["bore", "stroke"]].astype("float")
df[["normalized-losses"]] = df[["normalized-losses"]].astype("int")
df[["price"]] = df[["price"]].astype("float")
df[["peak-rpm"]] = df[["peak-rpm"]].astype("float")


#What is Standardization?
#Standardization is the process of transforming data into a common format 
#which allows the researcher to make the meaningful comparison.
#Example
#Transform mpg to L/100km:
#The formula for unit conversion is L/100km = 235 / mpg

df["city-L/100km'"] = 235/df["city-mpg"]
 
df["highway-L/100km'"] = 235/df["highway-mpg"]


#Data Normalization
#Why normalization?
#Normalization is the process of transforming values of several variables into a similar range. 
#Typical normalizations include scaling the variable so the variable average is 0, 
#scaling the variable so the variance is 1, or scaling variable so the variable values range from 0 to 1
#Example
#To demonstrate normalization, let's say we want to scale the columns "length", "width" and "height"
#Target:would like to Normalize those variables so their value ranges from 0 to 1.
#Approach: replace original value by (original value)/(maximum value)


df["length"] = df["length"]/ df["length"].max()
df["width"] = df["width"]/ df["width"].max()
df["height"] = df["height"]/ df["height"].max()


#Binning
#Why binning?
#Binning is a process of transforming continuous numerical variables into 
#discrete categorical 'bins', for grouped analysis.
#Example:
#
#In our dataset, "horsepower" is a real valued variable ranging from 48 to 288, 
#it has 57 unique values. What if we only care about the price difference between cars with high horsepower, 
#medium horsepower, and little horsepower (3 types)? 
#Can we rearrange them into three ‘bins' to simplify analysis?
#
#We will use the Pandas method 'cut' to segment the 'horsepower' column into 3 bins

df["horsepower"] = df["horsepower"].astype(int)

plt.pyplot.hist(df["horsepower"])
# set x/y labels and plot title
plt.pyplot.xlabel("horsepower")
plt.pyplot.ylabel("count")
plt.pyplot.title("horsepower bins")

#We would like 3 bins of equal size bandwidth so we use numpy's 
#linspace(start_value, end_value, numbers_generated function.
#Since we want to include the minimum value of horsepower we want to set start_value=min(df["horsepower"]).
#Since we want to include the maximum value of horsepower we want to set end_value=max(df["horsepower"]).
#Since we are building 3 bins of equal length, there should be 4 dividers, so numbers_generated=4.


bins = np.linspace(min(df["horsepower"]), max(df["horsepower"]),4)
print(bins)

group_names = ['Low', 'Medium', 'High']

df["horsepower-binned"] = pd.cut(df["horsepower"],bins, labels=group_names , include_lowest = True )
df[['horsepower','horsepower-binned']].head(20)


df["horsepower-binned"].value_counts()

pyplot.bar(group_names, df["horsepower-binned"].value_counts())
plt.pyplot.hist(df["horsepower-binned"])
plt.pyplot.xlabel("horsepower-binned")
plt.pyplot.ylabel("count")
plt.pyplot.title("horsepower binned")


# draw historgram of attribute "horsepower" with bins = 3
plt.pyplot.hist(df["horsepower"], bins = 5 )

# set x/y labels and plot title
plt.pyplot.xlabel("horsepower")
plt.pyplot.ylabel("count")
plt.pyplot.title("horsepower bins")



#Indicator variable (or dummy variable)
#What is an indicator variable?
#An indicator variable (or dummy variable) is a numerical variable used to label categories. 
#They are called 'dummies' because the numbers themselves don't have inherent meaning.
#Why we use indicator variables?
#So we can use categorical variables for regression analysis in the later modules.
#Example
#We see the column "fuel-type" has two unique values, "gas" or "diesel". 
#Regression doesn't understand words, only numbers. To use this attribute in regression analysis,
# we convert "fuel-type" into indicator variables.
#We will use the panda's method 'get_dummies' to assign numerical values to different categories of fuel type.


dummy_var_1 = pd.get_dummies(df["fuel-type"])
dummy_var_1.rename(columns = {"gas" : "fuel-type-gas" , "diesel" : "fuel-type-diesel"}, inplace = True)
df = pd.concat([df, dummy_var_1], axis=1)
df.drop("fuel-type", axis=1,inplace = True)

dummy_var_2 = pd.get_dummies(df["aspiration"])
dummy_var_2.rename(columns={'std':'aspiration-std', 'turbo': 'aspiration-turbo'}, inplace=True)
df = pd.concat([df, dummy_var_2], axis =1)
df.drop("aspiration", axis = 1, inplace=True)

df.to_csv('clean_df.csv')