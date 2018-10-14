import math, numbers, sys, logging
import numpy as np

log = logging.getLogger('root')

class Histogram: 
    def __init__(self, name, lower, upper, binWidth = 1):
        self.name       = name
        self.lower      = lower
        self.upper      = upper
        self.binWidth   = binWidth
        
        self.bins       = [0 for x in np.arange(lower, upper, binWidth)]
        self.binCount   = len(self.bins)
        self.totalCount = 0

    def bin(self, value):
        b = int(math.floor(self.binCount * (value - self.lower) / (self.upper - self.lower)))
        if b < 0 or b >= self.binCount:
            raise KeyError("Value outside permissible range")
        else:
            return b

    def key(self, bin):
        return (self.lower + bin * self.binWidth)

    def add(self, value):
        try:
            self.bins[self.bin(value)] += 1
            self.totalCount += 1
        except KeyError:
            log.warning("Could not add value {}".format(value))

    def normalize(self):
        if self.count > 0:
            for bin in self.bins:
                self.bin /= self.totalCount
            self.totalCount = 1

        return self

    def tsv(self, file = sys.stdout): 
        print("# Histogram \"{}\" ({} to {}, bin width {})".format(self.name, self.lower, self.upper, self.binWidth), file = file)
        for bin, count in enumerate(self.bins):
            print("{key:12.6f}\t{value:16.6f}".format(
                key         = self.key(bin),
                value       = count,
            ), file = file)

    @staticmethod
    def processTSV(file, name, min, max, step, column):
        result = Histogram(name, min, max, step)

        for line in open(file, 'r'):
            if line[0] == '#':
                continue

            values = line.rstrip('\n').split()
            result.add(float(values[column]))

        return result

    def __matmul__(self, other):
        return self.chiSquare(other)

    def chiSquare(self, other):
        if self.lower != other.lower or self.upper != other.upper or self.binWidth != other.binWidth:
            raise Exception("Incompatible histograms")

        if self.totalCount == 0 or other.totalCount == 0:
            return 2
    
        sum = 0

        self.normalize()
        other.normalize()

        for bin, count in enumerate(self.bins):
            denom = count + other.bins[bin]
            if denom > 0:
                sum += (count - other.bins[bin])**2 / denom

        return sum

