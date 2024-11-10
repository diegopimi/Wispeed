import subprocess
import re
import process_data
import sched
from datetime import datetime
import time
from flask import redirect, url_for

global_cmd = "speedtest-cli"
global_optn = "--secure"
seconds_to_minutes = 60
scheduler = sched.scheduler(time.time, time.sleep)
# ---------------

def repeat_function(func, interval):
    count = 0
    while (count<interval):
        func()                
        time.sleep(interval)  
        count=count+1

def main_func():
    try:
        command = [global_cmd, global_optn]

        result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

        print("=======Performing WIFI Test=======")

        download_speed_match = re.search(r'Download: ([\d.]+)', result.stdout)
        upload_speed_match = re.search(r'Upload: ([\d.]+)', result.stdout)

        if download_speed_match and upload_speed_match:
            download_speed = download_speed_match.group(1)
            upload_speed = upload_speed_match.group(1)

            print("Download Speed (Mbit/s):", download_speed)
            print("Upload Speed (Mbit/s):", upload_speed)

            date_r = datetime.now().strftime("%Y-%m-%d")
            time_r = datetime.now().strftime("%H:%M:%S")
            process_data.db_add_reading(download_speed, upload_speed, date_r, time_r)
        else:
            print("Error: Unable to extract speed values from command output")
    except Exception as e:
        print("Requester: Error running main_func:", e)

def periodic_reading(frequency, max_occurrences):
    messages = []
    counter = 0
    while counter < max_occurrences:
        main_func()
        read_count = counter + 1
        messages.append(f"Reading speed {read_count} / {max_occurrences}")
        time.sleep(frequency * seconds_to_minutes)
        counter += 1
    return messages 

def pop_up_rend(count):
    return redirect(url_for('index', popup = count))

def return_reading(date):
    return process_data.db_return_reading(date)

def return_all():
    return process_data.db_return_all()

def return_by_download():
    return process_data.db_return_by_download()

def return_by_upload():
    return process_data.db_return_by_upload()

def convert_to_computer_time(user_input):
    try:
        user_time = datetime.strptime(user_input, '%H:%M:%S').time()
        user_datetime = datetime.combine(datetime.today(), user_time)
        user_seconds = time.mktime(user_datetime.timetuple())
        return user_seconds
    except ValueError:
        print("Invalid input format. Please enter time in HH:MM:SS format.")
        return None

def reading_at(time_str):
    computer_time = convert_to_computer_time(time_str)
    if computer_time:
        print("Computer time:", datetime.fromtimestamp(computer_time))
        scheduler.enterabs(computer_time, 1, main_func, ())

    scheduler.run()
    return

    

    