import os, sys, pathlib
import argparse
from collections import OrderedDict
from copy import deepcopy
from typing import Union

import datetime
# from dateutil.parser import parse as dateparse
import time, math

import numpy as np
import pandas as pd
from pandas.tseries.offsets import *

import colorlover as cl

# import matplotlib
# matplotlib.use("Agg")
# import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set(style="ticks", color_codes=True)

import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.sandbox.regression.predstd import wls_prediction_std
import statsmodels.graphics.api as smg
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.stattools import adfuller

from sklearn import linear_model

from scipy.linalg import toeplitz

from flask_login import current_user

#from apps.settings.constants import EXTRA_OUT_DIR, REGRESSION_FEATURES_OUT_FILESUFFIX, \
#    MATPLOTLIB_OUT_DIR, MATPLOTLIB_OUT_FILESUFFIX, MATPLOTLIB_OUT_FILEFORMAT


# ==============================================================================

"""
Linear regression - return:
param = **{'bl_matplotlib':True}
regr_stats, regr_line, scatter_data = go_regression(Y, X, **param)
stats, series_regression = go_regression(lst_series_namestr, lst_series_fd[0], lst_series_fd[1:], **{'bl_matplotlib': True})
"""
def go_regression(lst_header, Y, X, **param):
    if param:
        regr_stats, series_regression = regr(Y, X, **param)
    else:
        regr_stats, series_regression = regr(Y, X)

    #summary_lst = str(regr_stats.summary()).split('\n')
    summary_adj = str(regr_stats.summary()).split('Omnibus')[0]

    ccm_title = 'Cross Corrlelation: Y'
    for i in range(len(X)):
      ccm_title += '   X' + str(i+1)
    ccm_title += '\n'
    ccm_title += '-'*len(ccm_title) + '\n'
    summary_adj += ccm_title + calc_corrcoeffmatrix(Y, X)

    bl_save_regression_feature = param.get('bl_save_regression_feature', None)
    if bl_save_regression_feature != False:
      save_regression_feature(lst_header, Y, X)
    return (summary_adj, series_regression)


"""
Linear regression
- statsmodels
- sklearn
"""
def regr(Y, X, **param):
    """
    param = {'lib':'sm or sklearn', }
    """
    if not param:
        return regr_ols_sm(Y, X)
    elif 'lib' not in param:
        return regr_ols_sm(Y, X, **param)
    elif param['lib'] == 'statsmodels':
        return regr_ols_sm(Y, X, **param)
    elif param['lib'] == 'sklearn':
        return regr_ols_sklearn(Y, X, **param)


"""
================================================================================
# MODEL FACTORY
================================================================================
"""
def ml_model_factory(y, X, ml_model):
    if ml_model=='regr_ols':
        model_reg, reg_model = None, None
        if len(y) >= 7:
            model_reg, reg_model = regr_ols_sm(y, X)
        return model_reg, reg_model

    if ml_model=='regr_ols_regu':
        model_reg, reg_model = None, None
        if len(y) >= 7:
            model_reg, reg_model = regr_ols_sm(y, X)
        return model_reg, reg_model

    if ml_model=='regr_gls':
        model_reg, reg_model = None, None
        if len(y) >= 7:
            model_reg, reg_model = regr_gls_sm(y, X)
        return model_reg, reg_model

    if ml_model=='regr_log':

        return model_reg, reg_model

"""
================================================================================
# Linear regression - # statsmodels
================================================================================
"""
def regr_ols_sm(y: Union[np.ndarray, pd.DataFrame], x: Union[np.ndarray, pd.DataFrame], **param):
    ''' Use:

    '''
    # X = np.column_stack( (np.ones(N), x**2) )   # ones at beg, BUT need length
    # if str(type(x)) == "<class 'numpy.ndarray'>" or type(x) is pd.core.frame.DataFrame:
    if type(x) == np.ndarray or type(x) is pd.DataFrame:
        X = sm.add_constant(x)
    else:
        X = np.array(x).T
        X = sm.add_constant(X)

    if str(type(y)) == "<class 'numpy.ndarray'>" or type(y) is pd.DataFrame:
        Y = y
    else:
        Y = np.array(y)

    #results = sm.OLS(endog=Y, exog=X).fit()    # endog == dep, exog == indp
    model = sm.OLS(endog=Y, exog=X)
    reg_model = model.fit()

    return model, reg_model


    """
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(y, X).fit()
    return results

    simulated data:
    X = sm.add_constant(np.arange(100))
    y = np.dot(X, [1,2]) + np.random.normal(size=100)

    pred:
    X = sm.add_constant(strat[eqn_]['df_train'].iloc[:,1:])
    y_hat = np.dot(X, reg_model.params)

    print(reg_model.predict()[-10:] == strat[eqn_]['df_train']['es_'][-10:]*reg_model.params[1] + reg_model.params[0])
    """

    bl_matplotlib = param.get('bl_matplotlib', None)
    if len(x) == 1 and bl_matplotlib:
        """
        fig, ax = plt.subplots()
        fig = sm.graphics.plot_fit(regr_stats, 0, ax=ax)
        ax.set_ylabel("Y")
        ax.set_xlabel("X")
        ax.set_title("Linear Regression")
        #plt.show()
        plt.savefig(os.path.join(MATPLOTLIB_OUT_DIR, MATPLOTLIB_OUT_FILESUFFIX + '.' + MATPLOTLIB_OUT_FILEFORMAT)
                    , bbox_inches='tight')
        """
        x_pred, y_pred = [], []
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.scatter(x, y, alpha=0.5, color='orchid')
        fig.suptitle('Regression Scatter Plot')
        fig.tight_layout(pad=2, w_pad=0.2)
        ax.grid(True)
        #fig.savefig(os.path.join(MATPLOTLIB_OUT_DIR, MATPLOTLIB_OUT_FILESUFFIX + '.' + MATPLOTLIB_OUT_FILEFORMAT),
        #            dpi=125)
        x_pred = np.linspace(X.min(), X.max(), 50)
        x_pred2 = sm.add_constant(x_pred)
        y_pred = regr.predict(x_pred2)
        ax.plot(x_pred, y_pred, '-', color='darkorchid', linewidth=2)
        fig.subplots_adjust(left=0.1)   #, right=0.9, top=0.9, bottom=0.1)
        fig.savefig(os.path.join(MATPLOTLIB_OUT_DIR, MATPLOTLIB_OUT_FILESUFFIX + '_' + current_user.username + '.' + MATPLOTLIB_OUT_FILEFORMAT),
                    dpi=125)

        return (regr, (x_pred, y_pred))


def regr_ols_sklearn(X, Y, **param):
    """
    sklearn.linear_model also has similar interfaces to do various kinds of regularizations on the regression.
    """
    reg_model = linear_model.LinearRegression(fit_intercept=True)
    reg_model.fit(X, Y)
    return reg_model

    """
    from sklearn import datasets ## imports datasets from scikit-learn

    data = datasets.load_boston()

    df = pd.DataFrame(data.data, columns=data.feature_names)   # X
    target = pd.DataFrame(data.target, columns=["MEDV"])       # y

    X = df["RM"]
    y = target[“MEDV”]
    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit()

    model.summary()

                            OLS Regression Results
==============================================================================
Dep. Variable:                   MEDV   R-squared:                       0.484
Model:                            OLS   Adj. R-squared:                  0.483
Method:                 Least Squares   F-statistic:                     471.8
Date:                Sat, 19 Jan 2019   Prob (F-statistic):           2.49e-74
Time:                        08:53:21   Log-Likelihood:                -1673.1
No. Observations:                 506   AIC:                             3350.
Df Residuals:                     504   BIC:                             3359.
Df Model:                           1
Covariance Type:            nonrobust
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
const        -34.6706      2.650    -13.084      0.000     -39.877     -29.465
RM             9.1021      0.419     21.722      0.000       8.279       9.925
==============================================================================
Omnibus:                      102.585   Durbin-Watson:                   0.684
Prob(Omnibus):                  0.000   Jarque-Bera (JB):              612.449
Skew:                           0.726   Prob(JB):                    1.02e-133
Kurtosis:                       8.190   Cond. No.                         58.4
==============================================================================

X = df[["RM", "LSTAT"]]
y = target["MEDV"]
model = sm.OLS(y, X).fit()
model.summary()

                            OLS Regression Results
==============================================================================
Dep. Variable:                   MEDV   R-squared:                       0.948
Model:                            OLS   Adj. R-squared:                  0.948
Method:                 Least Squares   F-statistic:                     4637.
Date:                Sat, 19 Jan 2019   Prob (F-statistic):               0.00
Time:                        08:57:20   Log-Likelihood:                -1582.9
No. Observations:                 506   AIC:                             3170.
Df Residuals:                     504   BIC:                             3178.
Df Model:                           2
Covariance Type:            nonrobust
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
RM             4.9069      0.070     69.906      0.000       4.769       5.045
LSTAT         -0.6557      0.031    -21.458      0.000      -0.716      -0.596
==============================================================================
Omnibus:                      145.153   Durbin-Watson:                   0.834
Prob(Omnibus):                  0.000   Jarque-Bera (JB):              442.157
Skew:                           1.351   Prob(JB):                     9.70e-97
Kurtosis:                       6.698   Cond. No.                         4.72
==============================================================================

    predictions = model.predict(X)


    lm = linear_model.LinearRegression()
    model = lm.fit(X,y)
    predictions = lm.predict(X)
    print(predictions)[0:5]
    lm.score(X,y)
    lm.coef_
    lm.intercept_

    print('Coefficients: \n', regr.coef_)
    print("Mean squared error: %.2f"
          % np.mean((regr.predict(diabetes_X_test) - diabetes_y_test) ** 2))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % regr.score(diabetes_X_test, diabetes_y_test))
    """


def regr_gls_sm(y: Union[np.ndarray, pd.DataFrame], x: Union[np.ndarray, pd.DataFrame], **param):
    ''' Use:

    '''
    # X = np.column_stack( (np.ones(N), x**2) )   # ones at beg, BUT need length
    # if str(type(x)) == "<class 'numpy.ndarray'>" or type(x) is pd.core.frame.DataFrame:
    if type(x) == np.ndarray or type(x) is pd.DataFrame:
        X = sm.add_constant(x)
    else:
        X = np.array(x).T
        X = sm.add_constant(X)

    if not str(type(y)) == "<class 'numpy.ndarray'>" or not type(y) is pd.DataFrame:
        y = np.array(y)

    model = sm.OLS(y, X)
    fit_ols = model.fit()

    # fit_ols = strat['model'][eqn_f]['fit_model']
    # y, X = strat['model'][eqn_f]['df_train_filter'].iloc[:,0], strat['model'][eqn_f]['df_train_filter'].iloc[:,1:]
    ols_resid = fit_ols.resid

    ols_resid = ols_resid.to_numpy()
    resid_fit = sm.OLS(ols_resid[1:], sm.add_constant(ols_resid[:-1])).fit()
    # print(resid_fit.tvalues[1])
    # print(resid_fit.pvalues[1])

    rho = resid_fit.params[1]
    order = toeplitz(range(len(ols_resid)))

    # so that our error covariance structure is actually rho**order which defines an autocorrelation structure
    sigma = rho**order
    model_gls = sm.GLS(y, X, sigma=sigma)
    fit_gls = model_gls.fit()

    model_glsar = sm.GLSAR(y, X, 1)
    fit_glsar = model_glsar.iterative_fit(1)

    # print(strat['model'][eqn_f]['fit_model'].summary())
    # print(gls_results.summary())
    # print(glsar_results.summary())

    # strat['model'][eqn_f]['fit_gls'] = gls_results
    # strat['model'][eqn_f]['fit_glsar'] = glsar_results
    #
    # print(gls_results.params)
    # print(glsar_results.params)
    # print(gls_results.bse)
    # print(glsar_results.bse)

    return fit_gls, fit_glsar

    """
    y = strat['model'][eqn_f]['df_train_filter'].iloc[:, 0]
    X = strat['model'][eqn_f]['df_train_filter'].iloc[:, 1:]

    ols_resid = strat['model'][eqn_f]['reg_model'].resid
    ols_resid = ols_resid.to_numpy()
    resid_fit = sm.OLS(ols_resid[1:], sm.add_constant(ols_resid[:-1])).fit()
    print(resid_fit.tvalues[1])
    print(resid_fit.pvalues[1])

    rho = resid_fit.params[1]
    order = toeplitz(range(len(ols_resid)))

    # so that our error covariance structure is actually rho**order which defines an autocorrelation structure
    sigma = rho**order
    gls_model = sm.GLS(y, X, sigma=sigma)
    gls_results = gls_model.fit()

    glsar_model = sm.GLSAR(y, X, 1)
    glsar_results = glsar_model.iterative_fit(1)

    glsar_results.summary()

    print(gls_results.params)
    print(glsar_results.params)
    print(gls_results.bse)
    print(glsar_results.bse)

    print(strat['model'][eqn_f]['df_train_filter'].columns)
    """


def calc_corrcoeffmatrix(Y,X):
    m = np.array(X)
    #if USER_ID == 4:
    #  m = np.row_stack((Y,m))
    m = np.row_stack((Y,m))
    ccm = np.corrcoef(m)
    return str(ccm)


def save_regression_feature(lst_header, Y, X):
    dir_file = os.path.join(EXTRA_OUT_DIR, REGRESSION_FEATURES_OUT_FILESUFFIX + '_' + current_user.username +'.csv')
    with open(dir_file, 'w', newline='') as fp:
      csv_writer = csv.writer(fp, delimiter=',')  # quoting=csv.QUOTE_NONNUMERIC, quotechar='"')

      csv_writer.writerow(lst_header)
      for i in range(len(Y)):
          data_row = [Y[i]]
          for x in X:
              data_row.append(x[i])
          csv_writer.writerow(data_row)

      """
      with open('thefile.csv', 'rb') as f:
        data = list(csv.reader(f))
        # or
        reader = csv.reader(f)
        for row in reader:
          print(row)

      fieldnames = ('Title 1', 'Title 2', 'Title 3')
      writer = csv.DictWriter(f, fieldnames=fieldnames)
      headers = dict( (n,n) for n in fieldnames )
      writer.writerow(headers)
      for i in range(10):
          writer.writerow({ 'Title 1':i+1,
                            'Title 2':chr(ord('a') + i),
                            'Title 3':'08/%02d/07' % (i+1),
                            })
      """

# ------------------------------------------------------------------------------

def clean_nan_inf_np(x, y):
    # X = np.column_stack( (np.ones(N), x**2) )   # ones at beg, BUT need length
    mask=[True]
    if str(type(x)) == "<class 'numpy.ndarray'>" or type(x) is pd.core.frame.DataFrame:
        if type(x) is np.ndarray:
            # x = x[~numpy.isnan(x)]
            # filter(lambda v: v==v, x)  works both for lists and numpy array since v!=v only for NaN, also strings
            # mask = np.all(np.isnan(a) | np.equal(a, 0), axis=1)
            # a[~mask]
            mask = np.isfinite(x)
            if not all(mask):
                X = x[mask]
        elif type(x) is pd.core.frame.DataFrame:
           # x = x.dropna(inplace=True)
           mask = ~x.isin([np.nan, np.inf, -np.inf]).any(1)
           if not all(mask):
               X = x[mask]
    else:
        X = np.array(x)
        mask = np.isfinite(X)
        if not all(mask):
            X = X[mask]

    if str(type(y)) == "<class 'numpy.ndarray'>" or type(y) is pd.core.frame.DataFrame:
        if type(y) is np.ndarray:
            #Y = y[np.isfinite(y)]
            if not all(mask):
                Y = y[mask]
        elif type(y) is pd.core.frame.DataFrame:
            #Y = y[~y.isin([np.nan, np.inf, -np.inf]).any(1)]
            if not all(mask):
                Y = y[mask]
    else:
        Y = np.array(y)
        # Y = Y[np.isfinite(Y)]
        if not all(mask):
            Y = Y[mask]

    # TODO:
    #np.nan_to_num(K)

    return X, Y


def clean_nan_inf_pd(df):
    #df.replace([np.inf, -np.inf], np.nan).dropna()  # subset=['col1','col2'], how='all')
    return df.replace([np.inf, -np.inf], np.nan).dropna()


def transform_pctchange_clean_standardize_sample_pd(
      x_all_raw: pd.Series, y_all_raw: pd.Series,
      idx_per_beg, idx_per_end) -> pd.Series:
    # Must be done in this order:

    #x_all = df_pair[sym_0_col].pct_change()
    #y_all = df_pair[sym_1_col].pct_change()
    #x_per = df_pair.loc[dtrange[0]:dtrange[1],sym_0_col].pct_change()#[1:]
    #y_per = df_pair.loc[dtrange[0]:dtrange[1],sym_1_col].pct_change()#[1:]

    # 0/ Stationarize
    x_all = x_all_raw.pct_change()
    y_all = y_all_raw.pct_change()

    # 1/ Clean
    #x_per, y_per = clean_nan_inf(x_per, y_per)
    x_all = clean_nan_inf_pd(x_all)
    y_all = clean_nan_inf_pd(y_all)

    # 2/ Standardize method 0/
    x_per = x_all.loc[idx_per_beg:idx_per_end]
    y_per = y_all.loc[idx_per_beg:idx_per_end]

    x_all = (x_all - x_all.mean())/x_all.std()
    y_all = (y_all - y_all.mean())/y_all.std()
    x_per = (x_per - x_per.mean())/x_per.std()
    y_per = (y_per - y_per.mean())/y_per.std()

    """
    # Standardize method 1/
    x_all = (x_all - x_all.mean())/x_all.std()
    y_all = (y_all - y_all.mean())/y_all.std()

    x_per = x_all.loc[idx_per_beg:idx_per_end]
    y_per = y_all.loc[idx_per_beg:idx_per_end]
    """

    return x_all, y_all, x_per, y_per


def transform_pctchange_clean_standardize_pd(x_all_raw:pd.Series) -> pd.Series:
    ''' Stationarize -> Clean -> Standardize '''
    # 0/ Stationarize
    x_all = x_all_raw.pct_change()
    # 1/ Clean
    x_all = clean_nan_inf_pd(x_all)
    # 2/ Standardize method 0/
    x_all = (x_all - x_all.mean())/x_all.std()

    return x_all


def calc_matrix_reg(x_all:pd.Series, y_all:pd.Series, per_corr:int) -> list:
    ''' matrix of regression - ie, rolling regression - usually for 3d surface plot '''
    steps = int(x_all.size/per_corr)

    z_reg_dt=[]
    y_dt=[]

    for s in range(steps):
        #x_per = x_all.loc[dtrange[0]:dtrange[1]]
        #y_per = y_all.loc[dtrange[0]:dtrange[1]]
        idx_beg, idx_end = x_all.size-(per_corr*(s+1)), x_all.size-(per_corr*s)
        print(idx_beg, idx_end)

        x_per = x_all.iloc[idx_beg:idx_end]
        y_per = y_all.iloc[idx_beg:idx_end]
        x_per = (x_per - x_per.mean())/x_per.std()
        y_per = (y_per - y_per.mean())/y_per.std()

        model, reg_model = regr_ols_sm(x_per, y_per)
        x_reg = x_per
        y_reg = reg_model.predict()

        # Cant just reverse, must order, but not just sort by itself, either bec could be downward sloping
        #z_reg_dt.append(y_reg.tolist()[::-1])
        _x, _y = (list(t) for t in zip(*sorted(zip(x_reg, y_reg))))
        z_reg_dt.append(_y[::-1])

        y_dt.append(str(x_per.index[-1])[:10])

        # print(reg_model.summary())
        #fig = get_figure_scatter_reg(x_all, y_all, x_per, y_per, x_reg, y_reg, sym_0, sym_1, per)
        #iplot(fig)

    x_idx_reg = list(range(1,len(y_per)+1))   # list(range(len(y_per),0,-1))
    y_dt.reverse()

    return x_idx_reg, y_dt, z_reg_dt
