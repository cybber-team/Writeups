#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import random
import string
from functools import wraps
from base64 import b32decode as b32


FLAG = "XXX"


def emojified(f):
    @wraps(f)
    def decorated_function(arg, *args, **kwargs):
        arg = arg.replace('{', '👉🏼')
        arg = arg.replace('}', '👈🏼')
        arg = arg.replace('School', '🎓')
        arg = arg.replace('CTF', '🏴')
        return f(arg, *args, **kwargs)
    return decorated_function


def reversed(f):
    @wraps(f)
    def decorated_function(arg, *args, **kwargs):
        arg = arg[:-1]
        return f(arg, *args, **kwargs)
    return decorated_function


def splitted(sep='_'):
    def real_decorator(f):
        @wraps(f)
        def decorated_function(arg, *args, **kwargs):
            arg = arg.split(sep)
            return f(arg, *args, **kwargs)
        return decorated_function
    return real_decorator


def mixed(seed=0):
    def real_decorator(f):
        @wraps(f)
        def decorated_function(arg, *args, **kwargs):
            random.seed(seed)
            random.shuffle(arg)
            return f(arg, *args, **kwargs)
        return decorated_function
    return real_decorator


def joined(sep='_'):
    def real_decorator(f):
        @wraps(f)
        def decorated_function(arg, *args, **kwargs):
            arg = sep.join(arg)
            return f(arg, *args, **kwargs)
        return decorated_function
    return real_decorator


def verbosed(f):
    @wraps(f)
    def decorated_function(arg, *args, **kwargs):
        num2words = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five',
                     6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten'}
        for k, v in num2words.items():
            arg = arg.replace(str(k), v.upper())
        return f(arg, *args, **kwargs)
    return decorated_function


def caesared(key):
    def real_decorator(f):
        @wraps(f)
        def decorated_function(arg, *args, **kwargs):
            arg = ''.join(
                chr((ord(c) - 0x61 + key) % len(string.ascii_lowercase) + 0x61)
                if c in string.ascii_lowercase else c for c in arg
            )
            return f(arg, *args, **kwargs)
        return decorated_function
    return real_decorator


def shuffled(from_, to):
    def real_decorator(f):
        @splitted(from_)
        @mixed(len(from_))
        @joined(to)
        @wraps(f)
        def decorated_function(arg, *args, **kwargs):
            return f(arg, *args, **kwargs)
        return decorated_function
    return real_decorator


def kittyfied(mew):
    def real_decorator(f):
        @wraps(f)
        def decorated_function(arg, *args, **kwargs):
            arg=arg.replace(mew, '^_MeW_^')
            return f(arg, *args, **kwargs)
        return decorated_function
    return real_decorator


@emojified
@splitted()
@mixed(int.from_bytes(mixed.__name__.encode(), 'big'))
@joined()
@verbosed
@caesared(23)
@shuffled((297515763796).to_bytes(5, 'little').decode(), 'to')
@kittyfied(b32(b'N52G6===').decode())
@splitted('_^_')
@mixed(sys.version_info[0])
@joined('\\')
def get_flag(flag):
    return flag


if __name__ == "__main__":
    print_flag(FLAG)