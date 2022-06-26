import pytest 
from solute import core, exceptions, utility

DATA = "Hello 123 App testing"
PASSWORD = "pwd@22"
ORIGINAL_IMAGE = "data/image.png"
ENCODED_IMAGE = "data/enc_image.png"

def test_encrypt_decrypt():
    enc_data = core.encrypt_decrypt(DATA, PASSWORD, mode='encrypt')
    decrypted_data = core.encrypt_decrypt(enc_data, PASSWORD, mode='decrypt')
    assert decrypted_data == DATA

def test_encode_decode_img():
    core.encode_img(ORIGINAL_IMAGE, DATA, ENCODED_IMAGE, PASSWORD)
    expected_data = DATA
    decoded_data = core.decode_img(ENCODED_IMAGE, PASSWORD)
    assert decoded_data == expected_data
    