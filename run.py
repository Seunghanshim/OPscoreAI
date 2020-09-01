import CreateCsv
import Zigzag
import Label
import band_cci_adx_obv as ind1
import RSI_SMI_MACD as ind2
import ensamble as es
import pandas as pd

tiker = 'BTC'

# CreateCsv.getCSV() # open, high, low, close, volume을 upbit에서 가져옴=
# Zigzag.getZigzag(tiker, 10)
# Zigzag.getZigzag(tiker, 7)
# Zigzag.getZigzag(tiker, 5)
#
# Label.getLabel(tiker, 10)
# Label.getLabel(tiker, 7)
# Label.getLabel(tiker, 5)

df = pd.read_csv('csv/' + tiker + '_month.csv')
df2 = ind1.getIndi(tiker)
df3 = ind2.getIndi(tiker)

df['band'] = df2['band']
df['cci'] = df2['cci']
df['adx'] = df2['adx']
df['obv'] = df2['obv']
df['smi'] = df3['smi']
df['macd'] = df3['macd']

df.to_csv('csv/' + tiker + '_train.csv')

es.ensambel(tiker, 10)
es.ensambel(tiker, 7)
es.ensambel(tiker, 5)


