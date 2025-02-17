from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# Load the secret key from file
with open("secret_key.txt", "r") as key_file:
    secret_key = key_file.read()

# Ensure the key is 16, 24, or 32 bytes (AES-128, AES-192, AES-256)
key = secret_key[:32].encode().ljust(32, b'\0')  # Pad with null bytes if needed

# Simulating the AES Encryption Process
print("\n--- AES Encryption Process ---")

# Person A wants to send a message to Person B securely using AES
plaintext = "Hallelujah."
print("Plaintext Message:", plaintext)

# Generate a random IV
iv = os.urandom(16)
cipher = AES.new(key, AES.MODE_CBC, iv)

# Encrypt the message
ciphertext = iv + cipher.encrypt(pad(plaintext.encode(), AES.block_size))
print("Encrypted Message (Hex):", ciphertext.hex())

# Simulating the AES Decryption Process
print("\n--- AES Decryption Process ---")

# Person B receives the encrypted message from Person A and decrypts it
received_iv = ciphertext[:16]  # Extract IV
received_ciphertext = ciphertext[16:]  # Extract encrypted part

# Decrypt the message
cipher = AES.new(key, AES.MODE_CBC, received_iv)
decrypted_text = unpad(cipher.decrypt(received_ciphertext), AES.block_size).decode()

print("Decrypted Message:", decrypted_text)
