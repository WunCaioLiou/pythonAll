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

#只取男女的資料
dataMale = df[df['Category1Title'] == '男']
dataFemale = df[df['Category1Title'] == '女']

#取得每個工作類別
jobList = df['Category2Title'][0:19]

#最小年份跟最大年份，並輸出成一個df
yearStar , yearEnd = int(df['year'].head(1).values), int(df['year'].tail(1).values)
joeListMale = pd.DataFrame(index=(np.arange(yearStar,yearEnd+1)))
joeListFemale = pd.DataFrame(index=(np.arange(yearStar,yearEnd+1)))

#工作類型變為欄位，values為Val
for job in jobList: 
    joeListMale[job] = dataMale[dataMale['Category2Title']==job]["Val"].values
    joeListFemale[job] = dataFemale[dataFemale['Category2Title']==job]["Val"].values


#折線圖
plt.figure(figsize=(35,20),dpi = 150)
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams['font.size'] = 16

count = 0
for job in jobList:
    count += 1
    plt.subplot(5,4,count)
    plt.plot(joeListMale.index, joeListMale[job], color="b",label="男")
    plt.plot(joeListFemale.index, joeListFemale[job], color="r",label="女")
    plt.ylim(joeListFemale.min().min(), joeListMale.max().max())
    plt.xlim(yearStar, yearEnd)
    plt.xticks(np.linspace(yearStar,yearEnd,15))
    if count == 1:
        plt.legend(loc=0)
    plt.title(job)

plt.suptitle("台灣經常性薪資變化，性別比較",fontsize=30)
plt.tight_layout()
plt.savefig("台灣經常性薪資變化_男女比較.png")




