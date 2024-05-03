import subprocess
import re
from pymongo import MongoClient
import crudFunc
import threading
import sched
from datetime import datetime
import time

# Global variables
global_cmd = "speedtest-cli"
global_optn = "--secure"
seconds_to_minutes = 60
scheduler = sched.scheduler(time.time, time.sleep)
# ---------------

def repeat_function(func, interval):
    count = 0
    while (count<interval):
        func()                # Call the specified function
        time.sleep(interval)  # Wait for the specified interval
        count=count+1

def main_func():
    try:
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
        date_r = datetime.now().strftime("%Y-%m-%d")
        time_r = datetime.now().strftime("%H:%M:%S")
        crudFunc.addReading(download_speed, upload_speed, date_r, time_r)
    except Exception as e:
        print("Error running main_func:", e)

def periodic_reading(frequency, max):
    counter = 0
    while counter < max:
        main_func()                               # Call the main_func function
        time.sleep(frequency*seconds_to_minutes)  # Convert frequency to minutes
        counter += 1   

def returnReading(date):
    return crudFunc.returnReading(date)

def returnAll():
    return crudFunc.returnAll()

def convert_to_computer_time(user_input):
    try:
        # Parse user input into a datetime object
        user_time = datetime.strptime(user_input, '%H:%M:%S').time()
        # Convert datetime.time object to datetime.datetime object
        user_datetime = datetime.combine(datetime.today(), user_time)
        # Convert datetime.datetime object to seconds since the epoch
        user_seconds = time.mktime(user_datetime.timetuple())
        return user_seconds
    except ValueError:
        # Handle invalid input format
        print("Invalid input format. Please enter time in HH:MM:SS format.")
        return None

def readingAt(time_str):
    computer_time = convert_to_computer_time(time_str)
    if computer_time:
        print("Computer time:", datetime.fromtimestamp(computer_time))
        scheduler.enterabs(computer_time, 1, main_func, ())

    scheduler.run()
    return

    

    