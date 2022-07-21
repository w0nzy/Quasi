
import builtins
import os
from core.utils.msgbox import *

from core.utils.printing import *

from core.utils.commons.randomize import random_string
class DataStore:
    pass
class Empty:
    def __init__(self,name: str):
        self.__name = name
    def __repr__(self):
        return "<class '%s'>" % (self.__class__.__name__)
class WrongDataType:
    def __init__(self,name: str,data,must_be=None):
        self.name = name
        self.data = data
        self.must_be = must_be
    def __repr__(self):
        return "<%s>" % (self.__class__.__name__)
class LineParser:
    def __init__(self,line = None,entry_intro = None,funcname = None):
        self.line = line
        self.line_split = line.split(" ")
        self.options = []
        self.options_names = {}
        self.option_atributes = {}
        self.f_name = funcname
    def help(self):
        print_pattern("LineParser v.1.0 Helper")
        intro = " ".join(self.options)
        outro = ""
        intro = self.f_name + " " + intro
        for o in self.options:
            help_doc = self.get_option_attributes(o,attribute="help")
            outro += f"{self.f_name} {Color.RED}{o}{Color.NORMAL} {help_doc}\n"
        print(intro,outro,sep="\n")
    def new_arguments(self,opt = None,name = None,is_required = False,default_value = None,typing = None,choices = [],help_doc = ""):
        if opt is None:
            raise ValueError("Hata opt boş bırakılamaz")
        if name is None:
            raise ValueError("Hata isimlendirme gereklidir")
        self.options.append(opt)
        self.options_names[opt]=name
        self.option_atributes[name] = {
            "is_required":is_required,
            "default_value":default_value,
            "type":typing,
            "choices":choices,
            "help":help_doc
            }
    def get_option_attributes(self,opt: str,attribute: str):
        name = self.options_names[opt]
        attr = self.option_atributes[name][attribute]
        return attr
    def get(self,opt: str) -> list:
        try:
            key = self.line_split.index(opt)
        except (IndexError,ValueError):
            key = Empty("key")
        try:
            value = self.line_split[self.line_split.index(opt)+1]
        except (IndexError,ValueError):
            value = Empty("value")
        return opt,value
    def set(self,name: str,value: Any):
        setattr(DataStore,name,value)
    def handler(self):
        skip = True
        for key in self.options:
            arg_key,arg_value = self.get(key)
            default_value = self.get_option_attributes(key,attribute="default_value")
            is_required = self.get_option_attributes(key,attribute="is_required")
            param_choices = self.get_option_attributes(key,attribute="choices")
            param_type = self.get_option_attributes(key,attribute="type")
            param_name = self.options_names[key]
            if not skip:
                self.help()
                break
            if isinstance(arg_key,Empty):
                if is_required and default_value is None:
                    skip = False
                    print_failure("Hata %s boş lütfen parametreyi doldurunuz" % (key))
                elif is_required and default_value:
                    self.set(param_name,default_value)
                elif not is_required:
                    pass
            elif isinstance(arg_value,Empty):
                if is_required and default_value is None:
                    skip = False
                    print_failure("Hata %s boş lütfen parametreyi doldurunuz" % (key))
                elif is_required and default_value:
                    self.set(param_name,default_value)
                elif not is_required:
                    pass
            else:
                param_type = self.get_option_attributes(key,attribute="type")
                if param_choices != [] and not arg_value in param_choices:
                    skip = False
                    print_failure("Hatalı seçim: %s sadece şunları seçebilirsin:" % (arg_value)," ".join(param_choices))
                if param_type:
                    if hasattr(builtins,str(param_type)):
                        try:
                            arg_value = getattr(builtins,str(param_type))(arg_value)
                        except:
                            return WrongDataType(
                                name=key,
                                data=arg_value,
                                must_be=str(param_type)
                            )
                self.set(param_name,arg_value)
        return skip
    def parse_args(self,dict = False):
        ret = self.handler()
        if ret:
            if isinstance(ret,WrongDataType):
                print_failure("Hatalı veri tipi %s %s için %s %s olmalıdır" % (ret.data,ret.name,ret.name,ret.must_be))
            else:
                return DataStore
        return False
def parse_list(liste: list,index = None):
    return liste[index]

def parse_header(dictionary: dict,index=None) -> Any:
    return parse_list(list(dictionary.keys()),index=index)

if __name__ == "__main__":
    pass