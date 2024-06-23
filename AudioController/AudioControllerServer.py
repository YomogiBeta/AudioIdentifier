# !/usr/bin/env python3
import socket
import threading
from .AudioControllerClient import AudioControllerClient


class AudioControllerServer:
    HOST = "127.0.0.1"

    def __init__(self, aPort, aClient: AudioControllerClient):
        self.aPort = aPort
        self.a_running = True
        self.aClient = aClient

    def start(self):
        self.a_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.a_sock.bind((self.HOST, self.aPort))

        def send_data():
            while self.a_running:
                data, addr = self.a_sock.recvfrom(1024)
                if data.decode('utf-8') == "stop":
                    self.a_running = False
                    self.close()

        self.a_thread = threading.Thread(target=send_data)
        self.a_thread.start()

    def close(self):
        self.aClient.close()
        self.a_sock.close()

    def thread(self):
        return self.a_thread
