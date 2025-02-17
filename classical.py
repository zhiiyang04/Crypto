import time
import numpy as np
from itertools import product

import time
import numpy as np
from itertools import product

# Playfair Cipher Implementation
class PlayfairCipher:
    def __init__(self, key):
        self.key = key
        self.matrix = self.construct_matrix()
    
    def construct_matrix(self):
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        key_string = "".join(dict.fromkeys(self.key.upper().replace("J", "I") + alphabet))
        matrix = np.array(list(key_string)).reshape(5, 5)
        print("\nPlayfair Cipher Key Matrix:")
        for row in matrix:
            print(" ".join(row))
        return matrix
    
    def locate_pair(self, char):
        row, col = np.where(self.matrix == char)
        return row[0], col[0]
    
    def encrypt_pair(self, a, b):
        row_a, col_a = self.locate_pair(a)
        row_b, col_b = self.locate_pair(b)
        if row_a == row_b:
            encrypted = self.matrix[row_a, (col_a + 1) % 5] + self.matrix[row_b, (col_b + 1) % 5]
        elif col_a == col_b:
            encrypted = self.matrix[(row_a + 1) % 5, col_a] + self.matrix[(row_b + 1) % 5, col_b]
        else:
            encrypted = self.matrix[row_a, col_b] + self.matrix[row_b, col_a]
        print(f"Encrypting Pair {a}{b} -> {encrypted} (RowA:{row_a}, ColA:{col_a}, RowB:{row_b}, ColB:{col_b})")
        return encrypted
    
    def decrypt_pair(self, a, b):
        row_a, col_a = self.locate_pair(a)
        row_b, col_b = self.locate_pair(b)
        if row_a == row_b:
            decrypted = self.matrix[row_a, (col_a - 1) % 5] + self.matrix[row_b, (col_b - 1) % 5]
        elif col_a == col_b:
            decrypted = self.matrix[(row_a - 1) % 5, col_a] + self.matrix[(row_b - 1) % 5, col_b]
        else:
            decrypted = self.matrix[row_a, col_b] + self.matrix[row_b, col_a]
        print(f"Decrypting Pair {a}{b} -> {decrypted} (RowA:{row_a}, ColA:{col_a}, RowB:{row_b}, ColB:{col_b})")
        return decrypted
    
    def process_text(self, text):
        text = text.upper().replace("J", "I").replace(" ", "")
        processed = ""
        i = 0
        while i < len(text):
            a = text[i]
            b = text[i + 1] if i + 1 < len(text) and text[i] != text[i + 1] else "X"
            processed += a + b
            i += 2 if b != "X" else 1
        print(f"Processed Text for Playfair: {processed}")
        return processed
    
    def encrypt(self, text):
        text = self.process_text(text)
        pairs = [text[i:i+2] for i in range(0, len(text), 2)]
        print("\nPlayfair Encryption Steps:")
        encrypted_text = "".join(self.encrypt_pair(p[0], p[1]) for p in pairs)
        print(f"Final Playfair Encrypted Text: {encrypted_text}\n")
        return encrypted_text
    
    def decrypt(self, text):
        pairs = [text[i:i+2] for i in range(0, len(text), 2)]
        print("\nPlayfair Decryption Steps:")
        decrypted_text = "".join(self.decrypt_pair(p[0], p[1]) for p in pairs)
        print(f"Final Playfair Decrypted Text: {decrypted_text}\n")
        return decrypted_text

# Rail Fence Cipher Implementation
def rail_fence_encrypt(text, depth):
    rail = [['\n' for _ in range(len(text))] for _ in range(depth)]
    dir_down = False
    row, col = 0, 0
    for char in text:
        if row == 0 or row == depth - 1:
            dir_down = not dir_down
        rail[row][col] = char
        col += 1
        row += 1 if dir_down else -1
    
    print("\nRail Fence Encryption Pattern:")
    for r in rail:
        print(" ".join(c if c != '\n' else ' ' for c in r))
    
    return "".join([c for row in rail for c in row if c != '\n'])

def rail_fence_decrypt(text, depth):
    rail = [['\n' for _ in range(len(text))] for _ in range(depth)]
    dir_down = None
    row, col = 0, 0
    for i in range(len(text)):
        if row == 0:
            dir_down = True
        if row == depth - 1:
            dir_down = False
        rail[row][col] = '*'
        col += 1
        row += 1 if dir_down else -1
    
    index = 0
    for i in range(depth):
        for j in range(len(text)):
            if rail[i][j] == '*' and index < len(text):
                rail[i][j] = text[index]
                index += 1
    
    print("\nRail Fence Decryption Pattern:")
    for r in rail:
        print(" ".join(c if c != '\n' else ' ' for c in r))
    
    result = []
    row, col = 0, 0
    for i in range(len(text)):
        if row == 0:
            dir_down = True
        if row == depth - 1:
            dir_down = False
        result.append(rail[row][col])
        col += 1
        row += 1 if dir_down else -1
    return "".join(result)

# Product Cipher Combination
def product_cipher_encrypt(plain_text, playfair_key, rail_depth):
    playfair = PlayfairCipher(playfair_key)
    encrypted_playfair = playfair.encrypt(plain_text)
    print(f"After Playfair Encryption: {encrypted_playfair}")
    encrypted_final = rail_fence_encrypt(encrypted_playfair, rail_depth)
    print(f"After Rail Fence Encryption: {encrypted_final}")
    return encrypted_final

def product_cipher_decrypt(cipher_text, playfair_key, rail_depth):
    decrypted_rail = rail_fence_decrypt(cipher_text, rail_depth)
    print(f"After Rail Fence Decryption: {decrypted_rail}")
    playfair = PlayfairCipher(playfair_key)
    decrypted_final = playfair.decrypt(decrypted_rail)
    print(f"After Playfair Decryption: {decrypted_final}")
    return decrypted_final

# Command-line Input Handling
if __name__ == "__main__":
    plaintext = input("Enter the text to encrypt: ")
    key = input("Enter Playfair key: ")
    depth = int(input("Enter Rail Fence depth: "))
    
    cipher_text = product_cipher_encrypt(plaintext, key, depth)
    print(f"Final Encrypted: {cipher_text}")
    
    decrypted_text = product_cipher_decrypt(cipher_text, key, depth)
    print(f"Final Decrypted: {decrypted_text}")
