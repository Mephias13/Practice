import unittest
from io import StringIO
from unittest.mock import patch
from shell_emulator import ls, cd, echo, clear, exit_shell, load_vfs, execute_command


class TestShellEmulator(unittest.TestCase):

    def setUp(self):
        self.vfs_data = {
            '/': None,
            '/file1.txt': 'content1',
            '/dir/': None,
            '/dir/file2.txt': 'content2',
            '/dir/file3.txt': 'content3',
            '/dir2/': None,
            '/dir2/name.txt': 'line1\nline2\nline1\nline3'


        }
        self.vfs = self.vfs_data
        self.current_dir = "/"

    def run_command(self, command):
        with patch('sys.stdout', new=StringIO()) as output:
            self.current_dir = execute_command(command, self.current_dir, self.vfs)
            return output.getvalue().strip()


    def test_echo(self):
        self.assertEqual(self.run_command("echo hello"), "hello")
        self.assertEqual(self.run_command("echo hello world"), "hello world")
        self.assertEqual(self.run_command("echo 123"), "123")


    def test_ls(self):
        self.assertEqual(self.run_command("ls /"), "dir\ndir2\nfile1.txt")
        self.assertEqual(self.run_command("cd dir; ls"), "file2.txt\nfile3.txt")
        self.assertEqual(self.run_command("cd /dir2; ls"), "name.txt")


    def test_cd(self):
        self.assertEqual(self.run_command("cd dir"), "")
        self.assertEqual(self.current_dir, "/dir")
        self.assertEqual(self.run_command("cd /"), "")
        self.assertEqual(self.current_dir, "/")
        self.assertEqual(self.run_command("cd invalid_dir"), "Directory not found.")


    @patch('os.system')
    def test_clear(self, mock_system):
        clear()
        clear()
        clear()




    def test_exit(self):
        with self.assertRaises(SystemExit):
            exit_shell()
        with self.assertRaises(SystemExit):
            exit_shell()
        with self.assertRaises(SystemExit):
            exit_shell()



if __name__ == "__main__":
    unittest.main()