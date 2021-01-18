import os
import time
from pathlib import Path

import schedule

old_files_folder_name = "old_files"

def clean_up_downloads():
    print("Cleaning up Downloads")

    # get all items from the downloads filder
    download_folder_path = os.path.join(Path.home(), "Downloads", "Downloads")
    download_items = os.listdir(download_folder_path)
    moved_items = 0

    # create the old files folder if not present
    old_files_folder_path = os.path.join(download_folder_path, old_files_folder_name)
    if old_files_folder_name not in download_items:
        print(f"No {old_files_folder_name} folder yet, creating folder")
        os.mkdir(old_files_folder_path)

    # create new folder with todays timestamp
    timestamp = time.strftime("%Y_%m_%d")
    datetime_folder_path = os.path.join(old_files_folder_path, timestamp)
    if not os.path.exists(datetime_folder_path):
        print(f"No {datetime_folder_path} folder yet, creating folder")
        os.mkdir(datetime_folder_path)
    else:
        print(f"{timestamp} folder already exists in {old_files_folder_name}")

    # rename all items to move them into the current datetime folder
    to_be_moved = [item for item in download_items if item != old_files_folder_name]

    for item in to_be_moved:
        print(f"Moving {item} to {datetime_folder_path} folder")
        old_path = os.path.join(download_folder_path, item)
        new_path = os.path.join(datetime_folder_path, item)
        os.rename(old_path, new_path)

        moved_items += 1

    print(f"Moved {moved_items} of {len(to_be_moved)} items")

# clean up the downloads folder every monday
schedule.every().monday.do(clean_up_downloads)

# keep the script running and sleep in between the checks
while True:
    schedule.run_pending()
    # sleep 24h
    time.sleep(60 * 60 * 24)