import logging
import os
from cp import cp_function
from mv import mv_function
from rm import rm_function
from cd import cd_function
from logging import getLogger

logger = getLogger(__name__)

history = []
cp_mv_rm = []
trash_history = []


def append_history(s, k: [list, int]) -> None:
    history.append(f'{k}. {' '.join(s)}')
    with open('.history', 'a', encoding='utf-8') as file:
        file.write(f'{' '.join(s)}\n')


def history_function(s: list) -> None:
    if s[1]:
        try:
            s[1] = int(s[1])
            if s[1] > len(history):
                for i in s:
                    print(i)
            elif s[1] >= 0:
                for i in range(-s[1], 0):
                    print(history[i])
            logger.info(f"{s}")
        except Exception:
            logger.error(f'history: unrecognized option')
            raise ValueError(f'history: unrecognized option')
    elif len(s) == 1:
        logger.info(f"{' '.join(s)}")
        for i in s:
            print(i)
    else:
        logger.error(f'history: unrecognized option')
        raise ValueError(f'history: unrecognized option')


def undo_function(last: list) -> None:
    if last[0] == 'cp':
        path1 = ''
        path2 = ''
        path3 = ''
        for i in last:
            if i != 'cp' and i != '-r':
                if len(path1) == 0:
                    path1 = i
                elif len(path2) == 0:
                    path2 = i
                elif len(path3) == 0:
                    path3 = i
        cd_function(['cd', path2])
        rm_function(['rm', path1])
        cd_function(['cd', path3])
        logger.info("undo for cp")
    elif last[0] == 'mv':
        path1 = ''
        path2 = ''
        path3 = ''
        for i in last:
            if i != 'mv':
                if len(path1) == 0:
                    path1 = i
                elif len(path2) == 0:
                    path2 = i
                elif len(path3) == 0:
                    path3 = i
        cd_function(['cd', path2])
        mv_function(['mv', path1, path3])
        cd_function(['cd', path3])
        logger.info("undo for mv")
    elif last[0] == 'rm':
        cp_function(['cp', os.path.join('.trash', f'{trash_history[-1]}'), last[-1]])
        trash_history.pop(-1)
        logger.info("undo for rm")
    else:
        logger.error(f'undo: unrecognized option')
        raise ValueError(f'undo: unrecognized option')
    cp_mv_rm.pop(-1)

