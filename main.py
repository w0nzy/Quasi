from core.base import Bootloader
from core.utils.printing import print_failure
try:
    with Bootloader() as bootloader:
        bootloader.boot()
except Exception as loader_err:
    print_failure("Hata boot edilirken bir hata oluştu",loader_err)