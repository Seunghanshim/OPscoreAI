import numpy as np
import pandas as pd
from sklearn import metrics
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("csv/final.csv")
df2 = pd.read_csv("csv/data2_7.csv")
df = df.drop(df.index[0:39])
df2 = df2.drop(df2.index[0:39])
df_y = df2['label']
df = df.drop(df.columns[0], axis=1)

print(df_y)

scalar = StandardScaler()

train_x = scalar.fit_transform(df[np.arange(len(df)) % 5 != 4])
train_y = df_y[np.arange(len(df_y)) % 5 != 4]
test_x = scalar.fit_transform(df[np.arange(len(df)) % 5 == 4])
test_y = df_y[np.arange(len(df_y)) % 5 == 4]

log_reg = LogisticRegression(C=100000, solver='newton-cg')
log_reg.fit(train_x, train_y)

x2 = sm.add_constant(df)
model = sm.OLS(df_y, x2)
result = model.fit()

print(result.summary())

y_pred = log_reg.predict(test_x)
print('정확도 : ', metrics.accuracy_score(test_y, y_pred))

print(pd.crosstab(y_pred, test_y))
