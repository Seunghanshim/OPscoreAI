from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np
from sklearn.preprocessing import StandardScaler
import pandas as pd


def ensambel(tiker='BTC', per=10):
    df = pd.read_csv('csv/' + tiker + '_train.csv')
    label = pd.read_csv('csv/' + tiker + '_label' + str(per) + '.csv')

    df = df.drop(df.index[0:39])
    label = label.drop(label.index[0:39])
    df_y = label['label']
    df = df.drop(df.columns[0], axis=1)

    x_train, x_test, y_train, y_test = train_test_split(df, df_y, test_size = 0.3, random_state = 123)

    scalar = StandardScaler()
    x_train = scalar.fit_transform(x_train)
    x_test = scalar.fit_transform(x_test)

    x_train.shape
    y_train.shape

    RFC = RandomForestClassifier()
    RFC.fit(x_train, y_train)

    y_pred = RFC.predict(x_test)
    y_true = y_test

    acc = accuracy_score(y_true, y_pred)

    print('RFC 분류정확도 =', acc)

    LOG = LogisticRegression(C=100000, solver='newton-cg')
    LOG.fit(x_train, y_train)

    y_pred = LOG.predict(x_test)
    y_true = y_test

    acc = accuracy_score(y_true, y_pred)

    print('LOG 분류정확도 =', acc)

    SVM = SVC(probability=True)
    SVM.fit(x_train, y_train)

    y_pred = SVM.predict(x_test)
    y_true = y_test

    acc = accuracy_score(y_true, y_pred)

    print('SVM 분류정확도 =', acc)

    VOT = VotingClassifier(estimators=[('lr', LOG), ('rf', RFC), ('svc', SVM)], voting="soft")

    VOT.fit(x_train, y_train)

    y_pred = VOT.predict(x_test)
    y_true = y_test

    acc = accuracy_score(y_true, y_pred)

    print('VOT 분류정확도 =', acc)
    print(pd.crosstab(y_pred, y_test))

    all_x = scalar.fit_transform(df)
    all_y = df_y
    all_y_pred = VOT.predict(all_x)

    dd = pd.DataFrame()

    dd['label'] = df_y
    dd['pred'] = all_y_pred
    dd['band'] = df['band']

    print(pd.crosstab(dd['pred'], dd['label']))
