## Introduction
**This script** listens to your clipboard for special triggers and sends copied text to an OpenAI model when needed. It also supports decrypting your API key using a short passphrase.

## Setup
**1.** Install `openai==0.28.0`:
pip uninstall openai
pip install openai==0.28.0

**2.** Install `pyperclip`:
pip install pyperclip

**3.** Encrypt your real API key:
   - Run `encrypt_key.py` from this project.
   - Enter your real key and a short passphrase.
   - Copy the printed encrypted key (something like `b'gAAAAABk...'`).

**4.** Update `config.py` with your **encrypted** API key:
ENCRYPTED_KEY = b'your_encrypted_key_here'

## Usage
**1.** Run:
python clipboard_listen.py

**2.** When prompted, enter your **short passphrase** that decrypts your real API key.

**3.** Copy `###` to mark the next clipboard item as a question.

**4.** Copy your actual question next. The script sends it to the model and replaces your clipboard with the answer.

**5.** Paste the answer wherever you need it.

**Stop** the script with Ctrl + C.
