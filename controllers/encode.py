def encrypt_decrypt(data, key):
    key = (key * (len(data) // len(key) + 1))[:len(data)]
    return bytearray(a ^ b for a, b in zip(data, key))
