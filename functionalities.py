import subprocess
import re
import datetime
from pymongo import MongoClient
import crudFunc
import threading
import time
# Global variables
global_cmd = "speedtest-cli"
global_optn = "--secure"
# ---------------
def repeat_function(func, interval):
    count = 0
    while (count<interval):
        func()                # Call the specified function
        time.sleep(interval)  # Wait for the specified interval
        count=count+1

def main_func():
# Define the command to run
    command = [global_cmd, global_optn]

    # Run the command and capture the output
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

    # Print the command output
    print("=======Performing WIFI Test=======")

    # print(result.stdout)
    result = result.stdout

    lines = result.split('\n')

    # parse command output
    download_speed_line = [line for line in lines if 'Download:' in line]
    upload_speed_line = [line for line in lines if 'Upload:' in line]
    download_speed = download_speed_line[0].split('Download: ')[1].strip()
    upload_speed = upload_speed_line[0].split('Upload: ')[1].strip()

    print("Download Speed:", download_speed)
    print("Upload Speed:", upload_speed)
    date_r = datetime.date.today()
    date_r = date_r.strftime("%Y-%m-%d")
    time_r = datetime.datetime.now()
    time_r = time_r.strftime("%H:%M:%S")
    crudFunc.addReading(download_speed, upload_speed, date_r, time_r)

def periodic_reading(frequency, max):
    # Frequency shall be read in minutes or hours.
    counter = 0
    while counter < max:
        main_func()  # Call the main_func function
        time.sleep(frequency)  # Convert frequency to minutes
        counter += 1