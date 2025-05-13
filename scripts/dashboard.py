# scripts/dashboard.py
import pandas as pd
import streamlit as st
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os
import json

st.set_page_config(page_title="ABAC ML Dashboard", layout="wide")

# Load data and model
df = pd.read_csv("data/access_logs_enriched.csv")
df["cookieEnabled"] = df["cookieEnabled"].astype(int)
df["headlessDetected"] = df["headlessDetected"].astype(int)

model = joblib.load("models/rf_model.pkl")
features = ["requestCount", "cookieEnabled", "headlessDetected"]
X = df[features]
y_true = df["label"]
y_pred = model.predict(X)
df["decision"] = ["BLOCK" if p == 1 else "ALLOW" for p in y_pred]

# Load recent live log entry if available
latest_decision = None
live_path = "data/live_requests.json"
if os.path.exists(live_path):
    with open(live_path, "r") as f:
        live_log = json.load(f)
    if live_log:
        latest = sorted(live_log, key=lambda x: x["timestamp"], reverse=True)[0]
        latest_decision = f"🔔 Last Live Access: {latest['decision']} | Count: {latest['input']['requestCount']} | Cookie: {latest['input']['cookieEnabled']} | Headless: {latest['input']['headlessDetected']}"

# Metrics
st.title("ABAC ML Access Control Dashboard")

if latest_decision:
    st.success(latest_decision)

col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 Label Distribution (Ground Truth)")
    st.bar_chart(df["label"].value_counts())

with col2:
    st.subheader("🚦 Model Decisions")
    st.bar_chart(df["decision"].value_counts())

st.subheader("🧠 Classification Report")
report = classification_report(y_true, y_pred, output_dict=True)
st.dataframe(pd.DataFrame(report).transpose())

st.subheader("🔁 Confusion Matrix")
cm = confusion_matrix(y_true, y_pred)
st.write("Rows = Actual, Columns = Predicted")
st.dataframe(pd.DataFrame(cm, columns=["Pred: Normal", "Pred: Bot"], index=["Actual: Normal", "Actual: Bot"]))

st.subheader("📈 Avg Request Count by Label")
st.bar_chart(df.groupby("label")["requestCount"].mean())

st.subheader("🕵️‍♀️ Headless Browser Use")
st.bar_chart(df["headlessDetected"].value_counts())

st.subheader("🔍 Referrers")
st.dataframe(df["referrer"].value_counts())

st.subheader("🕑 Requests by Hour")
df["requestHour"] = pd.to_datetime(df["timestamp"]).dt.hour
st.bar_chart(df["requestHour"].value_counts().sort_index())

# Display live policy evolution log if available
st.subheader("📜 Policy Evolution Log")
log_path = "data/abac_policy_log.json"
if os.path.exists(log_path):
    with open(log_path, "r") as f:
        policy_log = json.load(f)
    for entry in policy_log:
        st.markdown(f"**Timestamp:** {entry['timestamp']}")
        st.json({"Before": entry['previous_policy'], "After": entry['updated_policy']})
else:
    st.info("No policy evolution log found.")

# Live request log from CLI tool
st.subheader("📡 Live CLI Access Attempts")
if os.path.exists(live_path):
    with open(live_path, "r") as f:
        live_log = json.load(f)
    if live_log:
        df_live = pd.DataFrame(live_log)
        st.dataframe(df_live.sort_values(by="timestamp", ascending=False))
    else:
        st.info("Waiting for access attempts from CLI...")
else:
    st.warning("No live request log file found.")