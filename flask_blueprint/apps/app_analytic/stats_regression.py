
"""
You can get the prediction in statsmodels in a very similar way as in
scikit-learn, except that we use the results instance returned by fit
predictions = results.predict(X_test)

Given the predictions, we can calculate statistics that are based on the
prediction error

prediction_error = y_test - predictions

"""

"""
================================================================================
Linear regression - statsmodels
================================================================================
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

# Ex 0/ statsmodels ols
def regr_ols_sm(y, x):
    Y = x
    X = np.array(x).T
    X = sm.add_constant(X)  # need y-intercept so add column of 1's
    model = sm.OLS(endog=Y, exog=X)
    results = model.fit()
    return results
    """
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(y, X).fit()
    return results
    """

# Ex 0A/
yx = [[0.0, -6.75, -30.5, -21.25, 25.0, 34.25, -19.25, -12.5, -6.5, -7.75, -19.5, 24.5, -4.75, 8.25, 10.5, 29.25, -13.0, 10.0, -24.5, -37.5, 27.5, -27.75, 25.5, 24.75, -11.0, 24.75, -1.75, -11.0, 19.75, 3.75, 18.5, 8.5, -7.75, 10.5, -0.25, -0.25, 12.25, -0.75, 7.0, -3.5, 0.0, -5.0, 9.25, -9.75, -8.25, 3.0, -28.5, 6.75, -35.75, -2.0, 24.0, -13.75, 25.75, -1.75, 27.0, -11.25, 17.5, -4.5, -10.0, -31.25, -5.75, 4.75, 23.0, -17.0, -5.75, 6.75, -20.5, 33.75, -5.25, 8.25, 9.25, 10.25, -9.0, 4.25, 9.0, 0.5, -25.0, 15.5, 0.5, 9.0, 6.5, 4.75, -7.5, 7.75, -13.25, -17.0, 20.25, 7.25, -25.25, -9.5, 9.5, 24.0, -10.25, -2.75, -0.25, 23.0, 1.5, 6.75, -1.5, -2.0, 6.0, -3.75, -1.0, -18.25, 15.25, 1.25, -14.25, 1.75, -3.0, 10.0, -17.25, -7.0, -13.25, 1.0, 26.5, 2.75, -16.75, -9.5, 13.75, 0.0, 25.75, -17.0, 15.5, 3.5, -17.25, -6.0, 2.5, -44.75, 3.25, 17.0, -3.0, -3.0, -1.0, 9.0, -34.5, 1.5, 29.25, 24.5, 8.25, 2.0, 12.25, 2.25, 2.5, -6.75, -6.25, -9.75, -20.25, -14.25, 23.5, 13.5, 2.75, -3.75, -9.5, -7.75, 11.5, -14.75, -6.0, 25.75, -20.0, 5.25, -4.25, 8.75, 9.5, -5.5, -20.5, -48.0, -54.5, -101.5, 5.0, 62.25, 53.5, -0.5, -25.75, -47.5, 31.0, -1.0, -24.5, 10.25, 34.5, -23.0, 5.5, 11.75, -7.25, 26.5, 18.0, -12.5, -24.0, 12.25, -32.0, -2.25, -9.75, -0.5, -47.75, 3.5, 28.25, 13.5, 26.5, 32.25, -7.25, 19.25, 19.75, -0.25, 4.0, -17.0, -9.75, 35.0, 6.75, 1.5, -6.0, -13.0, 43.5, 14.0, -3.5, -1.75, 23.25, -0.75, -9.0, 20.75, 7.5, -7.5, -0.5, -0.5, -21.0, 5.0, -8.5, -28.5, -21.5, 29.0, 1.25, 29.75, 0.0, 9.5, -4.5, 0.25, 4.0, 6.5, -5.75, -6.75], [-23.25, 0.0, -6.75, -30.5, -21.25, 25.0, 34.25, -19.25, -12.5, -6.5, -7.75, -19.5, 24.5, -4.75, 8.25, 10.5, 29.25, -13.0, 10.0, -24.5, -37.5, 27.5, -27.75, 25.5, 24.75, -11.0, 24.75, -1.75, -11.0, 19.75, 3.75, 18.5, 8.5, -7.75, 10.5, -0.25, -0.25, 12.25, -0.75, 7.0, -3.5, 0.0, -5.0, 9.25, -9.75, -8.25, 3.0, -28.5, 6.75, -35.75, -2.0, 24.0, -13.75, 25.75, -1.75, 27.0, -11.25, 17.5, -4.5, -10.0, -31.25, -5.75, 4.75, 23.0, -17.0, -5.75, 6.75, -20.5, 33.75, -5.25, 8.25, 9.25, 10.25, -9.0, 4.25, 9.0, 0.5, -25.0, 15.5, 0.5, 9.0, 6.5, 4.75, -7.5, 7.75, -13.25, -17.0, 20.25, 7.25, -25.25, -9.5, 9.5, 24.0, -10.25, -2.75, -0.25, 23.0, 1.5, 6.75, -1.5, -2.0, 6.0, -3.75, -1.0, -18.25, 15.25, 1.25, -14.25, 1.75, -3.0, 10.0, -17.25, -7.0, -13.25, 1.0, 26.5, 2.75, -16.75, -9.5, 13.75, 0.0, 25.75, -17.0, 15.5, 3.5, -17.25, -6.0, 2.5, -44.75, 3.25, 17.0, -3.0, -3.0, -1.0, 9.0, -34.5, 1.5, 29.25, 24.5, 8.25, 2.0, 12.25, 2.25, 2.5, -6.75, -6.25, -9.75, -20.25, -14.25, 23.5, 13.5, 2.75, -3.75, -9.5, -7.75, 11.5, -14.75, -6.0, 25.75, -20.0, 5.25, -4.25, 8.75, 9.5, -5.5, -20.5, -48.0, -54.5, -101.5, 5.0, 62.25, 53.5, -0.5, -25.75, -47.5, 31.0, -1.0, -24.5, 10.25, 34.5, -23.0, 5.5, 11.75, -7.25, 26.5, 18.0, -12.5, -24.0, 12.25, -32.0, -2.25, -9.75, -0.5, -47.75, 3.5, 28.25, 13.5, 26.5, 32.25, -7.25, 19.25, 19.75, -0.25, 4.0, -17.0, -9.75, 35.0, 6.75, 1.5, -6.0, -13.0, 43.5, 14.0, -3.5, -1.75, 23.25, -0.75, -9.0, 20.75, 7.5, -7.5, -0.5, -0.5, -21.0, 5.0, -8.5, -28.5, -21.5, 29.0, 1.25, 29.75, 0.0, 9.5, -4.5, 0.25, 4.0, 6.5, -5.75], [-9.25, -23.25, 0.0, -6.75, -30.5, -21.25, 25.0, 34.25, -19.25, -12.5, -6.5, -7.75, -19.5, 24.5, -4.75, 8.25, 10.5, 29.25, -13.0, 10.0, -24.5, -37.5, 27.5, -27.75, 25.5, 24.75, -11.0, 24.75, -1.75, -11.0, 19.75, 3.75, 18.5, 8.5, -7.75, 10.5, -0.25, -0.25, 12.25, -0.75, 7.0, -3.5, 0.0, -5.0, 9.25, -9.75, -8.25, 3.0, -28.5, 6.75, -35.75, -2.0, 24.0, -13.75, 25.75, -1.75, 27.0, -11.25, 17.5, -4.5, -10.0, -31.25, -5.75, 4.75, 23.0, -17.0, -5.75, 6.75, -20.5, 33.75, -5.25, 8.25, 9.25, 10.25, -9.0, 4.25, 9.0, 0.5, -25.0, 15.5, 0.5, 9.0, 6.5, 4.75, -7.5, 7.75, -13.25, -17.0, 20.25, 7.25, -25.25, -9.5, 9.5, 24.0, -10.25, -2.75, -0.25, 23.0, 1.5, 6.75, -1.5, -2.0, 6.0, -3.75, -1.0, -18.25, 15.25, 1.25, -14.25, 1.75, -3.0, 10.0, -17.25, -7.0, -13.25, 1.0, 26.5, 2.75, -16.75, -9.5, 13.75, 0.0, 25.75, -17.0, 15.5, 3.5, -17.25, -6.0, 2.5, -44.75, 3.25, 17.0, -3.0, -3.0, -1.0, 9.0, -34.5, 1.5, 29.25, 24.5, 8.25, 2.0, 12.25, 2.25, 2.5, -6.75, -6.25, -9.75, -20.25, -14.25, 23.5, 13.5, 2.75, -3.75, -9.5, -7.75, 11.5, -14.75, -6.0, 25.75, -20.0, 5.25, -4.25, 8.75, 9.5, -5.5, -20.5, -48.0, -54.5, -101.5, 5.0, 62.25, 53.5, -0.5, -25.75, -47.5, 31.0, -1.0, -24.5, 10.25, 34.5, -23.0, 5.5, 11.75, -7.25, 26.5, 18.0, -12.5, -24.0, 12.25, -32.0, -2.25, -9.75, -0.5, -47.75, 3.5, 28.25, 13.5, 26.5, 32.25, -7.25, 19.25, 19.75, -0.25, 4.0, -17.0, -9.75, 35.0, 6.75, 1.5, -6.0, -13.0, 43.5, 14.0, -3.5, -1.75, 23.25, -0.75, -9.0, 20.75, 7.5, -7.5, -0.5, -0.5, -21.0, 5.0, -8.5, -28.5, -21.5, 29.0, 1.25, 29.75, 0.0, 9.5, -4.5, 0.25, 4.0, 6.5]]
y = yx[0]
x = [yx[1]]   # univariate
x = yx[1:]    # multivariate

regr_stats, regr_line = go_regression(y, x, **{'matplotlib':True})
print(regr_stats)

# Ex 0B/
# --------
y = np.dot(X, beta) + e
size_sample = 100
x = np.linspace(0, 10, size_sample)
X = np.column_stack((x, x**2))
beta = np.array([1, 0.1, 10])
e = np.random.normal(size=size_sample)

print(regr_stats.summary())

# ------------------------------------------------------------------------------
# Ex 0C/ statsmodels ols simulated
# ------------------------------------------------------------------------------
def statsmodels_ols_simulated():
N = 100
SIG = 0.25

""" X = np.array(x).T """
# Ex 0/
X = np.random.randn(N)
Y = X + np.random.randn(N) + 10

# Ex 1/
x1 = np.linspace(0, 20, N)
X = np.column_stack((x1, np.sin(x1), (x1-5)**2))


fig, ax = plt.subplots(figsize=(8, 4))
ax.scatter(X, Y, alpha=0.5, color='orchid')
fig.suptitle('Example Scatter Plot')
fig.tight_layout(pad=2);
ax.grid(True)
fig.savefig('graph_ols_data.png', dpi=125)


""" """
X = sm.add_constant(X) # constant intercept term


beta = [5., 0.5, 0.5, -0.02]
y_true = np.dot(X, beta)
y = y_true + sig * np.random.normal(size=N)


"""
  Model: y ~ x + c
  regr = sm.OLS(Y, X).fit()
"""
model = sm.OLS(Y, X)
regr = model.fit()
print(regr.params)     # the estimated parameters for the regression line
print(regr.summary())  # summary statistics for the regression



""" In sample prediction """
# Ex 0/
x_pred = np.linspace(X.min(), X.max(), 50)
x_pred2 = sm.add_constant(x_pred)
y_pred = regr.predict(x_pred2)

ax.plot(x_pred, y_pred, '-', color='darkorchid', linewidth=2)
fig.savefig('graph_ols_model.png', dpi=125)

# Ex 1/
ypred = regr.predict(X)
print(ypred)


# 95% confidence interval
y_hat = fitted.predict(X)
y_err = y - y_hat
mean_x = x.T[1].mean()
# N = len(X)
dof = N - regr.df_model - 1
t = stats.t.ppf(1-0.025, df=dof)
s_err = np.sum(np.power(y_err, 2))
conf = t * np.sqrt((s_err/(n-2))*(1.0/n + (np.power((x_pred-mean_x),2) /
   ((np.sum(np.power(x_pred,2))) - N*(np.power(mean_x,2))))))
upper = y_pred + abs(conf)
lower = y_pred - abs(conf)
ax.fill_between(x_pred, lower, upper, color='#888888', alpha=0.4)
fig.savefig('graph_ols_confidence.png', dpi=125)

# Prediction
sdev, lower, upper = wls_prediction_std(regr, exog=x_pred2, alpha=0.05)
ax.fill_between(x_pred, lower, upper, color='#888888', alpha=0.1)
fig.savefig('graph_ols_pred.png', dpi=125)


""" Out of sample prediction """
# Ex/1
x1n = np.linspace(20.5,25, 10)
Xnew = np.column_stack((x1n, np.sin(x1n), (x1n-5)**2))
Xnew = sm.add_constant(Xnew)
ynewpred =  regr.predict(Xnew) # predict out of sample
print(ynewpred)
# [ 10.789   10.6494  10.4216  10.1393   9.847    9.589    9.3986   9.2898
#    9.254    9.2621]

fig, ax = plt.subplots()
ax.plot(x1, y, 'o', label="Data")
ax.plot(x1, y_true, 'b-', label="True")
ax.plot(np.hstack((x1, x1n)), np.hstack((ypred, ynewpred)), 'r', label="OLS prediction")
ax.legend(loc="best")
fig.savefig('graph_ols2_pred.png', dpi=125)


# ------------------------------------------------------------------------------

# Ex 1/ statsmodels ols - using FORMULA
import statsmodels.formula.api as sm
lm = sm.ols(formula='y ~ x1 + x2 + x3 + x4 + x5 + x6 + x7', data=df).fit()
print(lm.params)

# Ex 1/ using same data as above
# use the I to indicate use of the Identity transform. Ie., we don't want any expansion magic from using **2
data = {"x1" : x1, "y" : y}
res = sm.ols("y ~ x1 + np.sin(x1) + I((x1-5)**2)", data=data).fit()
res.params
# Now we only have to pass the single variable and we get the transformed right-hand side variables automatically
res.predict(exog=dict(x1=x1n))
# array([ 10.789 ,  10.6494,  10.4216,  10.1393,   9.847 ,   9.589 ,
#          9.3986,   9.2898,   9.254 ,   9.2621])

"""
==================================================================================
Linear regression - numpy
==================================================================================
"""
import numpy as np
y = [-6,-5,-10,-5,-8,-3,-6,-8,-8]
x = [[-4.95,-4.55,-10.96,-1.08,-6.52,-0.81,-7.01,-4.46,-11.54],[-5.87,-4.52,-11.64,-3.36,-7.45,-2.36,-7.33,-7.65,-10.03],[-0.76,-0.71,-0.98,0.75,-0.86,-0.50,-0.33,-0.94,-1.03],[14.73,13.74,15.49,24.72,16.59,22.44,13.93,11.40,18.18],[4.02,4.47,4.18,4.96,4.29,4.81,4.32,4.43,4.28],[0.20,0.16,0.19,0.16,0.10,0.15,0.21,0.16,0.21],[0.45,0.50,0.53,0.60,0.48,0.53,0.50,0.49,0.55]]
X = np.column_stack(x+[[1]*len(x[0])])
beta_hat = np.linalg.lstsq(X,y)[0]
print beta_hat
# estimated output:
print np.dot(X,beta_hat)



"""
==================================================================================
Linear regression - scikit sklearn version

- sklearn.linear_model also has similar interfaces to do various kinds of
  regularizations on the regression.
- sklearn adds column vector of 1's so no need to add like statsmodels
==================================================================================
"""
import numpy as np
from sklearn import linear_model

# multivariate input
X = [[0., 0.], [1., 1.], [2., 2.], [3., 3.]]
# univariate output
Y = [0., 1., 2., 3.]
# multivariate output
Z = [[0., 1.], [1., 2.], [2., 3.], [3., 4.]]

# ---------------------------------
# OLS - ordinary least squares
# OLS - univariate # ex 0/
# ---------------------------------
clf = linear_model.LinearRegression()
clf.fit(X, Y)
print(clf.coef_)   # array([ 0.5,  0.5])
prediction = clf.predict([[1, 0.]])
# prediction_error = y_test - prediction

# OLS - ex 1/
b = np.array([3,5,7])
x = np.array([[1,6,9],
              [2,7,7],
              [3,4,5]])
y = np.array([96,90,64])
clf = linear_model.LinearRegression(fit_intercept=False)
clf.fit(x, y)
print(clf.coef_)
print("orig y - NOT yhat: ", np.dot(x, clf.coef_))
# Using fit_intercept=False prevents the LinearRegression object from working with x - x.mean(axis=0), which it would otherwise do (and capture the mean using a constant offset y = xb + c) - or equivalently by adding a column of 1 to x.

# ---------------------------------
# Ridge
# ---------------------------------
clf = linear_model.BayesianRidge()
# Ridge - univariate
clf.fit(X, Y)
clf.predict([[1, 0.]])
# Ridge - multivariate
clf.fit(X, Z)
clf.predict([[1, 0.]])

# ---------------------------------
# Lasso
# ---------------------------------
clf = linear_model.Lasso()
# Lasso - univariate
clf.fit(X, Y)
clf.predict([[1, 0.]])
# Lasso - multivariate
clf.fit(X, Z)
clf.predict([[1, 0.]])



print 'GFT + Wiki / GT R-squared: %.4f' % model.score(X_test, y_test)

There is a separate list of functions to calculate goodness of prediction statistics with it, but it's not integrated into the models, nor does it include R squared. (I've never heard of R squared used for out of sample data.) Calculating those requires a bit more work by the user and statsmodels does not have the same set of statistics, especially not for classification or models with a binary response variable.


from scipy.optimize import curve_fit
import scipy

def fn(x, a, b, c):
    return a + b*x[0] + c*x[1]

# y(x0,x1) data:
#    x0=0 1 2
# ___________
# x1=0 |0 1 2
# x1=1 |1 2 3
# x1=2 |2 3 4

x = scipy.array([[0,1,2,0,1,2,0,1,2,],[0,0,0,1,1,1,2,2,2]])
y = scipy.array([0,1,2,1,2,3,2,3,4])
popt, pcov = curve_fit(fn, x, y)
print popt

"""
Cross-validation
"""
# statsmodel ols
X_train, X_test, y_train, y_test = cross_validation.train_test_split(x, y, test_size=0.3, random_state=1)

x_train = sm.add_constant(X_train)
model = sm.OLS(y_train, x_train)
results = model.fit()

print "GFT + Wiki / GT  R-squared", results.rsquared









As larsmans noted, chi2 cannot be used for feature selection with regression data.

Upon updating to scikit-learn version 0.13, the following code selected the top two features (according to the f_regression test) for the toy dataset described above.

def f_regression(X,Y):
   import sklearn
   return sklearn.feature_selection.f_regression(X,Y,center=False) #center=True (the default) would not work ("ValueError: center=True only allowed for dense data") but should presumably work in general

from sklearn.datasets import load_svmlight_file

X_train_data, Y_train_data = load_svmlight_file(svmlight_format_train_file) #i.e. change this to  the name of my toy dataset file

from sklearn.feature_selection import SelectKBest
featureSelector = SelectKBest(score_func=f_regression,k=2)
featureSelector.fit(X_train_data,Y_train_data)
print [1+zero_based_index for zero_based_index in list(featureSelector.get_support(indices=True))]


"""
-----------------------------------
# Sklearn polynomial regression

Polynomial regression is a special case of linear regression. With the main idea of how do you select your features. Looking at the multivariate regression with 2 variables: x1 and x2. Linear regression will look like this: y = a1 * x1 + a2 * x2.

Now you want to have a polynomial regression (let's make 2 degree polynomial). We will create a few additional features: x1*x2, x1^2 and x2^2. So we will get your 'linear regression':

y = a1 * x1 + a2 * x2 + a3 * x1*x2 + a4 * x1^2 + a5 * x2^2
This nicely shows an important concept curse of dimensionality, because the number of new features grows much faster than linearly with the growth of degree of polynomial. You can take a look about this concept here.
-----------------------------------
"""
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model

X = [[0.44, 0.68], [0.99, 0.23]]
vector = [109.85, 155.72]
predict= [0.49, 0.18]

poly = PolynomialFeatures(degree=2)
X_ = poly.fit_transform(X)
predict_ = poly.fit_transform(predict)

clf = linear_model.LinearRegression()
clf.fit(X_, vector)
print(clf.predict(predict_))


"""
-----------------------------------
sklearn ridge regression
http://stats.stackexchange.com/questions/160096/what-are-the-differences-between-ridge-regression-using-rs-glmnet-and-pythons?rq=1
https://raw.githubusercontent.com/JWarmenhoven/ISL-python/master/Chapter%206.ipynb
-----------------------------------
"""



# ------------------------------------------------------------------------------
