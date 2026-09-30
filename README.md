# Enterprise-Grade Real-Time Financial Fraud Detection Pipeline

## Executive Summary
Proyek ini adalah arsitektur *Big Data streaming end-to-end* berskala *enterprise* yang dirancang untuk mendeteksi anomali dan penipuan finansial (seperti *Account Takeover* dan pencucian uang/*Smurfing*) secara *real-time*. Menggunakan dataset **PaySim** (simulasi jutaan transaksi *mobile money*), sistem ini mengimplementasikan **Apache Kafka** sebagai tulang punggung pengiriman pesan berkecepatan tinggi dan **Random Forest Classifier** pada arsitektur *microservice* untuk melakukan *real-time inference* dengan latensi tingkat milidetik.

Proyek ini mendemonstrasikan integrasi penuh antara **Data Engineering** (membangun *streaming data pipeline*) dan **Data Science** (melatih dan mengimplementasikan model *Machine Learning* ke dalam lingkungan produksi yang hidup).

---

## System Architecture & Data Flow

Arsitektur sistem dibangun menggunakan pendekatan *Event-Driven Architecture (EDA)* yang terbagi menjadi tiga fase utama:

1. **Data Ingestion (Producer):** Skrip `producer.py` membaca dataset mentah, melakukan serialisasi setiap baris log transaksi menjadi format JSON, dan menembakkannya (memublikasikan) ke dalam *message broker* dengan kecepatan yang dapat disesuaikan (mensimulasikan *traffic* nasabah *live*).
2. **Message Broker (Apache Kafka & Zookeeper):** Di- *hosting* di dalam *container* Docker, Kafka menerima dan menampung jutaan antrean *payload* JSON dalam *topic* `financial_transactions` tanpa mengalami *bottleneck*.
3. **Stream Processing & ML Inference (Consumer):** Skrip `consumer.py` bertindak sebagai layanan *microservice* independen yang mendengarkan *topic* Kafka secara *live*. Layanan ini mengekstrak fitur secara *on-the-fly* dan memasukkannya ke dalam model *Machine Learning* (`fraud_model.pkl`) untuk memprediksi probabilitas *fraud* di detik yang sama saat transaksi terjadi.

---

## Technology Stack

**Data Engineering / Infrastructure:**
- **Apache Kafka:** Distributed event streaming platform.
- **Apache Zookeeper:** Centralized service for maintaining configuration information.
- **Docker & Docker Compose:** Containerization & infrastructure orchestration.
- **Python (`kafka-python`):** Skrip antarmuka Producer & Consumer.

**Machine Learning / Data Science:**
- **Scikit-Learn:** Pembangunan dan pelatihan model *Random Forest Classifier*.
- **Pandas:** Manipulasi data dan *Feature Engineering* (Amount, Old Balance, New Balance).
- **Joblib:** Serialisasi dan penyimpanan model ML (*Pickling*).

---

## Repository Structure

```text
├── data/
│   └── raw/
│       └── transactions.csv      # Dataset mentah PaySim (tidak diunggah ke Git)
├── src/
│   ├── producer.py               # Kafka Producer (Simulasi data masuk)
│   ├── consumer.py               # Kafka Consumer (Real-time ML Inference)
│   ├── train_model.py            # Skrip pelatihan model ML
│   └── fraud_model.pkl           # Model Random Forest yang sudah dikompilasi
├── docker-compose.yml            # Konfigurasi infrastruktur Kafka & Zookeeper
└── README.md
```

## Machine Learning Model Details
- **Algorithm:** Random Forest Classifier (50 Estimators).
- **Feature Engineering:** Model dilatih menggunakan tiga metrik numerik krusial yang mewakili pergerakan aset: amount, oldbalanceOrg, dan newbalanceOrig.
- **Fraud Patterns Detected:**
  1. **Account Takeover:** Mengidentifikasi skenario pengurasan saldo masif secara tiba-tiba (CASH_OUT atau TRANSFER yang menyisakan saldo 0).
  2. **Smurfing / Money Laundering:** Mengidentifikasi rentetan transaksi bernominal identik dan tidak wajar yang memotong batasan logika sistem rule-based tradisional.

## Panduan Instalasi & Eksekusi
1. **Prasyarat Sistem**
   - Docker Desktop (dengan WSL 2 terinstalasi untuk pengguna Windows).
   - Python 3.8+
   - Minimal RAM 8GB (Direkomendasikan 16GB+).
     
2. **Persiapan Environment**
   - Clone repository dan masuk ke directory project:
   ```bash
    git clone https://github.com/rafiffrhn/realtime-anti-fraud-detection-pipeline.git
    cd realtime-anti-fraud-detection-pipeline
   ```
   - Instalasi seluruh dependensi python:
    ```bash
    python -m pip install pyspark kafka-python pandas scikit-learn joblib
   ```
   - Unduh dataset PaySim (Synthetic Financial Datasets For Fraud Detection) dari Kaggle. Ekstrak dan ubah nama file menjadi transactions.csv, lalu tempatkan di dalam direktori data/raw/.
     
3. **Menjalankan Infrastruktur Big Data**
   - Nyalakan cluster Apache Kafka dan Zookeeper menggunakan Docker secara detached:
   ```bash
    docker-compose up -d
   ```
   Pastikan kedua container berstatus *running* di dashboard Docker Desktop.
   
5. **Pelatihan Model ML**
   - Jalankan jika ingin melatih model dengan parameter yang berbeda:
   ```bash
    cd src
    python train_model.py
   ```
   Script ini akan memproses ulang data dan memperbarui *file* fraud_model.pkl
   
6. **Memulai Simulasi Real-Time**
   - Buka Terminal Pertama dan jalankan layanan Producer untuk mulai menembakkan aliran transaksi ke server Kafka:
   ```bash
    cd src
    python producer.py
   ```
   - Buka Terminal Kedua dan nyalakan radar deteksi berbasis Machine Learning:
   ```bash
    cd src
    python consumer.py
   ```
   Sistem sekarang berjalan secara live. Setiap anomali yang ditemukan oleh model AI akan langsung memicu peringatan 🚨 [AI FRAUD DETECTED] di terminal Consumer secara real-time.
   
7. **Terminasi Sistem**
   - Untuk mematikan pipeline secara aman dan membersihkan container Docker dari memori, jalankan:
    ```bash
    docker-compose down
   ```
