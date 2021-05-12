#!/usr/bin/python3

"""
Least Significant Bit Steganography
---------------------------------------
Name: LSB Steganography Application
Author: Sathvik PN
GitHub: https://github.com/SathvikPN/Steganography-application
"""

from hashlib import md5
from base64 import urlsafe_b64encode
from custom_exceptions import DataOverflowError, FileError, PasswordError
from cryptography.fernet import Fernet
from cv2 import imread, imwrite
from utility import string_to_binary, binary_to_string
from custom_exceptions import *
import inspect

# -------------------------------------------------------------------------------
def encrypt_decrypt(string, password, mode='encode'):
    """ Encodes or Decodes raw data w.r.t password based on mode specified. """
    _hash = md5(password.encode()).hexdigest() # get hash of password
    cipher_key = urlsafe_b64encode(_hash.encode()) # use the hash as the key of encryption
    cipher = Fernet(cipher_key) # get the cipher based on the cipher key
    if mode == 'encode':
        return cipher.encrypt(string.encode()).decode() #encrypt the data
    else:
        return cipher.decrypt(string.encode()).decode() #decrypt the data


# -----------------------------------------------------------------------------------
def encode(input_filepath, text, output_filepath, password=None):
    """ Creates an encoded image based on text with password and fed input image """
    if password is None:
        # bypass raw data encryption
        data = text
    else:
        # If password is provided, encrypt the data with given password
        data = encrypt_decrypt(text,password,'encode') 

    # get length of data to be encoded
    data_length = bin(len(data))[2:].zfill(32) 
    
    # add length of data with actual data and get the binary form of whole thing
    bin_data = iter(data_length + string_to_binary(data)) 

    # read the cover image
    img = imread(input_filepath,1) 

    if img is None:
        # if image is not accessible, raise an exception
        raise FileError("The image file '{}' is inaccessible".format(input_filepath))

    # get height and width of cover image
    height,width = img.shape[0],img.shape[1]

    # maximum number of bits of data that the cover image can hide
    total_pixels = height*width
    encoding_capacity = total_pixels*3

    # total bits in the data that needs to be hidden including 32 bits for specifying length of data
    total_bits = 32+len(data)*8  # Multiplication has higher precedence than addition

    if total_bits > encoding_capacity:
        # if cover image can't hide all the data, raise DataError exception
        raise DataOverflowError("The data size is too big to fit in this image!") 

    completed = False
    modified_bits = 0

    # traverse all the pixels of the whole image in left to right, top to bottom fashion 
    for i in range(height):
        for j in range(width):

            # get the current pixel that is being traversed
            pixel = img[i,j] 

            for k in range(3): # get next 3 bits from the binary data that is to be encoded in image
                try:
                    x = next(bin_data)
                except StopIteration:
                    # if there is no data to encode, mark the encoding process as completed
                    completed = True
                    break

                # if the bit to be encoded is '0' and the current LSB is '1'
                if x == '0' and pixel[k]%2==1: 
                    pixel[k] -= 1 # change LSB from 1 to 0
                    modified_bits += 1 # increment the modified bits count

                # elif the bit to be encoded is '1' and the current LSB is '0'
                elif x=='1' and pixel[k]%2==0: 
                    pixel[k] += 1 # change LSB from 0 to 1
                    modified_bits += 1 # increment the modified bits count
            
            if completed:
                break

        if completed:
            break

    # create a new image with the modified pixels
    written = imwrite(output_filepath,img) 

    if not written:
        raise FileError("Failed to write image '{}'".format(output_filepath))

    # calculate how many bits of the original image are changed 
    # in order to encode the secret message and 
    # calculate the percentage of data loss from it.
    loss_percentage = (modified_bits/encoding_capacity)*100
    return loss_percentage
    

# -----------------------------------------------------------------------------
def decode(input_filepath, password=None):
    """ Decodes the secret data from the cover image with right password """
    result = ''
    extracted_bits = 0
    completed = False
    number_of_bits = None

    # open image 
    img = imread(input_filepath)

    if img is None:
        raise FileError("The image file '{}' is inaccessible".format(input_filepath))
    
    height,width = img.shape[0],img.shape[1]  # Image dimensions

    # traverse all pixels in image from left to right and top to bottom fashion
    for i in range(height):
        for j in range(width):
            # Current pixel (RGB values)
            for k in img[i,j]:
                # extract LSB of RGB values
                result += str(k%2)
                extracted_bits += 1

                # First 32-bits represent data size. Actual data if after that
                if extracted_bits==32 and number_of_bits is None:
                    number_of_bits = int(result,2)*8
                    result = ''  # for actual data collection
                    extracted_bits = 0

                # if all required bits are extracted, mark the process as completed
                elif extracted_bits == number_of_bits:
                    completed = True
                    break

            if completed:
                break
        
        if completed:
            break

    if password is None:
        # data doesnot require password to unlock
        return binary_to_string(result)

    else:
        # try to decrypt the data with the given password and return decrypted data 
        try:
            return encrypt_decrypt(binary_to_string(result),password,'decode')
        except:
            raise PasswordError("Invalid password!")



# Command Line Interface--------------------------------------------------------------
def command_line_interface():
    """ Minimal Command Line Interface for the appliction """
    file_info = inspect.cleandoc("""
    ***********************************************************************************
    Steganography Application
    > Encrypt and Embed confidential data in an Image with right password.
    > https://github.com/SathvikPN/Steganography-application
    """)
    print(file_info, end='\n\n')

    # -----------------------------------------------------------------------------------
    menu = inspect.cleandoc("""
    ----- MENU -----
    [1]. Encrypt
    [2]. Decrypt

    Select your choice(1/2) : 
    """)

    choice = input(menu)

    def data_canvas():
        """ Decorate space for input data """
        print(inspect.cleandoc("""
        Enter Secret Data : (leave blank line to finish)
        ----------------------------------------------------------------
        """))
        datalines = []
        while True:
            line = input()
            if line:
                datalines.append(line)
            else:
                break
        data = '\n'.join(datalines)
        print(inspect.cleandoc("""
        ----------------------------------------------------------------
        """))
        return data
    
    if choice == "1":
        ip_file = input('Enter cover image name(path)(with extension): ')
        text = data_canvas()
        pwd = input('Enter password: ')
        op_file = input('Enter output image name(path)(with extension): ')

        try:
            loss = encode(ip_file,text,op_file,pwd)
        except FileError as fe:
            print(inspect.cleandoc("""
            -------------------------------------------------
            ERROR: {}
            -------------------------------------------------
            """.format(fe)))
            exit()
        except DataOverflowError as dfe:
            print(inspect.cleandoc("""
            -------------------------------------------------
            ERROR: {}
            -------------------------------------------------
            """.format(dfe)))
            exit()
        
        print(inspect.cleandoc("""
        Encoded successfully.
        Image Data loss : {:.4f}%
        """.format(loss)))

    elif choice == "2":
        ip_file = input('Enter encoded_image path: ')
        pwd = input('Enter password: ')

        try:
            data = decode(ip_file, pwd)
        except FileError as fe:
            print(inspect.cleandoc("""
            -------------------------------------------------
            ERROR: {}
            -------------------------------------------------
            """.format(fe)))
            exit()

        except PasswordError as pe:
            print(inspect.cleandoc("""
            -------------------------------------------------
            ERROR: {}
            -------------------------------------------------
            """.format(pe)))
            exit()

        print(inspect.cleandoc("""
        Decrypted Data: 
        -------------------------------------------------
        {}
        -------------------------------------------------
        """.format(data)))

    else:
        print("INVALID choice.")
        

# ------------------------------------------------------------------------------
if __name__=='__main__':
    # pass 
    command_line_interface()
    



    
