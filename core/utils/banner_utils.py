#!/usr/bin/env python3 

# -*- encoding: utf-8 -*-

import os
import random

from core.utils.printing import *
from core.utils.printing import Color

from core.utils.io_utils import Modes
from core.utils.io_utils import IOUtils

from core.utils.exceptions import NoBannerFoundError

class Banner:
    def __init__(self,banner = None):
        self.target_dir = os.path.join(os.path.dirname(__file__),"..","data","banner")
        self.__banner_filter = lambda file: file if file.endswith("banner") and os.path.isfile(file) else None
        self.target_dir_file_list = [os.path.join(self.target_dir,banner) for banner in os.listdir(self.target_dir)]
        self.banner_list = list(filter(self.__banner_filter,self.target_dir_file_list))
        if self.banner_list == []:
            raise NoBannerFoundError("Hata Banner dosyaları bulunamadı !!! ")
        self.random_banner = os.path.join(self.target_dir,random.choice(self.banner_list))
    def __enter__(self):
        return self
    def __exit__(self,*args):
        pass
    def show(self):
        with IOUtils(file_name=self.random_banner,mode=Modes.MODE_READ_AS_BINARY) as banner_io_handler:
            data = banner_io_handler.read()
            line = data.decode("utf-8")
            if "%red%" in line:
                line = line.replace("%red%",Color.RED)
            if "%yellow%" in line:
                line = line.replace("%yellow%",Color.YELLOW)
            if "%blue%" in line:
                line = line.replace("%blue%",Color.BLUE)
            if "%green%" in line:
                line = line.replace("%green%",Color.GREEN)
            if "%cyan%" in line:
                line = line.replace("%cyan%",Color.CYAN)
            if "%pink%" in line:
                line = line.replace("%pink%",Color.PINK)
            if "%clr%" in line:
                line = line.replace("%clr%",Color.NORMAL)
            if "%bold%" in line:
                line = line.replace("%bold%",Color.BOLD)
            if "%tab%" in line:
                line = line.replace("%tab%","\t")
            if "%newline%" in line:
                line = line.replace("%newline%","\n")
            if "%break%" in line:
                line = line.replace("%break","\r")
            print(line)
    def __repr__(self) -> str:
        return "<%s banner=%s>" % (
            self.__class__.__name__,
            self.random_banner
        )