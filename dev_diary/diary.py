import sys
import json

from os.path import exists
from pathlib import Path

from dev_diary.util import Util
from dev_diary.entry import Entry
from dev_diary.day import Day
from dev_diary.config import Config

import dev_diary.protos.diary_pb2 as diary_pb


class Diary:
    if len(sys.argv) >= 2:
        FILENAME = sys.argv[1]
    else:
        FILENAME = "./dev.diary"

    @classmethod
    def is_file_missing(cls):
        return not exists(cls.FILENAME)

    @classmethod
    def create_file(self):
        first_entry = {Util.today(): []}
        with open(self.FILENAME, "w") as diary_file:
            diary_file.write(json.dumps(first_entry))

    def __init__(self, config, days):
        self.config = config
        self.days = days
        self.selected_day_index = 0

    def to_pb(self):
        diary_pb_data = diary_pb.Diary()

        diary_pb_data.config.CopyFrom(Config.c_to_pb())

        days_struct = [{"date": date, "entries": self.days[date]} for date in self.days]
        days_pb = [Day(day).to_pb() for day in days_struct]

        diary_pb_data.days.extend(days_pb)

        return diary_pb_data

    def to_pb_str(self):
        return self.to_pb().SerializeToString()

    @classmethod
    def from_pb(cls, diary_pb):
        config = Config.from_pb(diary_pb.config)
        days = [Day.from_pb(day) for day in diary_pb.days]

        return cls(config, days)

    def __repr__(self):
        fmt_str = "\nDiary:\n  config:\n    {}\n  days:\n    {}"
        return fmt_str.format(self.config, self.days)

    def write(self):
        with open(self.FILENAME, "wb") as dump:
            dump.write(self.to_pb_str())

    def read():
        undump = open(Diary.FILENAME, "rb").read()
        diary = diary_pb.Diary()
        diary.ParseFromString(undump)
        return Diary.from_pb(diary)

    def debug(self):
        return str(self.selected_day_entries())

    def entry_dates(self):
        dates = [day.date for day in self.days]
        return list(sorted(dates, reverse=True))

    def day_count(self):
        return len(self.days)

    def max_day_index(self):
        return self.day_count() - 1

    def selected_date(self):
        return self.entry_dates()[self.selected_day_index]

    def selected_day(self):
        return self.days[self.selected_day_index]

    def selected_day_entries(self):
        return self.selected_day().entries

    def earliest_time_for_selected_day(self):
        entries = self.selected_day_entries()

        # If there are no entries, return EOD so that body_pad scrolls to default BOD
        # Basically, day never started
        if len(entries) == 0:
            return "23:45"

        return min([entry.start for entry in entries])

    def next_day(self):
        if self.selected_day_index < self.max_day_index():
            self.selected_day_index += 1
            self.selected_entry_index = 0

    def entry_line_count(self):
        return len(self.selected_day_entries())

    def previous_entry(self):
        self.selected_day().previous_entry()

    def next_entry(self):
        self.selected_day().next_entry()

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
