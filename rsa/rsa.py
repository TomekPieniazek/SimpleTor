from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    public_key = private_key.public_key()

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_key_pem, public_key_pem

def encrypt_message(public_key, message):
    public_key_obj = serialization.load_pem_public_key(
        public_key,
        backend=default_backend()
    )
    if isinstance(message, str):
        message = message.encode()
    cipher_text = public_key_obj.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return cipher_text


def decrypt_message(private_key, cipher_text):
    private_key_obj = serialization.load_pem_private_key(
        private_key,
        password=None,
        backend=default_backend()
    )
    plain_text = private_key_obj.decrypt(
        cipher_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plain_text.decode()


def encrypt(simple_string):
    first_lane = simple_string[::4]
    second_lane = simple_string[1::2]
    third_lane = simple_string[2::4]

    encrypted_phrase = ''.join(first_lane + second_lane + third_lane)
    return encrypted_phrase


def decrypt(encrypted_string):
    length = len(encrypted_string)

    first_lane_length = (length + 3) // 4
    second_lane_length = length // 2

    first_lane = list(encrypted_string[:first_lane_length])
    second_lane = list(encrypted_string[first_lane_length:first_lane_length + second_lane_length])
    third_lane = list(encrypted_string[first_lane_length + second_lane_length:])

    simple_list = []
    for i in range(length):
        if i % 4 == 0:
            simple_list.append(first_lane.pop(0))
        elif i % 4 == 1 or i % 4 == 3:
            simple_list.append(second_lane.pop(0))
        elif i % 4 == 2:
            simple_list.append(third_lane.pop(0))

    return ''.join(simple_list)