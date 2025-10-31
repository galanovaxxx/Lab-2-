import os
import logging
import re
from logging import getLogger

logger = getLogger(__name__)


def grep_function(user_input: list) -> None:
    """
    Функция для поиска текста по шаблону в файлах
    """
    pattern = ''  # Шаблон поиска
    path = ''  # Путь к файлу или директории
    r_mode = False  # Флаг рекурсивного поиска
    i_mode = False  # Флаг игнорирования регистра
    # Парсинг параметров команды
    for i in user_input:
        if i == 'grep':
            """Пропускаем название команды"""
            continue
        elif i == '-r':
            """Устанавливаем режим рекурсивного поиска"""
            r_mode = True
        elif i == '-i':
            """Устанавливаем режим игнорирования регистра"""
            i_mode = True
        elif len(pattern) == 0:
            """Запоминаем шаблон поиска"""
            pattern = i
        elif len(path) == 0:
            """Запоминаем путь"""
            path = i
        else:
            """Обрабатываем лишние параметры"""
            logger.error(f'grep: unrecognized option "{" ".join(user_input)}"')
            raise ValueError(f'grep: unrecognized option "{" ".join(user_input)}"')

    """ Обработка поиска в файле """
    if os.path.isfile(path):
        if os.access(path, os.R_OK):  # Проверяем права доступа
            # Настройка регулярного выражения
            if i_mode:  # Не учитываем регистр
                flags = re.IGNORECASE
                regex = re.compile(pattern, flags)
            else:
                regex = re.compile(pattern)
            # Поиск в файле
            with open(path, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    matches = regex.finditer(line)
                    for match in matches:
                        print(f"file: {path} string: {line_num} fragment: {match.group()}")
            logger.info(f"{' '.join(user_input)}")
        else:
            """Обрабатываем отсутствие прав доступа"""
            logger.error(f'no permission to read the dir "{path}"')
            raise PermissionError(f'no permission to read the dir: {path}')

    elif os.path.isdir(path):  # Обработка рекурсивного поиска
        if r_mode:
            try:  # Настройка регулярного выражения
                if i_mode:  # Не учитываем регистр
                    flags = re.IGNORECASE
                    regex = re.compile(pattern, flags)
                else:
                    regex = re.compile(pattern)
                # Рекурсивный поиск
                for root, dirs, files in os.walk(path):
                    for file_name in files:
                        file_path = os.path.join(root, file_name)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as file:
                                for line_num, line in enumerate(file, 1):
                                    line = line.rstrip('\n\r')
                                    if regex.search(line):
                                        print(f"file: {file_name} string: {line_num} fragment: {line}")
                        except UnicodeDecodeError:
                            continue
                logger.info(f"{' '.join(user_input)}")
            except Exception:  # Обрабатываем ошибки при поиске
                logger.error(f'incorrect pattern: "{pattern}"')
                raise PermissionError(f'incorrect pattern: {pattern}')
        else:  # Обрабатываем отсутствие флага рекурсии
            logger.error('no such file')
            raise FileNotFoundError('no such file')
    else:  # Обрабатываем несуществующий путь
        logger.error('no such file or directory')
        raise FileNotFoundError('no such file or directory')
