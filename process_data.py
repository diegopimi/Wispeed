from pathlib import Path
import json

project_root = Path(__file__).resolve().parent
log_file_path = project_root / "Logs" / "log.json"

def read_file():
    with open(log_file_path, "r") as file:
        data = json.load(file)
    return data

data = read_file()

def db_add_reading(download, upload, date_r, time_r):
    wifi_data = {
        'Download': download,
        'Upload': upload,
        'Date': date_r,
        'Time': time_r
    }
    existing_data = read_file()

    if not isinstance(existing_data, list):
        existing_data = [existing_data]

    existing_data.append(wifi_data)

    with open(log_file_path, "w") as file:
        json.dump(existing_data, file, indent=4)
    
    return True

def db_return_reading(date_r):
    results = []
    for entry in data:
        if entry.get("Date") == date_r:
            results.append(entry)
    return results

def db_return_all():
    result = data
    return result

def db_return_by_download():
    result = sorted(data, key=lambda x: x['Download'])
    return result

def db_return_by_upload():
    result = sorted(data, key=lambda x: x['Upload'])
    return result