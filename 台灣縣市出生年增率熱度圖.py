# -*- coding: utf-8 -*-
#https://data.gov.tw/dataset/14233 資料來源

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

st = "10001"  #起始月
yr = datetime.today().year - 1911
mn = datetime.today().month
nowym = str(yr) + "0" + str(mn) #最新當月

url = "https://statis.moi.gov.tw/micst/stmain.jsp?sys=220&kind=21&type=1&funid=c0120101&cycle=41&outmode=12&utf=1&compmode=0&outkind=3&fldspc=0,7,&codspc0=0,2,3,2,6,1,9,1,12,1,15,16,&rdm=eqrNnoet&ym="+ st +"&ymt="+ nowym 
df = pd.read_csv( url )

#資料清理，新增縣市欄位
df["出生人數"] = df["出生人數"].str.replace("<br>"," ")
df["縣市"] = df["出生人數"].str.split(" ").str[2]
df = df.fillna("")
df.loc[df["縣市"] == "","縣市"] = df[df["縣市"] == ""]["出生人數"].str.split(" ").str[1] + "(總合)"

#轉換數字型態
for i in range(1,4):
    df.iloc[:,i] = df.iloc[:,i].str.replace(",","")
    df.iloc[:,i] = pd.to_numeric(df.iloc[:,i] , errors="coerce")
for i in range(4,8):
    df.iloc[:,i] = pd.to_numeric(df.iloc[:,i] , errors="coerce")

cityAll = df.groupby("縣市").get_group("區域別總計(總合)") #抽出全縣市總合
cityAll["year"] = cityAll["出生人數"].str[0:3] #建立年份欄位

cityList = df["縣市"][1:23] #取得全台縣市名字列表
dfCity = pd.DataFrame( index = cityAll["year"] ) #建立一個空的df

#增加每個城市的欄位，並轉換成年增率
for city in cityList : 
    dfCity[city] = df.groupby("縣市").get_group(city)["出生人數(人)"].pct_change().values
dfCity = dfCity[1:].T #欄位倒轉

plt.figure(dpi=200)
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei' #中文
plt.rcParams['axes.unicode_minus'] = False #負數

sns.heatmap( dfCity, cmap = 'coolwarm', yticklabels = dfCity.index.str[0:3],annot=True, fmt = ".2f" , annot_kws={"size" : 5},center=0)
plt.title("各縣市出生人口年增率變化(%)")
plt.savefig("各縣市出生人口年增率熱度圖.png",bbox_inches='tight')


