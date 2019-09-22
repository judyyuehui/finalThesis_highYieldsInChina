import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
from matplotlib.mlab import PCA

#PCA 分析

data_address = '../data/中间数据/'
monthly_cb_value = pd.read_csv(data_address + 'monthly_cb_value_fin.csv')

factor_list = [ 'downside_risk_2', 'status_dsr', 'illiq_2_2', 'returns_p', 'creditRate', 'default_spread',
                'log_trade_value', 'res_day', 'vol', 'extreme_2', 'skew',  'total_size', 'coupon']

data = monthly_cb_value[factor_list]


data = data.fillna(0)

'''
PCA 方法1： 直接用sklearn的包
优势：用SVD降维，更加标准
劣势：由于不知道实际的correlation matrix，不知道该怎么选择component，以及每个component对应的projection 
'''
from sklearn.decomposition import PCA
X = np.array([[-1, 1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
pca=PCA(n_components=5)
pca.fit(data)
pca.transform(data)

'''
得到的结果：只有第一个component有意义
pca.explained_variance_ratio_
Out[21]: array([0.94569423, 0.04154984, 0.00570173, 0.00359057, 0.00259915])
'''


'''
PCA 方法2：根据定义自己来进行的PCA
优势：每一步都清楚是怎么做的
劣势：没有采用SVD，只是用correlation matrix来计算
'''
#scale the data(standardize from 0-1)
from sklearn.preprocessing import StandardScaler
factor_std = StandardScaler().fit_transform(data)

#caculating the covariance matrix
mean_vec = np.mean(factor_std, axis = 0)
cov_mat = (factor_std - mean_vec).T.dot((factor_std - mean_vec) / factor_std.shape[0] - 1)
#cov_mat = np.cov(X_std.T)
eig_vals, eig_vecs =  np.linalg.eig(cov_mat)

for ev in eig_vecs:
    np.testing.assert_array_almost_equal(1.0, np.linalg.norm(ev))
print('Everything ok!')

# Make a list of (eigenvalue, eigenvector) tuples
eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:,i]) for i in range(len(eig_vals))]

# Sort the (eigenvalue, eigenvector) tuples from high to low
eig_pairs.sort()
eig_pairs.reverse()

# Visually confirm that the list is correctly sorted by decreasing eigenvalues
print('Eigenvalues in descending order:')
for i in eig_pairs:
    print(i[0])

'''
2.273064675169854
1.9058572912632648
1.4149329289194608
1.177226739933212
1.0481516169657854
0.9858195662704755
0.9440439980437426
0.6766691902381288
0.5863283996766472
0.5704834417821217
0.33090886145980125
0.08651329032306783
0.0
'''

import plotly as py
tot = sum(eig_vals)
var_exp = [(i / tot)*100 for i in sorted(eig_vals, reverse=True)]
cum_var_exp = np.cumsum(var_exp)

trace1 = dict(
    type='bar',
    x=['PC %s' %i for i in range(1,5)],
    y=var_exp,
    name='Individual'
)

trace2 = dict(
    type='scatter',
    x=['PC %s' %i for i in range(1,5)],
    y=cum_var_exp,
    name='Cumulative'
)

data = [trace1, trace2]

layout=dict(
    title='Explained variance by different principal components',
    yaxis=dict(
        title='Explained variance in percent'
    ),
    annotations=list([
        dict(
            x=1.16,
            y=1.05,
            xref='paper',
            yref='paper',
            text='Explained Variance',
            showarrow=False,
        )
    ])
)

fig = dict(data=data, layout=layout)
py.plot(fig)


#得到前四个的因子的projection结果
matrix_w = np.hstack((eig_pairs[0][1].reshape(13,1),
                      eig_pairs[1][1].reshape(13,1),
                      eig_pairs[2][1].reshape(13, 1),
                      eig_pairs[3][1].reshape(13, 1)))
matrix_w.index = factor_list

'''
                        0         1         2         3
downside_risk_2 -0.478293 -0.137210  0.384094  0.069760
status_dsr      -0.061976 -0.062509  0.211771  0.309597
illiq_2_2        0.249994  0.119395  0.377741 -0.505791
returns_p       -0.004464 -0.017830 -0.031858  0.013654
creditRate      -0.170669  0.571809  0.004226 -0.081692
default_spread   0.000000  0.000000  0.000000  0.000000
log_trade_value  0.264545  0.140962  0.461324 -0.405704
res_day         -0.094191  0.352349  0.074525  0.006355
vol              0.571814  0.211424 -0.148477  0.278604
extreme_2        0.392163  0.187835  0.263154  0.480004
skew            -0.131668 -0.005062  0.573085  0.383481
total_size      -0.184993  0.339718 -0.142804  0.129923
coupon           0.254110 -0.544327  0.073591  0.000077

输出到pca_projection文件中
'''

