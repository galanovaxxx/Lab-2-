import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from datetime import datetime
from src.ls import ls_function
from src.my_errors import DirectoryNotFoundError


class TestLs:

    def setup_method(self):
        """Настройка перед каждым тестом - создаем экземпляр команды и тестовые данные"""
        self.ls = ls_function
        self.cwd = Path("/test/cwd")
        self.env = {}

    def test_ls_current_directory(self):
        """Тест: ls без аргументов должен показать содержимое текущей директории"""
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = True
        mock_target.is_dir.return_value = True

        mock_file1 = Mock(spec=Path)
        mock_file1.name = "file1.txt"
        mock_file2 = Mock(spec=Path)
        mock_file2.name = "file2.txt"

        mock_target.iterdir.return_value = [mock_file2, mock_file1]

        with patch('os.path.isdir', return_value=True), patch('os.listdir', return_value=['file1.txt', 'file2.txt']), \
                patch('builtins.print') as mock_print:
            result = self.ls(['ls'])

            assert result is None

            calls = [call[0][0] for call in mock_print.call_args_list]
            assert calls == ["file1.txt", "file2.txt", '_____']

    def test_ls_with_path_argument(self):
        """Тест: ls с указанием пути должен показать содержимое указанной директории"""
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = True
        mock_target.is_file.return_value = False

        mock_file = Mock(spec=Path)
        mock_file.name = "test.py"
        mock_target.iterdir.return_value = [mock_file]

        # Проверяем что to_path вызывается с переданным аргументом
        with patch('os.path.isdir', return_value=True), patch('os.listdir', return_value=['test.py']) as mock_to_path, \
                patch('builtins.print') as mock_print:
            result = self.ls(['ls', "srс"])

            # Убеждаемся что путь обрабатывается правильно
            mock_to_path.assert_called_once_with("srс")
            assert result is None
            calls = [call[0][0] for call in mock_print.call_args_list]
            assert calls == ["test.py", '_____']

    def test_ls_long_format(self):
        """Тест: ls -l должен показать детальную информацию о файлах"""
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = True
        mock_target.is_file.return_value = False

        mock_file = Mock(spec=Path)
        mock_file.name = "test.py"

        # Мокируем stat() чтобы format_long получил нужные данные
        # Не мокируем саму format_long - хотим протестировать её реальную работу!
        mock_stat = Mock()
        mock_stat.st_mode = 0o100644  # Обычный файл с правами rw-r--r--
        mock_stat.st_uid = 0
        mock_stat.st_size = 1024  # Размер 1024 байта
        mock_stat.st_mtime = datetime(2023, 1, 1, 12, 0).timestamp()  # Время модификации
        mock_file.stat.return_value = mock_stat

        mock_target.iterdir.return_value = [mock_file]

        with patch('os.stat', return_value=mock_stat), patch('os.path.isdir', return_value=True), patch('os.listdir', return_value=['test.py']) as mock_to_path, \
                patch('builtins.print') as mock_print:
            result = self.ls(['ls',"-l"])

            assert result is None
            # Проверяем что format_long создал правильную строку
            expected = "-rw-r--r-- 0 1024  2023-01-01 12:00:00 test.py"
            calls = [call[0][0] for call in mock_print.call_args_list]
            assert ' '.join([str(i) for i in calls]) == expected + ' _____'

    def test_ls_file(self):
        """ls с файлом выводит имя файла"""
        with patch('os.path.isdir', return_value=False), \
                patch('os.path.isfile', return_value=True), \
                patch('builtins.print') as mock_print:
            ls_function(['ls', 'file.txt'])
            mock_print.assert_called_once_with('file.txt')

    def test_ls_no_such_directory(self):
        """ls с несуществующей директорией вызывает DirectoryNotFoundError"""
        with patch('os.path.isdir', return_value=False), \
                patch('os.path.isfile', return_value=False):
            with pytest.raises(DirectoryNotFoundError, match='no such directory'):
                ls_function(['ls', 'no_dir'])

    def test_ls_unrecognized_option(self):
        """ls с лишними аргументами вызывает ValueError"""
        with pytest.raises(ValueError, match='ls: unrecognized option'):
            ls_function(['ls', '-l', 'dir', 'extra'])

    def test_ls_empty_directory(self):
        """ls для пустой директории"""
        with patch('os.path.isdir', return_value=True), \
                patch('os.listdir', return_value=[]), \
                patch('builtins.print') as mock_print:
            ls_function(['ls'])
            # Только '_____'
            mock_print.assert_called_once_with('_____')
