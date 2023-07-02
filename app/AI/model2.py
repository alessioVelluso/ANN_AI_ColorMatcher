from PIL import ImageColor
import pandas as pd
import numpy as np
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


# --- RGB processing
for i in range(len(X)):
    if len(X[i]) < 7: X[i] = X[i] + "0"*(7-len(X[i]))
X = [ImageColor.getcolor(val, "RGB") for val in X]


# --- Encoding
X = np.array([list(X[i])+[X_tot[0, 1]] for i in range(len(X))])
y = le.fit_transform(y)


# --- Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12)
X_train, X_test = ss.fit_transform(X_train), ss.transform(X_test)


# --- Model
class_n = max(y_train)+1
ANN = keras.models.Sequential()
ANN.add(keras.layers.Dense(units=6, activation='relu'))
ANN.add(keras.layers.Dense(units=9, activation='relu'))
ANN.add(keras.layers.Dense(units=6, activation='relu'))
ANN.add(keras.layers.Dense(units=class_n, activation='softmax'))

ANN.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=['accuracy'])

ANN.fit(X_train, y_train, batch_size=64, epochs=500)




""" Try 1 

X = positive_df.iloc[:, 0].values.reshape(-1, 1)
y = positive_df.iloc[:, 1].values

X = ct.fit_transform(X).toarray()
y = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=12)


# ---------------------------- Model
class_n = max(y_train)+1
ANN = keras.models.Sequential()
ANN.add(keras.layers.Dense(units=6, activation='relu'))
ANN.add(keras.layers.Dense(units=9, activation='relu'))
ANN.add(keras.layers.Dense(units=6, activation='relu'))
ANN.add(keras.layers.Dense(units=class_n, activation='softmax'))

ANN.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=['accuracy'])

ANN.fit(X_train, y_train, batch_size=10, epochs=300) """