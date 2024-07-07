import subprocess
import datetime
import re
import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 27017)

# Replace 'your_database_name' with the name of your database
db = client['DBPimi']
# Replace 'books' with the name of your collection
wispeed_collection = db['WiSpeed']


def db_add_reading(download, upload, date_r, time_r):
    wifi_data = {
        'Download': download,
        'Upload': upload,
        'Date': date_r,
        'Time': time_r
    }
    result = wispeed_collection.insert_one(wifi_data)
    return True

def db_return_reading(date_r):
    wifi_data = {
        'Date': date_r
    }
    result = wispeed_collection.find(wifi_data)
    return result

def db_return_all():
    result = wispeed_collection.find()
    return result

def db_return_by_download():
    result = wispeed_collection.find().sort('Download', -1)
    return result

def db_return_by_upload():
    result = wispeed_collection.find().sort('Upload', -1)
    return result