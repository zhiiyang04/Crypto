import random
import math

# Miller-Rabin Primality Test
def is_prime(n, k=5):  
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits=2048):
    while True:
        p = random.getrandbits(bits)
        if is_prime(p):
            return p

def generate_rsa_keys():
    p = generate_prime()
    q = generate_prime()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    while math.gcd(e, phi) != 1: 
        e = random.randint(2, phi - 1)
    d = pow(e, -1, phi)  # Modular inverse
    return ((e, n), (d, n))

def encrypt_secret_key(secret_key, public_key):
    e, n = public_key
    cipher_text = [pow(ord(char), e, n) for char in secret_key]
    return cipher_text

def decrypt_secret_key(encrypted_key, private_key):
    d, n = private_key
    decrypted_text = ''.join([chr(pow(char, d, n)) for char in encrypted_key])
    return decrypted_text

# Simulating the process
print("Generating RSA Key Pair for Person B...")
public_key, private_key = generate_rsa_keys()

# Assume Person A generates a secret key for AES
secret_symmetric_key = "SpidermanIsReal"
print("Secret Key to be shared:", secret_symmetric_key)

# Person A encrypts the secret key using Person B's public key
encrypted_key = encrypt_secret_key(secret_symmetric_key, public_key)
print("Encrypted Secret Key:", encrypted_key)

# Person B decrypts the secret key using their private key
decrypted_key = decrypt_secret_key(encrypted_key, private_key)
print("Decrypted Secret Key:", decrypted_key)

# Save the decrypted secret key to a file
with open("secret_key.txt", "w") as key_file:
    key_file.write(decrypted_key)
print("Secret Key saved to secret_key.txt")
