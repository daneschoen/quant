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

FIN_PATH = ''
FIN_PATHNAME = os.path.join(FIN_PATH, FIN_NAME)

CHART_PATH = "/static/images/"

DATA_DT_COL = 0
DATA_TIME_COL = 0
DATA_DTIME_COL = 0
DATA_YTRUE_COL = 0
DATA_YTRUE_NAME = 'std_2_dev'

# [3391 rows x 7 columns]  13 years = 2003 - 2016-quarter
# N_NOSEG = 5000
# N_Seg = 500  based on this:
KFOLDPARTITION_TYPE = "nooverlap"   # overlap
CV_TRAIN = 425    # 10 yr *250 = 2500 but seg...

CV_VALID = 50      # 2 yr       : 500
CV_TEST = 30
K_FOLD = 10
K_FOLD_FWD = 80

THRESHPRED_LST = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
THRESH_SUM_C = 0.0

VERBOSE = 2

# ------------------------------------------------------------------------------

class Struct_dot:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class Prediction:

    def __init__(self, seg_name=None):
        self.verbose = VERBOSE    # 0: None ,1: Minimum, eg files imported ok ,2: Normal, 3: yhat, ytrue
        self.savefiles = False

        self.seg_name = seg_name

        self.FIN_NAME = FIN_NAME
        # Index(['std_2_dev', '4_std_3_dev', 'o1_c1', 'o2_c3', 'std_dev', 'std_dev', 'std_3_dev'], dtype='object')
        self.FIN_PATH = FIN_PATH
        self.FIN_PATHNAME = os.path.join(FIN_PATH, FIN_NAME)

        self.CHART_PATH = CHART_PATH

        self.DATA_DT_COL = DATA_DT_COL   # 0
        self.DATA_TIME_COL = DATA_TIME_COL   # 0
        self.DATA_DTIME_COL = DATA_DTIME_COL   # 0
        self.DATA_YTRUE_COL = DATA_YTRUE_COL     # 0
        self.DATA_YTRUE_NAME = DATA_YTRUE_NAME   # 'std_2_dev'

        # N_Seg ~ 500
        self.kfoldpartition_type = KFOLDPARTITION_TYPE
        self.CV_TRAIN = CV_TRAIN         # 425   # 10 yr *250 = 2500 but seg...
        self.CV_VALID = CV_VALID         #  50   # 500: 2 yr ...
        self.CV_TEST = CV_TEST           #  25   # 250
        self.K_FOLD = K_FOLD             #  10   # 50
        self.K_FOLD_FWD = K_FOLD_FWD     #  10   no overlaps

        self.do_train_performance = False
        self.remove_minmax = True
        self.train_sizevar = False
        self.segment_post = False
        self.test_usevalid = False

        self.THRESHSEGMENT_LST = [0]           # THRESHSEGMENT_LST
        self.THRESHPRED_LST = THRESHPRED_LST   # [0.5, 0.6, 0.7, 0.8, 1.0]
        self.THRESH_SUM_C = THRESH_SUM_C

        l_fd = [0.0 for x in self.THRESHPRED_LST]
        self.d_threshpred_fd = {
            'thresh_both':l_fd.copy(), 'thresh_long':l_fd.copy(), 'thresh_shrt':l_fd.copy()
        }


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
            o1_c1 and std_medis 0.8, so DONT want both in same X
            """


    def segment_data(self):
        thresh_seg = self.THRESHSEGMENT_LST[-1]
        df = self.df
        df_seg_ = {}

        #df_train_seg_ = {}
        #df_test_seg_ = {}

        #df_train_3up = df_train[(df_train.std_med>= 0) & (df_train.std_dev >= 0) & (df_train.std_3_dev >= 0)].loc[:,['std_2_dev', 'std_dev', 'std_dev', 'std_3_dev']]
        #df_test_3up = df_test[(df_test.std_med>= 0) & (df_test.std_dev >= 0) & (df_test.std_3_dev >= 0)].loc[:,['std_2_dev', 'std_dev', 'std_dev', 'std_3_dev']]

        df_seg_['all'] = df
        df_seg_['std'] = df[ (df.std_med>= thresh_seg) & (df.std_dev >= thresh_seg) & (df.std_3_dev >= thresh_seg) ]
        df_seg_['std'] = df[ (df.std_med<= thresh_seg) & (df.std_dev <= thresh_seg) & (df.std_3_dev <= thresh_seg) ]
        df_seg_['std_oup'] = df[ (df.std_med>= thresh_seg) & (df.std_dev >= thresh_seg) & (df.std_3_dev >= thresh_seg)
                                 & (df.4_std_3_dev >= thresh_seg)
                                 #& (df_train.std_med+ df_train.std_dev + df_train.std_3_dev >= THRESH_SUM_C)
                               ]
        df_seg_['std_odn'] = df[ (df.std_med>= thresh_seg) & (df.std_dev >= thresh_seg) & (df.std_3_dev >= thresh_seg)
                                 & (df.4_std_3_dev <= thresh_seg)
                               ]
        df_seg_['std_odn'] = df[ (df.std_med<= thresh_seg) & (df.std_dev <= thresh_seg) & (df.std_3_dev <= thresh_seg)
                                & (df.4_std_3_dev <= thresh_seg)
                               ]
        df_seg_['std_oup'] = df[ (df.std_med<= thresh_seg) & (df.std_dev <= thresh_seg) & (df.std_3_dev <= thresh_seg)
                                 & (df.4_std_3_dev >= thresh_seg)
                               ]
        self.df_seg_ = df_seg_


    def split_kfold_partition(self, alg, train_sizevar, N_Seg, K_Fold, K_FoldFwd, N_Valid, N_Test, N_Train):
        # self.CV_VALID = 50      # 2 yr       : 500
        # self.CV_TEST = 25
        # self.K_FOLD = 10
        # self.K_FOLD_FWD = 10
        # self.CV_TRAIN = None

        d_RVT = {
            'train':None, 'valid':None, 'test':None
        }
        Struct_dot(**deepcopy(d_RVT))
        kfold_rvt = [Struct_dot(**deepcopy(d_RVT)) for _ in range(K_Fold)]

        if alg == "overlap":
            N_Train = N_Seg - ( N_Valid + N_Test + K_FoldFwd*(K_Fold-1) )
            for k in range(K_Fold):
                r_beg, r_end = K_FoldFwd*k, K_FoldFwd*k + N_Train
                v_beg, v_end = r_end, r_end + N_Valid
                t_beg, t_end = v_end, v_end + N_Test
                kfold_rvt[k].train = (r_beg, r_end)
                if train_sizevar:
                    kfold_rvt[k].train = (0, r_end)
                kfold_rvt[k].valid = (v_beg, v_end)
                kfold_rvt[k].test  = (t_beg, t_end)

        elif alg == "nooverlap":
            N_Train = int( (N_Seg - K_Fold*( N_Valid + N_Test))/K_Fold )
            for k in range(K_Fold):
                r_beg, r_end = k*N_Train + k*N_Valid + k*N_Test, (k+1)*N_Train + k*N_Valid + k*N_Test
                v_beg, v_end = (k+1)*N_Train + k*N_Valid + k*N_Test, (k+1)*N_Train + (k+1)*N_Valid + k*N_Test
                t_beg, t_end = (k+1)*N_Train + (k+1)*N_Valid + k*N_Test, (k+1)*N_Train + (k+1)*N_Valid + (k+1)*N_Test
                kfold_rvt[k].train = (r_beg, r_end)
                if train_sizevar:
                    kfold_rvt[k].train = (0, r_end)
                kfold_rvt[k].valid = (v_beg, v_end)
                kfold_rvt[k].test  = (t_beg, t_end)

        if self.verbose >= 2:
            print("\n-------------------------")
            print("Split kfold and partition")
            print("-------------------------")
            print("K_FOLD     :", K_Fold)
            print("K_FOLD_FWD :", K_FoldFwd)
            print("TRAIN : {0:14}     VALID: {1:<5} TEST: {2:<5}".format(
              N_Train, N_Valid, N_Test
            ))

            for k in range(K_Fold):
                print("  {0:<2} of {1:<4}   {2:10}  {3:10}   {4:10}".format(
                  k, K_Fold, str(kfold_rvt[k].train), str(kfold_rvt[k].valid), str(kfold_rvt[k].test)
                ))
            print()

        return N_Train, kfold_rvt


    def crossvalidate_kfold(self):

        self.metric_seg_k_ = []

        # self.CV_VALID = 50      # 2 yr       : 500
        # self.CV_TEST = 25
        # self.K_FOLD = 10
        # self.K_FOLD_FWD = 10
        # self.CV_TRAIN = None =

        self.CV_TRAIN, self.kfold_rvt = self.split_kfold_partition(self.kfoldpartition_type, self.train_sizevar,
                                        self.N_Seg, self.K_FOLD, self.K_FOLD_FWD, self.CV_VALID, self.CV_TEST, self.CV_TRAIN)

        for k, k_rvt in enumerate(self.kfold_rvt):
            r_beg, r_end = k_rvt.train
            v_beg, v_end = k_rvt.valid
            t_beg, t_end = k_rvt.test

            info_seg_k  = '{0:<22} {1:<}'.format( 'k: ' + str(k) + ' of KFold: ' + str(self.K_FOLD), 'KFold_fwd: ' + str(self.K_FOLD_FWD) ) + '\n'
            info_seg_k += '{0:<22} {1:<}'.format( 'seg_name: ' + self.seg_name, 'df_seg.shape: ' + str(self.df_seg.shape) ) + '\n'
            info_seg_k += '{0:<22} {1:<}'.format( 'train, valid, test: ', str((r_beg, r_end)) + ' , ' + str((v_beg, v_end))  + ' , ' + str((t_beg, t_end)) )

            if self.verbose >= 1:
                print(info_seg_k)

            df_train_seg_k = self.df_seg.iloc[r_beg:r_end, :]  # = self.df_seg.iloc[0:r_end, :]
            df_valid_seg_k = self.df_seg.iloc[v_beg:v_end, :]
            df_test_seg_k  = self.df_seg.iloc[t_beg:t_end, :]
            #self.df_train = self.df.iloc[:-self.CV_VALID]
            #self.df_test = self.df.iloc[-self.CV_VALID:]

            # Remove min, max
            if self.remove_minmax:
                df_train_seg_k = df_train_seg_k.loc[df_train_seg_k[self.DATA_YTRUE_NAME]!=df_train_seg_k[self.DATA_YTRUE_NAME].max()]
                df_train_seg_k = df_train_seg_k.loc[df_train_seg_k[self.DATA_YTRUE_NAME]!=df_train_seg_k[self.DATA_YTRUE_NAME].min()]

            # Can use this to model + predict test instead of  model_k_train = self.get_models(df_train_seg_k)
            df_train_valid_seg_k = pd.concat([df_train_seg_k, df_valid_seg_k], axis=0)

            model_k_train = self.get_models(df_train_seg_k)
            #model_k_train_valid = self.get_models(df_valid_seg_k)
            model_k_train_valid = self.get_models(df_train_valid_seg_k)
            #model_k_train_valid = self.get_models(df_seg.iloc[r_beg:v_end, :])
            #model_k_train_valid = self.get_models(df_seg.iloc[0:v_end, :])

            if self.do_train_performance:
                yhat_train_seg_k_m_ = self.get_pred_models(model_k_train, df_train_seg_k)
            yhat_valid_seg_k_m_ = self.get_pred_models(model_k_train, df_valid_seg_k)
            if self.test_usevalid:
                yhat_test_seg_k_m_ = self.get_pred_models(model_k_train_valid, df_test_seg_k)
            else:
                yhat_test_seg_k_m_ = self.get_pred_models(model_k_train, df_test_seg_k)

            metric_seg_k = {}

            if self.do_train_performance:
                ytrue_seg_train_k = df_train_seg_k[self.DATA_YTRUE_NAME]
                meta = {'info': info_seg_k}
                meta['partition'] = 'TRAIN'
                metric_seg_k['train'] = self.get_performance(ytrue_seg_train_k, yhat_train_seg_k_m_, df_train_seg_k, **meta)

            ytrue_seg_valid_k = df_valid_seg_k[self.DATA_YTRUE_NAME]
            meta = {'info': info_seg_k}
            meta['partition'] = 'VALID'
            metric_seg_k['valid'] = self.get_performance(ytrue_seg_valid_k, yhat_valid_seg_k_m_, df_valid_seg_k, **meta)

            ytrue_seg_test_k = df_test_seg_k[self.DATA_YTRUE_NAME]
            meta = {'info': info_seg_k}
            meta['partition'] = 'TEST'
            metric_seg_k['test']  = self.get_performance(ytrue_seg_test_k, yhat_test_seg_k_m_, df_test_seg_k, **meta)

            self.metric_seg_k_.append(metric_seg_k)

        self.model_selected = self.select_model()
        if self.verbose >= 1:
            print("Model Selected: ", self.model_selected)



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
        self.fm_.append("std_2_dev ~ std_med+ std_dev + std_3_dev")  # Adj. R-squared: 0.073
        self.fmX_.append(['std_dev', 'std_dev', 'std_3_dev'])

        self.fm_.append("std_2_dev ~ std_med+ std_dev + std_3_dev + 4_std_3_dev")  # Adj. R-squared: 0.073
        self.fmX_.append(['std_dev', 'std_dev', 'std_3_dev', '4_std_3_dev'])

        self.fm_.append("std_2_dev ~ std_med+ std_dev + std_3_dev + 4_std_3_dev:4_std_3_dev")    # Adj. R-squared:
        self.fmX_.append(['std_dev', 'std_dev', 'std_3_dev', '4_std_3_dev'])

        self.fm_.append("std_2_dev ~ std_dev:4_std_3_dev + std_dev:std_3_dev")    # Adj. R-squared: 0.082
        self.fmX_.append(['std_dev', 'std_dev', 'std_3_dev', '4_std_3_dev'])
        self.fm_.append("std_2_dev ~ std_dev:std_dev + 4_std_3_dev:std_3_dev")    # Adj. R-squared:
        self.fmX_.append(['std_dev', 'std_dev', 'std_3_dev', '4_std_3_dev'])
        self.fm_.append("std_2_dev ~ std_dev:std_3_dev + std_dev:4_std_3_dev")    # Adj. R-squared:
        self.fmX_.append(['std_dev', 'std_dev', 'std_3_dev', '4_std_3_dev'])

        self.fm_.append("std_2_dev ~ std_med+ std_dev:std_3_dev")
        self.fmX_.append(['std_dev', 'std_dev', 'std_3_dev'])

        self.fm_.append("std_2_dev ~ std_med+ 4_std_3_dev")    # Adj. R-squared: 0.081
        self.fmX_.append(['std_dev', '4_std_3_dev'])
        self.fm_.append("std_2_dev ~ std_dev*4_std_3_dev")
        self.fmX_.append(['std_dev', '4_std_3_dev'])

        self.fm_.append("std_2_dev ~ std_med+ std_dev")    # Adj. R-squared: 0.081
        self.fmX_.append(['std_dev', 'std_dev'])
        self.fm_.append("std_2_dev ~ std_dev:std_dev")      # Adj. R-squared: 0.183
        self.fmX_.append(['std_dev', '4_std_3_dev'])

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

    """
    ============================================================================
    Out of sample prediction
    ============================================================================

    x_test = np.linspace(0, CV_VALID-1, CV_VALID)
    #Xnew = np.column_stack((x1n, np.sin(x1n), (x1n-5)**2))
    #Xnew = sm.add_constant(Xnew)
    #yhat_outsample = model.predict(Xnew)        # predict out of sample

    # yhat_outsample = model.predict(X[-10:,:])   # predict out of sample

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
        for fm_m in self.fm_:
            #X_m = sm.add_constant(df_outsample_[fm_m])
            X_m = sm.add_constant(df_outsample)
            yhat_outsample_m_[fm_m] = model_[fm_m].predict(X_m)

            if self.verbose >= 3:
                print("--------------------------------------------")
                print("Calc yhat for: ", fm_m, '\n')
                print(df_outsample)
                print()
                print(yhat_outsample_m_[fm_m])
                print("--------------------------------------------\n")

        return yhat_outsample_m_

    """
    Verify predict: y ~ model.params*X

    df_test_[fm_m].ix[2902]  # .iloc[0]
    model_[fm_m].params * df_test_[fm_m].ix[2902].T

    df_test_[fm_m].ix[2902,0]*df_test_[fm_m].ix[2902,1]*model_[fm_m].params[1] + model_[fm_m].params[0]
      == yhat_test_[fm_m][0]

    df_test_[fm_m].ix[:,0]*df_test_[fm_m].ix[:,1]*model_[fm_m].params[1] + model_[fm_m].params[0]
      == yhat_test_[fm_m]

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


    def get_performance(self, ytrue, yhat_m_, df, **meta):
        #ytrue = df_seg_par_k[self.DATA_YTRUE_NAME]
        #ytrue = self.df_test_3up_oup['std_2_dev']

        metric = {}
        # metric['rms'] = self.get_perf_rms_m(ytrue, yhat_m_, **meta)
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
            metric_m_[fm_m]['ytru_pct_long'] = 0
            metric_m_[fm_m]['yhat_pct_long'] = 0
            metric_m_[fm_m]['apri_expect_long'] = 0
            metric_m_[fm_m]['apri_expect_long_pertrd'] = 0
            metric_m_[fm_m]['yhat_expect_long'] = 0
            metric_m_[fm_m]['yhat_expect_long_pertrd'] = 0
            metric_m_[fm_m]['yhat_expect_shrt'] = 0
            metric_m_[fm_m]['yhat_expect_shrt_pertrd'] = 0

            N_yhat_long=0
            N_yhat_shrt=0
            for y, (ytrue_y, yhat_m_y) in enumerate(zip(ytrue, yhat_m)):
                if ytrue_y >= 0:
                    metric_m_[fm_m]['ytru_pct_long'] +=1
                if yhat_m_y >= 0:
                    N_yhat_long += 1
                    metric_m_[fm_m]['yhat_pct_long'] +=1
                    metric_m_[fm_m]['yhat_expect_long'] += (ytrue_y)
                if yhat_m_y <= 0:
                    N_yhat_shrt += 1
                    metric_m_[fm_m]['yhat_expect_shrt'] += (-ytrue_y)

                metric_m_[fm_m]['apri_expect_long'] += ytrue_y

            metric_m_[fm_m]['ytru_pct_long'] /= ytrue.shape[0]
            metric_m_[fm_m]['yhat_pct_long'] /= ytrue.shape[0]
            metric_m_[fm_m]['apri_expect_long_pertrd'] = metric_m_[fm_m]['apri_expect_long'] / ytrue.shape[0]
            metric_m_[fm_m]['yhat_expect_long_pertrd'] = metric_m_[fm_m]['yhat_expect_long'] / N_yhat_long
            metric_m_[fm_m]['yhat_expect_shrt_pertrd'] = metric_m_[fm_m]['yhat_expect_shrt'] / N_yhat_shrt

            for z, threshpred_z in enumerate(self.THRESHPRED_LST):
                # print("Prediction Threshold: ", threshpred_z, '\n')
                N_trd_both_correct_z=0
                N_trd_long_correct_z=0
                N_trd_shrt_correct_z=0

                #print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                #print(ytrue.shape, yhat_m.shape, df.shape)
                for y, (ytrue_y, yhat_m_y) in enumerate(zip(ytrue, yhat_m)):
                    """ both """
                    if not self.segment_post or ( self.segment_post and
                        (df.iloc[y]['std_dev'] >= 0.0 and df.iloc[y]['std_dev'] >= 0.0 and df.iloc[y]['std_3_dev'] >= 0.0) ) :

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
                print("Model:", fm_m)
                print(meta['info'])
                print("Partition:", meta['partition'])
                print()

                print('                   {0:>9}  {1:>9}'.format('ytru','yhat'))
                print('pct_long        :  {0:>9.2f}  {1:>9.2f}'.format(metric_m_[fm_m]['ytru_pct_long'], metric_m_[fm_m]['yhat_pct_long']))
                print('expect_long     :  {0:>9.2f}  {1:>9.2f}'.format(metric_m_[fm_m]['apri_expect_long'], metric_m_[fm_m]['yhat_expect_long']))
                print('expect_long/trd :  {0:>9.2f}  {1:>9.2f}'.format(metric_m_[fm_m]['apri_expect_long_pertrd'], metric_m_[fm_m]['yhat_expect_long_pertrd']))
                print('expect_shrt     :  {0:>9}  {1:>9.2f}'.format('---', metric_m_[fm_m]['yhat_expect_shrt']))
                print('expect_shrt/trd :  {0:>9}  {1:>9.2f}'.format('---', metric_m_[fm_m]['yhat_expect_shrt_pertrd']))

                if self.verbose >= 3:
                    print("\n ytrue       yhat")
                    for y, (ytrue_y, yhat_m_y) in enumerate(zip(ytrue, yhat_m_[fm_m])):
                        print("{0:6.2f}  :  {1:6.2f}".format(ytrue_y, yhat_m_y))
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


    # --------------------------------------------------------------------------

    def go_segment_kfold(self, seg_name):
        self.import_data_pandas()
        self.segment_data()

        if seg_name not in self.df_seg_:
            raise RuntimeError('Segmentation name not in df_seg_:', self.df_seg_.keys())
        self.seg_name = seg_name

        self.df_seg = self.df_seg_[self.seg_name]
        self.N_Seg = self.df_seg.shape[0]    # 392
        if self.verbose >= 1:
            print("\n================================================================================\n")
            print("Segment   :", self.seg_name, "     df_seg.shape:", self.df_seg.shape)
            print("self.kfoldpartition_type:", self.kfoldpartition_type)
            print("self.remove_minmax:", self.remove_minmax)
            print("self.train_sizevar:", self.train_sizevar)
            print("self.segment_post:", self.segment_post)
            print("self.test_usevalid:", self.test_usevalid)

        # self.CV_VALID = 50      # 2 yr       : 500
        # self.CV_TEST = 25
        # self.K_FOLD = 10
        # self.K_FOLD_FWD = 10
        # self.CV_TRAIN = None

        self.crossvalidate_kfold()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--segment', type=str, required=True)
    parser.add_argument('--infile', type=argparse.FileType('r'), help='input file, in CSV format')
    parser.add_argument('-v', '--verbose', type=int, default=2)
    parser.add_argument('--segment_post', action='store_true', default=False)
    parser.add_argument('--test_usevalid', action='store_true', default=False)
    parser.add_argument('--train_sizevar', action='store_true', default=False)
    parser.add_argument('--kfold', nargs=6)

    args = parser.parse_args()

    pred = Prediction()
    #prediction.seg_name = args.segment

    if args.infile:    # self.FIN_NAME is default
        if not Prediction.checkfile(args.infile):
            print('Input file not found:', args.infile)
            sys.exit()
        self.FIN_NAME = args.infile

    pred.verbose = args.verbose

    pred.segment_post = args.segment_post
    pred.test_usevalid = args.test_usevalid
    pred.train_sizevar = args.train_sizevar

    # -kfold nooverlap 4 None None 27 25
    if args.kfold:
        pred.kfoldpartition_type = args.kfold[0]
        pred.K_FOLD = None
        if args.kfold[1] != "None":
            pred.K_FOLD = int(args.kfold[1])
        pred.K_FOLD_FWD = None
        if args.kfold[2] != "None":
            pred.K_FOLD_FWD = int(args.kfold[2])
        pred.CV_TRAIN = None
        if args.kfold[3] != "None":
            pred.CV_TRAIN = int(args.kfold[3])
        pred.CV_VALID = None
        if args.kfold[4] != "None":
            pred.CV_VALID = int(args.kfold[4])
        pred.CV_TEST = None
        if args.kfold[5] != "None":
            pred.CV_TEST = int(args.kfold[5])

    pred.go_segment_kfold(args.segment)
