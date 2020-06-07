
require(graphics)
require(stats)




"""
================================================================================
acf
================================================================================
"""
require(quantmod)

kpss.test
adf.test
Box.test

df_es <- read.table("df_es.csv", header = TRUE, sep = ",")
df_btcusd <- read.table("df_btcusd.csv", header = TRUE, sep = ",")
df_matrix <- read.table("df_btcusd_es.csv", header = TRUE, sep = ",")


>>> s_btcusd_pctchg = df_btcusd.loc[:, 'Adj Close'].pct_change()
# ---------------------------------------------------------------
s_es_0930_pctchg = diff(df_es$X09.30)/df_es$X09.30[-length(df_es$X09.30)]

s_btcusd_pctchg = diff(df_btcusd)/df_btcusd[-nrow(df_btcusd),] * 100
s_btcusd_cls_pctchg = diff(df_btcusd$Adj.Close)/df_btcusd$Adj.Close[-nrow(df_btcusd),] * 100
s_btcusd_pctchg = df_btcusd$Adj.Close/lag(df_btcusd$Adj.Close,-1) - 1
s_btcusd_pctchg = Delt(df_btcusd$Adj.Close,type='arithmetic')

df_es_1615_logchg = diff(log(df_matrix$es))

data <- ts(data.frame(x1=c(1:10), x2=c(11:20), x3=c(21:30)), start = c(2010,3), frequency = 4)
data_pctchg = data/lag(data,-1) - 1
            = diff(data)/data[-nrow(data),] * 100

df_es_chg = df_es$X16.15


>>> df.shape
>>> len(df)
num_rows = dim(s_btcusd_pctchg)[1]
         = nrow(data)
         = length(data)
min(s_btcusd_pctchg[2:num_rows,])
max(s_btcusd_pctchg[2:num_rows,])





hist(data, breaks=seq(0,80,l=6),
       freq=FALSE,col="orange",main="Histogram",
       xlab="x",ylab="f(x)",yaxs="i",xaxs="i")

hist(data,breaks=seq(min(data),max(data),l=number_of_bins+1),
            freq=FALSE,col="orange",
            main="Histogram",xlab="x",ylab="f(x)",yaxs="i",xaxs="i")

library(ggplot2)
qplot(s_btcusd_pctchg[2:num_rows,], geom="histogram")
qplot(s_btcusd_pctchg[2:num_rows,], geom="histogram", binwidth = 0.05, xlim=c(-1,1))



s_rand <- runif(1000, 0.0, 1.0)
s_rand_diff = diff(s_rand)
s_randn<-rnorm(1000)

hist(s_rand)
hist(s_randn)
hist(s_rand_diff)

acf(s_rand)
pacf(s_rand)

acf(s_randn)
pacf(s_randn)

acf(lh)
pacf(lh)

acf(ldeaths)
acf(ldeaths, ci.type = "ma")
acf(ts.union(mdeaths, fdeaths))
ccf(mdeaths, fdeaths, ylab = "cross-correlation")
# (just the cross-correlations)

presidents # contains missing values
acf(presidents, na.action = na.pass)
pacf(presidents, na.action = na.pass)


Acf(wineind)
Pacf(wineind)

taperedacf(wineind, nsim=50)
taperedpacf(wineind, nsim=50)


ccf(x, y, na.action=na.pass)


"""
================================================================================
corrlelation
running correlation
cor.test
================================================================================
"""


# ------------------------------------------------------------------------------
# cor.test
# ------------------------------------------------------------------------------
x <- c(44.4, 45.9, 41.9, 53.3, 44.7, 44.1, 50.7, 45.2, 60.1)
y <- c( 2.6,  3.1,  2.5,  5.0,  3.6,  4.0,  5.2,  2.8,  3.8)

##  The alternative hypothesis of interest is that the
##  Hunter L value is positively associated with the panel score.

cor.test(x, y, method = "kendall", alternative = "greater")
## => p=0.05972

cor.test(x, y, method = "kendall", alternative = "greater",
         exact = FALSE) # using large sample approximation
## => p=0.04765

## Compare this to
cor.test(x, y, method = "spearm", alternative = "g")
cor.test(x, y,                    alternative = "g")

## Formula interface.
require(graphics)
pairs(USJudgeRatings)
cor.test(~ CONT + INTG, data = USJudgeRatings)




# ------------------------------------------------------------------------------
# Corrlation Matrix
# ------------------------------------------------------------------------------
set.seed(955)
vvar <- 1:20 + rnorm(20,sd=3)
wvar <- 1:20 + rnorm(20,sd=5)
xvar <- 20:1 + rnorm(20,sd=3)
yvar <- (1:20)/2 + rnorm(20, sd=10)
zvar <- rnorm(20, sd=6)


# A data frame with multiple variables
data <- data.frame(vvar, wvar, xvar, yvar, zvar)
head(data)

library(ellipse)

# Make the correlation table
ctab <- cor(data)
round(ctab, 2)
#>       vvar  wvar  xvar  yvar  zvar
#> vvar  1.00  0.61 -0.85  0.75 -0.21
#> wvar  0.61  1.00 -0.81  0.54 -0.31
#> xvar -0.85 -0.81  1.00 -0.63  0.24
#> yvar  0.75  0.54 -0.63  1.00 -0.30
#> zvar -0.21 -0.31  0.24 -0.30  1.00

# Make the graph, with reduced margins
plotcorr(ctab, mar = c(0.1, 0.1, 0.1, 0.1))

# Do the same, but with colors corresponding to value
colorfun <- colorRamp(c("#CC0000","white","#3366CC"), space="Lab")
plotcorr(ctab, col=rgb(colorfun((ctab+1)/2), maxColorValue=255),
         mar = c(0.1, 0.1, 0.1, 0.1))



# ------------------------------------------------------------------------------
# Rolling Corrlation
# ------------------------------------------------------------------------------



install.packages("xml2")
install.packages("tidyverse")
install.packages("alphavantager")


library(tidyquant)  # Loads tidyverse, tidyquant, financial pkgs, xts/zoo
library(cranlogs)   # For inspecting package downloads over time
library(corrr)      # Tidy correlation tables and correlation plotting
library(cowplot)    # Multiple plots with plot_grid()




"""
================================================================================
Scatterplot, plot
lm - regression
================================================================================
"""

c(w[-1],0)


# Compare to good relationship
# Ex 0/
duration = faithful$eruptions
waiting = faithful$waiting
head(cbind(duration, waiting))

duration = faithful$eruptions        # the eruption durations
waiting = faithful$waiting           # the waiting interval
plot(duration, waiting,
  xlab="Eruption duration",
  ylab="Time waited")
abline(lm(waiting ~ duration))

The scatter plot of the eruption durations and waiting intervals
It reveals a positive linear relationship between them.

fit = lm(waiting ~ duration)
summary(fit)
plot(fit)

# Test residuals
mod = lm(prices[,1] ~ prices[,2])
res = mod$res
n = length(res)
mod2 = lm(res[-n] ~ res[-1])
summary(mod2)

# lmtest package.
dwtest(prices[,1] ~ prices[,2])


# Ex 1a/
input <- mtcars[,c('wt','mpg')]
print(head(input))

# Give the chart file a name.
png(file = "scatterplot.png")

# Plot the chart for cars with weight between 2.5 to 5 and mileage between 15 and 30.
plot(x = input$wt,y = input$mpg,
   xlab = "Weight",
   ylab = "Milage",
   xlim = c(2.5,5),
   ylim = c(15,30),
   main = "Weight vs Milage"
)

# Save the file.
dev.off()


# Ex 1b/
attach(mtcars)
plot(wt, mpg, main="Scatterplot Example",
  	xlab="Car Weight ", ylab="Miles Per Gallon ", pch=19)

# Add fit lines
abline(lm(mpg~wt), col="red")      # regression line (y~x)
lines(lowess(wt,mpg), col="blue")  # lowess line (x,y)


The scatterplot() function in the car package offers many enhanced features,
including fit lines, marginal box plots, conditioning on a factor, and
interactive point identification. Each of these features is optional.

# Enhanced Scatterplot of MPG vs. Weight
# by Number of Car Cylinders
library(car)
scatterplot(mpg ~ wt | cyl, data=mtcars,
  	xlab="Weight of Car", ylab="Miles Per Gallon",
   main="Enhanced Scatter Plot",
   labels=row.names(mtcars))




When we have more than 2 variables and we want to find the correlation between
one variable versus the remaining ones we use scatterplot matrix:
pairs() function to create matrices of scatterplots.

png(file = "scatterplot_matrices.png")

# Plot the matrices between 4 variables giving 12 plots.
# One variable with 3 others and total 4 variables.

pairs(~wt+mpg+disp+cyl,data = mtcars,
   main = "Scatterplot Matrix")

pairs(~cyl+mpg+disp+drat+wt,data=mtcars,
      main="Simple Scatterplot Matrix")

# Save the file.
dev.off()





shift <- function(x, lag) {
    n <- length(x)
    xnew <- rep(NA, n)
    if (lag < 0) {
        xnew[1:(n-abs(lag))] <- x[(abs(lag)+1):n]
    } else if (lag > 0) {
        xnew[(lag+1):n] <- x[1:(n-lag)]
    } else {
        xnew <- x
    }
    return(xnew)
}



# Scatterplot Matrices from the lattice Package
library(lattice)
splom(mtcars[c(1,3,5,6)], groups=cyl, data=mtcars,
  	panel=panel.superpose,
   key=list(title="Three Cylinder Options",
   columns=3,
   points=list(pch=super.sym$pch[1:3],
   col=super.sym$col[1:3]),
   text=list(c("4 Cylinder","6 Cylinder","8 Cylinder"))))



# Ex 2/ rnorm
set.seed(955)
# Make some noisily increasing data
dat <- data.frame(xvar = 1:100 + rnorm(20,sd=3),
                  yvar = 1:100 + rnorm(20,sd=3),
                  zvar = 1:100 + rnorm(20,sd=3))

head(dat)

# Plot the points using the vectors xvar and yvar
plot(dat$xvar, dat$yvar)

# Same as previous, but with formula interface
plot(yvar ~ xvar, dat)

# Add a regression line
fitline <- lm(dat$yvar ~ dat$xvar)
abline(fitline)


# Matrices plot
plot(dat[,1:3])

# scatterplot matrix, with regression lines
# and histogram/boxplot/density/qqplot/none along the diagonal
library(car)
scatterplotMatrix(dat[,1:3],
                   diagonal="histogram",
                   smooth=FALSE)



# ==============================================================================
# ==============================================================================
