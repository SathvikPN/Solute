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
from cryptography.fernet import Fernet
from cv2 import imread, imwrite
import inspect

from .utility import string_to_binary, binary_to_string
from .custom_exceptions import DataOverflowError, FileError, PasswordError
from .core import *


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
    command_line_interface()