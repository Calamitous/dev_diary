from datetime import datetime


class Util:
    @staticmethod
    def today():
        return datetime.today().strftime("%Y-%m-%d")

    @staticmethod
    def time_string_to_index(time_string):
        quarter_dict = {"00": 0, "15": 1, "30": 2, "45": 3}

        entry_hour, entry_quarter = time_string.split(":")
        return (int(entry_hour) * 4) + quarter_dict[entry_quarter]
