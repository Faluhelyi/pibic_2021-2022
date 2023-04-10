##################################################
# Note: 36h to run without pre trained models    #
# Especificacoes: intel core i5 7th gen; 8gm RAM # 
##################################################
if __name__=="__main__":
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
    from tqdm import tqdm

    ############################################################
    ##   Ajuste dos 140 (2*70) modelos SARIMAX, DHR e TBATS  ###
    #####################    &    ##############################
    ###                Submission files                      ###
    ############################################################
    SARIMAX_submission = base.sample_submission.copy()
    DHR_submission = base.sample_submission.copy()
    TBATS_submission = base.sample_submission.copy()
    c = 0
    while c <= 1:
        iter = '_validation' if c ==0 else '_evaluation'
        for index, id in enumerate(tqdm(base.sales_train['id'])):
            id_ = f'{id}{iter}'
            item = base.sales_train.loc[index]['item_id']
            dept = base.sales_train.loc[index][['dept_id', 'store_id']][0]
            store = base.sales_train.loc[index][['dept_id', 'store_id']][1]
            state = base.sales_train.loc[index]['state_id']
            serie_valid = base.filter_dept_store(dept, store)[0:-28].values
            serie_eva = base.filter_dept_store(dept, store).values
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
            #########  & ###########
            ##     Forecasts      ##
            ########################
            if iter == '_validation':
                ## SARIMAX
                if os.path.exists(f'{base.INPUT_DIR}/SARIMAX_models/{dept}_{store}_validation.pkl'):
                    result_sarimax_valid = joblib.load(f'{base.INPUT_DIR}/SARIMAX_models/{dept}_{store}_validation.pkl')
                    sarimax_forecast_valid = result_sarimax_valid.predict(28, X= exp_var[1913:1941])

                else:
                    result_sarimax_valid = pm.auto_arima(\
                        serie_valid, d = 1, start_p=0, start_q=0, max_p=3, max_q=3,\
                            seasonal = True, m = 7, D=1, start_P=0, start_Q=0, max_P=1, max_Q=1,\
                                information_criterion='aic', error_action='ignore', stepwise=True,\
                                    X = exp_var[0:1913]
                            )
                    sarimax_forecast_valid = result_sarimax_valid.predict(28, X= exp_var[1913:1941])
                    joblib.dump(result_sarimax_valid, f'{base.INPUT_DIR}/SARIMAX_models/{dept}_{store}_validation.pkl')
                ##
                ## DHR
                if os.path.exists(f'{base.INPUT_DIR}/DHR_models/{dept}_{store}_validation.pkl'):
                    trans = FourierFeaturizer((365.25/12), 3)
                    y_prime, x_f = trans.fit_transform(serie_valid)

                    result_dhr_valid = joblib.load(f'{base.INPUT_DIR}/DHR_models/{dept}_{store}_validation.pkl')
                    dhr_forecast_valid = result_dhr_valid.predict(28, X= pd.concat([exp_var[1913:1941].reset_index(), pd.DataFrame(x_f[-28:])\
                                                                                    .reset_index()], axis = 1).drop(['index'], axis = 1))

                else:
                    trans = FourierFeaturizer((365.25/12), 3)
                    y_prime, x_f = trans.fit_transform(serie_valid)

                    result_dhr_valid = pm.auto_arima(\
                        serie_valid, d = 1, start_p=0, start_q=0, max_p=3, max_q=3,\
                            seasonal = True, m = 7, D=1, start_P=0, start_Q=0, max_P=1, max_Q=1,\
                                information_criterion='aic', error_action='ignore', stepwise=True,\
                                    X = pd.concat([exp_var[0:1913], pd.DataFrame(x_f)], axis = 1)
                            )
                    dhr_forecast_valid = result_dhr_valid.predict(28, X= pd.concat([exp_var[1913:1941].reset_index(), pd.DataFrame(x_f[-28:])\
                                                                                    .reset_index()], axis = 1).drop(['index'], axis = 1))
                    joblib.dump(result_dhr_valid, f'{base.INPUT_DIR}/DHR_models/{dept}_{store}_validation.pkl')
                ##
                ## TBATS
                if os.path.exists(f'{base.INPUT_DIR}/TBATS_models/{dept}_{store}_validation.pkl'):
                    fitted_tbats = joblib.load(f'{base.INPUT_DIR}/TBATS_models/{dept}_{store}_validation.pkl')
                    tbats_forecast_valid = fitted_tbats.forecast(steps = 28)
                
                else:
                    result_tbats = TBATS(seasonal_periods=[365.25, 365.25/12, 7], n_jobs=1,\
                                         use_box_cox= False, use_arma_errors=False)
                    fitted_tbats = result_tbats.fit(serie_valid)
                    tbats_forecast_valid = fitted_tbats.forecast(steps = 28)
                    joblib.dump(fitted_tbats, f'{base.INPUT_DIR}/TBATS_models/{dept}_{store}_validation.pkl')

                #################################################################################################
                ### Top-Down approach - top-down Gross-Sohl method F (Proportions of the historical averages) ###
                #################################################################################################
                proportion = np.mean(base.filter_item_store(item, store)[-56:-28]/base.filter_dept_store(dept, store)[-56:-28])
                disaggregated_sarimax = proportion*sarimax_forecast_valid
                disaggregated_dhr = proportion*dhr_forecast_valid
                disaggregated_tbats = proportion*tbats_forecast_valid

                ########################
                ### Submission files ###
                ########################
                index_ = base.sample_submission[base.sample_submission['id'] == id_].index[0]
                SARIMAX_submission.iloc[index_, 1:] = np.round(disaggregated_sarimax, 0)
                DHR_submission.iloc[index_, 1:] = np.round(disaggregated_dhr, 0)
                TBATS_submission.iloc[index_, 1:] = np.round(disaggregated_tbats, 0)

            elif iter == '_evaluation':
                ## SARIMAX
                if os.path.exists(f'{base.INPUT_DIR}/SARIMAX_models/{dept}_{store}_evaluation.pkl'):
                    result_sarimax_eva = joblib.load(f'{base.INPUT_DIR}/SARIMAX_models/{dept}_{store}_evaluation.pkl')
                    sarimax_forecast_eva = result_sarimax_eva.predict(28, X= exp_var[1941:])

                else:
                    result_sarimax_eva = pm.auto_arima(\
                            serie_eva, d = 1, start_p=0, start_q=0, max_p=3, max_q=3,\
                                seasonal = True, m = 7, D=1, start_P=0, start_Q=0, max_P=1, max_Q=1,\
                                    information_criterion='aic', error_action='ignore', stepwise=True,\
                                        X = exp_var[0:1941]
                                )
                    sarimax_forecast_eva = result_sarimax_eva.predict(28, X= exp_var[1941:])
                    joblib.dump(result_sarimax_eva, f'{base.INPUT_DIR}/SARIMAX_models/{dept}_{store}_evaluation.pkl')
                ##
                ## DHR
                if os.path.exists(f'{base.INPUT_DIR}/DHR_models/{dept}_{store}_evaluation.pkl'):
                    trans = FourierFeaturizer((365.25/12), 3)
                    y_prime, x_f = trans.fit_transform(serie_eva)

                    result_dhr_eva = joblib.load(f'{base.INPUT_DIR}/DHR_models/{dept}_{store}_evaluation.pkl')
                    dhr_forecast_eva = result_sarimax_eva.predict(28, X= pd.concat([exp_var[1941:].reset_index(), pd.DataFrame(x_f[-28:])\
                                                                                    .reset_index()], axis = 1).drop(['index'], axis = 1))

                else:
                    trans = FourierFeaturizer((365.25/12), 3)
                    y_prime, x_f = trans.fit_transform(serie_eva)

                    result_dhr_eva = pm.auto_arima(\
                            serie_eva, d = 1, start_p=0, start_q=0, max_p=3, max_q=3,\
                                seasonal = True, m = 7, D=1, start_P=0, start_Q=0, max_P=1, max_Q=1,\
                                    information_criterion='aic', error_action='ignore', stepwise=True,\
                                        X = pd.concat([exp_var[0:1941], pd.DataFrame(x_f)], axis = 1)
                                )
                    dhr_forecast_eva = result_dhr_eva.predict(28, X= pd.concat([exp_var[1941:].reset_index(), pd.DataFrame(x_f[-28:])\
                                                                                    .reset_index()], axis = 1).drop(['index'], axis = 1))
                    joblib.dump(result_dhr_eva, f'{base.INPUT_DIR}/DHR_models/{dept}_{store}_evaluation.pkl')

                ##
                ## TBATS
                if os.path.exists(f'{base.INPUT_DIR}/TBATS_models/{dept}_{store}_evaluation.pkl'):
                    fitted_tbats = joblib.load(f'{base.INPUT_DIR}/TBATS_models/{dept}_{store}_evaluation.pkl')
                    tbats_forecast_eva = fitted_tbats.forecast(steps = 28)
                
                else:
                    result_tbats = TBATS(seasonal_periods=[365.25, 365.25/12, 7], n_jobs=1,\
                                         use_box_cox= False, use_arma_errors=False)
                    fitted_tbats = result_tbats.fit(serie_eva)
                    tbats_forecast_eva = fitted_tbats.forecast(steps = 28)
                    joblib.dump(fitted_tbats, f'{base.INPUT_DIR}/TBATS_models/{dept}_{store}_evaluation.pkl')

                #################################################################################################
                ### Top-Down approach - top-down Gross-Sohl method F (Proportions of the historical averages) ###
                #################################################################################################
                proportion = np.mean(base.filter_item_store(item, store)[-28:]/base.filter_dept_store(dept, store)[-28:])
                disaggregated_sarimax = proportion*sarimax_forecast_eva
                disaggregated_dhr = proportion*dhr_forecast_eva
                disaggregated_tbats = proportion*tbats_forecast_eva

                ########################
                ### Submission files ###
                ########################
                index_ = base.sample_submission[base.sample_submission['id'] == id_].index[0]
                SARIMAX_submission.iloc[index_, 1:] = np.round(disaggregated_sarimax, 0)
                DHR_submission.iloc[index_, 1:] = np.round(disaggregated_dhr, 0)
                TBATS_submission.iloc[index_, 1:] = np.round(disaggregated_tbats, 0)
            break
        c = c + 1
        
    SARIMAX_submission.to_csv(f'{base.INPUT_DIR}/submission_files/SARIMAX_incbac_submission.csv', index = False)
    DHR_submission.to_csv(f'{base.INPUT_DIR}/submission_files/DHR_incbac_submission.csv', index = False)
    TBATS_submission.to_csv(f'{base.INPUT_DIR}/submission_files/TBATS_incbac_submission.csv', index = False)