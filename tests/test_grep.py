import unittest, os, sys, shutil, tempfile
from io import StringIO
from unittest.mock import patch, mock_open
from src.grep import grep, find_in_file


class TestFindInFile(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.file1 = os.path.join(self.dir, 'file1.txt')

    def tearDown(self):
        shutil.rmtree(self.dir)

    @patch('sys.stdout', new_callable=StringIO)
    def test_find_in_file_basa(self, mock_stdout):
        with open(self.file1, 'w', encoding='utf-8') as f:
            f.write("АбВ\nгУсьА.\nА.!123\nqweАrty.")

        find_in_file(self.file1, "123", False)
        check = "Name: file1.txt       Number of line:     3 Line: А.!123\n"
        self.assertEqual(mock_stdout.getvalue(), check)

    @patch('sys.stdout', new_callable=StringIO)
    def test_find_in_file_re(self, mock_stdout):
        with open(self.file1, 'w', encoding='utf-8') as f:
            f.write("АбВ\nгУсьА.\nА.!123\nqweАrty.")

        find_in_file(self.file1, "^А", False)
        check = (
            'Name: file1.txt       Number of line:     1 Line: АбВ\n'
            'Name: file1.txt       Number of line:     3 Line: А.!123\n'
        )
        self.assertEqual(mock_stdout.getvalue(), check)

    @patch('sys.stdout', new_callable=StringIO)
    def test_find_in_file_regis(self, mock_stdout):
        with open(self.file1, 'w', encoding='utf-8') as f:
            f.write("АбВ\nгУсьА.\nА.!123\nqweАrty.")

        find_in_file(self.file1, "абв", True)
        check = (
            'Name: file1.txt       Number of line:     1 Line: АбВ\n'
        )
        self.assertEqual(mock_stdout.getvalue(), check)

    @patch('sys.stdout', new_callable=StringIO)
    def test_find_in_file_goose(self, mock_stdout):
        with open(self.file1, 'w', encoding='utf-8') as f:
            f.write("АбВ\nгУсь.\nА.!123\nqweАrty.")

        find_in_file(self.file1, "гусь", True)
        check = (
            'Name: file1.txt       Number of line:     2 Line: гУсь.\n'
        )
        self.assertEqual(mock_stdout.getvalue(), check)

    @patch('sys.stdout', new_callable=StringIO)
    def test_find_in_file_point(self, mock_stdout):
        with open(self.file1, 'w', encoding='utf-8') as f:
            f.write("АбВ\nгУсь.\nА.!123\nqweАrty.")

        find_in_file(self.file1, "\.$", True)
        check = (
            'Name: file1.txt       Number of line:     2 Line: гУсь.\n'
            'Name: file1.txt       Number of line:     4 Line: qweАrty.\n'
        )
        self.assertEqual(mock_stdout.getvalue(), check)

    @patch('sys.stdout', new_callable=StringIO)
    def test_find_in_file_empty(self, mock_stdout):
        with open(self.file1, 'w', encoding='utf-8') as f:
            pass
        find_in_file(self.file1, "goose", False)
        self.assertEqual(mock_stdout.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    def test_find_in_file_final(self, mock_stdout):
        with open(self.file1, 'w', encoding='utf-8') as f:
            f.write("АбВ\nгУсь.\nа.!123\nqweАrty.")

        find_in_file(self.file1, "^а|q", False)
        check = (
            'Name: file1.txt       Number of line:     3 Line: а.!123\n'
            'Name: file1.txt       Number of line:     4 Line: qweАrty.\n'
        )
        self.assertEqual(mock_stdout.getvalue(), check)

    def test_find_in_file_file_not_found(self):
        res = find_in_file("qweasdzxc.txt", "goose", False)
        self.assertEqual(res, "ERROR: File not found")

class TestGrep(unittest.TestCase):
    pass