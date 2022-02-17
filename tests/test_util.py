import pytest
import re
from dev_diary.util import Util


class TestUtil:
    def test_today_returns_formatted_date_str(self):
        assert re.fullmatch(r"\d\d\d\d-\d\d-\d\d", Util.today())

    def test_time_string_to_integers(self):
        assert Util.time_string_to_integers("00:15") == [0, 1]
        assert Util.time_string_to_integers("09:00") == [9, 0]
        assert Util.time_string_to_integers("15:30") == [15, 2]
        assert Util.time_string_to_integers("20:45") == [20, 3]

    def test_time_string_to_integers_bod(self):
        assert Util.time_string_to_integers("00:00") == [0, 0]

    def test_time_string_to_integers_eod(self):
        assert Util.time_string_to_integers("23:45") == [23, 3]

    def test_time_string_to_integers_with_non_time_string(self):
        with pytest.raises(ValueError, match="Time string must be formatted as HH:MM"):
            Util.time_string_to_integers("Foo")

        with pytest.raises(ValueError, match="Time string must be formatted as HH:MM"):
            Util.time_string_to_integers("This: That")

        with pytest.raises(ValueError, match="Time string must be formatted as HH:MM"):
            Util.time_string_to_integers("128:45678")

    def test_time_string_to_integers_with_invalid_time_string(self):
        with pytest.raises(
            ValueError,
            match="Hour must be 0-23 and minutes must be :00, :15, :30, or :45",
        ):
            Util.time_string_to_integers("99:99")

    def test_time_string_to_integers_with_invalid_hours(self):
        with pytest.raises(
            ValueError,
            match="Hour must be 0-23 and minutes must be :00, :15, :30, or :45",
        ):
            Util.time_string_to_integers("25:00")

    def test_time_string_to_integers_with_invalid_minutes(self):
        with pytest.raises(
            ValueError,
            match="Hour must be 0-23 and minutes must be :00, :15, :30, or :45",
        ):
            Util.time_string_to_integers("23:02")

        with pytest.raises(
            ValueError,
            match="Hour must be 0-23 and minutes must be :00, :15, :30, or :45",
        ):
            Util.time_string_to_integers("23:99")

    def test_time_integers_to_string(self):
        assert Util.time_integers_to_string(1, 0) == "01:00"
        assert Util.time_integers_to_string(8, 1) == "08:15"
        assert Util.time_integers_to_string(17, 2) == "17:30"
        assert Util.time_integers_to_string(21, 3) == "21:45"

    def test_time_integers_to_string_bod(self):
        assert Util.time_integers_to_string(0, 0) == "00:00"

    def test_time_integers_to_string_eod(self):
        assert Util.time_integers_to_string(23, 3) == "23:45"

    def test_time_integers_to_string_with_bad_hour_data(self):
        with pytest.raises(
            ValueError, match="Hour must be 0-23 and quarter must be 0-3"
        ):
            Util.time_integers_to_string(24, 0)

        with pytest.raises(
            ValueError, match="Hour must be 0-23 and quarter must be 0-3"
        ):
            Util.time_integers_to_string(-1, 0)

    def test_time_integers_to_string_with_bad_quarter_data(self):
        with pytest.raises(
            ValueError, match="Hour must be 0-23 and quarter must be 0-3"
        ):
            Util.time_integers_to_string(0, 4)

        with pytest.raises(
            ValueError, match="Hour must be 0-23 and quarter must be 0-3"
        ):
            Util.time_integers_to_string(0, -1)

    def test_time_integers_to_string_with_all_bad_data(self):
        with pytest.raises(
            ValueError, match="Hour must be 0-23 and quarter must be 0-3"
        ):
            Util.time_integers_to_string(128, 128)

        with pytest.raises(
            ValueError, match="Hour must be 0-23 and quarter must be 0-3"
        ):
            Util.time_integers_to_string(-1, -1)

    def test_time_string_to_index_bod(self):
        assert Util.time_string_to_index("00:00") == 0

    def test_time_string_to_index_eod(self):
        assert Util.time_string_to_index("23:45") == 23 * 4 + 3

    def test_time_string_to_index(self):
        assert Util.time_string_to_index("03:00") == 12
        assert Util.time_string_to_index("14:15") == 57
        assert Util.time_string_to_index("20:30") == 82
        assert Util.time_string_to_index("22:45") == 91

    def test_time_string_to_index_with_bad_data(self):
        with pytest.raises(
            ValueError,
            match="Hour must be 0-23 and minutes must be :00, :15, :30, or :45",
        ):
            Util.time_string_to_index("99:99")
