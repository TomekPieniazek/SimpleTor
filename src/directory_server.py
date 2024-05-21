import socket
import json
from random import choice
import threading


class Server:
    def __init__(self, ip, port):  # port is 50005
        self.ip = ip
        self.port = port

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))

        first_layer = ['87.206.157.239']  # Operują na porcie 50001
        second_layer = ['79.190.177.172']  # Operują na porcie 50002
        last_layer = ['87.206.157.239']  # Operują na porcie 50003
        main_data_server = ['79.190.177.172']  # Operują na porcie 50004

        client_ip = "127.0.0.1"
        client_port = 50000
        client = Client(client_ip, client_port)
        with open('../node/public.pem', 'r') as file:
            key_1 = file.read()

        with open('../keys/klucz_1.pem') as file:
            key_2 = file.read()

        with open('../keys/klucz_2.pem') as file:
            key_3 = file.read()

        x = {
            "first_layer": choice(first_layer),
            "second_layer": choice(second_layer),
            "last_layer": choice(last_layer),
            "key_1": key_1,
            "key_2": key_2,
            "key_3": key_3,
            "port_1": 50001,
            "port_2": 50002,
            "port_3": 50003,
        }

        while True:
            s.listen(5)
            client, addr = s.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()

    def receive(self, client):
        message_len = int(client.recv(5).decode("utf-8"))
        message = client.recv(message_len)

        if len(message) != message_len:
            print("pies cie jebal")
        else:
            message.decode("utf-8")

    def handle_client(self, client):
        x = {
            "Node_1": [choice(first_layer), key_1, 50001],
            "Node_2": [choice(second_layer), key_2, 50002],
            "Node_3": [choice(last_layer), key_3, 50003],
        }

        s.send(json.dumps(x).encode("utf-8"))


def main():
    server_ip = "127.0.0.1"
    server_port = 50005
    server = Server(server_ip, server_port)
    server.start()


if __name__ == "__main__":
    main()
