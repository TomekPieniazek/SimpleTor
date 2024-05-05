import socket
import json

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
        options = ["get", "send", "delete", "post"]

        match options:
            case "get":
                self.write(str(options[0]))
            case "send":
                self.write(str(options[1]))
            case "delete":
                self.write(str(options[2]))
            case "post":
                self.write(str(options[3]))
            case default:
                print("Invalid option")

