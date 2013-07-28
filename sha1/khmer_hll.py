import khmer
import screed


from hashlib import sha1
import bisect
import math

class KmerCardinality(object):

	def __init__(self,b,k):
		self.k=k
		self.b=b
		self.bits=self.b
		self.alpha=self.get_alpha(self.b)
		self.num_bins= 1 << self.bits
		self.bit_bins=[ 1L << i for i in range(160 - self.bits + 1) ]
		self.estimators = [0 for i in range(self.num_bins)]
	
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


	#def get_word(self, **args):
	def add(self,word):
		
		hash = long(sha1(word).hexdigest(), 16)
		bin = hash & ((1 << self.bits) - 1)
		remaining_bits = hash >> self.bits
		count = self.rho(remaining_bits)
		self.estimators[bin] = max(self.estimators[bin], count)

	def rho(self,w):
		return len(self.bit_bins) - bisect.bisect_right(self.bit_bins, w)
	


	def cardinality(self):
		E = self.alpha * float(len(self.estimators) ** 2) / sum(math.pow(2.0, -x) for x in self.estimators)
		
		if E <= 2.5 * self.bits:
			V = self.estimators.count(0)
			return self.estimators * math.log(self.estimators/ float(V)) if V > 0 else E
		elif E <= float(1L << 160) / 30.0:
			return round(E)
		else:
			return -(1L << 160) * math.log(1.0 - E / (1L << 160))

	def consume(self,sequence):
		kt=khmer.new_ktable(self.k)
		n=kt.consume(sequence)
		for i in range(n):
			self.add(sequence[i:i+self.k])



		
	def consume_fasta(self,fasta_file):
		for record in screed.fasta.fasta_iter(open(fasta_file)):
			self.consume(record['sequence'])



		

