from dev_diary.util import Util
import dev_diary.protos.diary_pb2 as diary_pb


class Config:
    VERSION = "0.02"
    START_TIME = "09:00"

    @classmethod
    def start_time_index(cls):
        return Util.time_string_to_index(cls.START_TIME)

    def to_pb(self):
        config_pb = diary_pb.Config()

        config_pb.file_format_version = self.VERSION
        config_pb.start_time = self.START_TIME

        return config_pb

    def to_pb_str(self):
        return self.to_pb().SerializeToString()
