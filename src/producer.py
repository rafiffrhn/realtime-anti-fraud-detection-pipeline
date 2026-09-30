import pandas as pd
from kafka import KafkaProducer
import json
import time

print("1. Menginisialisasi Kafka Producer...")
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic_name = 'financial_transactions'

print("2. Membaca dataset mentah (PaySim)...")
df = pd.read_csv('D:/PROJECT/realtime-fraud-detection-pipeline/data/raw/transactions.csv')

print(f"3. Memulai simulasi streaming Real-Time ke topik '{topic_name}'...")
for index, row in df.iterrows():
    transaction = row.to_dict()
 
    producer.send(topic_name, value=transaction)
    
    if index % 1000 == 0:
        print(f"Terkirim: {index} transaksi ke Kafka...")

    time.sleep(0.05)