import time
import logging
from TLE_pulling import main
from datetime import datetime, timezone

SLEEPING_TIME_IN_SECONDS = 60 * 60

def job():
    main()

def get_utc_time():
    return datetime.now(timezone.utc)

while True:
    try:
        current_utc_time = get_utc_time()
        if current_utc_time.hour == '7' or current_utc_time == '8':
            job()
        time.sleep(SLEEPING_TIME_IN_SECONDS)
        logging.info(f'Waiting until next time..., time right now: {str(datetime.now(timezone.utc))}')
    except Exception as e:
        logging.error(f"Error while running script: {e}") 