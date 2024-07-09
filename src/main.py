import time
import logging
from TLE_pulling import main
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)

def job():
    main()

def get_utc_time():
    return datetime.now(timezone.utc)

def should_run_now(current_utc_time: datetime):
    # Run every hour from 22:00 PM to 06:00 AM UTC
    hour = current_utc_time.hour
    return (hour >= 22 or hour < 6) and current_utc_time.minute == 0

while True:
    try:
        current_utc_time = get_utc_time()
        if should_run_now(current_utc_time):
            job()
            # Wait for an hour minus a few seconds to avoid missing the next hour's job
            time.sleep(3600 - 120)
        else:
            # Sleep until the next minute
            time.sleep(60)
        logging.info(f'Waiting until next time..., time right now: {str(current_utc_time)}')
    except Exception as e:
        logging.error(f"Error while running script: {e}")
        # Sleep for a minute before retrying in case of an error
        time.sleep(60)