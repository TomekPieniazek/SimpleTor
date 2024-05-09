from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes


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


private_key_1, public_key_1 = generate_rsa_key_pair()
private_key_2, public_key_2 = generate_rsa_key_pair()

with open('../keys/private_key_1.pem', 'wb') as f:
    f.write(private_key_1)

with open('../keys/public_key_1.pem', 'wb') as f:
    f.write(public_key_1)

with open('../keys/private_key_2.pem', 'wb') as f:
    f.write(private_key_2)

with open('../keys/public_key_2.pem', 'wb') as f:
    f.write(public_key_2)

print("RSA key pair generated successfully!")
