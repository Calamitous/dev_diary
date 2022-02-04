import curses

from colors import Colors
from config import Config
from screen import Screen
from math import floor, ceil
from textwrap import TextWrapper


class Pop:
    @staticmethod
    def max_text_length():
        return curses.COLS - 6

    @staticmethod
    def max_text_height():
        return curses.LINES - 4

    @classmethod
    def split_text(cls, text):
        if isinstance(text, list):
            return text[0 : cls.max_text_height()]
        else:
            return TextWrapper(
                width=cls.max_text_length(), max_lines=cls.max_text_height()
            ).wrap(text)

    @classmethod
    def text_dimensions(cls, lines):
        if len(lines) == 1:
            box_width = len(lines[0]) + 4
        else:
            box_width = cls.max_text_length() + 4

        box_height = min(len(lines), cls.max_text_height())
        return [box_height + 4, max(box_width, 10)]

    @classmethod
    def message(cls, text, color=Colors.INFO):
        lines = cls.split_text(text)

        box_height, box_width = cls.text_dimensions(lines)
        center_y, center_x = Screen.screen_center()
        win_top = center_y - floor(box_height / 2)
        win_left = center_x - floor(box_width / 2)

        win = curses.newwin(box_height, box_width, win_top, win_left)
        win.bkgdset(" ", curses.color_pair(color.value))

        win.clear()
        win.border()

        idx = floor(len(lines) / 2) * -1
        for line in lines:
            new_y = ceil(box_height / 2) - 1 + idx
            new_x = ceil(box_width / 2) - ceil(len(line) / 2)
            win.addstr(new_y, new_x, line)
            idx += 1

        # Display button
        button_text = " < OK > "
        win.move(box_height - 1, ceil(box_width / 2) - ceil(len(button_text) / 2))
        win.addstr(button_text, curses.color_pair(Colors.BUTTON.value))

        win.refresh()
        return win.getkey()


class Interface:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        Screen.init_curses(self.stdscr)
        self.header_win = self.create_header()
        self.footer_win = self.create_footer()

    def create_header(diary):
        header_win = curses.newwin(1, curses.COLS, 0, 0)
        header_win.bkgdset(' ', curses.color_pair(Colors.BUTTON.value))

        header_text = " Dev Diary v{}".format(Config.VERSION)
        header_win.clear()
        header_win.addstr(0, 0, header_text)

        return header_win


    def create_footer(diary):
        footer_win = curses.newwin(1, curses.COLS, Screen.max_y(), 0)
        footer_win.bkgdset(' ', curses.color_pair(Colors.BUTTON.value))

        footer_text = "Press '?' for help"
        footer_win.clear()
        footer_win.addstr(0, 0, footer_text)

        return footer_win


    def write_day_list(self, diary):
        line_height = max(diary.day_count() + 1, curses.LINES - 2)

        # 12 columns wide for the full date + 2 spaces padding
        day_list = curses.newpad(line_height, 12)
        day_list.bkgdset(' ', curses.color_pair(Colors.INFO.value))

        day_list.clear()

        list_idx = 0
        for date in diary.entry_dates():
            day_list.move(list_idx, 0)
            if list_idx == diary.selected_day_index:
                day_list.addstr(" {} ".format(date), curses.A_REVERSE)
            else:
                day_list.addstr(" {} ".format(date))
            list_idx += 1

        day_list.noutrefresh(0, 0, 1, 0, curses.LINES - 2, 12)

    def write_entry_panel(self, diary):
        # 24 hours x 4 15-minute increments
        # max theoretical body height = 24 * 4 + 1
        body_height = diary.entry_line_count()

        # Remaining width of screen wide by the max length
        body_pad = curses.newpad(body_height, curses.COLS - 12)
        body_pad.bkgdset(' ', curses.color_pair(Colors.DEFAULT.value))
        body_pad.clear()

        body_idx = 0
        for entry in diary.selected_day_entries():
            body_pad.move(body_idx, 0)

            display_line = str(entry)

            if entry == diary.selected_entry():
                body_pad.addstr(display_line, curses.A_REVERSE)
            else:
                body_pad.addstr(display_line)

            body_idx += 1

        body_pad.noutrefresh(0, 0, 1, 12, curses.LINES - 2, curses.COLS - 12)

    def print_display(self, diary):
        curses.update_lines_cols()
        # self.stdscr.clear()
        # TODO: START: Figure out this refresh nonsense
        self.stdscr.refresh()

        self.header_win.noutrefresh()
        self.footer_win.noutrefresh()

        self.write_day_list(diary)
        self.write_entry_panel(diary)
        curses.doupdate()
