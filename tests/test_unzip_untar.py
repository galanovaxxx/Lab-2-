import pytest
from unittest.mock import patch, MagicMock
from src.unzip_untar import unzip_untar_function
from src.my_errors import DirectoryNotFoundError


class TestUnzipUntar:
    def test_unzip_zip_success(self):
        with patch('os.path.isfile', return_value=True), \
                patch('os.access', return_value=True), \
                patch('zipfile.ZipFile') as mock_zip, \
                patch('builtins.print') as mock_print:
            mock_zip.return_value.__enter__.return_value.extractall = MagicMock()
            result = unzip_untar_function(['unzip', 'archive.zip'])
            mock_zip.assert_called_once_with('archive.zip', 'r')
            mock_zip.return_value.__enter__.return_value.extractall.assert_called_once_with()
            mock_print.assert_called_once_with('the file archive.zip in unarchived')
            assert result is None

    def test_untar_tar_success(self):
        with patch('os.path.isfile', return_value=True), \
                patch('os.access', return_value=True), \
                patch('tarfile.open') as mock_tar, \
                patch('builtins.print') as mock_print:
            mock_tar.return_value.__enter__.return_value.extractall = MagicMock()
            result = unzip_untar_function(['untar', 'archive.tar'])
            mock_tar.assert_called_once_with('archive.tar', 'r')
            mock_tar.return_value.__enter__.return_value.extractall.assert_called_once_with()
            mock_print.assert_called_once_with('the file archive.tar is unarchived')
            assert result is None

    def test_unzip_no_file(self):
        with patch('os.path.isfile', return_value=False):
            with pytest.raises(DirectoryNotFoundError, match='no such directory'):
                unzip_untar_function(['unzip', 'nofile.zip'])

    def test_untar_no_file(self):
        with patch('os.path.isfile', return_value=False):
            with pytest.raises(DirectoryNotFoundError, match='no such directory'):
                unzip_untar_function(['untar', 'nofile.tar'])

    def test_unzip_permission_error(self):
        with patch('os.path.isfile', return_value=True), \
                patch('os.access', return_value=False):
            with pytest.raises(PermissionError, match='no permission to read the dir: archive.zip'):
                unzip_untar_function(['unzip', 'archive.zip'])

    def test_untar_permission_error(self):
        with patch('os.path.isfile', return_value=True), \
                patch('os.access', return_value=False):
            with pytest.raises(PermissionError, match='no permission to read the dir: archive.tar'):
                unzip_untar_function(['untar', 'archive.tar'])

    def test_unzip_zip_fail(self):
        with patch('os.path.isfile', return_value=True), \
                patch('os.access', return_value=True), \
                patch('zipfile.ZipFile', side_effect=Exception("fail")):
            with pytest.raises(ValueError, match='unzip: unrecognized option "archive.zip"'):
                unzip_untar_function(['unzip', 'archive.zip'])

    def test_untar_tar_fail(self):
        with patch('os.path.isfile', return_value=True), \
                patch('os.access', return_value=True), \
                patch('tarfile.open', side_effect=Exception("fail")):
            with pytest.raises(ValueError, match='untar: unrecognized option "archive.tar"'):
                unzip_untar_function(['untar', 'archive.tar'])

    def test_wrong_args(self):
        with pytest.raises(ValueError, match='unzip: unrecognized option "archive.zip extra"'):
            unzip_untar_function(['unzip', 'archive.zip', 'extra'])
