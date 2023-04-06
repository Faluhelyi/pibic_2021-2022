import base_2 as base
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import os
import random
import seaborn as sns
import warnings
import pmdarima as pm
from pmdarima.preprocessing import FourierFeaturizer
from statsmodels.tsa.stattools import adfuller
from tbats import TBATS
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import joblib
import IPython
from pathlib import Path

##################################################
### Ajuste dos 70 modelos SARIMAX, DHR e TBATS ###
#####################  &  ########################
###             Submission files               ###
#####################  &  ########################
###                Acurácia                    ###
##################################################
c = 0
while c <= 1:
    iter = '_validation' if c ==0 else '_evaluation'
    for index, id in enumerate(base.sales_train['id']):
        id_ = f'{id}{iter}'
        item = base.sales_train.loc[index]['item_id']
        dept = base.sales_train.loc[index][['dept_id', 'store_id']][0]
        store = base.sales_train.loc[index][['dept_id', 'store_id']][1]
        state = base.sales_train.loc[index]['state_id']
        serie_valid = base.filter_dept_store(dept, store)[0:-28]
        serie_eva = base.filter_dept_store(dept, store)
        if state == 'CA':
            pct_change_price = base.get_price(dept, store).values
            exp_var = base.get_exp_var().drop(['snap_WI', 'snap_TX'], axis = 1)
            exp_var['pct_change_price'] = pct_change_price
        elif state == 'TX':
            pct_change_price = base.get_price(dept, store).values
            exp_var = base.get_exp_var().drop(['snap_WI', 'snap_CA'], axis = 1)
            exp_var['pct_change_price'] = pct_change_price
        else:
            pct_change_price = base.get_price(dept, store).values
            exp_var = base.get_exp_var().drop(['snap_TX', 'snap_CA'], axis = 1)
            exp_var['pct_change_price'] = pct_change_price

        ########################
        ## Ajuste dos modelos ##
        ########################
        if (os.path.isfile(f'{base.INPUT_DIR}/SARIMAX_models') == False) |\
            (os.path.isfile(f'{base.INPUT_DIR}/DHR_models') == False) |\
                (os.path.isfile(f'{base.INPUT_DIR}/TBATS_models') == False):

                if iter == '_validation':
                    result_sarimax_valid = pm.auto_arima(\
                        serie_valid, d = 1, start_p=0, start_q=0, max_p=3, max_q=3,\
                            seasonal = True, m = 7, D=1, start_P=0, start_Q=0, max_P=1, max_Q=1,\
                                information_criterion='aic', error_action='ignore', stepwise=True,\
                                    X = exp_var[0:1913]
                            )
                    joblib.dump(result_sarimax_valid, f'{base.INPUT_DIR}/SARIMAX_models/{dept}_{store}_validation')

                else:
                    result_sarimax_eva = pm.auto_arima(\
                        serie_eva, d = 1, start_p=0, start_q=0, max_p=3, max_q=3,\
                            seasonal = True, m = 7, D=1, start_P=0, start_Q=0, max_P=1, max_Q=1,\
                                information_criterion='aic', error_action='ignore', stepwise=True,\
                                    X = exp_var[0:1941]
                            )
                    joblib.dump(result_sarimax_eva, f'{base.INPUT_DIR}/SARIMAX_models/{dept}_{store}_evaluation')

                     
        else:
            if iter == '_validation':
                result_sarimax_valid = joblib.load(f'{base.INPUT_DIR}/SARIMAX_models/{dept}_{store}_validation')
            else:
                result_sarimax_eva = joblib.load(f'{base.INPUT_DIR}/SARIMAX_models/{dept}_{store}_evaluation')


        #################
        ### Forecasts ###
        #################
        if iter == '_validation':
            sarimax_forecast_valid = result_sarimax_valid.predict(28, X= exp_var[1913:1941])

        else:
            sarimax_forecast_eva = result_sarimax_eva.predict(28, X= exp_var[1941:])

        #################################################################################################
        ### Top-Down approach - top-down Gross-Sohl method F (Proportions of the historical averages) ###
        #################################################################################################

        .
    

    c = c + 1
    print(dept, store, id_)
    print(base.sample_submission[base.sample_submission['id'] == id_])






########################
### Submission files ###
########################