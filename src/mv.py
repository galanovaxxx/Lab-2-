import os
import shutil
import logging
from logging import getLogger

logger = getLogger(__name__)


def mv_function(user_input: list) -> None:
    """
        Функция для перемещения или переименования файлов и директорий
    """
    path1 = ''  # Исходный путь
    path2 = ''  # Целевой путь
    if len(user_input) != 3:
        logger.error(f'mv: unrecognized option "{' '.join(user_input[1:])}"')
        raise ValueError(f'mv: unrecognized option "{' '.join(user_input[1:])}"')
    """ Парсинг аргументов команды """
    for i in user_input:
        if i == 'mv':  # Пропускает название команды
            continue
        elif len(path1) == 0:  # Запоминает исходный путь
            path1 = i
        else:  # Запоминает целевой путь
            path2 = i
    # Проверяет права на чтение исходного файла и права доступа к целевому файлу
    if not os.access(path1, os.R_OK):
        logger.error(f'no permission to read the file: "{' '.join(user_input[1:])}"')
        raise PermissionError(f'no permission to read the file: {path1}')
    if not os.access(path2, os.R_OK) and os.path.isfile(path2):
        logger.error(f'no permission to read the file: "{' '.join(user_input[1:])}"')
        raise PermissionError(f'no permission to read the file: {path2}')
    if os.path.exists(path2) and os.path.exists(path1):
        # Обработка случая, когда целевой путь существует
        if os.path.isfile(path1) and os.path.isdir(path2):  # Перемещение файла в существующую директорию
            shutil.move(path1, path2)
            print(f'Файл {path1} перемещен в директорию {path2}')
            logger.info(f"{' '.join(user_input)}")
        elif os.path.isfile(path1) and os.path.isfile(path2):  # Перемещение файла с перезаписью существующего файла
            shutil.move(path1, path2)
            print(f'Файл {path1} удален и перезаписан в файл {path2}')
            logger.info(f"{' '.join(user_input)}")
        elif os.path.isdir(path1) and os.path.isdir(path2):  # Перемещение директории в существующую директорию
            shutil.move(path1, path2)
            print(f'Директория {path1} записана в директорию {path2}')
            logger.info(f"{' '.join(user_input)}")
    elif os.path.exists(path1):  # Обработка случая, когда целевой путь не существует
        if os.path.isfile(path1):  # Переименование файла
            shutil.move(path1, path2)
            print(f'Файл  {path1} переименован {path2}')
            logger.info(f"{' '.join(user_input)}")
        elif os.path.isdir(path1):  # Переименование директории
            shutil.move(path1, path2)
            print(f'Директория {path1} переименована {path2}')
            logger.info(f"{' '.join(user_input)}")
    else:  # Обработка ошибок, если файла не существует
        logger.info('no such file')
        raise FileNotFoundError('no such file')
