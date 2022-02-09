import curses

from dev_diary.colors import Colors

from math import floor, ceil


class Screen:
    def init_curses(stdscr):
        if curses.LINES < 4 or curses.COLS < 24:
            stdscr.addstr("Screen too small!  Must be at least 24x4 characters")
            stdscr.getkey()
            exit(1)

        stdscr.clear()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)

        # Invisibilize cursor
        curses.curs_set(0)
        curses.use_default_colors()

        Colors.initialize_color_pairs()

    def stop_curses(stdscr):
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    @classmethod
    def screen_center(cls):
        # Curses uses [y, x] coordinates.  Nobody knows why.
        return [floor(cls.max_y() / 2), floor(cls.max_x() / 2)]

    def max_x():
        return curses.COLS - 2

    def max_y():
        return curses.LINES - 1
