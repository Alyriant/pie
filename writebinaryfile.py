from array import array
from random import random

NUM_FLOATS = 10**7
FILENAME = 'floats.bin'

generator = (random() for i in range(NUM_FLOATS))
floats = array('d', generator)
print(floats[-1])

fp = open(FILENAME, 'wb')
floats.tofile(fp)
fp.close()

floats2 = array('d')
fp = open(FILENAME,'rb')
floats2.fromfile(fp, NUM_FLOATS)
fp.close()

print(floats2[-1])

