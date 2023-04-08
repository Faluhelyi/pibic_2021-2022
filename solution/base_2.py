############
### Note ###
############
# sales_train_eva contempla o sales_train_val e ainda adciona observacoes das vendas dos dias d_1914 - d_1941
# id = ..._validation => até d_1913
# id = ..._evaluation => até d_1941

############
### Goal ###
############
# validation part of submission sample => cross validation w/ d_1 to d_1913 => calculate sMAPE e MASE w/ d_1914 to d_1941
# evaluation part of submission sample => cross validation w/ d_1 to d_1941 => calculate M5 final score in kaggle by concatenating these parts

#####################################################################################################
### Script python para impotar as dados e definir funcoes basicas que usarei ao longo do trabalho ###
#####################################################################################################

############################################
########## IMPORTACAO DOS DADOS ############
############################################
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import os
import random
import seaborn as sns
import warnings

if os.path.exists('C:/Users/u00378/Desktop/PIBIC_2021-2022'):
    INPUT_DIR = 'C:/Users/u00378/Desktop/PIBIC_2021-2022'
else:
    INPUT_DIR = 'C:/Users/Igor/Desktop/PIBIC/PIBIC_2021-2022' # Update to your INPUT_DIR

calendar = pd.read_csv(f'{INPUT_DIR}/data_from_kaggle/calendar.csv')
selling_prices = pd.read_csv(f'{INPUT_DIR}/data_from_kaggle/sell_prices.csv')
sample_submission = pd.read_csv(f'{INPUT_DIR}/data_from_kaggle/sample_submission.csv')
sales_train_val = pd.read_csv(f'{INPUT_DIR}/data_from_kaggle/sales_train_validation.csv') # sales_train d_1 ate
                                                                                                                            # d_1913
sales_train_eva = pd.read_csv(f'{INPUT_DIR}/data_from_kaggle/sales_train_evaluation.csv') # sales_train d_1 ate
                                                                                                                            # d_1941
cols = []

for i in range(1, 1942, 1):
    col = f"d_{i}"
    cols.append(col)

sales_train = pd.concat([sales_train_val, sales_train_eva[cols[-28:]]], axis = 1)
sales_train['id'] = sales_train['id'].apply(lambda w : w.replace('_validation', ''))

calendar['date'] = pd.to_datetime(calendar['date'])

#################################################
### Filtros para alcançar as series temporais ###
#################################################
def filter_item_store(item_id, store_id):
    '''
    Funcao para filtrar os dados no nivel mais desagregado possivel - venda do item_id na store_id

    '''
    v = sales_train[(sales_train['item_id']== item_id) & (sales_train['store_id']== store_id)][cols].sum().values

    #, dtype = 'int64[pyarrow]'
    return pd.Series(v, index = calendar['date'][:-28])


def filter_dept_store(dept_id, store_id):
    '''
    Funcao para filtrar os dados no nivel da venda de todos os item_id do dept_id na store_id

    '''
    v = sales_train[(sales_train['dept_id']== dept_id) & (sales_train['store_id']== store_id)][cols].sum().values

    # , dtype = 'int64[pyarrow]'
    return pd.Series(v, index = calendar['date'][:-28])

def filter_store(store_id):
    '''
    Funcao para filtrar os dados no nivel da venda de todos os item_id na store_id

    '''
    v = sales_train[sales_train['store_id'] == store_id][cols].sum().values

    # , dtype = 'int64[pyarrow]'
    return pd.Series(v, index = calendar['date'][:-28])


def no_filter():
    '''
    Funcao para alcancar as vendas no nivel mais agregado possivel - vendas diarias da walmart como um todo

    '''
    v = sales_train[cols].sum().values
    
    # , dtype = 'int64[pyarrow]'
    return pd.Series(v, index = calendar['date'][:-28])


########################################################
### Filtros para alcanças as variaveis explanatorias ###
########################################################
def get_price(dept_id, store_id):
    '''
    retorna a variação percentual média dos preços dos item_id vendidos no dept_id na store_id

    '''
    itens = np.unique(sales_train[(sales_train['dept_id'] == dept_id) & (sales_train['store_id'] == store_id) ]['item_id'])
    v = selling_prices[(selling_prices['store_id'] == store_id) & (selling_prices['item_id'].isin(itens))].copy()
    v['pct_change_sell_price'] = v['sell_price'].pct_change()
    v.fillna(0, inplace = True)

    data = pd.merge(v, calendar[['wm_yr_wk', 'date', 'd']], on = 'wm_yr_wk', how = 'inner')\
        [['date', 'd', 'pct_change_sell_price']]
    return pd.Series(data = data['pct_change_sell_price'].values, index = data['date']).resample('D').mean()

def get_price_total():
    '''
    retorna a variação percentual média dos preços dos item_id vendidos pela walmart

    '''
    v = selling_prices.copy().groupby('wm_yr_wk')['sell_price'].mean()
    data = pd.DataFrame({'wm_yr_wk':v.index, 'sell_price_weekly':v.values})
    data['pct_change_sell_price_weekly'] = data['sell_price_weekly'].pct_change()
    data.fillna(0, inplace = True)

    data = pd.merge(data, calendar[['wm_yr_wk', 'date', 'd']], on = 'wm_yr_wk', how = 'inner')\
        [['date', 'd', 'pct_change_sell_price_weekly']]
    
    return pd.Series(data = data['pct_change_sell_price_weekly'].values, index = data['date']).resample('W').max()

def get_exp_var():
    exp_var = calendar[['date', 'd', 'weekday', 'event_type_1', 'event_type_2', 'snap_CA', 'snap_TX', 'snap_WI']].copy()
    exp_var.fillna('No_event', inplace = True)

    dummies = pd.get_dummies(\
        exp_var[['event_type_1', 'event_type_2', 'weekday']])

    for i in dummies.columns:
        a = f"{i}"
        exp_var[a] = dummies[a]

    exp_var = exp_var.drop(['date', 'd', 'event_type_1', 'event_type_2', 'event_type_1_No_event', 'event_type_2_No_event', 'weekday',\
                            'weekday_Wednesday'], axis = 1)
    exp_var.replace({False: 0, True: 1}, inplace=True)
    return exp_var


##################################################
### Construção da função para calcular o sMAPE ###
##################################################
##################################################
def calculate_smape(actual, forecast) -> float:
    # Convert actual and forecast  to numpy
    # array data type if not already
    if not all([isinstance(actual, np.ndarray), 
                isinstance(forecast, np.ndarray)]):
         actual, forecast  = np.array(actual), np.array(forecast)
  
    return round(\
        np.mean(\
        np.abs(forecast - actual) / ((np.abs(forecast) + np.abs(actual))/2))*100, \
            2)

##################################################
### Construção da função para calcular o MASE  ###
##################################################
##################################################
def MASE(training_series, testing_series, forecast_series):
    """
    Computes the MEAN-ABSOLUTE SCALED ERROR forcast error for univariate time series forecast.
    
    See "Another look at measures of forecast accuracy", Rob J Hyndman
    
    parameters:
        training_series: the series used to train the model, 1d numpy array
        testing_series: the test series to predict, 1d numpy array or float
        prediction_series: the prediction of testing_series, 1d numpy array (same size as testing_series) or float
        absolute: "squares" to use sum of squares and root the result, "absolute" to use absolute values.
    
    """
    print("Needs to be tested.")
    
    n = training_series.shape[0]
    d = np.abs(np.diff(training_series)).sum()/(n-1)
    
    errors = np.abs(testing_series - forecast_series)
    return errors.mean()/d