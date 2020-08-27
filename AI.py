import talib
import numpy as np
import CreateCsv
import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt



df2 = pd.DataFrame({"ds": [], "y": []})

df = pd.read_csv("data.csv")
df = CreateCsv.get_ohlcv()

for i in range(0, len(df.index)):
    # df2 = df2.append(pd.DataFrame({"ds": [df.iloc[i][0]], "y": [df.iloc[i][4]]}), ignore_index=True)
    df2 = df2.append(pd.DataFrame({"ds": [df.index[i]], "y": [df.iloc[i][3]]}), ignore_index=True)

m = Prophet()
m.fit(df2)
future = m.make_future_dataframe(periods=1)
future.tail()
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
fig2 = m.plot_components(forecast)
fig2.show()
