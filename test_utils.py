import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from utils.error_handler import get_recent_errors, report_error
from utils.retry import retry_call
from utils.validation import human_readable_size, validate_upload


class DummyUpload:
    def __init__(self, name, size, content_type=''):
        self.name = name
        self.size = size
        self.type = content_type


class RetryTests(unittest.TestCase):
    def test_retry_call_succeeds_after_transient_failures(self):
        calls = {'count': 0}

        def flaky():
            calls['count'] += 1
            if calls['count'] < 3:
                raise ValueError('transient')
            return 'ok'

        with mock.patch('utils.retry.time.sleep') as sleep_mock:
            result = retry_call(flaky, tries=3, delay=0.1, backoff=2.0)

        self.assertEqual(result, 'ok')
        self.assertEqual(calls['count'], 3)
        self.assertEqual(sleep_mock.call_count, 2)

    def test_retry_call_raises_last_exception_when_exhausted(self):
        calls = {'count': 0}

        def always_fail():
            calls['count'] += 1
            raise RuntimeError('boom')

        with mock.patch('utils.retry.time.sleep') as sleep_mock:
            with self.assertRaises(RuntimeError):
                retry_call(always_fail, tries=2, delay=0.1, backoff=2.0)

        self.assertEqual(calls['count'], 2)
        self.assertEqual(sleep_mock.call_count, 1)


class ValidationTests(unittest.TestCase):
    def test_validate_upload_accepts_supported_audio(self):
        file_obj = DummyUpload('lecture.mp3', 10 * 1024 * 1024, 'audio/mpeg')

        valid, message = validate_upload(file_obj)

        self.assertTrue(valid)
        self.assertEqual(message, '')

    def test_validate_upload_rejects_oversized_document(self):
        file_obj = DummyUpload('slides.pdf', 60 * 1024 * 1024, 'application/pdf')

        valid, message = validate_upload(file_obj, max_doc_mb=50)

        self.assertFalse(valid)
        self.assertIn('Document too large', message)

    def test_validate_upload_rejects_unknown_file_type(self):
        file_obj = DummyUpload('notes.txt', 1024, 'text/plain')

        valid, message = validate_upload(file_obj)

        self.assertFalse(valid)
        self.assertIn('Unsupported file type', message)

    def test_human_readable_size(self):
        self.assertEqual(human_readable_size(1023), '1023.0B')
        self.assertEqual(human_readable_size(1024), '1.0KB')


class ErrorHandlerTests(unittest.TestCase):
    def test_report_error_writes_json_log_and_get_recent_errors_reads_it(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)

            def fake_ensure_log_dir():
                return tmp_path

            try:
                1 / 0
            except Exception as exc:
                with mock.patch('utils.error_handler._ensure_log_dir', side_effect=fake_ensure_log_dir):
                    result = report_error(exc, context='during unit test', user_facing=False)
                    errors = get_recent_errors(limit=10)

            self.assertIn('Reference ID', result['message'])
            log_path = tmp_path / 'errors.log'
            self.assertTrue(log_path.exists())

            lines = log_path.read_text(encoding='utf-8').strip().splitlines()
            self.assertEqual(len(lines), 1)

            record = json.loads(lines[0])
            self.assertEqual(record['context'], 'during unit test')
            self.assertIn('division by zero', record['message'])

            self.assertEqual(len(errors), 1)
            self.assertEqual(errors[0]['context'], 'during unit test')

    def test_get_recent_errors_ignores_legacy_lines(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / 'errors.log').write_text(
                'legacy line\n'
                + json.dumps({'id': '1', 'timestamp': '2026-05-12T10:00:00Z', 'context': 'a', 'message': 'x', 'traceback': 'tb'})
                + '\n',
                encoding='utf-8'
            )

            with mock.patch('utils.error_handler._ensure_log_dir', return_value=tmp_path):
                errors = get_recent_errors(limit=10)

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['id'], '1')


if __name__ == '__main__':
    unittest.main()