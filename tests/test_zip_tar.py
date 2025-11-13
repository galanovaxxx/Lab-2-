import pytest
from unittest.mock import patch, MagicMock
from src.zip_tar import zip_tar_function
from pathlib import Path
from src.my_errors import DirectoryNotFoundError


class TestZipTar:
    def test_tar_success(self):
        with patch('os.path.isdir', return_value=True), \
                patch('os.access', return_value=True), \
                patch('tarfile.open') as mock_tar, \
                patch('builtins.print') as mock_print:
            tar_mock = MagicMock()
            mock_tar.return_value.__enter__.return_value = tar_mock
            zip_tar_function(['tar', '/dir', 'archive.tar.gz'])
            tar_mock.add.assert_called_once_with('/dir', arcname='archive.tar.gz')
            mock_print.assert_called_once_with('file /dir is archived as tar')

    def test_no_directory(self):
        with patch('os.path.isdir', return_value=False):
            with pytest.raises(DirectoryNotFoundError, match='no such directory'):
                zip_tar_function(['zip', '/no_dir', 'archive.zip'])

    def test_no_permission(self):
        with patch('os.path.isdir', return_value=True), \
                patch('os.access', side_effect=[False, False]):
            with pytest.raises(PermissionError, match='no permission to read the dir: /dir'):
                zip_tar_function(['zip', '/dir', 'archive.zip'])

    def test_wrong_args(self):
        with pytest.raises(ValueError, match='zip: unrecognized option'):
            zip_tar_function(['zip', '/dir'])

    def test_zip_exception(self):
        with patch('os.path.isdir', return_value=True), \
                patch('os.access', return_value=True), \
                patch('os.walk', return_value=[('/dir', [], ['a.txt'])]), \
                patch('zipfile.ZipFile', side_effect=Exception("fail")):
            with pytest.raises(ValueError, match='zip: unrecognized option'):
                zip_tar_function(['zip', '/dir', 'archive.zip'])

    def test_tar_exception(self):
        with patch('os.path.isdir', return_value=True), \
                patch('os.access', return_value=True), \
                patch('tarfile.open', side_effect=Exception("fail")):
            with pytest.raises(ValueError, match='tar: unrecognized option'):
                zip_tar_function(['tar', '/dir', 'archive.tar.gz'])
