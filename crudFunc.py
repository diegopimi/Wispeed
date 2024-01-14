import subprocess
import re
from pymongo import MongoClient
client = MongoClient('localhost', 27017)

# Replace 'your_database_name' with the name of your database
db = client['DBPimi']
# Replace 'books' with the name of your collection
wispeed_collection = db['WiSpeed']


def addReading(download, upload):
    wifi_data = {
        'Download': download,
        'Upload': upload
    }
    result = wispeed_collection.insert_one(wifi_data)
    return True