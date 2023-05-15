import hashlib
import secrets
import argon2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os

class SecureHasher(object):

    SALT_SIZE = 16
    KEY_SIZE = 32
    ITERATIONS = 512
    MEMORY = 512

    @staticmethod
    def hash_string(string):
        # if len(string) > 256:
        #     raise ValueError("Password length exceeds 256 characters")

        salt1 = secrets.token_bytes(SecureHasher.SALT_SIZE)
        salt2 = secrets.token_bytes(SecureHasher.SALT_SIZE)
        combined_salt = salt1 + salt2

        key = argon2.hash_password(string.encode('utf-8'), combined_salt, SecureHasher.ITERATIONS,
                                   SecureHasher.MEMORY, SecureHasher.KEY_SIZE)

        hash1 = hashlib.sha256(
            (key + combined_salt)).digest()

        hash2 = hashlib.sha512(
            (hash1 + combined_salt)).digest()

        hash3 = hashlib.blake2s((hash2 + combined_salt),
                                digest_size=32).hexdigest()

        return salt1 + salt2 + bytes.fromhex(hash3)

    @staticmethod
    def verify_string(string, hashed_string):
        # if len(string) > 256:
        #     return False

        salt1 = hashed_string[:SecureHasher.SALT_SIZE]
        salt2 = hashed_string[SecureHasher.SALT_SIZE:SecureHasher.SALT_SIZE*2]

        stored_hash = hashed_string[SecureHasher.SALT_SIZE*2:]

        combined_salt = salt1 + salt2

        derived_hash1 = hashlib.sha256(
            (argon2.hash_password(string.encode('utf-8'), combined_salt, SecureHasher.ITERATIONS,
                                  SecureHasher.MEMORY, SecureHasher.KEY_SIZE) + combined_salt)).digest()

        derived_hash2 = hashlib.sha512(
            (derived_hash1 + combined_salt)).digest()

        derived_hash3 = hashlib.blake2s((derived_hash2 + combined_salt),
                                        digest_size=32).hexdigest()

        derived_hash = bytes.fromhex(derived_hash3)

        return stored_hash == derived_hash
    
    
    class AESCipher:
        def __init__(self):
            self.key = pad(b'%\xe9\xd0\xf4\xbe\xbb: \xfcX\xceHq %\xa1nD\x9d\x0e\xd9\xb9\xec\x1bO_', AES.block_size)

        def encrypt(self, plaintext):
            iv = os.urandom(16)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            
            ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
            
            iv = base64.urlsafe_b64encode(iv).decode('utf-8').rstrip('=')
            ciphertext = base64.urlsafe_b64encode(ciphertext).decode('utf-8').rstrip('=')
            
            return iv + ':' + ciphertext

        def decrypt(self, ciphertext):
            iv, ciphertext = ciphertext.split(':')
            iv = base64.urlsafe_b64decode(iv + '==')
            
            ciphertext = base64.urlsafe_b64decode(ciphertext + '==')
            
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
            
            return plaintext.decode('utf-8')