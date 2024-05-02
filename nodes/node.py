import socket
import threading

class Node:
    def __init__(self, ip, port, nickname, privateKey, publicKey, ):
        self.ip = ip
        self.port = port
        self.nickname = nickname
        self.publicKey = publicKey
        self.privateKey = privateKey

    def handleConenction(self):
        pass

    def sendMessage(self, message):
        pass

    def receiveMessage(self):
        pass

    def forwardMessage(self, message):
        pass

    def backMessage(self, message):
        pass

    def decryptMessage(self, message):
        pass

    def startNode(self):
        node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        node_socket.bind((self.ip, self.port))
        node_socket.listen(10)

        while True:
            client_socket, address = node_socket.accept()

            client_handler = threading.Thread(target=self.handleConenction, args=(client_socket,))
            client_handler.start()

