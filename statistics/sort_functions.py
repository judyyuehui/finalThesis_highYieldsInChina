import pandas as pd
import numpy as np


def return_decile(feature, cut, columns_decile, decile_num):
    '''
    supporting function for univariate sorting (only for data with same 'datetime')
    :param feature: independent variable(the criteria to sort data)
    :param cut: the data(with same datetime)
    :param columns_decile: dependent variable
    :param decile_num: the number of deciles we want
    :return: the decile portfolio we constructed with means of each dependent variable
            return a DataFrame, columns = columns_decile, index = list[decile_num]
    '''
    decile_zero = pd.DataFrame(np.zeros((decile_num, len(columns_decile + ['decile']))))
    decile_zero.columns = columns_decile + ['decile']
    try:
        cut['decile'] = pd.qcut(cut[feature], decile_num, labels=False)
    except ValueError:
        return decile_zero

    cut['decile'] = cut['decile'].apply(lambda x: float(x))

    for name in cut.columns:
        cut[name] = cut[name].apply(lambda x: float(x))
    a = cut.groupby(cut['decile']).mean()
    if len(a) != decile_num:
        #print(a)
        return decile_zero
    else:
        a = a.fillna(0)
        return a

#return_decile_2：对于一个表格（sheet），分割每一天的数据，对每一天的数据进行排序，将所有每一天的decile数据加和进行平均
def return_decile_2(feature, sheet, columns_decile, decile_num = 5):
    '''
    the operating function to conduct univariate sorting
    :param feature: independent variable
    :param sheet: the total data we have(no restriction of datetime)
    :param columns_decile: dependent variable
    :param decile_num: decile number we want
    :return: the sorted portfolio with the means of each dependent variable
    '''
    decile_t = pd.DataFrame(np.zeros((decile_num, len(columns_decile) + 1)))
    decile_t.columns = columns_decile + ['decile']

    decile_t.index = [x for x in range(decile_num)]
    j = 0
    datelist = pd.DataFrame(sheet['datetime'].value_counts().index)
    datelist.columns = ['date']
    for date in datelist['date']:
        slice = sheet[sheet['datetime'] == date]
        slice = slice[columns_decile]
        a = return_decile(feature, slice, columns_decile, decile_num)
        #print('a')
        #print(a)
        decile_t = decile_t + a
        #print(decile_t)

    j = decile_t['decile'].iloc[4] / 4
    decile_t = decile_t / j
    return decile_t


if __name__ == "__main__":
    data_address = '~/Downloads/data/a/'
    monthly_cb_value = pd.read_csv(data_address + 'monthly_cb_value_fin_adjReturn.csv')
    factors = ['returns', 'returns_n', 'downside_risk_3', 'status_dsr', 'vol', 'skew', 'illiq_2_2', 'default_spread',
                  'creditRate', 'res_day']

    univSort_downside = return_decile_2('downside_risk_3', monthly_cb_value[monthly_cb_value['downside_risk_3'] != 0], factors)
