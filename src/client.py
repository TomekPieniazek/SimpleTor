import socket
from rsa_generation import generate_rsa_key_pair

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 1234))

s.send(b'Hi')

if s.recv(1024) == b'Hi':
    public_key, private_key = generate_rsa_key_pair()
    s.send(public_key)

print(s.recv(1024))
