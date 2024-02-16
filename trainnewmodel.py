# modules
import pandas as pd
import numpy as np
import sklearn
from keras.models import load_model
import tensorflow as tf



# for modeling
import keras
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.keras.regularizers import l1_l2
from tensorflow.keras.layers.experimental.preprocessing import CategoryEncoding
from keras.models import Sequential
from keras.layers import Dense, BatchNormalization,Dropout
from keras.utils import to_categorical 
from keras.callbacks import EarlyStopping
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import autokeras as ak
# Split your dataset into training and test sets

teamsAllStats2=pd.read_csv("teamsAllStats2.csv")

x=teamsAllStats2[['Rating','openRating','openminRating','openmaxRating','ratingPis','ratingminPis','ratingmaxPis','minRating'
                  ,'maxRating','Kda','minKda',"maxKda"
                ,'last10']]
y=teamsAllStats2[['Result']]

scaler = StandardScaler()
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

es = EarlyStopping(monitor='val_loss', 
                                   mode='min', # don't minimize the accuracy!
                                   patience=10,
                                   restore_best_weights=True)

model = Sequential()
model.add(BatchNormalization())
model.add(Dense(32, input_shape=([X_train.shape[1],]), activation='LeakyReLU', kernel_regularizer=l1_l2(l1=0.005, l2=0.005))) # Add an input shape! (features,)
model.add(Dropout(0.4))
model.add(Dense(32, activation='LeakyReLU',kernel_regularizer=l1_l2(l1=0.005, l2=0.005)))
model.add(Dropout(0.3))
model.add(Dense(1, activation='sigmoid'))
model.build(input_shape=(None, X_train.shape[1]))
model.summary()

# compile the model
model.compile(loss=BinaryCrossentropy(),  # Use BinaryCrossentropy for binary classification
            optimizer=Adam(0.0005),
              metrics=['accuracy'])

history = model.fit(X_train,
                    y_train,
                    epochs=800, # you can set this to a big number!
                    batch_size=8,
                    validation_data=(X_test, y_test),
                    shuffle=True,
                    callbacks=[es],
                    verbose=1)

model.evaluate(X_test, y_test)


model.save('autokeras_modelsolo6.keras')
