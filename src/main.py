import os
import logging
import shutil

from ls import ls_function
from cp import cp_function
from mv import mv_function
from rm import rm_function
from cd import cd_function
from cat import cat_function
from zip_tar import zip_tar_function
from unzip_untar import unzip_untar_function
from grep import grep_function
from history_undo import undo_function, history_function, append_history, cp_mv_rm, trash_history
from tokenization import tokenization_function

"""Настройка логгирования. Устанавливает параметры записи логов в файл с заданным форматом и кодировкой"""
logging.basicConfig(level=logging.DEBUG, filemode='w', filename='shell.log', encoding='utf-8',
                    format="%(asctime)s %(levelname)s %(message)s")

with open('.history', 'w', encoding='utf-8') as f:
    pass
shutil.rmtree('.trash')
os.mkdir('.trash')


def main() -> None:
    l = 0
    while True:
        s = input(os.getcwd() + ' ')
        s = tokenization_function(s)
        l += 1
        if s:
            try:
                if s[0] == 'ls':
                    append_history(s, l)
                    ls_function(s)
                if s[0] == 'cd':
                    append_history(s, l)
                    cd_function(s)
                if s[0] == 'cat':
                    append_history(s, l)
                    cat_function(s)
                if s[0] == 'cp':
                    if cp_function(s):
                        cp_mv_rm.append(s)
                    append_history(s, l)
                    cp_function(s)
                if s[0] == 'mv':
                    if mv_function(s):
                        cp_mv_rm.append(s[:-1] + [os.getcwd()])
                    append_history(s, l)
                    mv_function(s)
                if s[0] == 'rm':
                    append_history(s, l)
                    temp = rm_function(s)
                    if temp:
                        s = s + [os.getcwd()]
                        cp_mv_rm.append(s)
                        trash_history.append(s[1])
                if s[0] == 'zip' or s[0] == 'tar':
                    append_history(s, l)
                    zip_tar_function(s)
                if s[0] == 'unzip' or s[0] == 'untar':
                    append_history(s, l)
                    unzip_untar_function(s)
                if s[0] == 'history' and len(s) <= 2:
                    append_history(s, l)
                    history_function(s)
                if s[0] == 'undo' and len(s) == 1:
                    append_history(s, l)
                    undo_function(cp_mv_rm[-1])
                if s[0] == 'grep':
                    append_history(s, l)
                    grep_function(s)
            except FileNotFoundError:
                print('no such file or directory')
            except ValueError:
                print('unrecognized option')
            except PermissionError:
                print('no permission to read the file')
            except UnicodeDecodeError:
                print('failed to decode the file')

main()
