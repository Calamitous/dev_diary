import curses
import os
import sys

from dev_diary.diary import Diary
from dev_diary.help import help_text
from dev_diary.interface import Interface, Pop
from dev_diary.screen import Screen


def main(stdscr):
    interface = Interface(stdscr)

    if Diary.is_file_missing():
        Pop.message("No diary file found, creating...")
        Diary.create_file()

    diary = Diary.read()

    SINGLE_COMMANDS = {
        "g": diary.newest_day,
        "G": diary.oldest_day,
        "K": diary.previous_day,
        "k": diary.previous_entry,
        "J": diary.next_day,
        "j": diary.next_entry,
        "	": diary.next_entry,
        curses.KEY_BTAB: diary.next_entry,
        "w": diary.write,
        "r": diary.read,
    }

    while True:
        interface.print_display(diary)

        c = stdscr.getkey()

        if c in SINGLE_COMMANDS:
            SINGLE_COMMANDS[c].__call__()
        else:
            if c == "p":
                Pop.message("foo bar baz quux")
            if c == "d":
                filename = diary.dump_debug_file()
                Pop.message(filename)
            # if c == curses.KEY_RESIZE:
            # Pop.message("RESIZED")
            if c == "a":
                interface.add_entry(stdscr, diary)
            if c == "?":
                Pop.message(help_text())
            # if c == curses.KEY_DOWN:
            # diary.next_day
            if c == "q":
                break
            # else:
            # Pop.message("Unrecognized command: {}".format(str(c)))

    Screen.stop_curses(stdscr)


if __name__ == "__main__":
    # Eliminate long delay when pressing Esc (1000ms to 25ms)
    os.environ.setdefault("ESCDELAY", "25")

    sys.exit(curses.wrapper(main))
