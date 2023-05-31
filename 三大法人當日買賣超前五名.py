# 資料來源 台灣證卷交易所
# TWT44U 投信 TW38U 外資 TWT43U 自營商

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from datetime import datetime
import time
import requests
import json

def numeric(d): 
    for s in range(0,2): #清理字串空格
        d.iloc[:,s] = d.iloc[:,s].str.replace(" ",'')
    
    for s in range(2,5):  #將股數從字串轉換成數字
        d.iloc[:,s] = d.iloc[:,s].str.replace(",",'')
        d.iloc[:,s] = pd.to_numeric(d.iloc[:,s] , errors="coerce") 
        
    d = d.sort_values("買賣超股數",ascending=False) 
    return d

def dataGet(x):
    dtime = str(datetime.today()).split(" ")[0].replace("-","")  #最新日期
    while True : #如果當日資訊還未更新，就在往前一天取資料
        url = 'https://www.twse.com.tw/rwd/zh/fund/TWT'+ str(x) +'U?date='+ dtime +'&response=json'
        time.sleep(2) #避免過快讀取，被伺服器鎖定
        resp = requests.get(url)
        data = json.loads(resp.text) 
        if len(data) >= 8:
            break
        else:
            print(dtime+"未取得資料，在往前抓取")
            dtime = str(int(dtime)-1)
    return data

#投信
Tdata = dataGet(44) 
Ttitle = Tdata["title"].replace("彙總表","前五名") #取得標題
Tdf = pd.DataFrame(Tdata["data"],columns=Tdata["fields"])
Tdf = Tdf.iloc[:,1:]
Tdf = numeric(Tdf)

#外資
Ydata = dataGet(38)  
Ytitle = Ydata["title"].replace("彙總表","前五名") #取得標題
Ydf = pd.DataFrame(Ydata["data"],columns=Ydata["fields"])
Ydf = pd.concat([Ydf.iloc[:,1:3],Ydf.iloc[:,9:]],axis=1) #只取總數
Ydf = numeric(Ydf)

#自營商
Zdata = dataGet(43)  
Ztitle = Zdata["title"].replace("彙總表","前五名") #取得標題
Zdf = pd.DataFrame(Zdata["data"],columns=Zdata["fields"])
Zdf = pd.concat([Zdf.iloc[:,0:2],Zdf.iloc[:,8:]],axis=1) #只取總數
Zdf = numeric(Zdf)

plt.figure(figsize=[10,25], dpi=300, facecolor="#dde094")
plt.rcParams['font.sans-serif'] = 'DFKai-SB' #中文
plt.rcParams['axes.unicode_minus'] = False  #負號顯示

#投信資料繪圖
plt.subplot(311)
x1 = Tdf["證券名稱"].head(5)
x2 = Tdf[::-1]["證券名稱"].head(5)
plt.bar(x1, Tdf["買賣超股數"].head(5)/1000, width=0.4,color="r") #買超
plt.bar(x2, Tdf[::-1]["買賣超股數"].head(5)/1000, width=0.4,color="g") #賣超
plt.xticks(rotation=45)
plt.ylabel("千股")
plt.title(Ttitle)
plt.grid()

#外資資料繪圖
plt.subplot(312)
x1 = Ydf["證券名稱"].head(5)
x2 = Ydf[::-1]["證券名稱"].head(5)
plt.bar(x1, Ydf["買賣超股數"].head(5)/1000, width=0.4,color="r") 
plt.bar(x2, Ydf[::-1]["買賣超股數"].head(5)/1000, width=0.4,color="g")
plt.xticks(rotation=45)
plt.ylabel("千股")
plt.title(Ytitle)
plt.grid()

#自營商資料繪圖
plt.subplot(313)
x1 = Zdf["證券名稱"].head(5)
x2 = Zdf[::-1]["證券名稱"].head(5)
plt.bar(x1, Zdf["買賣超股數"].head(5)/1000, width=0.4,color="r")
plt.bar(x2, Zdf[::-1]["買賣超股數"].head(5)/1000, width=0.4,color="g")
plt.xticks(rotation=45)
plt.ylabel("千股")
plt.title(Ztitle)
plt.grid()

plt.tight_layout() 
plt.savefig("三大法人當日買賣超前5名")


