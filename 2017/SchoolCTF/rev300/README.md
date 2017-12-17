# Brute me all night long (REV 300) #
По заданию нам дан exe-шник. Попробуем его запусить. Открывается блокнот со следующим содержимым (нужно отключить перенос по словам):
```

              _____                    _____                    _____                    _____            _____                    _____          
             /\    \                  /\    \                  /\    \                  /\    \          /\    \                  /\    \         
            /::\    \                /::\    \                /::\    \                /::\____\        /::\    \                /::\    \        
           /::::\    \              /::::\    \               \:::\    \              /:::/    /       /::::\    \              /::::\    \       
          /::::::\    \            /::::::\    \               \:::\    \            /:::/    /       /::::::\    \            /::::::\    \      
         /:::/\:::\    \          /:::/\:::\    \               \:::\    \          /:::/    /       /:::/\:::\    \          /:::/\:::\    \     
        /:::/__\:::\    \        /:::/__\:::\    \               \:::\    \        /:::/    /       /:::/__\:::\    \        /:::/  \:::\    \    
       /::::\   \:::\    \      /::::\   \:::\    \              /::::\    \      /:::/    /       /::::\   \:::\    \      /:::/    \:::\    \   
      /::::::\   \:::\    \    /::::::\   \:::\    \    ____    /::::::\    \    /:::/    /       /::::::\   \:::\    \    /:::/    / \:::\    \  
     /:::/\:::\   \:::\    \  /:::/\:::\   \:::\    \  /\   \  /:::/\:::\    \  /:::/    /       /:::/\:::\   \:::\    \  /:::/    /   \:::\ ___\
    /:::/  \:::\   \:::\____\/:::/  \:::\   \:::\____\/::\   \/:::/  \:::\____\/:::/____/       /:::/__\:::\   \:::\____\/:::/____/     \:::|    |
    \::/    \:::\   \::/    /\::/    \:::\  /:::/    /\:::\  /:::/    \::/    /\:::\    \       \:::\   \:::\   \::/    /\:::\    \     /:::|____|
     \/____/ \:::\   \/____/  \/____/ \:::\/:::/    /  \:::\/:::/    / \/____/  \:::\    \       \:::\   \:::\   \/____/  \:::\    \   /:::/    /
              \:::\    \               \::::::/    /    \::::::/    /            \:::\    \       \:::\   \:::\    \       \:::\    \ /:::/    /  
               \:::\____\               \::::/    /      \::::/____/              \:::\    \       \:::\   \:::\____\       \:::\    /:::/    /   
                \::/    /               /:::/    /        \:::\    \               \:::\    \       \:::\   \::/    /        \:::\  /:::/    /    
                 \/____/               /:::/    /          \:::\    \               \:::\    \       \:::\   \/____/          \:::\/:::/    /     
                                      /:::/    /            \:::\    \               \:::\    \       \:::\    \               \::::::/    /      
                                     /:::/    /              \:::\____\               \:::\____\       \:::\____\               \::::/    /       
                                     \::/    /                \::/    /                \::/    /        \::/    /                \::/____/        
                                      \/____/                  \/____/                  \/____/          \/____/                  ~~              

```
Попробуем его проанализировать. Запускаем в IDA и видим, что это .Net-бинарь. Используем какой-нибудь .Net-декомпилятор (я использовал dotPeek) и получаем исходный код на языке C#. В ходе его анализа можно сделать следующие выводы:
1. Флаг формируется с помощью метода Success(), который принимает "кусочки" флага
2. Эти "кусочки" должны удовлетворять условиям, в основе которых лежат вычисления хэшей.
3. Есть догадка, что длины "кусочков" можно узнать из присваиваний их символов переменной StringBuilder
4. Зная примерный алфавит флага и длины "кусочков" мы можем реализовать брутфорс.

Первый кусок можно узнать, просто загуглив md5-хэш.

Для второго и других уже придется написать скрипт:
```python
from itertools import product
from string import printable
from hashlib import md5, sha256, sha384, sha512

def my_md5(text):
    return md5(text).digest().encode('hex')

def my_sha256(text):
    return sha256(text).digest().encode('hex')

def my_sha384(text):
    return sha384(text).digest().encode('hex')

def my_sha512(text):
    return sha512(text).digest().encode('hex')

HASH2 = "71036b1049de3e6627aa06ef7af933cc460996fdd7ffa9872bf4881e8d10a9c3153c8413ca4cd300a04e81e38d55d327"
HASH3 = "d0061dcf056a06713d5a757e0288d1b3"
HASH4 = "5056e21f6af2a289c9c3116c16bba55f"
HASH5 = "8e9b669109df89620b94f2387dc53206a82ddc71d658f8f7a2b3a9b417370d3e"
HASH6 = "566b014c957c19cb81aab7776eaf614701dadc084aa73fd002301bc7277091c4269ce1223d16746df4e803b85171733b89fa34bb1c61830799dee3611c38e006"
HASH7 = "c866a4f386df3da51a54c1f8434603eb"
HASH8 = "7f6e2c5beefd0fd0000c3a72db28b54d0819a93f5cc87a48507f79cdac37cfe0"

# text1 has been found by Google

def crack_hash2():
    N = 4
    for item in product(printable, repeat=N):
        if my_sha384(''.join(item)) == HASH2:
            print 'Text2 has been found: %s' % ''.join(item)
            return


def crack_hash3():
    N = 3
    for item in product(printable, repeat=N):
        text = "Ooooh so" + ''.join(item) + "salty"
        if my_md5(text) == HASH3:
            print 'Text3 has been found: %s' % ''.join(item)
            return

def crack_hash4():
    N = 1
    for item in product(printable, repeat=N):
        if my_md5("Stop trying to crack me god damnit!!!" + my_sha384(''.join(item))) == HASH4:
            print 'Text4 has been found: %s' % ''.join(item)
            return

def crack_hash5():
    N = 2
    for item in product(ALPHABET, repeat=N):
        if my_sha256(''.join(item) + "91") == HASH5:
            print 'Text5 has been found: %s' % ''.join(item)
            return

def crack_hash6():
    N = 3
    for item in product(printable, repeat=N):
        if my_sha512(''.join(item)) == HASH6:
            print 'Text6 has been found: %s' % ''.join(item)
            return            

def crack_hash7():
    N = 2
    for item in product(printable, repeat=N):
        if my_md5(my_sha384("Oh, i see you reading my source code! >:)") + ''.join(item)) == HASH7:
            print 'Text7 has been found: %s' % ''.join(item)
            return  

def crack_hash8():
    N = 2
    for item in product(printable, repeat=N):
        if my_sha256(my_sha384(my_sha512("FILL THE POWER OF SHA")) + ''.join(item)) == HASH8:
            print 'Text8 has been found: %s' % ''.join(item)
            return

```
Вызывая поочередно функции, мы узнаем "кусочки".
Теперь перепишем функцию Success(), чтобы она собрала нам флаг:
```python
def compose_flag():
    p1 = "541"
    p2 = "____"
    p3 = "md4"
    p4 = "l"
    p5 = "19"
    p6 = "757"
    p7 = "hh"
    p8 = "uJ"

    stringBuilder = list("Please stop it, noooooo")
    stringBuilder[0] = p8[1];
    stringBuilder[1] = p8[0];
    stringBuilder[2] = p6[1];
    stringBuilder[3] = p6[0];
    stringBuilder[4] = p2[3];
    stringBuilder[5] = p7[1];
    stringBuilder[6] = p1[1];
    stringBuilder[7] = p1[0];
    stringBuilder[8] = p7[0];
    stringBuilder[9] = p2[1];
    stringBuilder[10] = p1[2];
    stringBuilder[11] = p6[2];
    stringBuilder[12] = p2[2];
    stringBuilder[13] = p3[0];
    stringBuilder[14] = 'y';
    stringBuilder[15] = p2[0];
    stringBuilder[16] = p3[1];
    stringBuilder[17] = p3[2];
    stringBuilder[18] = 'r';
    stringBuilder[19] = p4[0];
    stringBuilder[20] = p5[0];
    stringBuilder[21] = 'n';
    stringBuilder[22] = p5[1];
    print "SchoolCTF{" + ''.join(stringBuilder) + "}";

compose_flag()
```
И вуа-ля, наш флаг:
```
SchoolCTF{Ju57_h45h_17_my_d4rl1n9}
```
