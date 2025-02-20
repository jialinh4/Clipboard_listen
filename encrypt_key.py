# encrypt_key.py
from cryptography.fernet import Fernet
import base64, os
from hashlib import sha256

def main():
    openai_key = input("Enter your REAL OpenAI API key: ").strip()
    passphrase = input("Enter a short passphrase (something easy to remember): ").strip()

    # Derive a 32-byte key from the passphrase
    # (Here we use a simple SHA-256; more secure would be a PBKDF2 with a salt)
    key_bytes = sha256(passphrase.encode("utf-8")).digest()
    fernet_key = base64.urlsafe_b64encode(key_bytes)
    cipher = Fernet(fernet_key)

    # Encrypt the real API key
    encrypted_key = cipher.encrypt(openai_key.encode("utf-8"))

    print("\nCopy this encrypted key and store it somewhere safe (e.g., config.py):")
    print(encrypted_key)

if __name__ == "__main__":
    main()
