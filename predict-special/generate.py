import random
import numpy

fake = []
for i in range(151):
    fake.append(random.randint(1, 49))

numpy.savetxt("../data/fake.csv", fake, '%d')

print fake
