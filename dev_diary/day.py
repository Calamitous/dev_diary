import dev_diary.protos.diary_pb2 as diary_pb
from dev_diary.util import Util

from dev_diary.entry import Entry, Activity


class Day:
    def __init__(self, date, entries):
        self.date = date
        self.entries = entries
        self.selected_entry_index = 0

    def quarter_to_index(hour, quarter, time_string):
        return 0

    @classmethod
    def create_today(cls):
        return Day(Util.today(), [])

    def line_is_selected_entry(self, hour, quarter, time_string):
        if len(self.entries) == 0:
            return False

        entry = self.selected_entry()
        return entry.line_is_entry(hour, quarter, time_string)

    def selected_entry(self):
        if len(self.entries) == 0:
            return None

        return self.entries[self.selected_entry_index]

    # TODO: Refactor this
    def lines(self):
        line_values = []

        activity = Activity["empty"]

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
                    "text": entry.text,
                    "activity": entry.activity_name(),
                    "selected": current_entry_selection,
                }
                line_values.append(new_line)

        return line_values

    def next_entry(self):
        self.selected_entry_index = min(
            len(self.entries) - 1, self.selected_entry_index + 1
        )

    def previous_entry(self):
        self.selected_entry_index = max(0, self.selected_entry_index - 1)

    def entry_for_line(self, hour, quarter, time_string):
        entries = self.entries
        data = [entry for entry in entries if time_string == entry.start]

        if len(data) == 1:
            return data[0]

        data = [
            entry
            for entry in entries
            if entry.line_is_entry(hour, quarter, time_string)
        ]

        if len(data) == 1:
            return Entry.activity_line(data[0].activity_name())

        return Entry.empty()

    def to_pb(self):
        day_pb = diary_pb.Day()

        day_pb.date = self.date

        entries_pb = [Entry(entry).to_pb() for entry in self.entries]
        day_pb.entries.extend(entries_pb)

        return day_pb

    def to_pb_str(self):
        return self.to_pb().SerializeToString()

    @classmethod
    def from_pb(cls, day_pb):
        entries = [Entry.from_pb(entry) for entry in day_pb.entries]
        return cls(day_pb.date, entries)

    def __repr__(self):
        fmt_str = "\nDay:\n  date: {}\n  entries:\n    {}"
        return fmt_str.format(self.date, self.entries)
