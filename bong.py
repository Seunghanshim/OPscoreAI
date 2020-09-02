import pandas as pd


def getBong(tiker='BTC'):
    df = pd.read_csv('csv/' + tiker + '_ohlcv.csv')

    df['bong'] = 0
    for i in range(0, len(df.index)):
        if df['open'][i] > df['close'][i]:
            df['bong'][i] = 0
        else: df['bong'][i] = 1

    df = df.drop(df.columns[[0, 1, 2]], axis=1)

    df.to_csv('csv/' + tiker + '_bong_cv.csv', index=False)

    return df
