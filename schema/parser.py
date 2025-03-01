from example import tables
from itertools import combinations

for x, y in combinations(tables, 2):
    # for z in x.values():
    #     print(z)
    for xx in x.values():
        print(xx)


def output():
    pass