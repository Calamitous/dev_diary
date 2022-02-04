import curses
import sys

from diary import Diary
from help import help_text
from interface import Interface, Pop
from screen import Screen
from util import Util


def main(stdscr):
    interface = Interface(stdscr)

    if Diary.is_file_missing():
        Pop.message("No diary file found, creating...")
        Diary.create_file()

    diary = Diary.load()

    SINGLE_COMMANDS = {
        'g': diary.newest_day,
        'G': diary.oldest_day,
        'K': diary.previous_day,
        'k': diary.previous_entry,
        'J': diary.next_day,
        'j': diary.next_entry,
    }

    while(True):
        interface.print_display(diary)

        c = stdscr.getkey()

        if c in SINGLE_COMMANDS:
            SINGLE_COMMANDS[c].__call__()
        else:
            if c == 'p':
                Pop.message("foo bar baz quux")
            if c == 'd':
                Pop.message(diary.debug())
            # if c == curses.KEY_RESIZE:
                # Pop.message("RESIZED")
            if c == '?':
                Pop.message(help_text())
            if c == 'q':
                break
            # else:
                # Pop.message("Unrecognized command: {}".format(str(c)))

    Screen.stop_curses(stdscr)

if __name__ == '__main__':
    sys.exit(curses.wrapper(main))
