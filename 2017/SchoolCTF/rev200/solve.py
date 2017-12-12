#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps
import string
from itertools import permutations
from reverseme import get_flag

FLAG = "MeW_^sto?👈🏼_v0r_qexq/ONEpto\MeW_^op\iiv_🎓🏴👉🏼@^_MeW_^qefkh"

def demojified(text):
    text = text.replace('👉🏼', '{')
    text = text.replace('👈🏼', '}')
    text = text.replace('🎓', 'SCHOOL')
    text = text.replace('🏴', 'CTF')
    return text

def decaesared(ct, key=23):
    pt = ''.join(
                chr((ord(c) - 0x61 - key) % len(string.ascii_lowercase) + 0x61)
                if c in string.ascii_lowercase else c for c in ct
            )
    return pt

def deverbosed(text):
    num2words = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five',
                 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten'}
    for k, v in num2words.items():
        text = text.replace(v.upper(), str(k))
    return text
        
        
def main():
    first_split = demojified(FLAG).split('\\')
    first_set = ['_^_'.join(x) for x in permutations(first_split, len(first_split))]
    first_set = [x.replace('^_MeW_^', 'oto') for x in first_set]
    first_set = first_set[-2:]  # без ^_MeW_^' только 2 варианта
    
    second_split = [x.split('to') for x in first_set]
    second_set = []
    for second_spl_i in second_split:
        second_set += ['THREE'.join(x) for x in permutations(second_spl_i, len(second_spl_i))]
    
    second_set = [deverbosed(decaesared(x)) for x in second_set]
    
    for i in second_set:
        print(i)
    
    third_split = [x.split('_') for x in second_set]
    third_set = []
    for third_spl_i in third_split:
        third_set += ['_'.join(x).replace('SCHOOL', 'School') for x in permutations(third_spl_i, len(third_spl_i)) if x[0].startswith('SCHOOL') and x[-1].endswith('}')]
    
    for i in third_set:
        if get_flag(i) == FLAG:
            print("FLAG: " + i)
            return
    
if __name__ == '__main__':
    main()