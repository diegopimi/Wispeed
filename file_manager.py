from pathlib import Path

project_root = Path(__file__).resolve().parent
log_file_path = project_root / "Logs" / "log.json"

def does_path_exist():
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    return log_file_path.exists()

def create_path():
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    log_file_path.touch()
    with log_file_path.open("w") as file:
        file.write("[]")
    print(log_file_path, "Has been created")

if does_path_exist() != True:
    create_path()
else:
    print("File already exists")