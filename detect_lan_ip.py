#!/usr/bin/env python3

import socket
import config

def main():
    try:
        # Attempt to discover the local IP by 'connecting' to a public IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        # Fallback if the above fails
        local_ip = socket.gethostbyname(socket.gethostname())

    print(f"Your local IP address might be: {local_ip}")
    print(f"Port configured in config.py: {config.PORT}")
    print("Use this IP and port for your chat_server.py (if needed) and for clients on the same LAN.")

if __name__ == "__main__":
    main()
