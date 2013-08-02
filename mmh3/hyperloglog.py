
from collections import defaultdict
from hashlib import sha1

import random
import khmer
import sys
import mmh3
import math




class HyperLogLog(object):

    def __init__(self, b):
        self.b = b
        self.m = 1 << b
        self.data = [0]*self.m
        self.alphaMM = (0.7213 / (1 + 1.079 / self.m)) * self.m * self.m

       	num=random.randint( 0 , 4**21)
       	self.large_prime=self.get_large_prime(num,self.is_prime)

		
		      
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
        
    def add(self, o):
    	

    	
        x = mmh3.hash(str(o), 0)

        #x= o % self.large_prime
        x = long(sha1(str(o)).hexdigest(),16)

        
        a, b = 32-self.b, self.b

        i = x >> a

        
        v = self._bitscan(x << b, a)
        
        self.data[i] = max(self.data[i], v)
        
    def cardinality(self):
        estimate = self.alphaMM / sum([2**-v for v in self.data])
        if estimate <= 2.5 * self.m:
            zeros = float(self.data.count(0))
            return round(-self.m * math.log(zeros / self.m))
        else:
            return round(estimate)
        
    def _bitscan(self, x, m):
        v = 1
        while v<=m and not x&0x80000000:
            v+=1
            x<<=1
        return v


if __name__ == '__main__':
    
    k=21


    alphabet={0:'A',1:'T',2:'G',3:'C'}

    given_string=''

    for i in range(10000):
        given_string+=alphabet[random.randint(0,3)]
    
    
    H = HyperLogLog(8)

    d=defaultdict(int)

    for i in range(len(given_string)-k+1):
        d[given_string[i:i+k]] += 1
        H.add(khmer.forward_hash(given_string[i:i+k],k))
        
    print 'Real:',len(d)
    print 'HyperLogLog(murmur3):', H.cardinality()
            
            
            
