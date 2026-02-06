import csv
from datetime import datetime
from pathlib import Path

# -------- CONFIG --------
LINE_Y = 300

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

CSV_PATH = DATA_DIR / "counts.csv"

# -------- STATE --------
previous_positions = {}
counted_ids = set()

in_count = 0
out_count = 0


def log_event(event):
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), event])


def process_counting(track_id, center_y):
    global in_count, out_count

    if track_id not in previous_positions:
        previous_positions[track_id] = center_y
        return

    prev_y = previous_positions[track_id]

    # TOP → BOTTOM
    if prev_y < LINE_Y and center_y > LINE_Y and track_id not in counted_ids:
        in_count += 1
        counted_ids.add(track_id)
        log_event("IN")
        print(f"[INFO] ID {track_id} ENTERED")

    # BOTTOM → TOP
    elif prev_y > LINE_Y and center_y < LINE_Y and track_id not in counted_ids:
        out_count += 1
        counted_ids.add(track_id)
        log_event("OUT")
        print(f"[INFO] ID {track_id} EXITED")

    previous_positions[track_id] = center_y
