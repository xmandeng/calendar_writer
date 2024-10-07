import logging
from datetime import datetime, timedelta

import pandas as pd
import pytz
from ics import Calendar, Event

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Set timezone to America/New_York for Eastern Daylight/Standard Time
eastern = pytz.timezone("America/New_York")

# Define the events using a pandas DataFrame
data = {
    "start_date": [
        "2024-10-03",
        "2024-10-14",
        "2024-11-01",
        "2024-11-07",
        "2024-11-08",
        "2024-11-27",
        "2024-12-20",
        "2024-12-23",
        "2025-01-20",
        "2025-01-21",
        "2025-01-29",
        "2025-02-13",
        "2025-02-14",
        "2025-02-17",
        "2025-03-17",
        "2025-03-31",
        "2025-04-18",
        "2025-05-02",
        "2025-05-26",
        "2025-06-05",
        "2025-06-17",
        "2025-06-18",
        "2025-06-19",
        "2025-06-20",
        "2025-07-04",
    ],
    "end_date": [
        "2024-10-04",
        "2024-10-14",
        "2024-11-01",
        "2024-11-07",
        "2024-11-08",
        "2024-11-29",
        "2024-12-20",
        "2025-01-03",
        "2025-01-20",
        "2025-01-21",
        "2025-01-29",
        "2025-02-13",
        "2025-02-14",
        "2025-02-18",
        "2025-03-28",
        "2025-03-31",
        "2025-04-18",
        "2025-05-02",
        "2025-05-26",
        "2025-06-05",
        "2025-06-17",
        "2025-06-18",
        "2025-06-19",
        "2025-06-20",
        "2025-07-04",
    ],
    "event_name": [
        "Rosh Hashanah - School Closed",
        "Indigenous Peoples' Day/Fall Weekend - School Closed",
        "Diwali - School Closed",
        "Family-Teacher Conferences - Noon Dismissal",
        "Family-Teacher Conferences - No Classes",
        "Thanksgiving Break - School Closed",
        "Winter Break - Noon Dismissal",
        "Winter Break - School Closed",
        "Martin Luther King, Jr. Day - School Closed",
        "Faculty & Staff Professional Development - No Classes",
        "Lunar New Year - School Closed",
        "Family-Teacher Conferences - Noon Dismissal",
        "Family-Teacher Conferences - No Classes",
        "Presidents’ Day Weekend - School Closed",
        "Spring Break - School Closed",
        "Eid al-Fitr - School Closed",
        "Good Friday - School Closed",
        "Grandparents & Special Visitors Day - Noon Dismissal",
        "Memorial Day - School Closed",
        "Eid al-Adha - School Closed",
        "Final Day of Classes - Noon Dismissal",
        "Graduation - 10:00 AM",
        "Juneteenth - School Closed",
        "Annual Reset Day - School Closed",
        "Independence Day - School Closed",
    ],
    "event_time": [
        "all_day",
        "all_day",
        "all_day",
        "12:00",
        "all_day",
        "all_day",
        "12:00",
        "all_day",
        "all_day",
        "all_day",
        "all_day",
        "12:00",
        "all_day",
        "all_day",
        "all_day",
        "all_day",
        "all_day",
        "12:00",
        "all_day",
        "all_day",
        "12:00",
        "10:00",
        "all_day",
        "all_day",
        "all_day",
    ],
}

# Create a DataFrame for the events
events_df = pd.DataFrame(data)

# Create a new calendar
cal = Calendar()


# Function to check if a date is a weekend
def is_weekend(date):
    return date.weekday() >= 5  # Saturday (5) and Sunday (6)


# Add events to the calendar, handling single-day and multi-day events
for index, row in events_df.iterrows():
    # Parse the start and end dates
    start = datetime.strptime(row["start_date"], "%Y-%m-%d")
    end = datetime.strptime(row["end_date"], "%Y-%m-%d")
    event_name = row["event_name"]
    event_time = row["event_time"]

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
                    logging.debug(f"Added all-day event: {event_name} from {block_start} to {event_end}")
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
            logging.debug(f"Added all-day event: {event_name} from {block_start} to {end}")

    # Handle events with specific times
    else:
        event_start = eastern.localize(datetime.strptime(f"{row['start_date']} {event_time}", "%Y-%m-%d %H:%M"))
        event_end = event_start + timedelta(hours=1)  # Default 1-hour duration
        event = Event(name=event_name, begin=event_start, end=event_end)
        cal.events.add(event)
        logging.debug(f"Added timed event: {event_name} at {event_start}")

# Save to an .ics file with UTF-8 encoding
ics_filename = "school_closings_calendar.ics"
with open(ics_filename, "w", encoding="utf-8") as f:
    f.writelines(cal)

logging.info(f"ICS file created: {ics_filename}")
