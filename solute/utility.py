"""Utility functions definitions for solute application"""

def string_to_binary(data: str) -> str:
    """ Returns Binary Representation of string """
    # # each character conversion procedure 
    # for c in data:
    #     ordinal = ord(c)
    #     binary_representation = bin(ordinal)
    #     binary_value = binary_representation[2:]
    #     byte_form = binary_value.zfill(8) 
    return ''.join((bin(ord(c))[2:]).zfill(8) for c in data)

def binary_to_string(bin_string:str) -> str:
    """ Returns String representation of binary values string """
    # reads a character represented in 8 bits  
    return ''.join(chr(int(bin_string[i:i+8],2)) for i in range(len(bin_string))[::8])