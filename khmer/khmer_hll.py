import khmer
import screed
import random
import bisect
import math

from hashlib import sha1

class KmerCardinality(object):

	def __init__(self,b,k,lower_limit,upper_limit):
		self.k=k
		self.b=b
		self.alpha=self.get_alpha(self.b)
		self.num_bins= 1 << self.b
		self.bit_bins=[ 1L << i for i in range(160 - self.b + 1) ]
		self.estimators = [0 for i in range(self.num_bins)]
		num=random.randint( lower_limit , upper_limit)
		self.large_prime=self.get_large_prime(num,self.is_prime)
	
	def get_alpha(self, b):
		
		if not (4 <= b <= 16):
			raise ValueError("b=%d should be in range [4 : 16]" % b)
		
		if b == 4:
			return 0.673
		if b == 5:
			return 0.697
		if b == 6:
			return 0.709

		return 0.7213 / (1.0 + 1.079 / (1 << b))

	def mrange(self,start, stop, step):
		i = start
		while i < stop:
			yield i
			i += step
	
	def is_prime(self,n):
		if n == 2:
			return True
		if (n < 2) or (n % 2 == 0):
			return False
		return all(n % i for i in self.mrange(3, int(math.sqrt(n)) + 1, 2))

	def get_large_prime(self,n, tester):
		if tester(n):
			n += 1
		if (n % 2 == 0) and (n != 2):
			n += 1
		while True:
			if tester(n):
				break
			n += 2
		return n

	def add(self,khmer_hash):


		khmer_hash = khmer_hash % self.large_prime
		
		bin = khmer_hash & ((1 << self.b) - 1)
		remaining_bits = khmer_hash >> self.b
		count = self.rho(remaining_bits)
		self.estimators[bin] = max(self.estimators[bin], count)

	def rho(self,w):
		return len(self.bit_bins) - bisect.bisect_right(self.bit_bins, w)
	
	def cardinality(self):
		E = self.alpha * float(len(self.estimators) ** 2) / sum(math.pow(2.0, -x) for x in self.estimators)
		
		if E <= 2.5 * self.b:
			V = self.estimators.count(0)
			return round(self.estimators * math.log(self.estimators/ float(V)))
		else:
			return round(E)

	def consume(self,sequence):
		num_kmers = len(sequence) - self.k + 1 
		for i in range(num_kmers):
			self.add(khmer.forward_hash(sequence[i:i+self.k],self.k))
	
	def consume_fasta(self,fasta_file):
		for record in screed.fasta.fasta_iter(open(fasta_file)):
			self.consume(record['sequence'])



		

