import talib
import pandas as pd
from sympy import symbols
import numpy as np


def getIndi(tiker='BTC'):
    df = pd.read_csv("csv/" + tiker + "_ohlcv.csv")

    cci_ = talib.CCI(df.high, df.low, df.close, 14)
    cci_signal = talib.MA(cci_, 9, 0)

    mfi_ = talib.MFI(df.high, df.low, df.close, df.volume, 14)

    obv_ = talib.OBV(df.close, df.volume)
    obv_signal = talib.MA(obv_, 9, 0)

    adx_ = talib.ADX(df.high, df.low, df.close, 14)
    di_pl = talib.PLUS_DI(df.high, df.low, df.close, 14)
    di_mi = talib.MINUS_DI(df.high, df.low, df.close, 14)

    sar_ = talib.SAR(df.high, df.low, 0.02, 0.2)

    upperband, middleband, lowerband = talib.BBANDS(df.close, 7, 2, 2, 0)
    bandwidth = 100.0 * (upperband - lowerband) / middleband

    df['band'] = 0.0

    for i in range(0, len(bandwidth.index)):
        if bandwidth[i] < 5:
            df['band'][i] = 0.0
            continue
        df['band'][i] = bandwidth[i]

    df['cci'] = 0
    chk = 0
    for i in range(1, len(cci_.index)):
        if cci_[i] == cci_[i] and cci_signal[i] == cci_signal[i]:
            if cci_[i - 1] <= cci_signal[i - 1] and cci_[i] >= cci_signal[i]:
                if cci_[i] <= -100:
                    chk = 8
                elif cci_[i] <= 0:
                    chk = 7
                elif cci_[i] <= 100:
                    chk = 6
                else:
                    chk = 5
            elif cci_[i - 1] >= cci_signal[i - 1] and cci_[i] <= cci_signal[i]:
                if cci_[i] >= 100:
                    chk = 1
                elif cci_[i] >= 0:
                    chk = 2
                elif cci_[i] >= -100:
                    chk = 3
                else:
                    chk = 4
            df['cci'][i] = chk

    df['adx'] = 0
    chk1 = 0
    chk2 = 0
    chk3 = 0
    chk4 = 0
    chk5 = 0
    chk6 = 0
    max_ = 0
    min_ = 0
    for i in range(1, len(df.index)):
        if di_pl[i] == di_pl[i] and di_mi[i] == di_mi[i] and adx_[i] == adx_[i] and sar_[i] == sar_[i]:
            if adx_[i] >= 20:
                if sar_[i] >= df['close'][i]:
                    chk1 = 0
                else:
                    chk1 = 1
            else:
                chk1 = 2

            if di_pl[i - 1] < di_mi[i - 1] and di_pl[i] > di_mi[i]:
                chk2 = 1
                chk5 = 0
                chk6 = 0
                if chk3 == 0:
                    max_ = i
                elif df['close'][i] >= df['high'][max_]:
                    chk4 = 1
                chk3 = 1
            elif di_pl[i - 1] > di_mi[i - 1] and di_pl[i] < di_mi[i]:
                chk2 = 2
                chk3 = 0
                chk4 = 0
                if chk5 == 0:
                    min_ = i
                elif df['close'][i] <= df['low'][min_]:
                    chk6 = 1
                chk5 = 1

            if chk1 == 0:
                if chk2 == 1:
                    if chk4 == 1:
                        df['adx'][i] = 12
                    else:
                        df['adx'][i] = 11
                else:
                    if chk6 == 1:
                        df['adx'][i] = 9
                    else:
                        df['adx'][i] = 10
            elif chk1 == 1:
                if chk2 == 1:
                    if chk4 == 1:
                        df['adx'][i] = 4
                    else:
                        df['adx'][i] = 3
                else:
                    if chk6 == 1:
                        df['adx'][i] = 1
                    else:
                        df['adx'][i] = 2
            else:
                if chk2 == 1:
                    if chk4 == 1:
                        df['adx'][i] = 8
                    else:
                        df['adx'][i] = 7
                else:
                    if chk6 == 1:
                        df['adx'][i] = 5
                    else:
                        df['adx'][i] = 6

    df['obv'] = 0

    for i in range(len(df.index)):
        if obv_[i] == obv_[i] and obv_signal[i] == obv_signal[i]:
            df['obv'][i] = obv_[i] - obv_signal[i]

    df = df.drop(df.columns[[0, 1, 2, 3, 4]], axis=1)

    df.to_csv("csv/" + tiker + "_indi1.csv", index=False)

    return df
