################################
### Script python para teste ###
################################

import base_2 as base
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import os
import random
import seaborn as sns
import warnings

  
#print(len(base.get_price_total()[0:-4]))

#print(len(base.no_filter().resample('W').sum()))

#print(base.sales_train_val.head())

#print(base.get_exp_var().columns)

#print(base.get_price('FOODS_3', 'WI_3'))

#print(base.filter_dept_store('FOODS_3', 'WI_3'))

#print(base.sample_submission.head())

#print(base.filter_dept_store('FOODS_3', 'WI_3'))
#print(base.filter_dept_store('FOODS_3', 'WI_3')[0:-28])


pct_change_price = base.get_price('FOODS_3', 'WI_3').values
exp_var = base.get_exp_var().drop(['snap_CA', 'snap_TX'], axis = 1)
exp_var['pct_change_price'] = pct_change_price
print(exp_var[0:1941])

print(base.filter_dept_store('FOODS_3', 'WI_3'))

#print(base.sample_submission)