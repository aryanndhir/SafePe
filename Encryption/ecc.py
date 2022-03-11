from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt

eth_k = generate_eth_key()
sk_hex = eth_k.to_hex()  # hex string
pk_hex = eth_k.public_key.to_hex()  # hex string
data = 'this is a test' 

enc_data = encrypt(pk_hex, data)
print(enc_data)

dec_data = decrypt(sk_hex, enc_data)
print(dec_data)

secp_k = generate_key()
sk_bytes = secp_k.secret  # bytes
pk_bytes = secp_k.public_key.format(True)  # bytes

decrypt(sk_bytes, encrypt(pk_bytes, data))