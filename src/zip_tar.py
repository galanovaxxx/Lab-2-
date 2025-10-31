import os
import logging
import zipfile
import tarfile
from logging import getLogger

logger = getLogger(__name__)


def zip_tar_function(user_input: list) -> None:
    """
    Функция для создания ZIP или TAR архивов
    """
    path1 = ''  # Исходный путь
    path2 = ''  # Путь к архиву
    if len(user_input) != 3:
        logger.error(f'zip: unrecognized option "{' '.join(user_input[1:])}"')
        raise ValueError(f'zip: unrecognized option "{' '.join(user_input[1:])}"')
    """ Парсинг путей из входных данных """
    for i in user_input:
        if i == 'zip' or i == 'tar':
            continue
        elif len(path1) == 0:
            path1 = i
        else:
            path2 = i
    if os.path.isdir(path1):  # Проверка существования директории
        if os.access(path1, os.R_OK) and os.access(path1, os.W_OK):  # Проверка прав доступа
            if user_input[0] == 'zip':
                """ Обработка создания ZIP архива """
                try:
                    """ Создает ZIP архив с содержимым директории """
                    with zipfile.ZipFile(path2, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for root, dirs, files in os.walk(path1):
                            for file in files:
                                file_path = os.path.join(root, file)
                                zipf.write(file_path, os.path.relpath(file_path, path1))
                            print(f'the file {path1} is archived as zip')
                            logger.info(f"{' '.join(user_input)}")
                except Exception:
                    """ Обработка ошибок при создании ZIP архива """
                    logger.error(f'zip: unrecognized option "{' '.join(user_input[1:])}"')
                    raise ValueError(f'zip: unrecognized option "{' '.join(user_input[1:])}"')
            elif user_input[0] == 'tar':
                """ Обработка создания TAR архива """
                try:
                    """ Создает TAR.GZ архив с содержимым директории """
                    with tarfile.open(path2, 'w:gz') as tar:
                        tar.add(path1, arcname=path2)
                        print(f"file {path1} is archived as tar")
                        logger.info(f"{' '.join(user_input)}")
                except Exception:
                    """ Обработка ошибок при создании TAR архива """
                    logger.error(f'tar: unrecognized option "{' '.join(user_input[1:])}"')
                    raise ValueError(f'tar: unrecognized option "{' '.join(user_input[1:])}"')
        else:  # Обрабатывает отсутствие прав доступа
            logger.error(f'no permission to read the dir "{' '.join(user_input[1:])}"')
            raise PermissionError(f'no permission to read the dir: {path1}')

    else:  # Обрабатывает случай несуществующей директории
        logger.error('no such directory')
        raise FileNotFoundError('no such directory')
