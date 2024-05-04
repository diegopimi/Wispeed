import subprocess
import re
import datetime
from pymongo import MongoClient
import crudFunc
from functionalities import repeat_function, main_func

# Replace 'localhost' with the actual hostname or IP address of your MongoDB server.
# If your MongoDB server is running on the default port (27017), you don't need to specify it.
client = MongoClient('mongodb', 27017)

# Replace 'your_database_name' with the name of your existing database.
db = client['DBPimi']

# Call the repeat_function with my_function and a frequency of 2 seconds
repeat_function(main_func, 1)
