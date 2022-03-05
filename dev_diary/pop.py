import curses

from math import floor, ceil
from textwrap import TextWrapper
from dev_diary.screen import Screen

from dev_diary.colors import Colors


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
        win.bkgdset(" ", curses.color_pair(color))

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
        win.addstr(button_text, curses.color_pair(Colors.BUTTON))

        win.refresh()
        return win.getkey()
