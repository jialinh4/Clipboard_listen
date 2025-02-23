#!/usr/bin/env python3

from flask import Flask, request, jsonify
from collections import deque
import socket
import config  # Import our PORT from config

app = Flask(__name__)

messages = deque(maxlen=100)

def get_local_ip():
    """
    Attempt a dummy connection to a public IP to figure out the local LAN address.
    Fallback to localhost if something fails.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "127.0.0.1"
    return local_ip

@app.route("/messages", methods=["GET"])
def get_messages():
    recent = list(messages)[-5:]
    return jsonify([f"{m['user']}: {m['content']}" for m in recent])

@app.route("/messages", methods=["POST"])
def post_message():
    data = request.json
    user = data.get("user")
    content = data.get("content")
    messages.append({"user": user, "content": content})
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    host_ip = get_local_ip()
    port = config.PORT  # Use PORT from config.py
    print(f"Starting chat server on {host_ip}:{port} ...")
    try:
        app.run(host="0.0.0.0", port=port)  # Bind to all interfaces
    except Exception as e:
        print(f"Failed to start server: {e}")
