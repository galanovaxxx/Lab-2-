import pytest
from src.ls import ls_function
from unittest.mock import patch, call
import os
import stat
from datetime import datetime


def test_ls_current_dir(mocker):
    mocker.patch("os.listdir", return_value=["file1.txt", "script.py"])
    mocker.patch("builtins.print")

    ls_function(['ls'])

    assert print.call_count == 3
    assert print.call_args_list[0] == call("file1.txt")
    assert print.call_args_list[1] == call("script.py")
    assert print.call_args_list[2] == call("_____")


def test_ls_with_path(mocker):
    mocker.patch("os.path.isdir", return_value=True)
    mocker.patch("os.listdir", return_value=["data.csv"])
    mocker.patch("builtins.print")

    ls_function(["ls", "/my/path"])

    assert print.call_count == 2
    assert print.call_args_list[0] == call("data.csv")
    assert print.call_args_list[1] == call("_____")


def test_ls_long_format(mocker):
    mocker.patch("os.path.isdir", return_value=True)
    mocker.patch("os.listdir", return_value=["a.txt"])

    stat_result = os.stat_result((
        0o100644,  # st_mode
        123,  # st_ino
        1,  # st_dev
        1,  # st_nlink
        1000,  # st_uid
        1000,  # st_gid
        1024,  # st_size
        1700000000,  # st_atime
        1700000000,  # st_mtime
        1700000000  # st_ctime
    ))
    mocker.patch("os.stat", return_value=stat_result)
    mocker.patch("builtins.print")

    ls_function(["ls", "-l"])

    expected_mode = stat.filemode(0o100644)
    expected_line = f"{expected_mode} 1000 1024  {datetime.fromtimestamp(1700000000)} a.txt"
    assert call(' '.join([str(i) for i in print.call_args_list[0][0]])) == call(expected_line)
    assert print.call_args_list[1] == call("_____")


def test_ls_l_with_path(mocker):
    mocker.patch("os.path.isdir", return_value=True)
    mocker.patch("os.listdir", return_value=["log.log"])

    stat_result = os.stat_result((0o100400, 0, 0, 1, 1001, 1001, 512, 1700000000, 1700000000, 1700000000))
    mocker.patch("os.stat", return_value=stat_result)
    mocker.patch("builtins.print")

    ls_function(["ls", "-l", "/var/log"])

    expected_mode = stat.filemode(0o100400)  # '-r--------'
    expected_line = f"{expected_mode} 1001 512   {datetime.fromtimestamp(1700000000)} log.log"
    assert call(' '.join([str(i) for i in print.call_args_list[0][0]])) == call(expected_line)
    assert print.call_args_list[1] == call("_____")


def test_ls_multiple_ls(mocker):
    """Тест: несколько 'ls' в команде — ошибка"""
    with pytest.raises(ValueError) as exc_info:
        ls_function(["ls", "ls", "file.txt"])

    assert "unrecognized option" in str(exc_info.value)


def test_ls_notexistent_directory(mocker, caplog):
    mocker.patch("os.path.isdir", return_value=False)
    mocker.patch("logging.Logger.error")

    with pytest.raises(FileNotFoundError) as exc_info:
        ls_function(["ls", "/non/existent"])

    assert str(exc_info.value) == "no such directory"


def test_ls_empty_directory(mocker):
    mocker.patch("os.path.isdir", return_value=True)
    mocker.patch("os.listdir", return_value=[])
    mocker.patch("builtins.print")

    ls_function(["ls"])

    assert print.call_count == 1
    assert print.call_args_list[0] == call("_____")
