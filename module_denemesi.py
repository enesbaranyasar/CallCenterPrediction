import random

import matplotlib.pyplot as plt

type(random)

import sklearn

from sklearn.linear_model import LinearRegression

liste = []
for i in range(100000):
    liste.append(random.Random().betavariate(3,5))

import matplotlib.pyplot as plt
liste = sorted(liste)
liste
plt.plot(liste)


liste = []
for i in range(100000):
    liste.append(random.Random().expovariate(.05))

import matplotlib.pyplot as plt
liste = sorted(liste)
liste
plt.plot(liste)
liste
liste

from collections import defaultdict,OrderedDict