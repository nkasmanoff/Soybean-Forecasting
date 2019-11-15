"""


Function to combine the fertilizer information with yield for a given state. 


"""


import numpy as np 
import pandas as pd 

def format_fertilizer(fertilizer_df):
	"""
	Formats the dataframe from usda with the given fertilizer information over a given space 
	and time into a panel suitable format. 


	Parameters
	----------
d
	fertilizer_df : df
		Raw dataframe pulled straight from usda quickstats lite

	Returns
	-------

	cleaned_fertilizer : df
		Cleaned fertilizer data 

	"""

	fertilizers = []

	for ftype, g in fertilizer_df.groupby("DOMAINCAT"):
	    ftype = ftype.split('(')[1].split(')')[0]
	    for col in g.columns[8:]:
	        g[ftype + ' ' + col] = g[col]
	        del g[col]
	    g.drop(columns= ['STATE ANSI', 'ASD CODE', 'COUNTY ANSI',
	       'REFERENCE PERIOD', 'COMMODITY','DOMAINCAT'],inplace=True)
	    fertilizers.append(g)

	print("Hopefully only 3 fertilizer types? If not fix this f. ", len(fertilizers))   

	cleaned_fertilizer = pd.merge(fertilizers[0],fertilizers[1],on=['YEAR','LOCATION'])
	cleaned_fertilizer = cleaned_fertilizer.merge(fertilizers[2],on = ['YEAR','LOCATION'])


	return cleaned_fertilizer