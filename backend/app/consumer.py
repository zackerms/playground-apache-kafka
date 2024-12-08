from kafka import KafkaConsumer
import json
import os
import csv
import datetime
import time
from app.data import write_log_data

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
            write_log_data(
                event_type=message.value.get("type", "unknown"), 
                event_data=message.value.get("data", "unknown"),
                source=f"kafka-{message.partition}"
            )
        except Exception as e:
            print(f"Error processing message: {e}")

if __name__ == "__main__":
    print("Starting consumer...")
    # 常にConsumerを起動し続ける
    while True:
        try:
            start_consumer()
        except Exception as e:
            time.sleep(1000 * 0.1)
            pass