import logging
from TLE_pulling import main
from crontab import CronTab
import sys
import os

def run_main():
    logging.basicConfig(level=logging.INFO)
    try:
        main()
    except Exception as e:
        logging.error(f"Error while running script: {e}")

def setup_cron_job():
    # Initialize a new crontab for the current user
    cron = CronTab(user=True)

    # Define the command to run your script
    script_path = os.path.abspath(__file__)
    command = f'python3 {script_path} --run-main'
    
    # Check if a cron job with this command already exists
    for job in cron:
        if job.command == command:
            print("Cron job already exists.")
            return

    # Create a new cron job
    job = cron.new(command=command, comment='TLE pulling job')

    # Schedule the job (every day at 04:54 UTC)
    job.setall('54 4 * * *')

    # Write the job to the crontab
    cron.write()

    print("Cron job added successfully.")

if __name__ == "__main__":
    # Check if the script should run the main function
    if len(sys.argv) > 1 and sys.argv[1] == '--run-main':
        run_main()
    else:
        setup_cron_job()
