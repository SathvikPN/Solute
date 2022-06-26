from hashlib import md5
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
from PIL import Image
import numpy as np

try:
    from exceptions import InvalidModeError, ReadImageError, DataOverflowError, WriteImageError, CorruptDataError, PasswordError
    from utility import string_to_binary, binary_to_string
except ModuleNotFoundError:
    from solute.exceptions import InvalidModeError, ReadImageError, DataOverflowError, WriteImageError, CorruptDataError, PasswordError
    from solute.utility import string_to_binary, binary_to_string


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
        raise ReadImageError(f"Image file {input_img} is inaccessible.")
    
    img_data = np.array(img)
    width, height = img.size
    total_pixels = height*width

    # each pixel of RGB --> 3 bytes --> 3 LSB bits --> 3 bits space per pixel to hide data
    encoding_capacity = 3*total_pixels

    # total bits in the data that needs to be hidden including 32 bits for specifying length of data
    data_bits = len(data_length) + len(string_to_binary(data))

    if data_bits > encoding_capacity:
        raise DataOverflowError("Data size too big to fit in this image!")

    encode_complete = False
    for x in range(height):
        for y in range(width):
            # reference of a mutable object 
            pixel = img_data[x][y]

            # each pixel has 3 LSB bits to hide data 
            for i in range(3):
                try:
                    d = next(bin_data)
                except StopIteration:
                    # no more binary data. objective accomplished
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
def decode_img(image_path:str, password:str='') -> str:
    """Extracts encoded text from the image and decrypts it with the password 

    Parameters:
        image: path to image
        password: key string to decrypt encoded text

    Returns:
        data_string
    """
    extracted_bits = []
    data_bits_length = None # length info

    try:
        img = Image.open(image_path)
    except:
        raise ReadImageError(f"Image file {image_path} is inaccessible.")
    
    img_data = np.array(img)

    # Image dimensions
    width, height = img.size 

    decode_complete = False 
    for x in range(height):
        for y in range(width):

            # current pixel RGB value
            pixel = img_data[x][y]

            # extract LSB bit of each RGB value
            for i in range(3):
                LSB_bit = str(pixel[i]&1)
                extracted_bits += LSB_bit

                if len(extracted_bits) == 32 and data_bits_length is None:
                    data_length = int(''.join(extracted_bits), base=2)
                    data_bits_length = data_length * 8 
                    # each character uses 8 bits

                    # Reset for actual data collection
                    extracted_bits = [] 
                
                # if all required bits are extracted, mark the process as completed
                elif len(extracted_bits) == data_bits_length:
                    decode_complete = True 
                    break 
            
            if decode_complete:
                break 
        if decode_complete:
            break
    if not decode_complete:
        raise CorruptDataError(f"Mismatched metadata and actual data. {image_path} is Corrupt!")
    
    binary_values = ''.join(extracted_bits)
    extracted_data = binary_to_string(binary_values)

    if password == '':
        return extracted_data
    else:
        try:
            data = encrypt_decrypt(extracted_data, password, mode='decrypt')
        except:
            raise PasswordError("Invalid Password. Please check.")
        return data 





