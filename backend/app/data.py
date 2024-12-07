import os
import csv
import datetime

def write_log_data(event_type, event_data):
    log_file_path = os.path.join("logs", "events.csv") 
    if not os.path.exists(log_file_path):
        with open(log_file_path, mode='w') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "type", "data"])

    # ログファイルに書き込み
    with open(log_file_path, mode='a') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.datetime.now().isoformat(),
            event_type,
            event_data,
        ])