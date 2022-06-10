############################################
#### BIBLIOTECAS E IMPORTACAO DOS DADOS ####
############################################

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# lendo os dados
INPUT_DIR = 'C:/Users/Igor/Desktop/PIBIC 2021 e 2022/Dados'

calendar = pd.read_csv(f'{INPUT_DIR}/calendar.csv')
selling_prices = pd.read_csv(f'{INPUT_DIR}/sell_prices.csv')
sample_submission = pd.read_csv(f'{INPUT_DIR}/sample_submission.csv')
sales_train_val = pd.read_csv(f'{INPUT_DIR}/sales_train_validation.csv') #sales_train d_1 ate d_1913
sales_train_eva = pd.read_csv(f'{INPUT_DIR}/sales_train_evaluation.csv') #sales_train d_1 ate d_1941

# NOTE: o banco sales_train_eva contempla o sales_train_val e ainda adciona observacoes das vendas dos dias d_1914 - d_1941

############################################
#### ANALISE EXPLORATORIA DOS DADOS ########
############################################

print(calendar.head(3))
print(selling_prices.head(3))
print(sample_submission.head(3))
print(sales_train_val.head(3))
print(sales_train_eva.head(3))