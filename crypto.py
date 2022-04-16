from base64 import b64decode, b64encode
import hashlib
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES,PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad,unpad
from os.path import exists

class Crpto:

    def __init__(self,app) -> None:
        self.app = app
        if not (exists(self.app.port +'/public/public_key.txt') and exists(self.app.port +'/private/private_key.txt')):
            random_gen = Random.new().read
            key = RSA.generate(1024,random_gen)
            self.public = key.public_key().exportKey()
            self.private = key.exportKey()
            
            

    
    def generateLocalKey(self,pswrd):
        hash_obj = hashlib.sha256(pswrd.encode('ascii'))
        self.pwdHash = hash_obj.digest()
        

        if (exists(self.app.port +'/public/public_key.txt') and exists(self.app.port +'/private/private_key.txt')):
            with open(self.app.port +'/public/public_key.txt','r') as pbKey:
                self.public = RSA.import_key(pbKey.read())
                pbKey.close()

            with open(self.app.port +'/private/private_key.txt','r') as pvKey:
                lines = pvKey.readlines()
                iv = b64decode(lines[0].encode('ascii'))
                self.cipher = AES.new(hash_obj.digest(),AES.MODE_CBC,iv)
                self.private = RSA.import_key(unpad(self.cipher.decrypt(b64decode(lines[1].encode('ascii'))),AES.block_size))
                pvKey.close()
        else:
            with open(self.app.port +'/public/public_key.txt','w+') as pbKey:
                pbKey.write(self.public.decode('ascii'))
                pbKey.close()
            
            with open(self.app.port +'/private/private_key.txt','w+') as pvKey:
                self.cipher = AES.new(hash_obj.digest(),AES.MODE_CBC)
                pvKey.write(b64encode(self.cipher.iv).decode('ascii') + "\n")
                pvKey.write(b64encode(self.cipher.encrypt(pad(self.private,AES.block_size))).decode('ascii'))
                pvKey.close()

        
    def encryptData(self,data):
        cipher_rsa = PKCS1_OAEP.new(self.public)
        return cipher_rsa.encrypt(data)

    def decryptData(self,data):
        cipher_rsa = PKCS1_OAEP.new(self.private)
        return cipher_rsa.decrypt(data)