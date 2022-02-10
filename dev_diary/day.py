import dev_diary.protos.diary_pb2 as diary_pb

from dev_diary.entry import Entry


class Day:
    def __init__(self, day_dict):
        self.date = day_dict["date"]
        self.entries = day_dict["entries"]

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
        day_dict = {
            "date": day_pb.date,
            "entries": [Entry.from_pb(entry) for entry in day_pb.entries],
        }

        return cls(day_dict)

    def __repr__(self):
        fmt_str = "Day:\n  date: {}\n  entries:\n    {}"
        return fmt_str.format(self.date, self.entries)
