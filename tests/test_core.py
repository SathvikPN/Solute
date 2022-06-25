import pytest 

# resolve relative import issues at windows 
import sys, os.path
solute_pkg = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
+ '/solute/')
sys.path.append(solute_pkg)
import core 

DATA = "Hello 123 App testing"
PASSWORD = "pwd@22"
ORIGINAL_IMAGE = "data/image.png"
ENCODED_IMAGE = "data/enc_image.png"

def test_encrypt_decrypt():
    enc_data = core.encrypt_decrypt(DATA, PASSWORD, mode='encrypt')
    decrypted_data = core.encrypt_decrypt(enc_data, PASSWORD, mode='decrypt')
    assert decrypted_data == DATA








