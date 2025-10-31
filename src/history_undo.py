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
            logger.info(f"{' '.join(s)}")
        except Exception:
            logger.error(f'history: unrecognized option "{' '.join(s[1:])}"')
            raise ValueError(f'history: unrecognized option "{' '.join(s[1:])}"')
    elif len(s) == 1:
        logger.info(f"{' '.join(s)}")
        for i in s:
            print(i)
    else:
        logger.error(f'history: unrecognized option "{' '.join(s[1:])}"')
        raise ValueError(f'history: unrecognized option "{' '.join(s[1:])}"')


def undo_function(last: list) -> None:
    if last[0] == 'cp':
        current_dir = os.getcwd()
        cd_function(['cd', f'{last[-1]}'])
        rm_function(['rm', f'{last[1]}'])
        cd_function(['cd', f'{current_dir}'])
        logger.info("undo")
    elif last[0] == 'mv':
        mv_function([last[0], last[1], last[2]])
        logger.info("undo")
    elif last[0] == 'rm':
        cp_function(['cp', os.path.join('.trash', f'{trash_history[-1]}'), last[-1]])
        trash_history.pop(-1)
        logger.info("undo")
    else:
        logger.error(f'undo: unrecognized option')
        raise ValueError(f'undo: unrecognized option')
    history.pop(-1)
    cp_mv_rm.pop(-1)
