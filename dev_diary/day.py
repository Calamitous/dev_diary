import dev_diary.protos.diary_pb2 as diary_pb
from dev_diary.debug import log

from dev_diary.entry import Entry

class Day:
    def __init__(self, day_dict):
        self.date = day_dict["date"]
        self.entries = day_dict["entries"]

    def to_pb(self):
        day_pb = diary_pb.Day()

        day_pb.date = self.date

        entries_pb = [Entry(entry).to_pb() for entry in self.entries]
        # TODO: START: Figure out why this isn't working
        log(">>>>>>>>>>>>>>>>>>>>>>>>")
        log(entries_pb)
        log("<<<<<<<<<<<<<<<<<<<<<")
        day_pb.entries.extend(self.entries)

        return day_pb

    def to_pb_str(self):
        return self.to_pb().SerializeToString()
