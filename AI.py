import talib
import pyupbit
import numpy as np
import pandas as pd
from fbprophet import Prophet

df2 = pd.DataFrame({"ds": [], "y": []})

df = pyupbit.get_ohlcv("KRW-BTC", interval="day",count=400)

print(df)

for j in range(0, len(df.index)):
    df2 = df2.append(pd.DataFrame({"ds": [df.index[j]], "y": [df.iloc[j][3]]}), ignore_index=True)

print(df2)

m = Prophet()
m.fit(df2)
future = m.make_future_dataframe(periods=20)
future.tail()
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
fig2 = m.plot_components(forecast)
fig2.show()