import os
import logging
import zipfile
import tarfile

from logging import getLogger

from src.my_errors import DirectoryNotFoundError

logger = getLogger(__name__)


def unzip_untar_function(user_input):
    """
        Функция для распаковки ZIP и TAR архивов
    """
    path = ''  # Путь к архиву
    if len(user_input) != 2:  # Проверка корректности количества аргументов
        logger.error(f'unzip: unrecognized option "{' '.join(user_input[1:])}"')
        raise ValueError(f'unzip: unrecognized option "{' '.join(user_input[1:])}"')
    """ Парсинг аргументов команды """
    for i in user_input:
        if i == 'unzip' or i == 'untar':  # Пропускает название команды
            continue
        else:  # Запоминает путь к архиву
            path = i
    if os.path.isfile(path):  # Проверка существования файла
        if os.access(path, os.R_OK) and os.access(path, os.W_OK):  # Проверка прав доступа
            if user_input[0] == 'unzip':
                """ Обработка распаковки ZIP архива """
                try:
                    # Распаковывает ZIP архив в текущую директорию
                    with zipfile.ZipFile(path, 'r') as zip_ref:
                        zip_ref.extractall()
                        print(f'the file {path} in unarchived')
                        logger.info(f"{' '.join(user_input)}")
                except Exception:
                    # Обработка ошибок при распаковке ZIP
                    logger.error(f'unzip: unrecognized option "{' '.join(user_input[1:])}"')
                    raise ValueError(f'unzip: unrecognized option "{' '.join(user_input[1:])}"')
            if user_input[0] == 'untar':
                """ Обработка распаковки TAR архива """
                try:
                    # Распаковывает TAR архив в текущую директорию
                    with tarfile.open(path, 'r') as tar:
                        tar.extractall()
                        print(f'the file {path} is unarchived')
                        logger.info(f"{' '.join(user_input)}")
                except Exception:
                    # Обработка ошибок при распаковке TAR
                    logger.error(f'untar: unrecognized option "{' '.join(user_input[1:])}"')
                    raise ValueError(f'untar: unrecognized option "{' '.join(user_input[1:])}"')
        else:
            # Обрабатывает отсутствие прав доступа
            logger.error(f'no permission to read the dir "{' '.join(user_input[1:])}"')
            raise PermissionError(f'no permission to read the dir: {path}')
    else:
        # Обрабатывает случай несуществующего файла
        logger.error('no such directory')
        raise DirectoryNotFoundError('no such directory')
