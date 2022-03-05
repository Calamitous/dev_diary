import pytest
from dev_diary.entry import Activity, ActivityNames, Entry
import dev_diary.protos.diary_pb2 as diary_pb


class TestActivity:
    def test_activity(self):
        assert len(Activity) == 7

    def test_activity_names(self):
        assert ActivityNames == [
            "administrivia",
            "downtime",
            "meeting",
            "pairing",
            "solo",
            "other",
            "empty",
        ]


class TestEntry:
    @pytest.fixture
    def entry(self):
        return Entry("09:00", 4, Activity["meeting"], "Foo")

    def test_create(self, entry):
        assert entry.start == "09:00"
        assert entry.duration == 4
        assert entry.activity == Activity["meeting"]
        assert entry.text == "Foo"

    def test_activity_name(self, entry):
        assert entry.activity_name() == "meeting"
        entry.activity = Activity["solo"]

    def test_to_pb_returns_protobuf(self, entry):
        assert type(entry.to_pb()) == diary_pb.Entry

    def test_to_pb_str_returns_str(self, entry):
        assert type(entry.to_pb_str()) == bytes

    def test___repr__(self, entry):
        assert (
            str(entry)
            == "\nEntry:\n  start: 09:00\n  duration: 4\n  activity: 2\n  text: Foo"
        )

    def test_activity_line(self, entry):
        entry = Entry.activity_line("downtime")
        assert entry.start == ""
        assert entry.duration == 0
        assert entry.activity_name() == "downtime"
        assert entry.text == ""

    def test_empty(self):
        entry = Entry.empty()
        assert entry.activity_name() == "empty"

    def test_line_is_entry(self, entry):
        # Should only return true if time falls within the duration of the entry
        assert not entry.line_is_entry(8, 0, "08:00")
        assert not entry.line_is_entry(8, 1, "08:15")
        assert not entry.line_is_entry(8, 1, "08:30")
        assert not entry.line_is_entry(8, 1, "08:45")
        assert entry.line_is_entry(9, 0, "09:00")
        assert entry.line_is_entry(9, 1, "09:15")
        assert entry.line_is_entry(9, 2, "09:30")
        assert entry.line_is_entry(9, 3, "09:45")
        assert not entry.line_is_entry(10, 0, "10:00")
        assert not entry.line_is_entry(10, 1, "10:15")
        assert not entry.line_is_entry(10, 2, "10:30")
        assert not entry.line_is_entry(10, 3, "10:45")

    def test_line_is_entry_bod(self, entry):
        assert not entry.line_is_entry(0, 0, "00:00")

    def test_line_is_entry_eod(self, entry):
        assert not entry.line_is_entry(23, 3, "23:45")

    def test_from_pb_creates_entry(self, entry):
        entry_pb = diary_pb.Entry()
        entry_pb.start = "11:00"
        entry_pb.duration = 3
        entry_pb.activity = Activity["downtime"]
        entry_pb.text = "Bar"

        entry = Entry.from_pb(entry_pb)

        assert entry.start == "11:00"
        assert entry.duration == 3
        assert entry.activity == Activity["downtime"]
        assert entry.text == "Bar"

    def test_duration_text(self, entry):
        entry.duration = 1
        assert entry.duration_text() == "15 minutes"
        entry.duration = 2
        assert entry.duration_text() == "30 minutes"
        entry.duration = 3
        assert entry.duration_text() == "45 minutes"
        entry.duration = 4
        assert entry.duration_text() == "1 hour"
        entry.duration = 5
        assert entry.duration_text() == "1 hour 15 minutes"
        entry.duration = 6
        assert entry.duration_text() == "1 hour 30 minutes"
        entry.duration = 7
        assert entry.duration_text() == "1 hour 45 minutes"
        entry.duration = 8
        assert entry.duration_text() == "2 hours"
        entry.duration = 83
        assert entry.duration_text() == "20 hours 45 minutes"

    def test_text_display_when_text_empty(self, entry):
        entry.text = ""
        assert entry.text_display(10) == "          "
        assert entry.text_display(0) == ""
        assert entry.text_display(37) == "                                     "

    def test_text_display_when_text_fits(self, entry):
        entry.text = "1234567890"
        assert entry.text_display(10) == "1234567890"
        assert entry.text_display(0) == ""
        assert entry.text_display(37) == "1234567890                           "

    def test_text_display_when_text_is_too_long(self, entry):
        entry.text = "1234567890123456789012345678901234567890"
        assert entry.text_display(10) == "1234567..."
        assert entry.text_display(0) == ""
        assert entry.text_display(37) == "1234567890123456789012345678901234..."

    # def test_new_entry(self):
