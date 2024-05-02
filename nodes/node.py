import socket
import threading

class Node:
    def __init__(self, ip, port, nickname, privateKey, publicKey):
        self.ip = ip
        self.port = port
        self.nickname = nickname
        self.publicKey = publicKey
        self.privateKey = privateKey

    def handle_connection(self, client_socket):
        pass

    def create_header(self, encoded_message):
        message_length = len(encoded_message)

        if message_length >= 10_000:
            raise ValueError("Message is too long")

        return f"{message_length:>5}".encode("utf-8")

    def send_message(self, encoded_message, client_socket):
        header = self.create_header(encoded_message)

        client_socket.sendall(header + encoded_message)

    def receive_message(self, client_socket):
        expected_message_len = int(client_socket.recv(5).decode("utf-8"))
        received_message = client_socket.recv(expected_message_len)

        if len(received_message) != expected_message_len:
            raise ConnectionError("Received message is not equal to expected message length")

        return received_message.decode("utf-8")

    def forward_message(self, message):
        pass

    def back_message(self, message):
        pass

    def decrypt_message(self, message):
        pass

    def start_node(self):
        node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        node_socket.bind((self.ip, self.port))
        node_socket.listen(10)

        while True:
            client_socket, address = node_socket.accept()

            client_handler = threading.Thread(target=self.handle_connection, args=(client_socket,))
            client_handler.start()

