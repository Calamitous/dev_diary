import dev_diary.protos.diary_pb2 as diary_pb

Activity = {
    "meeting": 0,
    "pairing": 1,
    "solo": 2,
    "downtime": 3,
    "administrivia": 4,
    "other": 5,
}


class Entry:
    def __init__(self, entry_dict):
        self.start = entry_dict["start"]
        self.duration = entry_dict["duration"]
        self.activity = entry_dict["activity"]
        self.text = entry_dict["text"]

    def to_pb(self):
        entry_pb = diary_pb.Entry()

        entry_pb.start = self.start
        entry_pb.duration = self.duration
        entry_pb.activity = Activity[self.activity]
        entry_pb.text = self.text

        return entry_pb

    def to_pb_str(self):
        return self.to_pb().SerializeToString()

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
        fmt_str = "Entry:\n  start: {}\n  duration: {}\n  activity: {}\n  text: {}"
        return fmt_str.format(self.start, self.duration, self.activity, self.text)
