import os, io, shutil, unittest, contextlib

import src.history_undo as history_undo

class TestHistoryUndo(unittest.TestCase):
    def setUp(self):
        self.path = os.path.abspath(history_undo.__file__)[:-19]
        self.his = os.path.join(os.getcwd(), 'his.history')
        self.undo_his = os.path.join(os.getcwd(), 'undo_his.history')
        for i in (self.his, self.undo_his):
            if os.path.exists(i):
                os.remove(i)

        self.new_path = []

    def tearDown(self):
        for i in (self.his, self.undo_his):
            try:
                if os.path.exists(i):
                    os.remove(i)
            except:
                pass

        for path in self.new_path:
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
            except:
                pass

    def _make_path(self, *path):
        return self.path + '\\' + '\\'.join(path) if path else self.path

    def _create(self, path, line):
        dir = os.path.dirname(path)
        if dir and not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)
            self.new_path.append(dir)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(line)
        self.new_path.append(path)

    def test_history(self):
        with open(self.his, 'w', encoding='utf-8') as f:
            f.write('Я скоро доделаю тесты\n')
            f.write('УРАААА\n')
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            res = history_undo.history()
        self.assertIsNone(res)
        self.assertEqual(out.getvalue(), '1: Я скоро доделаю тесты\n2: УРАААА\n')

    def test_error_empty_undo_history(self):
        with open(self.undo_his, 'w', encoding='utf-8'):
            pass
        res = history_undo.undo()
        self.assertEqual(res, "ERROR: History of the undo is empty")

    def test_undo_rm(self):
        file_path = self._make_path('deleted.txt')
        trash_path = f'{self.path}trash\\deleted.txt'
        self._create(trash_path, file_path)
        with open(self.undo_his, 'w', encoding='utf-8') as f:
            f.write(f'{self.path} <:> rm <:> deleted.txt\n')
        res = history_undo.undo()

        self.assertIsNone(res)
        self.assertTrue(os.path.exists(file_path))
        self.assertFalse(os.path.exists(trash_path))
        self.new_path.append(file_path)
        self.new_path.append(os.path.dirname(trash_path))

    def test_undo_mv(self):
        orig = self._make_path('orig.txt')
        moved = self._make_path('moved_dir')
        self._create(moved, 'goose')
        with open(self.undo_his, 'w', encoding='utf-8') as f:
            f.write(f'{self.path} <:> mv <:> orig.txt moved_dir\n')
        res = history_undo.undo()

        self.assertIsNone(res)
        self.assertTrue(os.path.exists(orig))
        self.assertFalse(os.path.exists(moved))
        self.new_path.append(orig)
        self.new_path.append(os.path.dirname(moved))

    def test_undo_cp(self):
        copy_path = self._make_path('dir' + '\\' + 'orig.txt')
        self._create(copy_path, 'copy')
        with open(self.undo_his, 'w', encoding='utf-8') as f:
            f.write(f'{self.path} <:> cp <:> orig.txt dir\n')
        res = history_undo.undo()

        self.assertIsNone(res)
        self.assertFalse(os.path.exists(copy_path))
        self.new_path.append(os.path.dirname(copy_path))

if __name__ == '__main__':
    unittest.main()