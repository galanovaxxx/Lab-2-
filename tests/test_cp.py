import pytest
from unittest.mock import patch
from src.cp import cp_function


class TestCp:
    def setup_method(self):
        self.cp = cp_function

    def test_cp_file_to_file(self):
        """cp копирует файл в файл"""
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=False), \
             patch('shutil.copy') as mock_copy, \
             patch('builtins.print') as mock_print:
            result = self.cp(['cp', 'file1.txt', 'file2.txt'])
            mock_copy.assert_called_once_with('file1.txt', 'file2.txt')
            assert result is True
            mock_print.assert_called_once_with('Файл file1.txt скопирован в file2.txt.')

    def test_cp_file_to_directory(self):
        """cp копирует файл в директорию"""
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', side_effect=[False, True]), \
             patch('shutil.copy') as mock_copy, \
             patch('builtins.print'):
            result = self.cp(['cp', 'file.txt', 'dir'])
            mock_copy.assert_called_once_with('file.txt', 'dir')
            assert result is True

    def test_cp_directory_without_r_flag(self):
        """cp без -r для директории вызывает IsADirectoryError"""
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True):
            with pytest.raises(IsADirectoryError, match='cp: omitting directory'):
                self.cp(['cp', 'dir1', 'dir2'])

    def test_cp_directory_with_r_flag(self):
        """cp -r копирует директорию рекурсивно"""
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('shutil.copytree') as mock_copytree, \
             patch('builtins.print') as mock_print:
            result = self.cp(['cp', '-r', 'dir1', 'dir2'])
            mock_copytree.assert_called_once_with('dir1', 'dir2')
            assert result is True
            mock_print.assert_called_once_with('Рекурсивное копирование dir1 в dir2.')

    def test_cp_no_arguments(self):
        """cp без достаточного количества аргументов вызывает ValueError"""
        with pytest.raises(ValueError, match='cp: unrecognized option'):
            self.cp(['cp'])

    def test_cp_one_argument(self):
        """cp с одним аргументом вызывает ValueError"""
        with pytest.raises(ValueError, match='cp: unrecognized option'):
            self.cp(['cp', 'file.txt'])

    def test_cp_nonexistent_source(self):
        """cp несуществующего источника вызывает FileNotFoundError"""
        with patch('os.path.exists', return_value=False):
            with pytest.raises(FileNotFoundError, match='no such file'):
                self.cp(['cp', 'no_file.txt', 'file2.txt'])

    def test_cp_too_many_arguments(self):
        """cp с лишними аргументами вызывает ValueError"""
        with pytest.raises(ValueError, match='cp: unrecognized option'):
            self.cp(['cp', 'a', 'b', 'c', 'd'])