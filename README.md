## Introduction
This project provides two main features:
1. **ChatGPT Integration** via clipboard triggers (copy "###" followed by your question).
2. **Multi-User Chat Room** via a simple Flask server (copy "!!!" to post a message, "@@@" to fetch recent chat logs).

By combining both, you can run a local or LAN-based chat room while still using GPT for quick queries.

---

## Setup & Installation

### 1. Clone or Download
Get the project files onto your machine. You should have:
- encrypt_key.py
- config.py
- chat_server.py
- clipboard_listen.py
- detect_lan_ip.py
- list_models.py
- requirements.txt
- README.md

### 2. Install Python Dependencies
We recommend Python 3.7+.

You can now simply use:
```pip install -r requirements.txt```

This installs everything in one command, including:
- openai==0.28.0
- pyperclip
- requests
- cryptography
- flask

Alternatively, you can set up a virtual environment:
```python -m venv venv```
```source venv/bin/activate``` (On Windows: venv\Scripts\activate)
```pip install -r requirements.txt```

### 3. Encrypt Your Real OpenAI Key (Optional)
If you want your API key hidden:
1. Run encrypt_key.py and enter your real sk-... key plus a short passphrase.
2. Copy the printed encrypted key into config.py as ENCRYPTED_KEY = b'your_encrypted_blob'.

### 4. Configure config.py
Inside config.py:
- PORT sets the port for the Flask server (e.g., 5050).
- MODEL_NAME sets which OpenAI model to query (e.g., "o1-mini", "gpt-3.5-turbo").
- ENCRYPTED_KEY is the encrypted key from the previous step.

---

## Usage

### Feature 1: ChatGPT Integration
- Trigger: Copy "###" → the next clipboard copy is your prompt.
- The script (clipboard_listen.py) sends it to OpenAI, and when GPT replies, your clipboard is replaced by the answer.
- Paste to see GPT's answer.

### Feature 2: Multi-User Chat Room

#### Server: chat_server.py
- Start it: ```python chat_server.py```
- Runs on 0.0.0.0:PORT so others on your LAN can connect.

#### Client: clipboard_listen.py
- Copy "!!!" → the next copied text is posted to the server as a new chat message.
- Copy "@@@" → retrieves the last 5 messages from the server and places them in your clipboard.

#### LAN Scenario
1. Run chat_server.py on one machine (Machine A).
2. On the same or another machine (Machine B) in the same LAN, run clipboard_listen.py.
3. Enter the server's IP (the script auto-appends the port from config.py).
4. Each user can post or fetch messages using the triggers above.

---

## Scripts & Their Purposes

1. encrypt_key.py
   - Encrypts your real sk-... key using a short passphrase.
   - Prints out a base64-like string to put into config.py.

2. config.py
   - Stores the encrypted key (ENCRYPTED_KEY), PORT, and MODEL_NAME.
   - You can quickly change the model or port here without editing other files.

3. chat_server.py
   - A Flask server to store chat messages in memory.
   - Provides /messages endpoint for GET (to fetch last 5 messages) and POST (to add a new message).

4. clipboard_listen.py
   - Runs in a loop, watching the clipboard.
   - If "###" is copied, it sends the next copied text to GPT.
   - If "!!!" is copied, it sends the next copied text to the chat server.
   - If "@@@" is copied, it fetches the last 5 messages from the server.
   - If the user's passphrase is incorrect, GPT is disabled but the script can still do chat, and vice versa.

5. detect_lan_ip.py
   - Prints your machine's local IP address and the port from config.py.
   - Helps you figure out which IP to give to other machines on your LAN.

6. list_models.py
   - Example script that sets openai.api_key and lists all models your account can access.

---

## Example Workflow

1. Detect IP on the server machine:
```python detect_lan_ip.py```
Suppose it prints 192.168.1.50 and the port is 5050.

2. Run Server on that IP/port:
```python chat_server.py```
Prints: Starting chat server on 192.168.1.50:5050 ...

3. Run Clipboard Listener on any machine in the LAN:
```python clipboard_listen.py```
- Enter passphrase (if you encrypted your key).
- Enter username for the chat room.
- Enter server IP (e.g. 192.168.1.50). The script automatically appends :5050.
- Now you can do GPT queries or chat triggers.

4. Chat:
- Copy "!!!", then copy "Hello from user!" → posted to the server.
- Copy "@@@" → fetch last 5 messages.

5. GPT:
- Copy "###", then copy "Write a Python function to add two numbers." → GPT answer in your clipboard.
