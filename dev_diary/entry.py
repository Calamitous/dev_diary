import dev_diary.protos.diary_pb2 as diary_pb
from math import floor


Activity = {
    "administrivia": 0,
    "downtime": 1,
    "meeting": 2,
    "pairing": 3,
    "solo": 4,
    "other": 5,
    "empty": 6,
}

ActivityNames = list(Activity.keys())


class Entry:
    def __init__(self, start, duration, activity, text):
        self.start = start
        self.duration = duration
        self.activity = activity
        self.text = text

    @classmethod
    def new_entry(cls):
        # TODO: Set start time to default start time
        return cls("09:00", 2, 0, "")

    def activity_name(self):
        return ActivityNames[self.activity]

    def duration_text(self):
        hours = floor(self.duration / 4)

        subs = self.duration % 4
        minutes = subs * 15

        if minutes > 0:
            minutes_text = "{} minutes".format(str(minutes))
        else:
            minutes_text = ""

        if hours > 0:
            if hours == 1:
                hours_text = "{} hour".format(str(hours))
            else:
                hours_text = "{} hours".format(str(hours))
        else:
            hours_text = ""

        return " ".join([hours_text, minutes_text]).strip()

    def text_display(self, width):
        padding = " " * width

        if len(self.text) > width:
            text = self.text[: width - 3] + "..."
        else:
            text = self.text

        return (text + padding)[:width]

    def to_pb(self):
        entry_pb = diary_pb.Entry()

        entry_pb.start = self.start
        entry_pb.duration = self.duration
        entry_pb.activity = self.activity
        entry_pb.text = self.text

        return entry_pb

    def to_pb_str(self):
        return self.to_pb().SerializeToString()

    # TODO: Refactor all this
    # TODO: Also, this is a terrible name
    def line_is_entry(self, hour, quarter, time_string):
        if time_string == self.start:
            return True

        test_time = (hour * 1000) + (quarter * 250)

        quarter_dict = {"00": 0, "15": 250, "30": 500, "45": 750}

        entry_hour, entry_quarter = self.start.split(":")
        entry_hour = int(entry_hour)
        entry_quarter = quarter_dict[entry_quarter]
        entry_duration = self.duration * 250

        entry_start_time = (entry_hour * 1000) + entry_quarter
        entry_end_time = entry_start_time + entry_duration - 1

        return entry_start_time <= test_time and entry_end_time >= test_time

    @classmethod
    def activity_line(cls, activity_string):
        return cls("", 0, Activity[activity_string], "")

    @classmethod
    def empty(cls):
        return cls.activity_line("empty")

    @classmethod
    def from_pb(cls, entry_pb):
        return cls(
            entry_pb.start,
            entry_pb.duration,
            entry_pb.activity,
            entry_pb.text,
        )

    def __repr__(self):
        fmt_str = "\nEntry:\n  start: {}\n  duration: {}\n  activity: {}\n  text: {}"
        return fmt_str.format(self.start, self.duration, self.activity, self.text)
