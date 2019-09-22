# -*- coding: utf-8 -*-
# translate the existing data to the monthly data, calculate all the factors(&supporting factors) and get the usable data

import numpy as np
import pandas as pd
from scipy.optimize import fsolve


'''
一、读取数据：
1. cb_trade_value: 锐思数据库中对应的上交所债券日交易数据（数据量较大）
2. cb_info: 债券对应发债信息和公司信息等（含有债券评级等属性）
3. AAminus_yields: 每日AA-等级债券对应的收益率

'''
#price info(cb_trade_value)
data_address = "~/Desktop/毕业设计/resset_value/resset_value_2/BDEXCHFIBDQUOT_3.xls" #这里应该对应的是data文件夹里原始数据的地址， 即../data/原始数据/BDEXCHFIBDQUOT_3.xls
cb_trade_value = pd.read_excel(data_address, encoding = 'utf-8')
for i in range(4, 80):
    data_address = "~/Desktop/毕业设计/resset_value/resset_value_2/BDEXCHFIBDQUOT_" + str(i) + ".xls"
    cb_trade_value = cb_trade_value.append(pd.read_excel(data_address, encoding = 'utf-8'))

#bond info(cb_info)
data_address = "~/Desktop/毕业设计/resset_value/BDINFO_1.xls" #这里对应的也是原始数据的地址（文件夹相同，文件名是BDINFO_1.xls）
cb_info = pd.read_excel(data_address, encoding = 'utf-8')
data_address = "~/Desktop/毕业设计/resset_value/BDINFO_2.xls"
cb_info = cb_info.append(pd.read_excel(data_address, encoding = 'utf-8'))
data_address = "~/Desktop/毕业设计/resset_value/BDINFO_3.xls"
cb_info = cb_info.append(pd.read_excel(data_address, encoding = 'utf-8'))

#AAminus_yields
data_address = "~/Desktop/毕业设计/cop_yield/cop_bond_yields_AAminus.xls"
AAminus_yields = pd.read_excel(data_address, encoding='utf-8')
AAminus_yields = AAminus_yields[1:-2]
AAminus_yields.index = pd.to_datetime(AAminus_yields['指标名称'])
AAminus_yields.columns = ['date', 0.0, 0.083, 0.25, 0.5, 0.75, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 15.0, 20.0, 30.0]
AAminus_yields = AAminus_yields[AAminus_yields.date.dt.year >= 2014]


'''
二、数据整合
为了方便后面的筛选，将cb_info中有用的信息附加到cb_trade_value上
删除某些类型的债券
'''

#通过cb_trade_value生成债券代码列表，对该列表进行循环给cb_trade_value增加信息
bondlist = pd.DataFrame(cb_trade_value['债券标识_BdId'].value_counts().index)
bondlist.columns = ['bondid']

#定义get_feature函数，输入bondid和cb_info，输出我们想要的对应债券代码的信息列表
def get_feature(slice, bondid):
    print(slice.iloc[0]['债券标识_BdId'])
    k = cb_info[cb_info['债券标识_BdId'] == bondid]
    if len(k) != 0:
        slice['债券类型()_BdType'] = k.iloc[0]['债券类型()_BdType']
        slice['市场标识_Mktflg'] = k.iloc[0]['市场标识_Mktflg']
        slice['发行总额(亿元)_IssSize'] = k.iloc[0]['发行总额(亿元)_IssSize']
        slice['信用级别_CredRat'] = k.iloc[0]['信用级别_CredRat']
        slice['上市日期_LstDt'] = k.iloc[0]['上市日期_LstDt']
    else:
        slice['债券类型()_BdType'] = -2
        slice['市场标识_Mktflg'] = -2
        slice['发行总额(亿元)_IssSize'] = -2
        slice['信用级别_CredRat'] = -2
        slice['上市日期_LstDt'] = -2
    return slice

cb_trade_value['债券标识_BdId'] = cb_trade_value['债券标识_BdId'].apply(lambda x: int(x))
bondlist['bondid'] = bondlist['bondid'].apply(lambda x: int(x))
slice = cb_trade_value[cb_trade_value['债券标识_BdId'] == bondlist.iloc[0]['bondid']]
cb_trade_value_2 = get_feature(slice, bondlist.iloc[0]['bondid'])

count = 0
cb_trade_value_3 = cb_trade_value_2[-1:]
for bondid in bondlist.iloc['bondid']:
    count = count + 1
    slice = cb_trade_value[cb_trade_value['债券标识_BdId'] == bondid]
    cb_trade_value_3 = cb_trade_value_3.append(get_feature(slice, bondid))
    cb_trade_value = cb_trade_value[cb_trade_value['债券标识_BdId'] != bondid ]
    if count % 200 == 0:
        cb_trade_value_3.to_csv("~/Desktop/毕业设计/data_in_process_2/cb_trade_value_2_" + str(count) + ".csv")
        cb_trade_value_3 = cb_trade_value_3[-1:]

# 删除国债、浮动利率等数据
cb_trade_value_2['债券类型()_BdType'] = cb_trade_value_2['债券类型()_BdType'].apply(lambda x: int(x))
cb_trade_value_2 = cb_trade_value_2[cb_trade_value_2['债券类型()_BdType']!=-2]
cb_trade_value_2 = cb_trade_value_2[cb_trade_value_2['债券类型()_BdType'] != 4]
cb_trade_value_2 = cb_trade_value_2[cb_trade_value_2['债券类型()_BdType'] != 5]
cb_trade_value_2 = cb_trade_value_2[cb_trade_value_2['债券类型()_BdType'] != 10]
cb_trade_value_2 = cb_trade_value_2[cb_trade_value_2['债券类型()_BdType'] != 11]
cb_trade_value_2 = cb_trade_value_2[cb_trade_value_2['债券类型()_BdType'] != 15]
cb_trade_value_2 = cb_trade_value_2[cb_trade_value_2['债券类型()_BdType'] != 36]

#数据暂存
data_address = "~/Desktop/毕业设计/data_in_process_2/cb_trade_value_3.csv"
cb_trade_value = pd.read_csv(data_address)


'''
三、债券月度数据计算
由于之前数据是日度数据，我们想要得到的是月度的特征值，因此将日度数据整合处理成月度数据。
主要操作： 
计算月度价格（High、Low、Open、Close）
合并债券信息（评级，cb_info等）
'''
#数据基本处理（数据类型转化成float）
cb_trade_value['交易日期_TrdDt'] = pd.to_datetime(cb_trade_value['交易日期_TrdDt'])
list = ['发行价格(元)_IssPr', '票面利率_CoupRt','应计利息(元)_AccInt','剩余年份_YrsTMat', '加权平均收益率(%)_YTMWghAvg',
       '净价昨收盘(元)_PreClNetPr', '净价开盘价(元)_OpNetPr', '净价最高价(元)_HiNetPr',
       '净价最低价(元)_LoNetPr', '净价收盘价(元)_ClNetPr', '净价均价(元)_AvgNetPr',
       '净价加权价(元)_WghNetPr', '净价涨跌幅(%)_ChgPCT', '净价振幅(%)_NetPrVibRag',
       '全价昨收盘(元)_PreClDirPr', '全价开盘价(元)_OpDirPr', '全价最高价(元)_HiDirPr',
       '全价最低价(元)_LoDirPr', '全价收盘价(元)_ClDirPr', '全价均价(元)_AvgDirPr',
       '全价加权价(元)_WghDirPr', '全价涨跌幅(%)_DirChgPCT', '全价振幅(%)_DirPrVibRag',
       '换手率(%)_TurRat', '成交量(张)_TrdVol', '成交金额(元)_TrdSum', '成交笔数(笔)_TrdDeals',
       '开盘价到期收益率(%)_YTMOp', '开盘价麦氏久期_DurOp', '开盘价修正久期_ModDurOp',
       '开盘价凸度_ConvOp', '最高价到期收益率(%)_YTMHi', '最高价麦氏久期_DurHi',
       '最高价修正久期_ModDurHi', '最高价凸度_ConvHi', '最低价到期收益率(%)_YTMLo',
       '最低价麦氏久期_DurLo', '最低价修正久期_ModDurLo', '最低价凸度_ConvLo',
       '收盘价到期收益率(%)_YTMCl', '收盘价麦氏久期_DurCl', '收盘价修正久期_ModDurCl',
       '收盘价凸度_ConvCl', '均价到期收益率(%)_YTMAvg', '均价麦氏久期_DurAvg',
       '均价修正久期_ModDurAvg', '均价凸度_ConvAvg', '利息回报(元)_RetInt', '价格回报(元)_RetPr',
       '总回报(元)_TotRet']

for f in list:
    print(f)
    cb_trade_value[f] = cb_trade_value[f].apply(lambda x: float(x))

#生成债券列表
cb_list = pd.DataFrame(cb_trade_value['债券代码_BdCd'].value_counts().index)
cb_list.columns = ['cb_id']
cut = cb_trade_value[cb_trade_value['债券代码_BdCd'] == cb_list.iloc[0]['cb_id']]

#由于债券剩余期限是小数形式，但是我们想要对应到低等级债券收益率曲线上，因此定义函数找到距离剩余期限最近期限
def nearest_maturity(maturity):
    '''
    supporting function to generate monthly info from daily info
    :param maturity:
    :return:
    '''
    #可改进的地方：每天生成收益率曲线，直接进行取值
    choice = pd.DataFrame([0.0, 0.083, 0.25, 0.5, 0.75, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 15.0, 20.0, 30.0])
    diff = abs(choice - maturity)
    diff.columns = ['0']
    choice.columns = ['0']
    return choice.iloc[diff['0'].argmin()][0]

month_columns = ['cb_id', 'trade_year', 'trade_month', 'bond_type', 'compcode', 'comcd', 'issue_price','matdate',
                 'high','low','open','close',
                 'downside_risk', 'illiq_1', 'illiq_2', 'credit_q', 'AA_minus','default_spread',
                 'trade_value', 'trade_num', 'res_day', 'coupon', 'on_market_date', 'total_size'
                 'vol', 'skew', 'kurt']
monthly_value_sheet = pd.DataFrame(np.zeros((1, len(month_columns))))
monthly_value_sheet.columns = month_columns

# 计算月度数据.
# 该函数输入日度数据:一个债券代码对应的slice，这样可以计算该债券在每个月的return
# 生成月度数据monthly_sheet
monthly_value_sheet = pd.DataFrame(np.zeros((1, len(month_columns))))
monthly_value_sheet.columns = month_columns
def daily_to_month(bond_sheet):
    '''
    :param bond_sheet: input the total daily data of the bonds
    :return: the monthly data of bonds with desired variables
    '''
    print(bond_sheet.iloc[0]['债券代码_BdCd'], bond_sheet.iloc[0]['交易日期_TrdDt'])
    bond_sheet = bond_sheet.sort_values('交易日期_TrdDt')
    bond_sheet['returns'] = bond_sheet['全价昨收盘(元)_PreClDirPr'] / bond_sheet['全价昨收盘(元)_PreClDirPr'].shift(1) - 1
    monthly_sheet = pd.DataFrame(np.zeros((1, len(month_columns))))
    monthly_sheet.columns = month_columns
    #债券代码
    monthly_sheet['cb_id'] = bond_sheet.iloc[0]['债券代码_BdCd']
    #债券交易的年份
    monthly_sheet['trade_year'] = bond_sheet.iloc[0]['交易日期_TrdDt'].year
    #债券交易的月份（这里将年和月分开，在之后以月份为精度进行数据筛选时使用比较方便）
    monthly_sheet['trade_month'] = bond_sheet.iloc[0]['交易日期_TrdDt'].month
    #债券类型
    monthly_sheet['bond_type'] = bond_sheet.iloc[0]['债券类型()_BdType']
    #公司代码
    monthly_sheet['compcode'] = bond_sheet.iloc[0]['公司代码_CompanyCode']
    #上市公司代码
    monthly_sheet['comcd'] = bond_sheet.iloc[0]['上市公司代码_ComCd']
    #发行价格（都是100）
    monthly_sheet['issue_price'] = bond_sheet.iloc[0]['发行价格(元)_IssPr']
    #全部的到期年份
    monthly_sheet['matdate'] = bond_sheet.iloc[0]['到期期限(年)_Maturity']
    #月度价格最高值
    monthly_sheet['high'] = bond_sheet['全价昨收盘(元)_PreClDirPr'].max()
    #价格最低值
    monthly_sheet['low'] = bond_sheet['全价昨收盘(元)_PreClDirPr'].min()
    #月度开盘价
    monthly_sheet['open'] = bond_sheet.iloc[0]['全价昨收盘(元)_PreClDirPr']
    #月度收盘价
    monthly_sheet['close'] = bond_sheet.iloc[-1]['全价昨收盘(元)_PreClDirPr']

    #downside_risk: 该月最低的日度回报率
    monthly_sheet['downside_risk'] = bond_sheet['returns'].min()
    #illiq_1: 该月记录的长度
    monthly_sheet['illiq_1'] = len(bond_sheet)
    #illiq 2: 该月每日价格和之前一日价格的相关系数（这个值其实没有意义，之后也没有采用这个数值，但是数据忘记删了）
    p = np.log(bond_sheet['全价昨收盘(元)_PreClDirPr'])
    delta_p = p - p.shift(1)
    monthly_sheet['illiq_2'] = - delta_p.corr(delta_p.shift(1))
    monthly_sheet['credit_q'] = bond_sheet['信用级别_CredRat']
    #计算defualt spread:即债券当时的到期收益率减去对应AA-公司债的平均债券收益率
    m = nearest_maturity(bond_sheet.iloc[-1]['剩余年份_YrsTMat'])
    k = AAminus_yields[AAminus_yields['date'] == bond_sheet.iloc[-1]['交易日期_TrdDt']]
    if(len(k) == 0):
        r = -10
    else:
        r = k[m].iloc[0]
    monthly_sheet['AA_minus'] = r
      #AAminus数据中有些到期收益率数值是Nan，我们把这些数值标记成-10，之后进行处理

    #成交价格
    monthly_sheet['trade_value'] = bond_sheet['成交金额(元)_TrdSum'].sum()
    #成交笔数
    monthly_sheet['trade_num'] = bond_sheet['成交笔数(笔)_TrdDeals'].sum()
    #剩余年份
    monthly_sheet['res_day'] = bond_sheet.iloc[-1]['剩余年份_YrsTMat']
    #票面利率
    monthly_sheet['coupon'] = bond_sheet.iloc[0]['票面利率_CoupRt']
    #上市日期
    monthly_sheet['on_market_date'] = bond_sheet.iloc[0]['上市日期_LstDt']
    #总发行额
    monthly_sheet['total_size'] = bond_sheet.iloc[0]['发行总额(亿元)_IssSize']
    #日度收益率的方差
    monthly_sheet['vol'] = bond_sheet['returns'].std()
    #日度收益率的偏度
    monthly_sheet['skew'] = bond_sheet['returns'].skew()
    #日度收益率的峰值
    monthly_sheet['kurt'] = bond_sheet['returns'].kurt()
    global monthly_value_sheet
    monthly_value_sheet = monthly_value_sheet.append(monthly_sheet)

#对cb_trade_value进行操作,计算得到月度数据
for id in cb_list['cb_id'][:1]:
    print(id)
    cut = cb_trade_value[cb_trade_value['债券代码_BdCd'] == id]
    list = pd.DataFrame(cut['key2'].value_counts().index)
    list.columns = ['month']
    for m in list['month'][:1]:
        print(m)
        cut_2 = cut[cut['key2'] == m]
        daily_to_month(cut_2)

#由于计算月度数据时间较长，保险起见我们将monthly_value_sheet拷贝一下进行操作
monthly_cb_value = monthly_value_sheet.copy()

'''
四、特征值计算及统计
1. 计算return并
2. 把之前的credit rate转化成数值形式
3. 计算Yields & Default Spread
4. 重新计算illiquidity 
'''
#return：
monthly_cb_value = monthly_value_sheet.copy()
monthly_cb_value['key_1'] = monthly_cb_value['cb_id']
monthly_cb_value_2 = monthly_cb_value.copy()
monthly_cb_value_2 = monthly_cb_value_2.iloc[:1]
monthly_cb_value_2['returns'] = 0
monthly_cb_value_2['returns_p'] = 0
monthly_cb_value_2['returns_n'] = 0
def get_return(bond_sheet):
    bond_sheet['datetime'] = bond_sheet['trade_year'].apply(lambda x: str(x)[:-2]) + '-' + bond_sheet['trade_month'].apply(lambda x: str(x)[:-2])
    bond_sheet['datetime'] = bond_sheet['datetime'].apply(lambda x: pd.to_datetime(x))
    bond_sheet = bond_sheet.sort_values('datetime')
    bond_sheet['returns'] = bond_sheet['close'] / bond_sheet['close'].shift(1) - 1
    bond_sheet['returns_p'] = bond_sheet['returns'].shift(1)
    bond_sheet['returns_n'] = bond_sheet['returns'].shift(-1)
    global monthly_cb_value_2
    monthly_cb_value_2 = monthly_cb_value_2.append(bond_sheet)


#credit rate:
#（credit rate的类型比较复杂，这里直接将所有数据分类来进行计算）
def transfer_credit(creditrate):
    if creditrate == 'AAA' or creditrate == 'AAA,AAA' or creditrate == 'AAA,AAApi' or creditrate == 'AA+,AAA' or creditrate == 'A-1':
        credit_q = 6
    elif creditrate == 'AA+' or creditrate == 'AA+,AA+' or creditrate == 'AA+,AA+pi' or creditrate == 'AA+pi,AA+ ' or creditrate == 'AAA,AA+':
        credit_q = 5
    elif creditrate == 'AA' or creditrate == 'AA,AA' or creditrate == 'AA,AApi' or creditrate == 'AApi,AA' or creditrate == 'AA+,AA ':
        credit_q = 4
    elif creditrate == 'AA-' or creditrate == 'AA-,AA':
        credit_q = 3
    elif creditrate == 'A+':
        credit_q = 2
    elif creditrate == 'A':
        credit_q = 1
    else:
        credit_q = 0
    return credit_q


#yields&default spread:
def findyield(price, par, coupon, maturity, l, r, precision=.00005):
    '''
    calculate the yields base on the bonds' basic info
    :param price: price of bonds(close)
    :param par: face value of bonds
    :param coupon: coupon rate of bonds
    :param maturity: residual maturity of bonds
    :param l: higher bonds
    :param r: lower bonds
    :param precision:
    :return:
    '''
    rate = (l + r)/2
    estimate = coupon * ((1 - (1/((1 + rate)**maturity)))/rate) + par/((1 + rate)**maturity)

    if(estimate - precision < price < estimate + precision):
        return rate
    if(estimate < price):
        return findyield(price, par, coupon, maturity, l, rate)
    else:
        return findyield(price, par, coupon, maturity, rate, r)


def get_yield(slice):
    print(slice['cb_id'], slice['trade_year'], slice['trade_month'])
    price = slice['close']
    par = slice['issue_price']
    coupon = slice['coupon'] * slice['issue_price'] / 100
    maturity = slice['res_day']
    try:
        a = findyield(price, par, coupon, maturity, 0, 1) * 100
    except:
        a = 0
    return a
monthly_cb_value['yields'] = monthly_cb_value.apply(get_yield)
monthly_cb_value['default_spread'] = monthly_cb_value['yields'] - monthly_cb_value['AA_minus_2']


#illiquidity:
#illiq1数据可用性很低，因此我们采取了另一种计算illiquidity的方法（记做illiq_2_2 也是论文最后采用的illiquidity计算方法）
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
xx=monthly_cb_value.drop_duplicates(subset=['cb_id'],keep='first')
for sym in xx['cb_id']:
    print(i)
    i+=1
    data=monthly_cb_value[monthly_cb_value['cb_id']==sym]
    data=data.sort_values(by=['trade_year','trade_month'])
    data['deltaPrice'] = data['close'] - data['close'].shift(1)
    data = pd.rolling_apply(data['deltaPrice'], 36, cal_illiqBao)
    data1=data1.append(data)
monthly_cb_value = data1.copy()

#extreme:
#补充计算一个极值因子，即日度收益率的最高值
def cal_datatime(slice):
    a = pd.to_datetime(str(slice['trade_year'])[:-2] + '-'+str(slice['trade_month'])[:-2])
    return a
def get_extreme(slice):
    cut = cb_trade_value[cb_trade_value['债券代码_BdCd'] == slice['cb_id']]
    cut = cut[cut['year'] == slice['trade_year']]
    cut = cut[cut['month'] == slice['trade_month']]
    cut['key_3'] = cut['交易日期_TrdDt']
    cut = cut.groupby('key_3').last()
    cut = cut.sort_values('交易日期_TrdDt')
    cut['returns'] = cut['全价昨收盘(元)_PreClDirPr'] / cut['全价昨收盘(元)_PreClDirPr'].shift(1) - 1
    slice['extreme_2'] = cut['returns'].max()
    global monthly_cb_value_p
    monthly_cb_value_p = monthly_cb_value_p.append(slice)
monthly_cb_value = monthly_cb_value_p.copy()


'''
五、债券数据分类：
低等级债券：债券评级低于AA
高收益债券：债券到期收益率高于8或者到期收益率高于同期AA-等级债券平均到期收益率
'''
low_rate_bond = monthly_cb_value[monthly_cb_value['creditRate'] <= 4]
high_yield_bond = monthly_cb_value[(monthly_cb_value['yields'] >= 8) | (monthly_cb_value['default_spread'] > 0)]

data_address = '~/Downloads/data/a/'
monthly_cb_value.to_csv(data_address + 'monthly_cb_value_fin.csv')
low_rate_bond.to_csv(data_address + 'low_rate_bond.csv')
high_yield_bond.to_csv(data_address + 'high_yield_bond.csv')

'''
summary for the final data: 
1. 重点的四个因子:
downside_risk_3: 下跌风险(已经乘以负号，即数值越大风险越大)
illiq_2_2: 流动性风险，计算方法和解释见论文中的因子说明部分
credit_q: 债券评级的数值
default spread: 债券到期收益率减去对应的AA-公司债曲线到期收益率得到的值
2. 下一个月的return由returns_n代表
'''
