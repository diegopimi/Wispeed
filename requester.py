import subprocess
import re
import sched
import time
from datetime import datetime

import process_data

# ── Constants ────────────────────────────────────────────────────────────────

SPEEDTEST_CMD  = ["speedtest-cli", "--secure"]
SECONDS_PER_MINUTE = 60

# Single scheduler instance — owned here, imported by app.py (never overwritten)
scheduler = sched.scheduler(time.time, time.sleep)


# ── Core speed test ──────────────────────────────────────────────────────────

def main_func() -> bool:
    """
    Run one speed test, parse the output, and persist the result.
    Returns True on success, False on failure.
    """
    try:
        print("======= Performing Wi-Fi Test =======")
        result = subprocess.run(
            SPEEDTEST_CMD,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            print(f"[requester] speedtest-cli exited with code {result.returncode}: {result.stderr.strip()}")
            return False

        dl_match = re.search(r"Download: ([\d.]+)", result.stdout)
        ul_match = re.search(r"Upload: ([\d.]+)",   result.stdout)

        if not dl_match or not ul_match:
            print("[requester] Could not parse speed values from output.")
            print("[requester] Raw output:", result.stdout)
            return False

        download_speed = float(dl_match.group(1))
        upload_speed   = float(ul_match.group(1))

        print(f"[requester] Download: {download_speed} Mbit/s")
        print(f"[requester] Upload:   {upload_speed} Mbit/s")

        date_r = datetime.now().strftime("%Y-%m-%d")
        time_r = datetime.now().strftime("%H:%M:%S")
        process_data.db_add_reading(download_speed, upload_speed, date_r, time_r)
        return True

    except Exception as e:
        print(f"[requester] Unexpected error in main_func: {e}")
        return False


# ── Periodic reading ─────────────────────────────────────────────────────────

def periodic_reading(frequency_minutes: float, max_occurrences: int) -> list[str]:
    """
    Run `max_occurrences` speed tests, waiting `frequency_minutes` between each.
    Returns a list of status messages.
    Note: call this from a background thread — it blocks for the full duration.
    """
    messages = []
    for i in range(1, max_occurrences + 1):
        success = main_func()
        status  = "OK" if success else "FAILED"
        msg     = f"Reading {i}/{max_occurrences} — {status}"
        messages.append(msg)
        print(f"[requester] {msg}")
        if i < max_occurrences:
            time.sleep(frequency_minutes * SECONDS_PER_MINUTE)
    return messages


# ── Scheduled reading ────────────────────────────────────────────────────────

def _parse_time_to_timestamp(time_str: str) -> float | None:
    """
    Parse a HH:MM:SS string into a Unix timestamp for today.
    Returns None if the format is invalid or the time has already passed.
    """
    try:
        user_time     = datetime.strptime(time_str, "%H:%M:%S").time()
        user_datetime = datetime.combine(datetime.today(), user_time)
        timestamp     = user_datetime.timestamp()

        if timestamp <= time.time():
            print(f"[requester] Scheduled time {time_str} has already passed today.")
            return None

        return timestamp
    except ValueError:
        print(f"[requester] Invalid time format '{time_str}'. Expected HH:MM:SS.")
        return None


def reading_at(time_str: str) -> bool:
    """
    Schedule one speed test at the given HH:MM:SS time today.
    Returns True if successfully scheduled, False otherwise.
    """
    timestamp = _parse_time_to_timestamp(time_str)
    if timestamp is None:
        return False

    print(f"[requester] Test scheduled for {datetime.fromtimestamp(timestamp)}")
    scheduler.enterabs(timestamp, 1, main_func, ())
    scheduler.run()
    return True


# ── Data query pass-throughs ─────────────────────────────────────────────────

def return_reading(date: str)  -> list: return process_data.db_return_reading(date)
def return_all()               -> list: return process_data.db_return_all()
def return_by_download()       -> list: return process_data.db_return_by_download()
def return_by_upload()         -> list: return process_data.db_return_by_upload()
