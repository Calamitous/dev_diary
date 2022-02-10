import dev_diary.protos.diary_pb2 as diary_pb


Activity = {
    "meeting": 0,
    "pairing": 1,
    "solo": 2,
    "downtime": 3,
    "administrivia": 4,
    "other": 5,
    "empty": 6,
}

ActivityNames = list(Activity.keys())


class Entry:
    def __init__(self, entry_dict):
        self.start = entry_dict["start"]
        self.duration = entry_dict["duration"]
        self.activity = entry_dict["activity"]
        self.text = entry_dict["text"]

    def activity_name(self):
        return ActivityNames[self.activity]

    def to_pb(self):
        entry_pb = diary_pb.Entry()

        entry_pb.start = self.start
        entry_pb.duration = self.duration
        entry_pb.activity = Activity[self.activity]
        entry_pb.text = self.text

        return entry_pb

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

    def to_pb_str(self):
        return self.to_pb().SerializeToString()

    @classmethod
    def empty(cls):
        return cls.activity_line("empty")

    @classmethod
    def activity_line(cls, activity_string):
        entry_dict = {
            "start": "",
            "duration": 0,
            "activity": Activity[activity_string],
            "text": "",
        }

        return cls(entry_dict)

    @classmethod
    def from_pb(cls, entry_pb):
        entry_dict = {
            "start": entry_pb.start,
            "duration": entry_pb.duration,
            "activity": entry_pb.activity,
            "text": entry_pb.text,
        }

        return cls(entry_dict)

    def __repr__(self):
        fmt_str = "\nEntry:\n  start: {}\n  duration: {}\n  activity: {}\n  text: {}"
        return fmt_str.format(self.start, self.duration, self.activity, self.text)
