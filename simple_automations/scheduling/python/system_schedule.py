import os
import datetime

# get the content of the current directory
dir_content = os.listdir(".")

# create a new summary.log file to append the content to
with open("summary.log", "a") as summary:
    current_working_dir = os.getcwd()
    print(f"Writing dir content of dir {current_working_dir} to summary.log")

    # get the current time stamp and write a header for the current execution
    current_timestamp = datetime.datetime.now()
    summary.write(f"{current_timestamp}\n")

    # write each entity of the folder content into the summary.log file
    for entity in dir_content:
        summary.write(f"\t{entity}\n")

    # add a new line
    summary.write("\n")
    print(f"Wrote {len(dir_content)} entries for {current_timestamp} to {current_working_dir}/summary.log.") 