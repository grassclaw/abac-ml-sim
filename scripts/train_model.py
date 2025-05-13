# scripts/train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load enriched data
df = pd.read_csv("data/access_logs_enriched.csv")

# Feature selection
features = [
    "requestCount", 
    "cookieEnabled", 
    "headlessDetected"
]

# Encode categorical: geoLocation, authType, referrer (optional for now)
df["cookieEnabled"] = df["cookieEnabled"].astype(int)
df["headlessDetected"] = df["headlessDetected"].astype(int)

X = df[features]
y = df["label"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Save model
joblib.dump(clf, "models/rf_model.pkl")
print("[+] Model trained and saved to models/rf_model.pkl")
