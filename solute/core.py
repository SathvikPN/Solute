from hashlib import md5
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from PIL import Image
import numpy as np

from exceptions import InvalidModeError
from utility import string_to_binary, binary_to_string


# ENCRYPT-DECRYPT Text Data ---------------------------------------------------
def encrypt_decrypt(data_string:str, password:str, mode='encrypt') -> str:
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
        error_msg = "Invalid mode for encrypt_decrypt() \nexpected {'encrypt', 'decrypt'}"
        raise InvalidModeError(error_msg)


# ENCODER section -------------------------------------------------------------
def encode_img(input_img:str, text:str, output_img:str, password:str='') -> None:
    """ Create an Image encoded with text data.

    Parameters:
        input_img : path to input image file
        text : text data that needs to be encoded
        output_img : path to write output image 
        password : key to encrypt text data
    
    Returns:
        None
    """    
    if password:
        data = encrypt_decrypt(text, password, mode='encrypt')
    else:
        data = text 

    # process data: 32-bit info about length of data to be encoded
    data_length = bin(len(data))[2:]    # eg: '0b11101' --> '11101'
    data_length = data_length.zfill(32)

    # encode data prefixed with data-length
    bin_data = iter(data_length + string_to_binary(data))

    # read cover image 
    try:
        img = Image.open(input_img)
    except:
        # error
