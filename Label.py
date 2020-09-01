import pandas as pd
import talib
import matplotlib.pyplot as plt


def getLabel(tiker='BTC', per=10):
    all = pd.read_csv("csv/" + tiker + "_ohlcv.csv")
    zz = pd.read_csv("csv/" + tiker + "_zigzag" + str(per) + ".csv")

    label = 3 # 상승
    if zz.iloc[0][6] == 0:
        label = 1 # 하락

    all['label'] = label
    cnt = 0
    for i in range(0, len(all.index) - 1):
        if cnt < len(zz.index) and i == zz.iloc[cnt][0]:
            cnt += 1
            if label == 1: label = 3
            else: label = 1
        all['label'][i] = label

    up, mid, lw = talib.BBANDS(all.close, 7, 2, 2, 0)

    for i in range(0, len(all.index)):
        if 100.0 * (up[i] - lw[i]) / mid[i] < 5:
            all['label'][i] = 2

    all.to_csv("csv/" + tiker + "_label" + str(per) + ".csv", index=False)
