#############################################################
######## CONSTRUCAO DO DICIONARIO 9 PARA EVALUATION #########
#############################################################

### Dicionario 9 - Sales of all products, aggregated for each store and department
dict_9_eva = {} # numero de vendas diarias de todos produtos, agregado por cada loja e departamento (dia 1 ate dia 1941)

departaments = list(np.unique(sales_train_eva['dept_id'].values))
stores = list(np.unique(sales_train_eva['store_id'].values))

a = []
for i in range(1941):
    a.append('d_' +str(i+1))
    

for store in stores:
    
    for departament in departaments:
        
        b = np.concatenate((np.array(
            sales_train_eva[(sales_train_eva['dept_id'] == departament) &
        (sales_train_eva['store_id'] == store)].groupby(['store_id', 'dept_id'])[a].sum()),
        np.array([np.nan]*28)), axis = None)[0:1941]
        
        dict_9_eva[str(store)+'_'+str(departament)] = pd.Series(b, index = calendar['date'][0:1941])



#############################################################
######## CONSTRUCAO DO DICIONARIO 9 PARA VALIDATION #########
#############################################################


### Dicionario 9 - Sales of all products, aggregated for each store and department
dict_9_val = {} # numero de vendas diarias de todos produtos, agregado por cada loja e departamento (dia 1 ate dia 1913)

departaments = list(np.unique(sales_train_val['dept_id'].values))
stores = list(np.unique(sales_train_val['store_id'].values))

a = []
for i in range(1913):
    a.append('d_' +str(i+1))
    

for store in stores:
    
    for departament in departaments:
        
        b = np.concatenate((np.array(
            sales_train_val[(sales_train_val['dept_id'] == departament) &
        (sales_train_val['store_id'] == store)].groupby(['store_id', 'dept_id'])[a].sum()),
        np.array([np.nan]*28)), axis = None)[0:1913]
        
        dict_9_val[str(store)+'_'+str(departament)] = pd.Series(b, index = calendar['date'][0:1913])


###############################################################
######## CONSTRUCAO DA FUNCAO ATTACH_DATAS(.) PARA VALIDATION #
###############################################################

def attach_datas_val(filtro, store_id, dept_id):
    '''Função que retorna um data frame com as informações de calendar.csv, sell_prices.csv e
    sales_train_validation.csv dado dict_9_val[store_id_dept_id] como entrada
    
    Argumentos:
    
    filtro pode assumir qualquer valor dentro do dict_9_val;
    store_id é uma string do id da loja;
    dept_id é uma string do id do departamento.
    
    '''
    
    b = calendar.loc[0:1940,]
    b['#sales'] = np.concatenate((np.array(filtro), np.array([np.nan]*28)), axis = None)

    selling_prices['id'] = selling_prices['item_id'] + '_' + selling_prices['store_id'] + '_validation'
    
    c = selling_prices[selling_prices['id'].isin([i for i in sales_train_val['id'] if ((store_id in i) & 
    (dept_id in i))])][selling_prices['wm_yr_wk'] <= 11617].groupby('wm_yr_wk').mean()
        
    m = pd.merge(b, c, how = 'outer', on = 'wm_yr_wk')

    m['date'] = pd.to_datetime(m['date'])

    m.set_index('date', inplace = True)

    m.rename(columns={'sell_price':'media_preco_de_venda'}, inplace = True)

    m['filtro'] = str(dept_id) + '_' + str(store_id) + '_validation'
    
    return pd.get_dummies(m, dummy_na= True, columns=['event_name_1', 'event_type_1', 'event_name_2','event_type_2'])



###############################################################
######## CONSTRUCAO DA FUNCAO ATTACH_DATAS(.) PARA EVALUATION #
###############################################################

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

    
    return pd.get_dummies(m, dummy_na= True, columns=['event_name_1', 'event_type_1', 'event_name_2','event_type_2'])
