from node import Node
from Crypto.PublicKey import RSA

key = RSA.generate(2048)
private_key = key.export_key()
with open("private.pem", "ab") as f:
    f.write(private_key)

public_key = key.publickey().export_key()
with open("public.pem", "ab") as f:
    f.write(public_key)

ip = input("Input ip in dotted format: ")
port = input("Input port: ")
nickname = input("Input Nickname of node: ")
private_key_path = "./private.pem"
public_key_path = "./public.pem"

Node(ip, int(port), nickname, private_key_path, public_key_path).start_node()