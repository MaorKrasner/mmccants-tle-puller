import os
import re
import logging
import requests
import html2text
from config import config
from dateutil.parser import parse
from datetime import datetime, time

logging.basicConfig(level=logging.INFO)

norad_ids = ["29155", "31135", "41183"]


def create_session():
    session = requests.Session()
    return session

def login(session: requests.Session):
    try:
        response = session.post(config["login_url"], data=config["credentials"])
        response.raise_for_status()

        if response.status_code == 200:
            logging.info("Login successful!")
            return True
        logging.error(f'Login failed. Status code: {response.status_code}')
        return False
    
    except requests.exceptions.ConnectionError:
        logging.error("A connection error occurred.")
    except requests.exceptions.Timeout:
        logging.error("The request timed out.")
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.TooManyRedirects:
        logging.error("Too many redirects.")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"An error occurred: {req_err}")
    
    return False

"""
def delete_all_old_files_in_new_space_folder():
    folder_path = str(os.path.abspath(config["new_space_output_folder_path"]))
    logging.info(f'Folder path: {folder_path}')
    if os.path.exists(folder_path):
        files_in_folder = os.listdir(folder_path)
        for file_name in files_in_folder:
            if "ny2o_tle_data" in file_name:
                file_path = os.path.join(folder_path, file_name)
                try:
                    os.remove(file_path)
                    logging.info(f"Deleted file: {file_path}")
                except Exception as e:
                    logging.error(f"Error deleting file {file_path}: {e}")
        return True
    else:
        logging.error("Folder to delete not found. Try again.")
    return False
"""

def delete_all_old_files_in_new_space_folder():
    folder_path = str(os.path.abspath(config["new_space_output_folder_path"]))
    logging.info(f'Folder path: {folder_path}')
    
    if os.path.exists(folder_path):
        files_in_folder = os.listdir(folder_path)
        today_date = datetime.now().date()
        cutoff_time = datetime.combine(today_date, time(22, 0))  # Combine today's date with 22:00 time

        for file_name in files_in_folder:
            if file_name.startswith("ny2o_tle_data"):
                try:
                    # Debug: Print the full file name
                    logging.debug(f"Processing file: {file_name}")
                    
                    date_part = file_name.split('_')[3].split('.')[0]
                    
                    # Debug: Print the extracted date part
                    logging.debug(f"Extracted date part: {date_part}")
                    
                    file_datetime = parse(date_part).replace(tzinfo=None)  # Make the datetime naive

                    # Debug: Print the parsed datetime
                    logging.debug(f"Parsed datetime: {file_datetime}")

                    # Compare the file datetime with the cutoff datetime
                    if file_datetime < cutoff_time:
                        file_path = os.path.join(folder_path, file_name)
                        try:
                            os.remove(file_path)
                            logging.info(f"Deleted file: {file_path}")
                        except Exception as e:
                            logging.error(f"Error deleting file {file_path}: {e}")
                
                except IndexError:
                    logging.warning(f"File {file_name} does not match expected format.")
                    continue
                except ValueError:
                    logging.warning(f"Invalid date format in file {file_name}.")
                    continue
        
        return True
    else:
        logging.error("Folder to delete not found. Try again.")
        return False



def find_satellite_name(text_content: str):
    satellite_name = ""
    whole_text_lines = text_content.split("\n")
    for whole_text_line in whole_text_lines:
        if whole_text_line.startswith("# "):
            satellite_name = whole_text_line.split("# ")[1]

    return satellite_name if satellite_name != "" else "unknown"

def write_tle_sets_into_text_file(tle_sets: list):
    current_date_time_in_iso = datetime.now().isoformat().replace(":", "-")
    #folder_path = config["new_space_output_folder_path"]
    #full_ny2o_file_path = os.path.join(folder_path, config["ny2o_output_file_name"] + "_" + str(current_date_time_in_iso) + ".txt")
    full_ny2o_file_path = os.path.join(config["ny2o_output_file_name"] + "_" + str(current_date_time_in_iso) + ".txt")

    with open(full_ny2o_file_path, "w") as f:
        time_now = datetime.now().strftime("%A, %B %d, %Y at %I:%M%p")
        f.write(f"File created at: {time_now}\n")
        for tle_set in tle_sets:
            f.write(f"\nSATELLITE NAME: {str(tle_set[2])}, NORAD ID: {str(tle_set[1])}\n")
            first_tle_line = "\n" if str(tle_set[0][3]).strip() == '' else str(tle_set[0][3]).lstrip()
            second_tle_line = "\n" if str(tle_set[0][4]).strip() == '' else str(tle_set[0][4]).lstrip()
            f.write(f"TLE line number 1: {first_tle_line}")
            f.write(f"TLE line number 2: {second_tle_line}")
            f.write("\n")

    f.close()
    logging.info(f'TLE objects written successfully into {full_ny2o_file_path}')

def extract_tle_sets_from_ny2o(session: requests.Session):
    #is_deleted_successfully = delete_all_old_files_in_new_space_folder()

    #if is_deleted_successfully:
    tle_sets = []
    for norad in norad_ids:
        data_response = session.get(f'{config["tle_objects_extraction_url"]}?s={norad}')
        logging.info(f"Parsing html page content for satellite with norad id {norad}...")
        html_content = data_response.text
        text_content = html2text.html2text(html_content)

        satellite_name = find_satellite_name(text_content=text_content)

        pattern_for_finding_tle_start_text = r'Two Line Element Set(?:\s*\([^)]*\))*:\s*(.*)'
        tle_data_matches = re.search(pattern_for_finding_tle_start_text, text_content, re.DOTALL)

        if tle_data_matches:
            content_after_tle_set_line = tle_data_matches.group(1).strip()
            cleaned_text = re.sub(r'\n{2,}', '\n', content_after_tle_set_line)
            lines = cleaned_text.split('\n')
            tle_sets.append([lines, norad, satellite_name])
            logging.info(f"The lines are: ")
            logging.info(lines[3])
            logging.info(lines[4])
        else:
            logging.info("Phrase 'Two Line Element Set' not found in the text.")
    
    write_tle_sets_into_text_file(tle_sets=tle_sets)
    #else:
    #    logging.error("Couldn't delete old files successfully, can't create new ny2o tle sets file.")

def main():
    #session = create_session()
    #is_login_successful = login(session=session)
    #if is_login_successful:
    #    extract_tle_sets_from_ny2o(session=session)
    delete_all_old_files_in_new_space_folder()

main()