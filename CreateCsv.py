import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import datetime
from datetime import datetime as dt, timedelta as td
import time


def requests_retry_session(retries=5, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    s = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    s.mount('http://', adapter)
    s.mount('https://', adapter)
    return s


def _call_public_api(url, **kwargs):
    try:
        resp = requests_retry_session().get(url, params=kwargs)
        contents = resp.json()
        return contents
    except Exception as x:
        print("It failed", x.__class__.__name__)
        return None


def get_ohlcv(ticker="KRW-BTC", interval="day", count=200, to="2020-08-25 09:00:00"):
    """
    일 캔들 조회
    :return:
    """
    try:
        if interval is "day":
            url = "https://api.upbit.com/v1/candles/days"
        elif interval is "minute1":
            url = "https://api.upbit.com/v1/candles/minutes/1"
        elif interval is "minute3":
            url = "https://api.upbit.com/v1/candles/minutes/3"
        elif interval is "minute5":
            url = "https://api.upbit.com/v1/candles/minutes/5"
        elif interval is "minute10":
            url = "https://api.upbit.com/v1/candles/minutes/10"
        elif interval is "minute15":
            url = "https://api.upbit.com/v1/candles/minutes/15"
        elif interval is "minute30":
            url = "https://api.upbit.com/v1/candles/minutes/30"
        elif interval is "minute60":
            url = "https://api.upbit.com/v1/candles/minutes/60"
        elif interval is "minute240":
            url = "https://api.upbit.com/v1/candles/minutes/240"
        elif interval is "week":
            url = "https://api.upbit.com/v1/candles/weeks"
        elif interval is "month":
            url = "https://api.upbit.com/v1/candles/months"
        else:
            url = "https://api.upbit.com/v1/candles/days"

        contents = _call_public_api(url, market=ticker, count=count, to=to)
        dt_list = [datetime.datetime.strptime(x['candle_date_time_kst'], "%Y-%m-%dT%H:%M:%S") for x in contents]
        df = pd.DataFrame(contents, columns=['opening_price', 'high_price', 'low_price', 'trade_price',
                                             'candle_acc_trade_volume'],
                          index=dt_list)
        df = df.rename(
            columns={"opening_price": "open", "high_price": "high", "low_price": "low", "trade_price": "close",
                     "candle_acc_trade_volume": "volume"})
        return df.iloc[::-1]
    except Exception as x:
        print(x.__class__.__name__)
        return None


def getCSV(tiker='BTC'):
    d = dt.now()
    df = pd.DataFrame()
    while True:
        s = d.strftime('%Y-%m-%d %H:%M:%S')
        print(s)
        dft = get_ohlcv(ticker='KRW-' + tiker, interval="minute240", count=200, to=s)
        if len(dft.index) == 0:
            break
        df = df.append(dft)
        d -= td(hours=200)
        time.sleep(1)

    df = df.sort_index()
    df = df.groupby(level=0).first()

    df.to_csv('csv/' + tiker + '_ohlcv.csv', index=False)

    df2 = df
    df2['month'] = 1  # 1 ~ 12
    for i in range(0, len(df2.index)):
        df2['month'][i] = df2.index[i].month

    df2 = df2.drop(df2.columns[[0, 1, 2, 3, 4]], axis=1)
    df2.to_csv('csv/' + tiker + '_month.csv', index=False)

    return df


if __name__ == "__main__":
    d = dt.now()
    df = pd.DataFrame()
    while True:
        s = d.strftime('%Y-%m-%d %H:%M:%S')
        print(s)
        dft = get_ohlcv(ticker="KRW-BTC", interval="minute240", count=200, to=s)
        if len(dft.index) == 0:
            break
        df = df.append(dft)
        d -= td(hours=200)
        time.sleep(1)

    df = df.sort_index()
    df = df.groupby(level=0).first()

    df['day'] = 1  # 1 ~ 7
    df['month'] = 1  # 1 ~ 12
    for i in range(0, len(df.index)):
        df['day'][i] = df.index[i].weekday() + 1
        df['month'][i] = df.index[i].month

    df.to_csv('csv/data1.csv', index=False)
