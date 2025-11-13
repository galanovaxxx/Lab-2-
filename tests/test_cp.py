import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from src.cp import cp_function

class TestCp:

    def setup_method(self):
        self.cp = cp_function
        self.cwd = Path("/test/cwd")
        self.env = {}

    def test_cp_overwrite_file(self):
        """cp file1 file2: перезаписывает содержимое file1 в file2"""
        user_input = ['cp', 'file1', 'file2']
        with patch('os.path.exists', side_effect=lambda p: True if p in ['file1', 'file2'] else False), \
                patch('os.path.isfile', return_value=True), \
                patch('shutil.copy') as mock_copy, \
                patch('builtins.print') as mock_print, \
                patch('src.cp.logger') as mock_logger:
            result = cp_function(user_input)
            mock_copy.assert_called_once_with('file1', 'file2')
            mock_print.assert_called_once_with('Файл file1 скопирован в file2.')
            mock_logger.info.assert_called_once_with('cp file1 file2')
            assert result is True

    def test_cp_file_to_existing_directory(self):
        # file существует и является файлом, dir существует
        with patch('os.path.exists', side_effect=lambda p: p in ['file', 'dir']), \
                patch('os.path.isfile', side_effect=lambda p: p == 'file'), \
                patch('shutil.copy') as mock_copy, \
                patch('builtins.print') as mock_print:
            result = cp_function(['cp', 'file', 'dir'])
            mock_copy.assert_called_once_with('file', 'dir')
            mock_print.assert_called_once_with('Файл file скопирован в dir.')
            assert result is True

    def test_cp_file_to_new_file(self):
        """cp file1 file2: file1 существует, file2 не существует, происходит копирование"""
        with patch('os.path.exists', side_effect=lambda path: path in ['file1', 'file2']), \
                patch('os.path.isfile', return_value=True), \
                patch('shutil.copy') as mock_copy, \
                patch('builtins.print') as mock_print, \
                patch('src.cp.logger') as mock_logger:
            result = cp_function(['cp', 'file1', 'file2'])
            mock_copy.assert_called_once_with('file1', 'file2')
            mock_print.assert_called_once_with('Файл file1 скопирован в file2.')
            mock_logger.info.assert_called()
            assert result is True

    def test_cp_file_not_exist_but_dir_exists(self):
        """cp file dir: file не существует, dir существует"""
        with patch('os.path.exists', side_effect=lambda p: p == 'dir'), \
                patch('os.path.isfile', return_value=False), \
                patch('os.path.isdir', return_value=True):
            with pytest.raises(FileNotFoundError, match='no such file'):
                cp_function(['cp', 'file', 'dir'])

    def test_cp_recursive_directory_copy(self):
        with patch('os.path.exists', side_effect=lambda p: p == 'dir1'), \
                patch('os.path.isfile', return_value=False), \
                patch('shutil.copytree') as mock_copytree, \
                patch('builtins.print') as mock_print, \
                patch('logging.getLogger') as mock_logger:
            result = cp_function(['cp', '-r', 'dir1', 'dir2'])
            mock_copytree.assert_called_once_with('dir1', 'dir2')
            mock_print.assert_called_once_with('Рекурсивное копирование dir1 в dir2.')
            assert result is True

    def test_cp_too_many_args_error(self):
        with pytest.raises(ValueError, match=r'cp: unrecognized option "-r dir1 dir2 dir3"'):
            cp_function(['cp', '-r', 'dir1', 'dir2', 'dir3'])