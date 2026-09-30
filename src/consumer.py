from kafka import KafkaConsumer
import json
import joblib
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

print("1. Memuat Model Machine Learning (Random Forest)...")
model = joblib.load('fraud_model.pkl')

print("2. Menghubungkan sistem deteksi ke server Kafka...")
consumer = KafkaConsumer(
    'financial_transactions',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("3. Radar AI Aktif! Menunggu aliran data transaksi...\n")
print("-" * 60)

for message in consumer:
    tx = message.value
    
    features = pd.DataFrame([{
        'amount': float(tx['amount']),
        'oldbalanceOrg': float(tx['oldbalanceOrg']),
        'newbalanceOrig': float(tx['newbalanceOrig'])
    }])
   
    # INFERENCE REAL-TIME
    prediction = model.predict(features)[0]
    
    if prediction == 1:
        print(f"🚨 [AI FRAUD DETECTED] 🚨")
        print(f"Status   : Model mengidentifikasi anomali transaksi!")
        print(f"Akun     : {tx['nameOrig']}")
        print(f"Tipe     : {tx['type']}")
        print(f"Nominal  : $ {float(tx['amount']):,.2f}")
        print("-" * 60)