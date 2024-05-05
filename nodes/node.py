import socket
import threading
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

class Node:
    def __init__(self, ip, port, nickname, private_key_path, public_key_path):
        self.ip = ip
        self.port = port
        self.nickname = nickname
        self.public_key_path = public_key_path
        self.private_key_path = private_key_path

        with open(private_key_path, 'rb') as f:
            self.private_key = RSA.importKey(f.read())
        with open(public_key_path, 'rb') as f:
            self.public_key = RSA.importKey(f.read())

    def handle_connection(self, client_socket, client_address):
        print(f"Client {client_address} connected")

        message = self.receive_message(client_socket)

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

            return self.decrypt_message(received_message)

        except Exception as e:

            print(f"Error connecting to directory server: {e}")

            return None

    def forward_message(self, message):
        pass

    def decrypt_message(self, message):
        try:
            decrypted_key = self.private_key.decrypt(message, padding=RSA.pkcs1.OAEP(
                mgf=RSA.pkcs1.MGF1(algorithm=hashes.SHA256())))

            if len(decrypted_key) not in (16, 24, 32):
                raise ValueError("Invalid AES key length")

            aes_key = decrypted_key

            cipher = AES.new(aes_key, AES.MODE_CBC)
            decrypted_data = cipher.decrypt(message[len(decrypted_key):])

            return decrypted_data.decode("utf-8")

        except Exception as e:
            print(f"Error decrypting message: {e}")
            return None

    def establish_circuit(self, ip, port):
        next_hop_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        next_hop_socket.connect((ip, port))

        return next_hop_socket

    def start_node(self):
        node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        node_socket.bind((self.ip, self.port))
        node_socket.listen(10)

        while True:
            client_socket, client_address = node_socket.accept()

            client_handler = threading.Thread(target=self.handle_connection, args=(client_socket, client_address))
            client_handler.start()

