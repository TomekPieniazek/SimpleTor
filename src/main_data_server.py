import socket
import threading

class DataServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def handle_client(self, client):
        message = client.recv(1024).decode("utf-8")
        if message == 'get_resource':
            response = "LSD, or lysergic acid diethylamide, is a long-lasting psychoactive drug that distorts and alters perceptions and sensations."
            client.send(response.encode())
        client.close()

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        s.listen(5)

        while True:
            client, addr = s.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()

if __name__ == "__main__":
    server = DataServer('127.0.0.1', 50004)
    server.start()