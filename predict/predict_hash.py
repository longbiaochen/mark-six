import numpy
import pandas
import string

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense

alphabet = "abcdefghijklmnopqrstuvwxyz1234567890"
char_to_int = dict((c, i) for i, c in enumerate(alphabet))
int_to_char = dict((i, c) for i, c in enumerate(alphabet))


def create_dataset(data):
    dataX = []
    print [char_to_int[char] for char in data[0]]
    for i in range(data.shape[0]):
        dataX.append([char_to_int[char] for char in data[i]])

    return numpy.array(dataX)


# load data
dataframe = pandas.read_csv("../data/X.csv", header=None)
dataset = dataframe.values[:, 0]
print dataset[0]
X = create_dataset(dataset)
X = X / float(len(alphabet))

#%%
dataframe = pandas.read_csv("../data/y.csv", header=None)
dataset = dataframe.values[:, 0]
y = pandas.get_dummies(pandas.Series(list(dataset)).astype(
    'category', categories=list(string.ascii_lowercase)))
print y.shape

# %%

n_features = 49
code = one_hot_encode(dataset, n_features)

train_size = int(len(dataset) * 0.67)
test_size = len(dataset) - train_size
train, test = code[0:train_size, :], code[train_size:len(code), :]
print(code.shape, train.shape, test.shape)

# reshape into X=t and Y=t+1
look_back = 32
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)
print trainX.shape, trainY.shape
print one_hot_decode(trainX[0, :, :]), one_hot_decode([trainY[0]])

# %% define model
hidden_size = 64
model = Sequential()
model.add(LSTM(hidden_size, input_shape=(
    look_back, n_features), return_sequences=True))
model.add(LSTM(hidden_size, input_shape=(look_back, n_features)))
model.add(Dense(n_features, activation='softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['acc'])
print(model.summary())

# fit model
model.fit(trainX, trainY, epochs=1000, batch_size=8, verbose=1)

# %% evaluate model with training set
scores = model.evaluate(trainX, trainY)
print("Model Accuracy: %.2f%%" % (scores[1] * 100))
trainYhat = model.predict(trainX)
for i in range(trainX.shape[0]):
    print [one_hot_decode(trainX[i, :, :]), one_hot_decode(
        [trainY[i]]), one_hot_decode([trainYhat[i]])]

# %% evaluate model with test set
scores = model.evaluate(testX, testY)
print("Model Accuracy: %.2f%%" % (scores[1] * 100))
testYhat = model.predict(testX)
for i in range(testX.shape[0]):
    print [one_hot_decode(testX[i, :, :]), one_hot_decode(
        [testY[i]]), one_hot_decode([testYhat[i]])]
