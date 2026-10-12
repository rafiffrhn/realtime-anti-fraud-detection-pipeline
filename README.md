# Enterprise-Grade Real-Time Financial Fraud Detection Pipeline

## Executive Summary
This project is an enterprise-scale, end-to-end Big Data streaming architecture designed to detect financial anomalies and fraud (such as Account Takeovers and Smurfing/Money Laundering) in real-time. Utilizing the **PaySim** dataset (simulating millions of mobile money transactions), this system implements **Apache Kafka** as the high-speed message delivery backbone and a **Random Forest Classifier** within a microservice architecture to perform real-time inference with millisecond latency.

This project demonstrates a seamless integration between **Data Engineering** (architecting streaming data pipelines) and **Data Science** (training and deploying Machine Learning models into a live production environment).

---

## System Architecture & Data Flow

The system architecture is built on an Event-Driven Architecture (EDA) approach, divided into three primary phases:

1. **Data Ingestion (Producer):** he `producer.py` script reads the raw dataset, serializes each transaction log row into a JSON payload, and publishes it into the message broker at an adjustable speed to simulate live customer traffic.
2. **Message Broker (Apache Kafka & Zookeeper):** Hosted within Docker containers, Kafka receives and queues millions of JSON payloads in the `financial_transactions` topic without encountering data bottlenecks.
3. **Stream Processing & ML Inference (Consumer):** The `consumer.py` script acts as an independent microservice that actively listens to the Kafka topic. It extracts features on-the-fly and feeds them into the Machine Learning model (`fraud_model.pkl`) to predict the probability of fraud at the exact moment the transaction occurs.

---

## Technology Stack

**Data Engineering / Infrastructure:**
- **Apache Kafka:** Distributed event streaming platform.
- **Apache Zookeeper:** Centralized service for maintaining configuration information.
- **Docker & Docker Compose:** Containerization & infrastructure orchestration.
- **Python (`kafka-python`):** Producer & Consumer interface scripts.

**Machine Learning / Data Science:**
- **Scikit-Learn:** Building and training the Random Forest Classifier.
- **Pandas:** Data manipulation and Feature Engineering (Amount, Old Balance, New Balance).
- **Joblib:** ML model serialization and storage (Pickling).

---

## Repository Structure

```text
├── data/
│   └── raw/
│       └── transactions.csv      # Raw PaySim dataset (not uploaded to Git)
├── src/
│   ├── producer.py               # Kafka Producer (Simulates incoming data)
│   ├── consumer.py               # Kafka Consumer (Real-time ML Inference)
│   ├── train_model.py            # ML model training script
│   └── fraud_model.pkl           # Compiled Random Forest model
├── docker-compose.yml            # Kafka & Zookeeper infrastructure config
└── README.md
```

## Machine Learning Model Details
- **Algorithm:** Random Forest Classifier (50 Estimators).
- **Feature Engineering:** The model is trained using three crucial numerical metrics representing asset movement: amount, oldbalanceOrg, and newbalanceOrig.
- **Fraud Patterns Detected:**
  1. **Account Takeover:** Identifies scenarios involving sudden and massive balance draining (CASH_OUT or TRANSFER leaving a 0 balance).
  2. **Smurfing / Money Laundering:** Identifies sequences of identical and unnatural transaction amounts designed to bypass traditional rule-based system limits.

## Installation & Execution Guide
1. **System Prerequisites**
   - Docker Desktop (dengan WSL 2 terinstalasi untuk pengguna Windows).
   - Python 3.8+
   - Minimal RAM 8GB (Direkomendasikan 16GB+).
     
2. **Environment Setup**
   - Clone the repository and navigate to the project directory:
   ```bash
    git clone https://github.com/rafiffrhn/realtime-anti-fraud-detection-pipeline.git
    cd realtime-anti-fraud-detection-pipeline
   ```
   - Install all required Python dependencies:
    ```bash
    python -m pip install pyspark kafka-python pandas scikit-learn joblib
   ```
   - Download the PaySim dataset (Synthetic Financial Datasets For Fraud Detection) from Kaggle. Extract and rename the file to transactions.csv, then place it inside the data/raw/ directory.
     
3. **Running the Big Data Infrastructure**
   - Start the Apache Kafka and Zookeeper cluster using Docker in detached mode:
   ```bash
    docker-compose up -d
   ```
  Ensure both containers are running in your Docker Desktop dashboard.
   
5. **ML Model Training**
   - Run this script if you wish to retrain the model with different parameters:
   ```bash
    cd src
    python train_model.py
   ```
   This will reprocess the data and update the fraud_model.pkl file.
   
6. **Starting the Real-Time Simulation**
   - Open the First Terminal and run the Producer service to start streaming transactions to the Kafka server:
   ```bash
    cd src
    python producer.py
   ```
   - Open a Second Terminal and activate the Machine Learning detection radar (Consumer):
   ```bash
    cd src
    python consumer.py
   ```
  The system is now running live. Every anomaly identified by the AI model will instantly trigger a 🚨 [AI FRAUD DETECTED] alert in the Consumer terminal in real-time.
   
7. **System Termination**
   - To safely shut down the pipeline and clear the Docker containers from memory, run:
    ```bash
    docker-compose down
   ```
