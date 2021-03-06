# Comments enriched version
`src/core.py` 

```py
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
        None
    """

    if password is None:
        # Bypass password encryption of data
        data = text
    else:
        data = encrypt_decrypt(text, password, mode='encrypt')

    # Process Encrypted data

    # 32-bit info about length of data to be encoded
    data_length = bin(len(data))[2:]  # eg: '0b11101' --> '11101'
    data_length = data_length.zfill(32)

    # Encode data length info with actual data and create an iterator
    bin_data = iter(data_length + string_to_binary(data))

    # read cover image 
    try:
        img = Image.open(input_img)
    except:
        raise ReadImageError(f"Image file {input_img} is inaccessible.")
    
    img_data = np.array(img)

    # Image dimensions
    width, height = img.size

    total_pixels = height*width
    # each pixel of RGB --> 3 bytes --> 3 LSB bits --> 3 bits space per pixel to hide data
    encoding_capacity = total_pixels*3 

    # total bits in the data that needs to be hidden including 32 bits for specifying length of data
    data_bits = len(data_length) + len(string_to_binary(data))  
    # Each character is stored using eight bits of information, giving a total number of 256 different characters

    if data_bits > encoding_capacity:
        raise DataOverflowError("The data size is too big to fit in this image!")

    encode_complete = False

    # traverse cover image pixels left to right and top to bottom fashion
    for x in range(height):
        for y in range(width):

            pixel = img_data[x][y]

            # each pixel have 3 LSB bits to hide data
            for i in range(3):
                try:
                    d = next(bin_data)
                except StopIteration:
                    # No more binary data. Objective accomplished
                    encode_complete = True
                    break
                
                # modify image bit according to data bit
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

    # length of data-bits exist in first 32 bits of cover image
    data_bits_length = None 
    # updates after 32 bits of cover image is read

    decode_complete = False

    # read cover image 
    try:
        img = Image.open(input_img)
    except:
        raise ReadImageError(f"Image file {input_img} is inaccessible.")
    
    img_data = np.array(img)

    # Image dimensions
    width, height = img.size[0], img.size[1]

    # traverse image pixels
    for x in range(height):
        for y in range(width):

            # current pixel RGB value
            pixel = img_data[x][y]

            for i in range(3):
                # extract LSB bit of each RGB value
                LSB_bit = str(pixel[i]&1)
                extracted_bits += LSB_bit
                extracted_bits_count += 1

                # First 32-bits represent data size. Actual data start 33rd bit onwards
                if extracted_bits_count==32 and data_bits_length is None:
                    data_length = int(extracted_bits, base=2) 
                    data_bits_length = data_length*8  # each character uses 8 bits

                    # Reset for actual data collection
                    extracted_bits = ""  
                    extracted_bits_count = 0

                # if all required bits are extracted, mark the process as completed
                elif extracted_bits_count == data_bits_length:
                    decode_complete = True
                    break
            
            if decode_complete:
                break
        
        if decode_complete:
            break
    
    extracted_data = binary_to_string(extracted_bits)

    if password is None:
        # return extracted data as it is.
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

    # Explicit breakdown-------------
    # for c in string:
    #     ordinal = ord(c)
    #     binary_representation = bin(ordinal)
    #     binary_value = binary_representation[2:]
    #     binary_form = binary_value.zfill(8)


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
            print(f'decoded_data: {decoded_data[:50]} ')




    # Execute Tests in DEBUG MODE ---------------------------------------------
    if DEBUG is True:
        print("[DEBUG Mode ON] ------------------------------------------------")
        print()
        test_encrypt_decrypt()
        test_encode_img()
        test_decode_img()



```