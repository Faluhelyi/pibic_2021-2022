#####################################
# OS 12 DICIONARIOS PARA EVALUATION #
#####################################

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
    
    b = np.concatenate((np.array(sales_train_eva[(sales_train_eva['item_id'] == product)].groupby(['item_id'])[a].sum()), np.array([np.nan]*28)),
    axis = None)[0:1941]
        
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
        
        dict_9_eva[str(store)+'_'+str(departament)] = pd.Series(b, index = pd.to_datetime(calendar['date'][0:1941])).asfreq('D')



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
        (sales_train_eva['dept_id'] == departament)].groupby(['state_id', 'dept_id'])[a].sum()), np.array([np.nan]*28)), axis = None)[0:1941]
        
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
        (sales_train_eva['cat_id'] == category)].groupby(['state_id', 'cat_id'])[a].sum()), np.array([np.nan]*28)), axis = None)[0:1941]
        
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
    
    b = np.concatenate((np.array(sales_train_eva[(sales_train_eva['cat_id'] == category)].groupby(['cat_id'])[a].sum()), np.array([np.nan]*28)),
    axis = None)[0:1941]
    
    dict_4_eva[str(category)] = pd.Series(b, index = calendar['date'][0:1941])
        
        

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
        
        

### Dicionário 2 - sales of all products, aggregated for each State
dict_2_eva = {} # número de vendas diárias de todos produtos, agregado por cada Estado (dia 1 até dia 1941)

states = list(np.unique(sales_train_eva['state_id'].values))

a = []
for i in range(1941):
    a.append('d_' +str(i+1))
    

for state in states:
    
    b = np.concatenate((np.array(sales_train_eva[(sales_train_eva['state_id'] == state)].groupby(['state_id'])[a].sum()), np.array([np.nan]*28)),
    axis = None)[0:1941]
    
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




#####################################
# OS 12 DICIONARIOS PARA VALIDATION #
#####################################

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


### Dicionário 11 - Sales of product x, aggregated for each State
dict_11_val = {} # número de vendas diárias do produto x, agregado por cada Estado (dia 1 até dia 1913)

states = list(np.unique(sales_train_val['state_id'].values))
products = list(np.unique(sales_train_val['item_id'].values))

a = []
for i in range(1913):
    a.append('d_' +str(i+1))

for state in states:
    
    for product in products:
        
        b = np.concatenate((np.array(sales_train_val[(sales_train_val['item_id'] == product) &
        (sales_train_val['state_id'] == state)].groupby(['item_id', 'state_id'])[a].sum()), np.array([np.nan]*28)), axis = None)[0:1913]
        
        dict_11_val[str(product)+'_'+ str(state)] = pd.Series(b, index = calendar['date'][0:1913])
             

### Dicionário 10 - Sales of product x, aggregated for all stores/states
dict_10_val = {} # número de vendas diárias do produto x, agregado para todas as lojas e Estados (dia 1 até dia 1913)

products = list(np.unique(sales_train_val['item_id'].values))

a = []
for i in range(1913):
    a.append('d_' +str(i+1))
    

    
for product in products:
    
    b = np.concatenate((np.array(sales_train_val[(sales_train_val['item_id'] == product)].groupby(['item_id'])[a].sum()), np.array([np.nan]*28)),
    axis = None)[0:1913]
        
    dict_10_val[str(product)] = pd.Series(b, index = calendar['date'][0:1913])
    


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



### Dicionário 8 - sales of all products, aggregated for each store and category
dict_8_val = {} # número de vendas diárias de todos produtos, agregado por cada loja e categoria (dia 1 até dia 1913)

categories = list(np.unique(sales_train_val['cat_id'].values))
stores = list(np.unique(sales_train_val['store_id'].values))

a = []
for i in range(1913):
    a.append('d_' +str(i+1))
    

for store in stores:
    
    for category in categories:
        
        b = np.concatenate((np.array(sales_train_val[(sales_train_val['cat_id'] == category) &
        (sales_train_val['store_id'] == store)].groupby(['store_id', 'cat_id'])[a].sum()), np.array([np.nan]*28)), axis = None)[0:1913]
        
        dict_8_val[str(store)+'_'+str(category)] = pd.Series(b, index = calendar['date'][0:1913])
        
        

### Dicionário 7 - sales of all products, aggregated for each State and department
dict_7_val = {} # número de vendas diárias de todos produtos, agregado por cada Estado e departamento (dia 1 até dia 1913)

states = list(np.unique(sales_train_val['state_id'].values))
departaments = list(np.unique(sales_train_val['dept_id'].values))

a = []
for i in range(1913):
    a.append('d_' +str(i+1))
    

for state in states:
    
    for departament in departaments:
        
        b = np.concatenate((np.array(sales_train_val[(sales_train_val['state_id'] == state) &
        (sales_train_val['dept_id'] == departament)].groupby(['state_id', 'dept_id'])[a].sum()), np.array([np.nan]*28)), axis = None)[0:1913]
        
        dict_7_val[str(state)+'_'+str(departament)] = pd.Series(b, index = calendar['date'][0:1913])
        
        

### Dicionário 6 - sales of all products, aggregated for each State and category
dict_6_val = {} # número de vendas diárias de todos produtos, agregado por cada Estado e categoria (dia 1 até dia 1913)

states = list(np.unique(sales_train_val['state_id'].values))
categories = list(np.unique(sales_train_val['cat_id'].values))

a = []
for i in range(1913):
    a.append('d_' +str(i+1))
    

for state in states:
    
    for category in categories:
        
        b = np.concatenate((np.array(sales_train_val[(sales_train_val['state_id'] == state) &
        (sales_train_val['cat_id'] == category)].groupby(['state_id', 'cat_id'])[a].sum()), np.array([np.nan]*28)), axis = None)[0:1913]
        
        dict_6_val[str(state)+'_'+str(category)] = pd.Series(b, index = calendar['date'][0:1913])
        
        

### Dicionário 5 - sales of all products, aggregated for each department
dict_5_val = {} # número de vendas diárias de todos produtos, agregado por cada departamneto (dia 1 até dia 1913)

departaments = list(np.unique(sales_train_val['dept_id'].values))

a = []
for i in range(1913):
    a.append('d_' +str(i+1))
    

for departament in departaments:
    
    b = np.concatenate((np.array(sales_train_val[(sales_train_val['dept_id'] == departament)].groupby(['dept_id'])[a].sum()),
    np.array([np.nan]*28)), axis = None)[0:1913]
    
    dict_5_val[str(departament)] = pd.Series(b, index = calendar['date'][0:1913])
        
        

### Dicionário 4 - sales of all products, aggregated for each category
dict_4_val = {} # número de vendas diárias de todos produtos, agregado por categoria (dia 1 até dia 1913)

categories = list(np.unique(sales_train_val['cat_id'].values))

a = []
for i in range(1913):
    a.append('d_' +str(i+1))
    

for category in categories:
    
    b = np.concatenate((np.array(sales_train_val[(sales_train_val['cat_id'] == category)].groupby(['cat_id'])[a].sum()),
    np.array([np.nan]*28)), axis = None)[0:1913]
    
    dict_4_val[str(category)] = pd.Series(b, index = calendar['date'][0:1913])
        
        

### Dicionário 3 - sales of all products, aggregated for each store
dict_3_val = {} # número de vendas diárias de todos produtos, agregado por cada loja (dia 1 até dia 1913)

stores = list(np.unique(sales_train_val['store_id'].values))

a = []
for i in range(1913):
    a.append('d_' +str(i+1))
    

for store in stores:
    
    b = np.concatenate((np.array(sales_train_val[(sales_train_eva['store_id'] == store)].groupby(['store_id'])[a].sum()),
    np.array([np.nan]*28)), axis = None)[0:1913]
    
    dict_3_val[str(store)] = pd.Series(b, index = calendar['date'][0:1913])
        
        

### Dicionário 2 - sales of all products, aggregated for each State
dict_2_val = {} # número de vendas diárias de todos produtos, agregado por cada Estado (dia 1 até dia 1913)

states = list(np.unique(sales_train_val['state_id'].values))

a = []
for i in range(1913):
    a.append('d_' +str(i+1))
    

for state in states:
    
    b = np.concatenate((np.array(sales_train_val[(sales_train_val['state_id'] == state)].groupby(['state_id'])[a].sum()), np.array([np.nan]*28)),
    axis = None)[0:1913]
    
    dict_2_val[str(state)] = pd.Series(b, index = calendar['date'][0:1913])
        
        
### Dicionário 1 - sales of all products, aggregated for all stores/states
dict_1_val = {} # número de vendas diárias de todos produtos sem hierarquia (dia 1 até dia 1913)


a = []
for i in range(1913):
    a.append('d_' +str(i+1))
    
data1 = sales_train_val
data1['sales_filter'] = np.array(['none']*len(sales_train_val))

b = np.concatenate((np.array(data1.groupby(['sales_filter'])[a].sum()), np.array([np.nan]*28)), axis = None)[0:1913]

dict_1_val['all'] = pd.Series(b, index = calendar['date'][0:1913])

###############################################################################################################
# Construção da função para agregar os dados dos múltiplos bancos da competição (attach_datas(.)) validation ##
###############################################################################################################
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





###############################################################################################################
# Construção da função para agregar os dados dos múltiplos bancos da competição (attach_datas(.)) evaluation ##
###############################################################################################################


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