""" Solute App

LSB Steganography Application
- Author: Sathvik PN
- GitHub: https://github.com/SathvikPN/Steganography-application
"""

DEBUG = True    # set False to turn off preliminary tests from being run

from hashlib import md5
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from PIL import Image
import numpy as np




# ENCRYPT-DECRYPT Text Data ---------------------------------------------------

def encrypt_decrypt(data_string, password, mode='encrypt'):
    """Encrypts OR Decrypts data_string w.r.t password based on mode specified
    
    Parameters:
        data_string: Text that needs to be encoded. passed in string format
        password: a string to encrypt data before encoding into an image.
        mode: 
            'encrypt' --> encrypts the data
            'decrypt' --> decrypts the data
    Returns:
        Data string either encrypted or decrypted based on mode specified
    """

    _hash = md5(password.encode()) 
    hash_value = _hash.hexdigest() 
    key = urlsafe_b64encode(hash_value.encode())
    cipher = Fernet(key)  # 32-byte key - URLsafe - base64-encoded 

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
        raise InvalidModeError("Expected 'encrypt' OR 'decrypt' ")




# ENCODER section -------------------------------------------------------------

def encode_img(input_img, text, output_img, password=None):
    """ Create an Image encoded with text data.

    Parameters:
        input_img : path of input image file
        text : textual data that needs to be encoded
        output_img : path to write output image 
        password : key to encrypt or decrypt text data
    
    Returns:
        None
    """

    if password is None:
        data = text
    else:
        data = encrypt_decrypt(text, password, mode='encrypt')

    data_length = bin(len(data))[2:]  
    data_length = data_length.zfill(32)     

    # Prefix 32-bit sized data length info
    bin_data = iter(data_length + string_to_binary(data))

    try:
        img = Image.open(input_img)
    except:
        raise ReadImageError(f"Image file {input_img} is inaccessible.")
    
    img_data = np.array(img)
    width, height = img.size
    total_pixels = height*width
    encoding_capacity = total_pixels*3 
    data_bits_length = len(data_length) + len(string_to_binary(data))  

    if data_bits_length > encoding_capacity:
        raise DataOverflowError("The data size is too big to fit in this image!")

    encode_complete = False
    for x in range(height):
        for y in range(width):

            pixel = img_data[x][y]
            for i in range(3):
                try:
                    d = next(bin_data)
                except StopIteration:
                    encode_complete = True
                    break
                
                if d=='0':
                    pixel[i] &= ~(1)  # reset LSB bit

                elif d=='1':
                    pixel[i] |= 1  # set LSB bit

            # ---------------------------------------------------------------
            if encode_complete:
                break
        # -----------------------------------------------------------
        if encode_complete:
            break
    
    try:
        encoded_img = Image.fromarray(img_data)
    except:
        raise WriteImageError("Error writing into new image")
        
    encoded_img.save(output_img)
    return None




# DECODER Section -------------------------------------------------------------

def decode_img(input_img, password=None):
    """ Extracts encoded text from input image with right password

    Parameters:
        input_img: Path of input image
        password: string key to decrypt the encrypted data
    
    Returns:
        data_string
    """
    extracted_bits = ""
    extracted_bits_count = 0
    data_bits_length = None 

    decode_complete = False

    try:
        img = Image.open(input_img)
    except:
        raise ReadImageError(f"Image file {input_img} is inaccessible.")
    
    img_data = np.array(img)
    width, height = img.size[0], img.size[1]

    for x in range(height):
        for y in range(width):

            pixel = img_data[x][y]

            for i in range(3):
                LSB_bit = str(pixel[i]&1)
                extracted_bits += LSB_bit
                extracted_bits_count += 1

                if extracted_bits_count==32 and data_bits_length is None:
                    data_length = int(extracted_bits, base=2) 
                    data_bits_length = data_length*8  

                    # Reset for actual data collection
                    extracted_bits = ""  
                    extracted_bits_count = 0

                elif extracted_bits_count == data_bits_length:
                    decode_complete = True
                    break
            
            if decode_complete:
                break
        
        if decode_complete:
            break
    
    extracted_data = binary_to_string(extracted_bits)

    if password is None:
        return extracted_data
    else:
        try:
            data = encrypt_decrypt(extracted_data, password, 'decrypt')
        except:
            raise PasswordError("INVALID Password! Please check.")
        return data




# Utility Functions -----------------------------------------------------------

def string_to_binary(data_string):
    """ Returns Binary Representation of string """

    return ''.join((bin(ord(c))[2:]).zfill(8) for c in data_string)


def binary_to_string(bin_string):
    """ Returns String representation of binary values string """

    return ''.join(chr(int(bin_string[i:i+8],2)) for i in range(len(bin_string))[::8])




# Custom Exceptions -----------------------------------------------------------
class InvalidModeError(Exception):
    pass

class ReadImageError(Exception):
    pass

class DataOverflowError(Exception):
    pass

class PasswordError(Exception):
    pass

class WriteImageError(Exception):
    pass




# DRIVER CODE -----------------------------------------------------------------------------

if __name__=='__main__':
    DATA = "Hello"
    PASSWORD = '123'
    ORIGINAL_IMAGE = r"data\image.png"
    ENCODED_IMAGE = r"data\enc_image.png"
    

    # Quick Tests -------------------------------------------------------------
    def test_encrypt_decrypt():
        print("[1] Testing encrypt_decrypt()...", end=' ')
        encrypted_data = encrypt_decrypt(DATA, PASSWORD, 'encrypt')
        decrypted_data = encrypt_decrypt(encrypted_data,PASSWORD, 'decrypt')
        if decrypted_data == DATA:
            print("OK")
            print("    - Data successfully retrieved")
        else:
            print("FAILED")
        print()


    def test_encode_img():
        print("[2] Testing encode_img()...", end=' ')
        PASSWORD = '123'
        encode_img(ORIGINAL_IMAGE, "Hello",ENCODED_IMAGE, PASSWORD)  
        try: 
            inp = Image.open(ORIGINAL_IMAGE)     
            inp_data = np.array(inp)
            op = Image.open(ENCODED_IMAGE)
            op_data = np.array(op)
        except:
            print("FAILED")
            print('    - ERROR with READ/WRITE')
            return

        if (inp_data == op_data).all():
            print("FAILED")
            print("    - Image NOT Modified.")
        else:
            print("Partially OK")
            print("    - New Modified Image created. ")
            print("    - Check needed if encoded correctly. ")
        print()


    def test_decode_img():
        print("[3] Testing decode_img()...", end=' ')
        expected_data = DATA
        decoded_data = decode_img(ENCODED_IMAGE, PASSWORD)
        if decoded_data == expected_data :
            print("OK")
            print("    - Returns original data from encoded image. ")
        else:
            print("FAILED")
            print(f'expected_data: {expected_data} ')
            print(f'decoded_data: {decoded_data} ')




    # Execute Tests in DEBUG MODE ---------------------------------------------
    if DEBUG is True:
        print("[DEBUG Mode ON] ------------------------------------------------")
        print()
        test_encrypt_decrypt()
        test_encode_img()
        test_decode_img()

# Code with more descriptive comments available at docs/doc_core.md