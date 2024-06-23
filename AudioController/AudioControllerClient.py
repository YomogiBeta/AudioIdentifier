# !/usr/bin/env python3
import socket
# import time
import threading


class AudioControllerClient:
    HOST = "127.0.0.1"

    def __init__(self, aPort):
        self.aPort = aPort
        self.a_running = True

    def start(self, task):
        self.a_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.a_sock .connect((self.HOST, self.aPort))

        self.a_thread = threading.Thread(target=task)
        self.a_thread.start()

    def send(self, aData):
        self.a_sock.send(aData.encode('utf-8'))

    def close(self):
        self.a_running = False
        self.a_sock.close()

    def is_running(self):
        return self.a_running

    def thread(self):
        return self.a_thread
