# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 13:02:05 2020

@author: ANSURI
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

headers = ["names","day1","day2","day3","day4","day5","day6","day7","day8","day9","day10","day11",
           "day12","day13","day14","day15","day16","day17","day18","day19","day20"]

header_Name = ["Alisa Smit" , "Amit Mohite", "André Evertse","Anil Suri","Madhuri Deshmukh","Mike Schevers",
"Mohit Arora","Shraddha Tilay","Siddhesh Dalavi","Tim de Graaf"]

df = pd.read_excel("SampleAttendenceSheet.xlsx", names = headers)

df_1 = pd.read_excel("https://capgemini.sharepoint.com/:x:/r/sites/TEAMSERVICESG/_layouts/15/Doc.aspx?sourcedoc=%7B371073E1-60A6-480A-98AB-55057F2DEFCA%7D&file=Availability%20for%20Sprint%2023.xlsx&wdLOR=cF78C7DF5-6C8B-4945-AFFB-BD05ED7973A2&action=default&mobileredirect=true")

df.replace(np.nan, "A", inplace = True)
df.replace(" ", "", inplace = True)

df.diff

df.drop('names', inplace=True, axis=1)


def stripSpaces (frame):    
    for columns in frame.columns.values.tolist():
        frame[columns]= frame[columns].str.strip()        

stripSpaces(df)

dic = {}

def countIndividualAttendence(frame):
    for label, content in frame.items():
        dic[label] = []
        dic[label].append(content);
    return(dic)

dic = countIndividualAttendence(df)



def countVarValue(frame, var_name):
    count = 0
    for var in df.values:
        for c_var in var:
            if (c_var == var_name):
                count += 1
    print(f'Count of {var_name} is : {count}')
    return count
    
count_X = countVarValue(df , 'X')
count_H = countVarValue(df , 'H')
count_A = countVarValue(df , 'A')
count_O = countVarValue(df , 'O')



# Data to plot
labels = 'Vaccation', 'WFH', 'Available', 'Other Projects'
sizes = [count_X,count_H,count_A,count_O]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
explode = (0.1, 0, 0, 0)  # explode 1st slice

# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')
plt.show()





N = len(dic)
v_ser = []
for k ,v in dic.items():
    v_ser = v_ser.append(v)
menMeans = dic["Anil Suri"]
womenMeans = (25, 32, 34, 20, 25)
ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, menMeans, width)
p2 = plt.bar(ind, womenMeans, width,
             bottom=menMeans)

plt.ylabel('Scores')
plt.title('Scores by group and gender')
plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
plt.yticks(np.arange(0, 81, 10))
plt.legend((p1[0], p2[0]), ('Men', 'Women'))

plt.show()

df_1 = df.T

for key, value in df_1.iteritems(): 
    print(value.value_counts()) 

 
    
df["day1"].value_counts()

df_1 = df.T

df_1.columns = header_Name

df_1.drop(index = 0, inplace = True)
df_1.reset_index(drop=True, inplace=True)