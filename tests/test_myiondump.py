import unittest
from unittest.mock import patch, mock_open, MagicMock
from myiondump import create_dump_service
from datetime import datetime, timedelta
import time

class TestCreateDumpService(unittest.TestCase):
    
    @patch('myiondump.os.chdir')
    @patch('myiondump.subprocess.run')
    @patch('myiondump.tarfile.open')
    @patch('myiondump.shutil.copyfile')
    @patch('myiondump.requests.post')
    @patch('builtins.open', new_callable=mock_open)
    @patch('myiondump.os.remove')
    @patch('myiondump.time.sleep', side_effect=lambda x: None)  # to avoid actual sleep during tests
    def test_create_dump_service(self, mock_sleep, mock_remove, mock_open, mock_requests_post, mock_copyfile, mock_tarfile_open, mock_run, mock_chdir):
        source_dir = "/fake/source/dir"
        upload_url = "http://fakeurl.com/upload"
        period = 10  # seconds
        
        mock_tarfile = MagicMock()
        mock_tarfile_open.return_value.__enter__.return_value = mock_tarfile
        mock_requests_post.return_value.status_code = 200
        
        start_time = datetime.now()
        period_delta = timedelta(seconds=period)
        
        # Simulate a short run of the loop
        with patch('myiondump.datetime') as mock_datetime:
            mock_datetime.now.side_effect = [
                start_time,
                start_time + timedelta(seconds=5),  # midway through the sleep period
                start_time + timedelta(seconds=period + 5),  # after the sleep period
                start_time + timedelta(seconds=period + 10),  # after the sleep period again
            ]
            create_dump_service(source_dir, upload_url, period)

        # Assertions to check if the function behaves as expected
        mock_chdir.assert_called_with(source_dir)
        mock_run.assert_any_call(["systemctl", "stop", "validator"], check=True)
        mock_run.assert_any_call(["systemctl", "start", "validator"], check=True)
        mock_tarfile_open.assert_called_once_with(f"/tmp/dump_{start_time.strftime('%Y-%m-%d_%H-%M-%S')}.tar.gz", "w:gz")
        mock_copyfile.assert_called_once()
        mock_requests_post.assert_called()
        mock_remove.assert_called_once()

if __name__ == '__main__':
    unittest.main()
