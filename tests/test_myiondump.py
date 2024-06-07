import unittest
from unittest.mock import patch, mock_open, MagicMock
from myiondump import create_dump_service
from datetime import datetime, timedelta
import os

class TestCreateDumpService(unittest.TestCase):

    @patch('myiondump.os.chdir')
    @patch('myiondump.subprocess.run')
    @patch('myiondump.tarfile.open')
    @patch('myiondump.shutil.copyfile')
    @patch('myiondump.os.remove')
    @patch('myiondump.time.sleep', side_effect=lambda x: None)  # to avoid actual sleep during tests
    def test_create_dump_service(self, mock_sleep, mock_remove, mock_copyfile, mock_tarfile_open, mock_run, mock_chdir):
        source_dir = "/fake/source/dir"
        backup_dir = "/fake/backup/dir"
        period = 10  # seconds

        # Setup the tarfile mock
        mock_tarfile = MagicMock()
        mock_tarfile_open.return_value.__enter__.return_value = mock_tarfile

        start_time = datetime.now()

        # Function to generate datetime values dynamically
        def generate_datetime_values(start, delta, count):
            current = start
            for _ in range(count):
                yield current
                current += delta

        # Calculate the required number of datetime values
        num_calls = 20  # Adjust based on the expected number of calls
        datetime_values = generate_datetime_values(start_time, timedelta(seconds=5), num_calls)

        # Simulate a short run of the loop
        with patch('myiondump.datetime') as mock_datetime:
            mock_datetime.now.side_effect = datetime_values
            with patch('builtins.open', mock_open(read_data='data')):
                create_dump_service(source_dir, backup_dir, period)

        # Assertions to check if the function behaves as expected
        mock_chdir.assert_called_with(source_dir)
        mock_run.assert_any_call(["systemctl", "stop", "validator"], check=True)
        mock_run.assert_any_call(["systemctl", "start", "validator"], check=True)
        archive_name = f"dump_{start_time.strftime('%Y-%m-%d_%H-%M-%S')}.tar.gz"
        mock_tarfile_open.assert_called_once_with(os.path.join(backup_dir, archive_name), "w:gz")
        mock_copyfile.assert_called_once_with(
            os.path.join(backup_dir, archive_name),
            os.path.join(backup_dir, "dump_latest.tar.gz")
        )
        mock_remove.assert_not_called()  # no removal in this case

if __name__ == '__main__':
    unittest.main()
