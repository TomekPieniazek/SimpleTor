import requests
import json
import socket
from rsa_generation import generate_rsa_key_pair

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 1234))
connected = []

while True:
    s.listen(1)
    conn, addr = s.accept()
    connected.append(conn)

    private_key, public_key = generate_rsa_key_pair()

    if s.recv(1024) == b'Hi':
        conn.send(b'Hi')
        connection_public_key = s.recv(1024)
        conn.send(public_key)


