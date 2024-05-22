import socket
import threading
import json
from rsa.rsa import aes_encrypt
import base64


class DataServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.default_file_path = "data"

    def client_handler(self, client):
        while True:
            message = json.loads(self.receive_message(client))
            nodes = message["route"]

            if message["type"] == "GET":
                to_send = self.extract_data(self.default_file_path)
                self.send_message(self.triple_encryption(to_send, nodes), client)

            elif message["type"] == "POST":
                data = message["data"]
                self.add_data(self.default_file_path, data)

            elif message["type"] == "END":
                client.close()

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
        i = 0

        for node in nodes:
            ip, port, key = node[0], node[1], node[2]

            metadata = {"ip": ip, "port": port}
            encrypted_message = aes_encrypt(message, key).decode('utf-8')
            layer_data = {"message": encrypted_message, "metadata": metadata}

            if i < len(nodes) - 1:
                next_rsa_key = nodes[i + 1][2]
                message = aes_encrypt(json.dumps(layer_data), next_rsa_key).decode('utf-8')
            else:
                payload = {"data": layer_data}
                message = base64.b64encode(json.dumps(payload).encode()).decode('utf-8')

        return message

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
