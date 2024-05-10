import random
import json
from rsa.rsa import generate_rsa_key_pair, encrypt_message, decrypt_message

request = {
    "id": random.randint(1, 1000000000000000000000),
    "method": "get",
    "resource_name": "dziecience_porno.mov"
}
request_json = json.dumps(request, separators=(',', ':'))

private, public = generate_rsa_key_pair()
x = encrypt_message(public, request_json)

print(decrypt_message(private, x))

