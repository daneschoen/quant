
"""
==================================================================================
Correlation
==================================================================================
"""
import os

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from sklearn import linear_model

import matplotlib.pyplot as plt

from flask_apps.stats import *
from flask_apps.globals import *

"""
----------------------------------------------------------------------------------
Cross-Correlation - numpy
----------------------------------------------------------------------------------
"""
a = np.array([12.0, 2.0, 5.0, 8.0])
b = np.array([13.0, 3.0, 5.0, 6.0])
c = np.array([-12.0, -2.0, -5.0, -8.0])

m = np.row_stack((a,b,c))

crosscorr = np.corrcoef(a,b)    # Pearson Pearson product-moment correlation coefficients matrix
crosscorr = np.corrcoef(m)
crosscorr = np.corrcoef((a,b,c))
# [[ 1.        ,  0.94634059, -1.        ],
#  [ 0.94634059,  1.        , -0.94634059],
#  [-1.        , -0.94634059,  1.        ]])

                                 cov(A,B)                     cov(A,B)
Correlation coefficient = -------------------------- = -------------------------- 
                           sqrt[ cov(A,A)*cov(A,A) ]     sqrt[ var(A) * var(B) ]

np.correlate(a,b)

if normalize:
    a = (a - mean(a)) / (std(a) * len(a))
    v = (v - mean(v)) /  std(v)
