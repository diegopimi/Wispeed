import json
from pathlib import Path

project_root  = Path(__file__).resolve().parent
log_file_path = project_root / "Logs" / "log.json"


# ── Path helpers ────────────────────────────────────────────────────────────

def does_path_exist() -> bool:
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    return log_file_path.exists()


def create_path() -> None:
    """Create the Logs directory and an empty JSON array file."""
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    log_file_path.touch()
    with log_file_path.open("w") as f:
        f.write("[]")
    print(f"[file_manager] Created log file at: {log_file_path}")


def ensure_log_exists() -> None:
    """Call once at app startup — creates the file only if missing."""
    if not does_path_exist():
        print("[file_manager] Log file not found — creating.")
        create_path()
    else:
        print("[file_manager] Log file already exists.")


# ── Data I/O ─────────────────────────────────────────────────────────────────

def read_file() -> list:
    """Read and return the full log as a Python list. Always fresh from disk."""
    with log_file_path.open("r") as f:
        data = json.load(f)
    return data if isinstance(data, list) else [data]


def write_file(data: list) -> None:
    """Overwrite the log file with the given list."""
    with log_file_path.open("w") as f:
        json.dump(data, f, indent=4)
