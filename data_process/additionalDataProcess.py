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
monthly_cb_value = pd.read_csv(data_address + 'monthly_cb_value_fin_adjReturn.csv')
monthly_cb_value = pd.read_csv(data_address + 'data1.csv')
high_yield_bond = pd.read_csv(data_address + 'high_yield_bond.csv')
low_rate_bond = pd.read_csv(data_address + 'low_rate_bond.csv')


#计算return
monthly_cb_value['month_coupon'] = 1/100 * monthly_cb_value['coupon'] * monthly_cb_value['issue_price'] * (1 / 12)

monthly_cb_value_2 = monthly_cb_value.copy()
monthly_cb_value_2 = monthly_cb_value_2.iloc[:1]
monthly_cb_value_2['returns'] = 0
monthly_cb_value_2['returns_p'] = 0
monthly_cb_value_2['returns_n'] = 0


def get_illiq1(slice):
    global cb_trade_value
    cut = cb_trade_value[cb_trade_value['债券代码_BdCd'] == slice['cb_id']]
    cut = cut[cut['year'] == slice['trade_year']]
    cut = cut[cut['month'] == slice['trade_month']]
    cb_trade_value = cb_trade_value[(cb_trade_value['债券代码_BdCd'] != slice['cb_id']) | (cb_trade_value['year'] != slice['trade_year']) | (cb_trade_value['month'] != slice['trade_month'])]
    cut['key_3'] = cut['交易日期_TrdDt']
    cut = cut.groupby('key_3').last()
    cut = cut.sort_values('交易日期_TrdDt')
    cut['returns'] = cut['全价昨收盘(元)_PreClDirPr'] / cut['全价昨收盘(元)_PreClDirPr'].shift(1) - 1

    slice['downside_risk_2'] = cut['returns'].min()
    slice['illiq_1_2'] = len(cut)
    p = np.log(cut['全价昨收盘(元)_PreClDirPr'])
    delta_p = p - p.shift(1)
    slice['illiq_2_2'] = - delta_p.corr(delta_p.shift(1))
    global monthly_cb_value
    monthly_cb_value = monthly_cb_value.append(slice)


xx=monthly_cb_value.drop_duplicates(subset=['cb_id'],keep='first')
# xx
from scipy.stats import norm


data0=pd.DataFrame([])
i=0
for sym in xx['cb_id']:
    print(i)
    i+=1
    data=monthly_cb_value[monthly_cb_value['cb_id']==sym]
    data=data.sort_values(by=['trade_year','trade_month'])
    data['reNew']=data['close']/data['close'].shift(1)-1
    value= norm.ppf(0.05)
    data['mu']=data['returns'].rolling(window=12,center=False).mean()
    data['sigma']=data['returns'].rolling(window=12,center=False).std()
    data['mu1']=data['returns'].rolling(window=36,center=False).mean()
    data['sigma1']=data['returns'].rolling(window=36,center=False).std()
    data['var1']=data['returns'].rolling(window=12,center=False).min()
    data['var2']=value*data['sigma']+data['mu']
    data['var3']=data['returns'].rolling(window=36,center=False).min()
    data['var4']=value*data['sigma1']+data['mu1']
# data
    data0=data0.append(data)


for sym in xx['cb_id']:
    print(i)
    i+=1
    data=monthly_cb_value[monthly_cb_value['cb_id']==sym]
    data=data.sort_values(by=['trade_year','trade_month'])
    data['reNew']=data['close']/data['close'].shift(1)-1
    data['deltaPrice'] = data['close'] - data['close'].shift(1)
    data['illiqBao'] = data['deltaPrice'].
    value= norm.ppf(0.05)
    data['mu']=data['returns'].rolling(window=12,center=False).mean()
    data['sigma']=data['returns'].rolling(window=12,center=False).std()
    data['mu1']=data['returns'].rolling(window=36,center=False).mean()
    data['sigma1']=data['returns'].rolling(window=36,center=False).std()
    data['var1']=data['returns'].rolling(window=12,center=False).min()
    data['var2']=value*data['sigma']+data['mu']
    data['var3']=data['returns'].rolling(window=36,center=False).min()
    data['var4']=value*data['sigma1']+data['mu1']
# data
    data0=data0.append(data)

# 20%的sigma为0


def cal_illiqBao(slice_data):
    '''
    this function is a supporting function for calculating illiquidity factor in Bao's method
    function: illiq_t = corr(delta(price_t), delta(price_t-1), n=36)

    :param slice_data: input the data['deltaPrice'] from the whole data(used in rolling apply)
    :return: the calculated illiquidity factor
    '''
    slice_data = pd.DataFrame(slice_data)
    slice_data.columns = ['factor']
    return slice_data['factor'].corr(slice_data['factor'].shift(1))

data1=pd.DataFrame([])
i = 0
for sym in xx['cb_id']:
    print(i)
    i+=1
    data=monthly_cb_value[monthly_cb_value['cb_id']==sym]
    data=data.sort_values(by=['trade_year','trade_month'])
    data['deltaPrice'] = data['close'] - data['close'].shift(1)
    corr = pd.rolling_apply(data['deltaPrice'], 36, cal_illiqBao)
    corr = pd.DataFrame(corr)
    corr.columns = ['corr']
    data['corr'] = corr['corr']
# data
    data1=data1.append(data)

xx = fm_regression.drop_duplicates(subset=['cb_id'], keep='first')


def var(x):
    x1 = x[x < 0]
    return x1.mean()


def auto(x1):
    return np.corrcoef(x1[1:], x1[:-1])[0, 1]


data0 = pd.DataFrame([])
i = 0
for sym in xx['cb_id']:
    print(i)
    i += 1
    data = fm_regression[fm_regression['cb_id'] == sym]
    data = data.sort_values(by=['trade_year', 'trade_month'])
    data['reNew'] = data['close'] / data['close'].shift(1) - 1
    value = norm.ppf(0.05)
    data['mu'] = data['returns'].rolling(window=12, center=False).mean()
    data['sigma'] = data['returns'].rolling(window=12, center=False).std()
    data['mu1'] = data['returns'].rolling(window=24, center=False).mean()
    data['sigma1'] = data['returns'].rolling(window=24, center=False).std()
    data['mu2'] = data['returns'].rolling(window=36, center=False).mean()
    data['sigma2'] = data['returns'].rolling(window=36, center=False).std()
    data['var1'] = data['returns'].rolling(window=12, center=False).min()

    data['var2'] = value * data['sigma'] + data['mu']
    data['var3'] = data['returns'].rolling(window=24, center=False).min()
    data['var4'] = value * data['sigma1'] + data['mu1']
    data['var5'] = data['returns'].rolling(window=36, center=False).min()
    data['var6'] = value * data['sigma2'] + data['mu2']
    data['var7'] = data['returns'].rolling(window=12, center=False).apply(var)
    data['var8'] = data['returns'].rolling(window=24, center=False).apply(var)
    data['var9'] = data['returns'].rolling(window=36, center=False).apply(var)
    data['tradeSum'] = data['log_trade_value'] / data['total_size']
    data['amihud'] = data['tradeSum'].rolling(window=36, center=False).mean()
    data['auto'] = -data['returns'].rolling(window=36, center=False).apply(auto)

    # data
    data0 = data0.append(data)

def var(x):
    x1=x[x<0]
    return x1.mean()


def auto(x1):
    return np.corrcoef(x1[1:], x1[:-1])[0, 1]


data0 = pd.DataFrame([])

marketExcessReturn = monthly_cb_value.groupby('datetime')['return']
'''
calculate the monthly factors for bond-market 5 factors
1. excess bond market returns
2. default factor
3. term factor
4. bond momentum factor
5. bond illiquidity factor
'''
