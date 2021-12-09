import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
  tf.config.experimental.set_memory_growth(gpu, True)

X_train, X_test, Y_train, Y_test = np.load('전처리후 학습코드', allow_pickle=True) #전처리파일 위치
model = Sequential()
model.add(Embedding(47335, 300, input_length=2000))   #Embeddiong 숫자 바꾸기
model.add(Conv1D(32, kernel_size=5, padding='same',
                 activation='relu'))
model.add(MaxPool1D(pool_size=1))
model.add(LSTM(128, activation='tanh',
               return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh',
               return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh'))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(10, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy']) #loss
fit_hist = model.fit(X_train, Y_train, batch_size=100, epochs=8, validation_data=(X_test, Y_test))

model.save('저장모델이름'.format(fit_hist.history['val_accuracy'][-1])) #저장모델파일명입력

plt.plot(fit_hist.history['accuracy'], label='accuracy')
plt.plot(fit_hist.history['val_accuracy'], label='val accuracy')
plt.legend()
plt.show()