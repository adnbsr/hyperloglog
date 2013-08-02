from pylab import *
import khmer
import random
from collections import defaultdict
from khmer_hll import KmerCardinality

def trial():

	k=22
	
	counter=KmerCardinality(8,k,4**(k/4),4**(k))
	
	alphabet={0:'A',1:'T',2:'G',3:'C'}
	
	given_string=''
	
	for i in range(1000):
		given_string+=alphabet[random.randint(0,3)]
	
	
	counter.consume(given_string)
	#counter.consume_file('*.fa')
	
	d=defaultdict(int)
	
	
	
	for i in range(len(given_string)-k+1):
		d[given_string[i:i+k]] += 1

	real_num=len(d)
	estimated = counter.cardinality() 

	error_rate=abs(real_num - estimated )/real_num
	

	if error_rate < 1:
		print counter.large_prime/float(4**k) , error_rate 
	else:
		print 'irrelevant'
	
for i in range(5):
	trial()