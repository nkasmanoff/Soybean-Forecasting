#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:53:15 2019

@author: noahkasmanoff




STEP 1: 
    
    Decide what soil metrics to use and keep, looking at each df individually
    
    
Step 2: 
    
    Load in yield data, merge with soil datasets (chemical usage etc)
    
step 3:
    
    Load in climate data, merge with two above
    
    
Step 4: 
    
    Model with random forest regressor, analyze results!
    
    
Conclusion:
    Sparsity is making these results look a lot better than they actually are, but we still can't afford to throw out examples. 
    
"""
import pandas as pd
import numpy as np

import os,sys

#%% Step 1 #######

#%% part 1, fertilizer

fertilizers = pd.read_csv('dat/fertilizers_cleaned.csv')

#normalize the two cols 

fertilizers['FERTILIZER: (NITROGEN)APPLICATIONS in LB'] = fertilizers['FERTILIZER: (NITROGEN)APPLICATIONS in LB'].apply(lambda z:
    np.log10(1 + z))

fertilizers['FERTILIZER: (PHOSPHATE)APPLICATIONS in LB'] = fertilizers['FERTILIZER: (PHOSPHATE)APPLICATIONS in LB'].apply(lambda z: 
    np.log10(1 + z))
    
fertilizers.isna().sum()
#current technique, fill na with -999

fertilizers.fillna(-999,inplace=True)

fertinfo = fertilizers.describe()

#and step 1 is continued by repeating this procedure for each farm var. For now just gonna go straight to step 2

#%% Step 2 ##### 

soybean_yield =  pd.read_csv('dat/clean_yield.csv')
#same normalization, but only preserve cols that don't give up too much information!

soybean_yield['AREA PLANTED in ACRES'] = soybean_yield['AREA PLANTED in ACRES'].apply(lambda z: np.log10(1 + z))

soybean_yield = soybean_yield[['YEAR','LOCATION','AREA PLANTED in ACRES','YIELD in BU / ACRE']]

#off the bat evidence of one variable to contribute to yield, plant more (duh)
# soybean_yield.corr()
#%% 

#now merge, based on soybean

soymerge = soybean_yield.merge(fertilizers,on = ['YEAR','LOCATION'],how = 'left')

#still nans, fill with same procedure (for now)

soymerge.fillna(-999,inplace=True)
#on to 3
#%% Step 3  Loading in cliamte info 


climate_df = pd.read_csv('../data/climate_df_withtemp.csv')

climate_df = climate_df[climate_df.columns[2:]]

#let's just assume all these vars are useful. merge with soymerge!


soymerge = soymerge.merge(climate_df,on = ['YEAR','LOCATION'],how = 'left') #again left, this preserves as much yield info as possible 
#%% again fill na the bad way? 

soymerge.fillna(-999,inplace = True)


#%% Step 4, let's see what a model can do!


X = soymerge.drop(columns = ['YEAR','YIELD in BU / ACRE'])
X = pd.get_dummies(X)
y = soymerge['YIELD in BU / ACRE']

#%% train test split crap 

from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test = train_test_split(X,y)


#%% Test 1: Linear regression


from sklearn.linear_model import LinearRegression

linreg = LinearRegression(normalize=True)

linreg.fit(X_train,y_train)


scr = linreg.score(X_test,y_test)
print("Linreg test score = ", scr) #good af

#%% Test 2 RF Regressor 

from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators = 150)
rf.fit(X_train,y_train)
rfscore = rf.score(X_test,y_test)

print("RF test score = ", rfscore) #good af


#%% Analysis: Let's see what feature prediction says about this task. 

#%%
col_names = []
for f in range(X.shape[1]):
   # print("%d. feature %d (%f)" % (f + , indices[f], importances[indices[f]]))
  #  print(X.columns[indices[f]])
    col_names.append(X.columns[indices[f]])
#%%

from sklearn.ensemble import ExtraTreesRegressor
import matplotlib.pyplot as plt
# Build a classification task using 3 informative features

# Build a forest and compute the feature importances
forest = ExtraTreesRegressor(n_estimators=1000,
                              random_state=0)
 
forest.fit(X_train, y_train)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]
col_names = []
for f in range(X.shape[1]):
   # print("%d. feature %d (%f)" % (f + , indices[f], importances[indices[f]]))
  #  print(X.columns[indices[f]])
    col_names.append(X.columns[indices[f]])

# Plot the feature importances of the forest
plt.figure(figsize = (15,5))
plt.title("Feature importances")
plt.bar(range(X.shape[1]), importances[indices],
       color="r", yerr=std[indices], align="center")
plt.xticks(range(X.shape[1]), col_names,rotation=90)
plt.xlim([-1, X.shape[1]])
plt.show()
