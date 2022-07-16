import os
import quasi
import subprocess
from argparse import ArgumentParser
from core.utils import get_framework_path
from core.utils.printing import print_status,print_failure,print_succes


def sign_exe(exe_path: str,pfx_file = None,pfx_password = None):
    def _signer(signtool_path = None,pfx_file_path = None,pfx_password = None,exe_path = None):
        cmd_args = "%s sign /f %s /p %s /td SHA256 %s" % (
            signtool_path,
            pfx_file_path,
            pfx_password,
            exe_path
        )
        cmd_args = cmd_args.split(" ")
        try:
            subprocess.call(cmd_args)
        except Exception as e:
            raise Exception("%s Dosyası şu sebebpten imzalanamadı " % (exe_path)) from e
    framework_path = get_framework_path()
    signtool_path = os.path.join(framework_path,"binaries","signtool.exe")
    pfx_file_path = os.path.join(framework_path,"data","certs","sign.pfx")
    if not os.path.exists(exe_path):
        print_failure("%s dosyası mevcut değil" % (exe_path))
    elif not os.path.exists(signtool_path):
        print_failure("%s bulunamadı !" % (signtool_path))
    elif not os.path.exists(pfx_file_path):
        print_failure("%s Dosyası olmadan imzalanamaz !" % (pfx_file_path))
    else:
        print_status("İMZALANIYOR: %s" % (exe_path))
        try:
            res = _signer(
                signtool_path=signtool_path,
                pfx_file_path=pfx_file_path,
                pfx_password=pfx_password,
                exe_path=exe_path
            )
        except Exception as e:
            print_failure("%s Dosyası şu sebebpten imzalanamadı %s" % (exe_path,e))
parser = ArgumentParser(epilog="Payload Signer(via signtool.exe)")
parser.add_argument("-e","--exe-path",dest="_exe_path",required=True,metavar = "payload.exe",help="İmzalanacak olan exe dosyası")
parser.add_argument("-f","--pfx-file",dest="_pfx_file_path",required=True,metavar = "Signature.pfx",help="İmza dosyası")
parser.add_argument("-p","--pfx-password",dest="_pfx_pass",required=True,metavar = "PassWord1234",help = "İmza Dosyasının anahtarı")
parser = parser.parse_args()
sign_exe(
    exe_path=parser._exe_path,
    pfx_file=parser._pfx_file_path,
    pfx_password=parser._pfx_pass

)