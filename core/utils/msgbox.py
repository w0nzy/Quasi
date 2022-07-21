#!/usr/bin/env python3

# -*- encoding: utf-8 -*-

import ctypes

class Dialogs:
    DIA_OK = 0
    DIA_OK_CANCEL = 1
    DIA_ABORT_RETRY_IGNORE = 2
    DIA_YES_NO_CANCEL = 3
    DIA_YES_NO = 4
    DIA_RETRY_CANCEL = 5

class Icon:
    ICO_STOP = 16
    ICO_QUESTION = 32
    ICO_EXCLAMATION = 48
    ICO_INFO = 64

class Response:
    RESP_OK = 1
    RESP_CANCEL = 2
    RESP_ABORT = 3
    RESP_RETRY = 4
    RESP_IGNORE = 5
    RESP_YES = 6
    RESP_NO = 7

class PreDialogs:
    DIA_OK_WITH_STOP_ICO = Dialogs.DIA_OK | Icon.ICO_STOP
    DIA_OK_WITH_QUESTION_ICO = Dialogs.DIA_OK | Icon.ICO_QUESTION
    DIA_OK_WITH_EXCLAMATION_ICO = Dialogs.DIA_OK | Icon.ICO_EXCLAMATION
    DIA_OK_WITH_INFO_ICO = Dialogs.DIA_OK | Icon.ICO_INFO
    
    DIA_OK_CANCEL_WITH_STOP_ICO = Dialogs.DIA_OK_CANCEL | Icon.ICO_STOP
    DIA_OK_CANCEL_WITH_QUESTION_ICO = Dialogs.DIA_OK_CANCEL | Icon.ICO_QUESTION
    DIA_OK_CANCEL_WITH_EXCLAMATION_ICO = Dialogs.DIA_OK_CANCEL | Icon.ICO_EXCLAMATION
    DIA_OK_CANCEL_WITH_INFO_ICO = Dialogs.DIA_OK_CANCEL | Icon.ICO_INFO
				   
    DIA_ABORT_RETRY_IGNORE_WITH_STOP_ICO = Dialogs.DIA_ABORT_RETRY_IGNORE | Icon.ICO_STOP
    DIA_ABORT_RETRY_IGNORE_WITH_QUESTION_ICO = Dialogs.DIA_ABORT_RETRY_IGNORE | Icon.ICO_QUESTION
    DIA_ABORT_RETRY_IGNORE_WITH_EXCLAMATION_ICO = Dialogs.DIA_ABORT_RETRY_IGNORE | Icon.ICO_EXCLAMATION
    DIA_ABORT_RETRY_IGNORE_WITH_INFO_ICO =  Dialogs.DIA_ABORT_RETRY_IGNORE | Icon.ICO_INFO

    DIA_YES_NO_CANCEL_WITH_STOP_ICO = Dialogs.DIA_YES_NO_CANCEL | Icon.ICO_STOP
    DIA_YES_NO_CANCEL_WITH_QUESTION_ICO = Dialogs.DIA_YES_NO_CANCEL | Icon.ICO_QUESTION
    DIA_YES_NO_CANCEL_WITH_EXCLAMATION_ICO = Dialogs.DIA_YES_NO_CANCEL | Icon.ICO_EXCLAMATION
    DIA_YES_NO_CANCEL_WITH_INFO_ICO = Dialogs.DIA_YES_NO_CANCEL | Icon.ICO_INFO
    
    DIA_YES_NO_WITH_STOP_ICO = Dialogs.DIA_YES_NO | Icon.ICO_STOP
    DIA_YES_NO_WITH_QUESTION_ICO = Dialogs.DIA_YES_NO | Icon.ICO_QUESTION
    DIA_YES_NO_WITH_EXCLAMATION_ICO = Dialogs.DIA_YES_NO  | Icon.ICO_EXCLAMATION
    DIA_YES_NO_WITH_INFO_ICO =  Dialogs.DIA_YES_NO | Icon.ICO_INFO
					        
    DIA_RETRY_CANCEL_WITH_INFO_ICO = Dialogs.DIA_RETRY_CANCEL | Icon.ICO_STOP
    DIA_RETRY_CANCEL_WITH_QUESTION_ICO = Dialogs.DIA_RETRY_CANCEL | Icon.ICO_QUESTION
    DIA_RETRY_CANCEL_WITH_EXCLAMATION_ICO = Dialogs.DIA_RETRY_CANCEL | Icon.ICO_EXCLAMATION
    DIA_RETRY_CANCEL_WITH_STOP_ICO = Dialogs.DIA_RETRY_CANCEL | Icon.ICO_STOP

dialogs = list(filter(lambda param:param if not param.startswith("_") else None,dir(PreDialogs)))
					    
class MessageBox:

    def __new__(
        self, 
        box = None,
        title = None,
        text = None
    ) -> None:
        self.msgbox_dll_handler = ctypes.windll.user32.MessageBoxW
        self.title = title
        self.text = text
        self.box = box
        return self.msgbox_dll_handler(None,self.text,self.title,self.box)

if __name__ == "__main__": pass
