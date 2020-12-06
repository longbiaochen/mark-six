from matplotlib import pyplot
from pandas import read_csv

# %% load data
dataframe = read_csv("../data/special.csv", header=None)
# dataframe = read_csv("../data/fake.csv", header=None)
dataset = dataframe.values[:, 0]
print dataset.shape
print dataset.max()

pyplot.hist(dataset, 49)
pyplot.show()


# %%
sum = 0
for i in range(1, 12):
    sum += 12 / i
print sum
