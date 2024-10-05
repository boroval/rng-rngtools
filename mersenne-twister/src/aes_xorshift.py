import numpy as np
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
# Parametry
n = 1000000
N = 37

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
        return rand_int % N

# Inicializace AES RNG se seedem
seed = get_random_bytes(16)
aes_rng = AESRNG(seed)

# Generování sekvence pomocí AES RNG
sequence_aes = [aes_rng.random_int() for _ in range(n)]

# Uložení sekvence do CSV souboru
filename_aes = "10M_AES_cisla9.csv"
np.savetxt(filename_aes, sequence_aes, fmt='%d', delimiter=",")

print(f"AES čísla uložena do {filename_aes}")
