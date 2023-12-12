import hashlib

def password_hash(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()