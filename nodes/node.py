class Node:
    def __init__(self, ip, port, nickname, privateKey, publicKey, ):
        self.ip = ip
        self.port = port
        self.nickname = nickname
        self.publicKey = publicKey
        self.privateKey = privateKey

    def handeConenction(self):
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
        pass

