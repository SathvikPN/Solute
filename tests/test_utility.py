import pytest
from solute import utility

def test_string_to_binary():
    text = "hi"
    binary_values = [bin(ord(c))[2:] for c in text]
    bytes_form = [None]*len(binary_values)
    for i,e in enumerate(binary_values):
        bytes_form[i] = e.zfill(8)
    expected = ''.join(bytes_form)
    actual = utility.string_to_binary(text)
    assert actual==expected

def test_binary_to_string():
    byte_form = '1011010110101010'
    grouping_chars = [byte_form[i:i+8] for i in range(0,len(byte_form), 8)]
    expected = ''.join([chr(int(x,2)) for x in grouping_chars])
    actual = utility.binary_to_string(byte_form)
    assert actual==expected
