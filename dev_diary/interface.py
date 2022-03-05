import curses
import curses.textpad

from dev_diary.colors import Colors
from dev_diary.config import Config
from dev_diary.form import Form
from dev_diary.pop import Pop
from dev_diary.screen import Screen
from dev_diary.util import Util

from dev_diary.debug import log


class Interface:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        Screen.init_curses(self.stdscr)
        self.header_win = self.create_header()
        self.footer_win = self.create_footer()

    def create_header(diary):
        header_win = curses.newwin(1, curses.COLS, 0, 0)
        header_win.bkgdset(" ", curses.color_pair(Colors.BUTTON))
        return header_win

    def write_header(self):
        header_text = " Dev Diary v{}".format(Config.VERSION)
        self.header_win.clear()
        self.header_win.addstr(0, 0, header_text)
        self.header_win.noutrefresh()

    def create_footer(diary):
        footer_win = curses.newwin(1, curses.COLS, Screen.max_y(), 0)
        footer_win.bkgdset(" ", curses.color_pair(Colors.BUTTON))
        return footer_win

    def write_footer(self):
        footer_text = "Press '?' for help"
        self.footer_win.clear()
        self.footer_win.addstr(0, 0, footer_text)
        self.footer_win.noutrefresh()

    def write_day_list(self, diary):
        line_height = max(diary.day_count() + 1, curses.LINES - 2)

        # 12 columns wide for the full date + 2 spaces padding
        day_list = curses.newpad(line_height, 12)
        day_list.bkgdset(" ", curses.color_pair(Colors.INFO))

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

    def add_entry(self, stdscr, diary):
        # TODO: Select first open time after day start for default_time
        default_time = "09:00"
        do_add, data = Form.add_form(stdscr, diary.selected_day(), default_time, True)
        if do_add:
            # Validation?  Or push to Form?
            diary.create_entry(data)

    @classmethod
    def pad_line(cls, text):
        max = cls.max_entry_width()
        if len(text) > max:
            text = text[: (max - 4)] + "..."

        text = (text + (" " * max))[: max - 1]
        return text

    @classmethod
    def max_entry_width(cls):
        # Width - Date column - Time column
        return curses.COLS - 12 - 7

    def write_entry_panel(self, diary):
        # TODO: Figure out how to show empty days

        lines = diary.selected_day().lines()
        # 24 hours x 4 15-minute increments
        # max theoretical body height = 24 * 4 + 1
        body_height = len(lines)

        # Remaining width of screen wide by the max length
        body_pad = curses.newpad(body_height, curses.COLS - 12)
        body_pad.bkgdset(" ", curses.color_pair(Colors.DEFAULT))

        body_pad.clear()

        body_idx = 0
        for line in lines:
            display_time = " {} ".format(line["time"])
            display_line = self.pad_line(line["text"])

            body_pad.move(body_idx, 0)

            if line["selected"]:
                body_pad.addstr(
                    display_time,
                    curses.color_pair(Colors.TIME) + curses.A_REVERSE,
                )
                body_pad.move(body_idx, 7)
                body_pad.addstr(
                    display_line,
                    curses.color_pair(Colors.ENTRIES[line["activity"]])
                    + curses.A_REVERSE,
                )
            else:
                body_pad.addstr(display_time, curses.color_pair(Colors.TIME))
                body_pad.move(body_idx, 7)
                body_pad.addstr(
                    display_line, curses.color_pair(Colors.ENTRIES[line["activity"]])
                )

            body_idx += 1

        start_index = min(
            Config.start_time_index(),
            Util.time_string_to_index(diary.earliest_time_for_selected_day()),
        )
        body_pad.noutrefresh(start_index, 0, 1, 12, curses.LINES - 2, curses.COLS)

    def print_display(self, diary):
        curses.update_lines_cols()
        self.stdscr.clear()
        # TODO: Figure out this refresh nonsense
        self.stdscr.refresh()

        self.write_header()
        self.write_footer()

        self.write_day_list(diary)
        self.write_entry_panel(diary)
        curses.doupdate()
