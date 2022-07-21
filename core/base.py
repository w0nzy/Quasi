#!/usr/bin/env python3 

# -*- encoding: utf-8 -*-
import os
import subprocess
from time import sleep
from importlib.util import find_spec as find_module
from threading import Thread
from core.utils.printing import *

from core.utils.sys_utils import SYSUtils

from core.cmds.main_console import ConsoleStart
class Bootloader:
    def __init__(self,silent=False):
        self.lib_path = os.path.dirname(__file__)
        self.clear_command = lambda:os.system("cls")
        self.necesarry_modules = {
            "requests":"requests",
            "pycryptodome":"Crypto",
            "pynput":"pynput",
            "cx_Freeze":"cx_Freeze",
            "json":"json",
            "pyreadline":"readline"
        }
        self.necesarry_files = [
            f'{self.lib_path}\\__init__.py',
            f'{self.lib_path}\\base.py',  
            f'{self.lib_path}\\utils\\crypto.py', 
            f'{self.lib_path}\\utils\\networking.py', 
            f'{self.lib_path}\\utils\\printing.py', 
            f'{self.lib_path}\\utils\\randomize.py', 
            f'{self.lib_path}\\utils\\__init__.py'
        ]
    def download_package(self,package: str):
        l = os.path.join(os.path.dirname(os.path.dirname(os.__file__)),"Scripts","pip.exe")
        command = l + " " + "install" + " " + package
        subprocess.call(command.split(" "),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    def __enter__(self):
        return self
    def __exit__(self,*args):
        return self
    def is_loaded(self,package: str):
        try:
            __import__(package)
        except:
            return False
        return True
    def check_modules(self):
        for modules in self.necesarry_modules.keys():
            optional_name = self.necesarry_modules[modules]
            if not self.is_loaded(optional_name):
                print_failure(f"Hata {optional_name} adlı modül eksik araç moduller tam olmadan çalışamaz pip install {optional_name} yazarak hatayı çözebilirsin !! ")
                self.download_package(modules)
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
        #self.check_requirement_files()
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