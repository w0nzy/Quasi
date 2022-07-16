import os
import struct
import marshal
import hashlib

from core.utils.commons.randomize import random_string
from core.utils.commons.io_utils import Modes
from core.utils.commons.crypto import AESCipher
from core.utils.commons.io_utils import IOUtils

from core.utils.printing import print_status
from core.utils.printing import print_succes
class Qpkg:
    """
    Quasi Package Hiearchy
    0mtime
    1 key,
    2 iv
    data:
        path_or_file_name:
            file_data
    """

    def __init__(self,target_file = None):
        self.target_file = target_file
        self.walk_mode = False
        self.pack_is_enable = False
        self.unpack_is_enable = False
        self.data = None
        self.cipher = AESCipher()
        if not os.path.exists(self.target_file):
            raise FileExistsError("Hata %s dosyası eksik" % (self.target_file))
        if os.path.isdir(self.target_file):
            self.walk_mode = True
            dirname,basename = os.path.split(self.target_file)
            if not dirname == "":
                self.path_seperator = basename
                self.pack_is_enable = True
        elif os.path.isfile(self.target_file):
            try:
                marshal.dumps(IOUtils(file_name=self.target_file,mode=Modes.MODE_READ_AS_BINARY).read())
                self.pack_is_enable = True
            except:
                self.unpack_is_enable = True

    def qpkg_path_joiner(self,path: str) -> str:
        l = path.split(self.path_seperator)[1]
        return self.path_seperator + os.sep + l
    def path_explorer(self) -> str:
        for root,_,files in os.walk(self.target_file):
            for f in files:
                x = os.path.join(root,f)
                yield x
    def key_encode(self,data:str or int) -> bytes:
        if isinstance(data,str):
            return data.encode()
        elif isinstance(data,int):
            return struct.pack("Q",data)
        elif isinstance(data,bytes):
            return data
    def pack(self,save=False):
        print_status("Paketleniyor: %s" % (self.target_file))
        pack_to_data = {}
        if self.pack_is_enable:
            first_pack = (os.path.getmtime(self.target_file),
                self.cipher.get_private_key_as_byte,
                self.cipher.get_iv_as_byte
            )
            for num,data in enumerate(first_pack):
                pack_to_data[self.key_encode(num)]=data
            if not self.walk_mode:
                with IOUtils(file_name=self.target_file,mode=Modes.MODE_READ_AS_BINARY) as fd:
                    data = self.cipher.encrypt(fd.read())
                    pack_to_data[self.key_encode(os.path.basename(self.target_file))]=data
                pack_to_data = marshal.dumps(pack_to_data)
            elif self.walk_mode:
                for p in self.path_explorer():
                    if hasattr(self,"path_seperator"):
                        xpath = self.qpkg_path_joiner(p)
                        encrypted = self.cipher.encrypt(IOUtils(file_name=p,mode=Modes.MODE_READ_AS_BINARY).read())
                        pack_to_data[self.key_encode(xpath)]=encrypted
                    else:
                        encrypted = self.cipher.encrypt(IOUtils(file_name=p,mode=Modes.MODE_READ_AS_BINARY).read())
                        pack_to_data[self.key_encode(p)]=encrypted
                pack_to_data = marshal.dumps(pack_to_data)
        return pack_to_data if not save else IOUtils(file_name=os.path.basename(self.target_file) + "_" + random_string(5) + ".Qpkg",mode=Modes.MODE_WRITE_AS_BINARY).write(pack_to_data)

