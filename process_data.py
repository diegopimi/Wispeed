from file_manager import read_file, write_file


# ── Write ────────────────────────────────────────────────────────────────────

def db_add_reading(download: float, upload: float, date_r: str, time_r: str) -> bool:
    """Append a new speed reading to the log. Speeds stored as floats."""
    wifi_data = {
        "Download": float(download),
        "Upload":   float(upload),
        "Date":     date_r,
        "Time":     time_r,
    }
    existing_data = read_file()          # always fresh from disk
    existing_data.append(wifi_data)
    write_file(existing_data)
    return True


# ── Read ─────────────────────────────────────────────────────────────────────

def db_return_reading(date_r: str) -> list:
    """Return all readings that match the given date string (YYYY-MM-DD)."""
    data = read_file()
    return [entry for entry in data if entry.get("Date") == date_r]


def db_return_all() -> list:
    """Return every reading, most recent first."""
    return read_file()


def db_return_by_download() -> list:
    """Return all readings sorted by download speed ascending (numeric)."""
    data = read_file()
    return sorted(data, key=lambda x: float(x["Download"]))


def db_return_by_upload() -> list:
    """Return all readings sorted by upload speed ascending (numeric)."""
    data = read_file()
    return sorted(data, key=lambda x: float(x["Upload"]))
