import os
from logging import getLogger

logger = getLogger(__name__)

def cd_function(user_input: list) -> None:
    """
        Функция для изменения текущей рабочей директории
    """
    path = ''
    """ Парсинг аргументов команды """
    for i in user_input:
        if i == 'cd':  # Пропускает название команды
            continue
        elif len(path) == 0:  # Запоминает указанный путь
            path = i
        else:  # Проверяет, что команда содержит ровно два аргумента
            logger.error(f'cd: unrecognized option "{' '.join(user_input[1:])}"')
            raise ValueError(f'cd: unrecognized option "{' '.join(user_input[1:])}"')
    if path[0] == '~':  # Обрабатывает путь, начинающийся с символа ~
        # Переходит в домашний каталог и обрабатывает оставшийся путь
        os.chdir(os.path.expanduser("~"))
        path = path[2:]
        logger.info(f"{' '.join(user_input)}")
    if len(path) > 0 and os.path.exists(path):  # Проверяет существование директории и выполняет переход
        os.chdir(path)
        if path[0] != '~':
            logger.info(f"{' '.join(user_input)}")
    elif len(path) > 0:  # Обрабатывает случай несуществующей директории
        logger.error('no such directory')
        raise FileNotFoundError('no such directory')
