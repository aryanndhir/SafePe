from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt

eth_k = generate_eth_key()  # environment variable
sk_hex = eth_k.to_hex()  # hex string
pk_hex = eth_k.public_key.to_hex()  # hex string

# b is used as it is a byte literal so basiacally it is a byte array and we use this instead of data.encode("utf8")
data = b'this is a test'

def encrypt_data(pk_hex, data):
    return encrypt(pk_hex, data)

def decrypt_data(sk_hex, enc_data):
    return decrypt(sk_hex, enc_data)
