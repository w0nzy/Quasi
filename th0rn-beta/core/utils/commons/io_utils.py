#!/usr/bin/env python3

# -*- encoding: utf-8 -*-
import io
import os
from typing import *
from enum import Enum
from core.utils.commons.exceptions import *
class Modes(Enum):
    MODE_WRITE = "w"
    MODE_WRITE_AS_BINARY = "wb"
    MODE_READ = "r"
    MODE_READ_AS_BINARY = "rb"
    MODE_WRITE_PLUS = "w+" # support read mode
    MODE_WRITE_AS_BINARY_PLUS = "wb+"
    MODE_READ_AS_BINARY_PLUS = "rb+"
    MODE_APPEND = "a"
    MODE_APPEND_PLUS = "a+" # support read mode 
    MODE_APPEND_AS_BINARY = "ab"
    MODE_APPEND_AS_BINARY_PLUS = "ab+" 
class IOUtils:
    def __init__(self,file_name=None,mode=Modes.MODE_WRITE,auto_kill=True):
        if mode in (
            Modes.MODE_READ,
            Modes.MODE_READ_AS_BINARY,
            Modes.MODE_READ_AS_BINARY_PLUS
        ): # BUG FIXED
            if not os.path.exists(file_name) or not os.path.isfile(file_name) or os.path.isdir(file_name):
                raise ItsNotFileError("Hata %s dosya değil veya mevcut değil" % (file_name))
            if not hasattr(Modes,mode._name_):
                raise InvalidModeError("Hata %s geçerli bir mod değil lütfen okuma modlarına dikkat ederek modu giriniz !!" % (mode))
        self.fd = open(file_name,mode=mode._value_)
        self.mode = mode._value_
        self.file_name = file_name
        self.auto_kill = auto_kill
    def __enter__(self):
        return self
    def __exit__(self,*args):
        """
        Why *args in params
        because without *args TypeError: __exit__() takes 1 positional argument but 4 were given
        """
        if self.auto_kill:
            try:
                self.fd.close()
            except:
                pass
            finally:
                self.fd.close()
    def __repr__(self) -> str:
        return "< %s file=%s mode=%s  >" % (self.__class__.__name__,self.file_name,self.mode)
    def read(self) -> Any:
        """
        read(bufsize=1024) # default
        if you in wrong read modes it's return False
        """
        return self.fd.read() if not self.mode in (
            Modes.MODE_WRITE._value_,
            Modes.MODE_WRITE_AS_BINARY._value_,
            Modes.MODE_APPEND_AS_BINARY._value_,
            Modes.MODE_APPEND._value_
            ) else False
    def read_line_by_line(self) -> list:
        return self.fd.readline()
    def read_line_by_lines(self) -> list:
        return self.fd.readlines()
    def write(self,data) -> bool:
        """
        write(data)
        write("127.0.0.1") e.g
        if succesfully writed it's return True else False
        """ 
        try:
            self.fd.write(data)
            return True
        except WriteError as write_error:
            raise WriteError("Hata %s adlı dosya yazılırken bir hata oluştu") from write_error
    @staticmethod
    def create_file(file_name: str) -> bool:
        """ 
        İf a error occured while new file creation function return None e.g create_file("C:\\Windows\\hello") else if file is exists already return False if succesfully created return True
        """
        if not os.path.exists(file_name):
            try:
                with open(file_name,"w") as fd:
                    fd.close()
                    return True
            except:
                return None # Fail
        return False # file exists
    @staticmethod
    def save_as(file_name:str,data) -> bool:
        mode = "w"
        if isinstance(data,bytes):
            mode = "wb"
        try:
            with open(file_name,mode) as fd:
                fd.write(data)
            return True
        except:
            return False

if __name__ == "__main__":
    pass