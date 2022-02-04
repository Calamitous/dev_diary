import json

from os.path import exists
from pathlib import Path

class Diary:
    FILENAME = './dev_diary.json'

    @classmethod
    def load(self):
        raw_entries = json.load(open(self.FILENAME))
        return self(raw_entries)


    @classmethod
    def is_file_missing(cls):
        return not exists(cls.FILENAME)


    @classmethod
    def create_file(self):
        first_entry = {Util.today(): {}}
        with open(self.FILENAME, "w") as diary_file:
            diary_file.write(json.dumps(first_entry))


    def __init__(self, days = {}):
        self.days = days
        self.selected_day_index = 0
        self.selected_entry_index = 0


    def debug(self):
        return str(self.selected_day_entries())


    def entry_dates(self):
        dates = self.days.keys()
        return list(sorted(dates, reverse=True))


    def day_count(self):
        return len(self.days.keys())


    def max_day_index(self):
        return self.day_count() - 1


    def selected_date(self):
        return self.entry_dates()[self.selected_day_index]


    def entry_lines(self):
        return self.days[self.selected_date()][self.selected_entry_index]


    def selected_day_entries(self):
        return self.days[self.selected_date()]


    def selected_entry(self):
        return self.days[self.selected_date()][self.selected_entry_index]


    def next_day(self):
        if self.selected_day_index < self.max_day_index():
            self.selected_day_index += 1
            self.selected_entry_index = 0


    def entry_line_count(self):
        return len(self.selected_day_entries())


    def previous_entry(self):
        self.selected_entry_index = max(0, self.selected_entry_index - 1)


    def next_entry(self):
        self.selected_entry_index = min(self.entry_line_count() - 1, self.selected_entry_index + 1)


    def previous_day(self):
        if self.selected_day_index > 0:
            self.selected_day_index = self.selected_day_index - 1
            self.selected_entry_index = 0


    def newest_day(self):
        self.selected_day_index = 0


    def oldest_day(self):
        self.selected_day_index = self.max_day_index()


    def last_entry(self):
        return self.selected_day_entries()[-1]
