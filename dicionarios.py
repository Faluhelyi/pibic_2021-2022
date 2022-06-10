############################################
#### BIBLIOTECAS E IMPORTAÇÃO DOS DADOS ####
############################################

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# lendo os dados
INPUT_DIR = 'C:/Users/Igor/Desktop/PIBIC 2021 e 2022/Dados'

calendar = pd.read_csv(f'{INPUT_DIR}/calendar.csv')
selling_prices = pd.read_csv(f'{INPUT_DIR}/sell_prices.csv')
sample_submission = pd.read_csv(f'{INPUT_DIR}/sample_submission.csv')
sales_train_val = pd.read_csv(f'{INPUT_DIR}/sales_train_validation.csv') #sales_train d_1 até d_1913
sales_train_eva = pd.read_csv(f'{INPUT_DIR}/sales_train_evaluation.csv') #sales_train d_1 até d_1941

# NOTE: o banco sales_train_eva contempla o sales_train_val e ainda adciona observações das vendas dos dias d_1914 - d_1941


#############################################################
######## CONSTRUÇÃO DOS DICIONÁRIOS PARA EVALUATION #########
#############################################################


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
        
        dict_12_eva[str(product)+'_'+ str(store)] = pd.Series(b, index = calendar['date'][0:1941])


### Dicionário 11 - Sales of product x, aggregated for each State
dict_11_eva = {} # número de vendas diárias do produto x, agregado por cada Estado (dia 1 até dia 1941)

states = list(np.unique(sales_train_eva['state_id'].values))
products = list(np.unique(sales_train_eva['item_id'].values))

a = []
for i in range(1941):
    a.append('d_' +str(i+1))

for state in states:
    
    for product in products:
        
        b = np.concatenate((np.array(sales_train_eva[(sales_train_eva['item_id'] == product) &
        (sales_train_eva['state_id'] == state)].groupby(['item_id', 'state_id'])[a].sum()), np.array([np.nan]*28)), axis = None)[0:1941]
        
        dict_11_eva[str(product)+'_'+ str(state)] = pd.Series(b, index = calendar['date'][0:1941])
             

### Dicionário 10 - Sales of product x, aggregated for all stores/states
dict_10_eva = {} # número de vendas diárias do produto x, agregado para todas as lojas e Estados (dia 1 até dia 1941)

products = list(np.unique(sales_train_eva['item_id'].values))

a = []
for i in range(1941):
    a.append('d_' +str(i+1))
    

    
for product in products:
    
    b = np.concatenate((np.array(sales_train_eva[(sales_train_eva['item_id'] == product)].groupby(['item_id'])[a].sum()),
    np.array([np.nan]*28)), axis = None)[0:1941]
        
    dict_10_eva[str(product)] = pd.Series(b, index = calendar['date'][0:1941])
    


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
        
        dict_9_eva[str(store)+'_'+str(departament)] = pd.Series(b, index = calendar['date'][0:1941])



### Dicionário 8 - sales of all products, aggregated for each store and category
dict_8_eva = {} # número de vendas diárias de todos produtos, agregado por cada loja e categoria (dia 1 até dia 1941)

categories = list(np.unique(sales_train_eva['cat_id'].values))
stores = list(np.unique(sales_train_eva['store_id'].values))

a = []
for i in range(1941):
    a.append('d_' +str(i+1))
    

for store in stores:
    
    for category in categories:
        
        b = np.concatenate((np.array(sales_train_eva[(sales_train_eva['cat_id'] == category) &
        (sales_train_eva['store_id'] == store)].groupby(['store_id', 'cat_id'])[a].sum()), np.array([np.nan]*28)), axis = None)[0:1941]
        
        dict_8_eva[str(store)+'_'+str(category)] = pd.Series(b, index = calendar['date'][0:1941])
        
        

### Dicionário 7 - sales of all products, aggregated for each State and department
dict_7_eva = {} # número de vendas diárias de todos produtos, agregado por cada Estado e departamento (dia 1 até dia 1941)

states = list(np.unique(sales_train_eva['state_id'].values))
departaments = list(np.unique(sales_train_eva['dept_id'].values))

a = []
for i in range(1941):
    a.append('d_' +str(i+1))
    

for state in states:
    
    for departament in departaments:
        
        b = np.concatenate((np.array(sales_train_eva[(sales_train_eva['state_id'] == state) &
        (sales_train_eva['dept_id'] == departament)].groupby(['state_id', 'dept_id'])[a].sum()), np.array([np.nan]*28)),
        axis = None)[0:1941]
        
        dict_7_eva[str(state)+'_'+str(departament)] = pd.Series(b, index = calendar['date'][0:1941])
        
        

### Dicionário 6 - sales of all products, aggregated for each State and category
dict_6_eva = {} # número de vendas diárias de todos produtos, agregado por cada Estado e categoria (dia 1 até dia 1941)

states = list(np.unique(sales_train_eva['state_id'].values))
categories = list(np.unique(sales_train_eva['cat_id'].values))

a = []
for i in range(1941):
    a.append('d_' +str(i+1))
    

for state in states:
    
    for category in categories:
        
        b = np.concatenate((np.array(sales_train_eva[(sales_train_eva['state_id'] == state) &
        (sales_train_eva['cat_id'] == category)].groupby(['state_id', 'cat_id'])[a].sum()), np.array([np.nan]*28)),
        axis = None)[0:1941]
        
        dict_6_eva[str(state)+'_'+str(category)] = pd.Series(b, index = calendar['date'][0:1941])
        
        

### Dicionário 5 - sales of all products, aggregated for each department
dict_5_eva = {} # número de vendas diárias de todos produtos, agregado por cada departamneto (dia 1 até dia 1941)

departaments = list(np.unique(sales_train_eva['dept_id'].values))

a = []
for i in range(1941):
    a.append('d_' +str(i+1))
    

for departament in departaments:
    
    b = np.concatenate((np.array(sales_train_eva[(sales_train_eva['dept_id'] == departament)].groupby(['dept_id'])[a].sum()),
    np.array([np.nan]*28)), axis = None)[0:1941]
    
    dict_5_eva[str(departament)] = pd.Series(b, index = calendar['date'][0:1941])
        
        

### Dicionário 4 - sales of all products, aggregated for each category
dict_4_eva = {} # número de vendas diárias de todos produtos, agregado por categoria (dia 1 até dia 1941)

categories = list(np.unique(sales_train_eva['cat_id'].values))

a = []
for i in range(1941):
    a.append('d_' +str(i+1))
    

for category in categories:
    
    b = np.concatenate((np.array(sales_train_eva[(sales_train_eva['cat_id'] == category)].groupby(['cat_id'])[a].sum()),
    np.array([np.nan]*28)), axis = None)[0:1941]
    
    dict_4_eva[str(category)] = pd.Series(b, index = calendar['date'][0:1941])
        
        

### Dicionário 3 - sales of all products, aggregated for each store
dict_3_eva = {} # número de vendas diárias de todos produtos, agregado por cada loja (dia 1 até dia 1941)

stores = list(np.unique(sales_train_eva['store_id'].values))

a = []
for i in range(1941):
    a.append('d_' +str(i+1))
    

for store in stores:
    
    b = np.concatenate((np.array(sales_train_eva[(sales_train_eva['store_id'] == store)].groupby(['store_id'])[a].sum()),
    np.array([np.nan]*28)), axis = None)[0:1941]
    
    dict_3_eva[str(store)] = pd.Series(b, index = calendar['date'][0:1941])
        
        

### Dicionário 2 - sales of all products, aggregated for each State
dict_2_eva = {} # número de vendas diárias de todos produtos, agregado por cada Estado (dia 1 até dia 1941)

states = list(np.unique(sales_train_eva['state_id'].values))

a = []
for i in range(1941):
    a.append('d_' +str(i+1))
    

for state in states:
    
    b = np.concatenate((np.array(sales_train_eva[(sales_train_eva['state_id'] == state)].groupby(['state_id'])[a].sum()),
    np.array([np.nan]*28)), axis = None)[0:1941]
    
    dict_2_eva[str(state)] = pd.Series(b, index = calendar['date'][0:1941])
        
        
### Dicionário 1 - sales of all products, aggregated for all stores/states
dict_1_eva = {} # número de vendas diárias de todos produtos sem hierarquia (dia 1 até dia 1941)


a = []
for i in range(1941):
    a.append('d_' +str(i+1))
    
data1 = sales_train_eva
data1['sales_filter'] = np.array(['none']*len(sales_train_eva))

b = np.concatenate((np.array(data1.groupby(['sales_filter'])[a].sum()), np.array([np.nan]*28)), axis = None)[0:1941]

dict_1_eva['all'] = pd.Series(b, index = calendar['date'][0:1941])


#############################################################
######## CONSTRUÇÃO DOS DICIONÁRIOS PARA VALIDATION #########
#############################################################

# Segue a mesma estrutura que a construção para Evaluation
# porém, utiliza-se os dados de sales_train_val
