import secp256k1
pk = secp256k1.PrivateKey(k.secret_exponent)
raw_sig = pk.ecdsa_sign(message, digest=blake2b_32)
sig = pk.ecdsa_serialize_compact(raw_sig)
print("secp lib sig: " + base58_encode(sig, b"spsig").decode())

