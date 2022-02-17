from re import fullmatch
from datetime import datetime


class Util:
    @staticmethod
    def today():
        return datetime.today().strftime("%Y-%m-%d")

    @staticmethod
    def time_string_to_index(time_string):
        hour, quarter = Util.time_string_to_integers(time_string)
        return (hour * 4) + quarter

    @staticmethod
    def time_string_to_integers(time_string):
        if not fullmatch(r"\d\d:\d\d", time_string):
            raise ValueError("Time string must be formatted as HH:MM")

        quarter_dict = {"00": 0, "15": 1, "30": 2, "45": 3}

        hour_str, minutes_str = time_string.split(":")

        hour = int(hour_str)
        quarter = quarter_dict.get(minutes_str)

        if quarter is None or hour < 0 or hour > 23 or quarter < 0 or quarter > 3:
            raise ValueError(
                "Hour must be 0-23 and minutes must be :00, :15, :30, or :45"
            )

        return [hour, quarter_dict[minutes_str]]

    @staticmethod
    def time_integers_to_string(hour, quarter):
        if hour < 0 or hour > 23 or quarter < 0 or quarter > 3:
            raise ValueError("Hour must be 0-23 and quarter must be 0-3")

        hour_string = "0{}".format(hour)[-2:]
        minute_string = "0{}".format(quarter * 15)[-2:]
        time_string = "{}:{}".format(hour_string, minute_string)
        return time_string
