# 資料來源 政府開放平台 https://data.gov.tw/dataset/151337

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

url = 'https://www.gender.ey.gov.tw/GecDB/Common/OpenXML.ashx?sn=6yrTVzOhjQtbqd8LlVgtKg@@'
df = pd.read_xml(url)

#年份處理
df['year'] = df["Period"].astype(str).str.replace("00","")
df.loc[df["year"] == '1', 'year'] = "100"

#只取總合欄位
dataTotal = df[df['Category1Title'] == '總計']

#取得每個工作類別
jobList = df['Category2Title'][0:19]

#最小年份跟最大年份，並輸出成一個df
yearStar , yearEnd = int(df['year'].head(1).values), int(df['year'].tail(1).values)
listAll = pd.DataFrame(index=(np.arange(yearStar,yearEnd+1)))

'''
#工作類型變為欄位，並除於1000，起始單元變為千元  參考中位數 center=30
#沒辦法客觀的看待各產業成長幅度，決定棄用
for job in jobList: 
    listAll[job] = dataTotal[dataTotal['Category2Title']==job]["Val"].values / 1000
'''

#工作類型變為欄位，並轉換為年增率百分比
for job in jobList: 
    listAll[job] = dataTotal[dataTotal['Category2Title']==job]["Val"].pct_change().values * 100
    

'''
#折線圖，呈現效果不佳，決定棄用
plt.figure(figsize=(50,20),dpi = 200)
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams['font.size'] = 24

for job in jobList:
    plt.plot(listAll.index,listAll[job],label=job)

plt.ylim(listAll.min().min(), listAll.max().max())
plt.xlim(yearStar, yearEnd)
plt.legend(loc='best', bbox_to_anchor=(1, 1))
plt.savefig("各產業經常性薪資變化.png")
'''

#熱度圖
listAll = listAll[1:].T
plt.figure(figsize=(35,10),dpi = 150)
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 16

sns.heatmap( listAll, cmap = 'coolwarm', annot=True, fmt = ".2f", annot_kws={"size" : 10},center=3, cbar_kws={"label":"百分比"})
plt.xlabel("民國年")
plt.title("各產業經常性薪資成長幅度")
plt.savefig("各產業經常性薪資成長幅度.png",bbox_inches='tight')

