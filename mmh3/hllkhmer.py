import random,khmer,sys, mmh3, math





class HyperLogLog:

    def __init__(self, log2m):
        self.log2m = log2m
        self.m = 1 << log2m
        self.data = [0]*self.m
        self.alphaMM = (0.7213 / (1 + 1.079 / self.m)) * self.m * self.m
        
    def add(self, o,k):
        
        x=mmh3.hash(str(0),0)

        a, b = 32-self.log2m, self.log2m

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
    
    k=12

    kt=khmer.new_ktable(k)

    alphabet={0:'A',1:'T',2:'G',3:'C'}

    given_string=''

    for i in range(1000):
        given_string+=alphabet[random.randint(0,3)]
    
    n=kt.consume(given_string)
    H = HyperLogLog(8)


    for i in range(n):
        H.add(given_string[i:i+k],k)
        

    print 'HyperLogLog(murmur3):', H.cardinality()
            
            
            
