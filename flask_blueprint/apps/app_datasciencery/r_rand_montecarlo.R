"""
================================================================================
# Random
# Sampling
================================================================================
"""

log_returns <- diff(log(prices), lag=1)  # diff(log(w))
lrest <- log(prices[-1]/prices[-length(prices)])


"""
For uniformly distributed (flat) random numbers,
runif() => real-valued
By default, its range is from 0 to 1.

sample => integer valued
"""

sample(c(1,2,3), 1)
 [1] 2

runif(1, 1, 3)
 [1] 1.448551

runif(1)
#> [1] 0.09006613

# Get a vector of 4 numbers
runif(4)
#> [1] 0.6972299 0.9505426 0.8297167 0.9779939

# Get a vector of 3 numbers from 0 to 100
runif(3, min=0, max=100)
#> [1] 83.702278  3.062253  5.388360

# Get 3 integers from 0 to 100
# Use max=101 because it will never actually equal 101
floor(runif(3, min=0, max=101))
#> [1] 11 67  1

# This will do the same thing
sample(1:100, 3, replace=TRUE)
#> [1]  8 63 64


x_rand <- sample(1:10, 1)   # integers
s_rand <- sample(1:10, 10, replace=T)

# Here's a fun exercise: what is the probability of running this command and
# having no repeats in the 5 numbers generated?)

x_rand <- runif(1, 5.0, 7.5)  # random number between 5.0 and 7.5 - uniform dist
[1] 6.715697
s_rand <- runif(10, 5.0, 7.5)

# generate a random subset - 10 distinct states of the US
sample(state.name, 10)
sample(state.name, 10, replace=T)
sample(state.name, 50)   # randomize states  # = state.name


"""
To generate numbers from a normal distribution, use rnorm().
By default the mean is 0 and the standard deviation is 1.
"""
rnorm(4)
#> [1] -2.3308287 -0.9073857 -0.7638332 -0.2193786

# Use a different mean and standard deviation
rnorm(4, mean=50, sd=10)
#> [1] 59.20927 40.12440 44.58840 41.97056

# To check that the distribution looks right, make a histogram of the numbers
x <- rnorm(400, mean=50, sd=10)
hist(x)


x <- 1:12
# a random permutation
sample(x)
# bootstrap resampling -- only if length(x) > 1 !
sample(x, replace = TRUE)

# 100 Bernoulli trials
sample(c(0,1), 100, replace = TRUE)

## More careful bootstrapping --  Consider this when using sample()
## programmatically (i.e., in your function or simulation)!

# sample()'s surprise -- example
x <- 1:10
sample(x[x >  8]) # length 2
sample(x[x >  9]) # oops -- length 10!
sample(x[x > 10]) # length 0

## safer version:
resample <- function(x, ...) x[sample.int(length(x), ...)]
resample(x[x >  8]) # length 2
resample(x[x >  9]) # length 1
resample(x[x > 10]) # length 0

## R 3.x.y only
sample.int(1e10, 12, replace = TRUE)
sample.int(1e10, 12) # not that there is much chance of duplicates

log_returns <- diff(log(prices), lag=1)

"""
For linear regression... 1. Don't worry much about normality. The CLT takes over
quickly and if you have all but the smallest sample sizes and an even remotely
reasonable looking histogram you are fine. 2. Worry about unequal variances
(heteroskedasticity). I worry about this to the point of (almost) using HCCM
tests by default. A scale location plot will give some idea of whether this is
broken, but not always. Also, there is no a priori reason to assume equal
variances in most cases. 3. Outliers. A cooks distance of > 1 is reasonable
cause for concern. Those are my thoughts (FWIW)

In practice, if an analysis assumes normality, e.g. lm, I would not do this
Shapiro-Wilk's test, but do the analysis and look at diagnostic plots of the
outcome of the analysis to judge whether any assumptions of the analysis where
violated too much. For linear regression using lm this is done by looking at
some of the diagnostic plots you get using plot(lm()). Statistics is not a
series of steps that cough up a few numbers (hey p < 0.05!) but requires a lot
of experience and skill in judging how to analysis your data correctly.

http://www.dummies.com/programming/r/how-to-test-data-normality-in-a-formal-way-in-r/
https://stackoverflow.com/questions/15427692/perform-a-shapiro-wilk-normality-test
https://stackoverflow.com/questions/7781798/seeing-if-data-is-normally-distributed-in-r/7788452#7788452

An additional issue with the Shapiro-Wilks test is that when you feed it more
data, the chances of the null hypothesis being rejected becomes larger. So what
happens is that for large amounts of data even veeeery small deviations from
normality can be detected, leading to rejection of the null hypothesis even
though for practical purposes the data is more than normal enough

boxcox transforms nonnormally distributed data to a set of data that has approximately normal distribution.
"""

#library(nortest)
# set.seed(1)  set.seed(Sys.time())

par(ask = TRUE)

x <- runif(10)   # (0,1)
print(paste(min(x), max(x))

x <- runif(10000)
x2 = runif(50, min=2, max=4)
# Manually scaling
x_man = (x - mean(x)) / sd(x)
x_scale = scale(x)
print(x_man)
print(x_scale)

hist(x)
hist(x_scale)
qqnorm(x);qqline(x)
qqnorm(x_scale);qqline(x_scale)

x_diff = diff(x)
hist(x_diff)
qqnorm(x_diff);qqline(x_diff)
shapiro.test(x_diff[1:100])
ad.test(x_diff)

x_diff_scale = scale(x_diff)
hist(x_diff_scale)
qqnorm(x_diff_scale);qqline(x_diff_scale)
shapiro.test(x_diff_scale[1:100])
ad.test(x_diff_scale)

print(mean(x_diff_scale))
print(sd(x_diff_scale))

# Test for normality
shapiro.test(x_scale[1:50])
shapiro.test(x_scale[1:100])
ad.test(x_scale[1:1000])

shapiro.test(x_diff_scale[1:100])
ad.test(x_diff_scale[1:1000])

#plot(density(x_diff_scale))
qqnorm(x_diff_scale);qqline(x_diff_scale)


x_pctchg = diff(x)/x[-length(x)]  # x[-1] / x[-length(x)] - 1
hist(x_pctchg)
qqnorm(x_pctchg);qqline(x_pctchg)
shapiro.test(x_pctchg[1:100])
ad.test(x_pctchg)

x_pctchg_scale = scale(x_pctchg)
hist(x_pctchg_scale)
qqnorm(x_pctchg_scale);qqline(x_pctchg_scale)
shapiro.test(x_pctchg_scale[1:100])
ad.test(x_pctchg_scale)

x_logchg = diff(log(x))  # = log(x[-1]/x[-length(x)])
hist(x_logchg)
plot(density(x_logchg))
qqnorm(x_logchg);qqline(x_logchg)
shapiro.test(x_logchg[1:100])
ad.test(x_logchg)

x_logchg_scale = scale(x_logchg)
hist(x_logchg_scale)
plot(density(x_walk_logchg))
qqnorm(x_logchg_scale);qqline(x_logchg_scale)
shapiro.test(x_logchg_scale[1:100])
ad.test(x_logchg_scale)



# vs normal random
# ----------------
x_norm <- rnorm(10000)
print(paste(min(x_norm), max(x_norm)))
hist(x_norm)
qqnorm(x_norm)
shapiro.test(x_norm[1:5000])

x_norm_diff = diff(x_norm)
x_norm_diff_scale = scale(x_norm_diff)
qqnorm(x_norm_diff);qqline(x_norm_diff)
qqnorm(x_norm_diff_scale);qqline(x_norm_diff_scale)
shapiro.test(x_norm_diff[1:5000])
shapiro.test(x_norm_diff_scale[1:5000])


# vs t dist
# ---------
x_t <- rt(10000,200)
# x <- rbinom(15,5,.6)
# x <- rlnorm(20,0,.4)

qqnorm(x_t);qqline(x_t)
shapiro.test(x_t[1:50])
ad.test(x_t)               # Anderson-Darling normality test
                           # finally rejects null
# A = 1.1003, p-value = 0.006975


# Random walk
N = 1000
w <- cumsum(rnorm(n=N, mean=3.5, sd=sqrt(31478.9)))
plot(w)
w_pctchg = diff(x_walk)/x_walk[-length(x_walk)]
hist(w)
hist(w_pctchg)
plot(density(w_pctchg))
qqnorm(w_pctchg);qqline(w_pctchg)
shapiro.test(w_pctchg[1:100])
ad.test(w_pctchg)

w_logchg = diff(log(w))
hist(w)
hist(w_logchg)
plot(density(w_logchg))
qqnorm(w_logchg);qqline(w_logchg)
shapiro.test(w_logchg[1:100])
ad.test(w_logchg)




x_log = log(x)
hist(x_log)
qqnorm(x_log);qqline(x_log)
shapiro.test(x_log[1:100])
ad.test(x_log)

x_log_scale = scale(x_log)
hist(x_log_scale)
qqnorm(x_log_scale);qqline(x_log_scale)
shapiro.test(x_log_scale[1:100])
ad.test(x_log_scale)

x_pctchg2 = exp(x_logchg) - 1


library(ffp)
library(forecast)
x <- arima.sim(list(order = c(1,0,0),ar = 0.2),n = 100)




# ------------------------------------------------------------------------------
# distributions
# ------------------------------------------------------------------------------
require(stats)
require(distr)

# par(ask = TRUE)

N = 10
t <- 1:N
y = exp(t)
# y = exp(log(t))
plot(y, type="l")

N = 100
t <- 1:N
y = log(t)
plot(y, type="l")

# for lowess, rpois, rnorm
plot(cars)
lines(lowess(cars))
points(lowess(cars))

plot(cars)
plot(lowess(cars), type="l", add=TRUE)

plot(sin); curve(cos, add=TRUE).

plot(sin, -pi, 2*pi) # see ?plot.function

## Discrete Distribution Plot:
plot(table(rpois(100, 5)), type = "h", col = "red", lwd = 10,
     main = "rpois(100, lambda = 5)")

## Simple quantiles/ECDF, see ecdf() {library(stats)} for a better one:
plot(x <- sort(rnorm(47)), type = "s", main = "plot(x, type = \"s\")")
points(x, cex = .5, col = "dark red")
# }


# ------------------------------------------------------------------------------
# Sine with noise
# ------------------------------------------------------------------------------
# ------------------------------
# y = a*sin(b*t) + err*amp
# ------------------------------

# set.seed(1)
# rm(.Random.seed, envir=globalenv())
# set.seed(Sys.time())

N <- 100 # number of data points
t <- seq(0,4*pi,,N)
a <- 3
b <- 2
c.unif <- runif(N)
c.norm <- rnorm(N)
amp <- 2

y_sin_uni <- a*sin(b*t) + c.unif*amp # uniform error
y_sin_nor <- a*sin(b*t) + c.norm*amp # Gaussian/normal error
y_sin_nor2 <- a*sin(b*t) + rnorm(n) # Gaussian/normal error
y_cos_nor <- a*cos(b*t)+c.norm*amp

# plot results
plot(t, y_sin_uni, t="l", ylim=range(y1,y2)*c(1,1.2))
lines(t, y_sin_nor, col=2)
legend("top", legend=c("y1 unifrom error", "y2 gaussian noise"), col=1:2, lty=1, ncol=2, bty="n")

# scatter
plot(y_sin_nor, y_sin_nor2, cex=0.5)
plot(diff(y_sin_nor), diff(y_sin_nor2), cex=0.5)





# ------------------------------------------------------------------------------
# Polynomial with noise
# ------------------------------------------------------------------------------
N=200
x <- 1:N
poly_x <- poly(x, degree = 3)
y_cubic = poly_x[,3]
y_cubic_nor = y_cubic + rnorm(N)/30

plot(y_cubic_nor, type="l")

acf(y_cubic_nor)
acf(diff(y_cubic_nor))



mod <- glm(output ~ poly(input, degree = 3), data=my.data)



# ------------------------------------------------------------------------------
# random walk
# ------------------------------------------------------------------------------
for(i in 2:n){
  x[i] <- x[i - 1] + sample(step, 1)
}
set.seed(1)

N <- 1000
x_walk <- cumsum(sample(c(-1, 1), n, TRUE))
x_walk <- cumsum(rnorm(n=N, mean=drift, sd=sqrt(variance)))
x_walk <- cumsum(rnorm(n=N, mean=3.5, sd=sqrt(31478.9)))




set.seed(1)
timeseriesmodel <- function(N, x0, delta, variance) {
      z<-cumsum(rnorm(n=N, mean=0, sd=sqrt(variance)))
      t<-1:N
      x<-x0+t*delta+z
      return(x)}
# 100 timeseries data sets of length 250.
> Series <- replicate(100, timeseriesmodel(250,1,0,1.2) )  # repeating 100 times `timeseriesmodel`
> dim(Series)   # each result is store column-wise
[1] 250 100
> cor(Series[249,], Series[250,] ) # here's the correlation between element 249 and 250
[1] 0.9975532




# Generate k random walks across time {0, 1, ... , T}
T <- 100
k <- 250
initial.value <- 10
GetRandomWalk <- function() {
  # Add a standard normal at each step
  initial.value + c(0, cumsum(rnorm(T)))
}
# Matrix of random walks
values <- replicate(k, GetRandomWalk())
# Create an empty plot
dev.new(height=8, width=12)
plot(0:T, rep(NA, T + 1), main=sprintf("%s Random Walks", k),
     xlab="time", ylab="value",
     ylim=10 + 4.5 * c(-1, 1) * sqrt(T))
mtext(sprintf("%s%s} with initial value of %s",
              "Across time {0, 1, ... , ", T, initial.value))
for (i in 1:k) {
  lines(0:T, values[ , i], lwd=0.25)
}
for (sign in c(-1, 1)) {
  curve(initial.value + sign * 1.96 * sqrt(x), from=0, to=T,
        n=2*T, col="darkred", lty=2, lwd=1.5, add=TRUE)
}
legend("topright", "1.96 * sqrt(t)",
       bty="n", lwd=1.5, lty=2, col="darkred")
savePlot("random_walks.png")





"""
# ------------------------------------------------------------------------------
# Heavy tail Distributions
# ------------------------------------------------------------------------------
"""
library(LambertW)
set.seed(1)
zz = rLambertW(n=1000, distname = "normal", beta = c(0,1), delta = 0.5)
normfit(zz)
You can also fit the best model to the data using a maximum likelihood estimator (MLE)

model = MLE_LambertW(zz, distname = "normal", type = "h")
summary(model)
plot(model)


# Laplace
# f(y) = exp(-abs(y-m)/s)/(2*s)
# where m is the location parameter of the distribution and s is the dispersion.

library(distr)
D <- DExp(rate = 1)
r(D)(1)


#Using pdf for a laplace RV:
#F(y) = 1/sqrt(2*sigma^2)*exp(sqrt(2)*abs(y-mu)/sigma)
rlaplace = function(n,mu,sigma){
  U = runif(n,0,1)
  #This will give negative value half of the time
  sign = ifelse(rbinom(n,1,.5)>.5,1,-1)
  y = mu + sign*sigma/sqrt(2)*log(1-U)
  y
}


library(rmulti)
dlaplace(y, m=0, s=1, log=FALSE)
plaplace(q, m=0, s=1)
qlaplace(p, m=0, s=1)
hlaplace(y, m=0, s=1)
rlaplace(n, m=0, s=1)
