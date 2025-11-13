import os
import logging
import pdfplumber
import docx2txt
from logging import getLogger

logger = getLogger(__name__)


def cat_function(user_input: list) -> None:
    """
        Функция для вывода содержимого файла в консоль
    """
    if len(user_input) == 2:  # Проверка корректности количества аргументов
        path = user_input[1]
        if os.path.isfile(path):  # Проверяет, что указанный путь является файлом
            file_type = os.path.splitext(path)[1]  # Получение расширения файла
            if file_type == '.pdf':  # Обрабатывает PDF файлы с помощью библиотеки pdfplumber
                with pdfplumber.open(path) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            print(text, end='')
                    logger.info(f"{' '.join(user_input)}")
            elif file_type == '.doc' or file_type == '.docx':  # Обрабатывает DOC/DOCX файлы с помощью docx2txt
                text = docx2txt.process(path)
                print(text, end='')
                logger.info(f"{' '.join(user_input)}")
            else:
                try:  # Пытается открыть и вывести содержимое обычного текстового файла
                    with open(user_input[1], "r") as file:
                        lines = file.readlines()
                        for i in range(len(lines)):
                            print(lines[i], end='')
                        logger.info(f"{' '.join(user_input)}")
                except Exception:  # Обрабатывает ошибки декодирования файла
                    logger.error('failed to decode the file')
                    raise UnicodeError('failed to decode the file')
        else:  # Обрабатывает случай, когда файл не существует
            logger.error('no such file')
            raise FileNotFoundError('no such file')
    else:  # Обрабатывает случай неверного количества аргументов
        logger.error(f'cat: unrecognized option "{' '.join(user_input[1:])}"')
        raise ValueError(f'cat: unrecognized option "{' '.join(user_input[1:])}"')
