from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import random

# Load the secret key from file
with open("secret_key.txt", "r") as key_file:
    secret_key = key_file.read()

# Ensure the key is 16, 24, or 32 bytes
key = secret_key[:32].encode().ljust(32, b'\0')

# Simulating the AES Encryption Process
print("\n--- AES Encryption Process ---")

plaintext = "This is a secret message."
print("Plaintext Message:", plaintext)

# Generate a random IV
iv = os.urandom(16)
cipher = AES.new(key, AES.MODE_CBC, iv)

# Encrypt the message
ciphertext = iv + cipher.encrypt(pad(plaintext.encode(), AES.block_size))
print("Original Encrypted Message (Hex):", ciphertext.hex())

# Simulating Bit Error Introduction
print("\n--- Introducing Bit Error in Ciphertext ---")

corrupted_ciphertext = bytearray(ciphertext)

# Pick a random byte index (excluding IV)
random_index = random.randint(16, len(ciphertext) - 1)
random_bit = 1 << random.randint(0, 7)  # Pick a random bit to flip in that byte

# Flip the bit
corrupted_ciphertext[random_index] ^= random_bit
corrupted_ciphertext = bytes(corrupted_ciphertext)

print("Corrupted Encrypted Message (Hex):", corrupted_ciphertext.hex())

# Simulating the AES Decryption Process with Bit Error
print("\n--- AES Decryption with Bit Error ---")

try:
    received_iv = corrupted_ciphertext[:16]  # Extract IV
    received_ciphertext = corrupted_ciphertext[16:]  # Extract corrupted encrypted data

    cipher = AES.new(key, AES.MODE_CBC, received_iv)
    decrypted_text = unpad(cipher.decrypt(received_ciphertext), AES.block_size).decode()

    print("Decrypted Message:", decrypted_text)
except Exception as e:
    print("Decryption Error:", e)
