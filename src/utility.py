# assistive utility functions

def string_to_binary(string):
    """ Returns Binary Representation of string """
    return ''.join((bin(ord(c))[2:]).zfill(8) for c in string)
    
    # Explicit breakdown-------------
    # for c in string:
    #     ordinal = ord(c)
    #     binary_representation = bin(ordinal)
    #     binary_value = binary_representation[2:]
    #     binary_value.zfill(8)



