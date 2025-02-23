#!/usr/bin/env python3

import time
import pyperclip
import openai
import config

import sys
import base64
import requests
import socket
from hashlib import sha256
from cryptography.fernet import Fernet, InvalidToken

def decrypt_api_key(encrypted_key: bytes, passphrase: str) -> str:
    key_bytes = sha256(passphrase.encode("utf-8")).digest()
    fernet_key = base64.urlsafe_b64encode(key_bytes)
    cipher = Fernet(fernet_key)
    try:
        decrypted = cipher.decrypt(encrypted_key)
    except InvalidToken:
        raise ValueError("Invalid passphrase or corrupted encrypted key.")
    return decrypted.decode("utf-8")

def get_chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model=config.MODEL_NAME,  # use the model from config.py
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()

def main():
    print("Script is running successfully...")

    # 1) Prompt for passphrase to unlock the OpenAI key
    passphrase = input("Enter passphrase to unlock API key: ").strip()

    gpt_enabled = False
    try:
        openai.api_key = decrypt_api_key(config.ENCRYPTED_KEY, passphrase)
        gpt_enabled = True
    except ValueError as e:
        print(f"GPT features disabled: {e}")
        print("You can still attempt to use chat room features.")

    # 2) Prompt for chat username
    username = input("Enter your username for the chat room (optional if server not available): ").strip()

    # 3) Prompt the user for the server IP
    host = input(f"Enter the chat server IP (LAN address), or leave empty for none: ").strip()
    if not host:
        host = None

    connected_to_server = False
    SERVER_URL = None

    if host:
        # build "http://<host>:<port>"
        test_url = f"http://{host}:{config.PORT}"
        print(f"Attempting to connect to chat server at {test_url} ...")
        try:
            r = requests.get(f"{test_url}/messages", timeout=5)
            if r.status_code == 200:
                # check data type
                data = r.json()
                if isinstance(data, list):
                    print(f"Successfully connected to chat server at {test_url}")
                    connected_to_server = True
                    SERVER_URL = test_url
                else:
                    print("Server responded with unexpected data (not a list). Disabling chat features.")
            else:
                print(f"Warning: server responded with status {r.status_code}. Chat may not work.")
        except Exception as e:
            print(f"Could not connect to server at {test_url}. Chat features disabled.")
            print(f"Details: {e}")
    else:
        print("No server IP provided. Chat features will be disabled.")

    # If BOTH GPT and chat are disabled, we exit
    if not gpt_enabled and not connected_to_server:
        print("Neither GPT nor chat server is available. Exiting program.")
        sys.exit(1)

    # Summarize state
    if gpt_enabled and connected_to_server:
        print(f"GPT is enabled (model: {config.MODEL_NAME}), and chat server is connected.")
    elif gpt_enabled and not connected_to_server:
        print(f"GPT is enabled (model: {config.MODEL_NAME}), but chat server is unavailable.")
    elif not gpt_enabled and connected_to_server:
        print("Chat server is available, but GPT is disabled.")

    print("Ready! Copy ### for GPT queries, !!! for chat messages, @@@ to fetch last 5 chat messages.")
    print("Note: Disabled features do nothing (or show a message).")

    prev_clipboard = pyperclip.paste()
    listening_for_query = False
    listening_for_chat = False

    while True:
        current_text = pyperclip.paste()
        if current_text != prev_clipboard:
            prev_clipboard = current_text
            print("Successfully received the clipboard:", current_text)

            # GPT Trigger
            if current_text == "###":
                if gpt_enabled:
                    listening_for_query = True
                else:
                    print("GPT is disabled. Ignoring '###'.")
                listening_for_chat = False

            elif listening_for_query:
                listening_for_query = False
                if gpt_enabled:
                    query = current_text
                    try:
                        answer = get_chatgpt_response(query)
                        print("Successfully received the ChatGPT response.")
                        pyperclip.copy(answer)
                    except Exception as e:
                        pyperclip.copy(f"Error from ChatGPT: {str(e)}")

            # Chat Trigger
            elif current_text == "!!!":
                if connected_to_server:
                    listening_for_chat = True
                else:
                    print("Chat server not connected. '!!!' ignored.")
                listening_for_query = False

            elif listening_for_chat:
                listening_for_chat = False
                if connected_to_server:
                    chat_msg = current_text
                    try:
                        r = requests.post(
                            f"{SERVER_URL}/messages",
                            json={"user": username, "content": chat_msg},
                            timeout=5
                        )
                        if r.status_code == 200:
                            print(f"Posted chat message: {username}: {chat_msg}")
                        else:
                            print(f"Error posting chat message: {r.text}")
                    except Exception as e:
                        print(f"Error posting chat message: {str(e)}")
                else:
                    print("Chat server not connected. Message ignored.")

            # Fetch last 5 messages
            elif current_text == "@@@":
                if connected_to_server:
                    try:
                        r = requests.get(f"{SERVER_URL}/messages", timeout=5)
                        if r.status_code == 200:
                            msgs = r.json()
                            if msgs:
                                combined = "\n".join(msgs)
                                pyperclip.copy(combined)
                            else:
                                pyperclip.copy("------no new message------")
                        else:
                            pyperclip.copy(f"Error fetching messages: {r.text}")
                    except Exception as e:
                        pyperclip.copy(f"Error fetching messages: {str(e)}")
                else:
                    print("Chat server not connected. '@@@' ignored.")

        time.sleep(1)

if __name__ == "__main__":
    main()
