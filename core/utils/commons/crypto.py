#!/usr/bin/env python3

# -*- encoding: utf-8 -*-


import base64
import binascii 
from Crypto.Cipher import AES
from core.utils.commons.randomize import random_byte_generator,random_string
from core.utils.printing import *
from core.utils.commons.io_utils import IOUtils,Modes
from Crypto.PublicKey import RSA as Rsa
from Crypto.Cipher import PKCS1_OAEP as Pkcs1Oaep


class AESCipher:
    """Bu modül AES ile verilerini şifrelemek ve deşifrelemek için kullanılır"""

    def __init__(self,key=random_byte_generator(key_size=32,beautify=True),iv=random_byte_generator(key_size=32,beautify=True)) -> None:
        """Not:Lütfen key bit uzunluğu ile iv uzunluğunu aynı yapın LÜTFEN"""
        self.iv = iv
        self.key = key
        self.initialization_vector = self.decoder(iv)
        self.cipher_key = self.decoder(key)
        self.cipher_types = {
            32:"AES-256",
            16:"AES-128"
        }
        try:
            self.cipher_type = self.cipher_types[len(self.cipher_key)]
        except KeyError as exc:
            raise Exception("Invalid bitsize %s") from exc
    def __enter__(self): return self
    def __exit__(self,*args): pass
    @staticmethod
    def decoder(key: str) -> bytes:
        return binascii.unhexlify(key)

    def __repr__(self):
        return "<%s AES-MODE=%s Key=%s Iv=%s Keybitsize=%s>" % (self.__class__.__name__,self.cipher_type,self.key,self.iv,len(self.cipher_key))

    def encrypt(self,data: bytes) -> bytes:
        data = bytes(data,encoding="utf-8") if not isinstance(data,bytes) else data
        cipher = AES.new(self.cipher_key,AES.MODE_GCM,self.initialization_vector)
        return cipher.encrypt(data)

    def decrypt(self,data: bytes) -> bytes:
        cipher = AES.new(self.cipher_key,AES.MODE_GCM,self.initialization_vector)
        return cipher.decrypt(data)      

    @property
    def get_private_key_as_hex(self):
        return self.key

    @property
    def get_private_key_as_byte(self):
        return self.cipher_key

    @property
    def get_iv_as_hex(self):
        return self.iv

    @property
    def get_iv_as_byte(self):
        return self.initialization_vector


class RSACipher:

    def __init__(self,key_size = None,private_key = None,public_key = None,silent=False) -> None:
        self.private_key = private_key
        self.public_key = public_key
        if self.private_key is None and self.public_key is None:
            if not key_size in (1024,2048,4096):
                raise KeyError("Hatalı anahtar bit'i sadece 1024,2048,4096 seçilebilir")
            if not silent:
                print_status("Generating new %s bit keys" % (key_size))
            key_handler = Rsa.generate(key_size)
            priv_key,pub_key = key_handler.exportKey(),key_handler.public_key().exportKey()
            self.private_key = priv_key
            self.public_key = pub_key
        else:
            self.private_key = private_key
            self.public_key = public_key 
        self.encryption_key = Rsa.import_key(self.public_key)
        self.decryption_key = Rsa.import_key(self.private_key)
        self.decryption_cipher = Pkcs1Oaep.new(self.decryption_key)
        self.encryption_cipher = Pkcs1Oaep.new(self.encryption_key)
    
    def encrypt(self,data: bytes) -> bytes:
        data = bytes(data,encoding="utf-8") if not isinstance(data, bytes) else data
        encrypted_data = self.encryption_cipher.encrypt(data)
        return base64.b85encode(encrypted_data)

    def decrypt(self,data: bytes) -> bytes:
        decrypted_data = self.decryption_cipher.decrypt(base64.b85decode(data))
        return decrypted_data

    def save_keys(self):
        random_private_key_file_name = "private_" + random_string(4)
        random_public_key_file_name = "public_" + random_string(4)
        print_status("Yeni dosyalar oluşturuluyor lütfen bekleyiniz")
        if IOUtils.create_file(random_private_key_file_name):
            print_succes("Başarılı bir şekilde oluşturuldu",random_private_key_file_name)
        if IOUtils.create_file(random_public_key_file_name):
            print_succes("Başarılı bir şekilde oluşturuldu",random_public_key_file_name)
        IOUtils.create_file(random_public_key_file_name)
        with IOUtils(file_name=random_private_key_file_name,mode=Modes.MODE_WRITE_AS_BINARY) as private_key_file_io_handler:
            try:
                private_key_file_io_handler.write(self.private_key)
                print_succes(f"Private key şuraya kaydedildi -> {random_private_key_file_name}")
            except Exception as private_key_save_error:
                print_failure(f"Hata private key kaydedilemedi sebebi ise {private_key_save_error}")
        with IOUtils(file_name=random_public_key_file_name,mode=Modes.MODE_WRITE_AS_BINARY) as public_key_file_io_handler:
            try:
                public_key_file_io_handler.write(self.public_key)
                print_succes(f"Public key şuraya kaydedildi -> {random_public_key_file_name}")
            except Exception as public_key_save_error:
                print_failure(f"Hata public key kaydedilemedi sebebi ise {public_key_save_error}")

if __name__ == "__main__":
    pass
