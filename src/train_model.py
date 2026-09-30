import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

print("1. Membaca dataset untuk pelatihan (mengambil 100.000 baris pertama agar ringan)...")
df = pd.read_csv('../data/raw/transactions.csv', nrows=100000)

print("2. Menyiapkan Fitur (Feature Engineering)...")
X = df[['amount', 'oldbalanceOrg', 'newbalanceOrig']]
y = df['isFraud']

print("3. Melatih model Random Forest Classifier...")
# n_estimators=50 agar proses training cepat namun akurat
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X, y)

print("4. Menyimpan model ke dalam file...")
joblib.dump(model, 'fraud_model.pkl')
print("Model sukses disimpan sebagai 'fraud_model.pkl'!")