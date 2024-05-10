import base64
import socket
import json
import random
from rsa.rsa import encrypt_message, decrypt_message

class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def connect_to_direct_server(self, ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 50005)) # 50005 coz to jest directory server
        global s

    def create_header(self, message):
        header = f"{len(message):<5}
        return header

    def write(self, message):
        header = self.create_header(message)
        s.send(header.encode("utf-8"))
        s.send(message.encode("utf-8"))

    def choice(self):

        while True:
            print("Choose an option:")
            print("1. Get")
            print("2. Post")
            option = input("Enter the number of the option you want to choose: ")

            match option:
                case "get":
                    requested_resource = input("Enter the resource you want to get: ")
                    request = {
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

                case "post":
                    resource_to_send = 'dziecieca_porno.txt'
                    f = open(resource_to_send, 'wr')
                    f_base64 = base64.encode(f)
                    lenght = len(f_base64)

                    first_stage_of_post = {
                        "method": "post",
                        "stage": 1,
                        "file_lenght": lenght
                    }
                    json.dumps(first_stage_of_post)

                    s.send(
                        first_stage_of_post
                    )

                    if s.recv(2) == "Ok":
                        s.send(f_base64)







