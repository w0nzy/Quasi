#!/usr/bin/env python3

# -*- encoding: utf-8 -*-

import os
import sys
import socket
import struct
import platform
import subprocess
from core.utils.printing import Color
class SYSUtils:
    @classmethod
    def get_sys_arch(cls) -> int:
        return struct.calcsize("P") * 8 # if you have 64 sys arch this function will be return 64 else
    @classmethod
    def get_sys_version(cls) -> str:
        return f"{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"
    @classmethod
    def get_sys_os(cls) -> str:
        return os.name
    @classmethod
    def get_sys_win_info(cls) -> str:
        return platform.platform()
    @classmethod
    def get_sys_ps1(cls) -> str:
        hostname = socket.gethostname()
        user = os.environ["username"]
        ps1 = f"{Color.YELLOW}{hostname}{Color.RED}@{Color.BLUE}{user} >{Color.NORMAL} "
        return ps1
    @classmethod
    def get_sys_ps2(cls) -> str:
        ps2 = f"{Color.RED}th{Color.BOLD}0{Color.RED}rn1 >{Color.NORMAL} "
        return ps2