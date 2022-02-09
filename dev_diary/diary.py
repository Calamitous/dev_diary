import json

from os.path import exists
from pathlib import Path

from dev_diary.util import Util
from dev_diary.entry import Entry


class Diary:
    FILENAME = "./dev_diary.json"

    @classmethod
    def load(self):
        raw_entries = json.load(open(self.FILENAME))
        # TODO: This
        # entries = [Entry(entry) for entry in raw_entries]
        # print(entries)
        return self(raw_entries)

    @classmethod
    def is_file_missing(cls):
        return not exists(cls.FILENAME)

    @classmethod
    def create_file(self):
        first_entry = {Util.today(): []}
        with open(self.FILENAME, "w") as diary_file:
            diary_file.write(json.dumps(first_entry))

    def __init__(self, days={}):
        self.days = days
        self.selected_day_index = 0
        self.selected_entry_index = 0

    def line_is_entry(self, hour, quarter, time_string, entry):
        if entry is None:
            return False

        if time_string == entry["start"]:
            return True

        test_time = (hour * 1000) + (quarter * 250)

        quarter_dict = {"00": 0, "15": 250, "30": 500, "45": 750}

        entry_hour, entry_quarter = entry["start"].split(":")
        entry_hour = int(entry_hour)
        entry_quarter = quarter_dict[entry_quarter]
        entry_duration = entry["duration"] * 250

        entry_start_time = (entry_hour * 1000) + entry_quarter
        entry_end_time = entry_start_time + entry_duration - 1

        return entry_start_time <= test_time and entry_end_time >= test_time

    def line_is_selected_entry(self, hour, quarter, time_string):
        entry = self.selected_entry()
        return self.line_is_entry(hour, quarter, time_string, entry)

    def entry_for_line(self, hour, quarter, time_string):
        entries = self.selected_day_entries()
        data = [entry for entry in entries if time_string == entry["start"]]
        if len(data) == 1:
            return data[0]

        data = [
            entry
            for entry in entries
            if self.line_is_entry(hour, quarter, time_string, entry)
        ]
        if len(data) == 1:
            return {"text": "", "type": data[0]["type"]}

        return {"text": "", "type": "empty"}

    def lines(self):
        line_values = []

        type = "empty"

        for hour in range(0, 23):
            hour_string = "0{}".format(hour)[-2:]
            for quarter in range(0, 4):
                minute_string = "0{}".format(quarter * 15)[-2:]
                time_string = "{}:{}".format(hour_string, minute_string)

                entry = self.entry_for_line(hour, quarter, time_string)

                current_entry_selection = self.line_is_selected_entry(
                    hour, quarter, time_string
                )

                new_line = {
                    "time": time_string,
                    "text": entry["text"],
                    "type": entry["type"],
                    "selected": current_entry_selection,
                }
                line_values.append(new_line)

        return line_values

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

    def selected_day_entries(self):
        return self.days[self.selected_date()]

    def selected_entry(self):
        if len(self.selected_day_entries()) == 0:
            return None

        return self.days[self.selected_date()][self.selected_entry_index]

    def earliest_time_for_selected_day(self):
        entries = self.selected_day_entries()

        # If there are no entries, return EOD so that body_pad scrolls to default BOD
        # Basically, day never started
        if len(entries) == 0:
            return "23:45"

        return min([entry["start"] for entry in entries])

    def next_day(self):
        if self.selected_day_index < self.max_day_index():
            self.selected_day_index += 1
            self.selected_entry_index = 0

    def entry_line_count(self):
        return len(self.selected_day_entries())

    def previous_entry(self):
        self.selected_entry_index = max(0, self.selected_entry_index - 1)

    def next_entry(self):
        self.selected_entry_index = min(
            self.entry_line_count() - 1, self.selected_entry_index + 1
        )

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
