# Quasi
<img src="https://static.vecteezy.com/ti/vecteur-libre/p1/2058317-retro-futuriste-annees-80-fond-gratuit-vectoriel.jpg" width="200" height="200" />











# Basit Kullanım
```bash
C:\Users\user\Quasi\python main.py
```
# Merhaba Saygı Değer Quası kullanıcısı! <img src="https://raw.githubusercontent.com/MartinHeinz/MartinHeinz/master/wave.gif" width="30px">
   * Desteklenen özellikler:
   * Keylogger
   * Download
   * Upload
   * Msgbox
   * Shell Executing
   * Directory listing
   * pwd 
   * cd
# Geçerli İşletim Sistemi
   * Windows
# Desteklenen İşletim Sistemi Versiyonu
   * Windows 10 >=
# Desteklenen Python Versiyonu
   * Python 3.7.x >= 
# Desteklenen İşletim Sistemi Mimarisi
   * X64
# Gereksinimler
* Crypto
* cx_Freeze
* requests
* pynput
* socket
* readline
* marshal
* base64
* hashlib
* os
* threading
* time
* struct
* sys
* platform
* binascii
* ctypes
* subprocess
* builtins
* random
* json
* ipaddress
* enum
* io

# Networking Modülü
  * Ağ için basic seviye modüldür ip kontrolü vb. ip adresi işlemleri içindir
  * kullanım
  ```python
  # import etmek için
  >>> from core.utils.commons.networking import *
  >>> ip_validator("127.0.0.1")
  >>> True
```

# LineParser Modülü
   * Amaç program içersinde ki komut üzerinden parametreleri işlemek
   * Kullanım
   ```python
   from core.utils.parser import LineParser
   # LineParser(line=None,funcname=None)
   def do_open(self,line: str):
      parser = LineParser(line=line,funcname="open")
      parser.new_arguments("-f",
      name="file",
      is_required=True,
      typing="str",
      choices=["main.ico","test.py"],
      help="Dosya okumak için"
      )
      p = parser.parse_args()
      # not eğer ki kullanıcı eksik bişey girerse örneğin zorunlu girilmesi gerek veya yanlış bi seçim veya hiç bir parametre girmezse False döndürür
      if p not False:
          print("Dosya: %s" % (p.file))
   ```
   ```sh
   python parser_test.py
   > open
   open -f
   open -f Dosya okumak için
   > open -f AnotherFile
   [-] Hatalı seçim: AnotherFile sadece şunları seçebilirsin:main.ico test.py
   > open -f main.ico
   Dosya: main.ico
   ```
# Şuan bu kadarlık ilerde proje tam bittiğinde bütün hepsi barındıracak şekilde yazılacaktır


   
   
