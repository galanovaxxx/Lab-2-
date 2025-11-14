import os
import shutil
import logging
from logging import getLogger

logger = getLogger(__name__)


def cp_function(user_input: list) -> bool:
    """
        Функция для копирования файлов и директорий
    """
    r_mode = False  # Флаг рекурсивного копирования
    path1 = ''  # Исходный путь
    path2 = ''  # Целевой путь
    if len(user_input) > 4 or (len(user_input) == 4 and '-r' not in user_input) or len(user_input) < 3:
        logger.error(f'cp: unrecognized option "{' '.join(user_input[1:])}"')
        raise ValueError(f'cp: unrecognized option "{' '.join(user_input[1:])}"')
    """ Парсинг аргументов команды """
    for i in user_input:
        if i == 'cp':
            continue
        elif i == '-r':
            r_mode = True
        elif len(path1) == 0:
            path1 = i
        else:
            path2 = i
    # Проверка существования исходного пути
    if not os.path.exists(path1):
        logger.error('no such file')
        raise FileNotFoundError('no such file')
    # Копирование директории
    if os.path.isdir(path1):
        if not r_mode:
            logger.error('cp: omitting directory (use -r flag)')
            raise IsADirectoryError('cp: omitting directory (use -r flag)')
        shutil.copytree(path1, path2)
        print(f'Рекурсивное копирование {path1} в {path2}.')
        logger.info(f"{' '.join(user_input)}")
    # Копирование файла
    else:
        # Если path2 — существующая директория, копируем файл внутрь
        if os.path.isdir(path2):
            shutil.copy(path1, path2)
        else:
            shutil.copy(path1, path2)
        print(f'Файл {path1} скопирован в {path2}.')
        logger.info(f"{' '.join(user_input)}")
    return True
