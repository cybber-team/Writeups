# Incorrect Pointer (REV 100) #
По заданию нам дан elf-файл. Запустим его:
```bash
adam@DESKTOP-QF2AHRP:/mnt/d/Workspace/CTF/2017/school/rev100$ ./incorrect_pointer
h♂ull!►<xv<~<
```
Откроем файл в IDA. И воспользуемся декомпилятором Hex-Rays.

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  const char **v4; // [sp+0h] [bp-18h]@1
  int v5; // [sp+Ch] [bp-Ch]@1

  v5 = argc;
  v4 = argv;
  hs_init(&v5, &v4, envp);
  hs_add_root(_stginit_Task);
  decrypt(&not_flag);
  puts(&flag);
  hs_exit(&flag);
  return 0;
}
```
К счастью, файл оказался не stripped, и мы можем по названию функции предположить, что делает программма. Например, в коде есть функция decrypt(), которая, скорей всего, выполняет дешифрования. Мы замечаем, что ей передается адрес на переменную not_flag, но затем мы выводим текст уже переменной flag. Попробуем сделать так, чтобы функции decrypt() передавался адрес на переменную flag. Для этого TAB'ом переключимся на ассемблер и пропатчим строку
```assembly
BF A0 31 7A 00                          mov     edi, offset not_flag
```
на
```assembly
BF 60 31 7A 00                          mov     edi, offset flag
```
Запустим теперь наш пропатченный elf:
```
SchoolCTF{d0_u_m@k3_M1$T@ke$_As_1_d0}
```
