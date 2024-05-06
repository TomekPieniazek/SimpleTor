import socket

from node import Node
from Crypto.PublicKey import RSA


def generate_key_pair(key_size=2048):
    key = RSA.generate(key_size)

    private_key_path = "private.pem"
    public_key_path = "public.pem"

    private_key = key.export_key()
    with open("private.pem", "ab") as f:
        f.write(private_key)

    public_key = key.publickey().export_key()
    with open("public.pem", "ab") as f:
        f.write(public_key)

    return private_key_path, public_key_path

def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def main():
    while True:
        ip = input("Input IP in dotted format: ")
        if is_valid_ip(ip):
            break
        else:
            print("Invalid IP address. Please enter a valid dotted-decimal IP.")

    while True:
        try:
            port = int(input("Input port (valid range: 1-65535): "))
            if 1 <= port <= 65535:
                break
            else:
                print("Invalid port number. Please enter a value between 1 and 65535.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    nickname = input("Input Nickname of node: ")

    private_key_path, public_key_path = generate_key_pair()

    try:
        node = Node(ip, port, nickname, private_key_path, public_key_path)
        node.start_node()
    except Exception as e:
        print(f"An error occurred while starting the node: {e}")


if __name__ == "__main__":
    main()