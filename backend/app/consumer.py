from kafka import KafkaConsumer
import json
import os
import csv
import datetime
import time

def start_consumer():
    consumer = KafkaConsumer(
        'events',
        bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='event_consumer_group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        # ここでイベントの処理を実装: ログ出力
        try:
            print(f"Received message: {message.value}")
            # ファイルがない場合は新規作成
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
                    message.value.get("type", "unknown"),
                    message.value.get("data", "unknown")
                ])
        except Exception as e:
            print(f"Error processing message: {e}")

if __name__ == "__main__":
    print("Starting consumer...")
    # 常にConsumerを起動し続ける
    while True:
        try:
            start_consumer()
        except Exception as e:
            time.sleep(5)