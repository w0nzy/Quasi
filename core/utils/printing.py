#!/usr/bin/env python3

# -*- encoding: utf-8 -*-
import random
from time import sleep as delay 
from typing import *
class Color:
    RED = "\033[1;31m"
    GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[1;34m"
    CYAN = "\033[1;96m"
    BOLD = "\033[1;37m"
    PINK = "\033[38;5;198m"
    NORMAL = "\033[1;0m"
arg_parser = lambda param: " ".join([str(x) for x in param])



def print_spinner(string,flush=False,particle="-\\|/"):
    max_str_len = len(string)
    max_particle_len = len(particle)
    string_counter = 0
    particle_counter = 0
    for _ in range(max_str_len):
        if particle_counter == max_particle_len:
            particle_counter = 0
        lowercase = string[0:string_counter].lower()
        uppercase = string[string_counter:string_counter+1].upper()
        aftercase = string[string_counter+1:max_str_len].lower()
        all_in_one = lowercase + uppercase + aftercase + " " + particle[particle_counter]
        print("\r",all_in_one,end="",flush=flush)
        particle_counter+=1
        string_counter+=1
        delay(0.1)
def print_loading(string,flush=False,delay_=0.1):
    dots = "........."
    dots_len = len(dots)
    for iter_ in range(len(string+1)):
        print("\r",string[0:iter_],flush=flush,end="")
        delay(delay_)

def print_failure(*msg: Any) -> Any:
    print(f"{Color.YELLOW}[{Color.RED}-{Color.YELLOW}]{Color.BOLD}{arg_parser(msg)}{Color.NORMAL}")


def print_succes(*msg: Any) -> Any:
    print(f"{Color.CYAN}[{Color.YELLOW}+{Color.CYAN}]{Color.BOLD}{arg_parser(msg)}{Color.NORMAL}")


def print_warning(*msg: Any) -> Any:
    print(f"{Color.CYAN}[{Color.YELLOW}!{Color.CYAN}]{Color.BOLD}{arg_parser(msg)}{Color.NORMAL}")


def print_status(*msg: Any) -> Any:
    print(f"\r{Color.CYAN}[{Color.YELLOW}*{Color.CYAN}]{Color.BOLD}{arg_parser(msg)}{Color.NORMAL}")

def print_pattern(*msg: Any,pattern = "-"):
    print(arg_parser(msg),"\n",pattern*len(arg_parser(msg)),sep="")

def print_slice(*msg: Any,delay_ = 0.1):
    data = arg_parser(msg)
    data_len = len(data)
    for iter_ in range(data_len+1):
        print("\r",data[0:iter_],end="")
        delay(delay_)
    print("\r\n")

if __name__ == "__main__":
    pass # do anything