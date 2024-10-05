class MersenneTwister:
    def __init__(self, seed):
        self.w, self.n, self.m, self.r = 32, 624, 397, 31
        self.a = 0x9908b0df
        self.u, self.d = 11, 0xffffffff
        self.s, self.b = 7, 0x9d2c5680
        self.t, self.c = 15, 0xefc60000
        self.l = 18
        self.f = 1812433253

        # Initialize the state array with the seed
        self.index = self.n
        self.mt = [0] * self.n
        self.mt[0] = seed
        for i in range(1, self.n):
            self.mt[i] = self.int_32(self.f * (self.mt[i - 1] ^ self.mt[i - 1] >> (self.w - 2)) + i)

    def int_32(self, x):
        return int(0xffffffff & x)

    def twist(self):
        for i in range(self.n):
            x = self.int_32((self.mt[i] & 0x80000000) + (self.mt[(i + 1) % self.n] & 0x7fffffff))
            xA = x >> 1
            if x % 2 != 0:
                xA ^= self.a
            self.mt[i] = self.mt[(i + self.m) % self.n] ^ xA
        self.index = 0

    def random(self):
        if self.index >= self.n:
            self.twist()

        y = self.mt[self.index]
        y ^= (y >> self.u) & self.d
        y ^= (y << self.s) & self.b
        y ^= (y << self.t) & self.c
        y ^= y >> self.l

        self.index += 1
        return self.int_32(y)

    def randint(self, low, high):
        return low + self.random() % (high - low)


# Example of using the MersenneTwister class
seed = 12345
mt = MersenneTwister(seed)

# Generate a sequence of random integers
N = 100  # Upper limit for random numbers (exclusive)
n = 10000000  # Number of random numbers

sequence = [mt.randint(0, N) for _ in range(n)]

# Save the sequence to a CSV file
import pandas as pd

filename = "10M2.csv"
df = pd.DataFrame(sequence, columns=["RandomNumbers"])
df.to_csv(filename, index=False, header=True)

# Optionally, print the first few rows for verification
print(df.head())
