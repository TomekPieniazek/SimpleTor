import socket
import threading
import json


class DataServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.default_file_path = "data"

    def client_handler(self, client):
        while True:
            message = json.loads(self.receive_message(client))

            if message["type"] == "GET":
                to_send = self.extract_data(self.default_file_path)

            elif message["type"] == "POST":
                data = message["data"]
                self.add_data(self.default_file_path, data)

            else:
                pass

    def extract_data(self, file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            f.close()
            return data

    def add_data(self, file_path, data):
        with open(file_path, "w") as f:
            json.dump(data, f)
            f.close()

    def create_header(self, encoded_message):
        message_length = len(encoded_message)

        if message_length >= 10_000:
            raise ValueError("Message is too long")

        return f"{message_length:>5}".encode("utf-8")

    def send_message(self, encoded_message, client_socket):
        header = self.create_header(encoded_message)

        client_socket.sendall(header + encoded_message)

    def receive_message(self, client_socket):
        try:
            expected_message_len = int(client_socket.recv(5).decode("utf-8"))
            received_message = client_socket.recv(expected_message_len)

            if len(received_message) != expected_message_len:
                raise ConnectionError("Received message is not equal to expected message length")

            return received_message

        except Exception as e:

            print(f"Error receiving the message: {e}")

            return None

    def triple_encryption(self, message, nodes):
        for node in nodes:
            pass

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        s.listen(5)

        while True:
            client, addr = s.accept()
            client_handler = threading.Thread(target=self.client_handler, args=(client,))
            client_handler.start()


if __name__ == "__main__":
    server = DataServer('127.0.0.1', 50004)
    server.start()
