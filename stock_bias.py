# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('whitegrid')


df = pd.read_csv('3049.TW.csv',index_col="Date")

df.head()

df.index = pd.to_datetime(df.index)

df.dropna(inplace=True)

df["Close"].plot()

price = df["Close"]
price

ma = price.rolling(60).mean()

price[-1000:].plot() #畫最後一千筆
ma[-1000:].plot()

#乖離率
bias = price/ma

bias.plot()

up = 1 + bias.rolling(60).std() * 1.5
lb = 1 - bias.rolling(60).std() * 1.5

up.plot()
lb.plot()
bias.plot()

price_after60_profit = price.shift(-60)/price

price

mydf = pd.DataFrame({
    'price': price,
    'bias': bias,
    'profit':price_after60_profit,
    'year': price.index.year
})

mydf.dropna(inplace=True)

sns.scatterplot(x='bias',y='profit',data=mydf)

sns.scatterplot(x="bias", y="profit", data=mydf,palette="Accent",hue='year',legend="full")
#hue:分顏色
#palette:色盤
#legend:不加不會全畫

fig,ax = plt.subplots(2,2)
ax[0] = sns.scatterplot(x="bias", y="profit", data=mydf['2020'],palette="Accent",hue='year',legend="full")
ax[0].set_title("3049")

###買進賣出策略
buy = (bias < lb) #如果<lower bond買入
sell = (bias > up) #如果>higher bond 賣出

hold = pd.Series(np.nan, index=price.index)
hold[buy] = 1
hold[sell] = 0
hold.plot()

hold = hold.ffill()
hold.plot()

#計算累積損益
profit = price.shift(-1)-price
cum_profit = profit.cumsum() #假設第一天是0 每一天累積的損益
cum_profit.plot()

#持有期間才會有損益
profit[hold==0] = 0
cum_profit = profit.cumsum()
cum_profit.plot()

#最佳化參數
def bia_strategy_withCost_best(p1,p2,p3,p4,draw_plot=False):
    ma = price.rolling(p1).mean()
    bias = price/ma
    ub =1+ bias.rolling(p2).std() * p3
    lb = 1 - bias.rolling(p2).std() * p4

    buy = (bias < lb) #如果>lower bond買入
    sell = (bias > ub) #如果<higher bond 賣出

    hold = pd.Series(np.nan, index=price.index)
    hold[buy] = 1
    hold[sell] = 0
    hold = hold.ffill()  #往前填值
    profit = price.shift(-1)-price
    profit[hold!=1] = 0 #持有期間才會賺錢  
    cum_profit = profit.cumsum().shift(1)
    if(draw_plot):
        cum_profit.plot()
    return 1000*cum_profit.dropna().iloc[-1]

vmax = 0 
for p1 in range(10,120,10):
  for p2 in range(10,120,10):
    v = bia_strategy_withCost_best(p1,p2,1.5,1.5)
    if v>vmax:
      vmax=v
      print(vmax,p1,p2,1.5,1.5)

bia_strategy_withCost_best(110,100,1.5,1.5,True)

