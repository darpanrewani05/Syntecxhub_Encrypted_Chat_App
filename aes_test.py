from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
import os

# Secret key (32 bytes)
key = b'12345678901234567890123456789012'

# Random IV
iv = os.urandom(16)

# Message
message = "Hello Darpan"

# Padding
padder = PKCS7(128).padder()
padded = padder.update(message.encode()) + padder.finalize()

# Encrypt
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(padded) + encryptor.finalize()

print("Encrypted:", ciphertext)


# Decrypt
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
decryptor = cipher.decryptor()
decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

unpadder = PKCS7(128).unpadder()
decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

print("Decrypted:", decrypted.decode())
