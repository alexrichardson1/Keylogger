import unittest
from unittest.mock import MagicMock
import logger as Log
from pynput.keyboard import Key


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Log.Keylogger(
            Log.EMAIL_ADDRESS,
            Log.EMAIL_PASSWORD,
            Log.SEND_REPORT_EVERY,
            Log.SECRET,
            MagicMock())

    def test_update_log(self):
        self.logger.update_log("a")
        self.assertEqual(self.logger.log, "a")

    def test_on_release(self):
        self.logger.on_release("'a'")
        self.assertEqual(self.logger.log, "a")

    def test_on_release_special_key(self):
        log = ""
        logger = self.logger
        ks = logger.ks
        for special_key in ks.keys():
            log += ks[special_key]
            logger.on_release(special_key)
            self.assertEqual(logger.log, log)

    def test_encrypt_log(self):
        self.logger.on_release("a")
        self.assertNotEqual(self.logger.encrypt_log(), self.logger.log)

    def mock_send_email(self, message):
        mock_server = self.logger.server
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with(
            self.logger.email, self.logger.password)
        mock_server.sendmail.assert_called_once_with(
            self.logger.email, self.logger.email, message)
        mock_server.quit.assert_called_once()

    def test_send_email_text(self):
        message = "hello world"
        self.logger.send_email(message)
        self.mock_send_email(message)

    def test_send_keys_empty_log(self):
        message = ""
        self.logger.send_keys()

        mock_server = self.logger.server
        mock_server.starttls.assert_not_called()
        mock_server.login.assert_not_called()
        mock_server.sendmail.assert_not_called()
        mock_server.quit.assert_not_called()

    def test_send_email_image(self):
        mock_screenshot = MagicMock()
        self.logger.send_email(mock_screenshot)
        self.mock_send_email(mock_screenshot)
        mock_screenshot.close()


if __name__ == '__main__':
    unittest.main()
