from hashlib import md5
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from cv2 import imread, imwrite
from utility import string_to_binary, binary_to_string


def encrypt_decrypt(string, password, mode='encode'):
    """ Encodes or Decodes raw data w.r.t password based on mode specified. """
    _hash = md5(password.encode()).hexdigest() # get hash of password
    cipher_key = urlsafe_b64encode(_hash.encode()) # use the hash as the key of encryption
    cipher = Fernet(cipher_key) # get the cipher based on the cipher key
    if mode == 'encode':
        return cipher.encrypt(string.encode()).decode() #encrypt the data
    else:
        return cipher.decrypt(string.encode()).decode() #decrypt the data



