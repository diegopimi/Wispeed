import subprocess
import re
import datetime
from pymongo import MongoClient
import crudFunc

# Replace 'localhost' with the actual hostname or IP address of your MongoDB server.
# If your MongoDB server is running on the default port (27017), you don't need to specify it.
client = MongoClient('localhost', 27017)

# Replace 'your_database_name' with the name of your existing database.
db = client['DBPimi']

# Define the command to run
command = ["speedtest-cli", "--secure"]

# Run the command and capture the output
result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

# Print the command output
print("=======Performing WIFI Test=======")

# print(result.stdout)
result = result.stdout

lines = result.split('\n')

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

