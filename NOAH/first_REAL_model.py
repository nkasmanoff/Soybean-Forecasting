#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 13:03:11 2019

@author: noahkasmanoff



Offset result of climate. Determine how much more we cn get from climate info and solve for what that gives us. 



"""



#%%


import pandas as pd
import numpy as np

import os,sys

import matplotlib.pyplot as plt

import seaborn as sns

sns.set_style('white')
#load in data

#%% Step 2 ##### 

soybean_yield =  pd.read_csv('NOAH/dat/clean_yield.csv')
#same normalization, but only preserve cols that don't give up too much information!

soybean_yield['AREA PLANTED in ACRES'] = soybean_yield['AREA PLANTED in ACRES'].apply(lambda z: np.log10(1 + z))

soybean_yield = soybean_yield[['YEAR','LOCATION','YIELD in BU / ACRE']]

#%% 


climate_df = pd.read_csv('data/climate_df_withtemp.csv')

climate_df = climate_df[climate_df.columns[2:]]


#%%

plt.hist(soybean_yield['YIELD in BU / ACRE'])
plt.xlabel('Yield in BU / ACRE',fontsize=25)
plt.ylabel('Frequency',fontsize = 25)


#%% A normal distribution, good!

#now merge with tempeature


soymerge = soybean_yield.merge(climate_df,on = ['YEAR','LOCATION'],how = 'left').dropna() #loses last state


#%% Now with this, what sort of output can we expect?

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
y = soymerge['YIELD in BU / ACRE']


X = soymerge.drop(columns = ['YEAR','LOCATION','YIELD in BU / ACRE'] )



X_train,X_test,y_train,y_test = train_test_split(X,y)




rf = RandomForestRegressor(n_estimators = 15)
rf.fit(X_train,y_train)
rfscore = rf.score(X_test,y_test)

print("RF test score = ", rfscore) #good af


#%% Look at feature importance, let's see what's missing? 


