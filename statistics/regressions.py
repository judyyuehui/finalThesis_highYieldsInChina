# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
import scipy
from scipy.stats import f
import scipy.stats as stats
# additional packages
from statsmodels.stats.diagnostic import lillifors
from pylab import mpl
from scipy import stats

data_address = '~/Downloads/data/a/'
monthly_cb_value = pd.read_csv(data_address + 'monthly_cb_value_fin.csv')
high_yield_bond = pd.read_csv(data_address + 'high_yield_bond.csv')
low_rate_bond = pd.read_csv(data_address + 'low_rate_bond.csv')

# data clean(if already cleaned in the statistic measure.ipynb, skip this part)
'''
    monthly_cb_value['key_1'] = monthly_cb_value.returns_n.isnull()
    monthly_cb_value = monthly_cb_value[monthly_cb_value['key_1'] == False]
    
    monthly_cb_value['key_1'] = monthly_cb_value.returns.isnull()
    monthly_cb_value = monthly_cb_value[monthly_cb_value['key_1'] == False]
    
    
    monthly_cb_value['key_1'] = monthly_cb_value.returns_p.isnull()
    monthly_cb_value = monthly_cb_value[monthly_cb_value['key_1'] == False]
    monthly_cb_value['default_spread'] = monthly_cb_value['default_spread'].fillna(0)
    monthly_cb_value['downside_risk_3'] = -1 * monthly_cb_value['downside_risk_3']
    
    #对high_yield等用相同的方法
    high_yield_bond['key_1'] = high_yield_bond.returns_n.isnull()
    high_yield_bond = high_yield_bond[high_yield_bond['key_1'] == False]
    
    high_yield_bond['key_1'] = high_yield_bond.returns.isnull()
    high_yield_bond = high_yield_bond[high_yield_bond['key_1'] == False]
    
    
    high_yield_bond['key_1'] = high_yield_bond.returns_p.isnull()
    high_yield_bond = high_yield_bond[high_yield_bond['key_1'] == False]
    high_yield_bond['default_spread'] = high_yield_bond['default_spread'].fillna(0)
    high_yield_bond['downside_risk_3'] = -1 * high_yield_bond['downside_risk_3']
    
    low_rate_bond['key_1'] = low_rate_bond.returns_n.isnull()
    low_rate_bond = low_rate_bond[low_rate_bond['key_1'] == False]
    
    low_rate_bond['key_1'] = low_rate_bond.returns.isnull()
    low_rate_bond = low_rate_bond[low_rate_bond['key_1'] == False]
    
    
    low_rate_bond['key_1'] = low_rate_bond.returns_p.isnull()
    low_rate_bond = low_rate_bond[low_rate_bond['key_1'] == False]
    low_rate_bond['default_spread'] = low_rate_bond['default_spread'].fillna(0)
    low_rate_bond['downside_risk_3'] = -1 * low_rate_bond['downside_risk_3']
    
    columns_decile = ['close', 'coupon','credit_q', 'default_spread',
    'downside_risk', 'high', 'illiq_1', 'illiq_2',
    'kurt', 'low','open', 'res_day',
    'returns', 'returns_n', 'returns_p', 'skew', 'total_size',
    'total_sizevol', 'trade_month', 'trade_num', 'trade_value',
    'trade_year', 'vol', 'yields', 'downside_risk_2', 'illiq_1_2',
    'illiq_2_2', 'downside_risk_3', 'log_trade_value']
    
    #删除不可用值之后的数据是Month_cb_value_del1.csv
    #对应的low_rate_bond_del1.csv和high_yield_bond_del1.csv
    
    '''

#
# ### 1. Linear Regression 
# use returns_p, log_trade_value, res_day, vol, extreme, skew, coupon, total size, coupon
# as main factors
# return_n(lagged return is the dependent variable)
#

fm_regression = monthly_cb_value.copy() 
#change fm_regression can use different dataset(can use it as a incomplete function)

formular = 'returns_n ~ 1 + downside_risk_2'
downside_risk_reg1 = smf.ols(formular,data=fm_regression).fit()
formular = 'returns_n ~ 1 + downside_risk_2 + returns_p + log_trade_value + res_day + extreme + skew + coupon + total_size + coupon'
downside_risk_reg2 = smf.ols(formular,data=fm_regression).fit()

formular = 'returns_n ~ 1 + status_dsr'
downside_risk_reg1 = smf.ols(formular,data=fm_regression).fit()
formular = 'returns_n ~ 1 + status_dsr + returns_p + log_trade_value + res_day + extreme + skew + coupon + total_size + coupon'
downside_risk_reg2 = smf.ols(formular,data=fm_regression).fit()

formular = 'returns_n ~ 1 + vol'
downside_risk_reg1 = smf.ols(formular,data=fm_regression).fit()
formular = 'returns_n ~ 1 + vol + returns_p + log_trade_value + res_day + extreme + skew + coupon + total_size + coupon'
downside_risk_reg2 = smf.ols(formular,data=fm_regression).fit()

formular = 'returns_n ~ 1 + illiq_2_2'
illiq2_risk_reg1 = smf.ols(formular,data=fm_regression).fit()
formular = 'returns_n ~ 1 + illiq_2_2 + returns_p + log_trade_value + res_day + extreme + skew + coupon + total_size + coupon'
illiq2_reg2 = smf.ols(formular,data=fm_regression).fit()

formular = 'returns_n ~ 1 + credit_q'
returns_reg1 = smf.ols(formular,data=fm_regression).fit()
formular = 'returns_n ~ 1 + credit_q  + returns_p  + log_trade_value + res_day + extreme + skew + coupon + total_size + coupon'
returns_reg2 = smf.ols(formular,data=fm_regression).fit()

formular = 'returns_n ~ 1 + default_spread'
filter2_reg1 = smf.ols(formular,data=fm_regression).fit()
formular = 'returns_n ~ 1 + default_spread  + returns_p  + log_trade_value + res_day + extreme + skew + coupon + total_size + coupon'
filter2_reg2 = smf.ols(formular,data=fm_regression).fit()

formular = 'returns_n ~ 1 + downside_risk_2 + status_dsr + vol + illiq_2_2 + credit_q + default_spread + returns_p +log_trade_value + res_day+ extreme + skew + coupon + total_size + coupon'
reg3 = smf.ols(formular,data=fm_regression).fit()


# ## 2. Fama-Macbeth Regression

#ols_coef: return the params
def ols_coef(x,formular):
    return smf.ols(formular,data=x).fit().params

#ols_tvalue：return t-values 
def ols_tvalue(x, formular):
    return smf.ols(formular, data=x).fit().tvalues

#fm_summary: input table p(the fm regression result ，that is, 
#the regressed parameters in each timestamp, return the statistics of each params 
def fm_summary(p):
    s = p.describe().T
    s['std_error'] = s['std'] / np.sqrt(s['count'])
    s['tstat'] = s['mean'] / s['std_error']
    return s[['mean', 'std_error', 'tstat']]


#return mean、std、t-value
s = pd.DataFrame(np.zeros((1, 3)))
s.columns = ['mean', 'std_error', 'tstat']

#multiple types of fm-rergession 
fm_regression = monthly_cb_value.copy() #we can change the dataset
s = pd.DataFrame(np.zeros((1, 3)))
s.columns = ['mean', 'std_error', 'tstat']
formular = 'returns_n ~ 1 + downside_risk_2'
downside_risk_reg1_fm1 = (fm_regression.groupby('datetime').apply(ols_coef, formular))
s = s.append(fm_summary(downside_risk_reg1_fm1))

formular = 'returns_n ~ 1 + downside_risk_2 + returns + log_trade_value + res_day + extreme_2 + skew + coupon'
downside_risk_reg1_fm2 = (fm_regression.groupby('datetime').apply(ols_coef, formular))
s = s.append(fm_summary(downside_risk_reg1_fm2))

formular = 'returns_n ~ 1 + status_dsr'
downside_risk_reg1_fm1 = (fm_regression.groupby('datetime').apply(ols_coef, formular))
s = s.append(fm_summary(downside_risk_reg1_fm1))

formular = 'returns_n ~ 1 + status_dsr + returns_p + log_trade_value + res_day + extreme + skew + coupon + total_size + coupon'
downside_risk_reg1_fm2 = (fm_regression.groupby('datetime').apply(ols_coef, formular))
s = s.append(fm_summary(downside_risk_reg1_fm2))

formular = 'returns_n ~ 1 + vol'
downside_risk_reg1_fm1 = (fm_regression.groupby('datetime').apply(ols_coef, formular))
s = s.append(fm_summary(downside_risk_reg1_fm1))

formular = 'returns_n ~ 1 + vol + returns_p + log_trade_value + res_day + extreme + skew + coupon + total_size + coupon'
downside_risk_reg1_fm2 = (fm_regression.groupby('datetime').apply(ols_coef, formular))
s = s.append(fm_summary(downside_risk_reg1_fm2))


formular = 'returns_n ~ 1 + illiq_2_2'
illiq2_risk_reg1_fm1 =(fm_regression.groupby('datetime').apply(ols_coef, formular))
s = s.append(fm_summary(illiq2_risk_reg1_fm1))

formular = 'returns_n ~ 1 + illiq_2_2 + returns_p + log_trade_value + res_day + extreme + skew + coupon + total_size + coupon'
illiq2_risk_reg1_fm2 =(fm_regression.groupby('datetime').apply(ols_coef, formular))
s = s.append(fm_summary(illiq2_risk_reg1_fm2))

formular = 'returns_n ~ 1 + credit_q'
credit_quality_reg1_fm1 = (fm_regression.groupby('datetime').apply(ols_coef, formular))
s = s.append(fm_summary(credit_quality_reg1_fm1))

formular = 'returns_n ~ 1 + credit_q + returns_p + log_trade_value + res_day + extreme + skew + coupon + total_size + coupon'
credit_quality_reg1_fm2 = (fm_regression.groupby('datetime').apply(ols_coef, formular))
s = s.append(fm_summary(credit_quality_reg1_fm2))


formular = 'returns_n ~ 1 + default_spread'
credit_quality_reg1_fm1 = (fm_regression.groupby('datetime').apply(ols_coef, formular))
s = s.append(fm_summary(credit_quality_reg1_fm1))

formular = 'returns_n ~ 1 + default_spread + returns_p  + log_trade_value + res_day + extreme + skew + coupon + total_size + coupon'
credit_quality_reg1_fm2 = (fm_regression.groupby('datetime').apply(ols_coef, formular))
s = s.append(fm_summary(credit_quality_reg1_fm2))

formular = 'returns_n ~ 1 + downside_risk_2 + status_dsr + vol + illiq_2_2  + returns_p + credit_q + default_spread + log_trade_value + res_day + vol + extreme + skew + coupon + total_size + coupon'
reg3_fm = (fm_regression.groupby('datetime').apply(ols_coef, formular))
s = s.append(fm_summary(reg3_fm))

# 's' is the final fama-macbeth result we get 
