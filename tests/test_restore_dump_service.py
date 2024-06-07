import unittest
from unittest.mock import patch, MagicMock, call
import os

# Import the function from the module
from myioninstaller import restore_dump_service

class TestRestoreDumpService(unittest.TestCase):
    @patch('os.makedirs')
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('shutil.rmtree')
    @patch('os.remove')
    @patch('tarfile.open')
    @patch('subprocess.run')
    def test_restore_dump_service(self, mock_subprocess_run, mock_tarfile_open, mock_remove, mock_rmtree, mock_isdir, mock_listdir, mock_makedirs):
        # Setup the mocks
        mock_listdir.return_value = ['dump_test.tar.gz']
        mock_isdir.side_effect = lambda d: d in ["/var/ion-work/db/adnl", "/var/ion-work/db/archive"]
        mock_tar = MagicMock()
        mock_tarfile_open.return_value.__enter__.return_value = mock_tar

        temp_dir = "/tmp/restore_dump_temp"
        dump_file = os.path.join(temp_dir, "dump_file.tar.gz")

        # Call the function
        dump_url = "http://example.com/path/to/dump_file.tar.gz"
        restore_dump_service(dump_url)

        # Debug output for subprocess.run calls
        print("subprocess.run calls:")
        for call_args in mock_subprocess_run.call_args_list:
            print(call_args)

        # Assert that the subprocess run calls are correct
        mock_subprocess_run.assert_any_call(["systemctl", "stop", "validator"])
        mock_subprocess_run.assert_any_call(["systemctl", "start", "validator"])
        mock_subprocess_run.assert_any_call(["wget", "-O", dump_file, dump_url], check=True)

        # Assert that the directories were checked and deleted
        self.assertEqual(mock_isdir.call_count, 7)  # Should check all 7 directories
        mock_rmtree.assert_any_call("/var/ion-work/db/adnl")
        mock_rmtree.assert_any_call("/var/ion-work/db/archive")

        # Assert that the tarfile was opened and extracted
        mock_tarfile_open.assert_called_once_with(dump_file, "r:gz")
        mock_tar.extractall.assert_called_once_with(path="/var/ion-work/db")

        # Assert that the temporary directory was created and deleted
        mock_makedirs.assert_called_once_with(temp_dir, exist_ok=True)
        mock_rmtree.assert_any_call(temp_dir)

    if __name__ == '__main__':
        unittest.main()
