import csv
from datetime import datetime

LINE_Y = 300   # Adjust based on camera view

counted_ids = set()
previous_positions = {}

in_count = 0
out_count = 0


def log_event(event):
    with open("data/counts.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), event])


def process_counting(track_id, center_y):
    global in_count, out_count

    if track_id not in previous_positions:
        previous_positions[track_id] = center_y
        return

    prev_y = previous_positions[track_id]

    # Top → Bottom (IN)
    if prev_y < LINE_Y and center_y > LINE_Y and track_id not in counted_ids:
        in_count += 1
        counted_ids.add(track_id)
        log_event("IN")
        print(f"ID {track_id} entered")

    # Bottom → Top (OUT)
    elif prev_y > LINE_Y and center_y < LINE_Y and track_id not in counted_ids:
        out_count += 1
        counted_ids.add(track_id)
        log_event("OUT")
        print(f"ID {track_id} exited")

    previous_positions[track_id] = center_y
