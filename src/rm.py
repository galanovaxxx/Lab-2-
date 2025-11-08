import os
import shutil
from pathlib import Path
from logging import getLogger

logger = getLogger(__name__)


def rm_function(user_input: list) -> bool:
    """
        Функция для удаления файлов и директорий
    """
    r_mode = False  # Флаг рекурсивного удаления
    path = ''  # Путь к удаляемому объекту
    """ Парсинг аргументов команды """
    for i in user_input:
        if i == 'rm' and r_mode == False:  # Пропускает название команды
            continue
        elif i == '-r':  # Устанавливает режим рекурсивного удаления
            r_mode = True
        elif len(path) == 0:  # Запоминает путь к удаляемому объекту
            path = i
        else:  # Обрабатывает ошибку, если есть лишние аргументы
            logger.error(f'rm: unrecognized option "{' '.join(user_input[1:])}"')
            raise ValueError(f'rm: unrecognized option "{' '.join(user_input[1:])}"')
    target = Path(path).resolve()
    if target == target.anchor: # Проверка на корневой каталог
        logger.error('can`t remove root directory')
        raise ValueError(f"Запрещено удалять корневой каталог: {target} (anchor: {target.anchor})")
    cwd_parent = Path.cwd().parent.resolve()
    if target == cwd_parent: # Проверка на родительский каталог (..)
        logger.error('can`t remove parent directory')
        raise ValueError(f"Запрещено удалять родительский каталог: {target}")
    if target.is_relative_to(cwd_parent) and target != cwd_parent: # Доп проверка: не позволяем удалять каталоги выше CWD
        logger.error('can`t remove parent directory')
        raise ValueError(f"Запрещено удалять каталоги выше текущего рабочего каталога: {target}")
    if r_mode == False:
        """ Обработка простого удаления файла """
        if os.path.exists(path) and os.path.isfile(path):  # Проверяет существование и тип файла
            print("Вы действительно хотите удалить файл?")
            answer = input("Введите y или n: ")
            if answer == "y":  # Обработка подтверждения удаления
                if os.path.isfile(path):
                    shutil.copy(path, '.trash')
                elif os.path.isdir(path):
                    shutil.copytree(path, '.trash')
                os.remove(path)
                print(f"Файл {path} удален.")
                logger.info(f"{' '.join(user_input)}")
            elif answer == "n":  # Обработка отмены удаления
                print(f"Файл {path} не удален.")
                logger.info(f"file {path} was not deleted")
            else:
                print("Ответ не соответствует y/n")
                logger.info(f"file {path} was not deleted")
        else:  # Обработка случая несуществующего файла
            logger.error('no such file')
            raise FileNotFoundError('no such file')
    else:
        """ Обработка рекурсивного удаления директории """
        if os.path.exists(path) and os.path.isdir(path):  # Проверяет существование и тип директории
            print("Вы действительно хотите удалить каталог?")
            answer = input("Введите y или n: ")
            if answer == "y":  # Обработка подтверждения удаления директории
                shutil.rmtree(path)
                print(f"Каталог {path} удален со всем содержимым.")
                logger.info(f"{' '.join(user_input)}")
            elif answer == "n":  # Обработка отмены удаления директории
                print(f"Каталог {path} не удален.")
                logger.info(f"directory {path} was not deleted")
            else:  # Обработка неверного ответа
                print("Ответ не соответствует yes/no")
                logger.info(f"directory {path} was not deleted")
        else:  # Обработка случая несуществующей директории
            logger.error('no such directory')
            raise FileNotFoundError('no such directory')
    return True
