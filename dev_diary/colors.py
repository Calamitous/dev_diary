import curses

from enum import Enum


class Colors:
    DEFAULT = 0
    ENTRIES = {
        "administrivia": 1,
        "downtime": 2,
        "empty": 3,
        "meeting": 4,
        "pairing": 5,
        "solo": 6,
    }
    INFO = 7
    WARN = 8
    ERROR = 9
    FATAL = 10
    BUTTON = 11
    TIME = 12
    DATE = 13
    FIELD = 14
    SELECTED_FIELD = 14
    HELPBAR = 15

    @classmethod
    def initialize_color_pairs(cls):
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

        curses.init_pair(cls.INFO, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(cls.WARN, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(cls.ERROR, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(cls.FATAL, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(cls.BUTTON, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(cls.TIME, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(cls.DATE, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(cls.FIELD, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(cls.SELECTED_FIELD, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(cls.HELPBAR, curses.COLOR_BLACK, curses.COLOR_GREEN)
