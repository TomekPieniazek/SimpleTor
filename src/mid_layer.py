import socket
import json
import threading

class Proxy:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def receive(self, client):
        try:
            message_len = int(client.recv(5).decode("utf-8"))
            message = client.recv(message_len)

            if len(message) != message_len:
                print("Error: Message length mismatch")
                return None
            else:
                return message.decode("utf-8")

        except Exception as e:
            print(f"Error receiving message: {e}")
            return None

    def ask_directory_server(self, server_ip='87.206.157.239', server_port=50005) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server_ip, server_port))
            s.send(b'get_last_connection')

            last_connection = self.receive(s)
            s.close()
            return last_connection
        except Exception as e:
            print(f"Error connecting to directory server: {e}")
            return None

    def handle_client(self, client):
        message = self.receive(client)
        if message is None:
            client.close()
            return

        resource_request = json.loads(message)
        resource_id = resource_request.get('resource_id')

        resource_server_ip = self.ask_directory_server()
        if resource_server_ip is None:
            client.close()
            return

        resource_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        resource_socket.connect((resource_server_ip, 50003))
        resource_socket.send(json.dumps({'request': 'get_resource', 'resource_id': resource_id}).encode())

        resource_data = self.receive(resource_socket)
        if resource_data is not None:
            client.send(resource_data.encode())

        resource_socket.close()
        client.close()

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        s.listen(5)

        while True:
            client, addr = s.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()