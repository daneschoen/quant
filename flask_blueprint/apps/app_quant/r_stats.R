
require(graphics)
require(stats)
require(quantmod)

# getOption("max.print")   # 1000
options(max.print=3000)

"""
================================================================================
import and pctchg
================================================================================
"""

df_es <- read.table(paste0(PATH, "df_es.csv"), header = TRUE, sep = ",")
df_btcusd <- read.table(paste0(PATH, "df_btcusd.csv"), header = TRUE, sep = ",")
df_matrix <- read.table(paste0(PATH, "df_btcusd_es.csv"), header = TRUE, sep = ",")
#df_matrix <- read.table("df_matrix.csv", header = TRUE, sep = ",")

colnames_df_matrix = colnames(df_matrix)

# >>> s_btcusd_pctchg = df_btcusd.loc[:, 'Adj Close'].pct_change()
# ----------------------------------------------------------------
# s_btcusd_cls_pctchg = df_btcusd$Adj.Close/lag(df_btcusd$Adj.Close, 1) - 1
# s_btcusd_cls_pctchg = Delt(df_btcusd$Adj.Close,type='arithmetic')
# s_btcusd_pctchg = diff(df_btcusd)/df_btcusd[-nrow(df_btcusd),] * 100
# Delt(df_es$X09.30, type='arithmetic')
s_es_0930_pctchg = diff(df_es$X09.30)/df_es$X09.30[-length(df_es$X09.30)]
s_es_1615_pctchg = diff(df_es$X16.15)/df_es$X16.15[-length(df_es$X16.15)]
s_es_1700_pctchg = diff(df_es$X17.00)/df_es$X17.00[-length(df_es$X17.00)]
s_btcusd_cls_pctchg = diff(df_btcusd$Adj.Close)/df_btcusd$Adj.Close[-length(df_btcusd$Adj.Close)]

df_es_1700_pctchg = diff(df_matrix$es)/df_matrix$es[-length(df_matrix$es)]
df_es_1700_logchg = diff(log(df_matrix$es))
df_btcusd_cls_pctchg = diff(df_matrix$btcusd)/df_matrix$btcusd[-length(df_matrix$btcusd)]
df_btcusd_cls_logchg= diff(log(df_matrix$btcusd))

df_matrix_pctchg = data.frame(df_matrix$ts[-1], df_btcusd_cls_pctchg, df_es_1700_pctchg)
df_matrix_logchg = data.frame(df_matrix$ts[-1], df_btcusd_cls_logchg, df_es_1700_logchg)
colnames(df_matrix_pctchg) <- colnames_df_matrix
colnames(df_matrix_logchg) <- colnames_df_matrix   # c("ts","es","btcusd")


num_rows = dim(s_btcusd_pctchg)[1]
n_df_btcusd_pctchg = nrow(df_btcusd_pctchg)
min(s_btcusd_pctchg[2:num_rows,])
max(s_btcusd_pctchg[2:num_rows,])

plot(s_es_1615_pctchg)
hist(s_es_1615_pctchg)
plot(s_btcusd_cls_pctchg)
hist(s_btcusd_cls_pctchg)

hist(data, breaks=seq(0,80,l=6),
       freq=FALSE,col="orange",main="Histogram",
       xlab="x",ylab="f(x)",yaxs="i",xaxs="i")

hist(data,breaks=seq(min(data),max(data),l=number_of_bins+1),
            freq=FALSE,col="orange",
            main="Histogram",xlab="x",ylab="f(x)",yaxs="i",xaxs="i")

# library(ggplot2)
# qplot(s_btcusd_pctchg[2:num_rows,], geom="histogram")
# qplot(s_btcusd_pctchg[2:num_rows,], geom="histogram", binwidth = 0.05, xlim=c(-1,1))



"""
================================================================================
scatterplot
lm - regression
================================================================================
"""

plot(df_es_1700_pctchg, df_btcusd_cls_pctchg,
  xlab="es 1700",
  ylab="btcusd cls")
abline(lm(df_btcusd_cls_pctchg ~ df_es_1700_pctchg))

fit = lm(df_btcusd_cls_pctchg ~ df_es_1700_pctchg)
summary(fit)
plot(fit)

# [(N-Per):N]
N = length(df_es_1700_pctchg)
per = 200
per = DAYS
per_end = N   # N ;  N-per
per_beg = per_end - per


do_stats <- function(y, x, bl_save=TRUE) {
  # y ~ x
  plot(df_es_1700_pctchg[per_beg:per_end], df_btcusd_cls_pctchg[per_beg:per_end],
    xlab=paste("es 1700 - per: ", per, " per_beg: ", per_beg, " per_end: ", per_end, sep=""),
    ylab="btcusd cls - per")
  abline(lm(df_btcusd_cls_pctchg[per_beg:per_end] ~ df_es_1700_pctchg[per_beg:per_end]))

  fit = lm(df_btcusd_cls_pctchg[per_beg:per_end] ~ df_es_1700_pctchg[per_beg:per_end])
  summary(fit)
  plot(fit)
}

library(car)

scatterplot(df_btcusd_cls_pctchg[per_beg:per_end] ~ df_es_1700_pctchg[per_beg:per_end])
abline(lm(df_btcusd_cls_pctchg[per_beg:per_end] ~ df_es_1700_pctchg[per_beg:per_end]))


# btc ~ es
# filter, shift
# names(df_matrix_pctchg)
# [1] "df_es_1700_pctchg"    "df_btcusd_cls_pctchg"



# ------------------------------------------------------------------------------
# btcusd[0] ~ es[-d]
# ------------------------------------------------------------------------------

# library(data.table)

rotate <- function(d, k) rbind( tail(d,k), head(d,-k), deparse.level = 0 )
rotate2 <- function(df,offset) df[((1:nrow(df))-1-offset)%%nrow(df)+1,]

shift_col <- function(x, lag) {
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


shift_df <- function(df, y_col, x_col, d) {
  if (d==0){ return(df) }

  y = shift_col(df[[y_col]], d)
  y = y[-(length(y)+(d+1)):-length(y)]
  x = df[[x_col]][-(nrow(df)+(d+1)):-nrow(df)]

  if("ts" %in% colnames(df)){
    # ts = df[-(length(y)+(d+1)):-length(y), "ts"]
    # ts = df[["ts"]][-(nrow(df)+(d+1)):-nrow(df)]
    ts = df[["ts"]][-1:d]
    df = data.frame(ts, y, x)
    colnames(df) <- c("ts", y_col, x_col)
  } else {
    df = data.frame(y, x)
    colnames(df) <- c(y_col, x_col)
  }

  return(df)
}


shift_df_matrix <- function(df, y_col, x_col, d) {
  if (d==0){ return(df) }

  y = shift_col(df[[y_col]], d)
  y = y[-(length(y)+(d+1)):-length(y)]
  x = df[[x_col]][-(nrow(df)+(d+1)):-nrow(df)]

  if("ts" %in% colnames(df)){
    # ts = df[-(length(y)+(d+1)):-length(y), "ts"]
    # ts = df[["ts"]][-(nrow(df)+(d+1)):-nrow(df)]
    ts = df[["ts"]][-1:d]
    df = data.frame(ts, y, x)
    colnames(df) <- c("ts", y_col, x_col)
  } else {
    df = data.frame(y, x)
    colnames(df) <- c(y_col, x_col)
  }

  return(df)
}


shift_df_autocorr_matrix <- function(df, y_col, d) {
  if (d==0){ return(df) }
  #
  # ts  btc  btc[+1]  btc[+2]  btc[+3]  btc[+4]  btc[+5]
  #
  # df1 = data.frame(u=1:10)
  # shift_df_autocorr_matrix(df1, "u", 5)
  # shift_df_autocorr_matrix(df1, "u", 3)
  #
  # df2 = shift_df_autocorr_matrix(df_matrix_pctchg_es_dn, "btcusd", 5)
  #

  y = df[y_col][-(nrow(df)-(d-1)):-nrow(df)]
  colnms = sapply("y", paste, 1:d, sep="_")

  if ("ts" %in% colnames(df)){
    ts = df[["ts"]][-1:d]
    df_shift = data.frame(df[["ts"]][-(nrow(df)-(d-1)):-nrow(df)])
    df_shift["x"] = df[[y_col]][-(nrow(df)-(d-1)):-nrow(df)]
    colnms = c("ts", "x", colnms)
  } else {
    df_shift = data.frame(df[[y_col]][-(nrow(df)-(d-1)):-nrow(df)])
    colnms = c("x", colnms)
  }

  for (v in 1:d){
    df_ = df[[y_col]][-1:-v]
    df_ = df_[-(nrow(df)-(d-v-1)):-nrow(df)]
    df_shift[colnms[v]] = df_
  }

  colnames(df_shift) <- colnms

  return(df_shift)
}


df_matrix_pctchg_es_dn = df_matrix_pctchg[df_matrix_pctchg$es < 0, ]
df_matrix_pctchg_es_up = df_matrix_pctchg[df_matrix_pctchg$es > 0, ]

#1
d = -1
y_es_dn1 = shift_col(df_matrix_pctchg_es_dn$btcusd, d)
y_es_dn1 = y_es_dn1[-length(y_es_dn1)]
x_es_dn1 = df_matrix_pctchg_es_dn$es[-nrow(df_matrix_pctchg_es_dn)]

y_es_up1 = shift_col(df_matrix_pctchg_es_up$btcusd, d)
y_es_up1 = y_es_up1[-length(y_es_up1)]
x_es_up1 = df_matrix_pctchg_es_up$es[-nrow(df_matrix_pctchg_es_up)]

df_es_dn1 = shift_df(df_matrix_pctchg_es_dn, 'btcusd', 'es', -1)
df_es_up1 = shift_df(df_matrix_pctchg_es_up, 'btcusd', 'es', -1)

# ------------------------------------------------------------------------------
# es[0] ~ btcusd[-d]
# ------------------------------------------------------------------------------
df_matrix_pctchg_btcusd_dn = df_matrix_pctchg[df_matrix_pctchg$btcusd < 0, ]
df_matrix_pctchg_btcusd_up = df_matrix_pctchg[df_matrix_pctchg$btcusd > 0, ]

#1
y_dn = shift(df_matrix_pctchg_dn$es,-1)
y_dn = y_dn[-length(y_dn)]
x_dn = df_matrix_pctchg_dn$es[-nrow(df_matrix_pctchg_btcusd_dn)]

y_up = shift(df_matrix_pctchg_btcusd_up$es,-1)
y_up = y_up[-length(y_up)]
x_up = df_matrix_pctchg_up$es[-nrow(df_matrix_pctchg_btcusd_up)]
#2


#3



# ------------------------------------------------------------------------------
# es<0> ~ btcusd<-1> ; es <0
# ------------------------------------------------------------------------------
plot_scatter <- function(y, x, per_end=FALSE, per_beg=FALSE, per=200, npar=TRUE, bl_save=TRUE) {
  if (!per_end) {
    per_end = length(x)
  }
  if (!per_beg) {
    per_beg = per_end - per
  }

  cat(per_end, per_beg)

  plot(y[per_beg:per_end] ~ x[per_beg:per_end], cex=0.5)
  abline(lm(y[per_beg:per_end] ~ x[per_beg:per_end]))
}


plot(df_matrix_pctchg_es_dn$es, df_matrix_pctchg_es_dn$btcusd)
abline(lm(df_matrix_pctchg_es_dn$btcusd ~ df_matrix_pctchg_es_dn$es))
N = nrow(df_matrix_pctchg_es_dn)
per = 200
per_end = N-200  # N-200   # N ;  N-per
per_beg = per_end - per
plot(df_matrix_pctchg_es_dn$btcusd[per_beg:per_end] ~ df_matrix_pctchg_es_dn$es[per_beg:per_end], cex=0.5)
abline(lm(df_matrix_pctchg_es_dn$btcusd[per_beg:per_end] ~ df_matrix_pctchg_es_dn$es[per_beg:per_end]))

plot_scatter(df_matrix_pctchg_es_dn$btcusd, df_matrix_pctchg_es_dn$es)
plot_scatter(df_matrix_pctchg_es_dn$btcusd, df_matrix_pctchg_es_dn$es, 664, 464)

plot(df_matrix_pctchg_es_up$es, df_matrix_pctchg_es_up$btcusd, cex=0.5)
abline(lm(df_matrix_pctchg_es_up$btcusd ~ df_matrix_pctchg_es_up$es))
N = nrow(df_matrix_pctchg_es_up)
per = 200
per_end = N # N-200   # N ;  N-per
per_beg = per_end - per
plot(df_matrix_pctchg_es_up$btcusd[per_beg:per_end] ~ df_matrix_pctchg_es_up$es[per_beg:per_end], cex=0.5)
abline(lm(df_matrix_pctchg_es_up$btcusd[per_beg:per_end] ~ df_matrix_pctchg_es_up$es[per_beg:per_end]))

plot_scatter(df_matrix_pctchg_es_up$btcusd, df_matrix_pctchg_es_up$es)


# ----------------
# btc<0> ~ es<-1>
# -----------------
plot(y_es_dn ~ x_es_dn, cex=0.5)
abline(lm(y_es_dn ~ x_es_dn))
N = length(y_es_dn)
per = 200
per_end = N  # N-200   # N ;  N-per
per_beg = per_end - per
plot(y_es_dn[per_beg:per_end] ~ x_es_dn[per_beg:per_end], cex=0.5)
abline(lm(y_es_dn[per_beg:per_end] ~ x_es_dn[per_beg:per_end]))

plot_scatter(y_es_dn, x_es_dn)
plot_scatter(y_es_dn, x_es_dn, length(y_es_dn)-100)


# up ou dn
df_es_1 = shift_df(df_matrix_pctchg, 'btcusd', 'es', -1)
df_es_2 = shift_df(df_matrix_pctchg, 'btcusd', 'es', -2)
df_es_3 = shift_df(df_matrix_pctchg, 'btcusd', 'es', -3)
df_es_4 = shift_df(df_matrix_pctchg, 'btcusd', 'es', -4)
df_es_5 = shift_df(df_matrix_pctchg, 'btcusd', 'es', -5)
plot_scatter(df_es_1[['btcusd']], df_es_1[['es']])
plot_scatter(df_es_1[['btcusd']], df_es_1[['es']], nrow(df_es_1)-100)
plot_scatter(df_es_2[['btcusd']], df_es_2[['es']])
plot_scatter(df_es_2[['btcusd']], df_es_2[['es']], nrow(df_es_2)-100)
plot_scatter(df_es_3[['btcusd']], df_es_3[['es']])
plot_scatter(df_es_3[['btcusd']], df_es_3[['es']], nrow(df_es_3)-100)
plot_scatter(df_es_4[['btcusd']], df_es_4[['es']])
plot_scatter(df_es_4[['btcusd']], df_es_4[['es']], nrow(df_es_4)-100)
plot_scatter(df_es_5[['btcusd']], df_es_5[['es']])
plot_scatter(df_es_5[['btcusd']], df_es_5[['es']], nrow(df_es_5)-100)


df_es_dn1 = shift_df(df_matrix_pctchg_es_dn, 'btcusd', 'es', -1)
df_es_dn2 = shift_df(df_matrix_pctchg_es_dn, 'btcusd', 'es', -2)
df_es_dn3 = shift_df(df_matrix_pctchg_es_dn, 'btcusd', 'es', -3)
df_es_dn4 = shift_df(df_matrix_pctchg_es_dn, 'btcusd', 'es', -4)
df_es_dn5 = shift_df(df_matrix_pctchg_es_dn, 'btcusd', 'es', -5)
plot_scatter(df_es_dn3[['btcusd']], df_es_dn3[['es']])
plot_scatter(df_es_dn3[['btcusd']], df_es_dn3[['es']], nrow(df_es_dn3)-100)
plot_scatter(df_es_dn4[['btcusd']], df_es_dn4[['es']])
plot_scatter(df_es_dn4[['btcusd']], df_es_dn4[['es']], nrow(df_es_dn4)-100)
plot_scatter(df_es_dn5[['btcusd']], df_es_dn5[['es']])
plot_scatter(df_es_dn5[['btcusd']], df_es_dn5[['es']], nrow(df_es_dn5)-100)


df_es_up1 = shift_df(df_matrix_pctchg_es_up, 'btcusd', 'es', -1)
df_es_up2 = shift_df(df_matrix_pctchg_es_up, 'btcusd', 'es', -2)
df_es_up3 = shift_df(df_matrix_pctchg_es_up, 'btcusd', 'es', -3)
df_es_up4 = shift_df(df_matrix_pctchg_es_up, 'btcusd', 'es', -4)
df_es_up5 = shift_df(df_matrix_pctchg_es_up, 'btcusd', 'es', -5)
plot_scatter(df_es_up1[['btcusd']], df_es_up1[['es']])
plot_scatter(df_es_up1[['btcusd']], df_es_up1[['es']], nrow(df_es_up1)-100)
plot_scatter(df_es_up2[['btcusd']], df_es_up2[['es']])
plot_scatter(df_es_up2[['btcusd']], df_es_up2[['es']], nrow(df_es_up1)-100)
plot_scatter(df_es_up3[['btcusd']], df_es_up3[['es']])
plot_scatter(df_es_up3[['btcusd']], df_es_up3[['es']], nrow(df_es_up3)-100)
plot_scatter(df_es_up4[['btcusd']], df_es_up4 [['es']])
plot_scatter(df_es_up4[['btcusd']], df_es_up4[['es']], nrow(df_es_up4)-100)
plot_scatter(df_es_up5[['btcusd']], df_es_up5[['es']])
plot_scatter(df_es_up5[['btcusd']], df_es_up5[['es']], nrow(df_es_up5)-100)



df_es_1 = shift_df(df_matrix_pctchg, 'btcusd', 'es', -1)
df_es_2 = shift_df(df_matrix_pctchg, 'btcusd', 'es', -2)
df_es_3 = shift_df(df_matrix_pctchg, 'btcusd', 'es', -3)
df_es_4 = shift_df(df_matrix_pctchg, 'btcusd', 'es', -4)
df_es_5 = shift_df(df_matrix_pctchg, 'btcusd', 'es', -5)
plot_scatter(df_es_3[['btcusd']], df_es_3[['es']])
plot_scatter(df_es_3[['btcusd']], df_es_3[['es']], nrow(df_es_3)-100)



# ----------------
# es<0> ~ btc<-1>
# ----------------

plot(df_matrix_pctchg_dn$es ~ df_matrix_pctchg_dn$btcusd)
abline(lm(df_matrix_pctchg_dn$es) ~ df_matrix_pctchg_dn$btcusd)
N_dn = nrow(df_matrix_pctchg_dn)
per = 200
per_end = N_dn  # N-200   # N ;  N-per
per_beg = per_end - per
plot(df_matrix_pctchg_dn$es[per_beg:per_end] ~ df_matrix_pctchg_dn$btcusd[per_beg:per_end], cex=0.5)
abline(lm(df_matrix_pctchg_dn$es[per_beg:per_end] ~ df_matrix_pctchg_dn$btcusd[per_beg:per_end]))

plot(df_matrix_pctchg_up$es ~ df_matrix_pctchg_up$btcusd, cex=0.5)
abline(lm(df_matrix_pctchg_up$es ~ df_matrix_pctchg_up$btcusd))
N_up = nrow(df_matrix_pctchg_up)
per = 200
per_end = N_up  # N-200   # N ;  N-per
per_beg = per_end - per
plot(df_matrix_pctchg_up$es[per_beg:per_end] ~ df_matrix_pctchg_up$btcusd[per_beg:per_end], cex=0.5)
abline(lm(df_matrix_pctchg_up$es[per_beg:per_end] ~ df_matrix_pctchg_up$btcusd[per_beg:per_end]))


# ------------------------------------------------------------------------------
# btc<0> ~ es<-1> ; es <0
# ------------------------------------------------------------------------------
plot(y_dn ~ x_dn, cex=0.5)
abline(lm(y_dn ~ x_dn))
N_dn = nrow(df_matrix_pctchg_dn)
per = 800
per_end = N_dn  # N-200   # N ;  N-per
per_beg = per_end - per
plot(y_dn[per_beg:per_end] ~ x_dn[per_beg:per_end])
abline(lm(y_dn[per_beg:per_end] ~ x_dn[per_beg:per_end]))

# btc<0> ~ es<-1> ; es > 0
plot(y_up ~ x_up, cex=0.5)
abline(lm(y_up ~ x_up))
N_up = nrow(df_matrix_pctchg_up)
per = 200
per_end = N_up-100  # N-200   # N ;  N-per
per_beg = per_end - per
plot(y_up[per_beg:per_end] ~ x_up[per_beg:per_end])
abline(lm(y_up[per_beg:per_end] ~ x_up[per_beg:per_end]))



"""
--------------------------------------------------------------------------------
autoregressive btcusd
--------------------------------------------------------------------------------
"""
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


require(distr)
N = 1000
t <- 1:N
