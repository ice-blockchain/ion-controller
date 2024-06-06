import unittest
from unittest.mock import patch, mock_open, MagicMock
import os

# Import the function from the module
from myioninstaller import restore_dump_service


class TestRestoreDumpService(unittest.TestCase):
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('shutil.rmtree')
    @patch('os.remove')
    @patch('tarfile.open')
    @patch('subprocess.run')
    def test_restore_dump_service(self, mock_subprocess_run, mock_tarfile_open, mock_remove, mock_rmtree, mock_isdir, mock_listdir):
        # Setup the mocks
        mock_listdir.return_value = ['dump_test.tar.gz']
        mock_isdir.side_effect = lambda d: d in ["/var/ion-work/db/adnl", "/var/ion-work/db/archive"]
        mock_tar = MagicMock()
        mock_tarfile_open.return_value.__enter__.return_value = mock_tar
        
        # Call the function
        restore_dump_service()
        
        # Assert that the subprocess run calls are correct
        mock_subprocess_run.assert_any_call(["systemctl", "stop", "validator"])
        mock_subprocess_run.assert_any_call(["systemctl", "start", "validator"])
        
        # Assert that the dump file was found and processed
        mock_listdir.assert_called_once_with("/var/ion-work")
        
        # Assert that the directories were checked and deleted
        self.assertEqual(mock_isdir.call_count, 7)  # Should check all 7 directories
        mock_rmtree.assert_any_call("/var/ion-work/db/adnl")
        mock_rmtree.assert_any_call("/var/ion-work/db/archive")
        
        # Assert that the tarfile was opened and extracted
        mock_tarfile_open.assert_called_once_with("/var/ion-work/dump_test.tar.gz", "r:gz")
        mock_tar.extractall.assert_called_once_with(path="/var/ion-work/db")
        
        # Assert that the dump file was removed after extraction
        mock_remove.assert_called_once_with("/var/ion-work/dump_test.tar.gz")

if __name__ == '__main__':
    unittest.main()
