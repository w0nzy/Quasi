#!/usr/bin/env python3

# -*- encoding: utf-8 -*-

import json
import random
import base64
import socket

import requests
from struct import pack,unpack
from core.utils.printing import *
from core.utils.parser import parse_list
from ipaddress import IPv4Address,IPv6Address,ip_address

get_random_ip = lambda:f"{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

def get_public_ip() -> str:
    target_url = "https://api.ipify.org?format=json"
    try:
        response = requests.get(target_url).json()
        return response["ip"]
    except:
        return False # no internet connection or specific exception


def get_local_ip() -> str:
    try:
        hostname = socket.gethostname()
        local_ip_addr = hostname_to_ip(hostname)
        return local_ip_addr
    except Exception as local_ip_addr_err:
        return False # failure


def hostname_to_ip(hostname: str) -> str:
    """
    NOTE(NOT):Hostname string http veya ile https ile başlamamalıdr
    Wrong usage:https://www.google.com
    Correct usage:www.google.com
    """
    try:
        return socket.gethostbyname(hostname)
    except:
        return False # invalid hostname

def port_validator(port: int) -> bool:
    if port > 1 and port < 65535:
        return True
    return False

def ip_validator(ip: str) -> bool:
    """
    Bu fonksiyon IPv6 veya IPv4 farketmeksizin ip geçerliliğini kontrol etmektedir
    ip_validator("::1") True
    ip_validator("::fkreckepokcpeokc") False
    ip_validator("127.0.0.1")
    ip_validatr("pojc.şek.12912") False
    """
    try:
        ip_address(ip) # BUG FIXED
        return True
    except: # invalid ip address IPv4 or IPv6
        return False


def is_valid_ipv4(ip: str) -> bool:
    """
    Bu fonksiyon ipv6 geçerliliğini kontrol etmek içindir kullanım şekli şöyledir
    is_valid_ipv6("127.0.0.1") True
    is_valid_ipv6("255.999.12312.313") False
    """
    try:
        IPv4Address(ip)
        return True
    except: # invalid ip address IPv4
        return False


def is_valid_ipv6(ip: str) -> bool:
    """
    Bu fonksiyon ipv6 geçerliliğini kontrol etmek içindir kullanım şekli şöyledir
    is_valid_ipv6("::1") True
    is_valid_ipv6("::1eckepofckepock") False
    """
    try:
        IPv6Address(ip)
        return True
    except: # invalid ip address IPv6
        return False


class IpToFamily:
    """
    bu class ip adresine göre soket oluştururken family seçmek içindir
    """
    def __new__(self,ip: str) -> int:
        try:
            is_valid_ipv4(ip)
            return socket.AF_INET
        except:
            pass
        try:
            is_valid_ipv6(ip)
            return socket.AF_INET6
        except:
            return False # invalid ip addr


def pack_msg(data: bytes,format=">I") -> bytes:
    """
    return pack(format,len(data)) + data
    Bu fonksiyon soket ile veri göndermeden önce önek uzunluğu eklemek içindir kullanım şu şekli şöyledir
    pack_msg(data: bytes,format='>I')
    format default value is '>I'
    it's function return bytes
    """
    return pack(format,len(data)) + data


def unpack_msg(data: bytes,format=">I") -> int:
    """
    return unpack(format,data)[0]
    Bu fonksiyon soket ile gönderilen paketlenmiş olan verinin önek uzunluğunu ortaya çıkarmak içindir kullanım şekli şöyledir
    unpack_msg(data: bytes,format='>I')
    format default value is '>I'
    it's function return int(integer)
    """
    return unpack(format,data)[0]
def JSONPacker(header,params = {}) -> dict:
    ret = {}
    def _encoder(data: AnyStr) -> str:
        encode = lambda param:"encoded" + base64.b85encode(param).decode("utf-8")
        if isinstance(data,bytes):
            return encode(data)
        return data
    for k,v in params.items():
        ret[k]=_encoder(v)
    return json.dumps({header:ret})
def JSONUnpacker(data: str,only_header = False) -> dict:
    ret = {}
    def _decoder(data: str) -> bytes:
        decode = lambda data:base64.b85decode(data[7:].encode("utf-8"))
        if isinstance(data,str):
            if data.startswith("encoded"):
                return decode(data)
        return data
    unpacked_json_data = json.loads(data)
    header = parse_list(list(unpacked_json_data.keys()),index=0)
    main_dictionary = unpacked_json_data[header]
    if only_header:
        return header
    for key,value in main_dictionary.items():
        ret[key]=_decoder(value)
    return {header:ret}

if __name__ == "__main__":
    pass # do anything
