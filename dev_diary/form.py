import curses
import curses.textpad
from math import floor, ceil

from dev_diary.colors import Colors
from dev_diary.entry import Entry

from dev_diary.debug import log


class Form:
    def __init__(self, scr, selected_day, entry, new_record=True):
        self.scr = scr
        self.entry = entry
        self.date = selected_day.date

        self.is_new_record = new_record

        self.width = curses.COLS
        self.height = curses.LINES
        self.label_area_width = floor(self.width / 3)
        self.field_area_width = floor(self.width / 3) * 2

        self.current_field_idx = 0

        self.date_win = self.create_date_win()
        self.helpbar_win = self.create_helpbar_win()

        self.labels = [
            [self.create_label(1), "Start Time:"],
            [self.create_label(4), "Duration:"],
            [self.create_label(7), "Activity:"],
            [self.create_label(10), "Text:"],
        ]

        self.fields = [
            [
                self.create_field(1),
                self.write_time_field_win,
                'Enter time as "XX:YY" or "XXYY".',
            ],
            [
                self.create_field(4),
                self.write_duration_field_win,
                "Press + or - to increment or decrement duration.",
            ],
            [
                self.create_field(7),
                self.write_activity_field_win,
                "Press + or - to select activity.",
            ],
            [
                self.create_field(10),
                self.write_text_field_win,
                "Add details of what you did here.  Press Enter to exit.",
            ],
        ]

        self.text_input = curses.textpad.Textbox(self.scr)
        # text = textpad.edit(Form.textbox_key_handler)

        self.life_loop()

    def print_display(self):
        self.scr.clear()
        self.scr.refresh()

        self.write_date_win()
        self.write_helpbar_win()

        [self.write_label(label) for label in self.labels]
        [field[1].__call__(field[0]) for field in self.fields]

        curses.doupdate()

    def create_label(self, y_start):
        label = curses.newwin(3, self.label_area_width, y_start, 0)
        label.bkgdset(" ", curses.color_pair(Colors.BUTTON))
        return label

    def write_label(self, label_data):
        label_win, label_text = label_data
        label_win.clear()
        label_win.addstr(1, self.label_area_width - len(label_text), label_text)
        label_win.noutrefresh()

    def create_field(self, y_start):
        duration_field = curses.newwin(
            3, self.field_area_width, y_start, self.label_area_width
        )
        duration_field.bkgdset(" ", curses.color_pair(Colors.BUTTON))
        return duration_field

    def write_field(self, field, text):
        if self.fields[self.current_field_idx][0] == field:
            color = curses.A_REVERSE + curses.color_pair(Colors.FIELD)
        else:
            color = curses.color_pair(Colors.FIELD)

        field.clear()
        field.addstr(1, 1, text, color)
        field.noutrefresh()

    def create_date_win(self):
        date_win = curses.newwin(1, self.width, 0, 0)
        date_win.bkgdset(" ", curses.color_pair(Colors.DATE))
        return date_win

    def write_date_win(self):
        self.date_win.clear()
        self.date_win.addstr(0, 0, "Adding entry for {}".format(self.date))
        self.date_win.noutrefresh()

    def create_helpbar_win(self):
        helpbar_win = curses.newwin(1, self.width, self.height - 1, 0)
        helpbar_win.bkgdset(" ", curses.color_pair(Colors.HELPBAR))
        return helpbar_win

    def write_helpbar_win(self):
        self.helpbar_win.clear()
        self.helpbar_win.addstr(0, 0, self.fields[self.current_field_idx][2])
        self.helpbar_win.noutrefresh()

    def write_time_field_win(self, field):
        self.write_field(field, self.entry.start)

    def write_duration_field_win(self, field):
        self.write_field(field, self.entry.duration_text())

    def write_activity_field_win(self, field):
        self.write_field(field, self.entry.activity_name().capitalize())

    def write_text_field_win(self, field):
        # TODO: Make this a TextBox?
        self.write_field(field, self.entry.text_display(self.field_area_width - 2))

    def life_loop(self):
        in_form = True

        while in_form:
            self.print_display()

            ch = self.scr.getkey()

            # if ch == "	":
            #     log("TABBED")
            #     self.text_input.edit(Form.textbox_key_handler)

            # Escape
            if ch == "":
                in_form = False
            if ch == "	":
                self.current_field_idx += 1
                if self.current_field_idx > len(self.fields) - 1:
                    self.current_field_idx = 0
            if ch == curses.KEY_BTAB:
                self.current_field_idx -= 1
                if self.current_field_idx < 0:
                    self.current_field_idx = len(self.fields) - 1
        #     # else:
        #         Pop.message("Unrecognized command: {}".format(str(c)))

    def textbox_key_handler(ch):
        # Enter
        if ch == 10:
            return 7  # Ctrl-G, ie. "Save and exit"
        else:
            return ch

    @staticmethod
    def add_form(stdscr, selected_day, default_time, new_record=True):
        form = Form(stdscr, selected_day, Entry.new_entry(), True)

        return True, form.entry
