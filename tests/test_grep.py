import unittest, os, shutil, tempfile
from io import StringIO
from unittest.mock import patch
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
        with open(self.file1, 'w', encoding='utf-8'):
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
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.file1 = os.path.join(self.dir, 'file1.txt')
        self.file2 = os.path.join(self.dir, 'file2.txt')
        self.file3 = os.path.join(self.dir, 'file3.txt')

        with open(self.file1, 'w', encoding='utf-8') as f:
            f.write("123\n345\nгусь567")
        with open(self.file2, 'w', encoding='utf-8') as f:
            f.write("абв.\nгусь\n$чебупель^")
        with open(self.file3, 'w', encoding='utf-8') as f:
            f.write("12 бананов\nне гусь\nГусЬ.")

    def tearDown(self):
        shutil.rmtree(self.dir)

    @patch('src.grep.find_in_file')
    def test_grep_basa(self, mock_find_in_file):
        grep(self.dir, ['"123"', "file1.txt"])
        mock_find_in_file.assert_called_with(self.file1, "123", False)

    @patch('src.grep.find_in_file')
    def test_grep_empty_patern(self, mock_find_in_file):
        grep(self.dir, ['""', "file1.txt"])
        mock_find_in_file.assert_called_with(self.file1, "", False)

    @patch('src.grep.find_in_file')
    def test_grep_ignor_reg(self, mock_find_in_file):
        grep(self.dir, ['-i', '"123"', "file1.txt"])
        mock_find_in_file.assert_called_with(self.file1, "123", True)

    @patch('src.grep.find_in_file')
    def test_grep_in_dir(self, mock_find_in_file):
        grep(self.dir, ['-r', '"гусь"', '.'])

        check = [
            unittest.mock.call(os.path.join(self.dir, '.', os.path.basename(self.file1)), "гусь", False),
            unittest.mock.call(os.path.join(self.dir, '.', os.path.basename(self.file2)), "гусь", False),
            unittest.mock.call(os.path.join(self.dir, '.', os.path.basename(self.file3)), "гусь", False),
        ]

        mock_find_in_file.assert_has_calls(check, any_order=False)
        self.assertEqual(mock_find_in_file.call_count, 3)

    @patch('src.grep.find_in_file')
    def test_grep_in_dir_ignor_reg(self, mock_find_in_file):
        grep(self.dir, ['-r', '-i', '"гусь"', '.'])

        check = [
            unittest.mock.call(os.path.join(self.dir, '.', os.path.basename(self.file1)), "гусь", True),
            unittest.mock.call(os.path.join(self.dir, '.', os.path.basename(self.file2)), "гусь", True),
            unittest.mock.call(os.path.join(self.dir, '.', os.path.basename(self.file3)), "гусь", True),
        ]

        mock_find_in_file.assert_has_calls(check, any_order=False)
        self.assertEqual(mock_find_in_file.call_count, 3)

    def test_grep_mis_r(self):
        res = grep(self.dir, ['"123"', '.'])
        self.assertEqual(res, "ERROR: missing -r")

    def test_grep_path_not_found(self):
        res = grep(self.dir, ['"goose"', 'doubleGoose'])
        self.assertEqual(res, f"ERROR: {self.dir}\\doubleGoose is not a file or directory")