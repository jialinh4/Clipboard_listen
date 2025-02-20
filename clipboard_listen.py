#!/usr/bin/env python3

import time
import pyperclip
import openai
import config

import sys
import base64
from hashlib import sha256
from cryptography.fernet import Fernet, InvalidToken

MODEL_NAME = "o1-mini"  # Or any valid model you have access to

def decrypt_api_key(encrypted_key: bytes, passphrase: str) -> str:
    """Try to decrypt the API key using the passphrase. Raise an exception if invalid."""
    key_bytes = sha256(passphrase.encode("utf-8")).digest()
    fernet_key = base64.urlsafe_b64encode(key_bytes)
    cipher = Fernet(fernet_key)

    # Attempt to decrypt
    try:
        decrypted = cipher.decrypt(encrypted_key)
    except InvalidToken:
        raise ValueError("Invalid passphrase or corrupted encrypted key.")

    return decrypted.decode("utf-8")

def get_chatgpt_response(prompt):
    """Send the prompt to the selected model using openai==0.28.x ChatCompletion."""
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()

def main():
    print("Script is running successfully...")

    # Prompt user for passphrase
    passphrase = input("Enter passphrase to unlock API key: ").strip()

    # Decrypt the stored encrypted key (or exit if passphrase is wrong)
    try:
        openai.api_key = decrypt_api_key(config.ENCRYPTED_KEY, passphrase)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    prev_clipboard = pyperclip.paste()
    listening_for_query = False

    while True:
        current_text = pyperclip.paste()
        if current_text != prev_clipboard:
            prev_clipboard = current_text
            print("Successfully received the clipboard:", current_text)

            # 1) If we see "###"
            if current_text == "###":
                listening_for_query = True
            # 2) If the script is waiting for a query
            elif listening_for_query:
                listening_for_query = False
                query = current_text
                try:
                    answer = get_chatgpt_response(query)
                    print("Successfully received the ChatGPT response.")
                    pyperclip.copy(answer)
                except Exception as e:
                    pyperclip.copy(f"Error from ChatGPT: {str(e)}")

        time.sleep(1)

if __name__ == "__main__":
    main()
