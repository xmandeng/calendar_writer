from ics import Calendar, Event
from datetime import datetime, timedelta
import pytz

# Set timezone to America/New_York for Eastern Daylight/Standard Time
eastern = pytz.timezone("America/New_York")

# Create a new calendar
cal = Calendar()

# List of events, including multi-day and single-day events
events = [
    ("2024-10-03", "2024-10-04", "Rosh Hashanah - School Closed", "all_day"),
    ("2024-10-14", "2024-10-14", "Indigenous Peoples' Day/Fall Weekend - School Closed", "all_day"),
    ("2024-11-01", "2024-11-01", "Diwali - School Closed", "all_day"),
    ("2024-11-07", "2024-11-07", "Family-Teacher Conferences - Noon Dismissal", "12:00"),
    ("2024-11-08", "2024-11-08", "Family-Teacher Conferences - No Classes", "all_day"),
    ("2024-11-27", "2024-11-29", "Thanksgiving Break - School Closed", "all_day"),
    ("2024-12-20", "2024-12-20", "Winter Break - Noon Dismissal", "12:00"),
    ("2024-12-23", "2025-01-03", "Winter Break - School Closed", "all_day"),
    ("2025-01-20", "2025-01-20", "Martin Luther King, Jr. Day - School Closed", "all_day"),
    ("2025-01-21", "2025-01-21", "Faculty & Staff Professional Development - No Classes", "all_day"),
    ("2025-01-29", "2025-01-29", "Lunar New Year - School Closed", "all_day"),
    ("2025-02-13", "2025-02-13", "Family-Teacher Conferences - Noon Dismissal", "12:00"),
    ("2025-02-14", "2025-02-14", "Family-Teacher Conferences - No Classes", "all_day"),
    ("2025-02-17", "2025-02-18", "Presidents’ Day Weekend - School Closed", "all_day"),
    ("2025-03-17", "2025-03-28", "Spring Break - School Closed", "all_day"),
    ("2025-03-31", "2025-03-31", "Eid al-Fitr - School Closed", "all_day"),
    ("2025-04-18", "2025-04-18", "Good Friday - School Closed", "all_day"),
    ("2025-05-02", "2025-05-02", "Grandparents & Special Visitors Day - Noon Dismissal", "12:00"),
    ("2025-05-26", "2025-05-26", "Memorial Day - School Closed", "all_day"),
    ("2025-06-05", "2025-06-05", "Eid al-Adha - School Closed", "all_day"),
    ("2025-06-17", "2025-06-17", "Final Day of Classes - Noon Dismissal", "12:00"),
    ("2025-06-18", "2025-06-18", "Graduation - 10:00 AM", "10:00"),
    ("2025-06-19", "2025-06-19", "Juneteenth - School Closed", "all_day"),
    ("2025-06-20", "2025-06-20", "Annual Reset Day - School Closed", "all_day"),
    ("2025-07-04", "2025-07-04", "Independence Day - School Closed", "all_day"),
]


# Function to check if a date is a weekend
def is_weekend(date):
    return date.weekday() >= 5  # Saturday (5) and Sunday (6)


# Add events to the calendar, handling single-day and multi-day events
for start_date, end_date, event_name, event_time in events:
    # Parse the start and end dates
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    # Handle all-day events
    if event_time == "all_day":
        current_date = start
        block_start = None
        while current_date <= end:
            if not is_weekend(current_date):
                if block_start is None:  # Start a new block of all-day events
                    block_start = current_date
            else:
                if block_start:
                    # End the event at the day before the current date
                    event_end = current_date - timedelta(days=1)
                    event = Event(
                        name=event_name,
                        begin=eastern.localize(block_start),
                        end=eastern.localize(event_end),  # End at the last valid day, no timedelta(days=1)
                    )
                    event.make_all_day()
                    cal.events.add(event)
                    block_start = None  # Reset block start
            current_date += timedelta(days=1)

        # Check if the last block extends to the end date
        if block_start and not is_weekend(end):  # Ensure the last block doesn't end on a weekend
            event = Event(
                name=event_name,
                begin=eastern.localize(block_start),
                end=eastern.localize(end),  # End at the last valid day, no timedelta(days=1)
            )
            event.make_all_day()
            cal.events.add(event)

    # Handle events with specific times
    else:
        event_start = eastern.localize(datetime.strptime(f"{start_date} {event_time}", "%Y-%m-%d %H:%M"))
        event_end = event_start + timedelta(hours=1)  # Default 1-hour duration
        event = Event(name=event_name, begin=event_start, end=event_end)
        cal.events.add(event)

# Save to an .ics file with UTF-8 encoding
with open("school_closings_calendar.ics", "w", encoding="utf-8") as f:
    f.writelines(cal)

print("ICS file created: school_closings_calendar.ics")
