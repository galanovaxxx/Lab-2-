import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
from src.cat import cat_function


class TestCat:
    def setup_method(self):
        self.cat = cat_function
        self.cwd = Path("/test/cwd")
        self.env = {}

    def test_cat_file(self):
        mock_target1 = Mock(spec=Path)
        mock_target1.exists.return_value = True
        mock_target1.is_dir.return_value = False

        file_content = "Hello, world!"

        with patch('os.path.isfile', return_value=True), patch('os.path.splitext', return_value=['', '.txt']), patch(
                'builtins.open', mock_open(read_data=file_content)), \
                patch('builtins.print') as mock_print:
            result = self.cat(["cat", "test.txt"])
            assert result is None

            mock_print.assert_called_once_with(file_content, end='')

    def test_cat_emptyfile(self):
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = True
        mock_target.is_dir.return_value = False

        file_content = ""

        with patch('os.path.isfile', return_value=True), patch('os.path.splitext', return_value=['', '.txt']), patch(
                'builtins.open', mock_open(read_data=file_content)), \
                patch('builtins.print') as mock_print:
            result = self.cat(["cat", "test.txt"])
            assert result is None

            mock_print.assert_not_called()

    def test_cat_no_exist(self):
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = False

        with pytest.raises(FileNotFoundError, match='no such file'):
            self.cat(['cat', "no_exist.txt"])

    def test_cat_inp_problem(self):
        with pytest.raises(ValueError, match='cat: unrecognized option ""'):
            self.cat(['cat'])

    def test_cat_dir(self):
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = True
        mock_target.is_dir.return_value = True

        with pytest.raises(FileNotFoundError, match="no such file"):
            self.cat(['cat', "dir"])

    def test_cat_format_error(self):
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = True
        mock_target.is_dir.return_value = False

        with patch('os.path.isfile', return_value=True), patch('os.path.splitext', return_value=['video', '.mp4']):
            with pytest.raises(UnicodeError, match='failed to decode the file'):
                self.cat(['cat', "video.mp4"])
