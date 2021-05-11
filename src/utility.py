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


def binary_to_string(bin_string):
    """ Returns String representation of binary values string """
    return ''.join(chr(int(bin_string[i:i+8],2)) for i in range(len(bin_string))[::8])


if __name__=='__main__':
    pass
    # b = string_to_binary('Hi')
    # print(b)
    # s = binary_to_string(b)
    # print(s)