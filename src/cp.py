import os
import shutil
import logging
from logging import getLogger

logger = getLogger(__name__)


def cp_function(user_input: list) -> None:
    """
        Функция для копирования файлов и директорий
    """
    r_mode = False  # Флаг рекурсивного копирования
    path1 = ''  # Исходный путь
    path2 = ''  # Целевой путь
    if len(user_input) > 4 or (len(user_input) == 4 and '-r' not in user_input) or len(user_input) < 3:
        # Проверка корректности количества аргументов
        logger.error(f'cp: unrecognized option "{' '.join(user_input[1:])}"')
        raise ValueError(f'cp: unrecognized option "{' '.join(user_input[1:])}"')
    """ Парсинг аргументов команды """
    for i in user_input:
        if i == 'cp':  # Пропускает название команды
            continue
        elif i == '-r':  # Устанавливает режим рекурсивного копирования
            r_mode = True
        elif len(path1) == 0:  # Запоминает исходный путь
            path1 = i
        else:  # Запоминает целевой путь
            path2 = i
    if os.path.exists(path1):  # Проверка существования исходного файла/директории
        if r_mode == False and os.path.isfile(path1) and os.path.exists(path2):
            """ Обработка простого копирования файла """
            shutil.copy(path1, path2)
            print(f'Файл {path1} скопирован в {path2}.')
            logger.info(f"{' '.join(user_input)}")
        elif r_mode == True:
            """ Обработка рекурсивного копирования """
            shutil.copytree(path1, path2)
            print(f'Рекурсивное копирование {path1} в {path2}.')
            logger.info(f"{' '.join(user_input)}")
    else:  # Обрабатывает случай несуществующего исходного файла
        logger.error('no such file')
        raise FileNotFoundError('no such file')
