from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaProducer
import json
import os
from app.data import write_log_data

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Kafka Producerの設定
producer = KafkaProducer(
    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
)

@app.post("/send-event/kafka")
async def send_event_kaka(event_data: dict):
    try:
        # イベントをKafkaに送信
        producer.send('events', value=event_data)
        return {"status": "success", "message": "Event sent to Kafka"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/send-event/direct")
async def send_event_direct(event_data: dict):
    try:
        # イベントをKafkaに送信
        write_log_data(
            event_type=event_data.get("type", "unknown"), 
            event_data=event_data.get("data", "unknown"),    
            source="direct"
        )
        return {"status": "success", "message": "Event sent to Kafka"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}