#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 17:06:37 2019

@author: noahkasmanoff
"""

import pandas as pd

climate_new = pd.read_csv('../dat/climate_df_new.csv')



extra_cols = ['Unnamed: 0.1','Unnamed: 0',
'Avg_Temp_Season_1',
'Avg_Temp_Season_2',
'Avg_Temp_Season_3',
'Avg_Temp_Season_4',
'Max_Temp_Season_1',
'Max_Temp_Season_2',
'Max_Temp_Season_3',
'Max_Temp_Season_4',
'Min_Temp_Season_1',
'Min_Temp_Season_2',
'Min_Temp_Season_3',
'Min_Temp_Season_4',
'Cooling_degree_days',
'Heating_degree_days',
'PDSI',
'PHDI','Palmer-Z-index']



climate_new.drop(columns = extra_cols,inplace=True)


#%% How's this do with yield??

#we'll find out soon! 


climate_new.to_csv('../dat/final_climate_raw.csv',index=False
                   )
