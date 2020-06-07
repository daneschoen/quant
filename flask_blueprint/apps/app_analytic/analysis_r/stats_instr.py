import os, sys

import numpy as np
import pandas as pd

import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.sandbox.regression.predstd import wls_prediction_std

from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split

import matplotlib.pyplot as plt
import pylab
import seaborn as sns

#from flask_apps.stats import *
#from flask_apps.globals import *


# ==============================================================================

class Regr_cv():

    OUTFILENAME_STATS = 'stats_instr.txt'
    OUTFILENAME_GRAPH = 'stats_graph.png'


    def __init__(self):
        self.OUTFILENAME_STATS = OUTFILENAME_STATS
        self.OUTFILENAME_GRAPH = OUTFILENAME_GRAPH


    def get_data(self):
        try:
          with open(self.INFILENAME, 'r') as fin:
            for row in fin:
                cmdline = row.strip()
                draw_method = getattr(self, self.token_dict.get(cmdline[0]))
                if draw_method:
                    draw_method(fout, cmdline = cmdline[1:].strip())
                # can raise exception if you want
                #else:
                #    raise Exception("Command %s not implemented" % draw_method)
        except IOError as e:
          errno, strerror = e.args
          print("I/O error({0}): {1}".format(errno,strerror))


    def calc_regression(self):
        # X = np.array(x).T

        x = np.linspace(0, self.N-1, self.N)  # used for graphs

        X = np.array(x).T
        X = sm.add_constant(X)
        Y = y
        #results = sm.OLS(endog=Y, exog=X).fit()   # endog == dep, exog == indp
        regr = sm.OLS(Y, X).fit()


    def graph(self):
        pass

FNAME = 'regression_feature_6.csv'
# Index(['std_dev', 'std_var', 'o1_c1', 'o2_c3', '4_std_3_dev', '2_std_3_dev', '3_std_3_dev'], dtype='object')
FPATH = ''
FPATHNAME = os.path.join(FPATH, FNAME)

CHART_PATH = "/static/images/"


N_TEST = 500

THRESH_PRED = 1.0
THRESH_SUM_C = 0.0


df = pd.read_csv(FPATHNAME)
df
df.head(10)
df.tail(10)

df.columns

col_headings = [ch.split(':')[1].strip() for ch in df.columns]
col_headings = [ch.replace('-','_') for ch in col_headings]
col_headings = [ch.replace('+','_') for ch in col_headings]
col_headings = [ch.replace('/','_') for ch in col_headings]
df.columns = col_headings

df.columns
df.describe()
df.describe().transpose()
df.info()

df.corr()

df.shape


# ------------------------------------------------------------------------------

df_train = df.iloc[:-N_TEST]
df_test = df.iloc[-N_TEST:]

#df_train_3up = df_train[(df_train.4_std_3_dev >= 0) & (df_train.2_std_3_dev >= 0) & (df_train.3_std_3_dev >= 0)].loc[:,['std_dev', '4_std_3_dev', '2_std_3_dev', '3_std_3_dev']]
#df_test_3up = df_test[(df_test.4_std_3_dev >= 0) & (df_test.2_std_3_dev >= 0) & (df_test.3_std_3_dev >= 0)].loc[:,['std_dev', '4_std_3_dev', '2_std_3_dev', '3_std_3_dev']]
df_train_3up = df_train[(df_train.4_std_3_dev >= 0) & (df_train.2_std_3_dev >= 0) & (df_train.3_std_3_dev >= 0)]
df_test_3up = df_test[(df_test.4_std_3_dev >= 0) & (df_test.2_std_3_dev >= 0) & (df_test.3_std_3_dev >= 0)]

df_train_3dn = df_train[(df_train.4_std_3_dev <= 0) & (df_train.2_std_3_dev <= 0) & (df_train.3_std_3_dev <= 0)]
df_test_3dn = df_test[(df_test.4_std_3_dev <= 0) & (df_test.2_std_3_dev <= 0) & (df_test.3_std_3_dev <= 0)]

fpathname, f_ext = os.path.splitext(FPATHNAME)

x_test = np.linspace(0, N_TEST-1, N_TEST)
#Xnew = np.column_stack((x1n, np.sin(x1n), (x1n-5)**2))
#Xnew = sm.add_constant(Xnew)
#ypred_outsample = model.predict(Xnew)        # predict out of sample

# ypred_outsample = model.predict(X[-10:,:])   # predict out of sample

X = df_test_3up.loc[:, ['4_std_3_dev', 'o1_o2']]
X = sm.add_constant(X)
ypred_outsample = model.predict(X)
print(ynewpred)
"""

print ("""--------------------------------------------------------------------------------
Out of sample prediction
--------------------------------------------------------------------------------\n\n
""")
# fm_ == ['std_dev ~ 4_std_3_dev + 2_std_3_dev + 3_std_3_dev + std_var', 'std_dev ~ 4_std_3_dev + std_var', 'std_dev ~ 4_std_3_dev:std_var']
ypred_test_={}
df_test_={}
#df_X = df_test_3up_o.loc[:, ['4_std_3_dev', '2_std_3_dev', '3_std_3_dev', 'std_var']]
df_test_[fm_[0]] = df_test_3up_o[['4_std_3_dev', '2_std_3_dev', '3_std_3_dev', 'std_var']]
df_test_[fm_[1]] = df_test_3up_o[['4_std_3_dev','std_var']]
df_test_[fm_[2]] = df_test_3up_o[['4_std_3_dev','std_var']]
# df_test_[fm_[2]] = pd.concat([df_test_3up_o.loc[:,'4_std_3_dev']*df.loc[:,'std_var']], axis=1, keys=['c1-c2:std_var'])
#                  df_test_3up_o['4_std_3_dev']*df_test_3up_o['std_var']  # series

for fm_m in fm_:
    X_m = sm.add_constant(df_test_[fm_m])
    ypred_test_[fm_m] = model_[fm_m].predict(X_m)
    print("--------------------------------------------")
    print(fm_m + '\n')
    print(ypred_test_[fm_m])
    print("--------------------------------------------\n\n")

print('\n\n')

"""
Verify predict: y ~ model.params*X

fm_m = 'std_dev ~ 4_std_3_dev + 2_std_3_dev + 3_std_3_dev + std_var'
df_test_[fm_m].ix[2902]  # .iloc[0]
model_[fm_m].params * df_test_[fm_m].ix[2902].T

fm_m = 'std_dev ~ 4_std_3_dev:std_var'
df_test_[fm_m].ix[2902,0]*df_test_[fm_m].ix[2902,1]*model_[fm_m].params[1] + model_[fm_m].params[0]
  == ypred_test_[fm_m][0]

df_test_[fm_m].ix[:,0]*df_test_[fm_m].ix[:,1]*model_[fm_m].params[1] + model_[fm_m].params[0]
  == ypred_test_[fm_m]

y_true: df_test_3up_o['4_std_3_dev'] == df_test_[fm_m]['4_std_3_dev']

  y_hat[0] = regr.params[0]*X[0,0] + regr.params[1]*X[0,1] + regr.params[2]*X[0,2] + regr.params[3]*X[0,3]
  y_hat    = regr.params[0]*X[:,regr.params[0]*X[:,0] + regr.params[1]*X[:,1] + regr.params[2]*X[:,2] + regr.params[3]*X[:,3]0] + regr.params[1]*X[:,1] + regr.params[2]*X[:,2] + regr.params[3]*X[:,3]
           == regr.predict()  ==  regr.predict(X)
"""

print("""
--------------------------------------------------------------------------------
RMS
--------------------------------------------------------------------------------
""")
for fm_m in fm_:
    print("--------------------------------------------")
    print(fm_m)
    ytrue = df_test_3up_o['std_dev']
    ypred = ypred_test_[fm_m]
    rms = np.sqrt( sum( (t-p)**2 for t,p in zip(ytrue, ypred) )/ytrue.shape[0])
    print("RMS : " + str(rms))

print('\n')


print("--------------------------------------------")
fm_m = 'std_dev ~ 4_std_3_dev + 2_std_3_dev + 3_std_3_dev + std_var'
print(fm_m)
print('ALL PREDICTIONS\n')
N_pred_nothresh_both=0
N_pred_nothresh_correct_both=0
N_pred_nothresh_correct_shrt=0
expect_gain=0.0
N_true_shrt=0


ytrue = df_test_3up_o['std_dev']
ypred = ypred_test_[fm_m]

print("ypred       ytrue")
for i in range(len(ypred)):
    print("{0:6.2f}  :  {1:6.2f}".format(ypred[i], ytrue.iloc[i]))
    N_pred_nothresh_both += 1
    if (ytrue.iloc[i] <= 0):
        N_true_shrt += 1
    if (ypred[i] <=0 and ytrue.iloc[i] <= 0):
        N_pred_nothresh_correct_shrt += 1
    if (ypred[i] <=0 and ytrue.iloc[i] <= 0) or (ypred[i] >=0 and ytrue.iloc[i] >= 0):
        N_pred_nothresh_correct_both += 1
print("\nPct correct      :  {0:7.2}".format(N_pred_nothresh_correct_both/N_pred_nothresh_both))
print("Pct correct shrt :  {0:7.2}\n".format(N_pred_nothresh_correct_shrt/N_true_shrt))
print("Pct dn           :  {0:7.2}\n".format(N_true_shrt/N_pred_nothresh_both))

# Include threshold
ytrue = df_test_3up_o['std_dev']
for fm_m in fm_:
    N_pred_nothresh_both=0
    N_pred_nothresh_correct_both=0
    N_pred_thresh_shrt=0
    N_pred_thresh_correct_shrt=0
    expect_gain_nothresh_both=0.0
    expect_gain_thresh_shrt=0.0
    print("--------------------------------------------")
    print(fm_m )
    print("Threshold: " + str(THRESH_PRED) + '\n')
    ypred = ypred_test_[fm_m]

    print("ypred       ytrue")
    for i in range(len(ypred)):
        if ypred[i] <= 0 or ypred[i] >= 0:
        #if ypred[i] <= 0:
            N_pred_nothresh_both += 1
            expect_gain_nothresh_both += ( ytrue.iloc[i] )
        if (ypred[i] <=0 and ytrue.iloc[i] <= 0) or (ypred[i] >=0 and ytrue.iloc[i] >= 0):
        #if (ypred[i] <=0 and ytrue.iloc[i] <= 0):
            N_pred_nothresh_correct_both += 1

        #if ypred[i] <= -THRESH_PRED or ypred[i] >= THRESH_PRED:
        if ypred[i] <= -THRESH_PRED:
            print("{0:6.2f}  :  {1:6.2f}".format(ypred[i], ytrue.iloc[i]))
            N_pred_thresh_shrt += 1
            expect_gain_thresh_shrt += ( ytrue.iloc[i] )
            if (ypred[i] <=0 and ytrue.iloc[i] <= 0) :
            #if (ypred[i] <=0 and ytrue.iloc[i] <= 0):
                N_pred_thresh_correct_shrt += 1
    print("\nPct correct all         :  {0:6.2} ".format(N_pred_nothresh_correct_both/N_pred_nothresh_both))
    print("Pct correct threshhold  :  {0:6.2} ".format(N_pred_thresh_correct_shrt/N_pred_thresh_shrt))
    print("Expected Gain per trade all       :  {0:6.2} ".format(expect_gain_nothresh_both/N_pred_nothresh_both))
    print("Expected Gain per trade threshold :  {0:6.2} ".format(expect_gain_thresh_shrt/N_pred_thresh_shrt))
print('\n')

"""
================================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfilename')
    args = parser.parse_args()

    if not Draw.checkfile(args.inputname):
        print('Input file ' + args.inputfilename + ' not found')
        sys.exit()

    self.INFILENAME = args.inputfilename

    get_data()
    calc_regression()
    # calc_crossvalidation()
    graph()

"""
