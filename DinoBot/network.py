import numpy as np
from sklearn.linear_model import Perceptron
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
from sklearn.cross_validation import train_test_split
import pandas as pd

class Network:
    def __init__(self):
        self.input_size = 3
        self.hidden_size = 4
        self.output_size = 1
        self.W1 = np.random.randn(self.input_size, self.hidden_size)
        self.W2 = np.random.randn(self.hidden_size, self.output_size)
        self.fitness = 0

    def forward(self, inputs):
        self.z2 = np.dot(inputs, self.W1)
        self.a2 = np.tanh(self.z2)
        self.z3 = np.dot(self.a2, self.W2)
        yHat = self.sigmoid(self.z3)
        return yHat

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

class Load_Network():
    def __init__(self):
        self.ppn = joblib.load('trainned_ga.pkl')
        X = pd.read_excel("./csv/input_ga.xlsx",sheet_name="Planilha1")
        y = pd.read_excel("./csv/output_ga.xlsx",sheet_name="Planilha1")
        np_X = np.ndarray(X.shape)
        np_y = np.ndarray(y.shape)
        np_X[X.index]=X.values
        np_y[y.index]=y.values
        X_train, _, _, _ = train_test_split(np_X,np_y, test_size=0.3, random_state=0)
        self.sc =StandardScaler()
        self.sc.fit(X_train)

    def predict(self,inputs):
        inputs = self.sc.transform([inputs])
        return self.ppn.predict(inputs)
