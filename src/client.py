import base64
import socket
import json
import random
from rsa.rsa import encrypt_message, decrypt_message
from typing import Any, Dict, Union


class Client:
    def __init__(self, ip: str, port: int):
        self.ip: str = ip
        self.port: int = port

    def connect_to_direct_server(self, ip: str) -> None:
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 50005))  # 50005 because this is the directory server

    def create_header(self, message: str) -> str:
        header = f"{len(message):<5}"
        return header

    def triple_layer_encryption(self, key_1: str, key_2: str, key_3: str, ip_1: str, ip_2: str, ip_3: str, port_1: int,
                                port_2: int, port_3: int, message: str) -> str:
        message_1 = (message + "DATA" + json.dumps({"ip": ip_1, "port": port_1})).encode('utf-8')
        message_1 = b''.join(
            [encrypt_message(key_1.encode(), message_1[i:i + 245]) for i in range(0, len(message_1), 245)])

        message_2 = bytearray()
        message_2.extend(message_1)
        message_2.extend(("DATA" + json.dumps({"ip": ip_2, "port": port_2})).encode('utf-8'))
        message_2 = b''.join(
            [encrypt_message(key_2.encode(), bytes(message_2[i:i + 245])) for i in range(0, len(message_2), 245)])

        message_3 = bytearray()
        message_3.extend(message_2)
        message_3.extend(("DATA" + json.dumps({"ip": ip_3, "port": port_3})).encode('utf-8'))
        message_3 = b''.join(
            [encrypt_message(key_3.encode(), bytes(message_3[i:i + 245])) for i in range(0, len(message_3), 245)])

        return base64.b64encode(message_3).decode('utf-8')

    def write(self, message: str) -> None:
        header = self.create_header(message)
        s.send(header.encode("utf-8"))
        s.send(message.encode("utf-8"))

    def choice(self) -> None:
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
                        response_len = int(s.recv(5).decode("utf-8"))

                        data = bytearray()
                        while len(data) < response_len:
                            packet = s.recv(response_len - len(data))
                            if not packet:
                                print("Error receiving response")
                                break
                            data.extend(packet)
                        response = decrypt_message(data)

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
                    json.dumps(first_stage_of_post)

                    s.send(json.dumps(first_stage_of_post).encode("utf-8"))

                    if s.recv(2).decode("utf-8") == "Ok":
                        s.send(f_base64)


def main():

    client_ip = "127.0.0.1"
    client_port = 50000
    client = Client(client_ip, client_port)
    with open('../node/public.pem', 'r') as file:
        key_1 = file.read()

    with open('../keys/klucz_1.pem') as file:
        key_2 = file.read()

    with open('../keys/klucz_2.pem') as file:
        key_3 = file.read()

    triple_edict = client.triple_layer_encryption(key_1, key_2, key_3, '127.0.0.1', '87.206.157.239', '87.206.157.239', 50001, 50005, 50003, 'huj')
    client.connect('127.0.0.1', 50001)
    client.write(triple_edict)

if __name__ == "__main__":
    main()







if __name__ == "__main__":
    main()
