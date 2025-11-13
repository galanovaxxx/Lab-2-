import os
import stat
from datetime import datetime
import logging
from logging import getLogger

from src.my_errors import DirectoryNotFoundError

logger = getLogger(__name__)


def ls_function(user_input: list) -> None:
    """
        Функция для обработки команды ls
    """
    l_mode = False  # Флаг подробного вывода информации (-l)
    path = ''  # Путь к директории для просмотра
    """ Парсинг аргументов команды """
    for i in user_input:
        if i == 'ls' and user_input.count('ls') == 1:  # Пропускает название команды
            continue
        elif i == '-l' and l_mode == False:  # Устанавливает режим подробного вывода
            l_mode = True
        elif len(path) == 0:  # Запоминает путь, если он указан
            path = i
        else:  # Обрабатывает случай лишних аргументов
            logger.error(f'''ls: unrecognized option "{' '.join(user_input[1:])}"''')
            raise ValueError(f'''ls: unrecognized option "{' '.join(user_input[1:])}"''')
    if os.path.isdir(path) or len(path) == 0:  # Проверка существования директории
        if path != '':
            files = os.listdir(path)  # Получает список файлов по указанному пути
        else:
            files = os.listdir()  # Получает список файлов текущей директории
        if files and l_mode == False:  # Простой вывод списка файлов
            for i in range(len(files)):
                print(files[i])
            print('_____')
            logger.info(f"{' '.join(user_input)}")
        else:  # Подробный вывод информации о файлах
            for i in range(len(files)):
                if len(path) != 0:
                    file_info = os.stat(path + '/' + files[i])
                else:
                    file_info = os.stat(files[i])
                print(stat.filemode(file_info.st_mode), end=' ')
                print(file_info.st_uid, end=' ')
                print(str(file_info.st_size) + ' ' * (5 - len(str(file_info.st_size))), end=' ')
                print(datetime.fromtimestamp(file_info.st_mtime), end= ' ')
                print(files[i])
            print('_____')
            logger.info(f"{' '.join(user_input)}")
    elif os.path.isfile(path):
        print(path)
        logger.info(f"{' '.join(user_input)}")
    else:  # Обрабатывает случай несуществующей директории
        logger.error('no such directory')
        raise DirectoryNotFoundError('no such directory')
