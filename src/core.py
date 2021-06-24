""" Solute App
LSB Steganography Application
- Author: Sathvik PN
- GitHub: https://github.com/SathvikPN/Steganography-application
"""

DEBUG = True

from hashlib import md5
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
import PIL
import numpy as np



# ENCRYPT-DECRYPT Text Data ---------------------------------------------------

def encrypt_decrypt(data_string, password, mode='encrypt'):
    """Encrypts OR Decrypts data_string w.r.t password based on mode specified"""

    # `password.encode()` --> conversion into bytes
    _hash = md5(password.encode()) 

    # hexadecimal hash value of hash object
    hash_value = _hash.hexdigest() 

    # Fernet key (bytes or str) –--> A URL-safe base64-encoded 32-byte key
    # https://cryptography.io/en/latest/fernet/ 
    key = urlsafe_b64encode(hash_value.encode())

    cipher = Fernet(key)

    if mode=='encrypt':
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
        InvalidModeError = "Invalid mode for encrypt_decrypt().\
            \nexpected {'encrypt','decrypt'}"
        raise InvalidMode(InvalidModeError)



# ENCODER section -------------------------------------------------------------

def encode_img(input_img, text, output_img, password=None):
    """ Create an Image encoded with text data.

    Parameters:
        input_img : path of input image file
        text : textual data that needs to be encoded
        output_img : path to write output image 
        password : key to encrypt or decrypt text data
    
    Returns:
        Percentage of data lost when image was written with encoded data
    """

    if password is None:
        # Bypass password encryption of data
        data = text
    else:
        data = encrypt_decrypt(text, password, mode='encrypt')

    
    # Process Encrypted data

    # 32-bit info about length of data to be encoded
    data_length = bin(len(data))[2:]  # eg: '0b11101'
    data_length.zfill(32)

    # Encode data length info with actual data
    bin_data = iter(data_length + string_to_binary(data))



# Utility Functions
def string_to_binary(data_string):
    """ Returns Binary Representation of string """
    return ''.join((bin(ord(c))[2:]).zfill(8) for c in data_string)
    
    # Explicit breakdown-------------
    # for c in string:
    #     ordinal = ord(c)
    #     binary_representation = bin(ordinal)
    #     binary_value = binary_representation[2:]
    #     binary_value.zfill(8)



# Custom Exceptions -----------------------------------------------------------
class InvalidMode(Exception):
    pass


if __name__=='__main__':

    # Quick Tests -------------------------------------------------------------
    def test_encrypt_decrypt():
        print("Testing encrypt_decrypt()...", end=' ')
        DATA = "Hi"
        PASSWORD = '123'
        encrypted_data = encrypt_decrypt(DATA, PASSWORD, 'encrypt')
        decrypted_data = encrypt_decrypt(encrypted_data,PASSWORD, 'decrypt')
        if decrypted_data == DATA:
            print("OK")
        else:
            print("FAILED")

    # Execute Tests in DEBUG MODE ---------------------------------------------
    if DEBUG is True:
        print("[DEBUG Mode ON] ------------------------------------------------")
        test_encrypt_decrypt()



        