from crypto_utils import encrypt_message, decrypt_message

msg = "Hello Secure Chat"

encrypted = encrypt_message(msg)

print("Encrypted:", encrypted)

decrypted = decrypt_message(encrypted)

print("Decrypted:", decrypted)
