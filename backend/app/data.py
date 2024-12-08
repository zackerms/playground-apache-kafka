import os
import csv
import datetime
import time

def write_log_data(event_type, event_data, source):
    time.sleep(0.001)  # 大規模ログが書き込まれている想定 
    log_file_path = os.path.join("logs", "events.csv") 
    if not os.path.exists(log_file_path):
        with open(log_file_path, mode='w') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "type", "data", "source"])

    # ログファイルに書き込み
    with open(log_file_path, mode='a') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.datetime.now().isoformat(),
            event_type,
            event_data,
            source
        ])