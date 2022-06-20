#!/usr/bin/env python3 

# -*- encoding: utf-8 -*-
import os
from time import sleep
from importlib.util import find_spec as find_module
from threading import Thread
from core.utils.printing import *

from core.cmds.main_console import ConsoleStart
from core.utils.sys_utils import SYSUtils
class Config:
    def __init__(self,opts = {
        "boot_config":
        {
            "show_banner_on_boot":True
        },
        "properties":
        {
            "max_socket_timeout":15,
            "encrypt_keylogs":False # if you wanna encrypt your keys log
        }
    }):
    self.config_json = "config.mka"
    self.lib_path = os.path.join(__file__,self.config_json)

class Bootloader:
    def __init__(self,silent=False):
        self.lib_path = os.path.dirname(__file__)
        self.clear_command = lambda:os.system("cls")
        self.necesarry_modules = [
            "Crypto",
            "pynput",
            "PyInstaller"
        ]
        self.necesarry_files = [
            f'{self.lib_path}\\__init__.py',
            f'{self.lib_path}\\base.py',  
            f'{self.lib_path}\\utils\\crypto.py', 
            f'{self.lib_path}\\utils\\networking.py', 
            f'{self.lib_path}\\utils\\printing.py', 
            f'{self.lib_path}\\utils\\randomize.py', 
            f'{self.lib_path}\\utils\\__init__.py'
        ]
    def __enter__(self):
        return self
    def __exit__(self,*args):
        return self
    def check_modules(self):
        for modules in self.necesarry_modules:
            if not find_module(modules):
                print_failure(f"Hata {modules} adlı modül eksik araç moduller tam olmadan çalışamaz pip install {modules} yazarak hatayı çözebilirsin !! ")
                print_status("Çıkılıyor...")
                os._exit(0)
            sleep(1.4)
    def check_requirement_files(self):
        for files in self.necesarry_files:
            if not os.path.exists(files):
                self.clear_command()
                print_failure(f"Hata {files} adlı dosya mevcut değil silinmiş veya taşınmış olabilir lütfen aracı tekrar kurup tekrar çalıştırmayı deneyiniz !!")
                print_status("Çıkılıyor...")
                os._exit(1) # hatalı çalışma exit kodu
            sleep(1.5)
    def __on_boot(self):
        if SYSUtils.get_sys_arch() != 64:
            print_failure("Üzgünüm ama araç sadece 64 bit için geçerlidir")
            os._exit(1)
        self.check_modules()
        self.check_requirement_files()
    def boot(self):
        """thr = Thread(target=self.__on_boot)
        thr.start()
        try:
            while thr.is_alive():
                print_spinner("th0rn başlatılıyor lütfen bekleyiniz")
        except KeyboardInterrupt:
            print_status("CTRL-C ALGILANDI ÇIKIŞ YAPILIYOR")
            os._exit(0)
        """
        ConsoleStart()
if __name__ == "__main__":
    pass