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
"""

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
"""

# ==============================================================================
"""
$ cp /opt/www/rivercast/data/regression_feature_admin.csv regression_feature_X.csv

$ scp stats_instr.py admin@192.241.219.240:~/projects/rivercast/flask_blueprint/apps/app_analytic/analysis_r/

>>> from stats_instr import *

1. Working well now.  Enter 1615, Exit next 1615,
O<C1
C<C2
C2<C4
C3<C5

y: c-c1
X: o1-c2, c1-c3, c3-c5, c4-c6

2. Strategy that used to work, but not now,  Enter 1615, Exit next 1615
O<C1
C<O
C<C3

y: c-c1
X: o1-c2, c1-c4

'regression_feature_admin_6.csv'
y : c-c1
X1: o1-c2, X2: o1-c1, X3: o2-c3, X4: c1-c2, X5: c2-c3, X6: c3-c4


y: c-c1
X: c3-c5, c4-c6, c1-c4
adjR^2: 0.08

"""

# ------------------------------------------------------------------------------

FNAME = 'regression_feature_6.csv'
# Index(['c_c1', 'o1_c2', 'o1_c1', 'o2_c3', 'c1_c2', 'c2_c3', 'c3_c4'], dtype='object')
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
"""
o1_c1 and c1_c2 is 0.8, so DONT want both in same X
"""
df.shape


# ------------------------------------------------------------------------------

df_train = df.iloc[:-N_TEST]
df_test = df.iloc[-N_TEST:]

#df_train_3up = df_train[(df_train.c1_c2 >= 0) & (df_train.c2_c3 >= 0) & (df_train.c3_c4 >= 0)].loc[:,['c_c1', 'c1_c2', 'c2_c3', 'c3_c4']]
#df_test_3up = df_test[(df_test.c1_c2 >= 0) & (df_test.c2_c3 >= 0) & (df_test.c3_c4 >= 0)].loc[:,['c_c1', 'c1_c2', 'c2_c3', 'c3_c4']]
df_train_3up = df_train[(df_train.c1_c2 >= 0) & (df_train.c2_c3 >= 0) & (df_train.c3_c4 >= 0)]
df_test_3up = df_test[(df_test.c1_c2 >= 0) & (df_test.c2_c3 >= 0) & (df_test.c3_c4 >= 0)]

df_train_3dn = df_train[(df_train.c1_c2 <= 0) & (df_train.c2_c3 <= 0) & (df_train.c3_c4 <= 0)]
df_test_3dn = df_test[(df_test.c1_c2 <= 0) & (df_test.c2_c3 <= 0) & (df_test.c3_c4 <= 0)]

"""
df = pd.read_csv("NBA_train.csv")
model = smf.ols(formula="W ~ PTS + oppPTS", data=df).fit()
model.summary()

# OR
y = df['W']
X = df[['PTS', 'oppPTS']]
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
model.summary()
"""

print("--------------------------------------------")
fm = "c_c1 ~ c1_c2 + c2_c3 + c3_c4"
model = smf.ols(formula=fm, data=df_train_3up).fit()
print(fm)
print("All other vars up or dn")
print("--------------------------------------------")
print(model.summary())


df_train_3up_o = df_train[ (df_train.c1_c2 >= 0) & (df_train.c2_c3 >= 0) & (df_train.c3_c4 >= 0)
                           & (df_train.o1_c2 >= 0)
                           & (df_train.c1_c2 + df_train.c2_c3 + df_train.c3_c4 >= THRESH_SUM_C)
                         ]
df_test_3up_o = df_test[ (df_test.c1_c2 >= 0) & (df_test.c2_c3 >= 0) & (df_test.c3_c4 >= 0)
                         & (df_test.o1_c2 >= 0)
                         & (df_test.c1_c2 + df_test.c2_c3 + df_test.c3_c4 >= THRESH_SUM_C)
                       ]

print(df_train_3up_o.describe())
print('\n\n')

fm_=[]
model_={}
fm_.append("c_c1 ~ c1_c2 + c2_c3 + c3_c4 + o1_c2")  # Adj. R-squared: 0.073
#fm_ = "c_c1 ~ c1_c2 + c2_c3:c3_c4 + o1_c2"  # Adj. R-squared: 0.082
# ! BUT THESE IS STILL ONLY DATA WHERE C2 > C3, C3 > c4
fm_.append("c_c1 ~ c1_c2 + o1_c2")    # Adj. R-squared: 0.081
fm_.append("c_c1 ~ c1_c2:o1_c2")      # Adj. R-squared: 0.183
for fm_m in fm_:
    model_m = smf.ols(formula=fm_m, data=df_train_3up_o).fit()
    model_[fm_m] = model_m
    print("--------------------------------------------")
    print(fm_m)
    print("--------------------------------------------")
    print(model_m.summary())

print('\n\n')

"""
fpathname, f_ext = os.path.splitext(FPATHNAME)
df_train_3up_o.to_csv(fpathname + '_train_3up_o' + f_ext)   #, cols=['a', 'b']), sep='\t', encoding='utf-8')
df_train_3up_o.to_csv(fpathname + '_test_3up_o' + f_ext)
"""

"""
--------------------------------------------------------------------------------
Out of sample prediction
--------------------------------------------------------------------------------
"""
"""
x_test = np.linspace(0, N_TEST-1, N_TEST)
#Xnew = np.column_stack((x1n, np.sin(x1n), (x1n-5)**2))
#Xnew = sm.add_constant(Xnew)
#ypred_outsample = model.predict(Xnew)        # predict out of sample

# ypred_outsample = model.predict(X[-10:,:])   # predict out of sample

X = df_test_3up.loc[:, ['c1_c2', 'o1_o2']]
X = sm.add_constant(X)
ypred_outsample = model.predict(X)
print(ynewpred)
"""

print ("""--------------------------------------------------------------------------------
Out of sample prediction
--------------------------------------------------------------------------------\n\n
""")
# fm_ == ['c_c1 ~ c1_c2 + c2_c3 + c3_c4 + o1_c2', 'c_c1 ~ c1_c2 + o1_c2', 'c_c1 ~ c1_c2:o1_c2']
ypred_test_={}
df_test_={}
#df_X = df_test_3up_o.loc[:, ['c1_c2', 'c2_c3', 'c3_c4', 'o1_c2']]
df_test_[fm_[0]] = df_test_3up_o[['c1_c2', 'c2_c3', 'c3_c4', 'o1_c2']]
df_test_[fm_[1]] = df_test_3up_o[['c1_c2','o1_c2']]
df_test_[fm_[2]] = df_test_3up_o[['c1_c2','o1_c2']]
# df_test_[fm_[2]] = pd.concat([df_test_3up_o.loc[:,'c1_c2']*df.loc[:,'o1_c2']], axis=1, keys=['c1-c2:o1_c2'])
#                  df_test_3up_o['c1_c2']*df_test_3up_o['o1_c2']  # series

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

fm_m = 'c_c1 ~ c1_c2 + c2_c3 + c3_c4 + o1_c2'
df_test_[fm_m].ix[2902]  # .iloc[0]
model_[fm_m].params * df_test_[fm_m].ix[2902].T

fm_m = 'c_c1 ~ c1_c2:o1_c2'
df_test_[fm_m].ix[2902,0]*df_test_[fm_m].ix[2902,1]*model_[fm_m].params[1] + model_[fm_m].params[0]
  == ypred_test_[fm_m][0]

df_test_[fm_m].ix[:,0]*df_test_[fm_m].ix[:,1]*model_[fm_m].params[1] + model_[fm_m].params[0]
  == ypred_test_[fm_m]

y_true: df_test_3up_o['c1_c2'] == df_test_[fm_m]['c1_c2']

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
    ytrue = df_test_3up_o['c_c1']
    ypred = ypred_test_[fm_m]
    rms = np.sqrt( sum( (t-p)**2 for t,p in zip(ytrue, ypred) )/ytrue.shape[0])
    print("RMS : " + str(rms))

print('\n')


print("--------------------------------------------")
fm_m = 'c_c1 ~ c1_c2 + c2_c3 + c3_c4 + o1_c2'
print(fm_m)
print('ALL PREDICTIONS\n')
N_pred_nothresh_both=0
N_pred_nothresh_correct_both=0
N_pred_nothresh_correct_shrt=0
expect_gain=0.0
N_true_shrt=0


ytrue = df_test_3up_o['c_c1']
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
ytrue = df_test_3up_o['c_c1']
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
