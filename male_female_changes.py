# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 22:42:13 2020

@author: jdfab
"""

import os 
import pandas as pd
data_folder = 'C:/Users/jdfab/Dropbox/baby_names/baby_names/Data'

df = pd.DataFrame(columns = ['Name','boys','girls','year'])
for file in os.listdir(data_folder):
    if file[-4:] == '.csv':
        year = int(file[-8:-4])
        boys = pd.read_csv(os.path.join(data_folder,file),encoding = 'cp1252',skiprows=6,usecols = [1,2])
        girls = pd.read_csv(os.path.join(data_folder,file),encoding = 'cp1252',skiprows =6, usecols = [5,6])
        boys = boys.rename(columns = {'Number of babies':'boys'})
        girls = girls.rename(columns = {'Name.1':'Name','Number of babies.1':'girls'})
        babies = boys.merge(girls,how = 'outer')
        babies['year']= year
        df = df.append(babies)
        

now = df[df.year >2015]
then = df[df.year <1980]
now = now.pivot_table(index = 'Name',values = ['boys','girls'],aggfunc = sum)
then = then.pivot_table(index = 'Name',values = ['boys','girls'],aggfunc = sum)
now['ratio'] = now.girls.div(now.boys+now.girls)
then['ratio'] = then.girls.div(then.boys+then.girls)
now = now[now.boys + now.girls > 5]
then = then[then.boys + then.girls > 5]

data = now.merge(then,left_index = True,right_index = True)
data = data.rename(columns = {'boys_x':'boys15-19','girls_x':'girls15-19','boys_y':'boys74-79','girls_y':'girls74-79'})
data = data.rename(columns = {'ratio_x':'ratio_2019','ratio_y':'ratio_1979'})
data['change'] = data['ratio_2019']-data['ratio_1979']

print(data.sort_values('change')[['boys15-19','girls15-19','boys74-79','girls74-79','change']].head(10).to_csv(float_format='%.2f'))
print(data.sort_values('change',ascending =False)[['boys15-19','girls15-19','boys74-79','girls74-79','change']].head(10).to_csv(float_format='%.2f'))
