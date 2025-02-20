#!/usr/bin/env python3

import openai
import config  # contains ENCRYPTED_KEY

import sys
import base64
from hashlib import sha256
from cryptography.fernet import Fernet, InvalidToken

def decrypt_api_key(encrypted_key: bytes, passphrase: str) -> str:
    """Try to decrypt the API key using the passphrase. Raise an exception if invalid."""
    key_bytes = sha256(passphrase.encode("utf-8")).digest()
    fernet_key = base64.urlsafe_b64encode(key_bytes)
    cipher = Fernet(fernet_key)

    try:
        decrypted = cipher.decrypt(encrypted_key)
    except InvalidToken:
        raise ValueError("Invalid passphrase or corrupted encrypted key.")

    return decrypted.decode("utf-8")

def main():
    # Prompt user for passphrase to decrypt the key
    passphrase = input("Enter passphrase to unlock API key: ").strip()

    # Decrypt the stored key or exit if incorrect
    try:
        openai.api_key = decrypt_api_key(config.ENCRYPTED_KEY, passphrase)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Fetch and list all models accessible with this API key
    models = openai.Model.list()
    for m in models["data"]:
        print(m["id"])

if __name__ == "__main__":
    main()
