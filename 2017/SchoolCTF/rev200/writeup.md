# Properly Decorated (REV 200) #
Заранее скажу, что я не уверен в оптимальности моего решения.
По заданию нам даны скрипт, который кодирует изначальный флаг, и результат скрипта:
```
 "MeW_^sto?👈🏼_v0r_qexq/ONEpto\MeW_^op\iiv_🎓🏴👉🏼@^_MeW_^qefkh"
 ```
В этом задании главное понять, что декораторы вызываются в прямом порядке, т.е. первоначально запускается декоратор @emojified.
Для того, чтобы лучше понять, что делает скрипт, закоментируем декортары. Попробуем FLAG присваивать разные значения, например SchoolCTF{english_or_1337}, и одновременно с этим будем поочередно декораторы раскомментировать. Благодаря этим действиям и анализу исходного кода, мы сумели вывести алгоритм кодирования флага:

Алгоритм кодирования флага
1. Заменяем слова School, CTF, { и } на эмоджи-символы
2. Разбиваем строку по разделителю "_"
3. Перемешиваем с помощью random.shuffle()
4. Обратно сцепляем, разделяя "_"
5. Заменяем цифры на их буквенное представление
6. Шифруем цезарем все буквы нижнего регистра
7. Разбиваем строку по разделителю "THREE"
8. Перемешиваем с помощью random.shuffle()
9. Обратно сцепляем, разделяя "to"
10. Заменяем "oto" на "^_MeW_^"
11. Разделяем строку по разделителю "_^_"
12. Перемешиваем с помощью random.shuffle()
13. Обратно сцепляем, разделяя ""\"

Просто взять и построить обратный алгоритм, который возьмет и просто вернет нам изначальный флаг, не получится из-за функций random.shuffle(), которые перемешивают список. Очевидно, что нужно использовать технику брутфорса.

Ключ для цезаря узнаем путем скармливания функции decaesared(text, key) закодированного флага и ключа от 10 до 100:


Вывело 91 вариант, но среди них есть строка с различимыми словами:
MhW_^vwr?????_y0u_that/ONEswr\MhW_^rs\lly_????????@^_MhW_^think [23]

Теперь возьмемся писать скрипт по получению флага. Напишем алгоритм декодирования:
1. Превращаем эмоджи в слова
2. Разделяем строку по разделителю "\"
3. Перемешиваем
4. Обратно сцепляем, разделяя "_^_"
5. Заменяем "^_MeW_^" на "oto"
6. Разделяем строку по разделителю "to"
7. Перемешиваем
8. Обратно сцепляем, разделяя "THREE"
9. Дешифруем цезарем
10. Заменяем буквенное представление на сами цифры
11. Разделяем строку по разделителю "_"
12. Перемешиваем
13. Обратно сцепляем, разделяя "_"

Начнем с реализации пп. 1-4:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps
import string
from itertools import permutations


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

    for i in first_set:
        print(i)

if __name__ == '__main__':
    main()
```
Вывод:
```
MeW_^sto?}_v0r_qexq/ONEpto_otoop_^_iiv_SCHOOLCTF{@otoqefkh
MeW_^sto?}_v0r_qexq/ONEpto_^_iiv_SCHOOLCTF{@otoqefkh_otoop
MeW_^op_otosto?}_v0r_qexq/ONEpto_^_iiv_SCHOOLCTF{@otoqefkh
MeW_^op_^_iiv_SCHOOLCTF{@otoqefkh_otosto?}_v0r_qexq/ONEpto
iiv_SCHOOLCTF{@otoqefkh_otosto?}_v0r_qexq/ONEpto_otoop
iiv_SCHOOLCTF{@otoqefkh_otoop_otosto?}_v0r_qexq/ONEpto
```
Здесь можно заметить, что строки 1-4 нам не подходят, потому что в дальнейшем нам неудастся избавиться от "MeW_^" в начале этих строк, так как вряд ли флаг содержит эти символы. Тем самым мы сократим время брутфорса. В следующем листинге представлены отсев этих четырех строк и реализация пп. 5-9. Для того, чтобы дешифровка Цезаря не тронула слово School, изменим функцию demojified: сделаем так, чтобы была замена не на School, а на SCHOOL.


```python
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
```        

Вывод:
```
lly_SCHOOLCTF{@r3think_r3v3?}_y0u_that/1s3_r3rs
lly_SCHOOLCTF{@r3think_r3v3?}_y0u_that/1s3rs3_r
lly_SCHOOLCTF{@r3think_r3v3_r3?}_y0u_that/1s3rs
.............
```

Наконец, реализация остальных пунктов и проверка флага путем редактирования исходного скрипта-кодера и импорта его функции

```python
from reverseme import get_flag

# .........

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
```

В искодном скрипте нужно заменить
```python
def print_flag(flag):
    print(flag)
```
на
```python
def get_flag(flag):
    return flag
```
И вуа-ля:
```
FLAG: SchoolCTF{@r3_y0u_r3lly_think_that/1s_r3v3rs3?}
```
