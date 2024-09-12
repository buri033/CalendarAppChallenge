from dataclasses import dataclass, field
from datetime import datetime, date, time, timedelta
from typing import ClassVar, Optional

from app.services.util import generate_unique_id, date_lower_than_today_error, event_not_found_error, \
    reminder_not_found_error, slot_not_available_error


# TODO: Implement Reminder class here
def slot_not_available_error():
    raise ValueError("Slot not available")


def event_not_found_error():
    raise ValueError("Event not found")


def reminder_not_found_error():
    raise ValueError("Reminder not found")


@dataclass
class Reminder:
    EMAIL = "email"
    SYSTEM = "system"

    date_time: datetime
    type: str = EMAIL

    def __str__(self) -> str:
        return f"Reminder on {self.date_time} of type {self.type}"

# TODO: Implement Event class here
@dataclass
class Event:
    title: str
    description: str
    date_: date
    start_at: time
    end_at: time
    reminders: list[Reminder] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(datetime.now().timestamp()))

    def add_reminder(self, date_time: datetime, type_: str = Reminder.EMAIL) -> None:
        self.reminders.append(Reminder(date_time=date_time, type=type_))

    def delete_reminder(self, reminder_index: int) -> None:
        if 0 <= reminder_index < len(self.reminders):
            del self.reminders[reminder_index]
        else:
            reminder_not_found_error()

    def __str__(self) -> str:
        return (f"ID: {self.id}\n"
                f"Event title: {self.title}\n"
                f"Description: {self.description}\n"
                f"Time: {self.start_at} - {self.end_at}")

# TODO: Implement Day class here
class Day:
    def __init__(self, date_: date) -> None:
        self.date_ = date_
        self.slots: dict[time, Optional[str]] = {}
        self._init_slots()

    def _init_slots(self) -> None:
        for hour in range(24):
            for minute in range(0, 60, 15):
                self.slots[time(hour, minute)] = None

    def add_event(self, event_id: str, start_at: time, end_at: time) -> None:
        current_time = start_at
        while current_time < end_at:
            if self.slots.get(current_time) is not None:
                slot_not_available_error()
            self.slots[current_time] = event_id
            current_time = (datetime.combine(date.min, current_time) + timedelta(minutes=15)).time()

    def delete_event(self, event_id: str):
        deleted = False
        for slot, saved_id in self.slots.items():
            if saved_id == event_id:
                self.slots[slot] = None
                deleted = True
        if not deleted:
            event_not_found_error()

    def update_event(self, event_id: str, start_at: time, end_at: time):
        for slot in self.slots:
            if self.slots[slot] == event_id:
                self.slots[slot] = None

        for slot in self.slots:
            if start_at <= slot < end_at:
                if self.slots[slot]:
                    slot_not_available_error()
                else:
                    self.slots[slot] = event_id

    def find_available_slots(self) -> list[time]:
        return [slot for slot, event_id in self.slots.items() if event_id is None]


# TODO: Implement Calendar class here
