import requests
import time
import threading
import os


def ping_server():
    server_url = os.getenv("SERVER_URL", "https://zsk-qr-seeker.onrender.com/health-check")
    while True:
        try:
            response = requests.get(server_url)
            if response.status_code == 200:
                print("Server is alive")
            else:
                print(f"Server responded with status code: {response.status_code}")
        except Exception as e:
            print(f"Error pinging server: {e}")
        time.sleep(60 * 10)  # Ping every 10 minutes

def start_keep_alive():
    thread = threading.Thread(target=ping_server)
    thread.daemon = True
    thread.start()