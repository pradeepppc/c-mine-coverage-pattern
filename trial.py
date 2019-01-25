l = [1, 2, 3, 4, 5]
print(l[0:len(l) - 1])

from bitarray import bitarray
b = bitarray(10)
print(b)

import itertools
a = ['acasc', 'cabc', 'cacc']
b = list(itertools.combinations(a, 2))
print(list(b[0]))


for item in l:
    if item == 2:
        l.remove(2)
    else:
        continue

print(l)