import os, sys
import argparse
from copy import deepcopy

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

from lasagne import layers
from lasagne.updates import nesterov_momentum
from lasagne.nonlinearities import softmax
from nolearn.lasagne import NeuralNet

#from flask_apps.stats import *
#from flask_apps.globals import *


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


TODO:
    - thresh matrix for performance
    - completely separte performance from algorithm - for ex include nn
    - train, valid, test - all rolling
    - pre segment thresholds: df_train.c1_c2 >= 1.0
    - o is opposite
    - rms: corr SEPARATELY for long and shrt
    - Statistics: matrix of threshold predictions
    - AVG loss (not max)
    - New segmentation, new models: logistic regression w regularization, loess

- Do rolling training with data from 1999 and predict next month.
  This way you will have thousands of predictions to see how it really does.
- Research more models, maybe variations on your favorite models.
  Should have at least dozen models. 3-5 models for long and 3-5 models for shrt
  and 12 sets of these for each class of trades such as 3up, 3dn, 1-4up,
  intrady trades: o-c trades, p@1000, etc.
- Automated training of coefficients on dozens of models on weekly or monthly
  basis and automatic prediction on daily basis. Once top dozen models or so are
  tested and chosen, everything should be automated.

On the issue of Rsquared, I realize why they are so low. Traditional statistics
will penalize if it predicts a bit long and it is actually very long. And it will
penalize less if it predicts a bit long and is a bit short. This is opposite of
what we want. If it is very long with a small long prediction this is a good thing.

"""

# ==============================================================================

FIN_NAME = 'regression_feature_6.csv'
# Index(['c_c1', 'o1_c2', 'o1_c1', 'o2_c3', 'c1_c2', 'c2_c3', 'c3_c4'], dtype='object')
FIN_PATH = ''
FIN_PATHNAME = os.path.join(FIN_PATH, FIN_NAME)

CHART_PATH = "/static/images/"

DATA_DT_COL = 0
DATA_TIME_COL = 0
DATA_DTIME_COL = 0
DATA_YTRUE_COL = 0
DATA_YTRUE_NAME = 'c_c1'

# [3391 rows x 7 columns]  13 years = 2003 - 2016-quarter
# N_NOSEG = 5000
# N_seg = 500  based on this:
CV_TRAIN = 425    # 10 yr *250 = 2500 but seg...
CV_VALID = 50      # 2 yr       : 500
CV_TEST = 25
CV_KFOLD = 10
CV_KFOLD_FWD = 10

THRESHPRED_LST = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
THRESH_SUM_C = 0.0

VERBOSE = 2

# ------------------------------------------------------------------------------

class Struct_dot:
    def __init__(self, **entries):
        self.__dict__.update(entries)

"""
l = [0.0 for x in THRESHPRED_LST]
d_threshpred = {
    'thresh_both':l.copy(), 'thresh_long':l.copy(), 'thresh_shrt':l.copy()
}

{'thresh_long': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'thresh_both': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'thresh_shrt': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}

foo = {}
for fm_m in self.fm_:
    foo[fm_m] = Struct_dot(**deepcopy(d_threshpred))

"""
# ------------------------------------------------------------------------------

class Prediction:

    def __init__(self, seg_name=None):
        self.verbose = VERBOSE    # 0: None ,1: Minimum, eg files imported ok ,2: Normal, 3: yhat, ytrue
        self.savefiles = False

        self.seg_name = seg_name

        self.FIN_NAME = FIN_NAME
        # Index(['c_c1', 'o1_c2', 'o1_c1', 'o2_c3', 'c1_c2', 'c2_c3', 'c3_c4'], dtype='object')
        self.FIN_PATH = FIN_PATH
        self.FIN_PATHNAME = os.path.join(FIN_PATH, FIN_NAME)

        self.CHART_PATH = CHART_PATH

        self.DATA_DT_COL = DATA_DT_COL   # 0
        self.DATA_TIME_COL = DATA_TIME_COL   # 0
        self.DATA_DTIME_COL = DATA_DTIME_COL   # 0
        self.DATA_YTRUE_COL = DATA_YTRUE_COL     # 0
        self.DATA_YTRUE_NAME = DATA_YTRUE_NAME   # 'c_c1'

        # N_seg ~ 500
        self.CV_TRAIN = CV_TRAIN         # 425   # 10 yr *250 = 2500 but seg...
        self.CV_VALID = CV_VALID         #  50   # 500: 2 yr ...
        self.CV_TEST = CV_TEST           #  25   # 250
        self.CV_KFOLD = CV_KFOLD             #  10   # 50
        self.CV_KFOLD_FWD = CV_KFOLD_FWD     #  10   no overlaps

        self.THRESHSEGMENT_LST = [0]           # THRESHSEGMENT_LST
        self.THRESHPRED_LST = THRESHPRED_LST   # [0.5, 0.6, 0.7, 0.8, 1.0]
        self.THRESH_SUM_C = THRESH_SUM_C

        l_fd = [0.0 for x in self.THRESHPRED_LST]
        self.d_threshpred_fd = {
            'thresh_both':l_fd.copy(), 'thresh_long':l_fd.copy(), 'thresh_shrt':l_fd.copy()
        }
        """
        foo = {}
        for fm_m in self.fm_:
            foo[fm_m] = Struct_dot(**deepcopy(d_threshpred))

        foo[fm_m].thresh_long[thresh_z]
        """


    def import_data_np(self):
        try:
          with open(self.FIN_PATHNAME, 'r') as fin:
            for row in fin:
                cmdline = row.strip()
                #draw_method = getattr(self, self.token_dict.get(cmdline[0]))
                #if draw_method:
                #    draw_method(fout, cmdline = cmdline[1:].strip())
                # can raise exception if you want
                #else:
                #    raise Exception("Command %s not implemented" % draw_method)
        except IOError as e:
          errno, strerror = e.args
          print("I/O error({0}): {1}".format(errno,strerror))


    def import_data_pandas(self):
        self.df = pd.read_csv(self.FIN_PATHNAME)
        if self.verbose >= 1:
            print("\n================================================================================\n")
            print("Imported", self.FIN_PATHNAME, "\n")
            if self.verbose >= 2:
                print(self.df)    # df.head(10),  df.tail(10)
                print(self.df.columns)

        col_headings = [ch.split(':')[1].strip() for ch in self.df.columns]
        col_headings = [ch.replace('-','_') for ch in col_headings]
        col_headings = [ch.replace('+','_') for ch in col_headings]
        col_headings = [ch.replace('/','_') for ch in col_headings]
        self.df.columns = col_headings

        if self.verbose >= 2:
            print(self.df.columns, '\n')
            print(self.df.describe(), '\n')
            print(self.df.describe().transpose(), '\n')

            print('df.shape:',self.df.shape, '\n')
            print(self.df.info(), '\n')

            print(self.df.corr(), '\n')
            """
            o1_c1 and c1_c2 is 0.8, so DONT want both in same X
            """


    def segment_data(self):
        thresh_seg = self.THRESHSEGMENT_LST[-1]
        df = self.df
        df_seg_ = {}

        #df_train_seg_ = {}
        #df_test_seg_ = {}

        #df_train_3up = df_train[(df_train.c1_c2 >= 0) & (df_train.c2_c3 >= 0) & (df_train.c3_c4 >= 0)].loc[:,['c_c1', 'c1_c2', 'c2_c3', 'c3_c4']]
        #df_test_3up = df_test[(df_test.c1_c2 >= 0) & (df_test.c2_c3 >= 0) & (df_test.c3_c4 >= 0)].loc[:,['c_c1', 'c1_c2', 'c2_c3', 'c3_c4']]

        df_seg_['all'] = df
        df_seg_['3up'] = df[ (df.c1_c2 >= thresh_seg) & (df.c2_c3 >= thresh_seg) & (df.c3_c4 >= thresh_seg) ]
        df_seg_['3dn'] = df[ (df.c1_c2 <= thresh_seg) & (df.c2_c3 <= thresh_seg) & (df.c3_c4 <= thresh_seg) ]
        df_seg_['3up_oup'] = df[ (df.c1_c2 >= thresh_seg) & (df.c2_c3 >= thresh_seg) & (df.c3_c4 >= thresh_seg)
                                 & (df.o1_c2 >= thresh_seg)
                                 #& (df_train.c1_c2 + df_train.c2_c3 + df_train.c3_c4 >= THRESH_SUM_C)
                               ]
        df_seg_['3up_odn'] = df[ (df.c1_c2 >= thresh_seg) & (df.c2_c3 >= thresh_seg) & (df.c3_c4 >= thresh_seg)
                                 & (df.o1_c2 <= thresh_seg)
                               ]
        df_seg_['3dn_odn'] = df[ (df.c1_c2 <= thresh_seg) & (df.c2_c3 <= thresh_seg) & (df.c3_c4 <= thresh_seg)
                                & (df.o1_c2 <= thresh_seg)
                               ]
        df_seg_['3dn_oup'] = df[ (df.c1_c2 <= thresh_seg) & (df.c2_c3 <= thresh_seg) & (df.c3_c4 <= thresh_seg)
                                 & (df.o1_c2 >= thresh_seg)
                               ]
        self.df_seg_ = df_seg_


    def go_segment_kfold(self, seg_name):
        self.import_data_pandas()
        self.segment_data()

        if seg_name not in self.df_seg_:
            raise RuntimeError('Segmentation name not in df_seg_:', self.df_seg_.keys())
        self.seg_name = seg_name

        # self.CV_VALID = 50      # 2 yr       : 500
        # self.CV_TEST = 25
        # self.CV_KFOLD = 10
        # self.CV_KFOLD_FWD = 10
        # self.CV_TRAIN = None

        self.crossvalidate_kfold()
        # self.calc_models()
        # self.calc_predictions()
        # self.calc_rms()
        # self.calc_cv(df_test_, yhat_test_)
        # graph()

        """
from s import *

seg_name = '3up_oup'
pred = Prediction()
pred = Prediction(seg_name)

# pred.THRESHSEGMENT_LST = [1.0]
# pred.go_segment_kfold(seg_name)

pred.get_data_pandas()
pred.segment_data()
# pred.seg_name = seg_name

pred.df_seg_.keys()
print('pred.seg_name:', pred.seg_name)
df_seg = pred.df_seg_[pred.seg_name]

pred.df_seg_['all'].head(30)
df_seg.head(10)

# self.CV_VALID = 50      # 2 yr       : 500
# self.CV_TEST = 25
# self.CV_KFOLD = 10
# self.CV_KFOLD_FWD = 10
# self.CV_TRAIN = None

pred.crossvalidate_kfold(pred.CV_KFOLD)

            print("--------------------------------------------")
            fm = "c_c1 ~ c1_c2 + c2_c3 + c3_c4"
            model_train = self.calc_ols(fm, self.df_seg_['all'])
            print(fm)
            print("Train - No segmentation", '\n')
            print(self.df_train.describe(), '\n')
            print(model_train.summary())
            print("--------------------------------------------")

            print("--------------------------------------------")
            fm = "c_c1 ~ c1_c2 + c2_c3 + c3_c4"
            model_train = self.calc_ols(fm, self.df_seg_['all'])
            print(fm)
            print("Train - No segmentation", '\n')
            print(self.df_train.describe(), '\n')
            print(model_train.summary())
            print("--------------------------------------------")

            print("--------------------------------------------")
            fm = "c_c1 ~ c1_c2 + c2_c3 + c3_c4"
            model_train_3up = self.calc_ols(fm, self.df_train_3up)
            print(fm)
            print("Train - Segmentation Threshold: x", '\n')
            print(self.df_train_3up.describe(), '\n')
            print(model_train_3up.summary(), '\n')
            print("--------------------------------------------")

            print("--------------------------------------------")
            fm = "c_c1 ~ c1_c2 + c2_c3 + c3_c4 + o1_c2"
            model_train_3up_oup = self.calc_ols(fm, self.df_train_3up_oup)
            print(fm)
            print("Train - Segmentation Threshold: x", '\n')
            print(self.df_train_3up_oup.describe(), '\n')
            print(model_train_3up_oup.summary(), '\n')
            print("--------------------------------------------")
            print('\n\n')


        df = prediction.df
        nparr = df.values   # df.as_matrix(columns=df.columns[1:])

        prediction.split_segment_data()

        df_train_3up_oup = prediction.df_train_3up_oup
        df_test_3up_oup = prediction.df_test_3up_oup

        prediction.calc_models()
        yhat_valid = calc_pred_models(self.df_valid_seg_k)
        prediction.calc_rms()
        prediction.calc_cv()
        """


    def crossvalidate_kfold(self):
        print("\n================================================================================\n")
        df_seg = self.df_seg_[self.seg_name]
        if self.verbose >= 1:
            print("Segment   :", self.seg_name, "     df_seg.shape:", df_seg.shape)

        self.N_seg = df_seg.shape[0]    # 392

        self.metric_seg_k_ = []

        # self.CV_VALID = 50      # 2 yr       : 500
        # self.CV_TEST = 25
        # self.CV_KFOLD = 10
        # self.CV_KFOLD_FWD = 10
        # self.CV_TRAIN = None
        self.CV_TRAIN = self.N_seg - ( self.CV_VALID + self.CV_TEST + self.CV_KFOLD_FWD*(self.CV_KFOLD-1) )
        model_k_=[]
        for k in range(self.CV_KFOLD):
            r_beg, r_end = self.CV_KFOLD_FWD*k, self.CV_KFOLD_FWD*k + self.CV_TRAIN
            v_beg, v_end = r_end, r_end + self.CV_VALID
            t_beg, t_end = v_end, v_end + self.CV_TEST
            if self.verbose >= 1:
                print("KFOLD     :", k, "of", self.CV_KFOLD)
                print("KFOLD_FWD :", self.CV_KFOLD_FWD)
                print("TRAIN     : {0}     VALID: {1}     TEST: {2}".format(
                  self.CV_TRAIN, self.CV_VALID, self.CV_TEST
                ))
                print("           [{0}:{1}]        [{2}:{3}]    [{4}:{5}]".format(
                  r_beg, r_end, v_beg, v_end, t_beg, t_end
                ))
            df_train_seg_k = df_seg.iloc[r_beg:r_end, :]
            df_valid_seg_k = df_seg.iloc[v_beg:v_end, :]
            df_test_seg_k  = df_seg.iloc[t_beg:t_end, :]
            #self.df_train = self.df.iloc[:-self.CV_VALID]
            #self.df_test = self.df.iloc[-self.CV_VALID:]
            model_k_.append(self.get_models(df_train_seg_k))

            yhat_train_seg_k_m_ = self.get_pred_models(model_k_[k], df_train_seg_k)
            yhat_valid_seg_k_m_ = self.get_pred_models(model_k_[k], df_valid_seg_k)
            yhat_test_seg_k_m_  = self.get_pred_models(model_k_[k], df_test_seg_k)

            info_seg_k  = '{0:<22} {1:<}'.format( 'k: ' + str(k) + ' of KFold: ' + str(self.CV_KFOLD), 'KFold_fwd: ' + str(self.CV_KFOLD_FWD) ) + '\n'
            info_seg_k += '{0:<22} {1:<}'.format( 'seg_name: ' + self.seg_name, 'df_seg.shape: ' + str(df_seg.shape) ) + '\n'
            info_seg_k += '{0:<22} {1:<}'.format( 'train, valid, test: ', str((r_beg, r_end)) + ' , ' + str((v_beg, v_end))  + ' , ' + str((t_beg, t_end)) )

            metric_seg_k = {}

            ytrue_seg_par_k = df_train_seg_k[self.DATA_YTRUE_NAME]
            meta = {'info': info_seg_k}
            meta['partition'] = 'TRAIN'
            metric_seg_k['train'] = self.get_performance(ytrue_seg_par_k, yhat_train_seg_k_m_, **meta)

            ytrue_seg_par_k = df_valid_seg_k[self.DATA_YTRUE_NAME]
            meta = {'info': info_seg_k}
            meta['partition'] = 'VALID'
            metric_seg_k['valid'] = self.get_performance(ytrue_seg_par_k, yhat_valid_seg_k_m_, **meta)

            ytrue_seg_par_k = df_test_seg_k[self.DATA_YTRUE_NAME]
            meta = {'info': info_seg_k}
            meta['partition'] = 'TEST'
            metric_seg_k['test']  = self.get_performance(ytrue_seg_par_k, yhat_test_seg_k_m_, **meta)

            self.metric_seg_k_.append(metric_seg_k)

        self.model_selected = self.select_model()
        if self.verbose >= 1:
            print("Model Selected: ", self.model_selected)
            print("\n================================================================================\n\n")

        """
        [0...500-1]   Train: 335 = 500 - (50+25+90)
        Kfold   Train     Valid     Test
                    +335       +50       +25
        0      [0   :335] [335:385] [385:410]
        1      [+10 :345] [345:395] [395:420]
        k      N: [F*k     : F*k+N]
               V: [F*k+N   : F*k+N+V]
               T: [F*k+N+V : F*k+N+V+T]
               ...
        9      [90  :425] [425:475] [475:500]

        NVT = [T, 50, 25]
        K_F = [10, 10]
        [0...392-1]   Train: 227 = 392 - (50+25+ (10*9))
        0      [0   :227] [227:277] [277:302]
        9      [90  :317] []        [   :392]

        NVT = [T, 50, 25]
        K_F = [20, 5]
        [0...392-1]   Train: 222 = 392 - (50+25+ 5*(20-1))
        0      [0   :222] [222:272] [272:297]
        19     [95 :T+95] [T+95: T+95+50] [T+50+95 :  T+50+25+95]
        19     [95 :] [317:317+50] [367:392]

        NVT = [T, 50, 25]
        K_F = [10, 5]
        [0...392-1]   Train: 272 = 392 - (50 + 25 + (5*(10-1)))
        0      [0  :272] [272:322] [322:347]
        1      [5  :277] [277:327] [327:352]
        9      [45 :317] [317:367] [342:392]

        CV_KFOLD = 1
        self.CV_TRAIN = self.N_seg - ( CV_VALID + CV_TEST + CV_KFOLD_FWD*(CV_KFOLD-1) )
                      = 392 - (50 + 25)
        """

    def select_model(self):

        return "TO DO"

    def get_sm_ols(self, fm, df):
        """
        y = df['y']
        X = df[['x1', 'x2']]
        X = sm.add_constant(X)
        model = sm.OLS(y, X).fit()
        model.summary()

        x = np.linspace(0, self.N-1, self.N)  # used for graphs

        X = np.array(x).T
        X = sm.add_constant(X)
        Y = y
        model = sm.OLS(endog=Y, exog=X).fit()   # endog == dep, exog == indp
        model = sm.OLS(Y, X).fit()
        """
        #self.model_train_3up = smf.ols(formula=fm, data=self.df_train_3up).fit()
        return smf.ols(formula=fm, data=df).fit()


    def get_models(self, df_train):
        self.fm_=[]
        self.fmX_=[]
        model_={}
        # ! THESE IS STILL ONLY DATA WHERE C2 > C3, C3 > c4
        self.fm_.append("c_c1 ~ c1_c2 + c2_c3 + c3_c4")  # Adj. R-squared: 0.073
        self.fmX_.append(['c1_c2', 'c2_c3', 'c3_c4'])
        self.fm_.append("c_c1 ~ c1_c2 + c2_c3:c3_c4")
        self.fmX_.append(['c1_c2', 'c2_c3', 'c3_c4'])
        self.fm_.append("c_c1 ~ c1_c2 + c2_c3 + c3_c4 + o1_c2")  # Adj. R-squared: 0.073
        self.fmX_.append(['c1_c2', 'c2_c3', 'c3_c4', 'o1_c2'])
        self.fm_.append("c_c1 ~ c1_c2:o1_c2 + c2_c3:c3_c4")    # Adj. R-squared: 0.082
        self.fmX_.append(['c1_c2', 'c2_c3', 'c3_c4', 'o1_c2'])
        self.fm_.append("c_c1 ~ c1_c2 + o1_c2")    # Adj. R-squared: 0.081
        self.fmX_.append(['c1_c2', 'o1_c2'])
        self.fm_.append("c_c1 ~ c1_c2*o1_c2")
        self.fmX_.append(['c1_c2', 'o1_c2'])
        self.fm_.append("c_c1 ~ c1_c2:o1_c2")      # Adj. R-squared: 0.183
        self.fmX_.append(['c1_c2', 'o1_c2'])

        for fm_m in self.fm_:
            model_m = smf.ols(formula=fm_m, data=df_train).fit()
            model_[fm_m] = model_m
            print("\n--------------------------------------------")
            print(fm_m)
            print("--------------------------------------------\n")
            print(model_m.summary())

        print('\n')

        if self.savefiles:
            self.savefiles_segment()

        return model_


    def savefiles_segment(self):
        fpathname, f_ext = os.path.splitext(FIN_PATHNAME)
        df_train_3up_oup.to_csv(fpathname + '_train_3up_o' + f_ext)   #, cols=['a', 'b']), sep='\t', encoding='utf-8')
        df_train_3up_oup.to_csv(fpathname + '_test_3up_o' + f_ext)


    """
    ============================================================================
    Out of sample prediction
    ============================================================================

    x_test = np.linspace(0, CV_VALID-1, CV_VALID)
    #Xnew = np.column_stack((x1n, np.sin(x1n), (x1n-5)**2))
    #Xnew = sm.add_constant(Xnew)
    #yhat_outsample = model.predict(Xnew)        # predict out of sample

    # yhat_outsample = model.predict(X[-10:,:])   # predict out of sample

    X = df_test_3up.loc[:, ['c1_c2', 'o1_o2']]
    X = sm.add_constant(X)
    yhat_outsample = model.predict(X)
    print(ynewpred)
    """
    def get_pred_models(self, model_, df_outsample):
        """
        Prediction - for all models - for any given df outsample
        """
        print ("""
================================================================================
CROSS-VALIDATION PHASE
Calc yhat for Out of sample prediction - for all models
================================================================================\n\n
        """)

        yhat_outsample_m_ ={}
        """
        df_outsample_m_ = {}
        #df_X = df_test_3up_oup.loc[:, ['c1_c2', 'c2_c3', 'c3_c4', 'o1_c2']]
        for fm_m, fmX_m in zip(self.fm_, self.fmX_):
            #df_test_[fm_m] = self.df_test_3up_oup[fmX_m]
            df_outsample_m_[fm_m] = df_outsample[fmX_m]
        """
        # df_test_[fm_[2]] = pd.concat([df_test_3up_oup.loc[:,'c1_c2']*df.loc[:,'o1_c2']], axis=1, keys=['c1-c2:o1_c2'])
        # df_test_3up_oup['c1_c2']*df_test_3up_oup['o1_c2']  # series

        for fm_m in self.fm_:
            #X_m = sm.add_constant(df_outsample_[fm_m])
            X_m = sm.add_constant(df_outsample)
            yhat_outsample_m_[fm_m] = model_[fm_m].predict(X_m)

            if self.verbose >= 2:
                print("--------------------------------------------")
                print("Calc yhat for: ", fm_m, '\n')
                if self.verbose >= 3:
                    print(yhat_outsample_m_[fm_m])
                print("--------------------------------------------\n")

        return yhat_outsample_m_
    """
    Verify predict: y ~ model.params*X

    fm_m = 'c_c1 ~ c1_c2 + c2_c3 + c3_c4 + o1_c2'
    df_test_[fm_m].ix[2902]  # .iloc[0]
    model_[fm_m].params * df_test_[fm_m].ix[2902].T

    fm_m = 'c_c1 ~ c1_c2:o1_c2'
    df_test_[fm_m].ix[2902,0]*df_test_[fm_m].ix[2902,1]*model_[fm_m].params[1] + model_[fm_m].params[0]
      == yhat_test_[fm_m][0]

    df_test_[fm_m].ix[:,0]*df_test_[fm_m].ix[:,1]*model_[fm_m].params[1] + model_[fm_m].params[0]
      == yhat_test_[fm_m]

    y_true: df_test_3up_oup['c1_c2'] == df_test_[fm_m]['c1_c2']

      y_hat[0] = regr.params[0]*X[0,0] + regr.params[1]*X[0,1] + regr.params[2]*X[0,2] + regr.params[3]*X[0,3]
      y_hat    = regr.params[0]*X[:,regr.params[0]*X[:,0] + regr.params[1]*X[:,1] + regr.params[2]*X[:,2] + regr.params[3]*X[:,3]0] + regr.params[1]*X[:,1] + regr.params[2]*X[:,2] + regr.params[3]*X[:,3]
               == regr.predict()  ==  regr.predict(X)
    """


    def get_perf_rms_m(self, ytrue, yhat_m_, **meta):
        metric_rms_m_ = {}  # add meta on return this
        metric_rms_m_['meta'] = meta

        for fm_m in self.fm_:
            yhat_m = yhat_m_[fm_m]

            metric_rms_m_[fm_m] = Struct_dot(**deepcopy(self.d_threshpred_fd))

            #self.metric_rms_m_[fm_m].thresh_both[z] = np.sqrt( sum( (t-p)**2 for t,p in zip(ytrue_test, yhat_test) )/ytrue_test.shape[0] )
            #self.rms_train[fm_m].thresh_both[z] = np.sqrt( sum( (t-p)**2 for t,p in zip(ytrue_train, yhat_train) )/ytrue_train.shape[0] )
            for z, threshpred_z in enumerate(self.THRESHPRED_LST):
                N_both=0
                N_long=0
                N_shrt=0
                for ytrue_y, yhat_m_y in zip(ytrue, yhat_m):
                    if yhat_m_y >= threshpred_z or yhat_m_y <= -threshpred_z:
                        metric_rms_m_[fm_m].thresh_both[z] += (ytrue_y - yhat_m_y)**2
                        N_both += 1
                    if yhat_m_y >= threshpred_z:
                        metric_rms_m_[fm_m].thresh_long[z] += (ytrue_y - yhat_m_y)**2
                        N_long += 1
                    if yhat_m_y <= -threshpred_z:
                        metric_rms_m_[fm_m].thresh_shrt[z] += (ytrue_y - yhat_m_y)**2
                        N_shrt += 1
                if N_both == 0:
                    metric_rms_m_[fm_m].thresh_both[z] = None
                else:
                    metric_rms_m_[fm_m].thresh_both[z] = np.sqrt( metric_rms_m_[fm_m].thresh_both[z]/N_both )
                if N_long == 0:
                    metric_rms_m_[fm_m].thresh_long[z] = None
                else:
                    metric_rms_m_[fm_m].thresh_long[z] = np.sqrt( metric_rms_m_[fm_m].thresh_long[z]/N_long )
                if N_shrt == 0:
                    metric_rms_m_[fm_m].thresh_shrt[z] = None
                else:
                    metric_rms_m_[fm_m].thresh_shrt[z] = np.sqrt( metric_rms_m_[fm_m].thresh_shrt[z]/N_shrt )

        # Output
        if self.verbose >= 2:
            print("""
================================================================================
RMS
================================================================================
            """)
            print(metric_rms_m_['meta']['info'])
            for fm_m in self.fm_:
                threshpred_hdr=""
                stat_both=""
                stat_long=""
                stat_shrt=""
                for z, threshpred_z in enumerate(self.THRESHPRED_LST):

                    threshpred_hdr += "{:6.2f}    ".format(threshpred_z)

                    if metric_rms_m_[fm_m].thresh_both[z] is None:
                        stat_both += "{:>6}    ".format("---")
                    else:
                        stat_both += "{:6.2f}    ".format(metric_rms_m_[fm_m].thresh_both[z])
                    if metric_rms_m_[fm_m].thresh_long[z] is None:
                        stat_long += "{:>6}    ".format("---")
                    else:
                        stat_long += "{:6.2f}    ".format(metric_rms_m_[fm_m].thresh_long[z])
                    if metric_rms_m_[fm_m].thresh_shrt[z] is None:
                        stat_shrt += "{:>6}    ".format("---")
                    else:
                        stat_shrt += "{:6.2f}    ".format(metric_rms_m_[fm_m].thresh_shrt[z])

                print('\n' + fm_m + '\n')
                print("Thresh Pred  ", threshpred_hdr)
                print("-"*(len(threshpred_hdr) + len("Thresh Pred  ")))
                print(metric_rms_m_['meta']['partition'].capitalize(), "both  :", stat_both)
                print(metric_rms_m_['meta']['partition'].capitalize(), "long  :", stat_long)
                print(metric_rms_m_['meta']['partition'].capitalize(), "shrt  :", stat_shrt)
                print("-"*(len(threshpred_hdr) + len("Thresh Pred  ")))
            print('\n')

        return metric_rms_m_


    def get_performance(self, ytrue, yhat_m_, **meta):
        #ytrue = df_seg_par_k[self.DATA_YTRUE_NAME]
        #ytrue = self.df_test_3up_oup['c_c1']

        metric = {}
        metric['rms'] = self.get_perf_rms_m(ytrue, yhat_m_, **meta)
        """
        print("\n--------------------------------------------------------------------------------\n")
        fm_m = 'c_c1 ~ c1_c2 + c2_c3 + c3_c4 + o1_c2'
        print(fm_m + '\n')
        print('Seg:', self.seg_name)
        N_pred_nothresh_both=0
        N_pred_nothresh_correct_both=0
        N_pred_nothresh_correct_shrt=0
        N_true_shrt=0

        ytrue = df_.iloc[:, 0]
        ypred = yhat_[fm_m]

        print(" ypred      ytrue")
        for i in range(len(ypred)):
            print("{0:6.2f}  :  {1:6.2f}".format(ypred[i], ytrue.iloc[i]))
            N_pred_nothresh_both += 1
            if (ytrue.iloc[i] <= 0):
                N_true_shrt += 1
            if (ypred[i] <=0 and ytrue.iloc[i] <= 0):
                N_pred_nothresh_correct_shrt += 1
            if (ypred[i] <=0 and ytrue.iloc[i] <= 0) or (ypred[i] >=0 and ytrue.iloc[i] >= 0):
                N_pred_nothresh_correct_both += 1

        print("\nPct correct both :  {0:7.2}".format(N_pred_nothresh_correct_both/N_pred_nothresh_both))
        print("Pct correct shrt :  {0:7.2}\n".format(N_pred_nothresh_correct_shrt/N_true_shrt))
        print("Pct dn           :  {0:7.2}\n".format(N_true_shrt/N_pred_nothresh_both))

        print("\n--------------------------------------------------------------------------------\n")
        """
        metric_m_ = {}
        metric['perf'] = metric_m_

        na_str = "---"   #"{0:>6}".format('---')
        l_fd  = [0.0 for _ in self.THRESHPRED_LST]
        l_str = [na_str for _ in self.THRESHPRED_LST]
        l_None = [None for _ in self.THRESHPRED_LST]

        d_threshpred_fd = { 'thresh_both':l_fd.copy(), 'thresh_both_str':l_str.copy(),
                         'thresh_long':l_fd.copy(), 'thresh_long_str':l_str.copy(),
                         'thresh_shrt':l_fd.copy(), 'thresh_shrt_str':l_str.copy()
                       }
        d_threshpred_None = { 'thresh_both':l_None.copy(), 'thresh_both_str':l_str.copy(),
                         'thresh_long':l_None.copy(), 'thresh_long_str':l_str.copy(),
                         'thresh_shrt':l_None.copy(), 'thresh_shrt_str':l_str.copy()
                       }

        for fm_m in self.fm_:
            yhat_m = yhat_m_[fm_m]

            metric_m_[fm_m] = {}
            metric_m_[fm_m]['N_trd'] = Struct_dot(**deepcopy(d_threshpred_fd))
            metric_m_[fm_m]['pctcorrect'] = Struct_dot(**deepcopy(d_threshpred_None))
            metric_m_[fm_m]['expectgain'] = Struct_dot(**deepcopy(d_threshpred_fd))
            metric_m_[fm_m]['expectgain_pertrd'] = Struct_dot(**deepcopy(d_threshpred_None))
            # expectgain_pertrd_str = Struct_dot(**d_threshcoeff2)

            for z, threshpred_z in enumerate(self.THRESHPRED_LST):
                # print("Prediction Threshold: ", threshpred_z, '\n')
                N_trd_both_correct_z=0
                N_trd_long_correct_z=0
                N_trd_shrt_correct_z=0
                for ytrue_y, yhat_m_y in zip(ytrue, yhat_m):
                    """ both """
                    if yhat_m_y <= -threshpred_z or yhat_m_y >= threshpred_z:    # just to be super clear what we are doing in for block
                        metric_m_[fm_m]['N_trd'].thresh_both[z] += 1
                        if yhat_m_y <= -threshpred_z:
                            metric_m_[fm_m]['expectgain'].thresh_both[z] += ( -ytrue_y )
                        else:
                            metric_m_[fm_m]['expectgain'].thresh_both[z] += ( ytrue_y )

                        if (yhat_m_y <= 0 and ytrue_y <= 0) or (yhat_m_y >= 0 and ytrue_y >= 0):
                            N_trd_both_correct_z += 1

                    """ long """
                    if yhat_m_y >= threshpred_z:
                        metric_m_[fm_m]['N_trd'].thresh_long[z] += 1
                        metric_m_[fm_m]['expectgain'].thresh_long[z] += ( ytrue_y )
                        if (yhat_m_y >=0 and ytrue_y >= 0):
                            N_trd_long_correct_z += 1

                    """ shrt """
                    if yhat_m_y <= -threshpred_z:
                        metric_m_[fm_m]['N_trd'].thresh_shrt[z] += 1
                        metric_m_[fm_m]['expectgain'].thresh_shrt[z] += ( -ytrue_y )
                        if (yhat_m_y <=0 and ytrue_y <= 0):
                            N_trd_shrt_correct_z += 1

                fdformat = "{0:6.2f}"
                if metric_m_[fm_m]['N_trd'].thresh_both[z] > 0:
                    metric_m_[fm_m]['pctcorrect'].thresh_both[z] = N_trd_both_correct_z / metric_m_[fm_m]['N_trd'].thresh_both[z]
                    metric_m_[fm_m]['pctcorrect'].thresh_both_str[z] = fdformat.format(metric_m_[fm_m]['pctcorrect'].thresh_both[z])
                    metric_m_[fm_m]['expectgain_pertrd'].thresh_both[z] = metric_m_[fm_m]['expectgain'].thresh_both[z] / metric_m_[fm_m]['N_trd'].thresh_both[z]
                    metric_m_[fm_m]['expectgain_pertrd'].thresh_both_str[z] = fdformat.format(metric_m_[fm_m]['expectgain_pertrd'].thresh_both[z])

                if metric_m_[fm_m]['N_trd'].thresh_long[z] > 0:
                    metric_m_[fm_m]['pctcorrect'].thresh_long[z] = N_trd_long_correct_z / metric_m_[fm_m]['N_trd'].thresh_long[z]
                    metric_m_[fm_m]['pctcorrect'].thresh_long_str[z] = fdformat.format(metric_m_[fm_m]['pctcorrect'].thresh_long[z])
                    metric_m_[fm_m]['expectgain_pertrd'].thresh_long[z] = metric_m_[fm_m]['expectgain'].thresh_long[z] / metric_m_[fm_m]['N_trd'].thresh_long[z]
                    metric_m_[fm_m]['expectgain_pertrd'].thresh_long_str[z] = fdformat.format(metric_m_[fm_m]['expectgain_pertrd'].thresh_long[z])

                if metric_m_[fm_m]['N_trd'].thresh_shrt[z] > 0:
                    metric_m_[fm_m]['pctcorrect'].thresh_shrt[z] = N_trd_shrt_correct_z / metric_m_[fm_m]['N_trd'].thresh_shrt[z]
                    metric_m_[fm_m]['pctcorrect'].thresh_shrt_str[z] = fdformat.format(metric_m_[fm_m]['pctcorrect'].thresh_shrt[z])
                    metric_m_[fm_m]['expectgain_pertrd'].thresh_shrt[z] = metric_m_[fm_m]['expectgain'].thresh_shrt[z] / metric_m_[fm_m]['N_trd'].thresh_shrt[z]
                    metric_m_[fm_m]['expectgain_pertrd'].thresh_shrt_str[z] = fdformat.format(metric_m_[fm_m]['expectgain_pertrd'].thresh_shrt[z])

        # Output
        if self.verbose >= 2:
            print("""
================================================================================
Performance Metrics - for all models - for a given seg, k, and partition
================================================================================
        """)
            print(meta['info'])
            print("Partition:", meta['partition'])

            for fm_m in self.fm_:
                print("\n--------------------------------------------------------------------------------\n")
                print("Model:", fm_m, "     Partition:", meta['partition'])

                if self.verbose >= 3:
                    print("ypred       ytrue")
                    for y in range(len(yhat_m)):
                        print("{0:6.2f}  :  {1:6.2f}".format(yhat_m[y], ytrue.iloc[i]))
                print()

                threshpred_hdr = ""
                line_N_trd = {"both":"", "long":"", "shrt":""}
                line_pctcorrect = {"both":"", "long":"", "shrt":""}
                line_expectgain_pertrd = {"both":"", "long":"", "shrt":""}
                for z, threshpred_z in enumerate(self.THRESHPRED_LST):

                    threshpred_hdr += "{:>6.2f}    ".format(threshpred_z)

                    line_N_trd["both"] += "{:>6.0f}    ".format(metric_m_[fm_m]['N_trd'].thresh_both[z])
                    line_N_trd["long"] += "{:>6.0f}    ".format(metric_m_[fm_m]['N_trd'].thresh_long[z])
                    line_N_trd["shrt"] += "{:>6.0f}    ".format(metric_m_[fm_m]['N_trd'].thresh_shrt[z])

                    line_pctcorrect["both"] += "{:>6}    ".format(metric_m_[fm_m]['pctcorrect'].thresh_both_str[z])
                    line_pctcorrect["long"] += "{:>6}    ".format(metric_m_[fm_m]['pctcorrect'].thresh_long_str[z])
                    line_pctcorrect["shrt"] += "{:>6}    ".format(metric_m_[fm_m]['pctcorrect'].thresh_shrt_str[z])

                    line_expectgain_pertrd["both"] += "{:>6}    ".format(metric_m_[fm_m]['expectgain_pertrd'].thresh_both_str[z])
                    line_expectgain_pertrd["long"] += "{:>6}    ".format(metric_m_[fm_m]['expectgain_pertrd'].thresh_long_str[z])
                    line_expectgain_pertrd["shrt"] += "{:>6}    ".format(metric_m_[fm_m]['expectgain_pertrd'].thresh_shrt_str[z])

                print("Thresh Pred           ", threshpred_hdr)
                print("-"*(len(threshpred_hdr) + len("Thresh Pred        ")))
                print("N both             :  ", line_N_trd["both"])
                print("N long             :  ", line_N_trd["long"])
                print("N shrt             :  ", line_N_trd["shrt"])
                print("Pct correct both   :  ", line_pctcorrect["both"])
                print("Pct correct long   :  ", line_pctcorrect["long"])
                print("Pct correct shrt   :  ", line_pctcorrect["shrt"])
                print("Expectgain/trd both:  ", line_expectgain_pertrd["both"])
                print("Expectgain/trd long:  ", line_expectgain_pertrd["long"])
                print("Expectgain/trd shrt:  ", line_expectgain_pertrd["shrt"])
                print("-"*(len(threshpred_hdr) + len("Thresh Pred        ")))

            print("\n")

        return metric

"""
================================================================================
p stats_instr_class.py -segment 3up_oup -verbose 3

p stats_instr_class.py -segment all  > stats_instr_class_all.txt
p stats_instr_class.py -segment 3up_oup  > stats_instr_class_3up_oup.txt


"""
if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-segment', type=str, required=True)
    parser.add_argument('-infile', type=argparse.FileType('r'), help='input file, in CSV format')
    parser.add_argument('-verbose')

    args = parser.parse_args()

    prediction = Prediction()
    #prediction.seg_name = args.segment

    if args.infile:    # self.FIN_NAME is default
        if not Prediction.checkfile(args.infile):
            print('Input file not found:', args.infile)
            sys.exit()
        self.FIN_NAME = args.infile

    if args.verbose:
        prediction.verbose = int(args.verbose)

    prediction.go_segment_kfold(args.segment)
