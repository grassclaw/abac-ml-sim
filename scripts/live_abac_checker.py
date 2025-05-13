# scripts/live_abac_checker.py
from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load("models/rf_model.pkl")

@app.route("/abac_check", methods=["POST"])
def abac_check():
    data = request.json

    try:
        # Extract required features
        features = [
            int(data.get("requestCount", 0)),
            int(data.get("cookieEnabled", False)),
            int(data.get("headlessDetected", False))
        ]

        prediction = model.predict([features])[0]
        decision = "BLOCK" if prediction == 1 else "ALLOW"

        return jsonify({
            "decision": decision,
            "input": data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
