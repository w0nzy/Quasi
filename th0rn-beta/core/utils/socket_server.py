#!/usr/bin/env python3

# -*- encoding: utf-8 -*-
import os
import time
import socket
import threading
from core.utils.printing import *
from core.utils.commons.exceptions import SocketServerError
from core.utils.commons.networking import ip_validator,IpToFamily
key = "30e79f45d426cabf4aeaebb7192c77b5742abf2a1a993bc0a26ebb272bf9809e"
iv = '30e79f45d426cabf4aeaebb7192c77b5742abf2a1a993bc0a26ebb272bf9809e'
class DataBase:
    all_client_num_tags = {}
    all_client_addrs = {}
    all_client_socks = {}
    all_client_hostnames = {}
if hasattr(os,"_exit"):
    exit = lambda:os._exit(0)

class SocketServer(DataBase):
    def __init__(self,host = "127.0.0.1", port = 4444,max_listen_devices = 20,aes_key = key,aes_iv = key) -> None:
        self.socket = None
        self.is_connectable = False
        self.is_binded = False
        self.credentials = {
            "aes_credentials":{
                "aes_key":aes_key,
                "aes_iv":aes_iv
            },
            "host":host,
            "port":int(port),
            "max_listen_devices":int(max_listen_devices)
        }
        self.create_sock()
    def __enter__(self):
        return self
    def __exit__(self,*args):
        pass
    def create_sock(self):
        if self.socket is None:
            print_status("Soket nesnesi oluşturuluyor")
            ip_family = IpToFamily(self.credentials["host"])
            if ip_family:
                try:
                    self.socket = socket.socket(ip_family,socket.SOCK_STREAM)
                    print_succes("Soket nesnesi oluşturuldu")
                except SocketServerError as sock_creat_err:
                    print_failure("Hata soket nesnesi oluşturulamadı sebebi ise ",sock_creat_err)
                    os._exit(1)
            else:
                print_failure("Hata geçersiz ip adresi",self.credentials["host"])

    def bind_sock(self) -> None:
        print_status("Soket bind ediliyor lütfen bekleyiniz ..")
        if self.socket:
            if not self.is_binded:
                try:
                    self.is_binded = True
                    self.socket.bind((self.credentials["host"],self.credentials["port"]))
                    self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                    self.socket.listen(self.credentials["max_listen_devices"])
                    print_succes(f"Soket bind edildi {self.credentials['host']}:{self.credentials['port']} üzerinden")
                except SocketServerError as sock_bind_err:
                    print_failure("Hata soket verilen bilgiler üzerinden bind edilemedi sebep ",sock_bind_err)
            else:
                print_failure("Soket zaten bind edilmiş ")
        else:
            print_failure("Soket oluşturulmamış lütfen oluşturduktan sonra bind ediniz")

    def __accept_clients(self):
        counter = 1
        while True:
            try:
                cli_sock,addrs = self.socket.accept()
                hostname = cli_sock.recv(4096).decode("utf-8")
                ip,port = addrs
                DataBase.all_client_num_tags[counter]=ip
                DataBase.all_client_addrs[ip]=port
                DataBase.all_client_hostnames[ip]=hostname
                DataBase.all_client_socks[ip]=cli_sock
                cli_sock.setblocking(True)
                print_status(f"Yeni bağlanan bir cihaz {ip}:{port}({hostname}) {counter}.")
                counter+=1
                time.sleep(1)
                continue
            except SocketServerError as cli_accept_err:
                print_failure("Hata yeni bir cihaz bağlanırken bir hata oluştu",cli_accept_err)
                continue
            # BUG FIXED
    def start(self):
        print_status("Server artık bağlanılabilir şekilde")
        self.is_connectable = True
        t = threading.Thread(target=self.__accept_clients)
        t.start()
    def close(self):
        if self.socket:
            try:
                self.socket.close()
                print_succes("Soket kapatıldı")
            except SocketServerError:
                self.socket.close()
            finally:
                self.socket.close()
            if DataBase.all_client_socks:
                for sock in DataBase.all_client_socks.values():
                    try:
                        sock.close()
                    except:
                        sock.close()
                    finally:
                        sock.close()
            os._exit(0)
    def __repr__(self) -> str:
        return "<%s host=%s port=%s max_listen_devices=%s socket=%s is_binded=%s is_connectable=%s total_connected_clients=%s>" % (
            self.__class__.__name__,
            self.credentials["host"],
            self.credentials["port"],
            self.credentials["max_listen_devices"],
            self.socket,
            self.is_binded,
            self.is_connectable,
            len(DataBase.all_client_socks)
        )
    def quick_bind(self):
        self.create_sock()
        self.bind_sock()
        self.start()
        
if __name__ == "__main__":
    pass # do anything