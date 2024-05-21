import socket
import json
import random
import threading


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.node_list = {}

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        s.listen(10)

        while True:
            client_socket, client_address = s.accept()

            client_handler = threading.Thread(target=self.client_handler(client_socket), args=(client_socket,))
            client_handler.start()

    def create_header(self, message):
        message_length = len(message)

        if message_length >= 10_000:
            raise ValueError("Message is too long")

        return f"{message_length:>5}".encode("utf-8")

    def send_message(self, message, client_socket):
        header = self.create_header(message)

        client_socket.sendall(header + message)

    def receive(self, client_socket):
        try:
            expected_message_len = int(client_socket.recv(5).decode("utf-8"))
            received_message = client_socket.recv(expected_message_len)

            if len(received_message) != expected_message_len:
                raise ConnectionError("Received message is not equal to expected message length")

            return received_message.decode("utf-8")

        except Exception as e:

            print(f"Error connecting to directory server: {e}")

            return None

    def client_handler(self, client):
        received_message = self.receive(client)

        message = json.loads(received_message.decode("utf-8"))

        if message["type"] == "POST":
            self.node_list[message["name"]] = (message["ip"], message["port"], message["public_key"])

        elif message["type"] == "GET":
            random_nodes = random.sample(list(self.node_list.keys()), 3)
            self.send_message(random_nodes.encode("utf-8"), client)

        else:
            print("I")


def main():
    server_ip = "127.0.0.1"
    server_port = 50005
    server = Server(server_ip, server_port)
    server.start()


if __name__ == "__main__":
    main()
