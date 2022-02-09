from dev_diary.util import Util


class Config:
    VERSION = "0.02"
    START_TIME = "09:00"

    @classmethod
    def start_time_index(cls):
        return Util.time_string_to_index(cls.START_TIME)
