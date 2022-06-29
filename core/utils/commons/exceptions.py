#!/usr/bin/env python3

# -*- encoding: utf-8 -*-
import socket
class MainExceptionClass(Exception):
    pass
class InvalidAESKey(MainExceptionClass):
    pass
class InvalidMode(MainExceptionClass):
    pass
class BindError(MainExceptionClass):
    pass
class InvalidModeError(MainExceptionClass):
    pass
class WriteError(MainExceptionClass):
    pass
class ReadError(MainExceptionClass):
    pass
class FileCreationError(MainExceptionClass):
    pass
class ItsNotFileError(MainExceptionClass):
    pass
class SocketServerError(Exception):
    pass
class ClientSendError(OSError,Exception):
    pass
class ClientRecvError(OSError,Exception):
    pass
class CDError(OSError):
    pass
class NoBannerFoundError(Exception):
    pass