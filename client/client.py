import base64
import socket
import json
import random
from rsa.rsa import rsa_encrypt, rsa_decrypt, aes_encrypt, aes_decrypt
from typing import Any, Dict, Union


class Client:
    def __init__(self, ip: str, port: int):
        self.ip: str = ip
        self.port: int = port

    def connect_to_direct_server(self, ip: str) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, 50005))

    def create_header(self, message: str) -> str:
        header = f"{len(message):<5}"
        return header

    def triple_layer_encryption(self, rsa_key_1: bytes, rsa_key_2: bytes, rsa_key_3: bytes, ip_1: str, ip_2: str,
                                ip_3: str, port_1: int,
                                port_2: int, port_3: int, message: str) -> str:

        encrypted_message = aes_encrypt(message, rsa_key_1).decode('utf-8')
        metadata_1 = {"ip": ip_1, "port": port_1}
        layer_1_data = {"message": encrypted_message, "metadata": metadata_1}

        encrypted_layer_1 = aes_encrypt(json.dumps(layer_1_data), rsa_key_2).decode('utf-8')
        metadata_2 = {"ip": ip_2, "port": port_2}
        layer_2_data = {"message": encrypted_layer_1, "metadata": metadata_2}

        encrypted_layer_2 = aes_encrypt(json.dumps(layer_2_data), rsa_key_3).decode('utf-8')
        metadata_3 = {"ip": ip_3, "port": port_3}
        layer_3_data = {"message": encrypted_layer_2, "metadata": metadata_3}

        payload = {
            "data": layer_3_data,
        }

        return base64.b64encode(json.dumps(payload).encode()).decode('utf-8')

    def write(self, message: str) -> None:
        header = self.create_header(message)
        self.s.send(header.encode("utf-8"))
        self.s.send(message.encode("utf-8"))

    def receive_message(self):
        try:
            expected_message_len = int(self.s.recv(5).decode("utf-8"))
            received_message = self.s.recv(expected_message_len)

            if len(received_message) != expected_message_len:
                raise ConnectionError("Received message is not equal to expected message length")

            return received_message

        except Exception as e:

            print(f"Error receiving the message: {e}")

            return None

    def client_handler(self) -> None:
        while True:
            print("Choose an option:")
            print("1. Get")
            print("2. Post")
            option = input("Enter the number of the option you want to choose: ")

            match option:
                case "1":
                    requested_resource = input("Enter the resource you want to get: ")
                    request: Dict[str, Union[int, str]] = {
                        "id": random.randint(1, 100000000000),
                        "requested_resource": requested_resource,
                        "request_type": "get"
                    }
                    self.write(json.dumps(request))

                    try:
                        response_len = int(self.s.recv(5).decode("utf-8"))

                        data = bytearray()
                        while len(data) < response_len:
                            packet = self.s.recv(response_len - len(data))
                            if not packet:
                                print("Error receiving response")
                                break
                            data.extend(packet)
                        response = rsa_decrypt(data)

                    except:
                        print("Error receiving response")
                        continue

                case "2":
                    resource_to_send = 'dziecieca_porno.txt'
                    with open(resource_to_send, 'rb') as f:
                        f_base64 = base64.b64encode(f.read())
                    length = len(f_base64)

                    first_stage_of_post: Dict[str, Union[str, int]] = {
                        "method": "post",
                        "stage": 1,
                        "file_length": length
                    }
                    self.write(json.dumps(first_stage_of_post))

                    if self.s.recv(2).decode("utf-8") == "Ok":
                        self.s.send(f_base64)

    def end_connection(self):
        self.s.close()

    def client_connect(self, ip, port):
        self.s.connect((ip, port))


def main():
    client_ip = "127.0.0.1"
    client_port = 50000
    client = Client(client_ip, client_port)

    with open('../node/public.pem', 'rb') as file:
        rsa_key_1 = file.read()

    with open('../keys/klucz_1.pem', 'rb') as file:
        rsa_key_2 = file.read()

    with open('../keys/klucz_2.pem', 'rb') as file:
        rsa_key_3 = file.read()

    triple_edict = client.triple_layer_encryption(rsa_key_1, rsa_key_2, rsa_key_3, '127.0.0.1', '87.206.157.239',
                                                  '87.206.157.239',
                                                  50001, 50005, 50003, 'huj')
    print(triple_edict)
    client.connect_to_direct_server('127.0.0.1')
    client.end_connection()

    client.client_connect('127.0.0.1', 50001)
    client.write(triple_edict)

    while True:
        message = client.receive_message()
        if message is not None:
            print(message.decode("utf-8"))
            break

    client.end_connection()


if __name__ == "__main__":
    main()
