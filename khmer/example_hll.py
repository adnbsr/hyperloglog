from pylab import *
import khmer
import random
from collections import defaultdict
from khmer_hll import KmerCardinality



k=5

counter=KmerCardinality(8,k,4**(k/8),4**(k/2))

alphabet={0:'A',1:'T',2:'G',3:'C'}

given_string=''

for i in range(10000):
	given_string+=alphabet[random.randint(0,3)]


counter.consume(given_string)
#counter.consume_file('*.fa')

d=defaultdict(int)


kt=khmer.new_ktable(k)
n=kt.consume(given_string)

for i in range(n):
	d[given_string[i:i+k]] += 1

print 'Large Prime:',counter.large_prime
print 'Real:',round(len(d))
print 'Estimated:',counter.cardinality()
