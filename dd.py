import curses
import curses.textpad

import json
import sys
import datetime

from os.path import exists
from pathlib import Path
from math import floor, ceil
from enum import Enum

class Colors(Enum):
    DEFAULT = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    FATAL = 4
    BUTTON = 5


class Config:
    VERSION = "0.01"


def init_curses(stdscr):
    stdscr.clear()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    # Invisibilize cursor
    curses.curs_set(0)
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)


def stop_curses(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


def screen_center():
    # Curses uses [y, x] coordinates.  Nobody knows why.
    return [floor(max_y() / 2), floor(max_x() / 2)]


def max_x():
    return curses.COLS - 2


def max_y():
    return curses.LINES - 1


def text_dimensions(text):
    # box_height = len(text.split())
    box_height = 1
    box_width = len(text)
    return [box_height + 4, max(box_width + 4, 10)]

def pop_message(text, color = Colors.INFO):
    box_height, box_width = text_dimensions(text)
    center_y, center_x = screen_center()
    win_top = center_y - ceil(box_height / 2)
    win_left = center_x - ceil(box_width / 2)

    win = curses.newwin(box_height, box_width, win_top, win_left)
    win.bkgdset(' ', curses.color_pair(color.value))

    win.clear()
    win.border()

    win.move(ceil(box_height / 2) - 1, ceil(box_width / 2) - ceil(len(text) / 2))
    win.addstr(text)

    # Display button
    button_text = " < OK > "
    win.move(box_height - 1, ceil(box_width / 2) - ceil(len(button_text) / 2))
    win.addstr(button_text, curses.color_pair(Colors.BUTTON.value))

    win.refresh()
    return win.getkey()


def print_display(diary):
    header = " Dev Diary v{}".format(Config.VERSION)
    footer = "Press '?' for help"

    header_win = curses.newwin(1, curses.COLS, 0, 0)
    header_win.bkgdset(' ', curses.color_pair(Colors.BUTTON.value))
    header_win.clear()

    header_win.move(0, 0)
    header_win.addstr(header)

    footer_win = curses.newwin(1, curses.COLS, max_y(), 0)
    footer_win.bkgdset(' ', curses.color_pair(Colors.BUTTON.value))
    footer_win.clear()

    footer_win.move(0, 0)
    footer_win.addstr(footer)

    list_win = curses.newwin(curses.LINES - 2, 12, 1, 0)
    list_win.bkgdset(' ', curses.color_pair(Colors.INFO.value))
    list_win.clear()

    list_idx = 0
    for date in diary.entry_dates():
        # pop_message("idx: {}, date: {}".format(list_idx, date))
        list_win.move(list_idx, 0)
        if list_idx == diary.selected_index:
            list_win.addstr(" {} ".format(date), curses.A_REVERSE)
        else:
            list_win.addstr(" {} ".format(date))
        list_idx += 1


    body_win = curses.newwin(curses.LINES - 2, curses.COLS - 12, 1, 12)
    body_win.bkgdset(' ', curses.color_pair(Colors.DEFAULT.value))
    body_win.clear()

    header_win.noutrefresh()
    footer_win.noutrefresh()
    list_win.noutrefresh()
    body_win.noutrefresh()
    curses.doupdate()


class Util:
    @classmethod
    def today(self):
        return datetime.datetime.today().strftime("%Y-%m-%d")


class Diary:
    FILENAME = './dev_diary.json'

    @classmethod
    def load(self):
        return self(json.load(open(self.FILENAME)))

    @classmethod
    def create_file_if_not_exists(self):
        if exists(self.FILENAME):
            return

        pop_message("No diary file found, creating...")
        with open(self.FILENAME, "w") as diary_file:
            diary_file.write(json.dumps({
                Util.today(): {
                }
            }))


    def __init__(self, entries = []):
        self.entries = entries
        self.selected_index = 0

    def debug(self):
        pop_message(str(self.entries))

    def entry_dates(self):
        return list(self.entries.keys())

    def entry_count(self):
        return len(self.entries.keys()) - 1

    def next(self):
        if self.selected_index < self.entry_count():
            self.selected_index += 1

    def previous(self):
        if self.selected_index > 0:
            self.selected_index = self.selected_index - 1


def main(stdscr):
    init_curses(stdscr)

    Diary.create_file_if_not_exists()
    diary = Diary.load()

    while(True):
        stdscr.clear()
        stdscr.refresh()
        print_display(diary)

        c = stdscr.getkey()

        if c == 'p':
            pop_message("foo bar baz quux")
        if c == 'd':
            diary.debug()
        if c == 'K':
            diary.previous()
        if c == 'J':
            diary.next()
        if c == 'q':
            break

    stop_curses(stdscr)

if __name__ == '__main__':
    sys.exit(curses.wrapper(main))
