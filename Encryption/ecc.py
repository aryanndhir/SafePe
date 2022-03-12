from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt

eth_k_sender = generate_eth_key()  # environment variable
sk_hex_sender = eth_k_sender.to_hex()  # hex string
pk_hex_sender = eth_k_sender.public_key.to_hex()  # hex string

eth_k_receiver = generate_eth_key()
sk_hex_receiver = eth_k_receiver.to_hex()  
pk_hex_receiver = eth_k_receiver.public_key.to_hex()  

# b is used as it is a byte literal so basiacally it is a byte array and we use this instead of data.encode("utf8")
data = b'this is a test'

def encrypt_data(data, bank):

    if bank == "sender":
        return encrypt(pk_hex_sender, data)
    else:
        return encrypt(pk_hex_receiver, data)

    # return encrypt(pk_hex, data)


def decrypt_data(enc_data, bank):

    if bank == "sender":
        return decrypt(sk_hex_sender, enc_data)
    else:
        return decrypt(sk_hex_receiver, enc_data)

    # return decrypt(sk_hex, enc_data)