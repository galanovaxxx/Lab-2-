import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from src.cd import cd_function
from src.my_errors import DirectoryNotFoundError


class TestCd:
    def setup_method(self):
        self.cd = cd_function
        self.cwd = Path("folder")
        self.env = {}

    def test_cd_to_existing_directory(self):
        """cd в существующую директорию"""
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = True
        mock_target.is_dir.return_value = True

        with patch('os.path.isdir', return_value=True), patch("os.chdir",
                                                              return_value=None) as mock_to_path:
            result = self.cd(['cd', "folder"])
        mock_to_path.assert_called_once_with('folder')

    def test_cd_to_nonexistent_directory(self):
        """cd в несуществующую директорию вызывает ошибку"""
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = False

        with pytest.raises(DirectoryNotFoundError, match='no such directory'):
            self.cd(['cd', "no_such_folder"])

    def test_cd_to_home_directory(self):
        with patch('os.path.expanduser', return_value='/home/testuser') as mock_expanduser, \
                patch('os.chdir', return_value=None) as mock_chdir, \
                patch('os.path.isdir', return_value=True) as mock_isdir:
            cd_function(['cd', '~'])
            mock_expanduser.assert_called_once_with("~")
            mock_chdir.assert_called_once_with('/home/testuser')

    def test_cd_to_file(self):
        """cd на файл вызывает ошибку"""
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = True
        mock_target.is_dir.return_value = False

        with pytest.raises(DirectoryNotFoundError, match='no such directory'):
            self.cd(['cd', "file.txt"])

    def test_cd_parent_directory(self):
        """cd .. переходит в директорию выше"""
        with patch('os.path.isdir', return_value=True) as mock_isdir, \
                patch('os.chdir', return_value=None) as mock_chdir:
            cd_function(['cd', '..'])
            mock_isdir.assert_called_once_with('..')
            mock_chdir.assert_called_once_with('..')
