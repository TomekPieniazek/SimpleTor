import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


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


with open('../keys/private_key_1.pem', 'rb') as f:
    private_key_1 = f.read()

with open('../keys/public_key_1.pem', 'rb') as f:
    public_key_1 = f.read()

with open('../keys/private_key_2.pem', 'rb') as f:
    private_key_2 = f.read()

with open('../keys/public_key_2.pem', 'rb') as f:
    public_key_2 = f.read()

test = 'Kubus Puchatek'
f_cipher = encrypt_message(public_key_1, test)
f_cipher = base64.standard_b64encode(f_cipher).decode()
f_cipher = encrypt(f_cipher)
print(f'Encrypted message: {f_cipher}')

# s_plain = decrypt_message(private_key_1, f_cipher)
# print(f'Double decrypted message: {s_plain}')
