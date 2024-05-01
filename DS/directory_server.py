import socket
import json
from random import choice
import threading


class Server:
    def __init__(self, ip, port): # port is 50005
        self.ip = ip
        self.port = port

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.ip, self.port))

        first_layer = ['87.206.157.239']  # Operują na porcie 50001
        second_layer = ['79.190.177.172']  # Operują na porcie 50002
        last_layer = ['87.206.157.239']  # Operują na porcie 50003
        main_data_server = ['79.190.177.172']  # Operują na porcie 50004

        x = {
            "first_layer": choice(first_layer),
            "second_layer": choice(second_layer),
            "last_layer": choice(last_layer),
            "main_data_server": choice(main_data_server)
        }
        global x

        while True:
            client, addr = server_socket.accept()

            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()

    def create_header(self, message):
        header = f"{len(message):<5}"
        return header

    def write_message(self, client, message):
        header = self.create_header(message)

        client.send(header.encode("utf-8"))
        client.send(message.encode("utf-8"))

    def receive_message(self, client):
        message_len = int(client.recv(5).decode("utf-8"))
        message = client.recv(message_len)

        if len(message) != message_len:
            print("pies cie jebal")
        else:
            message.decode("utf-8")

    def handle_client(self, client):
        message = self.receive_message(client)

        if message == "get":
            client.send(json.dumps(x).encode("utf-8"))

