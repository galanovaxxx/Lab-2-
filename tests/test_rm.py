import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from src.rm import rm_function

class TestRm:
    def setup_method(self):
        self.rm = rm_function
        self.cwd = Path("/test/cwd")
        self.env = {}

    def test_rm_file_confirmed(self):
        # Мокаем os.path.exists, os.path.isfile, os.remove, shutil.copy, input, print
        with patch('os.path.exists', return_value=True), \
                patch('os.path.isfile', return_value=True), \
                patch('shutil.copy') as mock_copy, \
                patch('os.remove') as mock_remove, \
                patch('builtins.input', return_value='y'), \
                patch('builtins.print') as mock_print:
            result = rm_function(['rm', 'file.txt'])
            mock_copy.assert_called_once_with('file.txt', '.trash')
            mock_remove.assert_called_once_with('file.txt')
            mock_print.assert_any_call("Вы действительно хотите удалить файл?")
            mock_print.assert_any_call("Файл file.txt удален.")
            assert result is True

    def test_rm_recursive_directory(self):
        with patch('os.path.exists', return_value=True), \
                patch('os.path.isdir', return_value=True), \
                patch('builtins.input', return_value='y'), \
                patch('shutil.rmtree') as mock_rmtree, \
                patch('builtins.print') as mock_print:
            result = rm_function(['rm', '-r', 'dir'])
            mock_rmtree.assert_called_once_with('dir')
            mock_print.assert_any_call("Вы действительно хотите удалить каталог?")
            mock_print.assert_any_call("Каталог dir удален со всем содержимым.")
            assert result is True

    def test_rm_file_not_exist(self):
        with patch('os.path.exists', return_value=False), \
                patch('os.path.isfile', return_value=False):
            with pytest.raises(FileNotFoundError, match='no such file'):
                rm_function(['rm', 'file.txt'])

    def test_rm_permission_error(self):
        # Мокаем os.path.exists и os.path.isfile, чтобы файл считался существующим
        with patch('os.path.exists', return_value=True), \
                patch('os.path.isfile', return_value=True), \
                patch('builtins.input', return_value='y'), \
                patch('shutil.copy'), \
                patch('os.remove', side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError, match="Permission denied"):
                rm_function(['rm', 'file'])