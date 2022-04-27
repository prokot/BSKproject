from base64 import b64decode, b64encode
import hashlib
from lib2to3.pgen2.pgen import generate_grammar
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES,PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad,unpad
from os.path import exists
import json

class Crpto:

    def __init__(self,app) -> None:
        self.app = app
        if not (exists(self.app.port +'/public/public_key.txt') and exists(self.app.port +'/private/private_key.txt')):
            random_gen = Random.new().read
            key = RSA.generate(2048,random_gen)
            self.public = key.public_key().exportKey()
            self.private = key
            
            

    
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
                pvKey.write(b64encode(self.cipher.encrypt(pad(self.private.exportKey(),AES.block_size))).decode('ascii'))
                pvKey.close()

    def generateSesKey(self):
        self.session = get_random_bytes(AES.block_size)
        return self.session
        
    def encryptDataRSA(self,data,pbkey):
        cipher_rsa = PKCS1_OAEP.new(RSA.import_key(pbkey))
        return cipher_rsa.encrypt(data)

    def decryptDataRSA(self,data,pvkey):
        cipher_rsa = PKCS1_OAEP.new(pvkey)
        return cipher_rsa.decrypt(data)

    def encryptDataCBC(self,data,key):
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        iv = b64encode(cipher.iv).decode('utf-8')
        ct = b64encode(ct_bytes).decode('utf-8')
        return {'iv':iv, 'ciphertext':ct}

    def decryptDataCBC(self,data,key):
        try:
            b64 = data
            iv = b64decode(b64['iv'])
            ct = b64decode(b64['ciphertext'])
            cipher = AES.new(key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt
        except (ValueError, KeyError):
            print("Incorrect decryption")
