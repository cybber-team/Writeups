import string

FLAG = "MeW_^sto?????_v0r_qexq/ONEpto\MeW_^op\iiv_????????@^_MeW_^qefkh"

def decaesared(ct, key):
    pt = ''.join(
                chr((ord(c) - 0x61 - key) % len(string.ascii_lowercase) + 0x61)
                if c in string.ascii_lowercase else c for c in ct
            )
    return pt
    
if __name__ == '__main__':
    for i in range(10, 101):
        print("{0} [{1}]".format(decaesared(FLAG, i), i))