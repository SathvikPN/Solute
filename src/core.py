""" Solute App
LSB Steganography Application
- Author: Sathvik PN
- GitHub: https://github.com/SathvikPN/Steganography-application
"""

DEBUG = True

from hashlib import md5
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from PIL import Image
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

    # Encode data length info with actual data and create an iterator
    bin_data = iter(data_length + string_to_binary(data))

    # read cover image 
    try:
        img = Image.open(input_img)
    except:
        raise ReadImageError(f"Image file {input_img} is inaccessible.")
    
    # img_data = np.asarray(img)
    img_data = np.array(img)
    img_data.setflags(write="WRITABLE")
    # Image dimensions
    width, height = img.size

    total_pixels = height*width
    # each pixel of RGB --> 3 bytes --> 3 LSB bits --> 3 bits space per pixel to hide data
    encoding_capacity = total_pixels*3 

    # total bits in the data that needs to be hidden including 32 bits for specifying length of data
    data_bits = 32 + len(data)*8  # Multiplication has higher precedence than addition
    # Each character is stored using eight bits of information, giving a total number of 256 different characters

    if data_bits > encoding_capacity:
        raise DataOverflowError("The data size is too big to fit in this image!")

    encode_complete = False
    modified_bits = 0

    # traverse cover image pixels left to right and top to bottom fashion
    for x in range(height):
        for y in range(width):

            # Current pixel
            pixel = img_data[x,y]

            # each pixel have 3 LSB bits to hide data
            for i in range(3):
                try:
                    d = next(bin_data)
                except StopIteration:
                    # No more binary data. Objective accomplished
                    encode_complete = True
                    break
            
                # Donot write into every LSB but only that differs with data
                # Proper count of modified bits
                # Pixel[i] = 0 to 255
                if d=='0' and pixel[i]%2==1:
                    pixel[i] -= 1  # reduce value by 1 --> LSB:1-->0
                    modified_bits += 1

                elif d=='1' and pixel[i]%2==0:
                    pixel[i] += 1  # LSB 0 --> 1 
                    modified_bits += 1
            # ---------------------------------------------------------------
            if encode_complete:
                break
        # -----------------------------------------------------------
        if encode_complete:
            break
    
    try:
        encoded_img = Image.fromarray(img_data)
    except:
        print("Error writing into new image")
        return None
    
    encoded_img.save(output_img)
    
    # loss_percentage = (modified_bits/encoding_capacity)*100
    # return loss_percentage

    


# Utility Functions -----------------------------------------------------------
def string_to_binary(data_string):
    """ Returns Binary Representation of string """
    return ''.join((bin(ord(c))[2:]).zfill(8) for c in data_string)

    # Explicit breakdown-------------
    # for c in string:
    #     ordinal = ord(c)
    #     binary_representation = bin(ordinal)
    #     binary_value = binary_representation[2:]
    #     binary_value.zfill(8)

def binary_to_string(bin_string):
    """ Returns String representation of binary values string """
    return ''.join(chr(int(bin_string[i:i+8],2)) for i in range(len(bin_string))[::8])


# Custom Exceptions -----------------------------------------------------------
class InvalidMode(Exception):
    pass

class ReadImageError(Exception):
    pass

class DataOverflowError(Exception):
    pass


if __name__=='__main__':

    # Quick Tests -------------------------------------------------------------
    def test_encrypt_decrypt():
        print("[1] Testing encrypt_decrypt()...", end=' ')
        DATA = "Hi"
        PASSWORD = '123'
        encrypted_data = encrypt_decrypt(DATA, PASSWORD, 'encrypt')
        decrypted_data = encrypt_decrypt(encrypted_data,PASSWORD, 'decrypt')
        if decrypted_data == DATA:
            print("OK")
        else:
            print("FAILED")
        print()




    # Execute Tests in DEBUG MODE ---------------------------------------------
    if DEBUG is True:
        print("[DEBUG Mode ON] ------------------------------------------------")
        print()
        # test_encrypt_decrypt()
        # test_encode_img()



        