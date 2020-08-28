import pandas as pd
import matplotlib.pyplot as plt

all = pd.read_csv("data.csv")
zz1 = pd.read_csv("zigzag.csv")
zz2 = pd.read_csv("zigzag2.csv")

zz1.columns = ['idx', 'oz', 'hz', 'lz', 'cz', 'vz', 'wz']
zz2.columns = ['idx2', 'oz2', 'hz2', 'lz2', 'cz2', 'vz2', 'wz2']


label = 1 # 하락
if zz1.iloc[0][6] == 0:
    label = 3 # 상승

all['label'] = label
cnt = 1
for i in range(1, len(all.index) - 1):
    all['label'][i] = label
    if cnt < len(zz1.index) and i == zz1.iloc[cnt][0]:
        cnt += 1
        if label == 1: label = 3
        else: label = 1


bong_cnt = 18
sub_mx_mn = 1.08

tmp = 0
for i in range(0, len(zz1.index) - 2):
    tmp += 1
    label = all['label'][zz1.iloc[i][0]]

    if zz2.iloc[tmp][0] == zz1.iloc[i + 1][0]: continue
    else:
        lst = tmp
        while True:
            if zz2.iloc[lst + 1][0] == zz1.iloc[i + 1][0]: break
            lst += 1
        print(zz2.iloc[tmp][0], zz2.iloc[lst][0], zz1.iloc[i+1][0])
        mx = 0
        mn = all['close'][zz2.iloc[tmp][0]]
        cnt = 0
        for j in range(int(zz2.iloc[tmp][0]), int(zz2.iloc[lst][0])):
            cnt += 1
            mn = min([mn, all['close'][j]])
            mx = max([mx, all['close'][j]])

        if cnt < bong_cnt or mx < mn * sub_mx_mn:
            tmp = lst + 1
            continue
        else:
            for j in range(int(zz2.iloc[tmp][0]), int(zz2.iloc[lst][0])):
                all['label'][j] = 2
        tmp = lst + 1

all.to_csv("data2.csv", index=False)




