import talib
import pyupbit
import numpy as np
import pandas as pd


def slope(x, y, t):
    return (y - x) / t


def getIndi(tiker='BTC'):
    df = pd.read_csv("csv/" + tiker + "_ohlcv.csv")

    mfi_ = talib.MFI(df.high, df.low, df.close, df.volume, 14)

    SMI_value = pd.DataFrame({"SMI": [], "SIG": [], "VAL": []})

    # 0 = open 1 = high 2 = low 3 = close 4 = volume

    df["smi"] = 0
    df["macd"] = 0

    high_ = []
    low_ = []

    sm_list = []
    period1 = 13
    period2 = 25
    period3 = 2
    period4 = 4

    for i in range(0, period1 - 1):
        high_.append(999999999)
        low_.append(999999999)

    for i in range(period1 - 1, len(df.index)):
        highest = 0
        lowest = 999999999
        for j in range(i - (period1 - 1), i + 1):
            if highest < df.iloc[j][1]:
                highest = df.iloc[j][1]
            if lowest > df.iloc[j][2]:
                lowest = df.iloc[j][2]
        high_.append(highest)
        low_.append(lowest)

    for i in range(0, period1 - 1):
        sm_list.append(999999999)

    for i in range(period1 - 1, len(df.index)):
        sm_list.append(float(df.iloc[i][3]) - float(high_[i] + low_[i]) / 2)

    aa1 = []

    for i in range(0, period2 - 1):
        aa1.append(999999999)

    for i in range(period2 - 1, len(df.index)):
        sum_ = 0
        for j in range(i - (period2 - 1), i + 1):
            sum_ = sum_ + sm_list[j]
        aa1.append(float(sum_) / float(period2))

    aa2 = []

    for i in range(0, period2 + period3 - 2):
        aa2.append(999999999)

    for i in range(period2 + period3 - 2, len(df.index)):
        sum_ = 0
        for j in range(i - (period3 - 1), i + 1):
            if aa1[j] == 999999999:
                break
            sum_ = sum_ + aa1[j]
        aa2.append(float(sum_) / float(period3))

    aa3 = []

    for i in range(0, period2 + period1 - 2):
        aa3.append(999999999)

    for i in range(period2 + period1 - 2, len(df.index)):
        sum_ = 0
        for j in range(i - (period2 - 1), i + 1):
            if high_[j] == 999999999:
                break
            if low_[j] == 999999999:
                break
            sum_ = sum_ + (high_[j] - low_[j])
        aa3.append(float(sum_) / float(period2))

    aa4 = []

    for i in range(0, period2 + period1 + period3 - 3):
        aa4.append(999999999)

    for i in range(period2 + period1 + period3 - 3, len(df.index)):
        sum_ = 0
        for j in range(i - (period3 - 1), i + 1):
            if aa3[j] == 999999999:
                break
            sum_ = sum_ + aa3[j]
        aa4.append(float(sum_) / float(period3))

    smi_list = []

    for i in range(0, period1 + period2 + period3 - 3):
        smi_list.append(999999999)

    for i in range(period1 + period2 + period3 - 3, len(df.index)):
        smi_list.append(aa2[i] / (aa4[i] / 2) * 100)

    smi_signal = []

    for i in range(0, period1 + period2 + period3 + period4 - 4):
        smi_signal.append(999999999)

    for i in range(period1 + period2 + period3 + period4 - 4, len(df.index)):
        sum_ = 0
        for j in range(i - (period4 - 1), i + 1):
            sum_ = sum_ + smi_list[j]
        smi_signal.append(float(sum_) / float(period4))

    SMI_value['SMI'] = smi_list
    SMI_value['SIG'] = smi_signal
    SMI_value.iloc[0][2] = 0

    for i in range(1, len(SMI_value.index)):
        if SMI_value.iloc[i][0] == 999999999 or SMI_value.iloc[i][1] == 999999999 or SMI_value.iloc[i-1][0] == 999999999 or SMI_value.iloc[i-1][1] == 999999999:
            SMI_value.iloc[i][2] = 5
        elif SMI_value.iloc[i - 1][0] <= SMI_value.iloc[i - 1][1] and SMI_value.iloc[i][0] >= SMI_value.iloc[i][1]:
            if SMI_value.iloc[i - 1][0] <= -40 or SMI_value.iloc[i][0] <= -40:
                SMI_value.iloc[i - 1][2] = 9
                SMI_value.iloc[i][2] = 9
            else:
                SMI_value.iloc[i - 1][2] = 8
                SMI_value.iloc[i][2] = 8
        elif SMI_value.iloc[i-1][0] >= SMI_value.iloc[i-1][1] and SMI_value.iloc[i][0] <= SMI_value.iloc[i][1]:
            if SMI_value.iloc[i-1][0] >= 40 or SMI_value.iloc[i][0] >= 40:
                SMI_value.iloc[i-1][2] = 1
                SMI_value.iloc[i][2] = 1
            else:
                SMI_value.iloc[i-1][2] = 2
                SMI_value.iloc[i][2] = 2
        else:
            if SMI_value.iloc[i][0] >= 40:
                SMI_value.iloc[i][2] = 7
            elif SMI_value.iloc[i][0] >= 0:
                SMI_value.iloc[i][2] = 6
            elif SMI_value.iloc[i][0] <= -40:
                SMI_value.iloc[i][2] = 4
            elif SMI_value.iloc[i][0] <=0:
                SMI_value.iloc[i][2] = 3

    for i in range(0, len(SMI_value.index)):
        df['smi'][i] = SMI_value.iloc[i][2]

    macd, macdsignal, macdhist = talib.MACD(df.close, 12, 26, 9)

    for i in range(1, len(macd.index)):
        if macd[i] == macd[i] and macdsignal[i] == macdsignal[i]:
            if macd[i-1] - macdsignal[i-1] < 0 < macd[i] - macdsignal[i]:
                df['macd'][i] = 6
            elif macd[i-1] - macdsignal[i-1] > 0 > macd[i] - macdsignal[i]:
                df['macd'][i] = 1
            else:
                sl = macd[i] - macd[i-1]
                if macd[i] <= 0 and sl <= 0:
                    df['macd'][i] = 2
                elif macd[i] <= 0 and sl >= 0:
                    df['macd'][i] = 4
                elif macd[i] >= 0 and sl <= 0:
                    df['macd'][i] = 3
                else:
                    df['macd'][i] = 5

    df = df.drop(df.columns[[0, 1, 2, 3, 4]], axis=1)

    df.to_csv("csv/" + tiker + "_indi2.csv")

    return df
