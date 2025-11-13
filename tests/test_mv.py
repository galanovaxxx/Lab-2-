import pytest
from unittest.mock import patch
from src.mv import mv_function

class TestMv:
    def test_mv_file_to_dir(self):
        """Перемещение файла в директорию"""
        with patch('os.access', return_value=True), \
             patch('os.path.exists', side_effect=lambda p: p in ['file.txt', 'dir']), \
             patch('os.path.isfile', side_effect=lambda p: p == 'file.txt'), \
             patch('os.path.isdir', side_effect=lambda p: p == 'dir'), \
             patch('shutil.move') as mock_move, \
             patch('builtins.print') as mock_print, \
             patch('src.mv.logger') as mock_logger:
            result = mv_function(['mv', 'file.txt', 'dir'])
            mock_move.assert_called_once_with('file.txt', 'dir')
            mock_print.assert_called_once_with('Файл file.txt перемещен в директорию dir')
            mock_logger.info.assert_called()
            assert result is True

    def test_mv_file_to_file(self):
        """Удаление файла с перезаписью"""
        with patch('os.access', return_value=True), \
             patch('os.path.exists', side_effect=lambda p: p in ['file1.txt', 'file2.txt']), \
             patch('os.path.isfile', side_effect=lambda p: p in ['file1.txt', 'file2.txt']), \
             patch('os.path.isdir', return_value=False), \
             patch('shutil.move') as mock_move, \
             patch('builtins.print') as mock_print, \
             patch('src.mv.logger') as mock_logger:
            result = mv_function(['mv', 'file1.txt', 'file2.txt'])
            mock_move.assert_called_once_with('file1.txt', 'file2.txt')
            mock_print.assert_called_once_with('Файл file1.txt удален и перезаписан в файл file2.txt')
            mock_logger.info.assert_called()
            assert result is True

    def test_mv_dir_to_dir(self):
        """Перемещение директории в директорию"""
        with patch('os.access', return_value=True), \
             patch('os.path.exists', side_effect=lambda p: p in ['dir1', 'dir2']), \
             patch('os.path.isfile', return_value=False), \
             patch('os.path.isdir', side_effect=lambda p: p in ['dir1', 'dir2']), \
             patch('shutil.move') as mock_move, \
             patch('builtins.print') as mock_print, \
             patch('src.mv.logger') as mock_logger:
            result = mv_function(['mv', 'dir1', 'dir2'])
            mock_move.assert_called_once_with('dir1', 'dir2')
            mock_print.assert_called_once_with('Директория dir1 записана в директорию dir2')
            mock_logger.info.assert_called()
            assert result is True

    def test_mv_rename_file(self):
        """Переименование файла"""
        with patch('os.access', return_value=True), \
             patch('os.path.exists', side_effect=lambda p: p == 'file.txt'), \
             patch('os.path.isfile', side_effect=lambda p: p == 'file.txt'), \
             patch('os.path.isdir', return_value=False), \
             patch('shutil.move') as mock_move, \
             patch('builtins.print') as mock_print, \
             patch('src.mv.logger') as mock_logger:
            result = mv_function(['mv', 'file.txt', 'file2.txt'])
            mock_move.assert_called_once_with('file.txt', 'file2.txt')
            mock_print.assert_called_once_with('Файл  file.txt переименован file2.txt')
            mock_logger.info.assert_called()
            assert result is True

    def test_mv_rename_dir(self):
        """Переименование директории"""
        with patch('os.access', return_value=True), \
             patch('os.path.exists', side_effect=lambda p: p == 'dir1'), \
             patch('os.path.isfile', return_value=False), \
             patch('os.path.isdir', side_effect=lambda p: p == 'dir1'), \
             patch('shutil.move') as mock_move, \
             patch('builtins.print') as mock_print, \
             patch('src.mv.logger') as mock_logger:
            result = mv_function(['mv', 'dir1', 'dir2'])
            mock_move.assert_called_once_with('dir1', 'dir2')
            mock_print.assert_called_once_with('Директория dir1 переименована dir2')
            mock_logger.info.assert_called()
            assert result is True

    def test_mv_no_such_file(self):
        """Исходный файл не существует"""
        with patch('os.access', return_value=True), \
             patch('os.path.exists', return_value=False), \
             patch('src.mv.logger') as mock_logger:
            with pytest.raises(FileNotFoundError, match='no such file'):
                mv_function(['mv', 'no_file.txt', 'file2.txt'])
            mock_logger.info.assert_called_with('no such file')

    def test_mv_permission_error(self):
        """Нет прав на чтение исходного файла"""
        with patch('os.access', side_effect=lambda p, mode: False if p == 'file.txt' else True), \
             patch('src.mv.logger') as mock_logger:
            with pytest.raises(PermissionError, match='no permission to read the file: file.txt'):
                mv_function(['mv', 'file.txt', 'file2.txt'])
            mock_logger.error.assert_called()

    def test_mv_wrong_args(self):
        """Неправильное количество аргументов"""
        with patch('src.mv.logger') as mock_logger:
            with pytest.raises(ValueError, match='mv: unrecognized option'):
                mv_function(['mv', 'file.txt'])
            mock_logger.error.assert_called()