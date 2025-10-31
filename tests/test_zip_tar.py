import unittest
from unittest.mock import patch

import src.zip_tar as zip_tar

class TestZip(unittest.TestCase):
    def setUp(self):
        self.abs_path = 'C:\\dir'

    @patch('src.zip_tar.shutil.make_archive')
    def test_zip_abs_path(self, mock_make_archive):
        res = zip_tar.zip(self.abs_path, ['D:\\dir', 'archive'])
        self.assertIsNone(res)
        mock_make_archive.assert_called_once_with('archive', 'zip', 'D:\\dir')

    @patch('src.zip_tar.shutil.make_archive')
    def test_zip_not_abs_path(self, mock_make_archive):
        res = zip_tar.zip(self.abs_path, ['dir', 'archive'])
        self.assertIsNone(res)
        mock_make_archive.assert_called_once_with('archive', 'zip', f'{self.abs_path}\\dir')

    @patch('src.zip_tar.shutil.make_archive')
    def test_zip_with_spaces(self, mock_make_archive):
        res = zip_tar.zip(self.abs_path, ['"D:\\d i r"', 'ar chi ve'])
        self.assertIsNone(res)
        mock_make_archive.assert_called_once_with('ar chi ve', 'zip', 'D:\\d i r')

    @patch('src.zip_tar.shutil.make_archive')
    def test_zip_file_not_found(self, mock_make_archive):
        mock_make_archive.side_effect = FileNotFoundError
        res = zip_tar.zip(self.abs_path, ['dir', 'archive'])
        self.assertEqual(res, "ERROR: File not found")

    @patch('src.zip_tar.shutil.make_archive')
    def test_zip_permission_error(self, mock_make_archive):
        mock_make_archive.side_effect = PermissionError
        res = zip_tar.zip(self.abs_path, ['dir', 'archive'])
        self.assertEqual(res, "ERROR: Permission error")

    @patch('src.zip_tar.shutil.make_archive')
    def test_zip_shutil_error(self, mock_make_archive):
        mock_make_archive.side_effect = zip_tar.shutil.Error("Test shutil error")
        res = zip_tar.zip(self.abs_path, ['dir', 'archive'])
        self.assertEqual(res, "ERROR: Shutil error")

    def test_zip_wrong_number_of_arg(self):
        res = zip_tar.zip(self.abs_path, ['archive'])
        self.assertEqual(res, "ERROR: Wrong number of arguments")

    def test_zip_empty_input(self):
        res = zip_tar.zip(self.abs_path, [])
        self.assertEqual(res, "ERROR: Wrong number of arguments")

    @patch('src.zip_tar.shutil.unpack_archive')
    def test_unzip_abs_path(self, mock_unpack_archive):
        res = zip_tar.unzip(self.abs_path, ['D:\\dir\\archives.zip'])
        self.assertIsNone(res)
        mock_unpack_archive.assert_called_once_with('D:\\dir\\archives.zip')

    @patch('src.zip_tar.shutil.unpack_archive')
    def test_unzip_not_abs_path(self, mock_unpack_archive):
        res = zip_tar.unzip(self.abs_path, ['archives.zip'])
        self.assertIsNone(res)
        mock_unpack_archive.assert_called_once_with(f'{self.abs_path}\\archives.zip')

    @patch('src.zip_tar.shutil.unpack_archive')
    def test_unzip_only_name(self, mock_unpack_archive):
        res = zip_tar.unzip(self.abs_path, ['archives'])
        self.assertIsNone(res)
        mock_unpack_archive.assert_called_once_with(f'{self.abs_path}\\archives.zip')

    @patch('src.zip_tar.shutil.unpack_archive')
    def test_unzip_permission_error(self, mock_unpack_archive):
        mock_unpack_archive.side_effect = PermissionError
        res = zip_tar.unzip(self.abs_path, ['archives.zip'])
        self.assertEqual(res, "ERROR: Permission error")

    @patch('src.zip_tar.shutil.unpack_archive')
    def test_unzip_file_not_found(self, mock_unpack_archive):
        mock_unpack_archive.side_effect = FileNotFoundError
        res = zip_tar.unzip(self.abs_path, ['archives.zip'])
        self.assertEqual(res, "ERROR: File not found")

    @patch('src.zip_tar.shutil.unpack_archive')
    def test_unzip_read_error(self, mock_unpack_archive):
        mock_unpack_archive.side_effect = zip_tar.shutil.ReadError("Test unzip error")
        res = zip_tar.unzip(self.abs_path, ['archives.zip'])
        self.assertEqual(res, "ERROR: It is not zip file")

    @patch('src.zip_tar.shutil.unpack_archive')
    def test_unzip_shutil_error(self, mock_unpack_archive):
        mock_unpack_archive.side_effect = zip_tar.shutil.Error("Test shutil error")
        res = zip_tar.unzip(self.abs_path, ['archives.zip'])
        self.assertEqual(res, "ERROR: Shutil error")

    def test_unzip_empty_input(self):
        res = zip_tar.unzip(self.abs_path, [])
        self.assertEqual(res, "ERROR: Wrong number of arguments")


class TestTar(unittest.TestCase):
    def setUp(self):
        self.abs_path = 'C:\\dir'

    @patch('src.zip_tar.shutil.make_archive')
    def test_tar_abs_path(self, mock_make_archive):
        res = zip_tar.tar(self.abs_path, ['D:\\dir', 'archive'])
        self.assertIsNone(res)
        mock_make_archive.assert_called_once_with('archive', 'gztar', 'D:\\dir')

    @patch('src.zip_tar.shutil.make_archive')
    def test_tar_not_abs_path(self, mock_make_archive):
        res = zip_tar.tar(self.abs_path, ['dir', 'archive'])
        self.assertIsNone(res)
        mock_make_archive.assert_called_once_with('archive', 'gztar', f'{self.abs_path}\\dir')

    @patch('src.zip_tar.shutil.make_archive')
    def test_tar_with_spaces(self, mock_make_archive):
        res = zip_tar.tar(self.abs_path, ['"D:\\d i r"', 'ar chi ve'])
        self.assertIsNone(res)
        mock_make_archive.assert_called_once_with('ar chi ve', 'gztar', 'D:\\d i r')

    @patch('src.zip_tar.shutil.make_archive')
    def test_tar_file_not_found(self, mock_make_archive):
        mock_make_archive.side_effect = FileNotFoundError
        res = zip_tar.tar(self.abs_path, ['dir', 'archive'])
        self.assertEqual(res, "ERROR: File not found")

    @patch('src.zip_tar.shutil.make_archive')
    def test_tar_permission_error(self, mock_make_archive):
        mock_make_archive.side_effect = PermissionError
        res = zip_tar.tar(self.abs_path, ['dir', 'archive'])
        self.assertEqual(res, "ERROR: Permission error")

    @patch('src.zip_tar.shutil.make_archive')
    def test_tar_shutil_error(self, mock_make_archive):
        mock_make_archive.side_effect = zip_tar.shutil.Error("Test shutil error")
        res = zip_tar.tar(self.abs_path, ['dir', 'archive'])
        self.assertEqual(res, "ERROR: Shutil error")

    def test_tar_wrong_number_of_arg(self):
        res = zip_tar.tar(self.abs_path, ['archive'])
        self.assertEqual(res, "ERROR: Wrong number of arguments")

    def test_tar_empty_input(self):
        res = zip_tar.tar(self.abs_path, [])
        self.assertEqual(res, "ERROR: Wrong number of arguments")

    @patch('src.zip_tar.shutil.unpack_archive')
    def test_untar_abs_path(self, mock_unpack_archive):
        res = zip_tar.untar(self.abs_path, ['D:\\dir\\archives.tar.gz'])
        self.assertIsNone(res)
        mock_unpack_archive.assert_called_once_with('D:\\dir\\archives.tar.gz')

    @patch('src.zip_tar.shutil.unpack_archive')
    def test_untar_not_abs_path(self, mock_unpack_archive):
        res = zip_tar.untar(self.abs_path, ['archives.tar.gz'])
        self.assertIsNone(res)
        mock_unpack_archive.assert_called_once_with(f'{self.abs_path}\\archives.tar.gz')

    @patch('src.zip_tar.shutil.unpack_archive')
    def test_untar_only_name(self, mock_unpack_archive):
        res = zip_tar.untar(self.abs_path, ['archives'])
        self.assertIsNone(res)
        mock_unpack_archive.assert_called_once_with(f'{self.abs_path}\\archives.tar.gz')

    @patch('src.zip_tar.shutil.unpack_archive')
    def test_untar_permission_error(self, mock_unpack_archive):
        mock_unpack_archive.side_effect = PermissionError
        res = zip_tar.untar(self.abs_path, ['archives.zip'])
        self.assertEqual(res, "ERROR: Permission error")

    @patch('src.zip_tar.shutil.unpack_archive')
    def test_untar_file_not_found(self, mock_unpack_archive):
        mock_unpack_archive.side_effect = FileNotFoundError
        res = zip_tar.untar(self.abs_path, ['archives.zip'])
        self.assertEqual(res, "ERROR: File not found")

    @patch('src.zip_tar.shutil.unpack_archive')
    def test_untar_read_error(self, mock_unpack_archive):
        mock_unpack_archive.side_effect = zip_tar.shutil.ReadError("Test untar error")
        res = zip_tar.untar(self.abs_path, ['archives.zip'])
        self.assertEqual(res, "ERROR: It is not zip file")

    @patch('src.zip_tar.shutil.unpack_archive')
    def test_untar_shutil_error(self, mock_unpack_archive):
        mock_unpack_archive.side_effect = zip_tar.shutil.Error("Test shutil error")
        res = zip_tar.untar(self.abs_path, ['archives.zip'])
        self.assertEqual(res, "ERROR: Shutil error")

    def test_untar_empty_input(self):
        res = zip_tar.untar(self.abs_path, [])
        self.assertEqual(res, "ERROR: Wrong number of arguments")