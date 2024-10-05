import sys
import random
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import pandas as pd

# AES-based RNG
class AESRNG:
    def __init__(self, seed):
        self.key = seed
        self.cipher = AES.new(self.key, AES.MODE_ECB)
        self.counter = 0

    def random_int(self):
        self.counter += 1
        counter_bytes = self.counter.to_bytes(16, 'big')
        encrypted = self.cipher.encrypt(counter_bytes)
        rand_int = int.from_bytes(encrypted, 'big')
        return rand_int

# Mersenne Twister RNG (from mersenne_twister.py)
class MersenneTwister:
    def __init__(self, seed):
        self.w, self.n, self.m, self.r = 32, 624, 397, 31
        self.a = 0x9908b0df
        self.u, self.d = 11, 0xffffffff
        self.s, self.b = 7, 0x9d2c5680
        self.t, self.c = 15, 0xefc60000
        self.l = 18
        self.f = 1812433253

        self.index = self.n
        self.mt = [0] * self.n
        self.mt[0] = seed
        for i in range(1, self.n):
            self.mt[i] = self.int_32(self.f * (self.mt[i - 1] ^ (self.mt[i - 1] >> (self.w - 2)) + i))

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

# Command parsing function
def parse_command(args):
    command = {}
    for i in range(len(args)):
        if args[i] == '-rw':
            command['writeSeed'] = True
        elif args[i] == '-n':
            command['count'] = int(args[i+1])
        elif args[i] == '-s':
            command['seed'] = int(args[i+1], 16)
        elif args[i] == '-r':
            command['range'] = int(args[i+1])
        elif args[i] == '-f':
            command['outputFile'] = args[i+1]
        elif args[i] == '-sf':
            command['seedFile'] = args[i+1]
        elif args[i] == '-rng':
            command['rng'] = args[i+1]
    return command

# Function to select the RNG based on the command
def choose_rng(rng_name, seed=None):
    if rng_name == 'mersenne':
        return MersenneTwister(seed)
    elif rng_name == 'aes':
        return AESRNG(seed)
    else:
        raise ValueError(f"Unknown RNG: {rng_name}")

# Function to generate binary sequence
def generate_binary_sequence(rng, count):
    byte_count = (count + 7) // 8
    binary_data = bytearray()
    for _ in range(byte_count):
        byte = 0
        for bit in range(8):
            if len(binary_data) * 8 + bit < count:
                byte |= (rng.random_int() & 1) << (7 - bit)
        binary_data.append(byte)
    return binary_data

# Function to generate range sequence
def generate_range_sequence(rng, range_, count):
    return [str(rng.random_int() % range_) for _ in range(count)]

# Main tool function
def rng_tool(args):
    command = parse_command(args)
    seed = command.get('seed', random.randint(0, 0xFFFFFFFF))
    rng = choose_rng(command.get('rng', 'mersenne'), seed)

    # Write seed to file if needed
    if command.get('writeSeed') and 'seedFile' in command:
        with open(command['seedFile'], 'w') as sf:
            sf.write(f"Seed: {seed}")

    # Generate binary sequence
    if command['outputFile'].endswith('.bin'):
        binary_data = generate_binary_sequence(rng, command['count'])
        with open(command['outputFile'], 'wb') as f:
            f.write(binary_data)
        print(f"Binary file written to {command['outputFile']}")
    
    # Generate range sequence
    elif command['outputFile'].endswith('.txt') and 'range' in command:
        number_sequence = generate_range_sequence(rng, command['range'], command['count'])
        with open(command['outputFile'], 'w') as f:
            f.write("\n".join(number_sequence))
        print(f"Text file with number sequence written to {command['outputFile']}")
    
    else:
        print("Unsupported file format or missing parameters.")

# Command-line usage
if __name__ == "__main__":
    rng_tool(sys.argv[1:])
