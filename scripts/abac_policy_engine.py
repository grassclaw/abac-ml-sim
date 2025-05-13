# scripts/abac_policy_engine.py (updated for policy evolution logging)
import pandas as pd
import joblib
import json
import os
from datetime import datetime

# Load data and model
df = pd.read_csv("data/access_logs_enriched.csv")
df["cookieEnabled"] = df["cookieEnabled"].astype(int)
df["headlessDetected"] = df["headlessDetected"].astype(int)

model = joblib.load("models/rf_model.pkl")
X = df[["requestCount", "cookieEnabled", "headlessDetected"]]
y_true = df["label"]
y_pred = model.predict(X)
df["decision"] = ["BLOCK" if p == 1 else "ALLOW" for p in y_pred]

# Define initial (static) ABAC policy
initial_policy = {
    "rule_id": "rule_001",
    "conditions": {
        "headlessDetected": True,
        "requestCount": "> 100"
    },
    "action": "BLOCK"
}

# Define enhanced policy based on new pattern
enhanced_policy = {
    "rule_id": "rule_002",
    "conditions": {
        "headlessDetected": True,
        "geoLocation": "CN"
    },
    "action": "BLOCK"
}

# Load or create policy log
policy_log_path = "data/abac_policy_log.json"
if os.path.exists(policy_log_path):
    with open(policy_log_path, "r") as f:
        policy_log = json.load(f)
else:
    policy_log = []

# Append old and new policy as a new evolution entry
policy_log.append({
    "timestamp": datetime.utcnow().isoformat(),
    "previous_policy": initial_policy,
    "updated_policy": enhanced_policy
})

# Write log
with open(policy_log_path, "w") as f:
    json.dump(policy_log, f, indent=2)

# Print decisions
for i, row in df.iterrows():
    decision = df.loc[i, "decision"]
    print(f"{row['timestamp']} | {row['userAgent']} | {row['geoLocation']} | Decision: {decision}")
