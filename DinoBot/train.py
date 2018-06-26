import matplotlib.pyplot as plt
from sklearn import datasets
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.externals import joblib

X = pd.read_excel("./csv/input_teste.xlsx",sheet_name="Planilha2")
y = pd.read_excel("./csv/output_teste.xlsx",sheet_name="Planilha1")
np_X = np.ndarray(X.shape)
np_y = np.ndarray(y.shape)
np_X[X.index]=X.values
np_y[y.index]=y.values
X_train, X_test, y_train, y_test = train_test_split(np_X,np_y, test_size=0.3, random_state=0)

sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

ppn = Perceptron(n_iter=20000, eta0=0.001, random_state=0)
#ppn = joblib.load('trainned.pkl')
ppn.fit(X_train_std, y_train)
y_pred = ppn.predict(X_test_std)
print('Missclassified samples: %d' % (y_test != y_pred).sum())
print('Accuracy: %.2f' % accuracy_score(y_test, y_pred))

teste = sc.transform([[0.557692308,0.3,0.25],
                      [0.357692308,0.3,0.25],
                      [0.034615385,0.3,0.25],
                      [1.1,0,0]])

print("Predict {}".format(ppn.predict(teste)))

joblib.dump(ppn, 'trainned_new.pkl')
