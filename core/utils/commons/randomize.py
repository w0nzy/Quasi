#!/usr/bin/env python3

# -*- encoding: utf-8 -*-
import os
import random
import string
import hashlib

shuffled_string = string.ascii_lowercase + string.ascii_uppercase + string.digits

random_string = lambda pass_len: "".join(random.sample(shuffled_string,pass_len)) # random_string(pass_len: int) -> str
random_byte_as_32bit = lambda:os.urandom(32) # it's returning 32 byte random chars for key generating crypto and other
#random_byte_as_24bit = lambda:os.urandom(24) # it's returning 24 byte random chars for key generating crypto and other disabled !!
random_byte_as_16bit = lambda:os.urandom(16) # it's returning 16 byte random chars for key generating crypto and other

def random_byte_generator(key_size=16,beautify=False):
    """
    Eğer ki daha güzel bi çıktı çıkmasını istiyorsan beautify=True yap
    with beautify:ecb91f9f5fb80f54b4bd8fb3c407b76519bc5fdeefbf50e3b511795485714f5a
    without beautify:\xcf\xbc\x1e\xff*\xf4\xf5\x87T\xa9[\xaa\xdf\xd38\x02\xeco\xfc\x96\xb2\x8e\x8c,\xd2'(\x8e\x9eY\x86Y
    """
    # Hesaplama şöyle: 1 byte == 8 bit
    # 32 * 8 = 256
    # 16 * 8 = 128
    key_sizes = {
        16:random_byte_as_16bit, # AES-128
        32:random_byte_as_32bit  # AES-256
    }
    key_sizes_to_sha = {
        16:hashlib.shake_128,
        32:hashlib.shake_256
    }
    try:
        random_bytes = key_sizes[key_size]()
    except:
        return False # invalid key size 
    return key_sizes_to_sha[key_size](random_bytes).hexdigest(key_size) if beautify else random_bytes

if __name__ == "__main__":
    pass # do anything