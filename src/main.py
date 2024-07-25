import time
import logging
from TLE_pulling import main
from datetime import datetime, timezone

def job():
    main()

def get_utc_time():
    return datetime.now(timezone.utc)

job_time_utc = "04:59"

while True:
    try:
        current_utc_time = get_utc_time()
        if current_utc_time.strftime("%H:%M") == job_time_utc:
            job()
        time.sleep(1)
        logging.info(f'Waiting until next time..., time right now: {str(datetime.now(timezone.utc))}')
    except Exception as e:
        logging.error(f"Error while running script: {e}") 