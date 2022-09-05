#########################################################
###### TEMPO PARA RODAR O CÓDIGO:  15min    #############
#########################################################

############################################
############## BIBLIOTECAS #################
############################################

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

import warnings


############################################
########## IMPORTACAO DOS DADOS ############
############################################

INPUT_DIR = 'C:/Users/Igor/Desktop/PIBIC 2021 e 2022/Dados'

calendar = pd.read_csv(f'{INPUT_DIR}/calendar.csv')
selling_prices = pd.read_csv(f'{INPUT_DIR}/sell_prices.csv')
sample_submission = pd.read_csv(f'{INPUT_DIR}/sample_submission.csv')
sales_train_val = pd.read_csv(f'{INPUT_DIR}/sales_train_validation.csv') #sales_train d_1 ate d_1913
sales_train_eva = pd.read_csv(f'{INPUT_DIR}/sales_train_evaluation.csv') #sales_train d_1 ate d_1941

# NOTE: o banco sales_train_eva contempla o sales_train_val e ainda adciona observacoes das vendas dos dias d_1914 - d_1941


############################################
#### Construção dos dicionários (filtros) ##
####        para evaluation               ##
############################################


### Dicionário 12 - Sales of product x, aggregated for each store
dict_12_eva = {} # número de vendas diárias do produto x, agregado por cada loja (dia 1 até dia 1941) 

stores = list(np.unique(sales_train_eva['store_id'].values))
products = list(np.unique(sales_train_eva['item_id'].values))

a = []
for i in range(1941):
    a.append('d_' +str(i+1))

for store in stores:
    
    for product in products:
        
        b = np.concatenate((np.array(sales_train_eva[(sales_train_eva['item_id'] == product) &
        (sales_train_eva['store_id'] == store)].groupby(['store_id', 'item_id']).sum()), np.array([np.nan]*28)), axis = None)[0:1941]
        
        dict_12_eva[str(product)+'_'+ str(store)+'_evaluation'] = pd.Series(b, index = pd.to_datetime(calendar['date'][0:1941])).asfreq('D')

### Dicionário 9 - Sales of all products, aggregated for each store and department
dict_9_eva = {} # número de vendas diárias de todos produtos, agregado por cada loja e departamento (dia 1 até dia 1941)

departaments = list(np.unique(sales_train_eva['dept_id'].values))
stores = list(np.unique(sales_train_eva['store_id'].values))

a = []
for i in range(1941):
    a.append('d_' +str(i+1))
    

for store in stores:
    
    for departament in departaments:
        
        b = np.concatenate((np.array(sales_train_eva[(sales_train_eva['dept_id'] == departament) &
        (sales_train_eva['store_id'] == store)].groupby(['store_id', 'dept_id'])[a].sum()), np.array([np.nan]*28)), axis = None)[0:1941]
        
        dict_9_eva[str(store)+'_'+str(departament)] = pd.Series(b, index = pd.to_datetime(calendar['date'][0:1941])).asfreq('D')



### Dicionário 3 - sales of all products, aggregated for each store
dict_3_eva = {} # número de vendas diárias de todos produtos, agregado por cada loja (dia 1 até dia 1941)

stores = list(np.unique(sales_train_eva['store_id'].values))

a = []
for i in range(1941):
    a.append('d_' +str(i+1))
    

for store in stores:
    
    b = np.concatenate((np.array(sales_train_eva[(sales_train_eva['store_id'] == store)].groupby(['store_id'])[a].sum()), np.array([np.nan]*28)),
    axis = None)[0:1941]
    
    dict_3_eva[str(store)] = pd.Series(b, index = calendar['date'][0:1941])


### Dicionário 1 - sales of all products, aggregated for all stores/states
dict_1_eva = {} # número de vendas diárias de todos produtos sem hierarquia (dia 1 até dia 1941)


a = []
for i in range(1941):
    a.append('d_' +str(i+1))
    
data1 = sales_train_eva
data1['sales_filter'] = np.array(['none']*len(sales_train_eva))

b = np.concatenate((np.array(data1.groupby(['sales_filter'])[a].sum()), np.array([np.nan]*28)), axis = None)[0:1941]

dict_1_eva['all'] = pd.Series(b, index = pd.to_datetime(calendar['date'][0:1941])).asfreq('D')

############################################
#### Construção dos dicionários (filtros) ##
####        para validation               ##
############################################


### Dicionário 12 - Sales of product x, aggregated for each store
dict_12_val = {} # número de vendas diárias do produto x, agregado por cada loja (dia 1 até dia 1913) 

stores = list(np.unique(sales_train_val['store_id'].values))
products = list(np.unique(sales_train_val['item_id'].values))

a = []
for i in range(1913):
    a.append('d_' +str(i+1))

for store in stores:
    
    for product in products:
        
        b = np.concatenate((np.array(sales_train_val[(sales_train_val['item_id'] == product) &
        (sales_train_val['store_id'] == store)].groupby(['store_id', 'item_id']).sum()), np.array([np.nan]*28)), axis = None)[0:1913]
        
        dict_12_val[str(product)+'_'+ str(store)+'_validation'] = pd.Series(b, index = pd.to_datetime(calendar['date'][0:1913])).asfreq('D')

### Dicionário 9 - Sales of all products, aggregated for each store and department
dict_9_val = {} # número de vendas diárias de todos produtos, agregado por cada loja e departamento (dia 1 até dia 1913)

departaments = list(np.unique(sales_train_val['dept_id'].values))
stores = list(np.unique(sales_train_val['store_id'].values))

a = []
for i in range(1913):
    a.append('d_' +str(i+1))
    

for store in stores:
    
    for departament in departaments:
        
        b = np.concatenate((np.array(sales_train_val[(sales_train_val['dept_id'] == departament) &
        (sales_train_val['store_id'] == store)].groupby(['store_id', 'dept_id'])[a].sum()), np.array([np.nan]*28)), axis = None)[0:1913]
        
        dict_9_val[str(store)+'_'+str(departament)] = pd.Series(b, index = pd.to_datetime(calendar['date'][0:1913])).asfreq('D')



### Dicionário 1 - sales of all products, aggregated for all stores/states
dict_1_val = {} # número de vendas diárias de todos produtos sem hierarquia (dia 1 até dia 1913)


a = []
for i in range(1913):
    a.append('d_' +str(i+1))
    
data1 = sales_train_val
data1['sales_filter'] = np.array(['none']*len(sales_train_val))

b = np.concatenate((np.array(data1.groupby(['sales_filter'])[a].sum()), np.array([np.nan]*28)), axis = None)[0:1913]

dict_1_val['all'] = pd.Series(b, index = pd.to_datetime(calendar['date'][0:1913])).asfreq('D')


##################################################
### Construção da função para agregar os dados ###
####    dos múltiplos bancos da competição     ###
####    (attach_datas(.)) validation           ###
##################################################
##################################################

def attach_datas_val(filtro, store_id, dept_id):
    '''Função que retorna um data frame com as informações de calendar.csv, sell_prices.csv e
    sales_train_validation.csv dado dict_9_val[store_id_dept_id] como entrada
    
    Argumentos:
    
    filtro pode assumir qualquer valor dentro do dict_9_val;
    store_id é uma string do id da loja;
    dept_id é uma string do id do departamento.
    
    '''
    b = pd.DataFrame(calendar.loc[0:1940, ])
    b['#sales'] = np.concatenate((np.array(filtro), np.array([np.nan]*28)), axis = None)

    selling_prices['id'] = selling_prices['item_id'] + '_' + selling_prices['store_id'] + '_validation'
    
    c = selling_prices[selling_prices['id'].isin([i for i in sales_train_val['id'] if ((store_id in i) & 
    (dept_id in i))])][selling_prices['wm_yr_wk'] <= 11617].groupby('wm_yr_wk').mean() 
        
    m = pd.merge(b, c, how = 'outer', on = 'wm_yr_wk')

    m['date'] = pd.to_datetime(m['date'])

    m.set_index('date', inplace = True)

    m.rename(columns={'sell_price':'media_preco_de_venda'}, inplace = True)

    m['filtro'] = str(dept_id) + '_' + str(store_id) + '_validation'
    
    return pd.get_dummies(m, dummy_na= True, columns=['event_name_1', 'event_type_1', 'event_name_2', 'event_type_2'])


##################################################
### Construção da função para agregar os dados ###
####    dos múltiplos bancos da competição     ###
####    (attach_datas(.)) evaluation           ###
##################################################
##################################################

def attach_datas_eva(filtro, store_id, dept_id):
    '''Função que retorna um data frame com as informações de calendar.csv, sell_prices.csv e
    sales_train_evaluation.csv dado dict_9_val[store_id_dept_id] como entrada
    
    Argumentos:
    
    filtro pode assumir qualquer valor dentro do dict_9_eva;
    store_id é uma string do id da loja;
    dept_id é uma string do id do departamento.
    
    '''
    
    b = calendar
    b['#sales'] = np.concatenate((np.array(filtro), np.array([np.nan]*28)), axis = None)

    selling_prices['id'] = selling_prices['item_id'] + '_' + selling_prices['store_id'] + '_evaluation'
    
    c = selling_prices[selling_prices['id'].isin([i for i in sales_train_eva['id'] if ((store_id in i) & 
    (dept_id in i))])].groupby('wm_yr_wk').mean()
        
    m = pd.merge(b, c, how = 'outer', on = 'wm_yr_wk')

    m['date'] = pd.to_datetime(m['date'])

    m.set_index('date', inplace = True)

    m.rename(columns={'sell_price':'media_preco_de_venda'}, inplace = True)

    m['filtro'] = str(dept_id) + '_' + str(store_id) + '_evaluation'

    
    return pd.get_dummies(m, dummy_na= True, columns=['event_name_1', 'event_type_1', 'event_name_2', 'event_type_2'])