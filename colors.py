import curses

from enum import Enum


class Colors:
    DEFAULT = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    FATAL = 4
    BUTTON = 5
    TIME = 6
    ENTRIES = {
        "administrivia": 7,
        "downtime": 8,
        "empty": 9,
        "meeting": 10,
        "pairing": 11,
        "solo": 12,
    }

    @classmethod
    def initialize_color_pairs(cls):
        curses.init_pair(cls.INFO, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(cls.WARN, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(cls.ERROR, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(cls.FATAL, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(cls.BUTTON, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(cls.TIME, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(cls.TIME, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(
            cls.ENTRIES["administrivia"], curses.COLOR_WHITE, curses.COLOR_BLUE
        )
        curses.init_pair(
            cls.ENTRIES["downtime"], curses.COLOR_WHITE, curses.COLOR_MAGENTA
        )
        curses.init_pair(cls.ENTRIES["empty"], curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(
            cls.ENTRIES["meeting"], curses.COLOR_BLACK, curses.COLOR_YELLOW
        )
        curses.init_pair(cls.ENTRIES["pairing"], curses.COLOR_RED, curses.COLOR_CYAN)
        curses.init_pair(cls.ENTRIES["solo"], curses.COLOR_WHITE, curses.COLOR_GREEN)
