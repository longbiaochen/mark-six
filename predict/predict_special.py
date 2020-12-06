import numpy
from pandas import read_csv
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense


def one_hot_encode(sequence, n_features):
    encoding = list()
    for value in sequence:
        vector = [0 for _ in range(n_features)]
        vector[value - 1] = 1
        encoding.append(vector)
    return numpy.array(encoding)


def one_hot_decode(code):
    return [(numpy.argmax(vector) + 1) for vector in code]


def create_dataset(data, look_back=1):
    dataX, dataY = [], []
    for i in range(data.shape[0] - look_back - 1):
        dataX.append(data[i:(i + look_back), :])
        dataY.append(data[i + look_back, :])
    return numpy.array(dataX), numpy.array(dataY)


# %% load data
dataframe = read_csv("../data/special.csv", header=None)
# dataframe = read_csv("../data/fake.csv", header=None)
dataset = dataframe.values[:, 0]
print dataset.shape

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
