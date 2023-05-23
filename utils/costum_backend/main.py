from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import BasePasswordHasher

#Third-Party Libraries
import hashlib
import secrets
import argon2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os

class MyBackend(BaseBackend):
    
    def authenticate(request, username = None, password = None):
        try:
            user = User.objects.get(email = username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username = username)
            except User.DoesNotExist:
                return None
        
        hashed_password = user.password

        hashed_password = eval(hashed_password)
        
        if MyBackend.check_Userpassword(password, hashed_password) == True:
            return user
        
        return None
    
    def check_Userpassword(password, hashed_password):
        return MyHasher.verify(password, hashed_password)
    
    def validate_password(password, user = None):
        error_messages = []
        
        try:
            validate_password(password, user)
        except ValidationError as e:
            for i in range(len(e.messages)):
                error_messages.append(e.messages[i])
        
        return error_messages


class MyAdminBackend(ModelBackend):
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        return MyBackend.authenticate(request, username = username, password = password)



class MyHasher(BasePasswordHasher):

    algorithm = 'myhasher'
    
    SALT_SIZE = 16
    KEY_SIZE = 32
    ITERATIONS = 512
    MEMORY = 512

    def encode(self, string, salt = None, *args, **kwargs):
        salt1 = secrets.token_bytes(MyHasher.SALT_SIZE)
        salt2 = secrets.token_bytes(MyHasher.SALT_SIZE)
        combined_salt = salt1 + salt2

        key = argon2.hash_password(string.encode('utf-8'), combined_salt, MyHasher.ITERATIONS,
                                   MyHasher.MEMORY, MyHasher.KEY_SIZE)

        hash1 = hashlib.sha256(
            (key + combined_salt)).digest()

        hash2 = hashlib.sha512(
            (hash1 + combined_salt)).digest()

        hash3 = hashlib.blake2s((hash2 + combined_salt),
                                digest_size=32).hexdigest()
        return salt1 + salt2 + bytes.fromhex(hash3)
    
    def verify(string, hashed_string: bytes):
        salt1 = hashed_string[:MyHasher.SALT_SIZE]
        salt2 = hashed_string[MyHasher.SALT_SIZE:MyHasher.SALT_SIZE*2]

        stored_hash = hashed_string[MyHasher.SALT_SIZE*2:]

        combined_salt = salt1 + salt2

        derived_hash1 = hashlib.sha256(
            (argon2.hash_password(string.encode('utf-8'), combined_salt, MyHasher.ITERATIONS,
                                  MyHasher.MEMORY, MyHasher.KEY_SIZE) + combined_salt)).digest()

        derived_hash2 = hashlib.sha512(
            (derived_hash1 + combined_salt)).digest()

        derived_hash3 = hashlib.blake2s((derived_hash2 + combined_salt),
                                        digest_size=32).hexdigest()

        derived_hash = bytes.fromhex(derived_hash3)
        return stored_hash == derived_hash
    

class AESCipher:
    key = pad(
        b'%\xe9\xd0\xf4\xbe\xbb: \xfcX\xceHq %\xa1nD\x9d\x0e\xd9\xb9\xec\x1bO_', 
        AES.block_size)

    def encrypt(plaintext):
        iv = os.urandom(16)
        cipher = AES.new(AESCipher.key, AES.MODE_CBC, iv)

        ciphertext = cipher.encrypt(
            pad(plaintext.encode('utf-8'), AES.block_size))

        iv = base64.urlsafe_b64encode(iv).decode('utf-8').rstrip('=')
        ciphertext = base64.urlsafe_b64encode(
            ciphertext).decode('utf-8').rstrip('=')

        return iv + ':' + ciphertext

    def decrypt(ciphertext):
        iv, ciphertext = ciphertext.split(':')
        iv = base64.urlsafe_b64decode(iv + '==')

        ciphertext = base64.urlsafe_b64decode(ciphertext + '==')

        cipher = AES.new(AESCipher.key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

        return plaintext.decode('utf-8')
