import os
import tempfile
import unittest
import unittest.mock
from pathlib import Path

from ..context import zoia
import zoia.cli.init


class TestIsValidInitDir(unittest.TestCase):
    def test__is_valid_init_dir_none(self):
        self.assertFalse(zoia.cli.init._is_valid_init_dir(None))

    def test__is_valid_init_dir_no_exists(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            directory = os.path.join(tmpdir, 'foo')
            self.assertTrue(zoia.cli.init._is_valid_init_dir(directory))

    def test__is_valid_init_dir_exists_and_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self.assertTrue(zoia.cli.init._is_valid_init_dir(tmpdir))

    def test__is_valid_init_dir_exists_not_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / 'foo').touch()
            self.assertFalse(zoia.cli.init._is_valid_init_dir(tmpdir))


@unittest.mock.patch('zoia.cli.init._is_valid_init_dir')
@unittest.mock.patch('zoia.cli.init.os.getcwd')
class TestGetDefaultDirectory(unittest.TestCase):
    def test__get_default_directory_cwd(
        self, mock_getcwd, mock_is_valid_init_dir
    ):
        mock_getcwd.return_value = '/home/foo'
        mock_is_valid_init_dir.side_effect = lambda x: x == '/home/foo'
        observed_default_directory = zoia.cli.init._get_default_library_root()
        expected_default_directory = '/home/foo'
        self.assertEqual(
            observed_default_directory, expected_default_directory
        )

    def test__get_default_directory_subdir(
        self, mock_getcwd, mock_is_valid_init_dir
    ):
        mock_getcwd.return_value = '/home/foo'
        mock_is_valid_init_dir.side_effect = lambda x: x == '/home/foo/zoia'
        observed_default_directory = zoia.cli.init._get_default_library_root()
        expected_default_directory = '/home/foo/zoia'
        self.assertEqual(
            observed_default_directory, expected_default_directory
        )

    def test__get_default_directory_none(
        self, mock_getcwd, mock_is_valid_init_dir
    ):
        mock_getcwd.return_value = '/home/foo'
        mock_is_valid_init_dir.side_effect = lambda x: False
        observed_default_directory = zoia.cli.init._get_default_library_root()
        self.assertIsNone(observed_default_directory)
