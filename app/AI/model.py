from PIL import ImageColor
import pandas as pd
import numpy as np
import colorsys
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow import keras

le = LabelEncoder()
ss = StandardScaler()
ct = ColumnTransformer(transformers=[('encode', OneHotEncoder(), [0])], remainder='passthrough')

df = pd.read_csv('AI/data.csv')

# --- Data
X_tot = df.iloc[:, [0, 2]].values
y = df.iloc[:, 1].values
X = X_tot[:, 0].tolist()


# --- HSL processing
for i in range(len(X)):
    if len(X[i]) < 7: X[i] = X[i] + "0"*(7-len(X[i]))
rgbs = [ImageColor.getcolor(val, "RGB") for val in X]
X = [colorsys.rgb_to_hls(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255) for rgb in rgbs]


# --- Encoding
X = np.array([list(X[i])+[X_tot[i, 1]] for i in range(len(X))])
y = le.fit_transform(y)


# --- Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12)
# X_train, X_test = ss.fit_transform(X_train), ss.transform(X_test)

X_train[:, :-1] = ss.fit_transform(X_train[:, :-1])
print('Prima', X_train[:, -1].tolist())
X_train[:, -1] = [float(val) for val in X_train[:, -1]]
print('Dopo', X_train[:, -1].tolist())
X_test[:, :-1] = ss.transform(X_test[:, :-1])
X_test[:, -1] = [float(val) for val in X_test[:, -1]]

# --- Model
class_n = max(y_train)+1
ANN = keras.models.Sequential()
ANN.add(keras.layers.Dense(units=16, activation='relu'))
ANN.add(keras.layers.Dense(units=64, activation='relu'))
ANN.add(keras.layers.Dense(units=128, activation='relu'))
ANN.add(keras.layers.Dense(units=255, activation='relu'))
ANN.add(keras.layers.Dense(units=class_n, activation='softmax'))

ANN.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=['accuracy'])

ANN.fit(X_train, y_train, batch_size=32, epochs=250)