import socket
import json
from random import choice
import threading


class Proxy:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def receive(self, client):
        try:
            message_len = int(client.recv(5).decode("utf-8"))
            message = client.recv(message_len)

            if len(message) != message_len:
                print("pies cie jebal")
                return None
            else:
                return message.decode("utf-8")

        except Exception as e:
            print(f"Error: {e}")
            return None

    def ask_directory_server(self, server_ip='87.206.157.239', server_port=50005) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server_ip, server_port))
            s.send(b'get_second_connection')

            second_connection = self.receive(s)
            s.close()
            return second_connection
        except Exception as e:
            print(f"Error connecting to directory server: {e}")
            return None

    def handle_client(self, client, socket):
        message = self.receive(client)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ask_directory_server(), 50002))

    def start(self, layer_to_ask=ask_directory_server()):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))

        while True:
            client, addr = s.accept()

            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()
