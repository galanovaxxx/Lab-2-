import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.grep import grep_function

class TestGrep:
    def test_grep_file_found(self):
        # Поиск совпадения в обычном файле
        file_content = "Hello world\nAnother line\n"
        with patch('os.path.isfile', return_value=True), \
             patch('os.access', return_value=True), \
             patch('builtins.open', mock_open(read_data=file_content)), \
             patch('builtins.print') as mock_print:
            grep_function(['grep', 'Hello', 'test.txt'])
            mock_print.assert_any_call('file: test.txt string: 1 fragment: Hello')

    def test_grep_file_not_found(self):
        # Файл не существует
        with patch('os.path.isfile', return_value=False), \
             patch('os.path.isdir', return_value=False):
            with pytest.raises(FileNotFoundError, match='no such file or directory'):
                grep_function(['grep', 'pattern', 'nofile.txt'])

    def test_grep_file_no_permission(self):
        # Нет прав на чтение файла
        with patch('os.path.isfile', return_value=True), \
             patch('os.access', return_value=False):
            with pytest.raises(PermissionError, match='no permission to read the dir: noaccess.txt'):
                grep_function(['grep', 'pattern', 'noaccess.txt'])

    def test_grep_dir_without_r(self):
        # Путь - директория, но без -r
        with patch('os.path.isfile', return_value=False), \
             patch('os.path.isdir', return_value=True):
            with pytest.raises(FileNotFoundError, match='no such file'):
                grep_function(['grep', 'pattern', 'somedir'])

    def test_grep_dir_with_r(self):
        # Рекурсивный поиск по директории
        files = ['a.txt', 'b.txt']
        walk_result = [('/root', [], files)]
        file_content = "pattern in this line\nno match\n"
        m = mock_open(read_data=file_content)
        with patch('os.path.isfile', return_value=False), \
             patch('os.path.isdir', return_value=True), \
             patch('os.walk', return_value=walk_result), \
             patch('builtins.open', m), \
             patch('builtins.print') as mock_print:
            grep_function(['grep', '-r', 'pattern', '/root'])
            mock_print.assert_any_call('file: a.txt string: 1 fragment: pattern in this line')
            mock_print.assert_any_call('file: b.txt string: 1 fragment: pattern in this line')

    def test_grep_dir_with_r_unicode_error(self):
        # Рекурсивный поиск, один из файлов вызывает UnicodeDecodeError
        files = ['a.txt', 'b.txt']
        walk_result = [('/root', [], files)]
        m = mock_open()
        m.side_effect = [mock_open(read_data="pattern\n").return_value,
                         UnicodeDecodeError("utf-8", b"", 0, 1, "reason")]
        with patch('os.path.isfile', return_value=False), \
             patch('os.path.isdir', return_value=True), \
             patch('os.walk', return_value=walk_result), \
             patch('builtins.open', m), \
             patch('builtins.print') as mock_print:
            grep_function(['grep', '-r', 'pattern', '/root'])
            mock_print.assert_any_call('file: a.txt string: 1 fragment: pattern')

    def test_grep_unrecognized_option(self):
        # Лишний аргумент
        with pytest.raises(ValueError, match='grep: unrecognized option'):
            grep_function(['grep', 'pattern', 'file.txt', 'extra'])

    def test_grep_ignore_case(self):
        # Поиск с -i (игнорировать регистр)
        file_content = "Hello world\nHELLO again\n"
        with patch('os.path.isfile', return_value=True), \
             patch('os.access', return_value=True), \
             patch('builtins.open', mock_open(read_data=file_content)), \
             patch('builtins.print') as mock_print:
            grep_function(['grep', '-i', 'hello', 'test.txt'])
            mock_print.assert_any_call('file: test.txt string: 1 fragment: Hello')
            mock_print.assert_any_call('file: test.txt string: 2 fragment: HELLO')