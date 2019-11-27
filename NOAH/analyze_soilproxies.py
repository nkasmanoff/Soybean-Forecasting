#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 11:25:29 2019

@author: noahkasmanoff


Soil quality is an extremely important indicator of the amount of yield for any crop,
and in particular for this study, soybean. However, such a measure "good, standard, poor"
is not a feasible metric for this study, nor is it actionable. 

Alternatively, we can observe the relationship between yield and the factors which
are under a farmer's control; pesticides, insecticides, herbicides, and fungicides. 
 

By constructing useful features from USDA surveys to american farmers on what they put in the soil, 
we can determine the optimal combinations for soybean yield.

"""

import pandas as pd
import numpy as np
import os,sys


soybean_yield = pd.read_csv('dat/clean_yield.csv')
fertilizers = pd.read_csv('dat/fertilizers_cleaned.csv')
herbicides = pd.read_csv('dat/herbicides_cleaned.csv')

herbicides.dropna(axis=1,inplace=True)


herbicides.columns

herbicides = herbicides[['YEAR', 'LOCATION', 'CHEMICAL, HERBICIDE: (TOTAL)APPLICATIONS in LB', 'CHEMICAL, HERBICIDE: (TOTAL)TREATED in PCT OF AREA PLANTED, AVG']]
herbicides['CHEMICAL, HERBICIDE: (TOTAL)APPLICATIONS in LB'] = herbicides['CHEMICAL, HERBICIDE: (TOTAL)APPLICATIONS in LB'].apply(lambda z: np.log10(1 + z))

"""
Lots of ways to proceed. firstly I want to switch to log for applications in lbs, and see 

"""

fertilizers.columns

fertilizers['FERTILIZER: (NITROGEN)APPLICATIONS in LB'] = fertilizers['FERTILIZER: (NITROGEN)APPLICATIONS in LB'].apply(lambda z: np.log10(1 + z))

fertilizers['FERTILIZER: (PHOSPHATE)APPLICATIONS in LB'] = fertilizers['FERTILIZER: (PHOSPHATE)APPLICATIONS in LB'].apply(lambda z: np.log10(1 + z))
soybean_yield['AREA PLANTED in ACRES'] = soybean_yield['AREA PLANTED in ACRES'].apply(lambda z: np.log10(1 + z))

#now that everything is in a pretty close order of magnitude, try this. 

fertilizers.isna().sum()

soymerge = soybean_yield.merge(fertilizers,on=['YEAR','LOCATION'],how='inner')
soymerge = soymerge.merge(herbicides,on = ['YEAR','LOCATION'],how = 'left')
soymerge.dropna(axis=1,inplace=True)

"""
Make a simple model out of this.. 

"""

y = soymerge['YIELD in BU / ACRE']
cols_to_drop = ['YIELD in BU / ACRE', 'PRODUCTION in BU','AREA HARVESTED in ACRES','YEAR','LOCATION']
X = soymerge.drop(columns = cols_to_drop)

from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test = train_test_split(X,y)

from sklearn.linear_model import LinearRegression

linreg = LinearRegression()

linreg.fit(X_train,y_train)


linreg.score(X_test,y_test)


from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators = 100)
rf.fit(X_train,y_train)
rf.score(X_test,y_test)


linreg.coef_

X_train.columns