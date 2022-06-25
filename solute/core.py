from hashlib import md5
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from PIL import Image
import numpy as np

# ENCRYPT-DECRYPT Text Data ---------------------------------------------------
def encrypt_decrypt(data_string:str, password:str, mode='encrypt'):
    """Encrypts OR Decrypts data_string w.r.t password based on mode specified 
    Parameters:
        data_string: Text data for cryptic transformation.
        password: key string to lock/unlock data.
        mode: 
            'encrypt' --> encrypts the data
            'decrypt' --> decrypts the data
    Returns:
        Data string either encrypted or decrypted based on mode specified    
    """   
    # `password.encode()` --> conversion into bytes
    _hash = md5(password.encode())

    # hexadecimal hash value of hash object
    hash_value = _hash.hexdigest()     

    # Fernet key (bytes or str) –--> A URL-safe base64-encoded 32-byte key
    key = urlsafe_b64encode(hash_value.encode())
    cipher = Fernet(key)

    if mode == 'encrypt':
        data_bytes = data_string.encode()
        encrypted_bytes = cipher.encrypt(data_bytes)
        encrypted_data_string = encrypted_bytes.decode()
        return encrypted_data_string

    elif mode=='decrypt':
        encrypted_bytes = data_string.encode()
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        decrypted_data_string = decrypted_bytes.decode()
        return decrypted_data_string

    else:
        # error