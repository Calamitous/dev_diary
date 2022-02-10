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

        return entry_pb.SerializeToString()
