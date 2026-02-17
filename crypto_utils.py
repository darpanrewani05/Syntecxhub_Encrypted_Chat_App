from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
import os

# 32-byte secret key (must be same for client and server)
KEY = b'12345678901234567890123456789012'


# 🔐 Encrypt Function
def encrypt_message(message):

    # Generate random IV
    iv = os.urandom(16)

    # Padding
    padder = PKCS7(128).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()

    # Encrypt
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv))
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Return IV + ciphertext
    return iv + ciphertext



# 🔓 Decrypt Function
def decrypt_message(encrypted_data):

    # Extract IV
    iv = encrypted_data[:16]

    # Extract ciphertext
    ciphertext = encrypted_data[16:]

    # Decrypt
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv))
    decryptor = cipher.decryptor()

    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove padding
    unpadder = PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

    return decrypted.decode()
