import os
import csv

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from sklearn import linear_model

from flask_login import current_user

from apps.settings.constants import EXTRA_OUT_DIR, REGRESSION_FEATURES_OUT_FILESUFFIX, \
    MATPLOTLIB_OUT_DIR, MATPLOTLIB_OUT_FILESUFFIX, MATPLOTLIB_OUT_FILEFORMAT


# ==============================================================================

"""
Linear regression - return:
param = **{'bl_matplotlib':True}
regr_stats, regr_line, scatter_data = go_regression(Y, X, **param)
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
Linear regression - statsmodels
"""
def regr_ols_sm(y, x, **param):
    X = np.array(x).T
    X = sm.add_constant(X)
    Y = y
    #results = sm.OLS(endog=Y, exog=X).fit()   # endog == dep, exog == indp
    regr = sm.OLS(Y, X).fit()

    # Graph
    x_pred, y_pred = [], []
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

    """
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(y, X).fit()
    return results
    """


def regr_ols_sklearn(Y, X, **param):
    """
    sklearn.linear_model also has similar interfaces to do various kinds of regularizations on the regression.
    """
    clf = linear_model.LinearRegression(fit_intercept=True)
    clf.fit()
    # clf.coef_ now contains coef


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
