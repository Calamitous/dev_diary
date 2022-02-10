from dev_diary.util import Util
import dev_diary.protos.diary_pb2 as diary_pb


class Config:
    VERSION = "0.02"
    DEFAULT_START_TIME = "09:00"

    def __init__(self, start_time, file_format_version):
        self.start_time = start_time
        self.file_format_version = file_format_version

    @classmethod
    def start_time_index(cls):
        # TODO make this an instance method
        return Util.time_string_to_index(cls.DEFAULT_START_TIME)

    @classmethod
    def default(cls):
        cls(cls.DEFAULT_START_TIME, cls.VERSION)

    @classmethod
    def c_to_pb(cls):
        config_pb = diary_pb.Config()

        config_pb.file_format_version = cls.VERSION
        config_pb.start_time = cls.DEFAULT_START_TIME

        return config_pb

    def to_pb(self):
        config_pb = diary_pb.Config()

        config_pb.file_format_version = self.VERSION
        config_pb.start_time = self.start_time

        return config_pb

    def to_pb_str(self):
        return self.to_pb().SerializeToString()

    @classmethod
    def from_pb(cls, config_pb):
        return cls(config_pb.start_time, config_pb.file_format_version)

    def __repr__(self):
        fmt_str = "\nConfig:\n  file_format_version: {}\n  start_time: {}"
        return fmt_str.format(self.file_format_version, self.start_time)
