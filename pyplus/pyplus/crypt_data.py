# import required module
from cryptography.fernet import Fernet
import os.path

def generate_key_for_encryption(filename):
    # key generation
    key = Fernet.generate_key()

    # string the key in a file
    with open(filename, 'wb') as file:
        file.write(key)
    
def encrypt_file(data,out_filename="a.enc",key_filename="a.key"):
    if not(os.path.isfile(key_filename)):
        generate_key_for_encryption(key_filename)

    with open(key_filename,'rb') as key_file:
        key = key_file.read()
        cipher = Fernet(key)
        encrypted_data = cipher.encrypt(data)

        with open(out_filename,'wb') as enc_file:
            enc_file.write(encrypted_data)

def decrypt_file(in_filename="a.enc",key_filename="a.key"):
    with open(key_filename,'rb') as key_file:
        key = key_file.read()
    
    cipher = Fernet(key)    

    with open(in_filename,'rb') as enc_file:
        decrypted_data = cipher.decrypt(enc_file.read())
        
        return decrypted_data

def decrypt_and_save_file(in_filename="a.enc",out_filename="a.dec",key_filename="a.key"):
    res = decrypt_file(filename=in_filename,key_filename=key_filename)
    with open(out_filename,'wb') as dec_file:
        dec_file.write(res)