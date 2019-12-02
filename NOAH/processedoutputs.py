#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 17:42:36 2019

@author: noahkasmanoff

Processed Outputs

"""
#%%
import pandas as pd
import numpy as np

import os,sys

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')

#%%
fertilizer_df = pd.read_csv('../noahdata/Processed_Outputs/FERTILIZER_Processed.csv')
fungicide_df = pd.read_csv('../noahdata/Processed_Outputs/FUNGICIDE_Processed.csv')
herbicide_df = pd.read_csv('../noahdata/Processed_Outputs/HERBICIDE_Processed.csv')
insecticide_df = pd.read_csv('../noahdata/Processed_Outputs/INSECTICIDE_Processed.csv')
#%%


# Still a lot of duplicated cols, how do I remove those (except year, loc)


fertilizer_df.drop('STATE_ANSI',axis=1,inplace=True)

#%%


insecticide_df.drop(columns = ['STATE_ANSI', 'AREA_OPERATED_IN_ACRES',
       'AREA_OPERATED_IN_ACRES_/_OPERATION', 'OPERATIONS_IN_OPERATIONS',
       'AREA_HARVESTED_IN_ACRES', 'AREA_PLANTED_IN_ACRES', 'PRODUCTION_IN_BU',
       'PRODUCTION_IN_$', 'PRICE_RECEIVED_IN_$_/_BU',
       'CONDITION_IN_PCT_VERY_POOR', 'CONDITION_IN_PCT_GOOD',
       'CONDITION_IN_PCT_FAIR', 'CONDITION_IN_PCT_POOR',
       'CONDITION_IN_PCT_EXCELLENT', 'CONDITION_5_YEAR_AVG_IN_PCT_EXCELLENT',
       'CONDITION_5_YEAR_AVG_IN_PCT_GOOD', 'CONDITION_5_YEAR_AVG_IN_PCT_POOR',
       'CONDITION_5_YEAR_AVG_IN_PCT_VERY_POOR',
       'CONDITION_5_YEAR_AVG_IN_PCT_FAIR',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_POOR',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_GOOD',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_VERY_POOR',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_EXCELLENT',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_FAIR', 'YIELD_IN_BU_/_ACRE'],inplace=True)

herbicide_df.drop(columns = ['STATE_ANSI', 'AREA_OPERATED_IN_ACRES',
       'AREA_OPERATED_IN_ACRES_/_OPERATION', 'OPERATIONS_IN_OPERATIONS',
       'AREA_HARVESTED_IN_ACRES', 'AREA_PLANTED_IN_ACRES', 'PRODUCTION_IN_BU',
       'PRODUCTION_IN_$', 'PRICE_RECEIVED_IN_$_/_BU',
       'CONDITION_IN_PCT_VERY_POOR', 'CONDITION_IN_PCT_GOOD',
       'CONDITION_IN_PCT_FAIR', 'CONDITION_IN_PCT_POOR',
       'CONDITION_IN_PCT_EXCELLENT', 'CONDITION_5_YEAR_AVG_IN_PCT_EXCELLENT',
       'CONDITION_5_YEAR_AVG_IN_PCT_GOOD', 'CONDITION_5_YEAR_AVG_IN_PCT_POOR',
       'CONDITION_5_YEAR_AVG_IN_PCT_VERY_POOR',
       'CONDITION_5_YEAR_AVG_IN_PCT_FAIR',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_POOR',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_GOOD',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_VERY_POOR',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_EXCELLENT',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_FAIR', 'YIELD_IN_BU_/_ACRE'],inplace=True)


fungicide_df.drop(columns = ['STATE_ANSI', 'AREA_OPERATED_IN_ACRES',
       'AREA_OPERATED_IN_ACRES_/_OPERATION', 'OPERATIONS_IN_OPERATIONS',
       'AREA_HARVESTED_IN_ACRES', 'AREA_PLANTED_IN_ACRES', 'PRODUCTION_IN_BU',
       'PRODUCTION_IN_$', 'PRICE_RECEIVED_IN_$_/_BU',
       'CONDITION_IN_PCT_VERY_POOR', 'CONDITION_IN_PCT_GOOD',
       'CONDITION_IN_PCT_FAIR', 'CONDITION_IN_PCT_POOR',
       'CONDITION_IN_PCT_EXCELLENT', 'CONDITION_5_YEAR_AVG_IN_PCT_EXCELLENT',
       'CONDITION_5_YEAR_AVG_IN_PCT_GOOD', 'CONDITION_5_YEAR_AVG_IN_PCT_POOR',
       'CONDITION_5_YEAR_AVG_IN_PCT_VERY_POOR',
       'CONDITION_5_YEAR_AVG_IN_PCT_FAIR',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_POOR',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_GOOD',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_VERY_POOR',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_EXCELLENT',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_FAIR', 'YIELD_IN_BU_/_ACRE'],inplace=True)

#%%


climate_df = pd.read_csv('../data/climate_df_withtemp.csv')

climate_df = climate_df[climate_df.columns[2:]]

#let's just assume all these vars are useful. merge with soymerge!

merged_df = fertilizer_df.merge(climate_df,on = ['YEAR','LOCATION'],how = 'left').dropna()
merged_df = merged_df.merge(insecticide_df,on = ['YEAR','LOCATION'],how = 'left').dropna()
merged_df = merged_df.merge(fungicide_df,on = ['YEAR','LOCATION'],how = 'left').dropna()
merged_df = merged_df.merge(herbicide_df,on = ['YEAR','LOCATION'],how = 'left').dropna()

#%% Now model test!

from sklearn.model_selection import train_test_split
X = merged_df.drop(columns = ['YEAR','LOCATION','AREA_HARVESTED_IN_ACRES'
                              , 'PRODUCTION_IN_BU','PRODUCTION_IN_$','PRICE_RECEIVED_IN_$_/_BU'
                              ,'YIELD_IN_BU_/_ACRE',
                              'AREA_OPERATED_IN_ACRES',
       'AREA_OPERATED_IN_ACRES_/_OPERATION', 'OPERATIONS_IN_OPERATIONS',
       'CONDITION_IN_PCT_VERY_POOR', 'CONDITION_IN_PCT_GOOD',
       'CONDITION_IN_PCT_FAIR', 'CONDITION_IN_PCT_POOR',
       'CONDITION_IN_PCT_EXCELLENT', 'CONDITION_5_YEAR_AVG_IN_PCT_EXCELLENT',
       'CONDITION_5_YEAR_AVG_IN_PCT_GOOD', 'CONDITION_5_YEAR_AVG_IN_PCT_POOR',
       'CONDITION_5_YEAR_AVG_IN_PCT_VERY_POOR',
       'CONDITION_5_YEAR_AVG_IN_PCT_FAIR',
       'CONDITION_PREVI OUS_YEAR_IN_PCT_POOR',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_GOOD',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_VERY_POOR',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_EXCELLENT',
       'CONDITION_PREVIOUS_YEAR_IN_PCT_FAIR'
        
        ])

y = merged_df[['YIELD_IN_BU_/_ACRE']]
X_train,X_test,y_train,y_test = train_test_split(X,y)


#%%

from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators = 2000)
rf.fit(X_train,y_train)
rfscore = rf.score(X_test,y_test)

print("RF train score = ", rf.score(X_train,y_train))
print("RF test score = ", rfscore) #good af

#%%
y_pred = rf.predict(X_test)

plt.plot(y_test,y_pred,'o')
plt.ylabel("Predicted Yield (BU / ACRE)",fontsize=20)
plt.xlabel("True Yield (BU / ACRE)", fontsize = 20)
plt.xlim([15,60])
plt.ylim([15,60])


#%%
#plt.figure(figsize = (30,30))
sns.heatmap(merged_df.sample(n=10,axis=1).corr())