import os.path
import unittest, shutil, tempfile
import io
from unittest.mock import patch
import src.EasyPart as EasyPart



class TestEasyPartFunctions(unittest.TestCase):
    def setUp(self):
        self.main_dir = tempfile.mkdtemp()
        self.abs_path = os.path.join(self.main_dir, '')

        self.fake_trash = os.path.join(self.main_dir, 'trash')
        os.makedirs(self.fake_trash, exist_ok=True)

        self.file1_name = 'file1.txt'
        self.file1_path = os.path.join(self.main_dir, self.file1_name)
        with open(self.file1_path, 'w', encoding='utf-8') as f:
            f.write('Goose company == ваше лучшее будущее.')

        self.file2_name = 'file2.txt'
        self.file2_path = os.path.join(self.main_dir, self.file2_name)
        with open(self.file2_path, 'w', encoding='utf-8') as f:
            f.write('Съешь ещё этих мягких французских булок.')

        self.dir1_name = 'dir1'
        self.dir1_path = os.path.join(self.main_dir, self.dir1_name)
        os.makedirs(self.dir1_path)
        with open(os.path.join(self.dir1_path, 'file3.txt'), 'w', encoding='utf-8') as f:
            f.write('Этот файл застрял :(')

        self.dir2_name = 'dir2'
        self.dir2_path = os.path.join(self.main_dir, self.dir2_name)
        os.makedirs(self.dir2_path)

        self.stdout = io.StringIO()
        self.stdout_patch = patch('sys.stdout', new=self.stdout)
        self.stdout_patch.start()

    def tearDown(self):
        if os.path.exists(self.main_dir):
            shutil.rmtree(self.main_dir)
        self.stdout_patch.stop()

    def test_ls_empty_arg(self):
        EasyPart.ls(self.abs_path, [])
        out = self.stdout.getvalue().strip().split('\n')
        self.assertIn(self.file1_name, out)
        self.assertIn(self.file2_name, out)
        self.assertIn(self.dir1_name, out)
        self.assertIn(self.dir2_name, out)
        self.assertIn('trash', out)

    def test_ls_abs_path(self):
        file256_name = 'file256.txt'
        file256_path = os.path.join(self.dir1_path, file256_name)
        with open(file256_path, 'w', encoding='utf-8') as f:
            f.write('Что писать в этих файлах? У меня уже идеи заканчиваются')

        self.stdout.seek(0)
        self.stdout.truncate(0)

        EasyPart.ls(self.abs_path, [self.dir1_path])
        out = self.stdout.getvalue().strip().split('\n')
        self.assertIn('file3.txt', out)
        self.assertIn(file256_name, out)
        self.assertNotIn(self.file1_name, out)

    def test_ls_not_abs_path(self):
        self.stdout.seek(0)
        self.stdout.truncate(0)

        EasyPart.ls(self.abs_path, [self.dir1_path])
        out = self.stdout.getvalue().strip().split('\n')
        self.assertIn('file3.txt', out)
        self.assertNotIn(self.file1_name, out)

    def test_ls_l(self):
        self.stdout.seek(0)
        self.stdout.truncate(0)

        EasyPart.ls(self.abs_path, ["-l"])
        out = self.stdout.getvalue().strip().split('\n')
        check = False
        for line in out:
            if self.file1_name in line and "Name:" in line and \
                    "Size:" in line and "Date:" in line and "Permission:" in line:
                check = True
        self.assertTrue(check)

    def test_ls_l_path(self):
        self.stdout.seek(0)
        self.stdout.truncate(0)

        EasyPart.ls(self.abs_path, ["-l", self.dir1_name])
        out = self.stdout.getvalue().strip().split('\n')
        check = False
        for line in out:
            if 'file3.txt' in line and "Name:" in line and \
                    "Size:" in line and "Date:" in line and "Permission:" in line:
                check = True
        self.assertTrue(check)
        self.assertNotIn(self.file1_name, out)

    def test_ls_file_not_found(self):
        res = EasyPart.ls(self.abs_path, ["я устал("])
        self.assertEqual(res, "ERROR: File not found")

    def test_ls_unknown_operation(self):
        res = EasyPart.ls(self.abs_path, ['-x', self.dir1_name])
        self.assertEqual(res, "ERROR: Unknown operation")

    def test_cd_up(self):
        sub_dir_path = os.path.join(self.dir1_path, 'sub_dir')
        os.makedirs(sub_dir_path)
        path = os.path.join(sub_dir_path, '')
        path = os.path.normpath(path)
        error, new_path = EasyPart.cd(path, ['..'])
        self.assertIsNone(error)
        self.assertEqual(new_path, os.path.join(self.dir1_path, ''))

    def test_cd_home_dir(self):
        home_dir = os.path.join(self.main_dir, 'home_dir')
        os.makedirs(home_dir, exist_ok=True)
        with patch('os.path.expanduser', return_value=home_dir):
            error, new_path = EasyPart.cd(home_dir, ['~'])
            self.assertIsNone(error)
            self.assertEqual(new_path, os.path.join(home_dir, ''))

    def test_cd_abs_path(self):
        error, new_path = EasyPart.cd(self.abs_path, [self.dir2_path])
        self.assertIsNone(error)
        self.assertEqual(new_path, os.path.join(self.dir2_path, ''))

    def test_cd_not_abs_path(self):
        error, new_path = EasyPart.cd(self.abs_path, [self.dir1_name])
        new_path = os.path.normpath(new_path) + '\\'
        self.assertIsNone(error)
        self.assertEqual(new_path, os.path.join(self.dir1_path, ''))

    def test_cd_dir_not_exists(self):
        error, new_path = EasyPart.cd(self.abs_path, ['goose_pass'])
        self.assertEqual(error, 'ERROR: File or directory does not exist')
        self.assertEqual(new_path, self.abs_path)

    def test_cd_file(self):
        error, new_path = EasyPart.cd(self.abs_path, [self.file1_name])
        self.assertEqual(error, 'ERROR: it is not directory')
        self.assertEqual(new_path, self.abs_path)

    def test_cat_file(self):
        self.stdout.seek(0)
        self.stdout.truncate(0)

        EasyPart.cat(self.abs_path, [self.file1_name])
        out = self.stdout.getvalue().strip().split('\n')
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0], '1: Goose company == ваше лучшее будущее.')

    def test_cat_abs_path(self):
        self.stdout.seek(0)
        self.stdout.truncate(0)

        EasyPart.cat(self.abs_path, [self.file2_path])
        out = self.stdout.getvalue().strip().split('\n')
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0], '1: Съешь ещё этих мягких французских булок.')

    def test_cat_file_not_found(self):
        res = EasyPart.cat(self.abs_path, ['23:05'])
        self.assertEqual(res, 'ERROR: File not found')

    def test_cp_file_to_directory(self):
        file_path = os.path.join(self.dir2_path, self.file1_name)
        res = EasyPart.cp(self.abs_path, [self.file1_name, self.dir2_name])
        self.assertIsNone(res)
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r', encoding='utf-8') as f:
            self.assertEqual(f.read(), 'Goose company == ваше лучшее будущее.')
        self.assertTrue(os.path.exists(self.file1_path))

    def test_cp_rename_file(self):
        file_path = os.path.join(self.abs_path, 'copy.txt')
        res = EasyPart.cp(self.abs_path, [self.file1_name, 'copy.txt'])
        self.assertIsNone(res)
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r', encoding='utf-8') as f:
            self.assertEqual(f.read(), 'Goose company == ваше лучшее будущее.')
        self.assertTrue(os.path.exists(self.file1_path))

    def test_cp_r_dir(self):
        dir_path = os.path.join(self.main_dir, 'copy_dir')
        res = EasyPart.cp(self.abs_path, ['-r', self.dir1_name, 'copy_dir'])
        self.assertIsNone(res)
        self.assertTrue(os.path.isdir(dir_path))
        self.assertTrue(os.path.exists(os.path.join(dir_path, 'file3.txt')))
        self.assertTrue(os.path.isdir(self.dir1_path))

    def test_cp_file_not_found(self):
        res = EasyPart.cp(self.abs_path, ['23:23', self.dir2_name])
        self.assertEqual(res, 'ERROR: File not found')

    def test_cp_missimg_r(self):
        res = EasyPart.cp(self.abs_path, [self.dir1_name, self.dir2_name])
        self.assertEqual(res, "ERROR: Permission error or add '-r'")

    def test_cp_wrong_number_of_arg(self):
        res = EasyPart.cp(self.abs_path, [self.file1_name])
        self.assertEqual(res, "ERROR: Wrong number of arguments")

    def test_cp_unknown_oper(self):
        res = EasyPart.cp(self.abs_path, ["-x", self.file1_name, self.dir2_name])
        self.assertEqual(res, "ERROR: Unknown operation")

    def test_cp_with_space(self):
        file_name = 'we need more space.txt'
        file_path = os.path.join(self.main_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('У меня тесты на 300 строк, для кода на 100 :(')

        dir_path = os.path.join(self.main_dir, 'GOOOSE')
        os.makedirs(dir_path)

        res = EasyPart.cp(self.abs_path, [f'"{file_name}"', f'{dir_path}'])
        self.assertIsNone(res)
        self.assertTrue(os.path.exists(os.path.join(dir_path, file_name)))

    def test_mv_file_to_dir(self):
        file_path = os.path.join(self.dir2_path, self.file1_name)
        res = EasyPart.mv(self.abs_path, [self.file1_name, self.dir2_name])
        self.assertIsNone(res)
        self.assertTrue(os.path.exists(file_path))
        self.assertFalse(os.path.exists(self.file1_path))

    def test_mv_file_rename(self):
        file_path = os.path.join(self.abs_path, 'copy.txt')
        res = EasyPart.mv(self.abs_path, [self.file2_name, 'copy.txt'])
        self.assertIsNone(res)
        self.assertTrue(os.path.exists(file_path))
        self.assertFalse(os.path.exists(self.file2_path))

    def test_mv_dir(self):
        dir_path = os.path.join(self.abs_path, 'dir')
        os.makedirs(dir_path)
        res = EasyPart.mv(self.abs_path, [self.dir1_name, 'dir'])
        self.assertIsNone(res)
        self.assertFalse(os.path.exists(self.dir1_path))

        new_dir_path = os.path.join(dir_path, self.dir1_name)
        self.assertTrue(os.path.isdir(new_dir_path))
        self.assertTrue(os.path.exists(os.path.join(new_dir_path, 'file3.txt')))

    def test_mv_file_not_found(self):
        res = EasyPart.mv(self.abs_path, ['23:59', self.dir2_name])
        self.assertEqual(res, 'ERROR: File not found')

    def test_mv_wrong_number_of_arg(self):
        res = EasyPart.mv(self.abs_path, [self.file1_name])
        self.assertEqual(res, "ERROR: Wrong number of arguments")

    def test_mv_with_space(self):
        file_name = 'we need more space.txt'
        file_path = os.path.join(self.main_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('Еще немного и можно спать.')

        dir_name = 'a lot of information'
        dir_path = os.path.join(self.main_dir, dir_name)
        os.makedirs(dir_path)

        res = EasyPart.mv(self.abs_path, [f'"{file_name}"', dir_name])
        self.assertIsNone(res)
        self.assertTrue(os.path.exists(os.path.join(dir_path, file_name)))
        self.assertFalse(os.path.exists(os.path.join(file_path)))

    @patch('builtins.input', return_value='y')
    def test_rm_file(self, mock_input):
        with patch('os.replace') as mock_os_replace:
            res = EasyPart.rm(self.abs_path, [self.file1_name])
            self.assertIsNone(res)
            mock_os_replace.assert_called_once()
            src, new_path = mock_os_replace.call_args[0]
            src, new_path = os.path.normpath(src), os.path.normpath(new_path)

            self.assertEqual(src, self.file1_path)
            self.assertTrue('trash' in new_path.lower())
            self.assertEqual(os.path.basename(new_path), os.path.basename(self.file1_path))

    @patch('builtins.input', return_value='y')
    def test_rm_dir_with_r(self, mock_input):
        with patch('os.replace') as mock_os_replace:
            res = EasyPart.rm(self.abs_path, ['-r', self.dir1_name])
            self.assertIsNone(res)
            mock_os_replace.assert_called_once()
            src, new_path = mock_os_replace.call_args[0]
            src, new_path = os.path.normpath(src), os.path.normpath(new_path)
            self.assertEqual(src, self.dir1_path)
            self.assertTrue('trash' in new_path.lower())
            self.assertEqual(os.path.basename(new_path), os.path.basename(self.dir1_path))

    @patch('builtins.input', return_value='n')
    def test_rm_dir_with_ans_n(self, mock_input):
        with patch('os.replace') as mock_os_replace:
            res = EasyPart.rm(self.abs_path, ['-r', self.dir1_name])
            self.assertIsNone(res)
            mock_os_replace.assert_not_called()
            self.assertTrue(os.path.exists(self.dir1_path))

    def test_rm_file_not_found(self):
        res = EasyPart.rm(self.abs_path, ['FakeFile.txt'])
        self.assertEqual(res, 'ERROR: File not found')

    def test_rm_dir_missing_r(self):
        res = EasyPart.rm(self.abs_path, [self.dir1_name])
        self.assertEqual(res, "ERROR: Unknown operation or missing '-r'")

    def test_rm_wrong_number_of_arg(self):
        res = EasyPart.rm(self.abs_path, [])
        self.assertEqual(res, 'ERROR: Wrong number of arguments')

    def test_rm_only_r(self):
        rs = EasyPart.rm(self.abs_path, ['-r'])
        self.assertEqual(rs, 'ERROR: OSError')