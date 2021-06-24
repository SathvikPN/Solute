""" Solute App
LSB Steganography Application
- Author: Sathvik PN
- GitHub: https://github.com/SathvikPN/Steganography-application
"""



from hashlib import md5
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet


def encrypt_decrypt(data_string, password, mode='encrypt'):
    """ Encrypts OR Decrypts data_string w.r.t password based on mode specified"""

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



# Custom Exceptions -----------------------------------------------------------
class InvalidMode(Exception):
    pass


if __name__=='__main__':
    if DEBUG is True:
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

        test_encrypt_decrypt()